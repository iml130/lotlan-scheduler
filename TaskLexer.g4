lexer grammar TaskLexer;

CommentInProgram : '#' ~[\n]+  -> skip;
TemplateStart: 'template ' [A-Z][a-zA-Z0-9_]* -> pushMode(TEMPLATE);
TaskStart: 'task ' [A-Z][a-zA-Z0-9_]* -> pushMode(TASK);
InstanceStart: [A-Z][a-zA-Z0-9_]* ' ' [a-z][a-zA-Z0-9_]* -> pushMode(INSTANCE);
WS: [ \t\r\n]+ -> skip;


mode TEMPLATE;
// Skip Comments/Empty Lines as long as Indentation is correct
CommentInTemplate : WS_T '#' ~[\n]+ -> skip;
CommentLineInTemplate : IndentationInTemplate '#' ~[\n]+ '\n'-> skip;
EmptyLineInTemplate: ('    '| '\t') '\n' -> skip;
EndInTemplate: 'end' -> popMode;

AttributeInTemplate: [a-z][a-zA-Z0-9_]*;
NLInTemplate: WS_T '\n';
IndentationInTemplate: ('    '|'\t');
fragment WS_T: [ \t]*;


mode INSTANCE;
// Skip Comments/Empty Lines as long as Indentation is correct
CommentInInstance : WS_I '#' ~[\n]+  -> skip;
CommentLineInInstance : IndentationInInstance '#' ~[\n]+ '\n'-> skip;
EmptyLineInInstance: ('    '| '\t') '\n' -> skip;
EndInInstance: 'end' -> popMode;

Equal: WS_I '=' WS_I;
NLInInstance: WS_I '\n';
IndentationInInstance: ('    '|'\t');
AttributeInInstance: [a-z][a-zA-Z0-9_]*;
ValueInInstance: ('"' [a-zA-Z0-9_]* '"' | [a-zA-Z0-9_]+);
fragment WS_I: [ \t]*;


mode TASK;
// Skip Comments/Empty Lines as long as Indentation is correct
CommentInTask : WS_TA '#' ~[\n]+  -> skip;
CommentLineInTask : IndentationInTask '#' ~[\n]+ '\n'-> skip;
EmptyLineInTask: ('    '| '\t') '\n' -> skip;
EndInTask: 'end' -> popMode;

NLInTask: WS_TA '\n';

//Definition of TransportOrder
Transport: 'Transport' WS_TA;
From: 'from' WS_TA;
To: 'to' WS_TA;


TriggeredBy: 'TriggeredBy' WS_TA ->  pushMode(EXPRESSION);
OnDone: 'OnDone' WS_TA;
Comma: ',' WS_TA;

IndentationInTask: ('    '|'\t');
NewInstance: [a-z][a-zA-Z0-9_]*; 
NewTask: [A-Z][a-zA-Z0-9_]*;
fragment WS_TA: [ \t]*;


mode EXPRESSION;
E_LeftParenthesis: '(';
E_RightParenthesis: ')';
E_LessThan: '<';
E_LessThanOrEqual: '<=';
E_GreaterThan: '>';
E_GreaterThanOrEqual: '>=';
E_Equal: '==' | '=';
E_NotEqual: '!=';
E_BooleanAnd:	'&&';
E_BooleanOr: '||';
E_Not: '!';
E_Attribute: [a-z][a-zA-Z0-9_]* '.' [a-z][a-zA-Z0-9_]*;
E_True: 'True' | 'TRUE';
E_False: 'False' | 'FALSE';
E_Integer: [0-9]+;
E_Float: [0-9]+( '.' [0-9]+);
E_WS: [ \r\t]  -> skip;
E_Comment: '#' ~[\n]+ -> skip;
E_NLInTask: [\n] -> popMode;