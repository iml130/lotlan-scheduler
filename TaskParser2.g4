parser grammar TaskParser2;

options {
	tokenVocab = TaskLexer2;
}

program : 
    (template | instance | task | transportOrderStep | whitespace)*;


// Template Layout
template: 
    TemplateStart NewLine 
        (Indentation LowerCaseString EqualInBlock Value NewLine)+
    EndInBlock;

// Instance Layout
instance: 
    InstanceStart NewLine
        (Indentation LowerCaseString EqualInBlock Value NewLine)+
    EndInBlock;


transportOrderStep:
    TransportOrderStepStart NewLine
        ( Indentation TriggeredByTOS expression E_NLInExpression
        | Indentation FinishedByTOS expression E_NLInExpression
        | Indentation LocationTOS NewLine  
        | Indentation OnDoneTOS NewLine)+
    EndInBlock;

// Task Layout
task: 
    TaskStart NewLine
        (transportOrder 
        | Indentation TriggeredBy expression E_NLInExpression
        | Indentation FinishedBy expression E_NLInExpression
        | Indentation Repeat RepeatTimes NewLine 
        | Indentation OnDone UpperCaseString NewLine)+
    EndInBlock;

whitespace:
    (Indentation | NewLine)+;

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
    c = (E_True 
        | E_False
        | E_Integer
        | E_Float);