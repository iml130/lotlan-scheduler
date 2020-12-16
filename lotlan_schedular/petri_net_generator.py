""" Contains the PetriNetGenerator class """

# standard libraries
from enum import Enum

# 3rd party packages
import snakes.plugins as plugins

# local sources
from lotlan_schedular.petri_net_drawer import PetriNetDrawer
from lotlan_schedular.api.transportorder import TransportOrder
from lotlan_schedular.api.event import Event

# global defines
from lotlan_schedular.defines import PetriNetConstants, LogicConstants

plugins.load(["labels", "gv"], "snakes.nets", "nets")
from nets import PetriNet, Place, Transition, Inhibitor, Value, Marking

PICKUP_NET = 0
DELIVERY_NET = 1

class PetriNetGenerator:
    """
        Takes a lotlan file as argument and generates a Petri Net
        which visualizes the connection between tasks and transportordersteps.
        For each task there is a png file generated
    """

    def __init__(self, tasks, event_instances,
                 test_flag=False, simple_representation=False):
        self.petri_nets = []
        self.tos_petri_nets = {} # petri nets for the tos for each task
        self.tasks = tasks
        self.petri_net_drawer = PetriNetDrawer()
        self.simple_representation = simple_representation
        self.net_task_dict = {}
        self.triggered_by_passed = {}
        self.test_flag = test_flag
        self.awaited_events = {}
        self.transition_fired = {}
        self.event_dict = {}
        self.event_counter = 0
        self.event_instances = event_instances

    def generate_task_nets(self):
        """ generates a petri net for each task in tasks """
        for task in self.tasks:
            task_net, pickup_net, delivery_net = self.generate_task_net(task)
            self.petri_nets.append(task_net)
            self.tos_petri_nets[task.name] = []
            self.tos_petri_nets[task.name].append(pickup_net)
            self.tos_petri_nets[task.name].append(delivery_net)

            if self.test_flag:
                self.draw_petri_net(task.name, task_net)
                self.draw_petri_net(task.name + "_pickup", pickup_net)
                self.draw_petri_net(task.name + "_delivery", delivery_net)

            self.awaited_events[task.name] = []

            task.transport_order.state = PetriNet

            self.transition_fired[task.name] = {}
            for transition in task_net._trans:
                self.transition_fired[task.name][transition] = False
            for transition in pickup_net._trans:
                self.transition_fired[task.name][transition] = False
            for transition in delivery_net._trans:
                self.transition_fired[task.name][transition] = False

        return self.petri_nets

    def generate_task_net(self, task):
        """ 
            Generates a petri net the task and the TransportOrderSteps of the TransportOrders
            Returns generated nets (Task, Pickup, Delivery)
        """
        task_net = PetriNet(task.name)
        self.net_task_dict[task.name] = task_net

        self.event_dict[task.name] =  {}

        # generate task action
        self.generate_task_operation(task.name, task_net)

        # generate places and transitions for TriggeredBy
        task.triggered_by_events = self.generate_triggered_by(task, task_net)

        # generate places and transitions for FinishedBy
        task.finished_by_events = self.generate_finished_by(task, task_net)

        self.triggered_by_passed[task.name] = False

        pickup_tos = task.transport_order.pickup_tos
        delivery_tos = task.transport_order.delivery_tos

        pickup_net = self.generate_tos_net(task, pickup_tos, task.name + "_pickup")
        delivery_net = self.generate_tos_net(task, delivery_tos, task.name + "_delivery")

        return (task_net, pickup_net, delivery_net)

    def generate_tos_net(self, task, tos, name):
        tos_net = PetriNet(name)
        self.generate_advanced_tos_operation(tos_net)
        self.generate_triggered_by_for_tos(task, tos, tos_net)
        self.generate_finished_by_for_tos(task, tos, tos_net)
        return tos_net

    def generate_task_operation(self, task_name, net):
        if self.simple_representation is True:
            self.generate_simple_task_operation(task_name, net)
        else:
            self.generate_advanced_task_operation(net)

    def generate_simple_task_operation(self, task_name, net):
        create_place(task_name, "action", net)

    def generate_advanced_task_operation(self, net):
        """
            generates a advanced representation for a Task
            contrary to the simple representation this one has
            more places for each state in a Task
        """
        create_place(PetriNetConstants.TASK_STARTED_PLACE,
                     PetriNetConstants.TASK_STARTED_PLACE, net)
        create_place(PetriNetConstants.TASK_DONE_PLACE, PetriNetConstants.TASK_DONE_PLACE, net)
        create_place("to_done", "to_done", net)
        create_place("task_finished", "task_finished", net)

        create_transition(PetriNetConstants.TASK_FIRST_TRANSITION,
                               PetriNetConstants.TASK_FIRST_TRANSITION, net)
        create_transition(PetriNetConstants.TASK_SECOND_TRANSITION,
                               PetriNetConstants.TASK_SECOND_TRANSITION, net)

        net.add_input(PetriNetConstants.TASK_STARTED_PLACE,
                      PetriNetConstants.TASK_FIRST_TRANSITION, Value(1))
        net.add_output(PetriNetConstants.TASK_DONE_PLACE,
                       PetriNetConstants.TASK_FIRST_TRANSITION, Value(1))
        net.add_input("to_done", PetriNetConstants.TASK_FIRST_TRANSITION, Value(1))
        net.add_input(PetriNetConstants.TASK_DONE_PLACE,
                      PetriNetConstants.TASK_SECOND_TRANSITION, Value(1))
        net.add_output("task_finished", PetriNetConstants.TASK_SECOND_TRANSITION, Value(1))

    def generate_advanced_tos_operation(self, net):
        """
            generates a advanced representation for a TransportOrderStep
            contrary to the simple representation this one has
            more places for each state in a Task
        """
        create_place(PetriNetConstants.TOS_STARTED_PLACE,
                     PetriNetConstants.TOS_STARTED_PLACE, net)
        create_place(PetriNetConstants.TOS_MOVED_TO_LOCATION_PLACE, PetriNetConstants.TOS_MOVED_TO_LOCATION_PLACE, net)
        create_place(PetriNetConstants.TOS_WAIT_FOR_ACTION_PLACE, PetriNetConstants.TOS_WAIT_FOR_ACTION_PLACE, net)
        create_place(PetriNetConstants.TOS_FINISHED_PLACE, PetriNetConstants.TOS_FINISHED_PLACE, net)

        create_transition(PetriNetConstants.TOS_FIRST_TRANSITION,
                               PetriNetConstants.TOS_FIRST_TRANSITION, net)
        create_transition(PetriNetConstants.TOS_SECOND_TRANSITION,
                               PetriNetConstants.TOS_SECOND_TRANSITION, net)

        net.add_input(PetriNetConstants.TOS_STARTED_PLACE,
                      PetriNetConstants.TOS_FIRST_TRANSITION, Value(1))
        net.add_output(PetriNetConstants.TOS_WAIT_FOR_ACTION_PLACE,
                       PetriNetConstants.TOS_FIRST_TRANSITION, Value(1))
        net.add_input(PetriNetConstants.TOS_MOVED_TO_LOCATION_PLACE, PetriNetConstants.TOS_FIRST_TRANSITION, Value(1))
        net.add_input(PetriNetConstants.TOS_WAIT_FOR_ACTION_PLACE,
                      PetriNetConstants.TOS_SECOND_TRANSITION, Value(1))
        net.add_output(PetriNetConstants.TOS_FINISHED_PLACE, PetriNetConstants.TOS_SECOND_TRANSITION, Value(1))

    def draw_petri_net(self, name, petri_net):
        file_path = "./" + name + PetriNetConstants.IMAGE_ENDING
        self.petri_net_drawer.draw_image(petri_net, file_path)

    def generate_triggered_by(self, task, net):
        """
            generates places and transition from the TriggeredBy expression
        """
        triggered_by_event_names = []
        if task.triggered_by:
            create_transition(PetriNetConstants.TRIGGERED_BY_TRANSITION, "", net)

            if self.simple_representation is True:
                create_place(PetriNetConstants.TRIGGERED_BY, "", net)
                net.add_input(PetriNetConstants.TRIGGERED_BY,
                              PetriNetConstants.TRIGGERED_BY_TRANSITION, Value(1))
                net.add_output(PetriNetConstants.TASK_STARTED_PLACE,
                               PetriNetConstants.TRIGGERED_BY_TRANSITION, Value(1))
            else:
                self.generate_places_from_expression(task.triggered_by, task.name,
                                      PetriNetConstants.TRIGGERED_BY_TRANSITION,
                                      triggered_by_event_names,
                                      False,
                                      tb_event = True)
                net.add_output(PetriNetConstants.TASK_STARTED_PLACE,
                               PetriNetConstants.TRIGGERED_BY_TRANSITION, Value(1))
        return triggered_by_event_names

    def generate_triggered_by_for_tos(self, task, tos, net):
        tb_statement = tos.triggered_by_statements
        if tb_statement:
            create_transition(PetriNetConstants.TOS_TRIGGERED_BY_TRANSITION, "", net)
            self.generate_places_from_expression(tb_statement, task.name,
                                                PetriNetConstants.TOS_TRIGGERED_BY_TRANSITION,
                                                [],
                                                False,
                                                tb_event = True,
                                                tos_net=net)
            net.add_output(PetriNetConstants.TOS_STARTED_PLACE,
                        PetriNetConstants.TOS_TRIGGERED_BY_TRANSITION, Value(1))

    def generate_finished_by_for_tos(self, task, tos, net):
        fb_statement = tos.finished_by_statements
        if fb_statement:
            self.generate_places_from_expression(fb_statement, task.name,
                                                PetriNetConstants.TOS_SECOND_TRANSITION,
                                                [],
                                                False,
                                                tb_event = False,
                                                tos_net=net)

    def generate_finished_by(self, task, net):
        """
            generates places and transition from the FinishedBy expression
        """
        finished_by_event_names = []
        if self.simple_representation is True:
            create_place(PetriNetConstants.FINISHED_BY, "", net)
            net.add_input(PetriNetConstants.FINISHED_BY, PetriNetConstants.ON_DONE_ENDING,
                          Value(1))
        else:
            if task.finished_by != "":
                self.generate_places_from_expression(task.finished_by, task.name,
                                      PetriNetConstants.TASK_SECOND_TRANSITION,
                                      finished_by_event_names, False, tb_event=False)
        return finished_by_event_names

    def generate_places_from_expression(self, expression, task_name, parent_transition, event_name_list, parent_is_not, tb_event, comparator="", value=None, tos_net=None):
        """ extracts the single events from the expression and creates a place for each """

        net = None
        if tos_net is not None:
            net = tos_net
        else:
            net = self.net_task_dict[task_name]

        if isinstance(expression, str):
            # generate single node
            event_postfix = ""

            uuid_str = expression + "_" + str(self.event_counter)

            self.event_counter = self.event_counter + 1
            place_name = uuid_str + event_postfix

            event_type = self.event_instances[expression].keyval["type"]
            event = Event(expression, "", event_type, comparator=comparator, value=value)
            create_place(place_name, "", net, event=event, initialized=False)
            net.place(place_name).label(tb_event=tb_event)

            if expression not in self.event_dict[task_name]:
                self.event_dict[task_name][expression] = []
            self.event_dict[task_name][expression].append(uuid_str)

            event_name_list.append(expression)
            if parent_is_not is True:
                net.add_input(place_name, parent_transition, Inhibitor(Value(1)))
            else:
                net.add_input(place_name, parent_transition, Value(1))

            return expression + event_postfix

        elif isinstance(expression, dict):
            if len(expression) == 2:
                new_parent_is_not = parent_is_not is not True
                self.generate_places_from_expression(expression["value"], task_name,
                                                     parent_transition,
                                                     event_name_list,
                                                     new_parent_is_not, tb_event, tos_net=tos_net)
            elif len(expression) == 3:
                if expression["binOp"] == ".":
                    new_expression = str(expression["left"]) + "." + str(expression["right"])
                    self.generate_places_from_expression(new_expression, task_name, net,
                                                         parent_transition,
                                                         event_name_list,
                                                         parent_is_not, tb_event, tos_net=tos_net)
                # case: expr == <True|False>
                elif expression["right"] == "True":
                    if expression["binOp"] == "==":
                        self.generate_places_from_expression(expression["left"],
                                                             task_name, parent_transition,
                                                             event_name_list, False, tb_event, tos_net=tos_net)
                    elif expression["binOp"] == "!=":
                        self.generate_places_from_expression(expression["left"], task_name,
                                                             parent_transition,
                                                             event_name_list, True, tb_event, tos_net=tos_net)
                elif expression["right"] == "False":
                    if expression["binOp"] == "==":
                        self.generate_places_from_expression(expression["left"], task_name,
                                                             parent_transition,
                                                             event_name_list, True, tb_event, tos_net=tos_net)
                    elif expression["binOp"] == "!=":
                        self.generate_places_from_expression(expression["left"], task_name,
                                                             parent_transition,
                                                             event_name_list, False, tb_event, tos_net=tos_net)
                elif expression["left"] == "(" and expression["right"] == ")":
                    return self.generate_places_from_expression(expression["binOp"], task_name,
                                                                parent_transition,
                                                                event_name_list, parent_is_not,
                                                                tb_event, tos_net=tos_net)
                elif expression["binOp"] == "and" or expression["binOp"] == "or":
                    composition = str(expression)

                    if expression["binOp"] == "and":
                        create_place(composition + "_end", "and", net)
                        create_transition(composition + "_t", "", net)

                        self.generate_places_from_expression(expression["left"], task_name,
                                                             composition + "_t",
                                                             event_name_list, False, tb_event, tos_net=tos_net)
                        self.generate_places_from_expression(expression["right"], task_name,
                                                             composition + "_t",
                                                             event_name_list, False, tb_event, tos_net=tos_net)

                        net.add_output(composition + "_end", composition + "_t", Value(1))

                    elif expression["binOp"] == "or":
                        create_place(composition + "_end", "or", net)

                        create_transition(composition + "_t1", "", net)
                        create_transition(composition + "_t2", "", net)

                        net.add_output(composition + "_end", composition + "_t1", Value(1))
                        net.add_output(composition + "_end", composition + "_t2", Value(1))

                        self.generate_places_from_expression(expression["left"], task_name,
                                                             composition + "_t1",
                                                             event_name_list, False, tb_event, tos_net=tos_net)
                        self.generate_places_from_expression(expression["right"], task_name,
                                                             composition + "_t2",
                                                             event_name_list, False, tb_event, tos_net=tos_net)

                    if parent_is_not is True:
                        net.add_input(composition + "_end", parent_transition, Inhibitor(Value(1)))
                    else:
                        net.add_input(composition + "_end", parent_transition, Value(1))
                elif is_value(expression["right"]):
                    self.generate_places_from_expression(expression["left"], task_name,
                                                         parent_transition,
                                                         event_name_list, parent_is_not, tb_event,
                                                         expression["binOp"], expression["right"], tos_net=tos_net)

    def evaluate_petri_net(self, petri_net, task, cb=None):
        """ tries to fire every transition as long as all transitions
            were tried and nothing can be done anymore
        """
        index = 0
        work_to_do = False

        transitions = list(petri_net._trans)
        while index < len(petri_net._trans) or work_to_do:
            transition = transitions[index]
            transition_fired = False

            if self.transition_fired[task.name][transition] is False:
                input_arcs = petri_net.transition(transition).input()
                input_arcs_initialized = True
                for input_arc in input_arcs:
                    input_place = input_arc[0]
                    if input_place.label("initialized") is False:
                        input_arcs_initialized = False
                # only fire if all places are initialized
                if input_arcs_initialized:
                    try:
                        petri_net.transition(transition).fire(Value(1))
                        self.transition_fired[task.name][transition] = True
                        transition_fired = True
                    except ValueError:
                        transition_fired = False

            if transition_fired:
                work_to_do = self.handle_current_state(task, petri_net, transition, cb)

            index = index + 1

            # restart loop if every transition was iterated but
            # there is still work to do
            if index == len(petri_net._trans) and work_to_do:
                index = 0
                work_to_do = False

        if self.test_flag:
            self.draw_petri_net(petri_net.name, petri_net)

    def handle_current_state(self, task, petri_net, transition, cb):
        """
            transition: the transition which was passed
            checks which transition was passed and calls the given cb with the
            message of the corresponding state
            returns if evaulation is done so there is nothing more to do or if
            there is still work to do
        """
        work_to_do = False
        msg = ""

        if transition == PetriNetConstants.TRIGGERED_BY_TRANSITION:
            remove_all_tokens(petri_net)
            msg = LogicConstants.TRIGGERED_BY_PASSED_MSG

            self.triggered_by_passed[task.name] = True
            work_to_do = True
        elif transition == PetriNetConstants.TASK_FIRST_TRANSITION:
            msg = LogicConstants.TO_DONE_MSG
            work_to_do = True
        elif transition == PetriNetConstants.TASK_SECOND_TRANSITION:
            remove_all_tokens(petri_net)
            msg = LogicConstants.TASK_FINISHED_MSG
            
            # allow transition firing again to work with loops
            for trans in petri_net._trans:
                self.transition_fired[task.name][trans] = False
        elif transition == PetriNetConstants.TOS_TRIGGERED_BY_TRANSITION:
            msg = LogicConstants.TOS_TB_PASSED_MSG
        elif transition == PetriNetConstants.TOS_FIRST_TRANSITION:
            msg = LogicConstants.TOS_WAIT_FOR_ACTION
        elif transition == PetriNetConstants.TOS_SECOND_TRANSITION:
            msg = LogicConstants.TOS_FINISHED_MSG
            for trans in petri_net._trans:
                self.transition_fired[task.name][trans] = False
        else:
            work_to_do = True

        if cb is not None:
            cb(msg, task)

        return work_to_do

    def get_petri_net(self, task):
        petri_net = None
        current_state = task.transport_order.state

        if current_state in [TransportOrder.TransportOrderState.PICKUP_STARTED,
                             TransportOrder.TransportOrderState.PICKUP_WAIT_FOR_TRIGGERED_BY,
                             TransportOrder.TransportOrderState.WAIT_FOR_LOADING]:
            petri_net = self.tos_petri_nets[task.name][PICKUP_NET]
        elif current_state in [TransportOrder.TransportOrderState.DELIVERY_STARTED,
                               TransportOrder.TransportOrderState.DELIVERY_WAIT_FOR_TRIGGERED_BY,
                               TransportOrder.TransportOrderState.WAIT_FOR_UNLOADING]:
            petri_net = self.tos_petri_nets[task.name][DELIVERY_NET]
        else:
            petri_net = self.net_task_dict[task.name]

        return petri_net

    def fire_event(self, task, event, cb=None):
        """
            adds a token to the corresponding place of the event in the petri net
            checks before if event is expected and can be fired
        """

        petri_net = self.get_petri_net(task)

        is_awaited_event = False
        for evt in self.awaited_events[task.name]:
            if evt is not None and evt.logical_name == event.logical_name:
                is_awaited_event = True
        if is_awaited_event:
            if event.logical_name in self.event_dict[task.name]:
                for event_uuid in self.event_dict[task.name][event.logical_name]:
                    if petri_net.has_place(event_uuid):
                        current_state = task.transport_order.state
                        event_can_be_fired = can_be_fired(current_state, event_uuid, petri_net)

                        if event_can_be_fired:
                            petri_net.place(event_uuid).label(initialized=True)
                            if isinstance(event.value, bool):
                                if event.value is True:
                                    petri_net.place(event_uuid).add(1)
                                    self.draw_petri_net(petri_net.name, petri_net)
                                else:
                                    remove_token(petri_net, event_uuid)
                            elif is_value(event.value):
                                event_from_place = petri_net.place(event_uuid).label("event")
                                if parse_comparator_and_value(event_from_place, event):
                                    petri_net.place(event_uuid).add(1)
                                    self.draw_petri_net(petri_net.name, petri_net)
                                else:
                                    remove_token(petri_net, event_uuid)
            else:
                if event.value is True:
                    petri_net.place(event.logical_name).add(1)
                    self.draw_petri_net(petri_net.name, petri_net)
                else:
                    try:
                        petri_net.place(event.logical_name).remove(1)
                    except ValueError:
                        pass
            self.evaluate_petri_net(petri_net, task, cb)

