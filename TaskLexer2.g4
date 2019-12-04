lexer grammar TaskLexer2;

TemplateStart: 'template ' UpperCaseString -> pushMode(BLOCK);
TaskStart: 'task ' UpperCaseString -> pushMode(BLOCK);
TransportOrderStepStart: 'TransportOrderStep ' LowerCaseString -> pushMode(BLOCK);
InstanceStart: UpperCaseString ' ' LowerCaseString -> pushMode(BLOCK);
Whitespace: [ \t\r\n]+ -> skip;
Comment: '#' ~[\n]+ -> skip;

mode BLOCK;

Indentation: ('    ' | '\t');
NewLine: Whitespace_Block '\n';

CommentInInstance : Whitespace_Block '#' ~[\n]+  -> skip;
CommentLineInInstance : Indentation '#' ~[\n]+ '\n'-> skip;

EqualInBlock: Whitespace_Block '=' Whitespace_Block;
EndInBlock: 'end' -> popMode;

Comma: ',' Whitespace_Block;

Location: 'Location' Whitespace_Block;

Transport: 'Transport';
From: 'from' Whitespace_Block;
To: 'to' Whitespace_Block;

OnDone: 'OnDone' Whitespace_Block;

TriggeredBy: 'TriggeredBy' Whitespace_Block -> pushMode(EXPRESSION);
FinishedBy: 'FinishedBy' Whitespace_Block -> pushMode(EXPRESSION);

Repeat: 'Repeat' Whitespace_Block;
RepeatTimes: [0-9]+ Whitespace_Block;

LowerCaseString: [a-z][a-zA-Z0-9_]*;
UpperCaseString: [A-Z][a-zA-Z0-9_]*;

Value: '"' [a-zA-Z0-9_]+ '"' | '"' ['*'' ''/'0-9]+ '"' | '""' ;

fragment Whitespace_Block: [ \t]*;

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