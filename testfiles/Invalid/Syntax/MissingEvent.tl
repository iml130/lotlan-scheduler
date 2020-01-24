Location pickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"
End

Location dropoffItem
    name = "ws1_dropoff"
    type = "SmallLoadCarrier"
End

Event triggerGetNewMaterial
    name = "virtualSensorNewMaterialToWs1"
    type = "Boolean"
End

TransportOrderStep loadStorage
    Location pickupItem
End

TransportOrderStep unloadWorkstation1
    Location dropoffItem
    TriggeredBy # error: there is no event given for 'Triggered By'
End

Task helloTask
    TriggeredBy triggerGetNewMateria == True
    Transport
    From loadStorage
    To unloadWorkstation1
End