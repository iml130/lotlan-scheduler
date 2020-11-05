## Primitives


A *Primitive* summarizes and specifies a set of *Instances*. All *Instances* have the same member variables as their corresponding Primitive. \
Primitives are declared in an additional template file and should not be changed by the user.
Currently there are 4 Primitves implemented:
* Location
* Event
* Time 
* Constraint

The Location *Primitive* is definied as followed:

```text
template Location
    type = ""
    name = ""
End
```

*Location* specifies two member variables, a *type* and a *value*. These attributes can be later on accessed inside the instances. Every TransportOrderStep needs to provide a *Location* Instance.

The *Primitives* *Event* and *Time* are defined as following:

```text
template Event
    name = ""
    type = ""
End

template Time
    timing = ""
End
```

*Event* and *Time* instances can be used in TriggeredBy or FinisheredBy statements.

And finally the Constraint Primitive:

```text
template Constraint
    type = ""
End
```
*Constraint* instances can be used in Tasks


Currently only the following 4 primitives are defined: `name`, `type`, `timing`, `constraint`