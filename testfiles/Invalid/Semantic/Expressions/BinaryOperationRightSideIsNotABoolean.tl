Location pickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"
end

Event event
    name = "event"
    type = "Boolean"
end

TransportOrderStep loadStorage
    Location pickupItem
    FinishedBy	event == pickupItem # error: the right side can not be resolved to a boolean (a String is never a boolean)
end