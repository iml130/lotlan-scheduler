# Location

A *Location* is an *Instance* and has to be passed in the *Location* statement of a *TransportOrderStep*. Each *TransportOrderStep* object holds a *Location* reference. For example there is a *Location* instance for each *TransportOrderStep* in a *TransportOrder*: one for loading and one for unloading.

```python
class Location:
    """ Represents a LoTLan Location instance """
    def __init__(self, logical_name, physical_name, location_type):
        self.logical_name = logical_name
        self.physical_name = physical_name
        self.location_type = location_type

    def __repr__(self):
        return (("Logical_Name: {}, Physical_Name: {}, Location_Type: {}")
                .format(self.logical_name, self.physical_name, self.location_type))
```

## Attributes

* logical_name: name for use in the *LoTLan* file 
* physical_name: name which is used in your backend
* location_type: type of the *Location*, e.g 'SmallLoadCarrier'