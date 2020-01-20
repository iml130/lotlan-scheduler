Event event
    name = "event"
    type = "NotABoolean"
end

task LoadStorage
    TriggeredBy event # error: expression is not an event instance
end