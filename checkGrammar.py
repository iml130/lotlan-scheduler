from antlr4 import *
from TaskLexer import TaskLexer
from TaskParserListener import TaskParserListener
from TaskParser import TaskParser
import sys


class PythonListener(TaskParserListener):
    def __init__(self):
        # Key, Value -> TemplateStr, [List of set Attr]
        self.templateDict = dict()
        # defined instances
        self.instances = []
        # defined tasks
        self.tasks = []
        self.transportOrderSteps = []
        # last visited template
        self.lastVisitedTemplate = None 

    def enterTemplate(self, ctx):
        # Get Templatename and removing Template prefix
        tempStr =  ctx.TemplateStart().getText()[9:] 
        self.templateDict[tempStr] = []
        self.lastVisitedTemplate = tempStr

    def enterInnerTemplate(self, ctx):
        for ele in ctx.AttributeInTemplate():
            self.templateDict[self.lastVisitedTemplate].append(ele.getText())

    def enterInstance(self, ctx):
        instanceStart = ctx.InstanceStart().getText().split()
        self.lastVisitedTemplate = instanceStart[0]
        self.instances.append(instanceStart[1])

    def enterInnerInstance(self, ctx):
        attrCount = 0
        for ele in ctx.AttributeInInstance():
            
            #Check if Template is already defined!
            if self.lastVisitedTemplate not in self.templateDict:
                raise Exception( "Template: " + self.lastVisitedTemplate + " was never declared!")

            # Check if all attrs are set within 
            if ele.getText() not in self.templateDict[self.lastVisitedTemplate]:
                raise Exception("Attribute: " + ele.getText() + " is not defined in template for instance: " + self.instances[-1])

            # Count set attributes
            attrCount += 1

        # Check if only necessary number of attrs are set
        if len(self.templateDict[self.lastVisitedTemplate]) > attrCount:
            raise Exception("One or more attributes are missing or set multiple times in: " + self.instances[-1])


    def enterTransportOrderStep(self, ctx):
        instanceStart =  ctx.TransportOrderStepStart().getText().split()
        self.transportOrderSteps.append(instanceStart[1])


    def enterTask(self, ctx):
        self.tasks.append(ctx.TaskStart().getText()[5:])

    def enterInnerTask(self, ctx):
        for ele in ctx.NewTask():
            if ele.getText() not in self.tasks:
                raise Exception("Task: " + ele.getText() + " was not previosuly defined!")

        pass

    def enterTransportOrder(self, ctx):
        for ele in ctx.NewInstance():
            if ele.getText() not in self.transportOrderSteps:
                raise Exception("TransortOrderStep: " + ele.getText() + " was not previosuly defined!")

def main():
    lexer = TaskLexer(InputStream(open("examples.tl").read()))
    stream = CommonTokenStream(lexer)
    parser = TaskParser(stream)
    tree = parser.program() 
    printer = PythonListener()
    # printer = TaskParserListener()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)

if __name__ == '__main__':
    main() 

