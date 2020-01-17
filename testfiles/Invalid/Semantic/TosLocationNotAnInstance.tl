Location dropoffItem
    name = "ws1_dropoff"
    type = "SmallLoadCarrier"
end

TransportOrderStep loadStorage
    Location dropoffItem2 # error: dropoffItem2 is not an instance
end