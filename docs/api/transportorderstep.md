# TransportOrderStep

A *TransportOrderStep* is a *Task*-fragment and is used in a *TransportOrder* to describe a destination.
The *TransportOrderStep* needs a location and can optionally have a TriggeredBy and FinishedBy statement, Parameters, OnDone.

```python
class TransportOrderStep:
    """
        Represents a TransportOrderStep in lotlan code
        as well as in scheduling
    """

    def __init__(self):
        self.name = ""
        self.location = ""
        self.triggered_by_statements = ""
        self.finished_by_statements = ""
        self.parameters = []
        self.on_done = []
        self.context = None
        self.context_dict = {}
        self.triggered_by = []
        self.finished_by = []
        
    def __str__(self):
        return (("\n\t Name: {}\n\t Location: {}\n\t TriggeredBy:\t{}\n\t FinishedBy:\t{}\n\t")
                .format(self.name, self.location, self.triggered_by, self.finished_by))
```

## Attributes

* name: logical name of the *TransportOrderStep*
* location: *Location* object
* triggered_by: list of awaited *TriggeredBy Events*
* finished_by: list of awaited *FinishedBy Events*
* parameters: defined parameters 
* on_done: *Tasks* which get started if the TOS is finished

The attributes triggered_by_statements, finsihed_by_statements, context and context_dict are used internally for syntax and semantic checks and should not be used.