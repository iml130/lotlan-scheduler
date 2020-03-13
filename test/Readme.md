Currently available tests:

Valid:
- HelloTask
- TriggeredBy
- RepeatForever
- NewLinesBetweenStatements
- Comments
- Expressions
- Parameters
- Constraints


Invalid:
- Syntax:
  - CommaAfterLastParameter
  - InvalidCharsForNames
  - LowerUpperCaseErrors
  - MissingEnd
  - MissingEvent
  - MissingLocation
  - MissingOnDone
  - MissingTOS
  - NamingError
  - NoCommaBetweenParameters
  - StatementBetweenParameters
  - WrongIndentation
  - WrongSpelledLocation
  - WrongSpelledOnDone
  - WrongSpelledTOS

- Semantic:
  - BinaryOperationLeftSideIsNotAnEvent 
  - BinaryOperationRightSideIsNotABoolean
  - SingleExpressionEventIsNotABoolean
  - SingleExpressionNoEventAnNoTime
  - UnaryOperationExpressionIsNotABoolean
  - InstanceDupilcate
  - MultipleRepeats
  - MultipleTransportOders
  - OnDoneAndRepeat
  - ParameterAmountDoesntMatch
  - TaskDuplicate
  - TaskMultipleOnDone
  - TaskUnknwonOnDoneTask
  - TempAttributeDoesntExist
  - TempAttributeNotDefinied
  - TosDuplicate
  - TosLocationHasOtherType
  - TosLocationNotAnInstance
  - TosMultipleLocations
  - TosMultipleOnDone
  - TosUnknownOnDoneTask
  - UnknownTaskInFrom
  - UnknownTaskInTo 
  - UnknownTemplate