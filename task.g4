grammar taskLanguage;            // Define a grammar called taskLanguage

/*
* Task Language
*/

 

program
	: entity;
	
entity
	: task;

task 
	: TASKSTART transportorder TASKEND;

// later: multiple tasks

transportorder
	: TRANSPORT item_list  TO itemdestination; // match keyword hello followed by an identifier 
item_list
	: LPAREN items (',' items)* RPAREN | items;
items 
	:  (QUANTITY TIMES)? (PREFIX_ID ID);
itemdestination 
	: (PREFIX_DEST ID);


/*
* LEXER RULES
*/

fragment LOWERCASE  : [a-z] ;
fragment UPPERCASE  : [A-Z] ;
fragment IDENTIFIER : '@';
fragment FRAG_TIMES : '*';
fragment DIGIT
	: [0-9];

LPAREN : '(';
RPAREN : ')';
// KEYWORDS 
TASKSTART
	: 'Task' WHITESPACE;
TASKEND
	: 'End';
TRANSPORT 
	: ('transport') WHITESPACE ;
TO
	: ('to') WHITESPACE;

// 
QUANTITY 
	:  NUMBER ;
TIMES 
	:  '*';

NUMBER 
	: DIGIT;
ID :
	LOWERCASE+ WHITESPACE?;   


WHITESPACE : (' ' | '\t') ;

PREFIX_ID 
	: IDENTIFIER('UID_' | 'uid_' );
 // match lower-case identifiers
WS 
	: [ \t\r\n]+ -> skip ;            // skip spaces, tabs, newlines, \r (Windows)

PREFIX_DEST 
	: IDENTIFIER('DEST_' | 'dest_' );

NEWLINE 
	: ('\r'? '\n' | '\r')+ ;

NAME : 
	(LOWERCASE)+ WHITESPACE;


/* 

Transport
    - Pickup
        - GoTo Destination
        - Loading
            - Manual
            - Automatic
    - Delivery
        - GoTo Destination
        - Loading
            - Manual
            - Automatic
            
TESTDATA 

{

"id"  : "NewTask",
"type" : "TaskEntity",

"task" : {

}

OnEvent(ButtonPalletReady, True):
	Engino

Task Engino
		Transport @uid_pallet to @uid_warehous_pos1
		Loading Automatic
		Unloading Automatic
	OnDone:
		Task Refill
End

Task Refill
	Transport @uid_empty_pallet to @uid_pallet
	OnDone:
		Charging
End

Task Charging
	GoTo @uid_charging_position
End


uid_pallet = { position =  (injection_pallet_position_id)}
uid_warehous_pos1 =  { position =  ( warehouse_pallet_position_1_id)}


injection_pallet_position_id = {x,y,theta} | topologyId 
warehouse_pallet_position_1_id = = {x,y,theta} | topologyId 

uid_warehous_pos1 = {position, ...}

Task transport 4*@uid_pallet to @dest_warehouse End
task asd transport 4*@uid_pallet to @dest_warehouse end
transport 4*@uid_pallet to @dest_warehouse
*/

