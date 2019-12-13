from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from antlr4.error.Errors import *

class ThrowErrorListener(ErrorListener):
    def __init__(self, logPath):
        super()
        self.lines = []
        self.isValid = True
        self.logPath = logPath

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.isValid = False

        # print different error messages according to the exception
        # current input does not match with the expected token
        if isinstance(e, InputMismatchException):  
            missingSymbol = e.getExpectedTokens().toString(recognizer.literalNames, recognizer.symbolicNames)
            print("Expecting symbol '" + missingSymbol + "'" + " at line: " + str(line) + ":" + str(column), file=open(self.logPath, 'a'))

        # the lexer could not decide which path to take so the input doesnt match with anything
        elif isinstance(e, LexerNoViableAltException):
            # if we get a LexerNoViableAltException in one line ignore the other
            # exceptions that will occur due to the first one
            if line not in self.lines:
                self.lines.append(line)
                print("Invalid Character at line: " + str(line) + ":" + str(column), file=open(self.logPath, 'a'))
        elif isinstance(e, FailedPredicateException):
            print(msg, line, column, file=open(self.logPath, 'a'))
        elif isinstance(e, NoViableAltException):
            print(msg, line, column, file=open(self.logPath, 'a'))
        else:
            print(msg, line, column, file=open(self.logPath, 'a'))

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        self.isValid = False
        raise Exception("Task-Language could not be parsed")

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        self.isValid = False
        raise Exception("Task-Language could not be parsed")

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        self.isValid = False
        raise Exception("Task-Language could not be parsed")