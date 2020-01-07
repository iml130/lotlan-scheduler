from antlr4 import *
from TaskLexer import TaskLexer
from TaskParserListener import TaskParserListener
from TaskParser import TaskParser
from CreateTreeTaskParserVisitor import CreateTreeTaskParserVisitor
from os import listdir
from os.path import isfile, join
import sys

from SemanticValidator import SemanticValidator
from ThrowErrorListener import ThrowErrorListener

TEST_FOLDER = "testfiles/"
LOG_PATH = "logs/log.txt"

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
    print("Valid files are tested now: \n", file=open(LOG_PATH, 'a'))
    for validFile in validFilenames:
        if testFile(validFile) == False:
            print(validFile + " is a valid tasklanguage program and got an error!", file=open(LOG_PATH, 'a'))
        print("\n", file=open(LOG_PATH, 'a'))

    # test invalid files
    print("Invalid files are tested now: \n", file=open(LOG_PATH, 'a'))
    for invalidFile in invalidFilenames:
        if testFile(invalidFile) == True:
            print(invalidFile + " is an invalid tasklanguage program and got no error!", file=open(LOG_PATH, 'a'))
        print("\n", file=open(LOG_PATH, 'a'))


def testFile(filename):
    print("testing file " + filename + ":", file=open(LOG_PATH, 'a'))

    lexer = TaskLexer(InputStream(open(filename).read()))
    templateLexer = TaskLexer(InputStream(open("templates.tl").read()))

    tokenStream = CommonTokenStream(lexer)
    templateTokenStream = CommonTokenStream(templateLexer)

    parser = TaskParser(tokenStream)
    templateParser = TaskParser(templateTokenStream)

    errorListener = ThrowErrorListener(LOG_PATH)

    lexer.removeErrorListeners()
    parser.removeErrorListeners()
    
    lexer._listeners.append(errorListener)
    parser.addErrorListener(errorListener)

    tree = parser.program()
    templateTree = templateParser.program()

    visitor = CreateTreeTaskParserVisitor()
    templateVisitor = CreateTreeTaskParserVisitor()

    #no syntax errors
    if errorListener.isValid:
        print("There are no syntax errors!", file=open(LOG_PATH, 'a'))
        t = visitor.visit(tree)
        templates = templateVisitor.visit(templateTree).templates

        semanticValidator = SemanticValidator(LOG_PATH, filename, templates)
        if semanticValidator.isValid(t):
            print("There are no semantic errros!", file=open(LOG_PATH, 'a'))
            return True
        else:
            print("There are semantic errors! Errors: " + str(semanticValidator.errorCount), file=open(LOG_PATH, 'a'))
            return False
    else:
        print("There are syntax errors!", file=open(LOG_PATH, 'a'))
        return False

def main():
    print("Syntax and semantic check \n\n", file=open(LOG_PATH, 'w'))
    if(len(sys.argv) == 2 and sys.argv[1] == "--test"):
        testFiles()
    else: 
        testFile("examples/Available_Options.tl")


if __name__ == '__main__':
    main()