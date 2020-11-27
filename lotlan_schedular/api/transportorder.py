""" Contains TransportOrder class """

from enum import IntEnum

# local sources
from lotlan_schedular.api.transportorder_step import TransportOrderStep

class TransportOrder:
    """
        Represents a TransportOrder in lotlan code
        as well as in scheduling
    """

    class TransportOrderState(IntEnum):
        WAIT_FOR_TRIGGERED_BY = 0
        TRANSPORT_ORDER_STARTED = 1
        WAIT_FOR_FINISHED_BY = 2
        FINISHED = 3

    def __init__(self):
        self.uuid = ""
        self.to_step_from = TransportOrderStep()
        self.to_step_to = TransportOrderStep()
        self.from_parameters = []
        self.to_parameters = []
        self.task_name = ""
        self.state = None

    def __str__(self):
        return (("\n UUID: {}\n To_Step_From: \t\t {} \n To_Step_To: \t\t {} \n\t")
                .format(self.uuid, self.to_step_from, self.to_step_to))

    def __repr__(self):
        return (("\n UUID: {}\n To_Step_From: \t\t {} \n To_Step_To: \t\t {} \n\t")
                .format(self.uuid, self.to_step_from, self.to_step_to))
