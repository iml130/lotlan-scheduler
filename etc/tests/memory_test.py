# standard libraries
import sys
import os
from os import walk
from os.path import splitext, join
import threading
import unittest
import time

# 3rd party packages
import xmlrunner
from snakes.nets import Marking, MultiSet

sys.path.append(os.path.abspath("../lotlan_schedular"))

# local sources
import lotlan_schedular.helpers as helpers
from lotlan_schedular.api.event import Event
from lotlan_schedular.schedular import LotlanSchedular
from lotlan_schedular.api.location import Location
from lotlan_schedular.logger.sqlite_logger import SQLiteLogger
from lotlan_schedular.defines import SQLCommands

# uninstall possible old lotlan_schedular packages
# so current code is used not old one
os.system("pip3 uninstall lotlan_schedular")

file_names = sorted(helpers.get_lotlan_file_names("etc/examples/Scheduling/"))
content = []
for i, file_ in enumerate(file_names):
    file_ = open(file_, "r")
    content.append(file_.read())

def run_transport_order_steps(task_uuid, material_flow):
    material_flow.fire_event(task_uuid, Event("moved_to_location", "", "Boolean", value=True))
    material_flow.fire_event(task_uuid, Event("moved_to_location", "", "Boolean", value=True))

def get_material_flow(test_number):
    lotlan_logic = LotlanSchedular(content[test_number], True)
    return lotlan_logic.get_materialflows()

def test_simple_task():
    material_flows = get_material_flow(0)

    material_flow = material_flows[0]
    material_flow.start()
    
    material_flow.fire_event("0",
                                Event("task_finished", "",
                                "Boolean", value=True))  # should not be allowed

    material_flow.fire_event("0", Event("to_done", "", "Boolean", value=True))
    material_flow.fire_event("0", Event("moved_to_location", "", "Boolean", value=True))

    material_flow.fire_event("0", Event("moved_to_location", "", "Boolean", value=True))

def test_triggered_by():
    material_flows = get_material_flow(1)

    material_flow = material_flows[0]
    material_flow.start()

    material_flow.fire_event("0", Event("buttonPressed", "", "Boolean", value=False))

    material_flow.fire_event("0", Event("buttonPressed", "", "Boolean", value=True))

    run_transport_order_steps("0", material_flow)

def test_finished_by():
    material_flows = get_material_flow(2)

    material_flow = material_flows[0]
    material_flow.start()

    material_flow.fire_event("0", Event("buttonPressed", "", "Boolean", value=False))
    material_flow.fire_event("0", Event("buttonPressed", "", "Boolean", value=True))

def test_trb_fb():
    material_flows = get_material_flow(3)

    material_flow = material_flows[0]
    material_flow.start()

    material_flow.fire_event("0", Event("buttonPressed", "", "Boolean", value=True))

    run_transport_order_steps("0", material_flow)

    material_flow.fire_event("0", Event("buttonPressed", "", "Boolean", value=True))  # should not be allowed
    material_flow.fire_event("0", Event("buttonPressed2", "", "Boolean", value=True))

def test__loop():
    material_flows = get_material_flow(4)

    material_flow = material_flows[0]
    material_flow.start()

    run_transport_order_steps("0", material_flow)
    run_transport_order_steps("0", material_flow)
    run_transport_order_steps("0", material_flow)

def test_two_tasks():
    material_flows = get_material_flow(5)

    material_flow_1 = material_flows[0]
    material_flow_2 = material_flows[1]
    material_flow_1.start()
    material_flow_2.start()

    run_transport_order_steps("0", material_flow_1)
    run_transport_order_steps("0", material_flow_2)

def test_triggered_by_and():
    material_flows = get_material_flow(6)

    material_flow = material_flows[0]
    material_flow.start()

    material_flow.fire_event("0", Event("buttonPressed", "", "Boolean", value=True))
    material_flow.fire_event("0", Event("buttonPressed2", "", "Boolean", value=True))
    material_flow.fire_event("0", Event("buttonPressed", "", "Boolean", value=False))

    run_transport_order_steps("0", material_flow)

def test_triggered_by_or():
    material_flows = get_material_flow(7)

    material_flow = material_flows[0]
    material_flow.start()

    material_flow.fire_event("0", Event("buttonPressed2", "", "Boolean", value=True))

    run_transport_order_steps("0", material_flow)

def test_triggered_by_xor():
    material_flows = get_material_flow(8)

    material_flow = material_flows[0]
    material_flow.start()

    material_flow.fire_event("0", Event("buttonPressed", "", "Boolean", value=True))
    material_flow.fire_event("0", Event("buttonPressed2", "", "Boolean", value=False))

    run_transport_order_steps("0", material_flow)

def test__loop_trb_fb():
    material_flows = get_material_flow(9)

    material_flow = material_flows[0]
    material_flow.start()

    material_flow.fire_event("0", Event("buttonPressed", "", "Boolean", value=True))

    run_transport_order_steps("0", material_flow)

    material_flow.fire_event("0", Event("buttonPressed2", "", "Boolean", value=True))
    material_flow.fire_event("0", Event("buttonPressed", "", "Boolean", value=True))

    run_transport_order_steps("0", material_flow)

    material_flow.fire_event("0", Event("buttonPressed2", "", "Boolean", value=True))

