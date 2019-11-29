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
    Location pickupItem  # Only one Location can be defined!
end

TransportOrderStep unloadWorkstation1
    Location dropoffItem
end

task HelloTask
    TriggeredBy triggerGetNewMaterial == True
    Transport
    from loadStorage
    to unloadWorkstation1
end
