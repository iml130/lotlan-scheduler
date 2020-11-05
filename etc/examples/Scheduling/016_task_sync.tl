Location pickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"
End

Location dropoffItem
    name = "ws1_dropoff"
    type = "SmallLoadCarrier2"
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
    OnDone helloTask3
End

Task helloTask2
    Transport
    From loadStorage
    To unloadWorkstation1
    OnDone helloTask3
End

Task helloTask3
    Transport
    From loadStorage
    To unloadWorkstation1
End