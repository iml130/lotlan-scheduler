# Event

The *Event* class describes a real world event caused by, e.g a sensor. *Events* can be used in *TriggeredBy* and *FinishedBy* expressions. They can also be connected by boolean operators so you can create more complex statements. Each event instance used in such a statement will be added into a list with the used comparator and value set to the expected value.

*Event* objects are used to fire events and to notify your application about the events a *Task* needs to trigger or finish a *TransportOrder* (These *Events* are in a list as described above)

```python
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
```

## Attributes

* logical_name: name for use in the *LoTLan* file 
* physical name: name which is used in your backend
* event_type: the type of an event, e.g string or boolean
* comparator: describes which comparation you defined, e.g '==', '<', '>'
* value: value of the *Event* 