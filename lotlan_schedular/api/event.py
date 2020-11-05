class Event:
    def __init__(self, logical_name, physical_name, event_type, comparator=None, value=None):
        self.logical_name = logical_name
        self.physical_name = physical_name
        self.event_type = event_type
        self.comparator = comparator
        if value is not None:
            self.value = value
    '''
    def set_value(self, _value):
        if self.validate(_value):
            self.value = _value

    def validate(self, _value):
        # eval the type + value
        return type(_value).__name__ == self.event_type

    def __repr__(self):
        return (("Logical_Name: {}, Physical_Name: {}, Event_Type: {}, Comparator: {}, Value: {}")
                .format(self.logical_name, self.physical_name, self.event_type, self.comparator, self.value))
    '''