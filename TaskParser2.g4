parser grammar TaskParser2;

options {
	tokenVocab = TaskLexer2;
}

program : 
    (template | instance | task | transportOrderStep)*;

// Template Layout
template: 
    Template UpperCaseString NewLine 
        memberVariable+
    EndInBlock;

// Instance Layout
instance: 
    Instance LowerCaseString NewLine
        memberVariable+
    EndInBlock;

memberVariable:
    Indentation LowerCaseString Equal Value NewLine;

// Transport Order Step
transportOrderStep:
    TransportOrderStep LowerCaseString NewLine
        optionalTransportOrderStepStatement*
        Indentation Location LowerCaseString NewLine // there have to be at least one Location statement
        optionalTransportOrderStepStatement*
    EndInBlock;

// Task Layout
task: 
    Task UpperCaseString NewLine
        taskStatement+
    EndInBlock;

taskStatement:
    transportOrder 
    | optionalTransportOrderStepStatement
    | Indentation Repeat RepeatTimes NewLine;

optionalTransportOrderStepStatement:
    Indentation TriggeredBy expression E_NLInExpression
    | Indentation FinishedBy expression E_NLInExpression
    | Indentation OnDone UpperCaseString NewLine;

transportOrder:
    Indentation Transport NewLine
    Indentation From LowerCaseString NewLine
    Indentation To dest = LowerCaseString NewLine;

expression:
    attr = E_Attribute
    | E_LeftParenthesis expression E_RightParenthesis
    | bleft = expression binOperation bright = expression
    | unOperation unAttr = expression
    | con;

binOperation:
    op = (E_LessThan
        | E_LessThanOrEqual
        | E_GreaterThan
        | E_GreaterThanOrEqual
        | E_Equal
        | E_NotEqual
        | E_BooleanAnd
        | E_BooleanOr);

unOperation:
    op = E_Not;

con:
    c = E_True 
        | E_False
        | E_Integer
        | E_Float;