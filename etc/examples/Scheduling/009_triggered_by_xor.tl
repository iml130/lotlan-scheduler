Location pickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"
End

Location dropoffItem
    name = "ws1_dropoff"
    type = "SmallLoadCarrier"
End

Event buttonPressed
    name = "button"
    type = "Boolean"
End

Event buttonPressed2
    name = "button"
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
    TriggeredBy (!buttonPressed and buttonPressed2) or (buttonPressed and !buttonPressed2)
End