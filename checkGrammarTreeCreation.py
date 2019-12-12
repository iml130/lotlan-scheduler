from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from antlr4.error.Errors import *
from TaskLexer import TaskLexer
from TaskParserListener import TaskParserListener
from TaskParser import TaskParser
from CreateTreeTaskParserVisitor import CreateTreeTaskParserVisitor
from os import listdir
from os.path import isfile, join
import sys

import taskValidator

TEST_FOLDER = "Tests/"


class ThrowErrorListener(ErrorListener):
    def __init__(self):
        self.lines = []
        self.isValid = True

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.isValid = False

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
        elif isinstance(e, FailedPredicateException):
            print(msg, line, column)
        elif isinstance(e, NoViableAltException):
            print(msg, line, column)
        else:
            print(msg, line, column)

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        self.isValid = False
        raise Exception("Task-Language could not be parsed")

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        self.isValid = False
        raise Exception("Task-Language could not be parsed")

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        self.isValid = False
        raise Exception("Task-Language could not be parsed")


def getFileNames(path):
    filenames = []

    for f in listdir(path):
        if isfile(join(path, f)):
            # only add tasklanguage files
            splittedString = f.split(".")
            if len(splittedString) == 2 and splittedString[1] == "tl":
                filenames.append(path + f)

    return filenames

def testFiles():
    validFilenames = getFileNames(TEST_FOLDER + "Valid/")
    invalidFilenames = getFileNames(TEST_FOLDER + "Invalid/")

    #test valid files

    print("Valid files are tested now:")
    for validFile in validFilenames:
        if testFile(validFile) == False:
            print(validFile + " is a valid tasklanguage program and got an error!")

    # test invalid files
    print("Invalid files are tested now:")
    for invalidFile in invalidFilenames:
        if testFile(invalidFile) == True:
            print(invalidFile + " is an invalid tasklanguage program and got no error!")


def testFile(filename):
    print("testing file " + filename)

    lexer = TaskLexer(InputStream(open(filename).read()))
    tokenStream = CommonTokenStream(lexer)
    parser = TaskParser(tokenStream)
    
    errorListener = ThrowErrorListener()

    lexer.removeErrorListeners()
    parser.removeErrorListeners()
    
    lexer._listeners.append(errorListener)
    parser.addErrorListener(errorListener)

    tree = parser.program()
    visitor = CreateTreeTaskParserVisitor()

    # check for some semantic errors while traversing through the tree and return the program data
    # t = visitor.visit(tree)

    #validate semantic
    #print("Semantic of program successfully tested:", taskValidator.isValid(t))

    if errorListener.isValid:#and taskValidator.isValid(t):
        return True
    else:
        return False

def main():
    if(len(sys.argv) == 2 and sys.argv[1] == "--test"):
        testFiles()
    else: 
        testFile("examples.tl")


if __name__ == '__main__':
    main()