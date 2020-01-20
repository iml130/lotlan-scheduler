Location pickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"
end

location dropoffItem # the keyword 'Location' was spelled wrong
    name = "ws1_dropoff"
    type = "SmallLoadCarrier"
end

TransportOrderStep loadStorage
    Location pickupItem
end


TransportOrderStep unloadWorkstation # the keyword 'TransportOrderStep' was spelled wrong
    Location dropoffItem
end


task helloTask # the keyword 'task' was spelled wrong
    Transport
    from loadStorage
    to unloadWorkstation
end