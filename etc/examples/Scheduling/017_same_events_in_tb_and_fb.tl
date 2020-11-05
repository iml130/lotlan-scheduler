Location pickupItem
    name = "Tag10"
    type = "pallet"
End

Location dropoffItem
    name = "Tag12"
    type = "pallet"
End

Event buttonPressed
    name = "button_1"
    type = "Boolean"
End

Event buttonPressed2
    name = "button_2"
    type = "Boolean"
End

TransportOrderStep loadPickupItem
    Location pickupItem
End

TransportOrderStep unloadDropoffItem
    Location dropoffItem
End

Task helloTask
    TriggeredBy buttonPressed == False or buttonPressed2 == True
    Transport
    From loadPickupItem
    To unloadDropoffItem
    FinishedBy buttonPressed == False and buttonPressed2 == True  
End