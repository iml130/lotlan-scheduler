from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from antlr4.error.Errors import *
from TaskLexer import TaskLexer
from TaskParserListener import TaskParserListener
from TaskParser import TaskParser
from CreateTreeTaskParserVisitor import CreateTreeTaskParserVisitor
import taskValidator

import sys

class ThrowErrorListener(ErrorListener):
    def __init__(self):
        self.lines = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        # print different error messages according to the exception
    
        # current input does not match with the expected token
        if isinstance(e, InputMismatchException):  
            missingSymbol = e.getExpectedTokens().toString(recognizer.literalNames, recognizer.symbolicNames)
            print("Expecting symbol '" + missingSymbol + "'" + " at line: " + str(line) + ":" + str(column))

        # the lexer could not decide which path to take so the input doesnt match with anything
        elif isinstance(e, LexerNoViableAltException):
            # if we get a LexerNoViableAltException in one line ignore the other
            # exceptions that will occur due to the first one
            if line not in self.lines:
                self.lines.append(line)
                print("Invalid Character at line: " + str(line) + ":" + str(column))

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        raise Exception("Task-Language could not be parsed")

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        raise Exception("Task-Language could not be parsed")

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        raise Exception("Task-Language could not be parsed")

def main():
    lexer = TaskLexer(InputStream(open("examples.tl").read()))
    parser = TaskParser(CommonTokenStream(lexer))

    errorListener = ThrowErrorListener()

    lexer.removeErrorListeners()
    parser.removeErrorListeners()
    
    lexer._listeners.append(errorListener)

    
    parser.addErrorListener(errorListener);

    tree = parser.program()
    visitor = CreateTreeTaskParserVisitor()

    # check for some semantic errors while traversing through the tree and return the program data
    t = visitor.visit(tree)

    #validate semantic
    print("Semantic of program successfully tested:", taskValidator.isValid(t))

if __name__ == '__main__':
    main()