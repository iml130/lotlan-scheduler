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
    TriggeredBy pickupItem == 10 # error: left side is not an event instance
end