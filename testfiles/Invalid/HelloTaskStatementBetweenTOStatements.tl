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
    Transport
    from loadStorage

    TriggeredBy triggerGetNewMaterial == True # error: a transport Order is an atomic statement so it cant be splitted

    to unloadWorkstation1
end
