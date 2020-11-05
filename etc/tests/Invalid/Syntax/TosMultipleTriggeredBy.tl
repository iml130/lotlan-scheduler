Location pickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"
End

Location dropoffItem
    name = "ws1_dropoff"
    type = "SmallLoadCarrier"
End

Event event
    name = "event"
    type = "Boolean"
End

Event event2
    name = "event2"
    type = "Integer"
End

TransportOrderStep loadStorage
    Location pickupItem 
End

TransportOrderStep unloadWorkstation1
    Location dropoffItem
    TriggeredBy event
    TriggeredBy event2
End

Task helloTask
    Transport
    From loadStorage
    To unloadWorkstation1
End