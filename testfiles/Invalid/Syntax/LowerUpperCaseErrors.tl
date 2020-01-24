Location PickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"
End

Location dropoffItem
    name = "ws1_dropoff"
    type = "SmallLoadCarrier"
End

TransportOrderStep LoadStorage # error: instance name has to start with an lowercase Character
    Location pickupItem 
End

TransportOrderStep unloadWorkstation1
    Location DropoffItem # error: instance name has to start with an lowercase Character
End

Task HelloTask # error: task name has to start with an lowercase Character
    Transport
    From loadStorage
    To unloadWorkstation1
End