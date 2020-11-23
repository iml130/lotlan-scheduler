# API

In this chapter we will give more information about the API classes.

## Callbacks

Materialflow objects can call 5 different callbacks depending on the current states of the 
internal petri nets of the tasks. The class also provides the corresponding methods to register the callback functions



* Wait for TriggeredBy Events
* Wait for FinishedBy Events
* Task Finished
* All Finished
* Next Transport Order


## TransportOrder
The base of a task is the TransportOrder. It is the elemental operation. Contains of a uuid to identify later which event is for which transportOrder

* Consists of 2 TransportOrderSteps
* Task name

## TransportOrderStep



## Location
Locations are defined and then used in TransportOrderSteps.

## Event
The event class describes a real world event caused by, e.g a sensor. Events can be used in TriggeredBy and FinishedBy expressions in the LoTLan file.