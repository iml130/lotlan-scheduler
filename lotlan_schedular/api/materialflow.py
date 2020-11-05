import uuid
import networkx as nx
import matplotlib.pyplot as plt

from lotlan_schedular.api.event import Event
from lotlan_schedular.api.transportorder import TransportOrder

from lotlan_schedular.PetriNetGenerator import PetriNetState
from lotlan_schedular.PetriNetGenerator import PetriNetGenerator

from lotlan_schedular.defines import PetriNetConstants, LogicConstants


class MaterialFlow():
    def __init__(self, _uuid, lotlan_structure, tasks_in_mf, test_flag=False):
        self._uuid = _uuid
        self.name = ""
        self._is_running = True
        self.triggered_by_cb = []
        self.finished_by_cb = []
        self.next_to_cb = []
        self.task_finished_cb = []
        self.all_finished_cb = []
        self.tasks_in_mf = tasks_in_mf  # list of tasks in this material flow
        self.petri_net_generator = None
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
        self.petri_net_generator = PetriNetGenerator(tasks_in_mf, self.event_instances, test_flag=test_flag)

        self.initialize_tasks(self.tasks_in_mf)

        if tasks_in_mf:
            self.name = tasks_in_mf[0].name

        self.call_graph = self.create_call_graph(tasks_in_mf)

        cycles = list(nx.simple_cycles(self.call_graph))
        self.cycle_in_call_graph = len(cycles) > 0

        self.startable_tasks = self.find_startable_tasks(self.call_graph, tasks_in_mf)

        for instance in self.lotlan_structure.instances.values():
            if instance.template_name == "Event":
                self.event_instances[instance.name] = instance
        self.petri_net_generator.generate_task_nets()
        self.create_event_information_list()

    def is_running(self):
        return self._is_running

    def start(self):
        self.start_tasks(self.startable_tasks)

    def start_tasks(self, tasks):
        next_tos = []
        for i, task in enumerate(tasks):
            uuid = self.ids[task.name]
            if self.triggered_by_events[task.name]:
                self.petri_net_generator.awaited_events[task.name] = self.triggered_by_events[task.name]
                self.petri_net_generator.petri_net_state[task.name] = PetriNetState.wait_for_tb
                self.wait_for_triggered_by(uuid, self.triggered_by_events[task.name])
            else:
                self.petri_net_generator.awaited_events[task.name] = [Event("task_started", "", "Boolean", comparator="", value=True)]
                self.fire_event(uuid, Event(PetriNetConstants.TASK_STARTED_PLACE, "", "Boolean", comparator="", value=True))
                next_tos.append(task)

        self.next_to(next_tos)

    # create call graph for the onDone statements
    def create_call_graph(self, tasks):
        call_graph = nx.DiGraph()
        for task in tasks:
            call_graph.add_node(task.name)
            for child in task.on_done:
                call_graph.add_edge(task.name, child)
        return call_graph

    def save_call_graph_img(self, filename):
        nx.draw(self.call_graph, with_labels=True)
        plt.savefig(filename, dpi=300, bbox_inches='tight')

    # find tasks that can be started:
    # a task with no incoming edges in graph
    def find_startable_tasks(self, graph, tasks):
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

    # fire event to petri net corresponding to task of uuid
    def fire_event(self, _uuid, event):
        task = self.tasks[str(_uuid)]
        self.petri_net_generator.fire_event(task, event, self.on_petri_net_response)

    def initialize_tasks(self, tasks):
        for i, task in enumerate(tasks):
            if self.test_flag:
                _uuid = i
            else:
                _uuid = uuid.uuid4()
            self.tasks[str(_uuid)] = task
            self.ids[task.name] = _uuid
            self.tasks_done[task.name] = False
            self.not_done_parents[task.name] = 0

    # out of the event names create a list with
    # api event objects for control
    def create_event_information_list(self):
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

    # Petri net response
    def on_petri_net_response(self, msg, task):
        if msg == LogicConstants.TRIGGERED_BY_PASSED_MSG:
            self.next_to([task])
        elif msg == LogicConstants.TO_DONE_MSG:
            self.on_to_done(task)
        elif msg == LogicConstants.TASK_FINISHED_MSG:
            self.on_task_finished(task)

    def next_to(self, task_info):
        if task_info:
            transport_orders = {}
            for task in task_info:
                uid = self.ids[task.name]
                locations = {}
                for instance in self.lotlan_structure.instances.values():
                    if instance.template_name == "Location":
                        locations[instance.name] = instance
                to_api = TransportOrder.create_to(uid, task, self.event_instances, locations)
                transport_orders[uid] = to_api

                self.petri_net_generator.awaited_events[task.name] = [Event("to_done", "", "Boolean", comparator="", value=True)]
                self.petri_net_generator.petri_net_state[task.name] = PetriNetState.wait_for_to_done 

            for callback in self.next_to_cb:
                callback(self._uuid, transport_orders)

    def on_to_done(self, task_info):
        uid = self.ids[task_info.name]
        if self.finished_by_events[task_info.name]:
            self.petri_net_generator.awaited_events[task_info.name] = self.finished_by_events[task_info.name]
            self.petri_net_generator.petri_net_state[task_info.name] = PetriNetState.wait_for_fb
            self.wait_for_finished_by(uid, self.finished_by_events[task_info.name])

    def on_task_finished(self, task_info):
        uid = self.ids[task_info.name]
        self.task_finished(uid)
        self.tasks_done[task_info.name] = True

        self.petri_net_generator.awaited_events[task_info.name] = [None]

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
        if self.cycle_in_call_graph is False:
            for task_done in self.tasks_done.values():
                if task_done is False:
                    return False
            return True
        return False

    def wait_for_triggered_by(self, _uuid, event_information):
        for callback in self.triggered_by_cb:
            callback(self._uuid, _uuid, event_information)

    def wait_for_finished_by(self, _uuid, event_information):
        for callback in self.finished_by_cb:
            callback(self._uuid, _uuid,  event_information)

    def task_finished(self, _uuid):
        for callback in self.task_finished_cb:
            callback(self._uuid, _uuid)

    def all_finished(self):
        for callback in self.all_finished_cb:
            callback(self._uuid)

    def register_callback_triggered_by(self, callback):
        if callback not in self.triggered_by_cb:
            self.triggered_by_cb.append(callback)

    def register_callback_next_to(self, callback):
        if callback not in self.next_to_cb:
            self.next_to_cb.append(callback)

    def register_callback_finished_by(self, callback):
        if callback not in self.finished_by_cb:
            self.finished_by_cb.append(callback)

    def register_callback_task_finished(self, callback):
        if callback not in self.task_finished_cb:
            self.task_finished_cb.append(callback)

    def register_callback_all_finished(self, callback):
        if callback not in self.all_finished_cb:
            self.all_finished_cb.append(callback)
