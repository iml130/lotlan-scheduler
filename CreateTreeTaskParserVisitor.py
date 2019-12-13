from TaskParserVisitor import TaskParserVisitor
from TaskParser import TaskParser
from enum import Enum

import copy

class OptType(Enum):
    TRIGGERED_BY = 1
    FINISHED_BY = 2
    ON_DONE = 3

class CompleteProgram(object):
    def __init__(self):
        self.templates = {} # All defined templates
        self.instances = {} # All defined instances
        self.transportOrderSteps = {} # All defined TaskOrderSteps
        self.taskInfos = {} # All defined tasks

class TaskInfo(object):
    def __init__(self):
        self.name = None # String Name of Task
        self.triggeredBy = [] # List of Triggers
        self.transportOrders = [] # List of Transport Order (from|to)
        self.onDone = [] # Reference to the next Tasks
        self.repeat = -1 # uninitialized
        self.finishedBy = []

class TransportOrder(object):
    def __init__(self):
        self.pickupFrom = None# From Instance
        self.deliverTo = None # Target Instance

class TransportOrderStep(object):
    def __init__(self):
        self.name = None # String Name of Task
        self.location = None
        self.triggeredBy = [] # List of Triggers
        self.finishedBy = []
        self.onDone = [] # Reference to the next Tasks
        
class Template(object):
    def __init__(self):
        self.name = None # String of the Template Name
        self.keyval = [] # A List of Attributes

class Instance(object):
    def __init__(self):
        self.name = None # String of the Instances Name
        self.templateName = None # String of the Instances origin Template
        self.keyval = {} # Dictionary of attributes with set value


