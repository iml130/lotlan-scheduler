# begin of program

# this defines the location pickupItem
Location pickupItem #block starts
    name = "s1_pickup"
    type = "SmallLoadCarrier"
end

# this defines a location
Location dropoffItem
    name = "ws1_dropoff"
    type = "SmallLoadCarrier"
end

######
## Multiline comments with multiple #
#######
TransportOrderStep loadStorage
    Location pickupItem  # Only one Location can be defined!
end

TransportOrderStep unloadWorkstation1
    Location dropoffItem
    #Comment before statement: TriggeredBy event
end

task HelloTask
    Transport #transport
    from loadStorage #from
    to unloadWorkstation1 #to

    # on done
    OnDone HelloTask
end #end of program