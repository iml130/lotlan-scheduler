Location dropoffItem
    name = "ws1_dropoff"
    type = "SmallLoadCarrier"
End

Event event
    name = "event"
    type = "Boolean"
End

TransportOrderStep loadStorage
    Location event
End