def can_be_fired(current_state, event_uuid, petri_net):
    """
        checks if the given event can be fired:
        only works for tb and fb events
        Prevents setting a mark in tb when fb event with the same name is fired
    """
    tb_event = petri_net.place(event_uuid).label("tb_event")

    task_tb_state = TransportOrder.TransportOrderState.TASK_WAIT_FOR_TRIGGERED_BY
    task_fb_state = TransportOrder.TransportOrderState.TASK_WAIT_FOR_FINISHED_BY

    pickup_tb_state = TransportOrder.TransportOrderState.PICKUP_WAIT_FOR_TRIGGERED_BY
    pickup_fb_state = TransportOrder.TransportOrderState.WAIT_FOR_LOADING

    delivery_tb_state = TransportOrder.TransportOrderState.DELIVERY_WAIT_FOR_TRIGGERED_BY
    delivery_fb_state = TransportOrder.TransportOrderState.WAIT_FOR_UNLOADING

    if ((current_state == task_tb_state and tb_event) or
        (current_state == task_fb_state and not tb_event)):
        return True
    if ((current_state == pickup_tb_state and tb_event) or
        (current_state == pickup_fb_state and not tb_event)):
        return True
    if ((current_state == delivery_tb_state and tb_event) or
        (current_state == delivery_fb_state and not tb_event)):
        return True

    return False

