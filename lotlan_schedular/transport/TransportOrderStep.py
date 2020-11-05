class TransportOrderStep(object):
    '''
        Represents a TransportOrderStep and all its data
    '''

    def __init__(self):
        self.name = None
        self.location = ""
        self.triggered_by = ""
        self.finished_by = ""
        self.parameters = []
        self.on_done = []
        self.context = None
        self.context_dict = {}
        self.triggered_by_events = []
        self.finished_by_events = []

    def __repr__(self):
        return ("Location: {} \n TriggeredBy: {} \n FinishedBy: {} \n Parameters: {} \n OnDone: {} \n"
                .format(self.location, self.triggered_by, self.finished_by, self.parameters, self.on_done))
