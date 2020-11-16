import sys
import os
sys.path.append(os.path.abspath("../lotlan_schedular"))

from lotlan_schedular.api.transportorder import TransportOrder
from lotlan_schedular.api.transportorder_step import TransportOrderStep
from lotlan_schedular.api.location import Location
from lotlan_schedular.api.event import Event

from lotlan_schedular.schedular import LotlanSchedular
from lotlan_schedular.defines import LogicConstants
from lotlan_schedular.transport.Task import Task

import unittest
from unittest.mock import MagicMock

import codecs
import xmlrunner


class TestMaterialflow(unittest.TestCase):
    """ Test Materialflow methods """

    def test_initialize_tasks(self):
        lotlan_string = codecs.open("etc/examples/Scheduling/001_simple_task.tl", "r",
                                    encoding="utf8").read()
        schedular = LotlanSchedular(lotlan_string)
        material_flow = schedular.get_materialflows()[0]

        transport_order = TransportOrder()
        tos_from = TransportOrderStep()
        tos_to = TransportOrderStep()

        tos_from.location = Location("pickupItem", "", "")
        tos_to.location = Location("dropoffItem", "", "")

        transport_order.to_step_from = tos_from
        transport_order.to_step_to = tos_to

        task = Task()
        task.name = "Task"
        task.transport_order = transport_order

        material_flow.initialize_tasks([task])

        self.assertEqual(len(material_flow.tasks), 2) # 2 because one task is created from the file
        self.assertEqual(len(material_flow.ids), 2)
        self.assertEqual(len(material_flow.tasks_done), 2)
        self.assertEqual(len(material_flow.not_done_parents), 2)
        self.assertEqual(tos_from.location.physical_name, "s1_pickup")
        self.assertEqual(tos_from.location.location_type, "SmallLoadCarrier")
        self.assertEqual(tos_to.location.physical_name, "ws1_dropoff")
        self.assertEqual(tos_to.location.location_type, "SmallLoadCarrier")

    def test_find_startable_tasks(self):
        lotlan_string = codecs.open("etc/examples/Scheduling/001_simple_task.tl", "r",
                                    encoding="utf8").read()
        schedular = LotlanSchedular(lotlan_string, True)
        material_flow = schedular.get_materialflows()[0]

        startable_tasks = material_flow.find_startable_tasks(material_flow.call_graph,
                                                             material_flow.tasks_in_mf)
        self.assertEqual(len(startable_tasks), 1)
        self.assertEqual(startable_tasks[0].name, "helloTask")

        lotlan_string = codecs.open("etc/examples/Scheduling/006_two_tasks.tl", "r",
                                    encoding="utf8").read()
        schedular = LotlanSchedular(lotlan_string, True)
        material_flow = schedular.get_materialflows()[1]

        startable_tasks = material_flow.find_startable_tasks(material_flow.call_graph,
                                                             material_flow.tasks_in_mf)
        self.assertEqual(len(startable_tasks), 1)
        self.assertEqual(startable_tasks[0].name, "helloTask2")

        lotlan_string = codecs.open("etc/examples/Scheduling/016_task_sync.tl", "r",
                                    encoding="utf8").read()
        schedular = LotlanSchedular(lotlan_string, True)
        material_flow = schedular.get_materialflows()[0]

        startable_tasks = material_flow.find_startable_tasks(material_flow.call_graph,
                                                             material_flow.tasks_in_mf)
        self.assertEqual(len(startable_tasks), 2)
        self.assertEqual(startable_tasks[0].name, "helloTask")
        self.assertEqual(startable_tasks[1].name, "helloTask2")


    def test_on_petri_net_response(self):
        lotlan_string = codecs.open("etc/examples/Scheduling/001_simple_task.tl", "r",
                                    encoding="utf8").read()
        schedular = LotlanSchedular(lotlan_string)
        material_flow = schedular.get_materialflows()[0]

        material_flow.next_to = MagicMock()
        material_flow.on_petri_net_response(LogicConstants.TRIGGERED_BY_PASSED_MSG, None)
        material_flow.next_to.assert_called_once_with([None])

        material_flow.on_to_done = MagicMock()
        material_flow.on_petri_net_response(LogicConstants.TO_DONE_MSG, None)
        material_flow.on_to_done.assert_called_once_with(None)

        material_flow.on_task_finished = MagicMock()
        material_flow.on_petri_net_response(LogicConstants.TASK_FINISHED_MSG, None)
        material_flow.on_task_finished.assert_called_once_with(None)

    def test_all_tasks_done(self):
        lotlan_string = codecs.open("etc/examples/Scheduling/005_self_loop.tl", "r",
                                    encoding="utf8").read()
        schedular = LotlanSchedular(lotlan_string, True)
        material_flow = schedular.get_materialflows()[0]
        material_flow.start()
        self.assertEqual(material_flow.all_tasks_done(), False)
        material_flow.fire_event("0", Event("to_done", "", "Boolean", value=True))
        self.assertEqual(material_flow.all_tasks_done(), False)

        lotlan_string = codecs.open("etc/examples/Scheduling/001_simple_task.tl", "r",
                                    encoding="utf8").read()
        schedular = LotlanSchedular(lotlan_string, True)
        material_flow = schedular.get_materialflows()[0]
        material_flow.start()
        self.assertEqual(material_flow.all_tasks_done(), False)
        material_flow.fire_event("0", Event("to_done", "", "Boolean", value=True))
        self.assertEqual(material_flow.all_tasks_done(), True)


if __name__ == "__main__":
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output="test-reports"),
                  failfast=False, buffer=False, catchbreak=False)
