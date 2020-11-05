# standard libraries
import codecs
import sys
from os.path import dirname
from pathlib import Path
import argparse
from enum import Enum

# 3rd party packages
from antlr4 import InputStream, CommonTokenStream
import snakes.plugins

# local sources
from lotlan_schedular.parser.CreateTreeTaskParserVisitor import CreateTreeTaskParserVisitor
from lotlan_schedular.PetriNetDrawer import PetriNetDrawer

# global defines
from lotlan_schedular.defines import ANTLR_COMMAND, PetriNetConstants

from lotlan_schedular.parser.LoTLanLexer import LoTLanLexer
from lotlan_schedular.parser.LoTLanParser import LoTLanParser
from lotlan_schedular.api.event import Event

from nets import PetriNet, Place, Transition, Inhibitor, Value, Marking
snakes.plugins.load(["labels", "gv"], "snakes.nets", "nets")

import uuid

class PetriNetState(Enum):
    not_started = 0
    wait_for_tb = 1
    wait_for_to_done = 2
    wait_for_fb = 3
    finished = 4

class PetriNetGenerator:
    """
        Takes a lotlan file as argument and generates a Petri Net
        which visualizes the connection between tasks and transportordersteps.
        For each task there is a png file generated
    """

    def __init__(self, tasks, event_instances, file_folder=".", test_flag=False, simple_representation=False):
        self.petri_nets = []
        for i, task in enumerate(tasks):
            net = PetriNet(PetriNetConstants.PETRI_NET_NAME + str(i))
            self.petri_nets.append(net)

        self.tasks = tasks
        self.file_folder = file_folder
        self.petri_net_drawer = PetriNetDrawer()
        self.simple_representation = simple_representation
        self.net_task_dict = {}
        self.triggered_by_passed = {}
        self.test_flag = test_flag
        self.awaited_events = {}
        self.petri_net_state = {}
        self.transition_fired = {}
        self.event_dict = {}
        self.event_counter = 0
        self.event_instances = event_instances

    def generate_task_nets(self):
        for i, task in enumerate(self.tasks):
            petri_net = self.petri_nets[i]

            self.net_task_dict[task.name] = petri_net
            self.event_dict[task.name] =  {}

            # generate task action
            self.generate_task_operation(task.name, petri_net)

            # generate places and transitions for TriggeredBy
            task.triggered_by_events = self.generate_triggered_by(task, petri_net)

            # generate places and transitions for FinishedBy
            task.finished_by_events = self.generate_finished_by(task, petri_net)

            self.triggered_by_passed[task.name] = False

            if self.test_flag:
                self.draw_petri_net(task.name, petri_net)

            self.awaited_events[task.name] = []
            self.petri_net_state[task.name] = PetriNetState.not_started

        for transition in petri_net._trans:
            self.transition_fired[transition] = False

        return self.petri_nets

    def draw_petri_net(self, name, petri_net):
        self.petri_net_drawer.draw_image(petri_net, self.file_folder + "/" + name + PetriNetConstants.IMAGE_ENDING)

    def generate_triggered_by(self, task, net):
        triggered_by_event_names = []
        if task.triggered_by:
            self.create_transition(PetriNetConstants.TRIGGERED_BY_TRANSITION, "", net)

            if self.simple_representation is True:
                self.create_place(PetriNetConstants.TRIGGERED_BY, "", net)
                net.add_input(PetriNetConstants.TRIGGERED_BY,
                              PetriNetConstants.TRIGGERED_BY_TRANSITION, Value(1))
                net.add_output(PetriNetConstants.TASK_STARTED_PLACE,
                               PetriNetConstants.TRIGGERED_BY_TRANSITION, Value(1))
            else:
                self.check_expression(task.triggered_by, task.name,
                                      PetriNetConstants.TRIGGERED_BY_TRANSITION,
                                      triggered_by_event_names,
                                      False,
                                      tb_event = True)
                net.add_output(PetriNetConstants.TASK_STARTED_PLACE,
                               PetriNetConstants.TRIGGERED_BY_TRANSITION, Value(1))
        return triggered_by_event_names

    def generate_finished_by(self, task, net):
        finished_by_event_names = []
        if self.simple_representation is True:
            self.create_place(PetriNetConstants.FINISHED_BY, "", net)
            net.add_input(PetriNetConstants.FINISHED_BY, PetriNetConstants.ON_DONE_ENDING, Value(1))
        else:
            if task.finished_by != "":
                self.check_expression(task.finished_by, task.name, PetriNetConstants.TASK_SECOND_TRANSITION,
                                      finished_by_event_names, False, tb_event=False)
        return finished_by_event_names

    def generate_task_operation(self, task_name, net):
        if self.simple_representation is True:
            self.generate_simple_task_operation(task_name, net)
        else:
            self.generate_advanced_task_operation(task_name, net)

    def generate_simple_task_operation(self, task_name, net):
        self.create_place(task_name, "action", net)

    def generate_advanced_task_operation(self, task_name, net):
        self.create_place(PetriNetConstants.TASK_STARTED_PLACE, PetriNetConstants.TASK_STARTED_PLACE, net)
        self.create_place(PetriNetConstants.TO_DONE_PLACE, PetriNetConstants.TO_DONE_PLACE, net)
        self.create_place("to_done", "to_done", net)
        self.create_place("task_finished", "task_finished", net)

        self.create_transition(PetriNetConstants.TASK_FIRST_TRANSITION,
                               PetriNetConstants.TASK_FIRST_TRANSITION, net)
        self.create_transition(PetriNetConstants.TASK_SECOND_TRANSITION,
                               PetriNetConstants.TASK_SECOND_TRANSITION, net)

        net.add_input(PetriNetConstants.TASK_STARTED_PLACE,
                      PetriNetConstants.TASK_FIRST_TRANSITION, Value(1))
        net.add_output(PetriNetConstants.TO_DONE_PLACE,
                       PetriNetConstants.TASK_FIRST_TRANSITION, Value(1))
        net.add_input("to_done", PetriNetConstants.TASK_FIRST_TRANSITION, Value(1))
        net.add_input(PetriNetConstants.TO_DONE_PLACE, PetriNetConstants.TASK_SECOND_TRANSITION, Value(1))
        net.add_output("task_finished", PetriNetConstants.TASK_SECOND_TRANSITION, Value(1))


    def is_float(self, x):
        try:
            a = float(x)
        except (TypeError, ValueError):
            return False
        else:
            return True

    def is_int(self, x):
        try:
            a = float(x)
            b = int(a)
        except (TypeError, ValueError):
            return False
        else:
            return a == b

    def is_value(self, x):
        return self.is_float(x) or self.is_int(x) or isinstance(x, str)


    def cast_value(self, value, requested_type):
        if requested_type == "Boolean":
            return value == "True"
        elif requested_type == "Integer":
            return int(value)
        elif requested_type == "Float":
            return float(value)
        else:
            return value

    def check_expression(self, expression, task_name, parent_transition, event_name_list, parent_is_not, tb_event, comparator="", value=None):
        net = self.net_task_dict[task_name]
        if isinstance(expression, str):
            # generate single node
            event_postfix = ""

            uuid_str = expression + "_" + str(self.event_counter)

            self.event_counter = self.event_counter + 1
            place_name = uuid_str + event_postfix

            event_type = self.event_instances[expression].keyval["type"]
            event = Event(expression, "", event_type, comparator=comparator, value=value)
            self.create_place(place_name, "", net, event=event, initialized=False)
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
                self.check_expression(expression["value"], task_name, parent_transition, event_name_list, new_parent_is_not, tb_event)
            elif len(expression) == 3:
                if expression["binOp"] == ".":
                    self.check_expression(str(expression["left"]) + "." + str(expression["right"]), task_name,
                                          net, parent_transition, event_name_list, parent_is_not, tb_event)
                # case: expr == <True|False>
                elif expression["right"] == "True":
                    if expression["binOp"] == "==":
                        self.check_expression(expression["left"], task_name, parent_transition, event_name_list, False, tb_event)
                    elif expression["binOp"] == "!=":
                        self.check_expression(expression["left"], task_name, parent_transition, event_name_list, True, tb_event)
                elif expression["right"] == "False":
                    if expression["binOp"] == "==":
                        self.check_expression(expression["left"], task_name, parent_transition, event_name_list, True, tb_event)
                    elif expression["binOp"] == "!=":
                        self.check_expression(expression["left"], task_name, parent_transition, event_name_list, False, tb_event)
                elif expression["left"] == "(" and expression["right"] == ")":
                        return self.check_expression(expression["binOp"], task_name,
                                                         parent_transition, event_name_list, parent_is_not, tb_event)
                elif expression["binOp"] == "and" or expression["binOp"] == "or":
                    composition = str(expression)

                    if expression["binOp"] == "and":
                        self.create_place(composition + "_end", "and", net)
                        self.create_transition(composition + "_t", "", net)

                        self.check_expression(expression["left"], task_name, composition + "_t", event_name_list, False, tb_event)
                        self.check_expression(expression["right"], task_name, composition + "_t", event_name_list, False, tb_event)

                        net.add_output(composition + "_end", composition + "_t", Value(1))

                    elif expression["binOp"] == "or":
                        self.create_place(composition + "_end", "or", net)

                        self.create_transition(composition + "_t1", "", net)
                        self.create_transition(composition + "_t2", "", net)

                        net.add_output(composition + "_end", composition + "_t1", Value(1))
                        net.add_output(composition + "_end", composition + "_t2", Value(1))

                        self.check_expression(expression["left"], task_name, composition + "_t1", event_name_list, False, tb_event)
                        self.check_expression(expression["right"], task_name, composition + "_t2", event_name_list, False, tb_event)

                    if parent_is_not is True:
                        net.add_input(composition + "_end", parent_transition, Inhibitor(Value(1)))
                    else:
                        net.add_input(composition + "_end", parent_transition, Value(1))
                elif self.is_value(expression["right"]):
                    self.check_expression(expression["left"], task_name, parent_transition, event_name_list, parent_is_not, tb_event, expression["binOp"], expression["right"])

    def create_place(self, place_name, place_type, net, event = None, initialized = True):
        if net.has_place(place_name) is False:
            net.add_place(Place(place_name, []))
            net.place(place_name).label(placeType=place_type, event=event, initialized=initialized)

    def create_transition(self, transition_name, transition_type, net):
        net.add_transition(Transition(transition_name))
        net.transition(transition_name).label(transitionType=transition_type)

    def evaluate_petri_net(self, petri_net, task, cb=None):
        index = 0
        work_to_do = False

        transitions = list(petri_net._trans)
        while index < len(petri_net._trans) or work_to_do:
            transition = transitions[index]
            transition_fired = False

            if self.transition_fired[transition] is False:
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
                        self.transition_fired[transition] = True
                        transition_fired = True
                    except ValueError:
                        transition_fired = False

            if transition_fired:
                if transition == PetriNetConstants.TRIGGERED_BY_TRANSITION:
                    self.remove_all_tokens(petri_net)

                    if cb is not None:
                        cb("t_by", task)
                        self.triggered_by_passed[task.name] = True
                    
                    work_to_do = True
                elif transition == PetriNetConstants.TASK_FIRST_TRANSITION:
                    if cb is not None:
                        cb("t_done", task)
                        
                    work_to_do = True
                elif transition == PetriNetConstants.TASK_SECOND_TRANSITION:
                    self.remove_all_tokens(petri_net)

                    if cb is not None:
                        cb("t_finished", task)
                    # allow transition firing again to work with loops
                    for trans in petri_net._trans:
                        self.transition_fired[trans] = False

                    work_to_do = False
                    index = len(petri_net._trans)
                else:
                    work_to_do = True
            index = index + 1

            # restart loop if every transition was iterated but
            # there is still work to do
            if index == len(petri_net._trans) and work_to_do:
                index = 0
                work_to_do = False

        if self.test_flag:
            self.draw_petri_net(task.name, petri_net)

    def fire_event(self, task, event, cb=None):
        petri_net = self.net_task_dict[task.name]

        awaited_event = False
        for evt in self.awaited_events[task.name]:
            if evt is not None and evt.logical_name == event.logical_name:
                awaited_event = True
    
        if awaited_event:
            if event.logical_name in self.event_dict[task.name]:
                for event_uuid in self.event_dict[task.name][event.logical_name]:
                    if petri_net.has_place(event_uuid):
                        tb_event = petri_net.place(event_uuid).label("tb_event")

                        can_be_fired = False
                        if ((self.petri_net_state[task.name] == PetriNetState.wait_for_tb and tb_event) or
                            (self.petri_net_state[task.name] == PetriNetState.wait_for_fb and not tb_event)):
                            can_be_fired = True
                        
                        if can_be_fired:
                            petri_net.place(event_uuid).label(initialized=True)
                            if isinstance(event.value, bool):
                                if event.value is True:
                                    petri_net.place(event_uuid).add(1)
                                    self.draw_petri_net(task.name, petri_net)
                                else:
                                    self.remove_token(petri_net, event_uuid)
                            elif self.is_value(event.value):
                                event_from_place = petri_net.place(event_uuid).label("event")
                                if self.parse_comparator_and_value(event_from_place, event):
                                    petri_net.place(event_uuid).add(1)
                                    self.draw_petri_net(task.name, petri_net)
                                else:
                                    self.remove_token(petri_net, event_uuid)

            else:
                if event.value is True:
                    petri_net.place(event.logical_name).add(1)
                    self.draw_petri_net(task.name, petri_net)
                else:
                    try:
                        petri_net.place(event.logical_name).remove(1)
                    except ValueError:
                        pass
            self.evaluate_petri_net(petri_net, task, cb)

    def remove_all_tokens(self, net):
        task_started_tokens = net.place(PetriNetConstants.TASK_STARTED_PLACE).tokens
        task_finished_tokens = net.place("task_finished").tokens
        net.set_marking(Marking(task_started = task_started_tokens, task_finished=task_finished_tokens))

    def parse_comparator_and_value(self, required_event, fired_event):
        required_event_type = required_event.event_type
        fired_event_type = fired_event.event_type

        if required_event_type != fired_event_type:
            print("Something went wrong!")
        else:
            comparator = required_event.comparator
            given_value = self.cast_value(fired_event.value, required_event_type)
            required_value = self.cast_value(required_event.value, required_event_type)
            
            if required_event_type == "String":
                required_value = str.replace(required_value, '"', '')

            if comparator == ">":
                return given_value > required_value
            elif comparator == "==":
                return given_value == required_value
            elif comparator == ">=":
                return given_value >= required_value
            elif comparator == "<":
                return given_value < required_value
            elif comparator == "<=":
                return given_value <= required_value
            elif comparator == "!=":
                return given_value != required_value
            else:
                print("Illegal comparator was defined!: " + comparator)
        return False

    def remove_token(self, petri_net, place_name):
        try:
            petri_net.place(place_name).remove(1)
        # there was no token so do nothing
        except ValueError:
            pass


def main():
    parser = argparse.ArgumentParser(prog="", description="Generates petri nets from lotlan file")
    parser.add_argument("file_path", help="path to lotan file", type=str)
    parser.add_argument("--advanced", help="show advanced visualization of petri net", action="store_false")

    args = parser.parse_args()

    lexer = None

    try:
        language_file = codecs.open(args.file_path, "r", encoding='utf8')
        lexer = LoTLanLexer(InputStream(language_file.read()))
    except IOError:
        print("error while reading lotlan file")
        return

    token_stream = CommonTokenStream(lexer)

    parser = LoTLanParser(token_stream)

    tree = parser.program()

    visitor = CreateTreeTaskParserVisitor(None)

    t = visitor.visit(tree)

    petri_net_generator = PetriNetGenerator(t, Path(args.file_path).stem,
                                            dirname(args.file_path), args.advanced)
    petri_net_generator.generate_task_nets()


if __name__ == '__main__':
    main()
