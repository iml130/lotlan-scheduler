__author__ = "Maximilian Hörstrup"
__version__ = "0.0.1"
__maintainer__ = "Maximilian Hörstrup"

# standard libraries
from enum import Enum

# local sources
from TaskParserVisitor import TaskParserVisitor
from TaskParser import TaskParser

from transport.CompleteProgram import CompleteProgram, ContextObject
from transport.Template import Template
from transport.Instance import Instance
from transport.TaskInfo import TaskInfo, TransportOrder
from transport.TransportOrderStep import TransportOrderStep

import re

# Enum to set the type of the optional statement when returned
class OptType(Enum):
    TRIGGERED_BY = 1
    FINISHED_BY = 2
    ON_DONE = 3

class CreateTreeTaskParserVisitor(TaskParserVisitor):
    def __init__(self):
        super()

    # Visit a parse tree produced by TaskParser#program.
    def visitProgram(self, ctx):
        # Create Program
        self.cp = CompleteProgram()

        if ctx.children:
            for child in ctx.children:
                TempOrInstOrTaskOrTOS = self.visit(child)  # Get object Template|Instance|Task

                # append appropiatly into the corresponding list
                if isinstance(TempOrInstOrTaskOrTOS, Template):
                    self.cp.templates[TempOrInstOrTaskOrTOS.name] = (TempOrInstOrTaskOrTOS)
                if isinstance(TempOrInstOrTaskOrTOS, Instance):
                    self.cp.instances[TempOrInstOrTaskOrTOS.name] = (TempOrInstOrTaskOrTOS)
                if isinstance(TempOrInstOrTaskOrTOS, TaskInfo):
                    self.cp.taskInfos[TempOrInstOrTaskOrTOS.name] = (TempOrInstOrTaskOrTOS)
                if isinstance(TempOrInstOrTaskOrTOS, TransportOrderStep):
                    self.cp.transportOrderSteps[TempOrInstOrTaskOrTOS.name] = (TempOrInstOrTaskOrTOS)

        return self.cp

    # Visit a parse tree produced by TaskParser#template.
    def visitTemplate(self, ctx):
        t = Template()
        t.name = self.visitTemplateStart(ctx.templateStart())
        t.context = ctx

        keyval = []
        for child in ctx.memberVariable():
            variableContent = self.visitMemberVariable(child)
            keyval.append(variableContent[0])
        t.keyval = keyval

        return t

    # Visit a parse tree produced by TaskParser#templateStart.   
    def visitTemplateStart(self, ctx):
        return ContextObject(ctx.TEMPLATE().getText().split(" ")[1], ctx)

    # Visit a parse tree produced by TaskParser#instance.
    def visitInstance(self, ctx):
        i = Instance()

        # Retreive Template and Instance name
        names = self.visitInstanceStart(ctx.instanceStart())

        i.templateName = names[0]
        i.name = names[1]
        i.context = ctx

        keyval = {}
        for child in ctx.memberVariable():
            variableContent = self.visitMemberVariable(child)
            keyval[variableContent[0]] = variableContent[1]
        i.keyval = keyval

        return i

    # Visit a parse tree produced by TaskParser#instanceStart.
    def visitInstanceStart(self, ctx):
        templateName = ContextObject(ctx.INSTANCE().getText().split(" ")[0], ctx) # get template name without whitespace after it
        instanceName = ContextObject(ctx.STARTS_WITH_LOWER_C_STR().getText(), ctx)

        return (templateName, instanceName)

    # Visit a parse tree produced by TaskParser#memberVariable.
    def visitMemberVariable(self, ctx):
        assignmentStr = ctx.ASSIGNMENT().getText()

        p = re.compile('\w+')
        assignmentStr = p.search(assignmentStr).group(0)
        variableName = ContextObject(assignmentStr, ctx)
        value = ContextObject(self.visitValue(ctx.value()), ctx)

        return (variableName, value)


    # Visit a parse tree produced by TaskParser#value.
    def visitValue(self, ctx):
        value = 0

        if ctx.STRING_VALUE():
            value = ctx.STRING_VALUE().getText()
        elif ctx.NUMERIC_VALUE():
            value = ctx.NUMERIC_VALUE().getText()
        else:
            value = ctx.EMPTY_VALUE().getText()

        return value

    # Visit a parse tree produced by TaskParser#transportOrderStep.
    def visitTransportOrderStep(self, ctx):
        tos = TransportOrderStep()
        tos.name = self.visitTosStart(ctx.tosStart())
        tos.context = ctx

        for child in ctx.tosStatement():
            self.visitTosStatement(child, tos)
        return tos

    # Visit a parse tree produced by TaskParser#tosStart.
    def visitTosStart(self, ctx):
        return ContextObject(ctx.STARTS_WITH_LOWER_C_STR().getText(), ctx)

    # Visit a parse tree produced by TaskParser#tosStatements.
    def visitTosStatement(self, ctx, tos):
        if ctx.optTosStatement():
            values = self.visitOptTosStatement(ctx.optTosStatement())
            if values[1] == OptType.TRIGGERED_BY:
                tos.triggeredBy.append(ContextObject(values[0], ctx.optTosStatement()))
            elif values[1] == OptType.FINISHED_BY:
                tos.finishedBy.append(ContextObject(values[0], ctx.optTosStatement()))
            elif values[1] == OptType.ON_DONE:
                tos.onDone.append(ContextObject(values[0], ctx.optTosStatement()))
        elif ctx.locationStatement():
            location = self.visitLocationStatement(ctx.locationStatement())
            tos.locations.append(ContextObject(location, ctx.locationStatement()))
        elif ctx.parameterStatement():
            parameters = self.visitParameterStatement(ctx.parameterStatement())
            tos.parameters = parameters
    
    def visitParameterStatement(self, ctx):
        parameters = []
        for parameter in ctx.STARTS_WITH_LOWER_C_STR():
            parameters.append(ContextObject(parameter.getText(), ctx))
        return parameters

    # Visit a parse tree produced by TaskParser#Location Statement.
    def visitLocationStatement(self, ctx):
        return ctx.STARTS_WITH_LOWER_C_STR().getText()

    # Visit a parse tree produced by TaskParser#optTosStatement.
    def visitOptTosStatement(self, ctx):
        childs = ctx.children
        for i  in range(len(ctx.children)):
            if childs[i] == ctx.eventStatement():
                return self.visitEventStatement(ctx.eventStatement())
            elif childs[i] == ctx.onDoneStatement():
                return self.visitOnDoneStatement(ctx.onDoneStatement())

    def visitEventStatement(self, ctx):
        if ctx.TRIGGERED_BY():
            return (self.visitExpression(ctx.expression()), OptType.TRIGGERED_BY)
        elif ctx.FINISHED_BY():
            return (self.visitExpression(ctx.expression()), OptType.FINISHED_BY)

    def visitOnDoneStatement(self, ctx):
        return (ctx.STARTS_WITH_LOWER_C_STR().getText(), OptType.ON_DONE)

    # Visit a parse tree produced by TaskParser.
    def visitTask(self, ctx):
        ti = TaskInfo()
        ti.name = self.visitTaskStart(ctx.taskStart())
        ti.context = ctx

        for child in ctx.taskStatement():
            self.visitTaskStatement(child, ti)
        return ti

    # Visit a parse tree produced by TaskParser#taskStart.
    def visitTaskStart(self, ctx):
        return ContextObject(ctx.STARTS_WITH_LOWER_C_STR().getText(), ctx)

    # Visit a parse tree produced by TaskParser#taskStatement.
    def visitTaskStatement(self, ctx, taskInfo):
        if(ctx.repeatStatement()):
            taskInfo.repeat.append(self.visitRepeatStatement(ctx.repeatStatement()))
        elif ctx.optTosStatement():
            values = self.visitOptTosStatement(ctx.optTosStatement())
            if values[1] == OptType.TRIGGERED_BY:
                taskInfo.triggeredBy.append(ContextObject(values[0], ctx))
            elif values[1] == OptType.FINISHED_BY:
                taskInfo.finishedBy.append(ContextObject(values[0], ctx))
            elif values[1] == OptType.ON_DONE:
                taskInfo.onDone.append(ContextObject(values[0], ctx))
        elif ctx.transportOrder():
            taskInfo.transportOrders.append(ContextObject(self.visitTransportOrder(ctx.transportOrder()), ctx))

    # Visit a parse tree produced by TaskParser#transportOrder.
    def visitTransportOrder(self, ctx):
        transportOrder = TransportOrder()

        childs = ctx.children
        for i in range(len(childs)):
            if childs[i] == ctx.fromStatement():
                self.visitFromStatement(ctx.fromStatement(), transportOrder)
            elif childs[i] == ctx.toStatement():
                self.visitToStatement(ctx.toStatement(), transportOrder)
        return transportOrder

    def visitFromStatement(self, ctx, transportOrder):
        transportOrder.pickupFrom = ContextObject(ctx.STARTS_WITH_LOWER_C_STR().getText(), ctx.STARTS_WITH_LOWER_C_STR())
        parameters = ctx.parameters()
        if parameters != None:
            for parameter in parameters.children:
                if parameter.getText() != ",":
                    transportOrder.fromParameters.append(parameter.getText())

    def visitToStatement(self, ctx, transportOrder):
        transportOrder.deliverTo = ContextObject(ctx.STARTS_WITH_LOWER_C_STR().getText(), ctx.STARTS_WITH_LOWER_C_STR())
        parameters = ctx.parameters()
        if parameters != None:
            for parameter in parameters.children:
                if parameter.getText() != ",":
                    transportOrder.toParameters.append(parameter.getText())

    def visitParameters(self, ctx):
        parameters = []
        if len(ctx) > 0:
            for parameter in ctx:
                parameters.append(ContextObject(parameter.getText(), ctx))
        return parameters

    def visitRepeatStatement(self, ctx):
        return ContextObject(ctx.INTEGER().getText(), ctx)

    # Visit a parse tree produced by TaskParser#expression.
    def visitExpression(self, ctx):
        length =  len(ctx.children)
        # CASE: 1 Terminal,  returns TERMINAL
        # CASE: 2 UnOperation, returns {unop: !, value: EXPRESSION}
        # CASE: 3 binOperation:, returns {op: (==|!=|<=|..|), left: EXPRESSION, right:EXPRESSION}
        if length == 1:
            ele = self._getContent(ctx.children[0])
            return ele
        if length == 2: 
            unOp = self._getContent(ctx.children[0]) # UnOperation
            ele = self._getContent(ctx.children[1]) # Attribute
            return dict(unop=unOp, value=ele)

        if length == 3: 
            left = self._getContent(ctx.children[0]) # left
            binOp = self._getContent(ctx.children[1]) # binOperation
            right = self._getContent(ctx.children[2]) # right
            return dict(binOp=binOp, left=left, right=right)

        return None

    def _getContent(self, child):
        ele =  self.visit(child)
        # If None, then an instance.value is used!
        if ele == None:
            ele = child.getText()
        return ele

    # Visit a parse tree produced by TaskParser#binOperation.
    def visitBinOperation(self, ctx):
        return ctx.children[0].getText()

    # Visit a parse tree produced by TaskParser#unOperation.
    def visitUnOperation(self, ctx):
        return ctx.children[0].getText()

    # Visit a parse tree produced by TaskParser#con.
    def visitCon(self, ctx):
        return ctx.children[0].getText()