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
    OnDone HelloTask
    OnDone SameTask # error: there is already a OnDone statement
End

Task helloTask
    Transport
    From loadStorage
    To unloadWorkstation1
End

Task sameTask
    Transport
    From loadStorage
    To unloadWorkstation1
End