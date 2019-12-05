Location pickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"
end

Locatinn dropoffItem
    name = "ws1_dropoff"
    type = "SmallLoadCarrier"
end

TransportOrderStep loadStorage
    location pickupItemm
end

TransportOrderStep unloadWorkstation1
    Location dropoffItem
end

task HelloTask
    Transport
    from loadStorage
    to unloadWorkstation1
end