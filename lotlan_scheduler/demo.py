""" Contains main program example for scheduler """

# standard libraries
import sys
import os

sys.path.append(os.path.abspath("../lotlan_scheduler"))

# local sources
from lotlan_scheduler.scheduler import LotlanScheduler
from lotlan_scheduler.api.event import Event


def cb_triggered_by(mf_uuid, uuid_, event_information):
    print("cb_triggered_by from mf: " + str(mf_uuid))
    print("UUID: " + str(uuid_), "Event_Info: " + str(event_information))
    # foreach event in event_information


def cb_next_to(mf_uuid, transport_orders):
    print("cb_next_to from mf: " + str(mf_uuid))
    print(str(transport_orders))


def cb_finished_by(mf_uuid, uuid_, event_information):
    print("cb_finished_by from mf: " + str(mf_uuid))
    print("UUID: " + str(uuid_), "Event_Info: " + str(event_information))


def cb_task_finished(mf_uuid, uuid_):
    print("cb_task_finished from mf: " + str(mf_uuid))
    print("task with uuid " + str(uuid_) + " finished")


def cb_all_finished(mf_uuid):
    print("cb_all_finished from mf: " + str(mf_uuid))


def main():
    test_flag = False
    lotlan_string = ""

    if len(sys.argv) >= 2:
        if sys.argv[1] == "--test":
            test_flag = True
            with open(sys.argv[2], "r") as file:
                lotlan_string = file.read()
        else:
            with open(sys.argv[1], "r") as file:
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
        while material_flow_running:
            input_str = str(input("Wait for input:>"))

            if input_str != "":
                mf_number, uid, input_type, input_name, input_value = input_str.split(" ")

                mf_number = int(mf_number)

                if mf_number < len(material_flows):
                    if input_type == "b":
                        input_type = "Boolean"
                        input_value = input_value == "True"
                    elif input_type == "i":
                        input_type = "Integer"
                        input_value = int(input_value)
                    elif input_type == "f":
                        input_type = "Float"
                        input_value = float(input_value)
                    elif input_type == "s":
                        input_type = "String"

                    material_flows[mf_number].fire_event(str(uid), Event(input_name, "",
                                                        input_type, value=input_value))

            # check if a material flow is still running
            # if every material flow is finished we are done otherwise continue
            material_flow_running = False
            for mf in material_flows:
                if mf.is_running() is True:
                    material_flow_running = True


if __name__ == "__main__":
    main()
