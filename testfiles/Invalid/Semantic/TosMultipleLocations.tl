Location dropoffItem
    name = "ws1_dropoff"
    type = "SmallLoadCarrier"
End

Location dropoffItem2
    name = "ws2_dropoff"
    type = "SmallLoadCarrier"
End

TransportOrderStep loadStorage
    Location dropoffItem
    Location dropoffItem2
End