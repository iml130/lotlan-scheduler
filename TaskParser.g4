parser grammar TaskParser;

options {
	tokenVocab = TaskLexer;
}


program : 
    (template | instance | task)*;


// Template Layout
template: 
    TemplateStart NLInTemplate 
        innerTemplate 
    EndInTemplate;

innerTemplate: 
    (IndentationInTemplate AttributeInTemplate NLInTemplate)+;

// Instance Layout
instance: 
    InstanceStart NLInInstance 
        innerInstance 
    EndInInstance;

innerInstance: 
    (IndentationInInstance AttributeInInstance Equal ValueInInstance NLInInstance)+;

// Task Layout
task: 
    TaskStart NLInTask 
        innerTask 
    EndInTask;
 
innerTask:
    (transportOrder 
    | IndentationInTask TriggeredBy expression E_NLInTask
    | IndentationInTask OnDone NewTask NLInTask)+;

transportOrder:
    IndentationInTask Transport NLInTask
    IndentationInTask From NewInstance (Comma NewInstance)* NLInTask
    IndentationInTask To dest = NewInstance NLInTask;


expression:
    attr = E_Attribute
   | E_LeftParenthesis expression E_RightParenthesis
   | expression binOperation expression
   | unOperation expression
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


