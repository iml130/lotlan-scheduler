Location pickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"
End

Event event
    name = "event"
    type = "Boolean"
End

Time time
    timing = "30 12 * * *"
End

Task loadStorage
    TriggeredBy pickupItem # error: expression is not an event instance
End