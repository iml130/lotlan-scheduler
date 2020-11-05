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
    TriggeredBy buttonPressed or !lightSensorTriggered and helloTask2IsDone 
End

Task helloTask2
    Transport
    From loadStorage
    To unloadWorkstation1
End