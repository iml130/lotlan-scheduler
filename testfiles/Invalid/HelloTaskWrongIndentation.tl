Location pickupItem
        name = "s1_pickup"
            type = "SmallLoadCarrier"
         # error: there is one and two indentations too much
end

Location dropoffItem
    name = "ws1_dropoff"
    type = "SmallLoadCarrier"
    end # error: there is one indentation too much

TransportOrderStep loadStorage
    Location pickupItem 
end

TransportOrderStep unloadWorkstation1
Location dropoffItem # error: there is missing an indentation
end

    task HelloTask # error: there is one indentation too much
    Transport
    from loadStorage
    to unloadWorkstation1
end