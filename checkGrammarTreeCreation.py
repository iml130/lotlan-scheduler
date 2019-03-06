from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from TaskLexer import TaskLexer
from TaskParserListener import TaskParserListener
from TaskParser import TaskParser
from CreateTreeTaskParserVisitor import CreateTreeTaskParserVisitor
import sys

class ThrowErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise e

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        raise Exception("Task-Language could not be parsed")

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        raise Exception("Task-Language could not be parsed")

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        raise Exception("Task-Language could not be parsed")


def main():
    lexer = TaskLexer(InputStream(open("examples.txt").read()))
    lexer._listeners.append(ThrowErrorListener())
    stream = CommonTokenStream(lexer)
    parser = TaskParser(stream)

    tree = parser.program() 
    visitor = CreateTreeTaskParserVisitor()
    # printer = TaskParserListener()
    t = visitor.visit(tree)

    print t.taskInfos["Transport_Task"].triggers[2]

if __name__ == '__main__':
    main() 

