Location pickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"
end

Location dropoffItem
    name = "ws1_dropoff"
    type = "SmallLoadCarrier"
end

TransportOrderStep loadStorage
    OnDone HelloTask
    Location pickupItem
    TriggeredBy event
    TriggeredBy	event && (event2 || event3)
    FinishedBy True
end

TransportOrderStep unloadWorkstation1
    Location dropoffItem
    TriggeredBy	5 == 5
    TriggeredBy !(5 != 5)
    FinishedBy (event2 || event3)    
end