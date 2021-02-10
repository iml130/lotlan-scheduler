""" Contains PetriNetLogic class """

# local sources
import lotlan_scheduler.helpers as helpers
from lotlan_scheduler.petri_net.drawer import PetriNetDrawer
from lotlan_scheduler.api.transportorder import TransportOrder

# global defines
from lotlan_scheduler.defines import PetriNetConstants, LogicConstants

from nets import Value, Marking

class PetriNetLogic:
    """
        Scheduling of the generated petri nets is done in this class
    """
    def __init__(self, task_representations, test_flag=False):
        self.task_representations = task_representations
        self.petri_net_drawer = PetriNetDrawer()
        self.test_flag = test_flag

    def set_awaited_events(self, task, awaited_events):
        self.task_representations[task.name].awaited_events = awaited_events

    def draw_petri_net(self, name, petri_net):
        """ Saves the given petri net as an image in the current working directory """
        file_path = "./" + name + PetriNetConstants.IMAGE_ENDING
        self.petri_net_drawer.draw_image(petri_net, file_path)

    def get_petri_nets(self):
        """ Returns a list of all task petri nets """
        task_petri_nets = []
        for task_repr in self.task_representations.values():
            task_petri_nets.append(task_repr.net)
        return task_petri_nets

    def get_pickup_nets(self):
        """ Returns a list of all pickup petri nets """
        pickup_nets = []
        for task_repr in self.task_representations.values():
            pickup_nets.append(task_repr.pickup_net)
        return pickup_nets

    def get_delivery_nets(self):
        """ Returns a list of all delivery petri nets """
        delivery_nets = []
        for task_repr in self.task_representations.values():
            delivery_nets.append(task_repr.delivery_net)
        return delivery_nets

    def evaluate_petri_net(self, petri_net, task, cb=None):
        """ Tries to fire every transition as long as all transitions
            were tried and nothing can be done anymore
        """
        index = 0
        work_to_do = False

        transitions = list(petri_net._trans)
        task_repr = self.task_representations[task.name]
        while index < len(petri_net._trans) or work_to_do:
            transition = transitions[index]
            transition_fired = False

            if task_repr.transition_fired[transition] is False:
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
                        task_repr.transition_fired[transition] = True
                        transition_fired = True
                    except ValueError:
                        transition_fired = False

            if transition_fired:
                work_to_do, index = self.handle_current_state(task, petri_net,
                                                            transition, cb, index)

            index = index + 1

            # restart loop if every transition was iterated but
            # there is still work to do
            if index == len(petri_net._trans) and work_to_do:
                index = 0
                work_to_do = False

        if self.test_flag:
            self.draw_petri_net(petri_net.name, petri_net)

    def handle_current_state(self, task, petri_net, transition, cb, index):
        """
            Checks which transition was passed and calls the given cb with the
            message of the corresponding state.
            Returns if evaulation is done so there is nothing more to do or if
            there is still work to do

            transition: the transition fired
        """
        work_to_do = True
        msg = ""
        task_repr = self.task_representations[task.name]

        if transition == PetriNetConstants.TRIGGERED_BY_TRANSITION:
            remove_all_tokens(petri_net)
            msg = LogicConstants.TRIGGERED_BY_PASSED_MSG

        elif transition == PetriNetConstants.TASK_FIRST_TRANSITION:
            msg = LogicConstants.TO_DONE_MSG
        elif transition == PetriNetConstants.TASK_SECOND_TRANSITION:
            remove_all_tokens(petri_net)
            msg = LogicConstants.TASK_FINISHED_MSG

            # allow transition firing again to work with loops
            for trans in petri_net._trans:
                task_repr.transition_fired[trans] = False
            work_to_do = False
            index = len(petri_net._trans)
        elif transition == PetriNetConstants.TOS_TRIGGERED_BY_TRANSITION:
            msg = LogicConstants.TOS_TB_PASSED_MSG
        elif transition == PetriNetConstants.TOS_FIRST_TRANSITION:
            msg = LogicConstants.TOS_WAIT_FOR_ACTION
        elif transition == PetriNetConstants.TOS_SECOND_TRANSITION:
            msg = LogicConstants.TOS_FINISHED_MSG
            for trans in petri_net._trans:
                task_repr.transition_fired[trans] = False

        if cb is not None:
            cb(msg, task)

        return work_to_do, index

    def get_petri_net(self, task):
        """
            Returns the currently active petri net depending on
            the current state of the TransportOrder
        """
        petri_net = None
        task_repr = self.task_representations[task.name]
        current_state = task.transport_order.state

        if current_state in [TransportOrder.TransportOrderState.PICKUP_STARTED,
                             TransportOrder.TransportOrderState.PICKUP_WAIT_FOR_TRIGGERED_BY,
                             TransportOrder.TransportOrderState.WAIT_FOR_LOADING]:
            petri_net = task_repr.pickup_net
        elif current_state in [TransportOrder.TransportOrderState.DELIVERY_STARTED,
                               TransportOrder.TransportOrderState.DELIVERY_WAIT_FOR_TRIGGERED_BY,
                               TransportOrder.TransportOrderState.WAIT_FOR_UNLOADING]:
            petri_net = task_repr.delivery_net
        else:
            petri_net = task_repr.net

        return petri_net

    def fire_event(self, task, event, cb=None):
        """
            Adds a token to the corresponding place of the event in the petri net
            checks before if event is expected and can be fired
        """

        petri_net = self.get_petri_net(task)
        task_repr = self.task_representations[task.name]

        is_awaited_event = False
        for evt in task_repr.awaited_events: # Falscher Inhalt: 'helloTask2': []
            if evt is not None and evt.logical_name == event.logical_name:
                is_awaited_event = True
        if is_awaited_event:
            if event.logical_name in task_repr.event_dict:
                for event_uuid in task_repr.event_dict[event.logical_name]:
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
                            elif helpers.is_value(event.value):
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
        Checks if the given event can be fired:
        Only works for tb and fb events.
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

def cast_value(value, requested_type):
    """ Tries to cast the given value to the given type """
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
    """
        If types of both events are the same execute
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
