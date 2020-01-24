Location pickupItem
    name            # errorsdfasd asd fasdf asdfa 
    type = "SmallLoadCarrier"
End

TransportOrderStep loadStorage
    Location pickupItem 
End

TransportOrderStep unloadWorkstation1
    Location # error: there is no location given for 'Location'
End

Task helloTask
    Transport
    From loadStorage
    To unloadWorkstation1
End