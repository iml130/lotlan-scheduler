Location pickupItem
    name = "s1_pickup"
    type = "SmallLoadCarrier"
end

Location dropoffItem
    name = "ws1_dropoff"
    type = "SmallLoadCarrier"
end

TransportOrderStep loadStorage
    Location pickupItem
end

TransportOrderStep unloadWorkstation
    Location dropoffItem
end

task HelloTask
    Transport
    from loadStorage
    to unloadWorkstation
    OnDone HelloTask22  # error: the task name was spelled wrong so the validator cant find the correct instance
end

task HelloTask2
    Transport
    from loadStorage
    to unloadWorkstation
end