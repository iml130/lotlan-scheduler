__author__ = "Maximilian Hörstrup"
__version__ = "0.0.1"
__maintainer__ = "Maximilian Hörstrup"

# standard libraries
import sys
from os import walk
from os.path import splitext, join
from contextlib import contextmanager
import codecs

# 3rd party lib
from antlr4 import *
from tabulate import tabulate

# local sources
from TaskLexer import TaskLexer
from TaskParser import TaskParser
from TaskParserListener import TaskParserListener
from CreateTreeTaskParserVisitor import CreateTreeTaskParserVisitor
from SemanticValidator import SemanticValidator
from ThrowErrorListener import ThrowErrorListener

# globals defines
from defines import TEST_FOLDER, LOG_PATH, TEMPLATES_PATH

class ErrorInformation(object):
    def __init__(self, syntaxErrorCount, semanticErrorCount):
        self.syntaxErrorCount = syntaxErrorCount
        self.semanticErrorCount = semanticErrorCount

def getFileNames(path):
    filenames = []

    for root, dirs, files in walk(path):
        for file in files:
            full_path = join(root, file)
            ext = splitext(file)[1]

            if ext == ".tl":
                filenames.append(full_path)

    return filenames

# redirects the output(stdout) to a given file
@contextmanager
def stdoutRedirection(fileobj):
    old = sys.stdout
    sys.stdout = fileobj
    try:
        yield fileobj
    finally:
        sys.stdout = old

# method for testing: if a valid file got an error or vice versa return 0
def testFiles():
    validFilenames = getFileNames(TEST_FOLDER + "Valid/")
    invalidFilenames = getFileNames(TEST_FOLDER + "Invalid/")

    failedTests = 0
    testResults = []

    print("Error messages of tests: \n")
    count = 1
    for validFile in validFilenames:
        errorInformation = testFile(validFile, TEMPLATES_PATH)
        syntaxErrors = errorInformation.syntaxErrorCount
        semanticErrors = errorInformation.semanticErrorCount
        errorCount =  syntaxErrors + semanticErrors
        if  errorCount != 0:
            testResults.append((count, validFile, "0 , 0", str(syntaxErrors) + " , " + str(semanticErrors), False))
            failedTests = failedTests + 1
        else:
            testResults.append((count, validFile, "0 , 0", "0 , 0", True))
        count = count + 1

    testResults.append(("------", "-----------------------------------------", "-----", "-----", "-----"))

    for invalidFile in invalidFilenames:
        errorInformation = testFile(invalidFile, TEMPLATES_PATH)
        syntaxErrors = errorInformation.syntaxErrorCount
        semanticErrors = errorInformation.semanticErrorCount
        errorCount =  syntaxErrors + semanticErrors

        expectedErrorsString = ""

        if "Semantic" in invalidFile:
            expectedErrorsString = "0 , 1"
            if syntaxErrors == 0 and semanticErrors == 1:
                testResults.append((count, invalidFile, expectedErrorsString, "0 , 1", True))
            else:
                testResults.append((count, invalidFile, expectedErrorsString, str(syntaxErrors) + " , " + str(semanticErrors), False))
                failedTests = failedTests + 1
        else:
            expectedErrorsString = ">0 , 0"
            if syntaxErrors > 0:
                testResults.append((count, invalidFile, expectedErrorsString,str(syntaxErrors) + " , 0", True))
            else:
                testResults.append((count, invalidFile, expectedErrorsString, "0 , " + str(semanticErrors), False))
                failedTests = failedTests + 1

        print("\n")
        count = count + 1

    testCount = len(validFilenames) + len(invalidFilenames)
    print(tabulate(testResults, headers = ["Test Nr.", "Test Name", "Expected error count (syntax , semantic)", "Error count", "Has passed"], tablefmt="orgtbl"))
    print("Tests passed: {} of {}".format(testCount - failedTests, testCount))

    # pre-commit script checks if there was errors (checks for return value 1)
    if failedTests > 0:
        sys.exit(1) 

# returns errocount
def testFile(input, templatePath, usedInExtension = False):
    lexer = None

    # this checks wether the input is a String or a File to test
    try:
        languageFile = codecs.open(input, "r", encoding = 'utf8')
        lexer = TaskLexer(InputStream(languageFile.read()))
    except IOError:
        lexer = TaskLexer(InputStream(input))

    tokenStream = CommonTokenStream(lexer)

    parser = TaskParser(tokenStream)
    errorListener = ThrowErrorListener(input, usedInExtension, tokenStream)

    lexer.removeErrorListeners()
    parser.removeErrorListeners()
    
    lexer._listeners.append(errorListener)
    parser.addErrorListener(errorListener)

    tree = parser.program()

    visitor = CreateTreeTaskParserVisitor()

    if errorListener.isValid == False:
        return ErrorInformation(errorListener.errorCount, 0)
    else:
        t = visitor.visit(tree)
        templates = loadTemplates(templatePath)

        semanticValidator = SemanticValidator(input, templates, usedInExtension)
        if semanticValidator.isValid(t) == False:
            return ErrorInformation(0, semanticValidator.errorCount)
        return ErrorInformation(0, 0)
        

# templates definied in the task language are in a separate file
def loadTemplates(path):
    lexer = TaskLexer(InputStream(open(path).read()))
    tokenStream = CommonTokenStream(lexer)
    parser = TaskParser(tokenStream)
    tree = parser.program()
    visitor = CreateTreeTaskParserVisitor()

    return visitor.visit(tree).templates

def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--log":
        print("Test Output is printed to file:", LOG_PATH)
        with open(LOG_PATH, 'w') as out:
            with stdoutRedirection(out):
                testFiles()
    else:
        testFiles()
    
    # sys exit for pre-commit script
    sys.exit(0)

if __name__ == '__main__':
    main()