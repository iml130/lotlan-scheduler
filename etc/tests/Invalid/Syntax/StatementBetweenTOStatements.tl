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
End

Task helloTask
    Transport
    From loadStorage

    TriggeredBy triggerGetNewMaterial == True # error: a transport Order is an atomic statement so it cant be splitted

    To unloadWorkstation1
End
