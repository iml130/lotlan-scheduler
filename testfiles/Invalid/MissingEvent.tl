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
    TriggeredBy # error: there is no event given for 'Triggered By'
end

task HelloTask
    TriggeredBy triggerGetNewMateria == True
    Transport
    from loadStorage
    to unloadWorkstation1
end