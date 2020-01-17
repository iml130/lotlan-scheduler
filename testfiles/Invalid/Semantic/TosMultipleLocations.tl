Location dropoffItem
    name = "ws1_dropoff"
    type = "SmallLoadCarrier"
end

Location dropoffItem2
    name = "ws2_dropoff"
    type = "SmallLoadCarrier"
end

TransportOrderStep loadStorage
    Location dropoffItem
    Location dropoffItem2
end