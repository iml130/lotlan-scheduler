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

# local sources
from TaskLexer import TaskLexer
from TaskParser import TaskParser
from TaskParserListener import TaskParserListener
from CreateTreeTaskParserVisitor import CreateTreeTaskParserVisitor
from SemanticValidator import SemanticValidator
from ThrowErrorListener import ThrowErrorListener
# globals defines
from defines import TEST_FOLDER, LOG_PATH, TEMPLATES_PATH

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

    testFailed = False

    #test valid files
    print("Valid files are tested now:\n")
    for validFile in validFilenames:
        if testFile(validFile, False, TEMPLATES_PATH) == False:
            print(validFile + " is a valid tasklanguage program and got an error!")
            testFailed = True
        else:
            print(validFile + " passed the Test!");

    # test invalid files
    print("\nInvalid files are tested now:\n")
    for invalidFile in invalidFilenames:
        if testFile(invalidFile, False, TEMPLATES_PATH) == True:
            print(invalidFile + " is an invalid tasklanguage program and got no error!")
            testFailed = True
        else:
            print(invalidFile + " passed the Test!");
        print("\n")

    # pre-commit script checks if there was errors (checks for return value 1)
    if testFailed == True:
        sys.exit(1)
    
    print("All tests passed!")

def testFile(input, usedInExtension, templatePath = TEMPLATES_PATH):
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
        return False
    else:
        t = visitor.visit(tree)
        templates = loadTemplates(templatePath)

        semanticValidator = SemanticValidator(input, templates, usedInExtension)
        if semanticValidator.isValid(t) != True:
            return False
        else:
            return True

# templates definied in the task language are in a separate file
def loadTemplates(path):
    lexer = TaskLexer(InputStream(open(path).read()))
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
    elif len(sys.argv) == 4 :
        if sys.argv[2] == "--ext":
            testFile(sys.argv[1], True, sys.argv[3])
                
    # sys exit for pre-commit script
    sys.exit(0)

if __name__ == '__main__':
    main()