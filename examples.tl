##############################
#This is just a Template to show available options
##############################

# Basic TransportOrderStep-structure
TransportOrderStep moldingPalette
    Location moldingPalette_location     # Only one Location can be defined!
    FinishedBy workerPressedButtonAtMoldingPalette
end

TransportOrderStep warehouse
    Location warehouse_location
    FinishedBy workerPressedButtonAtWarehouse
end

TransportOrderStep t1#should work
	Location testitest
	TriggeredBy mitarbeiterButtonDasErFertigIst
	FinishedBy abc == bce < 5
	OnDone MeineTask7
end

# Basic Template structure
template Palette
	name = ""
	type  = "" # readonly
end

template PaletteSensor # A Sensor which sets the Value to true if full
	name = ""
	type = ""# readonly
end

template Container
	name = ""
    type = ""
end

Container container
	name = ""
    type = "Container"
end

Container room
	name = ""
    type = "Supply_Room"
end


# Basic Instance structure
Palette palette_1
	name  =	"LightSensor"
	type = "boolean"
end

Palette palette_2
	name  =	"LightSensor"
	type = "boolean"
end

Palette palette_3
	name  =	"LightSensor"
	type = "boolean"
end

PaletteSensor palette_1Full
	type = "Boolean"
	name = "my_sensor"
end

PaletteSensor palette_2Full
	type = "Boolean"
	name = "your_sensor"
end

PaletteSensor palette_3Full
	type = "Boolean"
	name = "some_sensor"
end


task Reset_Task
	Transport 
    from 		t1
    to 			moldingPalette
end 


# Basic Task structure
task Transport_Task
    # Transport something from A to B
	Transport 
    from 		t1
    to 			warehouse
    
	TriggeredBy	palette_1Full == TRUE
	TriggeredBy	palette_2Full == FALSE
	TriggeredBy	palette_3Full == !12 || 42.42 <= 42.31
    
	OnDone		Reset_Task
end



###########################################
# This section below shows what is currently parsable 
###########################################



Palette this_palette
	name  =	"LightSensor"
	type = "boolean"
end

Palette that_palette
	name  =	"LightSensor"
	type = "boolean"
end



template Position # Required for correct Parsing of thisPos and emptyPAllet
	name = ""
	type = ""
end


Position thisPos
	# ExampleDescription of an Instance
	type = "pallet"
    
	name = "thisPos" # Values can also be set inside "
    
    
    
end




# Spaces and Tabs can be used to format nicely
# Also Empty Lines are allowed
task Nice_Formatted_Task#Comment everywhere
	Transport       # A Comment can also be expanded via Spaces and Tabs
    from			moldingPalette
	to				warehouse
    
	TriggeredBy		thisPos == 42.42 && 3 <= 4
	
    
	#Afterwards 
	OnDone 			Reset_Task
end####### End of Task








Position emptyPallet   # Another Comment
	type = "pallet"
	name =   "warehouse_empty_pallet"
	#Again empty Lines
    
    #type = "SomethingDebugged"
	#position = "OnRoof"
    
	#Test
end    # Another Comement



#Outside of Task Instance and Template Comments can be
														# set freely
      # Even with Spaces


template Sensor_B#Another Comment
	name   = ""
	type    =    ""
    
    
	# Empty Lines are allowed
	# Also Comment Lines
	type = ""
	value = "" #readonly
    value_2 = ""  #writeonly
	#CommentLine
    
end#END


Container warehouse_pos1
	name = "SomeName"
	type = "WareHouse"
end

task Refill
    Transport 
	from t1
	to moldingPalette
end

task Transport_Palette_Task1
	Transport 
    from t1 # All Pallets!
	to warehouse
	TriggeredBy warehouse_pos1 # Suddenly Expressions!
	OnDone Refill
end


task Transport_Palette_Task2
	Transport 
    from t1 # All Pallets!
	to warehouse
	FinishedBy warehouse_pos1 # Suddenly Expressions!
	OnDone Refill
end

task Transport_Palette_Task3
	Transport 
    from warehouse # All Pallets!
	to t1
	FinishedBy warehouse_pos1 # Suddenly Expressions!
	OnDone Refill
	Repeat 12321321321213
end


task Transport_Palette_Task4
	Transport 
    from warehouse # All Pallets!
	to t1
	FinishedBy warehouse_pos1 # Suddenly Expressions!
	TriggeredBy warehouse_pos2 # Suddenly Expressions!
	OnDone Refill
	Repeat 123
end


template Time
    # As in Cron
    timing = "* * * * *"
end



template Time2
    # As in Cron
    timing = "* * * * */10"
end





template Time3
    # As in Cron
    timing = "* * *  * */10"
end


### TEMPLATES
template Location
    name = ""
    type = ""
end

template Event
    name = ""
    type = ""
end


### INSTANCES 

Location moldingPallet
    name = "Tag10_11"
    type = "pallet"
end

Location blaPosition
    name = "Tag10_12"
    type = "Boolean"
end

Event sensorTest
    type = "Boolean"
    name = "LightBarrier"
end



task Pickup
    FinishedBy sensorTest == True # manual loading 
end


 # TASKS


task Transport_Palette_Task 
	TriggeredBy mitarbeiterButtonDasErFertigIst
    Transport 
    from moldingPalette # All Pallets!
    to warehouse 
	Repeat 3
end


