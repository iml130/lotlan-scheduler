Location pickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"
End

Location dropoffItem
    name = "ws1_dropoff"
    type = "SmallLoadCarrier"
End

TransportOrderStep loadStorage
    location pickupItemm
End

TransportOrderStep unloadWorkstation1
    Location dropoffItem2  # error: the instace name was spelled wrong so the validator cant find the correct instance
End

Task helloTask
    Transport
    From loadStorage
    To unloadWorkstation1
End