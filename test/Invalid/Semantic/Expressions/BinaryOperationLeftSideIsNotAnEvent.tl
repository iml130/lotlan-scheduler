Location pickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"
End

Event event
    name = "event"
    type = "Boolean"
End

TransportOrderStep loadStorage
    Location pickupItem
    TriggeredBy pickupItem == 10 # error: left side is not an event instance
End