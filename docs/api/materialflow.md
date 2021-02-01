# Materialflow

A *Materialflow* is a set of at least one *Task* which describes a materialflow in logistics.
It is possible that there are multiple *Materialflows* in a *LoTLan* file, for example two individual *Tasks* without any concatenation.

## Callback registration

*Materialflow* objects can call 5 different callback functions depending on the current states of the 
internal petri nets of the *Tasks*. The class also provides the corresponding methods to register the callback functions.
Additionally you can use each of these functions to add more than one callback.

```python
def register_callback_triggered_by(self, callback):
```
If a *Task* can be started and has a *TriggeredBy* defined, all registered callback functions will be called.

The signature of the callback function should be: *Materialflow* uuid, *TransportOrder* uuid, list of *Events*

```python
def register_callback_finished_by(self, callback):
```
Functions passed in to this method will be called when the *TransportOrder* is done which means a "to_done" event was sent and a *FinishedBy* was defined.

The signature of the callback function should be the same as above.


```python
def register_callback_next_to(self, callback):
```
If a *Task* was started and the *TriggeredBy* condition is satisfied or there is no *TriggeredBy* all callback functions registered here will be called
    
The signature of the callback function should be: *Materialflow* uuid, dict of *TransportOrders*


```python
def register_callback_task_finished(self, callback):
```
If a *Task* is finished functions registered here are being called.

The signature of the callback function should be: *Materialflow* uuid, *TransportOrder*/*Task* uuid

```python
def register_callback_all_finished(self, callback):
```
If all *Tasks* in a *Materialflow* are finished functions registered here are being called.

The signature of the callback function should be: *Materialflow* uuid

```python
def register_callback_pickup_finished(self, callback):
```
Functions passed in to this method will be called when the Pickup TransportOrderStep 
of a task is finished

The signature of the callback function should be: *Materialflow* uuid, *TransportOrder*/*Task* uuid


```python
def register_callback_delivery_finished(self, callback):
```
Functions passed in to this method will be called when the Delivery TransportOrderStep
of a task is finished

The signature of the callback function should be: *Materialflow* uuid, *TransportOrder*/*Task* uuid


## Methods for running

```python
def start(self):
```
Starts scheduling of the *Tasks*. If a *Task* has a *TriggeredBy* statement it waits for incoming events, otherwise the *TransportOrder* can be executed and so next_to is called.


```python
def is_running(self):
```
Returns True if the *Materialflow* is still running which means there are still tasks to be executed.
Will always return False if the *Materialflow* contains a loop.

```python
def fire_event(self, uuid_, event):
```
Fires given *Event* to the corresponding *Task* which contains a *TransportOrder* with the given uuid.
If the *Event* was awaited it will be processed otherwise nothing happens. (For example when an event from *FinishedBy* is fired when *TriggeredBy* is still not passed)

## Attributes

* uuid_: the uuid of the *Materialflow*
* name: name of the *Materialflow*