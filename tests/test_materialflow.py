""" Contains unit tests for the Materialflow class """

# standard libraries
import sys
import os
import unittest
from unittest.mock import MagicMock
import codecs

# 3rd party packages
import xmlrunner

sys.path.append(os.path.abspath("../lotlan_schedular"))

# local sources
from lotlan_schedular.api.transportorder import TransportOrder
from lotlan_schedular.api.transportorder_step import TransportOrderStep
from lotlan_schedular.api.location import Location
from lotlan_schedular.api.event import Event

from lotlan_schedular.schedular import LotlanSchedular
from lotlan_schedular.defines import LogicConstants
from lotlan_schedular.transport.task import Task

class TestMaterialflow(unittest.TestCase):
    """ Test Materialflow methods """

    def test_initialize_tasks(self):
        lotlan_file = codecs.open("etc/examples/Scheduling/001_simple_task.tl", "r",
                                  encoding="utf8")
        lotlan_string = lotlan_file.read()
        schedular = LotlanSchedular(lotlan_string)
        material_flow = schedular.get_materialflows()[0]

        transport_order = TransportOrder()
        pickup_tos = TransportOrderStep()
        delivery_tos = TransportOrderStep()

        pickup_tos.location = Location("pickupItem", "", "")
        delivery_tos.location = Location("dropoffItem", "", "")

        transport_order.pickup_tos = pickup_tos
        transport_order.delivery_tos = delivery_tos

        task = Task()
        task.name = "Task"
        task.transport_order = transport_order

        material_flow.initialize_tasks([task])

        self.assertEqual(len(material_flow.tasks), 2) # 2 because one task is created from the file
        self.assertEqual(len(material_flow.ids), 2)
        self.assertEqual(len(material_flow.tasks_done), 2)
        self.assertEqual(len(material_flow.not_done_parents), 2)
        self.assertEqual(pickup_tos.location.physical_name, "s1_pickup")
        self.assertEqual(pickup_tos.location.location_type, "SmallLoadCarrier")
        self.assertEqual(delivery_tos.location.physical_name, "ws1_dropoff")
        self.assertEqual(delivery_tos.location.location_type, "SmallLoadCarrier")

        lotlan_file.close()

    def test_find_startable_tasks(self):
        lotlan_file = codecs.open("etc/examples/Scheduling/001_simple_task.tl", "r",
                                  encoding="utf8")
        lotlan_string = lotlan_file.read()
        schedular = LotlanSchedular(lotlan_string, True)
        material_flow = schedular.get_materialflows()[0]

        startable_tasks = material_flow.find_startable_tasks(material_flow.call_graph,
                                                             material_flow.tasks_in_mf)
        self.assertEqual(len(startable_tasks), 1)
        self.assertEqual(startable_tasks[0].name, "helloTask")

        lotlan_file.close()

        lotlan_file = codecs.open("etc/examples/Scheduling/006_two_tasks.tl", "r",
                                  encoding="utf8")
        lotlan_string = lotlan_file.read()
        schedular = LotlanSchedular(lotlan_string, True)
        material_flow = schedular.get_materialflows()[1]

        startable_tasks = material_flow.find_startable_tasks(material_flow.call_graph,
                                                             material_flow.tasks_in_mf)
        self.assertEqual(len(startable_tasks), 1)
        self.assertEqual(startable_tasks[0].name, "helloTask2")

        lotlan_file.close()

        lotlan_file = codecs.open("etc/examples/Scheduling/016_task_sync.tl", "r",
                                  encoding="utf8")
        lotlan_string = lotlan_file.read()
        schedular = LotlanSchedular(lotlan_string, True)
        material_flow = schedular.get_materialflows()[0]

        startable_tasks = material_flow.find_startable_tasks(material_flow.call_graph,
                                                             material_flow.tasks_in_mf)
        self.assertEqual(len(startable_tasks), 2)
        self.assertEqual(startable_tasks[0].name, "helloTask")
        self.assertEqual(startable_tasks[1].name, "helloTask2")

        lotlan_file.close()

    def test_on_petri_net_response(self):
        lotlan_file = codecs.open("etc/examples/Scheduling/001_simple_task.tl", "r",
                                  encoding="utf8")
        lotlan_string = lotlan_file.read()
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

        lotlan_file.close()

    def test_all_tasks_done(self):
        lotlan_file = codecs.open("etc/examples/Scheduling/005_self_loop.tl", "r",
                                  encoding="utf8")
        lotlan_string = lotlan_file.read()
        schedular = LotlanSchedular(lotlan_string, True)

        material_flow = schedular.get_materialflows()[0]
        material_flow.start()

        self.assertEqual(material_flow.all_tasks_done(), False)
        material_flow.fire_event("0", Event("to_done", "", "Boolean", value=True))
        self.assertEqual(material_flow.all_tasks_done(), False)
        lotlan_file.close()

        lotlan_file = codecs.open("etc/examples/Scheduling/001_simple_task.tl", "r",
                                  encoding="utf8")
        lotlan_string = lotlan_file.read()
        schedular = LotlanSchedular(lotlan_string, True)
        material_flow = schedular.get_materialflows()[0]
        material_flow.start()
        self.assertEqual(material_flow.all_tasks_done(), False)

        material_flow.fire_event("0", Event("moved_to_location", "", "Boolean", value=True))
        material_flow.fire_event("0", Event("moved_to_location", "", "Boolean", value=True))

        material_flow.fire_event("0", Event("to_done", "", "Boolean", value=True))
        self.assertEqual(material_flow.all_tasks_done(), True)

        lotlan_file.close()

if __name__ == "__main__":
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output="test-reports"),
                  failfast=False, buffer=False, catchbreak=False)
