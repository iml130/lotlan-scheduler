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
        TASK_STARTED = 0
        WAIT_FOR_TRIGGERED_BY = 1
        TRANSPORT_ORDER_STARTED = 2
        WAIT_FOR_FINISHED_BY = 3
        FINISHED = 4

    def __init__(self):
        self.uuid = ""
        self.pickup_tos = TransportOrderStep()
        self.delivery_tos = TransportOrderStep()
        self.from_parameters = []
        self.to_parameters = []
        self.task_name = ""
        self.state = None

    def __str__(self):
        return (("\n UUID: {}\n To_Step_From: \t\t {} \n To_Step_To: \t\t {} \n\t")
                .format(self.uuid, self.pickup_tos, self.delivery_tos))

    def __repr__(self):
        return (("\n UUID: {}\n To_Step_From: \t\t {} \n To_Step_To: \t\t {} \n\t")
                .format(self.uuid, self.pickup_tos, self.delivery_tos))
