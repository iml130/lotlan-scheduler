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
    onDone HelloTask22  # error: 'onDone' is not correct it has to be 'OnDone'
end

task HelloTask2
    Transport
    from loadStorage
    to unloadWorkstation
end