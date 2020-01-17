Location pickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"
end

Location dropoffItem
    name = "ws1_dropoff"
    type = "SmallLoadCarrier"
end

TransportOrderStep loadStorage
    location pickupItemm
end

TransportOrderStep unloadWorkstation1
    Location dropoffItem2  # error: the instace name was spelled wrong so the validator cant find the correct instance
end

task HelloTask
    Transport
    from loadStorage
    to unloadWorkstation1
end