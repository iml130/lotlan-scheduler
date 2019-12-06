parser grammar TaskParser;

options {
	tokenVocab = TaskLexer;
}


program : 
    (template | instance | task | transportOrderStep)*;


// Template Layout
template: 
    TemplateStart NLInTemplate 
        innerTemplate 
    EndInTemplate;

innerTemplate: 
    (IndentationInTemplate AttributeInTemplate EqualInTemplate ValueInTemplate NLInTemplate)+; 

// Instance Layout
instance: 
    InstanceStart NLInInstance 
        innerInstance 
    EndInInstance;

innerInstance: 
    (IndentationInInstance AttributeInInstance EqualinInstance ValueInInstance NLInInstance)+;

transportOrderStep:
    TransportOrderStepStart NLInTransportOrderStep
        innerTransportOrderStep
    EndInTransportOrderStep;

innerTransportOrderStep:
    ( IndentationInTransportOrderStep TriggeredByTOS expression E_NLInExpression
    | IndentationInTransportOrderStep FinishedByTOS expression E_NLInExpression
    | IndentationInTransportOrderStep LocationTOS NewInstanceInTransportOrderStep NLInTransportOrderStep  
    | IndentationInTransportOrderStep OnDoneTOS NewTaskInTransportOrderStep NLInTransportOrderStep)+;


// Task Layout
task: 
    TaskStart NLInTask
        innerTask 
    EndInTask;
 
innerTask:
    (transportOrder 
    | IndentationInTask TriggeredBy expression E_NLInExpression
    | IndentationInTask FinishedBy expression E_NLInExpression
    | IndentationInTask Repeat RepeatTimes NLInTask 
    | IndentationInTask OnDone NewTask NLInTask)+;

transportOrder:
    IndentationInTask Transport NLInTask
    IndentationInTask From NewInstance NLInTask
    IndentationInTask To dest = NewInstance NLInTask;


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
    c = (E_True 
        | E_False
        | E_Integer
        | E_Float);


