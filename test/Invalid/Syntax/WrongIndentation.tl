Location pickupItem
        name = "s1_pickup"
            type = "SmallLoadCarrier"
         # error: there is one and two indentations too much
End

Location dropoffItem
    name = "ws1_dropoff"
    type = "SmallLoadCarrier"
    End # error: there is one indentation too much

TransportOrderStep loadStorage
    Location pickupItem 
End

TransportOrderStep unloadWorkstation1
Location dropoffItem # error: there is missing an indentation
End

    Task helloTask # error: there is one indentation too much
    Transport
    From loadStorage
    To unloadWorkstation1
End