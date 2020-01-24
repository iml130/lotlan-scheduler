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
    FinishedBy	event == pickupItem # error: the right side can not be resolved to a boolean (a String is never a boolean)
End