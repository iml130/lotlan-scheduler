parser grammar TaskParser2;

options {
	tokenVocab = TaskLexer2;
}

program : 
    (template | instance | task | transportOrderStep)*;

// Template Layout
template: 
    TEMPLATE UPPER_CASE_STRING NEW_LINE 
        memberVariable+
    END_IN_BLOCK;

// Instance Layout
instance: 
    INSTANCE LOWER_CASE_STRING NEW_LINE
        memberVariable+
    END_IN_BLOCK;

memberVariable:
    INDENTATION LOWER_CASE_STRING EQUAL VALUE NEW_LINE;

// Transport Order Step
transportOrderStep:
    TRANSPORT_ORDER_STEP LOWER_CASE_STRING NEW_LINE
        optionalTransportOrderStepStatement*
        INDENTATION LOCATION LOWER_CASE_STRING NEW_LINE // there have to be at least one Location statement
        optionalTransportOrderStepStatement*
    END_IN_BLOCK;

// Task Layout
task: 
    TASK UPPER_CASE_STRING NEW_LINE
        taskStatement+
    END_IN_BLOCK;

taskStatement:
    transportOrder 
    | optionalTransportOrderStepStatement
    | INDENTATION REPEAT REPEAT_TIMES NEW_LINE;

optionalTransportOrderStepStatement:
    INDENTATION TRIGGERED_BY expression E_NL_IN_EXPRESSION
    | INDENTATION FINISHED_BY expression E_NL_IN_EXPRESSION
    | INDENTATION ON_DONE UPPER_CASE_STRING NEW_LINE;

transportOrder:
    INDENTATION TRANSPORT NEW_LINE
    INDENTATION FROM LOWER_CASE_STRING NEW_LINE
    INDENTATION TO dest = LOWER_CASE_STRING NEW_LINE;

expression:
    attr = E_Attribute
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