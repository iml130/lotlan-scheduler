""" Contains Materialflow and MaterialFlowCallbacks class """

# standard libraries
import uuid
import networkx as nx
import matplotlib.pyplot as plt

# local sources
from lotlan_scheduler.api.event import Event
from lotlan_scheduler.api.transportorder import TransportOrder

from lotlan_scheduler.logger.sqlite_logger import SQLiteLogger

from lotlan_scheduler.petri_net.logic import PetriNetLogic

from lotlan_scheduler.petri_net.generator import PetriNetGenerator

# globals defines
from lotlan_scheduler.defines import PetriNetConstants, LogicConstants

class MaterialFlowCallbacks(object):
    """
        Contains lists of registered callback functions
        for different states in the scheduling process
    """
    def __init__(self):
        self.triggered_by_cb = []
        self.pickup_finished_cb = []
        self.delivery_finished_cb = []
        self.finished_by_cb = []
        self.next_to_cb = []
        self.task_finished_cb = []
        self.all_finished_cb = []

class MaterialFlow():
    """ Represents an abstract materialflow """

    def __init__(self, _uuid, lotlan_structure, lotlan_string, tasks_in_mf, test_flag=False):
        self._uuid = _uuid
        self.name = ""
        self._is_running = True
        self.materialflow_callbacks = MaterialFlowCallbacks()
        self.tasks_in_mf = tasks_in_mf
        self.lotlan_structure = lotlan_structure
        self.tasks = {}
        self.ids = {}
        self.triggered_by_events = {}
        self.finished_by_events = {}
        self.event_instances = {}
        self.not_done_parents = {}  # 0 if all parent tasks are done
        self.tasks_done = {}
        self.test_flag = test_flag
        self.parent_count = {}
        self.lotlan_string = lotlan_string
        self.petri_net_generator = PetriNetGenerator(tasks_in_mf,
                                                     self.event_instances,
                                                     test_flag=test_flag)
        self.logger = None
        self.call_graph = None
        self.startable_tasks = None
        self.cycle_in_call_graph = None
        self.petri_net_logic = None

    def is_running(self):
        return self._is_running

    def start(self):
        """
            Starts the materialflow scheduling
        """
        self.logger = SQLiteLogger()
        self.logger.insert_materialflow_in_sql(self._uuid, self.lotlan_string)

        self.initialize_tasks(self.tasks_in_mf)

        if self.tasks_in_mf:
            self.name = self.tasks_in_mf[0].name

        self.call_graph = self.create_call_graph(self.tasks_in_mf)

        cycles = list(nx.simple_cycles(self.call_graph))
        self.cycle_in_call_graph = len(cycles) > 0

        self.startable_tasks = self.find_startable_tasks(self.call_graph, self.tasks_in_mf)

        for instance in self.lotlan_structure.instances.values():
            if instance.template_name == "Event":
                self.event_instances[instance.name] = instance
        task_representations = self.petri_net_generator.generate_task_nets()
        self.petri_net_logic = PetriNetLogic(task_representations, self.test_flag)

        self.create_event_information_list()
        self.start_tasks(self.startable_tasks)

    def start_tasks(self, tasks):
        """
            Starts scheduling of the given tasks

            if a task has a triggeredBy statement it waits for incoming events
            otherwise the transport_order can be executed and so next_to is called
        """
        next_tos = []
        for task in tasks:
            uuid_ = self.ids[task.name]
            transport_order = task.transport_order
            pickup = transport_order.pickup_tos.location
            delivery = transport_order.delivery_tos.location

            transport_order.state = TransportOrder.TransportOrderState.TASK_STARTED
            state = transport_order.state
            self.logger.insert_transport_order(self._uuid, uuid_, state, pickup, delivery)

            if self.triggered_by_events[task.name]:
                tb_events_of_task = self.triggered_by_events[task.name]
                self.petri_net_logic.set_awaited_events(task, tb_events_of_task)

                self.wait_for_triggered_by(uuid_, self.triggered_by_events[task.name])

                transport_order.state = TransportOrder.TransportOrderState.TASK_WAIT_FOR_TRIGGERED_BY
                state = transport_order.state
                self.logger.insert_transport_order(self._uuid, uuid_, state, pickup, delivery)
            else:
                task_started_event = Event(PetriNetConstants.TASK_STARTED_PLACE, "", "Boolean",
                                           comparator="", value=True)
                self.petri_net_logic.set_awaited_events(task, [task_started_event])
                self.fire_event(uuid_, task_started_event)
                next_tos.append(task)

        self.next_to(next_tos)

    def create_call_graph(self, tasks):
        """
            Creates a graph where every node is a task
            and a directed edge represents an onDone
        """
        call_graph = nx.DiGraph()
        for task in tasks:
            call_graph.add_node(task.name)
            for child in task.on_done:
                call_graph.add_edge(task.name, child)
        return call_graph

    def save_call_graph_img(self, filename):
        """ Saves the generated call graph of the materialflow as image """
        nx.draw(self.call_graph, with_labels=True)
        plt.savefig(filename, dpi=300, bbox_inches="tight")

    def find_startable_tasks(self, graph, tasks):
        """
            Finds tasks that can be started:
            task with no incoming edges in graph
        """
        startable_tasks = []
        for task in tasks:
            incoming_edges = 0
            for u, v in graph.in_edges(task.name):
                # ignore self loops
                if u != v:
                    incoming_edges = incoming_edges + 1
                else:
                    self.not_done_parents[task.name] = 1
            self.not_done_parents[task.name] = self.not_done_parents[task.name] + incoming_edges
            self.parent_count[task.name] = self.not_done_parents[task.name]
            if incoming_edges == 0:
                startable_tasks.append(task)

        return startable_tasks

    def fire_event(self, uuid_, event):
        """ Fires event to petri net corresponding to task of uuid """
        task = self.tasks[str(uuid_)]
        self.petri_net_logic.fire_event(task, event, self.on_petri_net_response)

    def initialize_tasks(self, tasks):
        """ Adds information for api classes to tasks and init dicts """
        for i, task in enumerate(tasks):
            if self.test_flag:
                uuid_ = i
            else:
                uuid_ = uuid.uuid4()
            self.tasks[str(uuid_)] = task
            self.ids[task.name] = uuid_
            self.tasks_done[task.name] = False
            self.not_done_parents[task.name] = 0

            transport_order = task.transport_order
            transport_order.uuid = uuid_
            pickup_tos = transport_order.pickup_tos
            delivery_tos = transport_order.delivery_tos

            for instance in self.lotlan_structure.instances.values():
                if instance.template_name == "Location":
                    if pickup_tos.location.logical_name == instance.name:
                        pickup_tos.location.physical_name = instance.keyval["name"]
                        pickup_tos.location.location_type = instance.keyval["type"]
                    elif delivery_tos.location.logical_name == instance.name:
                        delivery_tos.location.physical_name = instance.keyval["name"]
                        delivery_tos.location.location_type = instance.keyval["type"]

    def create_event_information_list(self):
        """ Creates a list of events objects out of the event names """
        for task in self.tasks_in_mf:
            triggered_by = []
            for event_name in task.triggered_by_events:
                logical_name = self.event_instances[event_name].name
                physical_name = self.event_instances[event_name].keyval["name"]
                event_type = self.event_instances[event_name].keyval["type"]
                triggered_by.append(Event(logical_name, physical_name, event_type, None, None))
            self.triggered_by_events[task.name] = triggered_by

            finished_by = []
            for event_name in task.finished_by_events:
                logical_name = self.event_instances[event_name].name
                physical_name = self.event_instances[event_name].keyval["name"]
                event_type = self.event_instances[event_name].keyval["type"]
                finished_by.append(Event(logical_name, physical_name, event_type, None, None))
            self.finished_by_events[task.name] = finished_by

    def on_petri_net_response(self, msg, task):
        """
            Handles incoming messages from the petri net logic and
            calls corresponding methods
        """
        if msg == LogicConstants.TRIGGERED_BY_PASSED_MSG:
            self.next_to([task])
        elif msg == LogicConstants.TOS_TB_PASSED_MSG:
            self.on_tos_tb_passed(task)
        elif msg == LogicConstants.TOS_WAIT_FOR_ACTION:
            self.on_tos_wait_for_action(task)
        elif msg == LogicConstants.TOS_FINISHED_MSG:
            self.on_tos_finished(task)
        elif msg == LogicConstants.TO_DONE_MSG:
            self.on_to_done(task)
        elif msg == LogicConstants.TASK_FINISHED_MSG:
            self.on_task_finished(task)

    def next_to(self, task_info):
        """ Notifies listeners about the next transport orders and set petri net state """
        if task_info:
            transport_orders = {}
            for task in task_info:
                uid = self.ids[task.name]

                transport_order = task.transport_order
                task.transport_order.state = TransportOrder.TransportOrderState.PICKUP_STARTED
                transport_orders[uid] = transport_order

                to_done_event = Event("to_done", "", "Boolean",
                                      comparator="", value=True)

                self.petri_net_logic.set_awaited_events(task, [to_done_event])

                self.start_tos(task, transport_order.pickup_tos)

            for callback in self.materialflow_callbacks.next_to_cb:
                callback(self._uuid, transport_orders)

    def start_tos(self, task, tos, pickup=True):
        """ Starts scheduling of the given TransportOrderStep """
        if tos.triggered_by:
            self.petri_net_logic.set_awaited_events(task, tos.triggered_by)

            if pickup:
                task.transport_order.state = TransportOrder.TransportOrderState.PICKUP_WAIT_FOR_TRIGGERED_BY
            else:
                task.transport_order.state = TransportOrder.TransportOrderState.DELIVERY_WAIT_FOR_TRIGGERED_BY
            
            uid = self.ids[task.name]
            self.log_transport_order(uid, task.transport_order)
        else:
            tos_started_event = Event(PetriNetConstants.TOS_STARTED_PLACE, "", "Boolean", value=True)
            tos_done_event = Event(PetriNetConstants.TOS_MOVED_TO_LOCATION_PLACE, "", "Boolean", True)
            self.petri_net_logic.set_awaited_events(task, [tos_started_event, tos_done_event])
            self.petri_net_logic.fire_event(task, tos_started_event)

    def on_tos_tb_passed(self, task):
        """
            Gets called when a TriggeredBy is passed in a TransportOrderStep net.
            Set the petr net state and set new awaited event "moved_to_location" for
            either the Pickup Net or the Delivery net depending on the current state
        """
        current_state = task.transport_order.state
        uid = self.ids[task.name]
        transport_order = task.transport_order

        # check the current state and set the new one
        if current_state == TransportOrder.TransportOrderState.PICKUP_WAIT_FOR_TRIGGERED_BY:
            task.transport_order.state = TransportOrder.TransportOrderState.PICKUP_STARTED
        elif current_state == TransportOrder.TransportOrderState.DELIVERY_WAIT_FOR_TRIGGERED_BY:
            task.transport_order.state = TransportOrder.TransportOrderState.DELIVERY_STARTED

        self.log_transport_order(uid, transport_order)

        moved_to_locaction_event = Event("moved_to_location", "", "Boolean", value=True)
        self.petri_net_logic.set_awaited_events(task, [moved_to_locaction_event])

    def on_tos_wait_for_action(self, task):
        """ 
            Gets called when the AGV has moved to the Location.
            Set the petri net state and set FinishedBy events as awaited events.
        """
        current_state = task.transport_order.state
        tos = None
        uid = self.ids[task.name]
        transport_order = task.transport_order

        # check the current state and set the new one
        if current_state == TransportOrder.TransportOrderState.PICKUP_STARTED:
            task.transport_order.state = TransportOrder.TransportOrderState.WAIT_FOR_LOADING
            tos = task.transport_order.pickup_tos
        elif current_state == TransportOrder.TransportOrderState.DELIVERY_STARTED:
            task.transport_order.state = TransportOrder.TransportOrderState.WAIT_FOR_UNLOADING
            tos = task.transport_order.delivery_tos
        else:
            print("Something went wrong!")

        self.log_transport_order(uid, transport_order)

        self.petri_net_logic.set_awaited_events(task, tos.finished_by)

    def on_tos_finished(self, task):
        """
            Gets called when a TransportOrderStep is done.
            Set the petri net state and either call on_pickup_finished method
            or on_delivery_finished method depending on the current state
        """
        current_state = task.transport_order.state
        uid = self.ids[task.name]
        transport_order = task.transport_order

        # check the current state and set the new one
        if current_state == TransportOrder.TransportOrderState.WAIT_FOR_LOADING:
            task.transport_order.state = TransportOrder.TransportOrderState.PICKUP_FINISHED
            self.log_transport_order(uid, transport_order)
            self.on_pickup_finished(task)
        elif current_state == TransportOrder.TransportOrderState.WAIT_FOR_UNLOADING:
            task.transport_order.state = TransportOrder.TransportOrderState.DELIVERY_FINISHED
            self.log_transport_order(uid, transport_order)
            self.on_delivery_finished(task)
        else:
            print("Something went wrong!")

    def on_pickup_finished(self, task):
        """
            Gets called when the Pickup TransportOrderStep is finished.
            Set petri net state and start Delivery TransportOrderStep
        """
        self.pickup_finished(self.ids[task.name])

        task.transport_order.state = TransportOrder.TransportOrderState.DELIVERY_STARTED
        self.start_tos(task, task.transport_order.delivery_tos, False)

    def on_delivery_finished(self, task):
        """
            Gets called when the Delivery TransportOrderStep is finished.
            Set petri net state and fire the to_done event to the task net
        """
        self.delivery_finished(self.ids[task.name])

        to_done_event = Event("to_done", "", "Boolean", value=True) 
        self.petri_net_logic.set_awaited_events(task, [to_done_event])
        self.petri_net_logic.fire_event(task, to_done_event, self.on_petri_net_response)

    def on_to_done(self, task_info):
        """
            Gets called when transport order is done by the AGV.
            Set petri net state (wait for possible FinishedBy events)
        """
        uid = self.ids[task_info.name]
        if self.finished_by_events[task_info.name]:
            transport_order = task_info.transport_order
            transport_order.state = TransportOrder.TransportOrderState.TASK_WAIT_FOR_FINISHED_BY
            self.log_transport_order(uid, transport_order)

            finished_by_events = self.finished_by_events[task_info.name]
            self.petri_net_logic.set_awaited_events(task_info, finished_by_events)
            self.wait_for_finished_by(uid, self.finished_by_events[task_info.name])

    def on_task_finished(self, task_info):
        """
            Gets called when task is finished.
            Starts possible onDone tasks and set petri net state
        """
        uid = self.ids[task_info.name]
        self.task_finished(uid)
        self.tasks_done[task_info.name] = True

        self.petri_net_logic.set_awaited_events(task_info, [None])
        task_info.transport_order.state = TransportOrder.TransportOrderState.FINISHED
        self.log_transport_order(uid, task_info.transport_order)

        if task_info.on_done:
            startable_tasks = []
            for task in task_info.on_done:
                self.not_done_parents[task] = self.not_done_parents[task] - 1

                # all parent tasks are done start the task
                if self.not_done_parents[task] == 0:
                    task_key = self.tasks[str(self.ids[task])]
                    startable_tasks.append(task_key)
                    self.not_done_parents[task_key.name] = self.parent_count[task_key.name]

            self.start_tasks(startable_tasks)
        elif self.all_tasks_done():
            self._is_running = False
            self.all_finished()

    def all_tasks_done(self):
        """
            Returns true if all tasks are done
        """
        if self.cycle_in_call_graph is False:
            for task_done in self.tasks_done.values():
                if task_done is False:
                    return False
            return True
        return False

    def log_transport_order(self, to_uuid, transport_order):
        """
            Saves the given TransportOrder with its locations in the db 
            by calling insert method of the logger
        """
        pickup_location = transport_order.pickup_tos.location
        delivery_location = transport_order.delivery_tos.location
        self.logger.insert_transport_order(self._uuid, to_uuid, transport_order.state,
                                           pickup_location, delivery_location)

    def wait_for_triggered_by(self, uuid_, event_information):
        for callback in self.materialflow_callbacks.triggered_by_cb:
            callback(self._uuid, uuid_, event_information)

    def wait_for_finished_by(self, uuid_, event_information):
        for callback in self.materialflow_callbacks.finished_by_cb:
            callback(self._uuid, uuid_,  event_information)

    def task_finished(self, uuid_):
        for callback in self.materialflow_callbacks.task_finished_cb:
            callback(self._uuid, uuid_)

    def all_finished(self):
        for callback in self.materialflow_callbacks.all_finished_cb:
            callback(self._uuid)

    def pickup_finished(self, uuid_):
        for callback in self.materialflow_callbacks.pickup_finished_cb:
            callback(self._uuid, uuid_)

    def delivery_finished(self, uuid_):
        for callback in self.materialflow_callbacks.delivery_finished_cb:
            callback(self._uuid, uuid_)

    def register_callback_triggered_by(self, callback):
        """
            If a Task can be started and has a TriggeredBy defined, all
            registered callback functions will be called
        """
        if callback not in self.materialflow_callbacks.triggered_by_cb:
            self.materialflow_callbacks.triggered_by_cb.append(callback)

    def register_callback_next_to(self, callback):
        """
            If a Task was started and the TriggeredBy condition is satisfied or there is
            no TriggeredBy all callback functions registered here will be called
        """
        if callback not in self.materialflow_callbacks.next_to_cb:
            self.materialflow_callbacks.next_to_cb.append(callback)

    def register_callback_finished_by(self, callback):
        """
            Functions passed in to this method will be called when the TransportOrder is done
            which means a "to_done" event was sent and a FinishedBy was defined
        """
        if callback not in self.materialflow_callbacks.finished_by_cb:
            self.materialflow_callbacks.finished_by_cb.append(callback)

    def register_callback_task_finished(self, callback):
        """
            If a Task is finished functions registered here are being called.
        """
        if callback not in self.materialflow_callbacks.task_finished_cb:
            self.materialflow_callbacks.task_finished_cb.append(callback)

    def register_callback_all_finished(self, callback):
        """
            If all Tasks in a Materialflow are finished functions registered here are being called
        """
        if callback not in self.materialflow_callbacks.all_finished_cb:
            self.materialflow_callbacks.all_finished_cb.append(callback)

    def register_callback_pickup_finished(self, callback):
        """
            Functions passed in to this method will be called when the Pickup TransportOrderStep
            of a task is finished
        """
        if callback not in self.materialflow_callbacks.pickup_finished_cb:
            self.materialflow_callbacks.pickup_finished_cb.append(callback)

    def register_callback_delivery_finished(self, callback):
        """
            Functions passed in to this method will be called when the Delivery TransportOrderStep
            of a task is finished
        """
        if callback not in self.materialflow_callbacks.delivery_finished_cb:
            self.materialflow_callbacks.delivery_finished_cb.append(callback)