class CreateTreeTaskParserVisitor(TaskParserVisitor):

    # Visit a parse tree produced by TaskParser#program.
    def visitProgram(self, ctx):
        # Create Program
        self.cp = CompleteProgram()
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

    def printProgram(self):
        for template in self.cp.templates.values():
            print("Template Name:", template.name)
            print("Keyval:", template.keyval)
            print("\n")
        for instance in self.cp.instances.values():
            print("Template Name:", instance.templateName)
            print("Instance Name:", instance.name)
            print("Keyval:", instance.keyval)
            print("\n")
        for tos in self.cp.transportOrderSteps.values():
            print("TransportOrderStepName:", tos.name)
            print("Location:", tos.location)
            print("Triggered By:", tos.triggeredBy)
            print("Finished By:", tos.finishedBy)
            print("OnDone:", tos.onDone)
            print("\n")
        for task in self.cp.taskInfos.values():
            print("TaskName:", task.name)
            print("Transport Order:", task.transportOrders)
            print("Triggered By:", task.triggeredBy)
            print("Finished By:", task.finishedBy)
            print("OnDone:", task.onDone)
            print("Repeat:", task.repeat)
            print("\n")

    # Visit a parse tree produced by TaskParser#template.
    def visitTemplate(self, ctx):
        t = Template()
        t.name = ctx.UpperCaseString().getText()

        keyval = {}
        for child in ctx.memberVariable():
            variableContent = self.visitMemberVariable(child)
            keyval[variableContent[0]] = variableContent[1]
        i.keyval = keyval

        return t

    def visitTemplateStart(self, ctx):
        return ctx.STARTS_WITH_UPPER_C_STR().getText()

    # Visit a parse tree produced by TaskParser#instance.
    def visitInstance(self, ctx):
        i = Instance()

        # Retreive Template and Instance name
        names = self.visitInstanceStart(ctx.instanceStart())

        i.templateName = names[0]
        i.name = names[1]

        keyval = {}
        for child in ctx.memberVariable():
            variableContent = self.visitMemberVariable(child)
            keyval[variableContent[0]] = variableContent[1]
        i.keyval = keyval

        return i

    def visitInstanceStart(self, ctx):
        templateName = ctx.INSTANCE().getText().split(" ")[0] # get template name without whitespace after it
        instanceName = ctx.STARTS_WITH_LOWER_C_STR().getText()

        return (templateName, instanceName)

    def visitMemberVariable(self, ctx):
        variableName = ctx.STARTS_WITH_LOWER_C_STR().getText()
        value = self.visitValue(ctx.value())

        return (variableName, value)

    def visitValue(self, ctx):
        value = 0

        if ctx.STRING_VALUE():
            value = ctx.STRING_VALUE().getText()
        elif ctx.NUMERIC_VALUE():
            value = ctx.NUMERIC_VALUE().getText()
        else:
            value = ctx.EMPTY_VALUE().getText()

        return value

    def visitTransportOrderStep(self, ctx):
        tos = TransportOrderStep()
        tos.name = self.visitTosStart(ctx.tosStart())
        self.visitTosStatements(ctx.tosStatements(), tos)
        return tos

    def visitTosStart(self, ctx):
        return ctx.STARTS_WITH_LOWER_C_STR().getText()

    def visitTosStatements(self, ctx, tos):
        for child in ctx.children:
            if isinstance(child, TaskParser.OptTosStatementContext):
                values = self.visitOptTosStatement(child)
                if values[1] == OptType.TRIGGERED_BY:
                    tos.triggeredBy.append(values[0])
                elif values[1] == OptType.FINISHED_BY:
                    tos.finishedBy.append(values[0])
                elif values[1] == OptType.ON_DONE:
                    tos.onDone.append(values[0])

            elif isinstance(child, TaskParser.LocationStatementContext):
                location = self.visitLocationStatement(child)
                tos.location = location
    
    def visitLocationStatement(self, ctx):
        return ctx.STARTS_WITH_LOWER_C_STR().getText()

    def visitOptTosStatement(self, ctx):
        childs = ctx.children
        for i  in range(len(ctx.children)):
            if childs[i] == ctx.TRIGGERED_BY():
                return(self.visitExpression(childs[i+1]), OptType.TRIGGERED_BY)
            if childs[i] == ctx.FINISHED_BY():
                return(self.visitExpression(childs[i+1]), OptType.FINISHED_BY)
            elif childs[i] == ctx.ON_DONE():
                return(ctx.STARTS_WITH_UPPER_C_STR().getText(), OptType.ON_DONE)

    # Visit a parse tree produced by TaskParser#task.
    def visitTask(self, ctx):
        ti = TaskInfo()
        ti.name = self.visitTaskStart(ctx.taskStart())
        
        for child in ctx.taskStatement():
            self.visitTaskStatement(child, ti)

        return ti

    def visitTaskStart(self, ctx):
        return ctx.STARTS_WITH_UPPER_C_STR().getText()

    def visitTaskStatement(self, ctx, taskInfo):
        if ctx.REPEAT_TIMES():
            taskInfo.repeat = ctx.REPEAT_TIMES().getText()
        elif ctx.optTosStatement():
            values = self.visitOptTosStatement(ctx.optTosStatement())
            if values[1] == OptType.TRIGGERED_BY:
                taskInfo.triggeredBy.append(values[0])
            elif values[1] == OptType.FINISHED_BY:
                taskInfo.finishedBy.append(values[0])
            elif values[1] == OptType.ON_DONE:
                taskInfo.onDone.append(values[0])
        elif ctx.transportOrder():
            taskInfo.transportOrders.append(self.visitTransportOrder(ctx.transportOrder()))

    # Visit a parse tree produced by TaskParser#transportOrder.
    def visitTransportOrder(self, ctx):
        to = TransportOrder()

        childs = ctx.children
        for i in range(len(childs)):
            if childs[i] == ctx.FROM():
                to.pickupFrom = childs[i+1].getText()
            elif childs[i] == ctx.TO():
                to.deliverTo = childs[i+1].getText()

        return to

    ### Expression parsing:

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
        return 