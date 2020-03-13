Location pickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"
End

Location dropoffItem
    name = "w?s1_dropoff" #error: '?' is not a valid character for the name attribute
    type = "SmallLoadCarrier"
End

TransportOrderStep loadStorage
    Location pickupItem 
End

TransportOrderStep unloadWorkstation1§
    Location !!dropoffItem # error: '!' is not a valid character for an instance name
End

Event triggerGetNewMaterial.. # error: '.' is not a valid character for an instance name
    name = "virtualSensorNewMaterialToWs1"
    type = "Boolean"
End


Task helloTask
    Transport 
    From loadStorage
    To UnloadWorkstation1 # error: instance names has to start with an lowercase char
End