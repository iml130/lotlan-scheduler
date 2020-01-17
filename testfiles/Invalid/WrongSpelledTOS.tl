Location pickupItem
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
    From loadStorage
    to unloadWorkstationcvx # error: the tos name was spelled wrong so the validator cant find the correct instance
end