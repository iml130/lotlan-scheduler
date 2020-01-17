Location pickupItem
    name            # errorsdfasd asd fasdf asdfa 
    type = "SmallLoadCarrier"
end

TransportOrderStep loadStorage
    Location pickupItem 
end

TransportOrderStep unloadWorkstation1
    Location # error: there is no location given for 'Location'
end

task HelloTask
    Transport
    from loadStorage
    to unloadWorkstation1
end