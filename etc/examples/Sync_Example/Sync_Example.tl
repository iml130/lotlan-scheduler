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

Task t1
    Transport
    From loadStorage
    To unloadWorkstation1
End

Task t2
    Transport
    From loadStorage
    To unloadWorkstation1
End

Task t3
    Transport
    From loadStorage
    To unloadWorkstation1
    TriggeredBy t1_is_done and t2_is_done
End