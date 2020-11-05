Location pickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"
End

Location dropoffItem
    name = "ws1_dropoff"
    type = "SmallLoadCarrier"
End

TransportOrderStep loadStorage
    Location pickupItem 
End

TransportOrderStep unloadWorkstation
    Location dropoffItem
End

Task helloTask
    Transport
    From loadStorage
    To unloadWorkstation
    
    Repeat 5  # error: you can only use either of them
    OnDone helloTask
End