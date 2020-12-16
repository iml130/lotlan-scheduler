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
        """ Represents the current state of the Transport Order """
        TASK_STARTED = 0
        TASK_WAIT_FOR_TRIGGERED_BY = 1
        PICKUP_WAIT_FOR_TRIGGERED_BY = 2
        PICKUP_STARTED = 3
        MOVED_TO_PICKUP = 4
        WAIT_FOR_LOADING = 5
        PICKUP_FINISHED = 6
        DELIVERY_WAIT_FOR_TRIGGERED_BY = 7
        DELIVERY_STARTED = 8
        MOVED_TO_DELIVERY = 9
        WAIT_FOR_UNLOADING = 10
        DELIVERY_FINISHED = 11
        TASK_WAIT_FOR_FINISHED_BY = 12
        FINISHED = 13


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
