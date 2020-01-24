Location pickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"

Location dropoffItem
    name = "ws1_dropoff"
    type = "SmallLoadCarrier"
# error: missing End

TransportOrderStep loadStorage
    Location pickupItem 
End

TransportOrderStep unloadWorkstation1
    Location dropoffItem
# error: missing End

Task helloTask
    Transport
    From loadStorage
    To unloadWorkstation1
# error: missing End