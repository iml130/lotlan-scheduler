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
    TriggeredBy !time
    TriggeredBy	time == 60
    FinishedBy !event == 5
end