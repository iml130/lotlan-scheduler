__author__ = "Maximilian Hörstrup"
__version__ = "0.0.1"
__maintainer__ = "Maximilian Hörstrup"

# standard libraries
import sys
import codecs

#3rd party packages
import networkx as nx
from antlr4 import *
import pydot

# local sources
from TaskLexer import TaskLexer
from TaskParser import TaskParser
from TaskParserListener import TaskParserListener
from CreateTreeTaskParserVisitor import CreateTreeTaskParserVisitor
from ThrowErrorListener import ThrowErrorListener

class TaskGraphGenerator:
    def __init__(self, completeProgram):
        self.taskGraphs = []
        for task in completeProgram.taskInfos:
            self.taskGraphs.append(nx.DiGraph())

        self.completeProgram = completeProgram

    def generateTaskGraphs(self):
        tasks = self.completeProgram.taskInfos

        i = 0
        for task in tasks.values():
            self.taskGraphs[i].add_node(task.name.value)
            for onDoneTask in task.onDone:
                self.taskGraphs[i].add_edge(task.name.value, onDoneTask.value)
                i = i + 1

        return self.taskGraphs

def main():
    lexer = None

    if len(sys.argv) == 2:
        try:
            languageFile = codecs.open(sys.argv[1], "r", encoding = 'utf8')
            lexer = TaskLexer(InputStream(languageFile.read()))
        except IOError:
            print("error while reading lotlan file")

        tokenStream = CommonTokenStream(lexer)

        parser = TaskParser(tokenStream)

        tree = parser.program()

        visitor = CreateTreeTaskParserVisitor()

        t = visitor.visit(tree)
        taskGraphGenerator = TaskGraphGenerator(t)
        graphs = taskGraphGenerator.generateTaskGraphs()

        i = 0
        for graph in graphs:
            pydot_graph = nx.nx_pydot.to_pydot(graph)
            pydot_graph.write_png("taskGraph" + str(i) + ".png")
            i = i + 1
    else:
        print("You need to provide a lotlan file")


if __name__ == '__main__':
    main()