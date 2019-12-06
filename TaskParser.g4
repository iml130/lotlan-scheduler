parser grammar TaskParser2;

options {
	tokenVocab = TaskLexer2;
}

program : 
    (template | instance | task | transportOrderStep)*;

// Template Layout
template: 
    templateStart memberVariable+ END_IN_BLOCK;

templateStart:
    TEMPLATE UPPER_CASE_STRING NEW_LINE+;

// Instance Layout
instance: 
    instanceStart memberVariable+ END_IN_BLOCK;

instanceStart:
    INSTANCE LOWER_CASE_STRING NEW_LINE+;

memberVariable:
    INDENTATION LOWER_CASE_STRING EQUAL VALUE NEW_LINE+;

// Transport Order Step
transportOrderStep:
    tosStart tosStatements END_IN_BLOCK;

tosStart:
    TRANSPORT_ORDER_STEP LOWER_CASE_STRING NEW_LINE+;

tosStatements:
    optTosStatement*
        INDENTATION LOCATION LOWER_CASE_STRING NEW_LINE+ // there have to be at least one Location statement
    optTosStatement*;

// Task Layout
task:
    taskStart taskStatement+ END_IN_BLOCK;

taskStart:
    TASK UPPER_CASE_STRING NEW_LINE+;

taskStatement:
    transportOrder 
    | optTosStatement NEW_LINE* // optional new lines after \n in expression
    | INDENTATION REPEAT REPEAT_TIMES NEW_LINE+;

// transport from to 
transportOrder:
    INDENTATION TRANSPORT NEW_LINE
    INDENTATION FROM LOWER_CASE_STRING NEW_LINE
    INDENTATION TO dest = LOWER_CASE_STRING NEW_LINE+;

// optional to extend functionality
optTosStatement:
    INDENTATION TRIGGERED_BY expression E_NL_IN_EXPRESSION
    | INDENTATION FINISHED_BY expression E_NL_IN_EXPRESSION
    | INDENTATION ON_DONE UPPER_CASE_STRING NEW_LINE;

expression:
    attr = E_ATTRIBUTE
    | E_LEFT_PARENTHESIS expression E_RIGHT_PARENTHESIS
    | bleft = expression binOperation bright = expression
    | unOperation unAttr = expression
    | con;

binOperation:
    op = (E_LESS_THAN
        | E_LESS_THAN_OR_EQUAL
        | E_GREATER_THAN
        | E_GREATER_THAN_OR_EQUAL
        | E_EQUAL
        | E_NOT_EQUAL
        | E_BOOLEAN_AND
        | E_BOOLEAN_OR);

unOperation:
    op = E_BOOLEAN_NOT;

con:
    c = E_TRUE 
        | E_FALSE
        | E_INTEGER
        | E_FLOAT;