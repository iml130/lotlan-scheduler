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

TransportOrderStep unloadWorkstation1
    Location dropoffItem
    OnDone helloTask2 # error: the given tasks doesnt exist
End

Task helloTask
    Transport
    From loadStorage
    To unloadWorkstation1
End