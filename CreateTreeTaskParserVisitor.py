from TaskParserVisitor import TaskParserVisitor
from TaskParser import TaskParser

class CompleteProgram(object):
    def __init__(self):
        self.templates = {} # All defined templates
        self.instances = {} # All defined instances
        self.taskInfos = {} # All defined tasks

class TaskInfo(object):
    def __init__(self):
        self.name = None # String Name of Task
        self.triggers = [] # List of Triggers
        self.transportOrders = [] # List of Transport Order (from|to)
        self.onDone = [] # Reference to the next Tasks

class TransportOrder(object):
    def __init__(self):
        self.formm = [] # From many Instances
        self.to = None # Target Instance

class Template(object):
    def __init__(self):
        self.name = None # String of the Template Name
        self.attributes = [] # A List of Attributes

class Instance(object):
    def __init__(self):
        self.name = None # String of the Instances Name
        self.templateName = None # String of the Instances origin Template
        self.keyval = {} # Dictionary of attributes with set value


class CreateTreeTaskParserVisitor(TaskParserVisitor):

    # Visit a parse tree produced by TaskParser#program.
    def visitProgram(self, ctx):
        # Create Program
        cp = CompleteProgram()


        for child in ctx.children:
            TempOrInstOrTask = self.visit(child)  # Get object Template|Instance|Task

            # append appropiatly into the corresponding list
            if isinstance(TempOrInstOrTask, Template):
                cp.templates[TempOrInstOrTask.name] = (TempOrInstOrTask)
            if isinstance(TempOrInstOrTask, Instance):
                cp.instances[TempOrInstOrTask.name] = (TempOrInstOrTask)
            if isinstance(TempOrInstOrTask, TaskInfo):
                cp.taskInfos[TempOrInstOrTask.name] = (TempOrInstOrTask)
        return cp


    # Visit a parse tree produced by TaskParser#template.
    def visitTemplate(self, ctx):
        t = Template()
        # Retreive the Templates name
        t.name = ctx.TemplateStart().getText()[9:] 

        # Iterate until we found an innerTemplate
        for child in ctx.children:
            if isinstance(child, TaskParser.InnerTemplateContext):
                t.attributes.append(self.visitInnerTemplate(child))
                break
        return t


    # Visit a parse tree produced by TaskParser#innerTemplate.
    def visitInnerTemplate(self, ctx):
        l = []
        # Create a List of all Attributes inside a Template
        for ele in ctx.AttributeInTemplate():
            l.append(ele.getText())
        return l


    # Visit a parse tree produced by TaskParser#instance.
    def visitInstance(self, ctx):
        i = Instance()
        # Retreive Template and Instance name
        TempAndInst = ctx.InstanceStart().getText().split()
        i.templateName = TempAndInst[0]
        i.name = TempAndInst[1]

        # Iterate until we found an innerInstance
        for child in ctx.children:
            if isinstance(child, TaskParser.InnerInstanceContext):
                i.keyval = self.visitInnerInstance(child)
                break
        return i


    # Visit a parse tree produced by TaskParser#innerInstance.
    def visitInnerInstance(self, ctx):
        keyval = {}
        # Createa Dictionary of Key-Value pairs in Instance
        for key, val in zip(ctx.AttributeInInstance(), ctx.ValueInInstance()):
            keyval[key.getText()] = val.getText()
        return keyval


    # Visit a parse tree produced by TaskParser#task.
    def visitTask(self, ctx):
        ti = TaskInfo()
        # Retreive Task name
        ti.name = ctx.TaskStart().getText()[5:] 
        
        # Iterate until we found an innerTask
        for child in ctx.children:
            if isinstance(child, TaskParser.InnerTaskContext):
                self.visitInnerTask(child, ti)
                break
        return ti


    # Visit a parse tree produced by TaskParser#innerTask.
    def visitInnerTask(self, ctx, taskInfo):
        # For each onDone we append a new Task
        for trigger in ctx.NewTask():
            taskInfo.onDone.append(trigger.getText())

        # For each Expression Or Trigger we call the functions and append
        for child in ctx.children:
            if isinstance(child, TaskParser.ExpressionContext):
                taskInfo.triggers.append(self.visitExpression(child))
            if isinstance(child, TaskParser.TransportOrderContext):
                taskInfo.transportOrders.append(self.visitTransportOrder(child))
            

        
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TaskParser#transportOrder.
    def visitTransportOrder(self, ctx):
        to = TransportOrder
        l = []
        # Create the List
        for srcDst in ctx.NewInstance():
            l.append(srcDst.getText())

        # Extract From/To
        dst = l[-1]
        l = l[:-1]
        to.fromm = l
        to.to = dst
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
        # Just Return the Operation
        return ctx.op.text


    # Visit a parse tree produced by TaskParser#unOperation.
    def visitUnOperation(self, ctx):
        return ctx.op.text


    # Visit a parse tree produced by TaskParser#con.
    def visitCon(self, ctx):
        return ctx.c.text


