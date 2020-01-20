Location pickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"
end

Event event
    name = "event"
    type = "Boolean"
end

Time time
    timing = "30 12 * * *"
end

task LoadStorage
    TriggeredBy pickupItem # error: expression is not an event instance
end