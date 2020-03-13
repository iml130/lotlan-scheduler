__author__ = "Maximilian Hörstrup"
__version__ = "0.0.1"
__maintainer__ = "Maximilian Hörstrup"

class TransportOrderStep(object):
    def __init__(self):
        self.name = None # String Name of Task
        self.locations = []
        self.triggeredBy = [] # List of Triggers
        self.finishedBy = []
        self.parameters = []
        self.onDone = [] # Reference to the next Tasks
        self.context = None
    
    def __repr__(self):
        return ("Location: {} \n TriggeredBy: {} \n FinishedBy: {} \n Parameters: {} \n OnDone: {} \n"
                .format(self.locations, self.triggeredBy, self.finishedBy, self.parameters, self.onDone))