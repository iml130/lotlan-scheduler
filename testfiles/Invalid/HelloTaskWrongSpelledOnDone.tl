Location pickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"
end

Location dropoffItem
    name = "ws1_dropoff"
    type = "SmallLoadCarrier"
end


TransportOrderStep loadStorage
    Location pickupItem  # Only one Location can be defined!
end

TransportOrderStep unloadWorkstation1
    Location dropoffItem
end

task HelloTask
    Transport
    from loadStorage
    to unloadWorkstation1
    OnDone HelloTask2
end