def test_tos_triggered_by():
    material_flows = get_material_flow(10)

    material_flow = material_flows[0]
    material_flow.start()

    material_flow.fire_event("0", Event("buttonPressed", "", "Boolean", value=True))

    run_transport_order_steps("0", material_flow)

def test_tos_finished_by():
    material_flows = get_material_flow(11)

    material_flow = material_flows[0]
    material_flow.start()

    material_flow.fire_event("0", Event("moved_to_location", "", "Boolean", value=True))
    material_flow.fire_event("0", Event("buttonPressed", "", "Boolean", value=True))
    material_flow.fire_event("0", Event("moved_to_location", "", "Boolean", value=True))

def test_on_done():
    material_flows = get_material_flow(12)

    material_flow = material_flows[0]
    material_flow.start()

    run_transport_order_steps("0", material_flow)
    run_transport_order_steps("1", material_flow)

def test_on_done_and_other_task():
    material_flows = get_material_flow(13)

    material_flow_1 = material_flows[0]
    material_flow_2 = material_flows[1]
    material_flow_1.start()
    material_flow_2.start()

    run_transport_order_steps("0", material_flow_1)
    run_transport_order_steps("0", material_flow_2)

    run_transport_order_steps("1", material_flow_1)

def test_on_done_with_many_tasks():
    material_flows = get_material_flow(14)

    material_flow = material_flows[0]
    material_flow.start()

    run_transport_order_steps("0", material_flow)
    run_transport_order_steps("1", material_flow)
    run_transport_order_steps("2", material_flow)
    run_transport_order_steps("3", material_flow)
    run_transport_order_steps("4", material_flow)

def test_task_sync():
    material_flows = get_material_flow(15)

    material_flow = material_flows[0]
    material_flow.start()

    run_transport_order_steps("0", material_flow)
    run_transport_order_steps("2", material_flow)
    run_transport_order_steps("1", material_flow)

def test_same_events_in_tb_and_fb():
    material_flows = get_material_flow(16)

    material_flow = material_flows[0]
    material_flow.start()

    material_flow.fire_event("0", Event("buttonPressed", "", "Boolean", value=True))
    material_flow.fire_event("0", Event("buttonPressed2", "", "Boolean", value=False))
    material_flow.fire_event("0", Event("buttonPressed", "", "Boolean", value=False))

    run_transport_order_steps("0", material_flow)

    material_flow.fire_event("0", Event("buttonPressed2", "", "Boolean", value=True))
    material_flow.fire_event("0", Event("buttonPressed", "", "Boolean", value=False))

def test_same_event_in_condition():
    material_flows = get_material_flow(17)

    material_flow = material_flows[0]
    material_flow.start()

    material_flow.fire_event("0", Event("buttonPressed2", "", "Boolean", value=True))
    material_flow.fire_event("0", Event("buttonPressed", "", "Boolean", value=True))

    run_transport_order_steps("0", material_flow)

def test_tb_with_integer():
    material_flows = get_material_flow(18)

    material_flow = material_flows[0]
    material_flow.start()

    material_flow.fire_event("0", Event("sensor", "", "Integer", value=3))
    material_flow.fire_event("0", Event("sensor", "", "Integer", value=51))
    material_flow.fire_event("0", Event("sensor2", "", "Integer", value=5))

    run_transport_order_steps("0", material_flow)

def test_tb_with_string():
    material_flows = get_material_flow(19)

    material_flow = material_flows[0]
    material_flow.start()

    material_flow.fire_event("0", Event("terminal", "", "String", value="ab"))
    material_flow.fire_event("0", Event("terminal", "", "String", value="abc"))

    run_transport_order_steps("0", material_flow)

def main():
    test_simple_task()
    time.sleep(1)
    test_triggered_by()
    time.sleep(1)
    test_finished_by()
    time.sleep(1)
    test_trb_fb()
    time.sleep(1)
    test__loop()
    time.sleep(1)
    test_two_tasks()
    time.sleep(1)
    test_triggered_by_and()
    time.sleep(1)
    test_triggered_by_or()
    time.sleep(1)
    test_triggered_by_xor()
    time.sleep(1)
    test__loop_trb_fb()
    time.sleep(1)
    test_tos_triggered_by()
    time.sleep(1)
    test_tos_finished_by()
    time.sleep(1)
    test_on_done()
    time.sleep(1)
    test_on_done_and_other_task()
    time.sleep(1)
    test_on_done_with_many_tasks()
    time.sleep(1)
    test_task_sync()
    time.sleep(1)
    test_same_events_in_tb_and_fb()
    time.sleep(1)
    test_same_event_in_condition()
    time.sleep(1)
    test_tb_with_integer()
    time.sleep(1)
    test_tb_with_string()

if __name__ == "__main__":
    main()
