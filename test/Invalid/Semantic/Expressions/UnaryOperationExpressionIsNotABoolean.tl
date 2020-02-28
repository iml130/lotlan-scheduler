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
    FinishedBy !(evdent) # error: it is not possible to use a single Time instance with an unary operation (only works with event)
End