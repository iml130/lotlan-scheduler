# Event

The *Event* class describes a real world event caused by, e.g a sensor. *Events* can be used in *TriggeredBy* and *FinishedBy* expressions.

*Event* objects are used to fire events and to notify your application about the events a task needs to trigger or finish a *TransportOrder*.

## Attributes

* logical_name: name for use in the *LoTLan* file 
* physical name: name which is used in your backend
* event_type: the type of an event, e.g string or boolean
* comparator: describes which comparation you defined, e.g '==', '<', '>'
* value: value of the *Event* 