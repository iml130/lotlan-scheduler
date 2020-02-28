__author__ = "Maximilian Hörstrup"
__version__ = "0.0.1"
__maintainer__ = "Maximilian Hörstrup"

class TransportOrder(object):
    def __init__(self):
        self.pickupFrom = None# From Instance
        self.deliverTo = None # Target Instance

class TransportOrderStep(object):
    def __init__(self):
        self.name = None # String Name of Task
        self.locations = []
        self.triggeredBy = [] # List of Triggers
        self.finishedBy = []
        self.onDone = [] # Reference to the next Tasks
        self.context = None