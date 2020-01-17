Location dropoffItem
    name = "ws1_dropoff"
    type = "SmallLoadCarrier"
end

Event event
    name = "event"
    type = "Boolean"
end

TransportOrderStep loadStorage
    Location event
end