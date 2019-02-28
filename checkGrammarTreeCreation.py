from antlr4 import *
from TaskLexer import TaskLexer
from TaskParserListener import TaskParserListener
from TaskParser import TaskParser
from CreateTreeTaskParserVisitor import CreateTreeTaskParserVisitor
import sys

def main():
    lexer = TaskLexer(InputStream(open("examples.txt").read()))
    stream = CommonTokenStream(lexer)
    parser = TaskParser(stream)
    tree = parser.program() 
    visitor = CreateTreeTaskParserVisitor()
    # printer = TaskParserListener()
    t = visitor.visit(tree)

    print t.taskInfos["Transport_Task"].triggers[2]

if __name__ == '__main__':
    main() 

