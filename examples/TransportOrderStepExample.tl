template Location
    name = ""
    type = ""
end

Location moldingPalette_location
    name = "palette_10C"
    type = "palette"
end

Location warehouse_location
    name = "warehouse_2"
    type = "warehouse"
end


TransportOrderStep moldingPalette
    Location moldingPalette_location     # Only one Location can be defined!
    FinishedBy workerPressedButtonAtMoldingPalette
end


TransportOrderStep warehouse
    Location warehouse_location
    FinishedBy workerPressedButtonAtWarehouse
end

task TransportToWareHouse
    # Transport Order now needs TransportOrderSteps instead of regular instances
    Transport
    from moldingPalette
    to warehouse
    TriggeredBy someEventOutside
    Repeat 3 
end