Location pickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"
End

Location pickupItem2
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
End

Task helloTask
    Transport
    From loadStorage
    To unloadWorkstation1
    Repeat		5
    Repeat		1 # error: an repeat statement was already definied
End