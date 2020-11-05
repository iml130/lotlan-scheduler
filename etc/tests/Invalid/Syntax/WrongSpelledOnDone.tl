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
    onDone helloTask22  # error: 'onDone' is not correct it has to be 'OnDone'
End

Task helloTask2
    Transport
    From loadStorage
    To unloadWorkstation
End