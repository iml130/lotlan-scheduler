Location PickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"
end

Location dropoffItem
    name = "ws1_dropoff"
    type = "SmallLoadCarrier"
end

TransportOrderStep LoadStorage
    Location pickupItem 
end

TransportOrderStep unloadWorkstation1
    Location DropoffItem
end

task helloTask
    Transport
    from loadStorage
    to unloadWorkstation1
end