""" Contains the PetriNetGenerator class """

# 3rd party packages
import snakes.plugins as plugins

# local sources
import lotlan_scheduler.helpers as helpers

from lotlan_scheduler.petri_net.drawer import PetriNetDrawer
from lotlan_scheduler.api.transportorder import TransportOrder
from lotlan_scheduler.api.event import Event

# global defines
from lotlan_scheduler.defines import PetriNetConstants, LogicConstants

plugins.load(["labels", "gv"], "snakes.nets", "nets")
from nets import PetriNet, Place, Transition, Inhibitor, Value, Marking

class TaskRepresentation:
    """
        A representation of a LoTLan Task which contains
        all nessessary data for scheduling
    """
    def __init__(self):
        self.net = None
        self.pickup_net = None
        self.delivery_net = None
        self.awaited_events = []
        self.transition_fired = {}
        self.event_dict = {}

class PetriNetGenerator:
    """
        Takes a lotlan file as argument and generates a Petri Net
        which visualizes the connection between tasks and transportordersteps.
        For each task there is a png file generated
    """

    def __init__(self, tasks, event_instances,
                 test_flag=False, simple_representation=False):
        self.tasks = tasks
        self.petri_net_drawer = PetriNetDrawer()
        self.simple_representation = simple_representation
        self.test_flag = test_flag
        self.event_counter = 0
        self.net_task_dict = {}
        self.event_instances = event_instances
        self.task_representations = {}

    def generate_task_nets(self):
        """ Generates a petri net for each task in tasks """

        self.task_representations = {}
        for task in self.tasks:
            task_repr = TaskRepresentation()
            self.task_representations[task.name] = task_repr
            task_net, pickup_net, delivery_net = self.generate_task_net(task)
            task_repr.net = task_net
            task_repr.pickup_net = pickup_net
            task_repr.delivery_net = delivery_net

            if self.test_flag:
                self.draw_petri_net(task.name, task_net)
                self.draw_petri_net(task.name + "_pickup", pickup_net)
                self.draw_petri_net(task.name + "_delivery", delivery_net)

            for transition in task_net._trans:
                task_repr.transition_fired[transition] = False
            for transition in pickup_net._trans:
                task_repr.transition_fired[transition] = False
            for transition in delivery_net._trans:
                task_repr.transition_fired[transition] = False

        return self.task_representations

    def generate_task_net(self, task):
        """
            Generates a petri net for the task and the TransportOrderSteps of the TransportOrders
            Returns generated nets (Task, Pickup, Delivery)
        """
        task_net = PetriNet(task.name)
        self.net_task_dict[task.name] = task_net

        # generate task action
        self.generate_task_operation(task.name, task_net)

        # generate places and transitions for TriggeredBy
        task.triggered_by_events = self.generate_triggered_by(task, task_net)

        # generate places and transitions for FinishedBy
        task.finished_by_events = self.generate_finished_by(task, task_net)

        pickup_tos = task.transport_order.pickup_tos
        delivery_tos = task.transport_order.delivery_tos

        pickup_net = self.generate_tos_net(task, pickup_tos, task.name + "_pickup")
        delivery_net = self.generate_tos_net(task, delivery_tos, task.name + "_delivery")

        return (task_net, pickup_net, delivery_net)

    def generate_tos_net(self, task, tos, name):
        """
            Generates a petri net for the given TransportOrderStep
        """
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
            Generates a advanced representation for a Task
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
            Generates a advanced representation for a TransportOrderStep
            contrary to the simple representation this one has
            more places for each state in a Task
        """
        create_place(PetriNetConstants.TOS_STARTED_PLACE,
                     PetriNetConstants.TOS_STARTED_PLACE, net)
        create_place(PetriNetConstants.TOS_MOVED_TO_LOCATION_PLACE,
                     PetriNetConstants.TOS_MOVED_TO_LOCATION_PLACE, net)
        create_place(PetriNetConstants.TOS_WAIT_FOR_ACTION_PLACE,
                     PetriNetConstants.TOS_WAIT_FOR_ACTION_PLACE, net)
        create_place(PetriNetConstants.TOS_FINISHED_PLACE,
                     PetriNetConstants.TOS_FINISHED_PLACE, net)

        create_transition(PetriNetConstants.TOS_FIRST_TRANSITION,
                          PetriNetConstants.TOS_FIRST_TRANSITION, net)
        create_transition(PetriNetConstants.TOS_SECOND_TRANSITION,
                          PetriNetConstants.TOS_SECOND_TRANSITION, net)

        net.add_input(PetriNetConstants.TOS_STARTED_PLACE,
                      PetriNetConstants.TOS_FIRST_TRANSITION, Value(1))
        net.add_output(PetriNetConstants.TOS_WAIT_FOR_ACTION_PLACE,
                       PetriNetConstants.TOS_FIRST_TRANSITION, Value(1))
        net.add_input(PetriNetConstants.TOS_MOVED_TO_LOCATION_PLACE,
                      PetriNetConstants.TOS_FIRST_TRANSITION, Value(1))
        net.add_input(PetriNetConstants.TOS_WAIT_FOR_ACTION_PLACE,
                      PetriNetConstants.TOS_SECOND_TRANSITION, Value(1))
        net.add_output(PetriNetConstants.TOS_FINISHED_PLACE,
                       PetriNetConstants.TOS_SECOND_TRANSITION, Value(1))

    def draw_petri_net(self, name, petri_net):
        """ Saves the given petri net as an image in the current working directory """
        file_path = "./" + name + PetriNetConstants.IMAGE_ENDING
        self.petri_net_drawer.draw_image(petri_net, file_path)

    def generate_triggered_by(self, task, net):
        """
            Generates places and transitions for the TriggeredBy expression
            of the given Task
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

    def generate_finished_by(self, task, net):
        """
            Generates places and transitions for the FinishedBy expression
            of the given Task
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

    def generate_triggered_by_for_tos(self, task, tos, net):
        """
            Generates places and transitions for the TriggeredBy expression
            of the given TransportOrderStep
        """
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
        """
            Generates places and transitions for the FinishedBy expression
            of the given TransportOrderStep
        """
        fb_statement = tos.finished_by_statements
        if fb_statement:
            self.generate_places_from_expression(fb_statement, task.name,
                                                PetriNetConstants.TOS_SECOND_TRANSITION,
                                                [],
                                                False,
                                                tb_event = False,
                                                tos_net=net)

    def generate_places_from_expression(self, expression, task_name, parent_transition, event_name_list, parent_is_not, tb_event, comparator="", value=None, tos_net=None):
        """ Extracts the single events from the expression and creates a place for each """

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

            if expression not in self.task_representations[task_name].event_dict:
                self.task_representations[task_name].event_dict[expression] = []
    
            self.task_representations[task_name].event_dict[expression].append(uuid_str)

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
                elif helpers.is_value(expression["right"]):
                    self.generate_places_from_expression(expression["left"], task_name,
                                                         parent_transition,
                                                         event_name_list, parent_is_not, tb_event,
                                                         expression["binOp"], expression["right"], tos_net=tos_net)

def create_place(place_name, place_type, net, event = None, initialized = True):
    """
        Utility function for creating a place with the snakes module.
        It is used to add a place with the given name and to add labels for
        scheduling (for example if the place represents an event or if its initialized)
    """
    if net.has_place(place_name) is False:
        net.add_place(Place(place_name, []))
        net.place(place_name).label(placeType=place_type, event=event, initialized=initialized)

def create_transition(transition_name, transition_type, net):
    """
        Utility function for creating a transition with the snakes module.
        It is used to add a transition with the given name and to add labels for
        scheduling (currently only the type of the transition)
    """
    net.add_transition(Transition(transition_name))
    net.transition(transition_name).label(transitionType=transition_type)
