""" Contains TransportOrder class """

from enum import IntEnum

# local sources
from lotlan_scheduler.api.transportorder_step import TransportOrderStep

class TransportOrder:
    """
        Represents a TransportOrder in lotlan code
        as well as in scheduling
    """

    class TransportOrderState(IntEnum):
        """ Represents the current state of the Transport Order """
        TASK_STARTED = 0
        TASK_WAIT_FOR_TRIGGERED_BY = 1
        PICKUP_WAIT_FOR_TRIGGERED_BY = 2
        PICKUP_STARTED = 3
        WAIT_FOR_LOADING = 4
        PICKUP_FINISHED = 5
        DELIVERY_WAIT_FOR_TRIGGERED_BY = 6
        DELIVERY_STARTED = 7
        WAIT_FOR_UNLOADING = 8
        DELIVERY_FINISHED = 9
        TASK_WAIT_FOR_FINISHED_BY = 10
        FINISHED = 11

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
