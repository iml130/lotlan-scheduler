Location pickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"
end

Location pickupItem2
    name = "s1_pickup"
    type = "SmallLoadCarrier"
end

Location dropoffItem
    name = "ws1_dropoff"
    type = "SmallLoadCarrier"
end

TransportOrderStep loadStorage
    Location pickupItem 
end

TransportOrderStep unloadWorkstation1
    Location dropoffItem
end

task HelloTask
    Transport
    from loadStorage
    to unloadWorkstation1
    Repeat		5
    Repeat		1 # error: an repeat statement was already definied
end