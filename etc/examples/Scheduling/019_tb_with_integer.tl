Location pickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"
End

Location dropoffItem
    name = "ws1_dropoff"
    type = "SmallLoadCarrier"
End

Event sensor
    name = "sensor_1"
    type = "Integer"
End

Event sensor2
    name = "sensor_2"
    type = "Integer"
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
    To unloadWorkstation1
    TriggeredBy sensor > 50 and sensor2 == 5
End