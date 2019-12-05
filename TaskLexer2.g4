lexer grammar TaskLexer2;

Template: 'template ' -> pushMode(BLOCK);
Task: 'task ' -> pushMode(BLOCK);
TransportOrderStep: 'TransportOrderStep ' -> pushMode(BLOCK);
Instance: UpperCaseString ' ' -> pushMode(BLOCK);
Whitespace: [ \t\r\n]+ -> skip;
Comment: '#' ~[\n]+ -> skip;

mode BLOCK;

Indentation: ('    ' | '\t');
NewLine: Whitespace_Block '\n';

CommentInBlock : Whitespace_Block '#' ~[\n]+  -> skip;
CommentLineInBlock : Indentation '#' ~[\n]+ '\n'-> skip;

Equal: Whitespace_Block '=' Whitespace_Block;
EndInBlock: 'end' -> popMode;

// Only For TransportOrderStep
Location: 'Location' Whitespace_Block;

// Only For Task
Repeat: 'Repeat' Whitespace_Block;
RepeatTimes: [0-9]+ Whitespace_Block;

// Transport Order used in Task
Transport: 'Transport';
From: 'from' Whitespace_Block;
To: 'to' Whitespace_Block;

// Used in both
OnDone: 'OnDone' Whitespace_Block;
TriggeredBy: 'TriggeredBy' Whitespace_Block -> pushMode(EXPRESSION);
FinishedBy: 'FinishedBy' Whitespace_Block -> pushMode(EXPRESSION);

Comma: ',' Whitespace_Block;

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