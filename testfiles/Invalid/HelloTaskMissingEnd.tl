Location pickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"

Location dropoffItem
    name = "ws1_dropoff"
    type = "SmallLoadCarrier"
# error: missing end

TransportOrderStep loadStorage
    Location pickupItem 
end

TransportOrderStep unloadWorkstation1
    Location dropoffItem
# error: missing end

task HelloTask
    Transport
    from loadStorage
    to unloadWorkstation1
# error: missing end