""" Contains TransportOrderStep class """

class TransportOrderStep:
    """
        Represents a TransportOrderStep in lotlan code
        as well as in scheduling
    """

    def __init__(self):
        self.name = ""
        self.location = ""
        self.triggered_by_statements = ""
        self.finished_by_statements = ""
        self.parameters = []
        self.on_done = []
        self.context = None
        self.context_dict = {}
        self.triggered_by = []
        self.finished_by = []
   
    def __str__(self):
        return (("\n\t Name: {}\n\t Location: {}\n\t TriggeredBy:\t{}\n\t FinishedBy:\t{}\n\t")
                .format(self.name, self.location, self.triggered_by, self.finished_by))
