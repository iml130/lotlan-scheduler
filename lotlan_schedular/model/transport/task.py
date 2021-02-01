""" Contains Task class """

class Task(object):
    '''
        Represents a Task and all its data
    '''

    def __init__(self):
        self.name = None
        self.triggered_by = ""
        self.finished_by = ""
        self.transport_order = None
        self.on_done = []
        self.repeat = ""
        self.constraints = ""
        self.context = None
        self.context_dict = {}
        self.triggered_by_events = []
        self.finished_by_events = []

    def __repr__(self):
        return (("\n TriggeredBy: {} \n FinishedBy: {} \n TransportOrder: \n{}"
                 "\n OnDone: {} \n Repeat: {} \n Constraints: {} \n ")
                .format(self.triggered_by, self.finished_by, self.transport_order,
                self.on_done, self.repeat, self.constraints))
