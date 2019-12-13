parser grammar TaskParser;

options {
	tokenVocab = TaskLexer;
}

program : 
    (template | instance | task | transportOrderStep)*;

// Template Layout
template: 
    templateStart memberVariable+ END_IN_BLOCK;

templateStart:
    TEMPLATE STARTS_WITH_UPPER_C_STR NEW_LINE+;

// Instance Layout
instance: 
    instanceStart memberVariable+ END_IN_BLOCK;

instanceStart:
    INSTANCE STARTS_WITH_LOWER_C_STR NEW_LINE+;

memberVariable:
    INDENTATION STARTS_WITH_LOWER_C_STR EQUAL value NEW_LINE+;

value:
    STRING_VALUE | NUMERIC_VALUE | EMPTY_VALUE;

// Transport Order Step
transportOrderStep:
    tosStart tosStatements END_IN_BLOCK;

tosStart:
    TRANSPORT_ORDER_STEP STARTS_WITH_LOWER_C_STR NEW_LINE+;

tosStatements:
    optTosStatement* locationStatement optTosStatement*;

locationStatement:
    INDENTATION LOCATION STARTS_WITH_LOWER_C_STR NEW_LINE+;

// optional to extend functionality
optTosStatement:
    INDENTATION TRIGGERED_BY expression E_NL_IN_EXPRESSION
    | INDENTATION FINISHED_BY expression E_NL_IN_EXPRESSION
    | INDENTATION ON_DONE STARTS_WITH_UPPER_C_STR NEW_LINE;

// Task Layout
task:
    taskStart taskStatement+ END_IN_BLOCK;

taskStart:
    TASK STARTS_WITH_UPPER_C_STR NEW_LINE+;

taskStatement:
    transportOrder 
    | optTosStatement NEW_LINE* // optional new lines after \n in expression
    | INDENTATION REPEAT REPEAT_TIMES NEW_LINE+;

// transport from to 
transportOrder:
    INDENTATION TRANSPORT NEW_LINE
    INDENTATION FROM STARTS_WITH_LOWER_C_STR NEW_LINE
    INDENTATION TO STARTS_WITH_LOWER_C_STR NEW_LINE+;

expression:
    E_ATTRIBUTE
    | E_LEFT_PARENTHESIS expression E_RIGHT_PARENTHESIS
    | expression binOperation expression
    | unOperation expression
    | con;

binOperation:
    E_LESS_THAN
    | E_LESS_THAN_OR_EQUAL
    | E_GREATER_THAN
    | E_GREATER_THAN_OR_EQUAL
    | E_EQUAL
    | E_NOT_EQUAL
    | E_BOOLEAN_AND
    | E_BOOLEAN_OR;

unOperation:
    E_BOOLEAN_NOT;

con:
    E_TRUE 
    | E_FALSE
    | E_INTEGER
    | E_FLOAT;