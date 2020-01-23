__author__ = "Maximilian Hörstrup"
__version__ = "0.0.1"
__maintainer__ = "Maximilian Hörstrup"

# local sources
from antlr4.error.Errors import *
from antlr4.error.ErrorListener import ErrorListener


symbolicNames = {
    "STARTS_WITH_LOWER_C_STR"                                       : "a String that starts with a lowercase char",
    "STARTS_WITH_UPPER_C_STR"                                       : "a String that starts with a uppercase char",
    '{STRING_VALUE, NUMERIC_VALUE, \'""\'}'                         : "a value (String, number, nothing)",
    "EQUAL"                                                         : "an equal literal",
    "{'(', '!', E_ATTRIBUTE, E_TRUE, E_FALSE, E_INTEGER, E_FLOAT}"  : "a condition",
    "TO"                                                            : "a to",
    "FROM"                                                          : "a from",
    "INDENTATION"                                                   : "an indentation",
}

class ThrowErrorListener(ErrorListener):
    def __init__(self, filePath, usedInExtension, tokenStream):
        super()
        self.lines = []
        self.isValid = True
        self.filePath = filePath
        self.usedInExtension = usedInExtension
        self.tokenStream = tokenStream

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.isValid = False
        # current input does not match with the expected token
        if isinstance(e, InputMismatchException):
            missingSymbol = e.getExpectedTokens().toString(recognizer.literalNames, recognizer.symbolicNames)

            symbolDescription = symbolicNames.get(missingSymbol)
            msg = ""
            if symbolDescription:
                msg = "Expecting " + symbolicNames[missingSymbol] + "'"
            else:
                msg = "Expecting symbol '" + missingSymbol + "'"

            offendingSymbolLength = len(offendingSymbol.text)
    
            hiddenToken = self.tokenStream.getHiddenTokensToLeft(offendingSymbol.tokenIndex)
            if hiddenToken != None:
                lastToken = hiddenToken.pop()
                commentLength = len(lastToken.text)
                column = column - commentLength

            self.printError(msg, line, column, offendingSymbolLength)

        # the lexer could not decide which path to take so the input doesnt match with anything
        elif isinstance(e, LexerNoViableAltException):
            # if we get a LexerNoViableAltException in one line ignore the other
            # exceptions that will occur due to the first one
            if line not in self.lines:
                self.lines.append(line)
                invalidChar = msg[msg.find("'") + 1 : msg.rfind("'")]
                msg = "Invalid Character '" + invalidChar + "'"
                offendingSymbolLength = 1 # the first char that doesnt match so length is 1

                self.printError(msg, line, column, offendingSymbolLength)
        # a valid symbol by the lexer but there is no parser rule to match it in the current context
        elif isinstance(e, NoViableAltException):
            msg = "Symbol '" + offendingSymbol.text + "' cant be used here"
            offendingSymbolLength = len(offendingSymbol.text)
            
            self.printError(msg, line, column, offendingSymbolLength)
        else:
            offendingSymbolLength = len(offendingSymbol.text)

            hiddenToken = self.tokenStream.getHiddenTokensToLeft(offendingSymbol.tokenIndex)
            if hiddenToken != None:
                lastToken = hiddenToken.pop()
                commentLength = len(lastToken.text)
                column = column - commentLength
                
            self.printError(msg, line, column, offendingSymbolLength)

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        self.isValid = False
        raise Exception("Task-Language could not be parsed")

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        self.isValid = False
        raise Exception("Task-Language could not be parsed")

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        self.isValid = False
        raise Exception("Task-Language could not be parsed")

    def printError(self, msg, line, column, offSymbolLength):
        # python shell in extension parses print statements of python
        if self.usedInExtension == True:
            print(msg)
            print(line)
            print(column) # for ext: antlr starts at column 0, vs code at column 1
            print(offSymbolLength)
        else:
            print(msg)
            print("File '" + self.filePath + "', line " + str(line) + ":" + str(column))