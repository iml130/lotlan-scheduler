parser grammar TaskParser;

options {
	tokenVocab = TaskLexer;
}


program: 
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
    | IndentationInTask TriggeredBy NewInstance NLInTask 
    | IndentationInTask OnDone NewTask NLInTask)+;

transportOrder:
    IndentationInTask Transport NLInTask
    IndentationInTask From NewInstance (Comma NewInstance)* NLInTask
    IndentationInTask To NewInstance NLInTask;

