Location pickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"
End

location dropoffItem # the keyword 'Location' was spelled wrong
    name = "ws1_dropoff"
    type = "SmallLoadCarrier"
End

TransportOrderStep loadStorage
    Location pickupItem
End


TransportOrderStepp unloadWorkstation # the keyword 'TransportOrderStep' was spelled wrong
    Location dropoffItem
End


Taskk helloTask # the keyword 'Task' was spelled wrong
    Transport
    From loadStorage
    To unloadWorkstation
End