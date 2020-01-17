Location pickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"
end

Event event
    name = "event"
    type = "boolean"
end

TransportOrderStep loadStorage
    Location event # error: an event instance is used as location
end