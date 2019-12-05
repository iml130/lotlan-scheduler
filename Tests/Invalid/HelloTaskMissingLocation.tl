Location pickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"
end

TransportOrderStep loadStorage
    Location pickupItem 
end

TransportOrderStep unloadWorkstation1
    Location
end

task HelloTask
    Transport
    from loadStorage
    to unloadWorkstation1
end