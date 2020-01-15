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

    testFailed = False

    #test valid files
    print("Valid files are tested now:\n")
    for validFile in validFilenames:
        if testFile(validFile, False) == False:
            print(validFile + " is a valid tasklanguage program and got an error!")
            testFailed = True
        else:
            print(validFile + " passed the Test!");

    # test invalid files
    print("\nInvalid files are tested now:\n")
    for invalidFile in invalidFilenames:
        if testFile(invalidFile, False) == True:
            print(invalidFile + " is an invalid tasklanguage program and got no error!")
            testFailed = True
        else:
            print(invalidFile + " passed the Test!");
        print("\n")

    # pre-commit script checks if there was errors (checks for return value 1)
    if testFailed == True:
        sys.exit(1)
    
    print("All tests passed!")

def testFile(input, usedInExtension):
    lexer = None

    # this checks wether the input is a String or a File to test
    try:
        languageFile = open(input, "r")
        lexer = TaskLexer(InputStream(languageFile.read()))
    except IOError:
        lexer = TaskLexer(InputStream(input))

    tokenStream = CommonTokenStream(lexer)
    parser = TaskParser(tokenStream)
    errorListener = ThrowErrorListener(input, usedInExtension)

    lexer.removeErrorListeners()
    parser.removeErrorListeners()
    
    lexer._listeners.append(errorListener)
    parser.addErrorListener(errorListener)

    tree = parser.program()

    visitor = CreateTreeTaskParserVisitor()

    if errorListener.isValid == False:
        return False
    else:
        t = visitor.visit(tree)
        templates = loadTemplates()

        semanticValidator = SemanticValidator(input, templates, usedInExtension)
        if semanticValidator.isValid(t) != True:
            return False
        else:
            return True

# templates definied in the task language are in a separate file
def loadTemplates():
    lexer = TaskLexer(InputStream(open(TEMPLATES_PATH).read()))
    tokenStream = CommonTokenStream(lexer)
    parser = TaskParser(tokenStream)
    tree = parser.program()
    visitor = CreateTreeTaskParserVisitor()

    return visitor.visit(tree).templates

def main():
    if len(sys.argv) == 2:
        # command line argument for testing the grammar and semantic check
        if sys.argv[1] == "--test":
            # redirect stdout to the log file because we test many files
            print("Test Output is printed to file:", LOG_PATH)
            with open(LOG_PATH, 'w') as out:
                with stdoutRedirection(out):
                    testFiles()
        else:
            testFile(sys.argv[1], False)
    # a file or string has been passed and the ext keyword so the script is called by the extension
    elif len(sys.argv) == 3 and sys.argv[2] == "--ext":
        testFile(sys.argv[1], True)

    # sys exit for pre-commit script
    sys.exit(0)

if __name__ == '__main__':
    main()