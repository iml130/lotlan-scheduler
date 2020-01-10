from antlr4 import *
from TaskLexer import TaskLexer
from TaskParserListener import TaskParserListener
from TaskParser import TaskParser
from CreateTreeTaskParserVisitor import CreateTreeTaskParserVisitor
from os import listdir
from os.path import isfile, join
from contextlib import contextmanager

import sys

from SemanticValidator import SemanticValidator
from ThrowErrorListener import ThrowErrorListener

TEST_FOLDER = "testfiles/"
LOG_PATH = "logs/log.txt"
TEMPLATES_PATH = "templates.tl"

def getFileNames(path):
    filenames = []

    for f in listdir(path):
        if isfile(join(path, f)):
            # only add tasklanguage files
            splittedString = f.split(".")
            if len(splittedString) == 2 and splittedString[1] == "tl":
                filenames.append(path + f)

    return filenames

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

    testFailed = False

    #test valid files
    print("Valid files are tested now: \n")
    for validFile in validFilenames:
        if testFile(validFile) == 1:
            print(validFile + " is a valid tasklanguage program and got an error!")
            testFailed = True
        print("\n")

    # test invalid files
    print("Invalid files are tested now: \n")
    for invalidFile in invalidFilenames:
        if testFile(invalidFile) == 0:
            print(invalidFile + " is an invalid tasklanguage program and got no error!")
            testFailed = True
        print("\n")

    if testFailed == True:
        sys.exit(1)

def testFile(documentText):
    lexer = TaskLexer(InputStream(documentText))
    tokenStream = CommonTokenStream(lexer)

    parser = TaskParser(tokenStream)

    errorListener = ThrowErrorListener()

    lexer.removeErrorListeners()
    parser.removeErrorListeners()
    
    lexer._listeners.append(errorListener)
    parser.addErrorListener(errorListener)

    tree = parser.program()

    visitor = CreateTreeTaskParserVisitor()

    if errorListener.isValid:
        t = visitor.visit(tree)
        templates = loadTemplates()

        semanticValidator = SemanticValidator(documentText, templates)
        if semanticValidator.isValid(t):
            return 0
        else:
            return 1
    else:
        return True

def loadTemplates():
    lexer = TaskLexer(InputStream(open(TEMPLATES_PATH).read()))
    tokenStream = CommonTokenStream(lexer)
    parser = TaskParser(tokenStream)
    tree = parser.program()
    visitor = CreateTreeTaskParserVisitor()

    return visitor.visit(tree).templates

def main():
    if(len(sys.argv) == 2 and sys.argv[1] == "--test"):
        # redirect stdout to the log file if we test many files
        with open(LOG_PATH, 'w') as out:
            with stdoutRedirection(out):
                testFiles()
    elif len(sys.argv) == 2:
        testFile(sys.argv[1])
    sys.exit(0)

if __name__ == '__main__':
    main()