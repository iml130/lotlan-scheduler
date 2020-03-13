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
    Parameter liftHeight, unloadDirection
End

TransportOrderStep unloadWorkstation1
    Location dropoffItem
    Parameter unloadDirection
End

Task helloTask
    Transport
    From loadStorage 10 , "right",
    To unloadWorkstation1 "left"
End