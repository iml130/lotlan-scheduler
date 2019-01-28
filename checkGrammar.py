from antlr4 import *
from TaskLexer import TaskLexer
from TaskParserListener import TaskParserListener
from TaskParser import TaskParser
import sys

class HelloPrintListener(TaskParserListener):
    def enterProgram(self, ctx):
        pass

def main():
    lexer = TaskLexer(InputStream(open("examples.txt").read()))
    stream = CommonTokenStream(lexer)
    parser = TaskParser(stream)
    tree = parser.program() 
    printer = HelloPrintListener()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)

if __name__ == '__main__':
    main() 