""" Contains Event class """

class Event:
    """ Represents a LoTLan Event instance """

    def __init__(self, logical_name, physical_name, event_type, comparator=None, value=None):
        self.logical_name = logical_name
        self.physical_name = physical_name
        self.event_type = event_type
        self.comparator = comparator
        self.value = value

    def __repr__(self):
        return (("Logical_Name: {}, Physical_Name: {}, Event_Type: {}, Comparator: {}, Value: {}")
                .format(self.logical_name, self.physical_name, self.event_type,
                        self.comparator, self.value))
