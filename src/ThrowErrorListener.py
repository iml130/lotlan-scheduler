__author__ = "Maximilian Hörstrup"
__version__ = "0.0.1"
__maintainer__ = "Maximilian Hörstrup"

# 3rd party packages
from antlr4.error.Errors import *
from antlr4.error.ErrorListener import ErrorListener

# globals defines
from defines import SYMBOLIC_NAMES

class ThrowErrorListener(ErrorListener):
    def __init__(self, filePath, usedInExtension, tokenStream):
        super()
        self.lines = []
        self.isValid = True
        self.filePath = filePath
        self.usedInExtension = usedInExtension
        self.tokenStream = tokenStream
        self.errorCount = 0


    # if there are more than one possible symbol that can be used 
    # antlr produces a string in the format: {token1, token2, ..}
    def parseExpectedSymbols(self, symbolString):
        if symbolString.startswith("{") and symbolString.endswith("}"):
            tokens = symbolString.split(",")

            outputString = ""
            for token in tokens:
                token = token.replace(' ', '').replace("{", "").replace("}", "")
                symbol = SYMBOLIC_NAMES.get(token)
                if symbol:
                    outputString += symbol + " or "
                else:
                    outputString += token + " or "
            outputString = outputString[:-4] # remove last or
            return outputString
        else:
            symbol = SYMBOLIC_NAMES.get(symbolString)
            if symbol:
                return symbol
            else:
                return symbolString

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.isValid = False
        # current input does not match with the expected token
        if isinstance(e, InputMismatchException):
            missingSymbol = e.getExpectedTokens().toString(recognizer.symbolicNames, recognizer.literalNames)

            symbolDescription = self.parseExpectedSymbols(missingSymbol)

            msg = "expected " + symbolDescription

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

        # those errors dont throw an exception so check it like this
        elif msg.startswith("extraneous input"):
            offendingSymbol = msg.split("'")[1]
            startIndex = msg.find("expecting") + len("expecting") + 1
            endIndex = len(msg)
            expectedSymbol = msg[startIndex : endIndex]

            symbolDescription = self.parseExpectedSymbols(expectedSymbol)
            msg = "Wrong symbol '" + offendingSymbol + "' used. Expected " + symbolDescription

            self.printError(msg, line, column, len(offendingSymbol))
        elif msg.startswith("missing"):
            missingSymbol = msg.split(" ")[1]
            symbolDescription = self.parseExpectedSymbols(missingSymbol)
            msg = "Missing " + symbolDescription
            self.printError(msg, line, column, 1)
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
        self.errorCount = self.errorCount + 1