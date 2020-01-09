Location pickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"
end

Location dropoffItem
    name = "?ws1_dropoff" # error: '?' is not a valid character for the name attribute
    type = "SmallLoadCarrier"
end

TransportOrderStep loadStorage
    Location pickupItem 
end

TransportOrderStep unloadWorkstation1§
    Location !!dropoffItem # error: '!' is not a valid character for an instance name
end

Event triggerGetNewMaterial.. # error: '.' is not a valid character for an instance name
    name = "virtualSensorNewMaterialToWs1"
    type = "Boolean"
end


task HelloTask
    Transport
    from loadStorage
    to UnloadWorkstation1 # error: instance names has to start with an lowercase char
end