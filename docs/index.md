![Example introduction](/img/LoTLan.svg)

This documentation contains information about the schedular for the **Lo**gistic **T**ask **Lan**guage (LoTLan).

If you are more interested in LoTLan itself please visit the official [LoTLan docu](https://lotlan.readthedocs.io/en/latest/).

# What does the schedular do?
The LoTLan Schedular parses LoTLan files and processes given events. If a Task is for example triggered by a button that has to be pressed, the schedular will pass you the corresponding TransportOrder on receive of the 'buttonPressed' *Event*.

You can put in all type of *Events* following the syntax described in the [LoTLan docu](https://lotlan.readthedocs.io/en/latest/lotlan/primitives.html#event). Depending on the events the next state of the *Task* is set.
You can register callback functions which are called on certain states of the Task (Wait for triggeredBy, TransportOrder is done...). If a *TransportOrder* is ready to be executed the corresponding callback function will be called and you receive the *TransportOrder* object.

Detailed information about the process can be found [here](./api/materialflow.md)

# Get started

At first visit the [install guide](./install.md) and install the schedular. Afterwards you can check out our [tutorial](./tutorials/cli.md) for creating a CLI program to test the schedular or visit the [materialflow section](./api/materialflow.md)

