Location pickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"
end

Location dropoffItem
    name = "ws1_dropoff"
    type = "SmallLoadCarrier"
end

Event triggerGetNewMaterial
    name = "virtualSensorNewMaterialToWs1"
    type = "Boolean"
end

TransportOrderStep loadStorage
    Location pickupItem
end

TransportOrderStep unloadWorkstation1
    Location dropoffItem
end

task HelloTask
    TriggeredBy triggerGetNewMateria == True # error: the instace name was spelled wrong so the validator cant find the correct instance
    Transport
    from loadStorage
    to unloadWorkstation1
end