lexer grammar TaskLexer;

TEMPLATE: 'template ' -> pushMode(BLOCK);
TASK: 'task ' -> pushMode(BLOCK);
TRANSPORT_ORDER_STEP: 'TransportOrderStep ' -> pushMode(BLOCK);
INSTANCE: STARTS_WITH_UPPER_C_STR ' ' -> pushMode(BLOCK);

WHITESPACE: [ \t\r\n]+ -> skip;
COMMENT: '#' ~[\n]+ -> skip;

mode BLOCK;

NEW_LINE: WHITESPACE_BLOCK '\n';

INDENTATION: ('    ' | '\t');

COMMENT_IN_BLOCK : WHITESPACE_BLOCK '#' ~[\n]+  -> skip;
COMMENT_LINE_IN_BLOCK : INDENTATION '#' ~[\n]+ '\n'-> skip;

EQUAL: WHITESPACE_BLOCK '=' WHITESPACE_BLOCK;
END_IN_BLOCK: 'end' -> popMode;

// Only For TransportOrderStep
LOCATION: 'Location' WHITESPACE_BLOCK;

// Only For Task
REPEAT: 'Repeat' WHITESPACE_BLOCK;
REPEAT_TIMES: [0-9]+ WHITESPACE_BLOCK;

// Transport Order used in Task
TRANSPORT: 'Transport';
FROM: 'from' WHITESPACE_BLOCK;
TO: 'to' WHITESPACE_BLOCK;

// Used in both
ON_DONE: 'OnDone' WHITESPACE_BLOCK;
TRIGGERED_BY: 'TriggeredBy' WHITESPACE_BLOCK -> pushMode(EXPRESSION);
FINISHED_BY: 'FinishedBy' WHITESPACE_BLOCK -> pushMode(EXPRESSION);

COMMA: ',' WHITESPACE_BLOCK;

STARTS_WITH_LOWER_C_STR: [a-z][a-zA-Z0-9_]*;
STARTS_WITH_UPPER_C_STR: [A-Z][a-zA-Z0-9_]*;

STRING_VALUE: '"' [a-zA-Z0-9_]+ '"';
NUMERIC_VALUE: '"' ['*'' ''/'0-9]+ '"';
EMPTY_VALUE: '""';

fragment WHITESPACE_BLOCK: [ \t]*;

mode EXPRESSION;
E_LEFT_PARENTHESIS: '(';
E_RIGHT_PARENTHESIS: ')';
E_LESS_THAN: '<';
E_LESS_THAN_OR_EQUAL: '<=';
E_GREATER_THAN: '>';
E_GREATER_THAN_OR_EQUAL: '>=';
E_EQUAL: '==' | '=';
E_NOT_EQUAL: '!=';
E_BOOLEAN_AND:	'&&';
E_BOOLEAN_OR: '||';
E_BOOLEAN_NOT: '!';
E_ATTRIBUTE: [a-z][a-zA-Z0-9_]*;
E_TRUE: 'True' | 'TRUE';
E_FALSE: 'False' | 'FALSE';
E_INTEGER: [0-9]+;
E_FLOAT: [0-9]+( '.' [0-9]+);
E_WS: [ \r\t]  -> skip;
E_COMMENT: '#' ~[\n]+ -> skip;
E_NL_IN_EXPRESSION: [\n] -> popMode;