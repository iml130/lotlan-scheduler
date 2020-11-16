import sys
import os

sys.path.append(os.path.abspath('../lotlan_schedular'))

from lotlan_schedular.api.event import Event
from lotlan_schedular.schedular import LotlanSchedular
from snakes.nets import Marking, MultiSet


from test_api_classes import ApiClassTest

from os import walk
from os.path import splitext, join
import subprocess as su
import unittest
import unittest
import xmlrunner


# uninstall possible old lotlan_schedular packages
# so current code is used not old one
os.system("pip3 uninstall lotlan_schedular")


def get_file_names(path):
    file_names = []

    for root, dirs, files in walk(path):
        for file in files:
            full_path = join(root, file)
            ext = splitext(file)[1]

            if ext == ".tl":
                file_names.append(full_path)

    return file_names


class TestScheduling(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        lotlan_logic = {}
        material_flows = {}

        file_names = sorted(get_file_names("etc/examples/Scheduling/"))
        for i, file_name in enumerate(file_names):
            f = open(file_name, "r")
            lotlan_logic[i] = LotlanSchedular(f.read(), True)
            material_flows[i] = lotlan_logic[i].get_materialflows()

            for material_flow in material_flows[i]:
                material_flow.start()
            f.close()
        cls.lotlan_logic = lotlan_logic
        cls.material_flows = material_flows

    def test_simple_task(self):
        material_flows = self.get_material_flows(0)
        self.assertEqual(len(material_flows), 1)

        material_flow = material_flows[0]
        petri_net = material_flow.petri_net_generator.petri_nets[0]

        material_flow.fire_event("0", Event(
            "task_finished", "", "Boolean", value=True))  # should not be allowed

        initial_marking = Marking(task_started=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(), initial_marking)

        material_flow.fire_event("0", Event(
            "to_done", "", "Boolean", value=True))
        finished_marking = Marking(task_finished=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(), finished_marking)

    def test_triggered_by(self):
        material_flows = self.get_material_flows(1)
        self.assertEqual(len(material_flows), 1)

        material_flow = material_flows[0]
        petri_net = material_flow.petri_net_generator.petri_nets[0]

        initial_marking = Marking()
        self.assertEqual(petri_net.get_marking(), initial_marking)

        material_flow.fire_event("0", Event(
            "buttonPressed", "", "Boolean", value=False))
        self.assertEqual(petri_net.get_marking(), initial_marking)

        material_flow.fire_event("0", Event(
            "buttonPressed", "", "Boolean", value=True))
        marking_after_triggered_by_passed = Marking(task_started=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(),
                         marking_after_triggered_by_passed)

        material_flow.fire_event("0", Event(
            "to_done", "", "Boolean", value=True))
        finished_marking = Marking(task_finished=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(), finished_marking)

    def test_finished_by(self):
        material_flows = self.get_material_flows(2)
        self.assertEqual(len(material_flows), 1)

        material_flow = material_flows[0]
        petri_net = material_flow.petri_net_generator.petri_nets[0]

        initial_marking = Marking(task_started=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(), initial_marking)

        material_flow.fire_event("0", Event(
            "to_done", "", "Boolean", value=True))
        marking_after_to_done = Marking(task_done=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(), marking_after_to_done)

        material_flow.fire_event("0", Event(
            "buttonPressed", "", "Boolean", value=False))
        self.assertEqual(petri_net.get_marking(), marking_after_to_done)

        material_flow.fire_event("0", Event(
            "buttonPressed", "", "Boolean", value=True))
        marking_after_finished_by = Marking(task_finished=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(), marking_after_finished_by)

    def test_trb_fb(self):
        material_flows = self.get_material_flows(3)
        self.assertEqual(len(material_flows), 1)

        material_flow = material_flows[0]
        petri_net = material_flow.petri_net_generator.petri_nets[0]

        initial_marking = Marking()
        self.assertEqual(petri_net.get_marking(), initial_marking)

        material_flow.fire_event("0", Event(
            "buttonPressed", "", "Boolean", value=True))
        marking_after_triggered_by_passed = Marking(task_started=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(),
                         marking_after_triggered_by_passed)

        material_flow.fire_event("0", Event(
            "to_done", "", "Boolean", value=True))
        marking_after_to_done = Marking(task_done=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(), marking_after_to_done)

        material_flow.fire_event("0", Event(
            "buttonPressed", "", "Boolean", value=True))  # should not be allowed
        material_flow.fire_event("0", Event(
            "buttonPressed2", "", "Boolean", value=True))
        marking_after_finished_by = Marking(task_finished=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(), marking_after_finished_by)

    def test_self_loop(self):
        material_flows = self.get_material_flows(4)
        self.assertEqual(len(material_flows), 1)

        material_flow = material_flows[0]
        petri_net = material_flow.petri_net_generator.petri_nets[0]

        initial_marking = Marking(task_started=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(), initial_marking)

        material_flow.fire_event("0", Event(
            "to_done", "", "Boolean", value=True))
        finished_marking = Marking(
            task_finished=MultiSet([1]), task_started=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(), finished_marking)

        material_flow.fire_event("0", Event(
            "to_done", "", "Boolean", value=True))
        second_iteration_marking = Marking(
            task_finished=MultiSet([1, 1]), task_started=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(), second_iteration_marking)

        material_flow.fire_event("0", Event(
            "to_done", "", "Boolean", value=True))
        third_iteration_marking = Marking(
            task_finished=MultiSet([1, 1, 1]), task_started=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(), third_iteration_marking)

    def test_two_tasks(self):
        material_flows = self.get_material_flows(5)
        self.assertEqual(len(material_flows), 2)

        material_flow_1 = material_flows[0]
        material_flow_2 = material_flows[1]

        petri_net_m1 = material_flow_1.petri_net_generator.petri_nets[0]
        petri_net_m2 = material_flow_2.petri_net_generator.petri_nets[0]

        initial_marking_m1 = initial_marking_m2 = Marking(
            task_started=MultiSet([1]))

        self.assertEqual(petri_net_m1.get_marking(), initial_marking_m1)
        self.assertEqual(petri_net_m2.get_marking(), initial_marking_m2)

        material_flow_1.fire_event("0", Event(
            "to_done", "", "Boolean", value=True))
        material_flow_2.fire_event("0", Event(
            "to_done", "", "Boolean", value=True))

        final_marking_m1 = final_marking_m2 = Marking(
            task_finished=MultiSet([1]))
        self.assertEqual(petri_net_m1.get_marking(), final_marking_m1)
        self.assertEqual(petri_net_m2.get_marking(), final_marking_m2)

    def test_triggered_by_and(self):
        material_flows = self.get_material_flows(6)
        self.assertEqual(len(material_flows), 1)

        material_flow = material_flows[0]
        petri_net = material_flow.petri_net_generator.petri_nets[0]

        initial_marking = Marking()
        self.assertEqual(petri_net.get_marking(), initial_marking)

        material_flow.fire_event("0", Event(
            "buttonPressed", "", "Boolean", value=True))
        material_flow.fire_event("0", Event(
            "buttonPressed2", "", "Boolean", value=True))

        marking_after_both_true = Marking(
            buttonPressed_0=MultiSet([1]), buttonPressed2_1=MultiSet([1]))

        # check if evaluation of negation works correctly
        self.assertEqual(petri_net.get_marking(), marking_after_both_true)

        material_flow.fire_event("0", Event(
            "buttonPressed", "", "Boolean", value=False))
        marking_after_triggered_by_passed = Marking(task_started=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(),marking_after_triggered_by_passed)

        material_flow.fire_event("0", Event(
            "to_done", "", "Boolean", value=True))
        finished_marking = Marking(task_finished=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(), finished_marking)

    def test_triggered_by_or(self):
        material_flows = self.get_material_flows(7)
        self.assertEqual(len(material_flows), 1)

        material_flow = material_flows[0]
        petri_net = material_flow.petri_net_generator.petri_nets[0]

        initial_marking = Marking()
        self.assertEqual(petri_net.get_marking(), initial_marking)

        material_flow.fire_event("0", Event(
            "buttonPressed2", "", "Boolean", value=True))
        marking_after_triggered_by_passed = Marking(task_started=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(),
                         marking_after_triggered_by_passed)

        material_flow.fire_event("0", Event(
            "to_done", "", "Boolean", value=True))
        finished_marking = Marking(task_finished=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(), finished_marking)

    def test_triggered_by_xor(self):
        material_flows = self.get_material_flows(8)
        self.assertEqual(len(material_flows), 1)

        material_flow = material_flows[0]
        petri_net = material_flow.petri_net_generator.petri_nets[0]

        initial_marking = Marking()
        self.assertEqual(petri_net.get_marking(), initial_marking)

        material_flow.fire_event("0", Event(
            "buttonPressed", "", "Boolean", value=True))
        marking_after_bp_true = Marking(
            buttonPressed_0=MultiSet([1]), buttonPressed_2=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(), marking_after_bp_true)

        material_flow.fire_event("0", Event(
            "buttonPressed2", "", "Boolean", value=False))
        marking_after_tb_passed = Marking(task_started=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(), marking_after_tb_passed)

        material_flow.fire_event("0", Event(
            "to_done", "", "Boolean", value=True))
        finished_marking = Marking(task_finished=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(), finished_marking)

    def test_self_loop_trb_fb(self):
        material_flows = self.get_material_flows(9)
        self.assertEqual(len(material_flows), 1)

        material_flow = material_flows[0]
        petri_net = material_flow.petri_net_generator.petri_nets[0]

        initial_marking = Marking()
        self.assertEqual(petri_net.get_marking(), initial_marking)

        material_flow.fire_event("0", Event(
            "buttonPressed", "", "Boolean", value=True))
        marking_after_triggered_by_passed = Marking(task_started=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(),
                         marking_after_triggered_by_passed)

        material_flow.fire_event("0", Event(
            "to_done", "", "Boolean", value=True))
        finished_marking = Marking(task_done=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(), finished_marking)

        material_flow.fire_event("0", Event(
            "buttonPressed2", "", "Boolean", value=True))
        marking_after_finished_by = Marking(task_finished=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(), marking_after_finished_by)

        material_flow.fire_event("0", Event(
            "buttonPressed", "", "Boolean", value=True))
        marking_after_triggered_by_passed_2 = Marking(
            task_started=MultiSet([1]), task_finished=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(),
                         marking_after_triggered_by_passed_2)

        material_flow.fire_event("0", Event(
            "to_done", "", "Boolean", value=True))
        second_iteration_marking = Marking(
            task_finished=MultiSet([1]), task_done=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(), second_iteration_marking)

        material_flow.fire_event("0", Event(
            "buttonPressed2", "", "Boolean", value=True))
        marking_after_finished_by_2 = Marking(task_finished=MultiSet([1, 1]))
        self.assertEqual(petri_net.get_marking(), marking_after_finished_by_2)

    def test_on_done(self):
        material_flows = self.get_material_flows(12)
        self.assertEqual(len(material_flows), 1)

        material_flow = material_flows[0]
        petri_net = material_flow.petri_net_generator.petri_nets[0]
        petri_net_2 = material_flow.petri_net_generator.petri_nets[1]

        initial_marking = Marking(task_started=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(), initial_marking)

        material_flow.fire_event("0", Event(
            "to_done", "", "Boolean", value=True))
        first_task_finished_marking = Marking(task_finished=MultiSet([1]))
        initial_marking_task2 = Marking(task_started=MultiSet([1]))

        self.assertEqual(petri_net.get_marking(), first_task_finished_marking)
        self.assertEqual(petri_net_2.get_marking(), initial_marking_task2)

        material_flow.fire_event("1", Event(
            "to_done", "", "Boolean", value=True))
        second_task_finished_marking = Marking(task_finished=MultiSet([1]))
        self.assertEqual(petri_net_2.get_marking(),
                         second_task_finished_marking)

    def test_on_done_and_other_task(self):
        material_flows = self.get_material_flows(13)
        self.assertEqual(len(material_flows), 2)

        material_flow_1 = material_flows[0]
        material_flow_2 = material_flows[1]

        petri_net_m1_1 = material_flow_1.petri_net_generator.petri_nets[0]
        petri_net_m1_2 = material_flow_1.petri_net_generator.petri_nets[1]
        petri_net_m2_1 = material_flow_2.petri_net_generator.petri_nets[0]

        initial_marking_m1_1 = Marking(task_started=MultiSet([1]))
        initial_marking_m1_2 = Marking()
        initial_marking_m2_1 = initial_marking_m1_1

        self.assertEqual(petri_net_m1_1.get_marking(), initial_marking_m1_1)
        self.assertEqual(petri_net_m1_2.get_marking(), initial_marking_m1_2)
        self.assertEqual(petri_net_m2_1.get_marking(), initial_marking_m2_1)

        material_flow_1.fire_event("1", Event(
            "to_done", "", "Boolean", value=True))  # should not be accepted
        material_flow_1.fire_event("0", Event(
            "to_done", "", "Boolean", value=True))
        material_flow_2.fire_event("0", Event("to_done", "", "Boolean", value=True))

        marking_after_to_done_m1_1 = Marking(task_finished=MultiSet([1]))
        marking_after_to_done_m1_2 = Marking(task_started=MultiSet([1]))
        marking_after_to_done_m2_1 = marking_after_to_done_m1_1

        self.assertEqual(petri_net_m1_1.get_marking(),
                         marking_after_to_done_m1_1)
        self.assertEqual(petri_net_m1_2.get_marking(),
                         marking_after_to_done_m1_2)
        self.assertEqual(petri_net_m2_1.get_marking(),
                         marking_after_to_done_m2_1)

        material_flow_1.fire_event("1", Event(
            "to_done", "", "Boolean", value=True))
        material_flow_1.fire_event("0", Event(
            "task_started", "", "Boolean", value=True))  # should not be accepted
        material_flow_2.fire_event("0", Event(
            "task_started", "", "Boolean", value=True))  # should not be accepted

        self.assertEqual(petri_net_m1_1.get_marking(),
                         marking_after_to_done_m1_1)
        self.assertEqual(petri_net_m1_2.get_marking(),
                         marking_after_to_done_m1_1)
        self.assertEqual(petri_net_m2_1.get_marking(),
                         marking_after_to_done_m2_1)

    def test_on_done_with_many_tasks(self):
        material_flows = self.get_material_flows(14)
        self.assertEqual(len(material_flows), 1)

        material_flow = material_flows[0]
        petri_net_1 = material_flow.petri_net_generator.petri_nets[0]
        petri_net_2 = material_flow.petri_net_generator.petri_nets[1]
        petri_net_3 = material_flow.petri_net_generator.petri_nets[2]
        petri_net_4 = material_flow.petri_net_generator.petri_nets[3]
        petri_net_5 = material_flow.petri_net_generator.petri_nets[4]

        started_marking = Marking(task_started=MultiSet([1]))
        finished_marking = Marking(task_finished=MultiSet([1]))
        empty_marking = Marking()

        self.assertEqual(petri_net_1.get_marking(), started_marking)
        self.assertEqual(petri_net_2.get_marking(), empty_marking)
        self.assertEqual(petri_net_3.get_marking(), empty_marking)
        self.assertEqual(petri_net_4.get_marking(), empty_marking)
        self.assertEqual(petri_net_5.get_marking(), empty_marking)

        material_flow.fire_event("0", Event(
            "to_done", "", "Boolean", value=True))
        self.assertEqual(petri_net_1.get_marking(), finished_marking)
        self.assertEqual(petri_net_2.get_marking(), started_marking)
        self.assertEqual(petri_net_3.get_marking(), started_marking)
        self.assertEqual(petri_net_4.get_marking(), empty_marking)
        self.assertEqual(petri_net_5.get_marking(), empty_marking)

        material_flow.fire_event("1", Event(
            "to_done", "", "Boolean", value=True))
        material_flow.fire_event("2", Event(
            "to_done", "", "Boolean", value=True))
        self.assertEqual(petri_net_1.get_marking(), finished_marking)
        self.assertEqual(petri_net_2.get_marking(), finished_marking)
        self.assertEqual(petri_net_3.get_marking(), finished_marking)
        self.assertEqual(petri_net_4.get_marking(), started_marking)
        self.assertEqual(petri_net_5.get_marking(), started_marking)

        material_flow.fire_event("3", Event(
            "to_done", "", "Boolean", value=True))
        material_flow.fire_event("4", Event(
            "to_done", "", "Boolean", value=True))
        self.assertEqual(petri_net_1.get_marking(), finished_marking)
        self.assertEqual(petri_net_2.get_marking(), finished_marking)
        self.assertEqual(petri_net_3.get_marking(), finished_marking)
        self.assertEqual(petri_net_4.get_marking(), finished_marking)
        self.assertEqual(petri_net_5.get_marking(), finished_marking)

    def test_task_sync(self):
        material_flows = self.get_material_flows(15)
        self.assertEqual(len(material_flows), 1)

        material_flow = material_flows[0]

        petri_net_1 = material_flow.petri_net_generator.petri_nets[0]
        petri_net_2 = material_flow.petri_net_generator.petri_nets[1]
        petri_net_3 = material_flow.petri_net_generator.petri_nets[2]

        started_marking = Marking(task_started=MultiSet([1]))
        finished_marking = Marking(task_finished=MultiSet([1]))
        empty_marking = Marking()

        self.assertEqual(petri_net_1.get_marking(), started_marking)
        self.assertEqual(petri_net_2.get_marking(), empty_marking)
        self.assertEqual(petri_net_3.get_marking(), started_marking)

        material_flow.fire_event("0", Event(
            "to_done", "", "Boolean", value=True))
        self.assertEqual(petri_net_1.get_marking(), finished_marking)
        self.assertEqual(petri_net_2.get_marking(), empty_marking)
        self.assertEqual(petri_net_3.get_marking(), started_marking)

        material_flow.fire_event("2", Event(
            "to_done", "", "Boolean", value=True))
        self.assertEqual(petri_net_1.get_marking(), finished_marking)
        self.assertEqual(petri_net_2.get_marking(), started_marking)
        self.assertEqual(petri_net_3.get_marking(), finished_marking)

        material_flow.fire_event("1", Event(
            "to_done", "", "Boolean", value=True))
        self.assertEqual(petri_net_1.get_marking(), finished_marking)
        self.assertEqual(petri_net_2.get_marking(), finished_marking)
        self.assertEqual(petri_net_3.get_marking(), finished_marking)

    def test_same_events_in_tb_and_fb(self):
        material_flows = self.get_material_flows(16)
        self.assertEqual(len(material_flows), 1)

        material_flow = material_flows[0]
        petri_net = material_flow.petri_net_generator.petri_nets[0]

        # check if triggeredby and finishedby event places are created
        self.assertEqual(10, len(petri_net._place))

        initial_marking = Marking()
        self.assertEqual(petri_net.get_marking(), initial_marking)

        material_flow.fire_event("0", Event(
            "buttonPressed", "", "Boolean", value=True))
        marking_after_button_pressed = Marking(buttonPressed_0=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(), marking_after_button_pressed)

        material_flow.fire_event("0", Event(
            "buttonPressed2", "", "Boolean", value=False))
        self.assertEqual(petri_net.get_marking(), marking_after_button_pressed)

        material_flow.fire_event("0", Event(
            "buttonPressed", "", "Boolean", value=False))
        marking_after_tb = Marking(task_started=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(), marking_after_tb)

        material_flow.fire_event("0", Event(
            "to_done", "", "Boolean", value=True))
        marking_after_to_done = Marking(task_done=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(), marking_after_to_done)

        material_flow.fire_event("0", Event(
            "buttonPressed2", "", "Boolean", value=True))
        marking_after_bp2_true = Marking(
            task_done=MultiSet([1]), buttonPressed2_3=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(), marking_after_bp2_true)

        material_flow.fire_event("0", Event(
            "buttonPressed", "", "Boolean", value=False))
        marking_after_fb = Marking(task_finished=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(), marking_after_fb)

    def test_same_event_in_condition(self):
        material_flows = self.get_material_flows(17)
        self.assertEqual(len(material_flows), 1)

        material_flow = material_flows[0]
        petri_net = material_flow.petri_net_generator.petri_nets[0]

        initial_marking = Marking()
        self.assertEqual(petri_net.get_marking(), initial_marking)

        material_flow.fire_event("0", Event(
            "buttonPressed2", "", "Boolean", value=True))
        material_flow.fire_event("0", Event(
            "buttonPressed", "", "Boolean", value=True))
        marking_after_tb = Marking(task_started=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(), marking_after_tb)

        material_flow.fire_event("0", Event(
            "to_done", "", "Boolean", value=True))
        marking_after_to_done = Marking(task_finished=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(), marking_after_to_done)

    def test_tb_with_integer(self):
        material_flows = self.get_material_flows(18)
        self.assertEqual(len(material_flows), 1)

        material_flow = material_flows[0]
        petri_net = material_flow.petri_net_generator.petri_nets[0]

        initial_marking = Marking()
        self.assertEqual(petri_net.get_marking(), initial_marking)

        material_flow.fire_event("0", Event("sensor", "", "Integer", value=3))
        self.assertEqual(petri_net.get_marking(), initial_marking)

        material_flow.fire_event("0", Event("sensor", "", "Integer", value=51))
        marking_after_sensor_is_51 = Marking(sensor_0=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(), marking_after_sensor_is_51)

        material_flow.fire_event("0", Event("sensor2", "", "Integer", value=5))
        marking_after_sensor2_is_5 = Marking(task_started=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(), marking_after_sensor2_is_5)

        material_flow.fire_event("0", Event(
            "to_done", "", "Boolean", value=True))
        finished_marking = Marking(task_finished=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(), finished_marking)

    def test_tb_with_string(self):
        material_flows = self.get_material_flows(19)
        self.assertEqual(len(material_flows), 1)

        material_flow = material_flows[0]
        petri_net = material_flow.petri_net_generator.petri_nets[0]

        initial_marking = Marking()
        self.assertEqual(petri_net.get_marking(), initial_marking)

        material_flow.fire_event("0", Event(
            "terminal", "", "String", value="ab"))
        self.assertEqual(petri_net.get_marking(), initial_marking)

        material_flow.fire_event("0", Event(
            "terminal", "", "String", value="abc"))
        marking_after_terminal_is_ab = Marking(task_started=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(), marking_after_terminal_is_ab)

        material_flow.fire_event("0", Event(
            "to_done", "", "Boolean", value=True))
        finished_marking = Marking(task_finished=MultiSet([1]))
        self.assertEqual(petri_net.get_marking(), finished_marking)

    def get_material_flows(self, test_number):
        return TestScheduling.material_flows[test_number]


if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'), failfast=False, buffer=False, catchbreak=False)
