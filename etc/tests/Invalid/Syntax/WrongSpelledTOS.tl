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
End

Task helloTask
    Transport
    from loadStorage # 'from' is not correct it has to be 'From'
    To unloadWorkstation
End