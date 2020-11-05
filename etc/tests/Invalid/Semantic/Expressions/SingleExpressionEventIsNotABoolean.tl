Event event
    name = "event"
    type = "NotABoolean"
End

Task loadStorage
    TriggeredBy event # error: expression is not an event instance
End