# LoTLan Scheduler
![Unit-Tests](https://github.com/iml130/lotlan-scheduler/workflows/Unit-Tests/badge.svg?branch=feature%2Fgithub-action-for-unittests)

Scheduler for [LoTLan](https://lotlan.readthedocs.io/en/latest/) tasks. Parses LoTLan files and accepts events defined in the files to schedule.

The repository for the LoTLan grammar can be found [here](https://github.com/iml130/LoTLan)
## Task examples

You can find many LoTLan files / examples in the LoTLan Scheduler [repository](https://github.com/iml130/lotlan-scheduler) or in the official [Documentation](https://lotlan-scheduler.readthedocs.io)

## Quickstart / Example

Here is an example how the scheduler can be used
```python
import sys

from lotlan_scheduler.scheduler import LotlanScheduler
from lotlan_scheduler.api.event import Event

# gets called for each materialflow that is waiting for
# the triggeredBy condition to be satisfied
# event information contains info about the events in tb
def cb_triggered_by(mf_uuid, _uuid, event_information):
    print("cb_triggered_by from mf: " + str(mf_uuid))
    print("UUID: " + str(_uuid), "Event_Info: " + str(event_information))
    # foreach event in event_information

# gets called when triggeredBy condition is satisfied
# transport_orders contains the next transport orders which 
# can be executed
def cb_next_to(mf_uuid, transport_orders):
    print("cb_next_to from mf: " + str(mf_uuid))
    print(str(transport_orders))

# gets called for each materialflow that is waiting for
# the finishedBy condition to be satisfied
# event information contains info about the events in fb
def cb_finished_by(mf_uuid, _uuid, event_information):
    print("cb_finished_by from mf: " + str(mf_uuid))
    print("UUID: " + str(_uuid), "Event_Info: " + str(event_information))

# gets called if a task with the id _uuid has finished
def cb_task_finished(mf_uuid, _uuid):
    print("cb_task_finished from mf: " + str(mf_uuid))
    print("task with uuid " + str(_uuid) + " finished")

# gets called if every task is finished
# will never be called if the LoTLan file contains a cycle
def cb_all_finished(mf_uuid):
    print("cb_all_finished from mf: " + str(mf_uuid))


def main():
    test_flag = False
    lotlan_string = ""

    if len(sys.argv) >= 2:
        if sys.argv[1] == "--test":
            test_flag = True
            with open(sys.argv[2], 'r') as file:
                lotlan_string = file.read()
        else:
            with open(sys.argv[1], 'r') as file:
                lotlan_string = file.read()

        lotlan_logic = LotlanScheduler(lotlan_string, test_flag)
        material_flows = lotlan_logic.get_materialflows()

        for material_flow in material_flows:
            material_flow.register_callback_triggered_by(cb_triggered_by)
            material_flow.register_callback_next_to(cb_next_to)
            material_flow.register_callback_finished_by(cb_finished_by)
            material_flow.register_callback_task_finished(cb_task_finished)
            material_flow.register_callback_all_finished(cb_all_finished)
            material_flow.start()

        material_flow_running = True
        while (material_flow_running):
            _input = str(input("Wait for input:>"))
            mf_number = 0
            uid = 0
            input_name = "buttonPressed"
            input_value = "True"

            if _input != "":
                mf_number, uid, input_name, input_value = _input.split(" ")

            mf_number = int(mf_number)

            if mf_number < len(material_flows):
                material_flows[mf_number].fire_event(str(uid), Event(input_name, "", "bool", input_value == "True"))

            # check if a material flow is still running
            # if every material flow is finished we are done otherwise continue
            material_flow_running = False
            for mf in material_flows:
                if mf.is_running() is True:
                    material_flow_running = True

if __name__ == '__main__':
    main()

```

## License
LoTLan Scheduler is licensed under the terms of the Apache license. See [LICENCSE](./LICENSE) for more information.

## Contributors
Peter Detzner, Maximilian Hoerstrup, Dominik Lux


## Conference

P. Detzner, T. Kirks and J. Jost, "[A Novel Task Language for Natural Interaction in Human-Robot Systems for Warehouse Logistics](https://ieeexplore.ieee.org/document/8845336)", 2019 14th International Conference on Computer Science & Education (ICCSE), Toronto, ON, Canada, 2019, pp. 725-730.
