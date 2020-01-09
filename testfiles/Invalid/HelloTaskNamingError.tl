Location pickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"
end

Locatio dropoffItem # the keyword 'Location' was spelled wrong
    name = "ws1_dropoff"
    type = "SmallLoadCarrier"
end

TransportOrderStep loadStorage
    Location pickupItem
end

TransporOrderStep unloadWorkstation # the keyword 'TransportOrderStep' was spelled wrong
    Location dropoffItem
end

Task HelloTask # the keyword 'task' was spelled wrong
    Transport
    from loadStorage
    to unloadWorkstation
end