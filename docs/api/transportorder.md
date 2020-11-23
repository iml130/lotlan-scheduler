# TransportOrder

The base of a *Task* is the *TransportOrder*. Each *Task* has to define a TransportOrder.

## Attributes:

* uuid: the uuid of the *TransportOrder*
* to_step_from: Object of *TransportOrderStep* defined in 'From'
* to_step_to: Object of *TransportOrderStep* defined in 'To'
* from_parameters: *Parameters* defined in 'From' *TransportOrderStep*
* to_parameters: *Parameters* defined in 'To' *TransportOrderStep*
* task_name: name of the *Task* this *TransportOrder* is in