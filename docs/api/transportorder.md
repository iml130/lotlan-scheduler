# TransportOrder

A *TransportOrder* is a task, to move goods from a specific source to a dedicated destination. The *TransportOrder* consists of two TransportOrderSteps, defining the pickup and the delivery.
If a *TransportOrder* is ready, for example if the *TriggeredBy* conditions of the corresponding task are fullfilled, a *TransportOrder* object is passed as parameter of the registered callback function.

```python
class TransportOrder:
    """
        Represents a TransportOrder in lotlan code
        as well as in scheduling
    """
    def __init__(self):
        self.uuid = ""
        self.to_step_from = TransportOrderStep()
        self.to_step_to = TransportOrderStep()
        self.from_parameters = []
        self.to_parameters = []
        self.task_name = ""

    def __str__(self):
        return (("\n UUID: {}\n To_Step_From: \t\t {} \n To_Step_To: \t\t {} \n\t")
                .format(self.uuid, self.to_step_from, self.to_step_to))

    def __repr__(self):
        return (("\n UUID: {}\n To_Step_From: \t\t {} \n To_Step_To: \t\t {} \n\t")
                .format(self.uuid, self.to_step_from, self.to_step_to))
```

## Attributes

* uuid: the uuid of the *TransportOrder*
* to_step_from: Object of *TransportOrderStep* defined in 'From'
* to_step_to: Object of *TransportOrderStep* defined in 'To'
* from_parameters: *Parameters* defined in 'From' *TransportOrderStep*
* to_parameters: *Parameters* defined in 'To' *TransportOrderStep*
* task_name: name of the *Task* this *TransportOrder* is in