def create_place(place_name, place_type, net, event = None, initialized = True):
    if net.has_place(place_name) is False:
        net.add_place(Place(place_name, []))
        net.place(place_name).label(placeType=place_type, event=event, initialized=initialized)

def create_transition(transition_name, transition_type, net):
    net.add_transition(Transition(transition_name))
    net.transition(transition_name).label(transitionType=transition_type)

def remove_token(petri_net, place_name):
    try:
        petri_net.place(place_name).remove(1)
    # there was no token so do nothing
    except ValueError:
        pass

def remove_all_tokens(net, task=True):
    if task:
        task_started_tokens = net.place(PetriNetConstants.TASK_STARTED_PLACE).tokens
        task_finished_tokens = net.place("task_finished").tokens
        net.set_marking(Marking(task_started = task_started_tokens,
                                task_finished=task_finished_tokens))
    else:
        tos_started_tokens = net.place(PetriNetConstants.TOS_STARTED_PLACE).tokens
        tos_finished_tokens = net.place(PetriNetConstants.TOS_FINISHED_PLACE).tokens
        net.set_marking(Marking(tos_started = tos_started_tokens,
                                tos_finished=tos_finished_tokens))

def parse_comparator_and_value(required_event, fired_event):
    """ If types of both events are the same execute
        given comparison with python operators
    """
    required_event_type = required_event.event_type
    fired_event_type = fired_event.event_type

    if required_event_type != fired_event_type:
        print("Something went wrong!")
    else:
        comparator = required_event.comparator
        given_value = cast_value(fired_event.value, required_event_type)
        required_value = cast_value(required_event.value, required_event_type)

        if required_event_type == "String":
            required_value = str.replace(required_value, '"', "")

        if comparator == ">":
            return given_value > required_value
        if comparator == "==":
            return given_value == required_value
        if comparator == ">=":
            return given_value >= required_value
        if comparator == "<":
            return given_value < required_value
        if comparator == "<=":
            return given_value <= required_value
        if comparator == "!=":
            return given_value != required_value
        print("Illegal comparator was defined!: " + comparator)
    return False

def is_value(x):
    return isinstance(x, (float, int, str))

def cast_value(value, requested_type):
    """Tries to cast the given value to the given type"""
    try:
        if requested_type == "Boolean":
            return value == "True"
        if requested_type == "Integer":
            return int(value)
        if requested_type == "Float":
            return float(value)
        return value
    except TypeError:
        print("Value doesnt match with given type")
