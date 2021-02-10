""" Contains unit tests for the API classes """

# standard libraries
import sys
import os
import unittest

# 3rd party packages
import xmlrunner

sys.path.append(os.path.abspath("../lotlan_scheduler"))

# local sources
from lotlan_scheduler.scheduler import LotlanScheduler

# uninstall possible old lotlan_scheduler packages
# so current code is used not old one
os.system("pip3 uninstall lotlan_scheduler")

test_string = """
Location pickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"
End

Location dropoffItem
    name = "ws1_dropoff"
    type = "SmallLoadCarrier"
End

Event buttonPressed
    name = "button"
    type = "Boolean"
End

TransportOrderStep loadStorage
    Location pickupItem
    TriggeredBy buttonPressed
End

TransportOrderStep unloadWorkstation1
    Location dropoffItem
    FinishedBy buttonPressed
End

Task helloTask
    Transport
    From loadStorage
    To unloadWorkstation1
End
"""

class TestApiClasses(unittest.TestCase):
    """
        Tests if objects of api classes contains the correct attribute values
        while scheduling
    """
    def setUp(self):
        lotlan_logic = LotlanScheduler(test_string, True)
        material_flow = lotlan_logic.get_materialflows()[0]
        self.lotlan_logic = lotlan_logic
        self.material_flow = material_flow
        self.material_flow.start()
        self.transport_order_steps = material_flow.lotlan_structure.transport_order_steps

    def test_location(self):
        self.assertEqual(len(self.transport_order_steps), 2)

        load_storage_location = self.transport_order_steps["loadStorage"].location
        unload_workstation_location = self.transport_order_steps["unloadWorkstation1"].location

        self.assertEqual(load_storage_location.logical_name, "pickupItem")
        self.assertEqual(load_storage_location.physical_name, "s1_pickup")
        self.assertEqual(load_storage_location.location_type, "SmallLoadCarrier")
        self.assertEqual(unload_workstation_location.logical_name, "dropoffItem")
        self.assertEqual(unload_workstation_location.physical_name, "ws1_dropoff")
        self.assertEqual(unload_workstation_location.location_type, "SmallLoadCarrier")

    def test_triggered_by(self):
        self.assertEqual(len(self.transport_order_steps), 2)
        triggered_by_events = self.transport_order_steps["loadStorage"].triggered_by

        self.assertEqual(len(triggered_by_events), 1)
        tb_event = triggered_by_events[0]

        self.assertEqual(tb_event.logical_name, "buttonPressed")
        self.assertEqual(tb_event.physical_name, "button")
        self.assertEqual(tb_event.event_type, "Boolean")
        self.assertEqual(tb_event.comparator, "==")
        self.assertEqual(tb_event.value, True)

    def test_finished_by(self):
        self.assertEqual(len(self.transport_order_steps), 2)
        finished_by_events = self.transport_order_steps["unloadWorkstation1"].finished_by

        self.assertEqual(len(finished_by_events), 1)
        fb_event = finished_by_events[0]

        self.assertEqual(fb_event.logical_name, "buttonPressed")
        self.assertEqual(fb_event.physical_name, "button")
        self.assertEqual(fb_event.event_type, "Boolean")
        self.assertEqual(fb_event.comparator, "==")
        self.assertEqual(fb_event.value, True)


if __name__ == "__main__":
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output="test-reports"),
                  failfast=False, buffer=False, catchbreak=False)
