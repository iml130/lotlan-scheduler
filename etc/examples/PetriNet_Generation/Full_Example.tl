Location pickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"
End

Location dropoffItem
    name = "ws1_dropoff"
    type = "SmallLoadCarrier"
End

Event buttonPressed
    name = "bp"
    type = "Boolean"
End

Event lightSensorTriggered
    name = "ls_t"
    type = "Boolean"
End

TransportOrderStep loadStorage
    Location pickupItem 
End

TransportOrderStep unloadWorkstation1
    Location dropoffItem
End

Task helloTask
    Transport
    From loadStorage
    To unloadWorkstation1
    TriggeredBy !(helloTask2.IsDone or helloTask3.IsDone) and (buttonPressed or lightSensorTriggered)
    OnDone helloTask, helloTask2, helloTask3
End

Task helloTask2
    Transport
    From loadStorage
    To unloadWorkstation1
End

Task helloTask3
    Transport
    From loadStorage
    To unloadWorkstation1
End

Task helloTask4
    Transport
    From loadStorage
    To unloadWorkstation1
End

