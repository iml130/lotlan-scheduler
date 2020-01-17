Location PickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"
end

Location dropoffItem
    name = "ws1_dropoff"
    type = "SmallLoadCarrier"
end

TransportOrderStep LoadStorage # error: instance name has to start with an lowercase Character
    Location pickupItem 
end

TransportOrderStep unloadWorkstation1
    Location DropoffItem # error: instance name has to start with an lowercase Character
end

task helloTask # error: task name has to start with an Uppercase Character
    Transport
    from loadStorage
    to unloadWorkstation1
end