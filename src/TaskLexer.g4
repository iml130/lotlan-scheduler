lexer grammar TaskLexer;

TEMPLATE: 'Template ' STARTS_WITH_UPPER_C_STR-> pushMode(BLOCK);
TASK: 'Task ' -> pushMode(BLOCK);
TRANSPORT_ORDER_STEP: 'TransportOrderStep ' -> pushMode(BLOCK);
INSTANCE: STARTS_WITH_UPPER_C_STR ' ' -> pushMode(BLOCK);

WHITESPACE: [ \t\r\n]+ -> skip;
COMMENT: '#' ~[\n]* -> skip;

mode BLOCK;

NEW_LINE: '\n';
INDENTATION: ('    ' | '\t');

COMMENT_IN_BLOCK : '#' ~[\n]+  -> channel(HIDDEN);
COMMENT_LINE_IN_BLOCK : INDENTATION '#' ~[\n]+ '\n'-> channel(HIDDEN);


END_IN_BLOCK: 'End' -> popMode;

// Only For TransportOrderStep
LOCATION: 'Location';
PARAMETER: 'Parameter';

// Only For Task
REPEAT: 'Repeat';
CONSTRAINTS: 'Constraints';

TRANSPORT: 'Transport';
FROM: 'From';
TO: 'To';

// Used in both TOS and Task
ON_DONE: 'OnDone';
TRIGGERED_BY: 'TriggeredBy';
FINISHED_BY: 'FinishedBy';

EQUAL: '=';
COMMA: ',';

E_LEFT_PARENTHESIS: '(';
E_RIGHT_PARENTHESIS: ')';
E_LESS_THAN: '<';
E_LESS_THAN_OR_EQUAL: '<=';
E_GREATER_THAN: '>';
E_GREATER_THAN_OR_EQUAL: '>=';
E_EQUAL: '==';
E_NOT_EQUAL: '!=';
E_BOOLEAN_AND: 'and';
E_BOOLEAN_OR: 'or';
E_BOOLEAN_NOT: '!';
E_TRUE: 'True' | 'TRUE';
E_FALSE: 'False' | 'FALSE';

STARTS_WITH_LOWER_C_STR: [a-z][a-zA-Z0-9_]*;
STARTS_WITH_UPPER_C_STR: [A-Z][a-zA-Z0-9_]*;

STRING_VALUE: '"' [a-zA-Z0-9_]+ '"';
NUMERIC_VALUE: '"' ['*'' ''/'0-9]+ '"';
EMPTY_VALUE: '""';

INTEGER: [0-9]+;
FLOAT: [0-9]+( '.' [0-9]+);

WHITESPACE_BLOCK: [ \t\r]+ -> channel(HIDDEN);