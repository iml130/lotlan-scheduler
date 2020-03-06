__author__ = "Maximilian Hörstrup"
__version__ = "0.0.1"
__maintainer__ = "Maximilian Hörstrup"

class TaskInfo(object):
    def __init__(self):
        self.name = None # Name of Task
        self.triggeredBy = [] # Triggers
        self.finishedBy = []
        self.transportOrders = [] # Transport Order (from|to)
        self.onDone = [] # Reference to the next Tasks
        self.repeat = []
        self.constraints = []
        self.context = None

    def __repr__(self):
        return (("TriggeredBy: {} \n FinishedBy: {} \n TransportOrder: \n OnDone: {} \n Repeat: {} \n Constraints: {} \n ")
                .format(self.triggeredBy, self.finishedBy, self.onDone, self.repeat, self.constraints))

class TransportOrder(object):
    def __init__(self):
        self.pickupFrom = None # From Instance
        self.deliverTo = None # Target Instance
        self.fromParameters = []
        self.toParameters = []

    def __repr__(self):
        return (("PickupFrom: {} \n  Parameters: {} \n DelieverTo: {} \n  Parameters: {}")
                .format(self.pickupFrom, self.fromParameters, self.deliverTo, self.toParameters))