lexer grammar TaskLexer2;

TemplateStart: 'template ' [A-Z][a-zA-Z0-9_]* Whitespace;
TaskStart: 'task ' [A-Z][a-zA-Z0-9_]* Whitespace;
TransportOrderStepStart: 'TransportOrderStep ' [a-z][a-zA-Z0-9_]* Whitespace;
InstanceStart: [A-Z][a-zA-Z0-9_]* ' ' [a-z][a-zA-Z0-9_]* Whitespace;

fragment Whitespace: [ \t]*;

NewLine: '\n';
Indentation: ('    ' | '\t');

Comment: '#' ~[\n]+ -> skip;
CommentInLine: Whitespace '#' ~[\n]+ '\n'-> skip;
EqualInBlock: Whitespace '=' Whitespace;

LowerCaseString: [a-z][a-zA-Z0-9_]*;
UpperCaseString: [A-Z][a-zA-Z0-9_]*;

Value: '"' [a-zA-Z0-9_]+ '"' | '"' ['*'' ''/'0-9]+ '"' | '""' ;

EndInBlock: 'end';

// Transport Order Step Rules
TriggeredByTOS: 'TriggeredBy' Whitespace ->  pushMode(EXPRESSION);
FinishedByTOS: 'FinishedBy' Whitespace ->  pushMode(EXPRESSION);
LocationTOS: 'Location' Whitespace LowerCaseString;
OnDoneTOS: 'OnDone' Whitespace UpperCaseString;
CommaTOS: ',' Whitespace;


// Task Rules
Transport: 'Transport' Whitespace;
From: 'from' Whitespace;
To: 'to' Whitespace;

TriggeredBy: 'TriggeredBy' Whitespace ->  pushMode(EXPRESSION);
FinishedBy: 'FinishedBy' Whitespace ->  pushMode(EXPRESSION);
Repeat: 'Repeat' Whitespace;
RepeatTimes: [0-9]+ Whitespace;
OnDone: 'OnDone' Whitespace;
Comma: ',' Whitespace;

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
E_Attribute: [a-z][a-zA-Z0-9_]+;
E_True: 'True' | 'TRUE';
E_False: 'False' | 'FALSE';
E_Integer: [0-9]+;
E_Float: [0-9]+( '.' [0-9]+);
E_WS: [ \r\t]  -> skip;
E_Comment: '#' ~[\n]+ -> skip;
E_NLInExpression: [\n] -> popMode;