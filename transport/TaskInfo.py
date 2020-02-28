__author__ = "Maximilian Hörstrup"
__version__ = "0.0.1"
__maintainer__ = "Maximilian Hörstrup"

class TaskInfo(object):
    def __init__(self):
        self.name = None # Name of Task
        self.triggeredBy = [] # Triggers
        self.transportOrders = [] # Transport Order (from|to)
        self.onDone = [] # Reference to the next Tasks
        self.repeat = []
        self.finishedBy = []
        self.context = None