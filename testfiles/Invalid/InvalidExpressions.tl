Location pickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"
end

Event event
    name = "event"
    type = "Boolean"
end

Event event2
    name = "event2"
    type = "Integer"
end

Time time
    timing = "30 12 * * *"
end

TransportOrderStep loadStorage
    Location pickupItem
    TriggeredBy !time # error: it is not possible to use a single Time instance with an unary operation (only works with event)
    TriggeredBy	time == 60 # error: you cant compare time with something (time format in cron)
end