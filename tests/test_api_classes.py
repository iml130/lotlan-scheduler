import sys
import os
sys.path.append(os.path.abspath('../lotlan_schedular'))

from lotlan_schedular.api.event import Event
from lotlan_schedular.api.location import Location
from lotlan_schedular.schedular import LotlanSchedular

import subprocess as su
import unittest

import xmlrunner

# uninstall possible old lotlan_schedular packages
# so current code is used not old one
os.system("pip3 uninstall lotlan_schedular")

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

class ApiClassTest(unittest.TestCase):

    @classmethod
    def setUp(self):
        lotlan_logic = LotlanSchedular(test_string, True)
        material_flow = lotlan_logic.get_materialflows()[0]
        self.lotlan_logic = lotlan_logic
        self.material_flow = material_flow
        self.material_flow.start()
        self.transport_order_steps = material_flow.lotlan_structure.transport_order_steps

    def test_location(self):
        self.assertEqual(len(self.transport_order_steps), 2)

        self.assertEqual(self.transport_order_steps["loadStorage"].location.logical_name, "pickupItem")
        self.assertEqual(self.transport_order_steps["loadStorage"].location.physical_name, "s1_pickup")
        self.assertEqual(self.transport_order_steps["loadStorage"].location.location_type, "SmallLoadCarrier")
        self.assertEqual(self.transport_order_steps["unloadWorkstation1"].location.logical_name, "dropoffItem")
        self.assertEqual(self.transport_order_steps["unloadWorkstation1"].location.physical_name, "ws1_dropoff")
        self.assertEqual(self.transport_order_steps["unloadWorkstation1"].location.location_type, "SmallLoadCarrier")
        
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


if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'), failfast=False, buffer=False, catchbreak=False)
