class Location:
    def __init__(self, logical_name, physical_name, location_type):
        self.logical_name = logical_name
        self.physical_name = physical_name
        self.location_type = location_type

    def validate(self, _value):
        # eval the type + value
        return type(_value).__name__ == self.event_type

    def __repr__(self):
        return (("Logical_Name: {}, Physical_Name: {}, Location_Type: {}")
                .format(self.logical_name, self.physical_name, self.location_type))
