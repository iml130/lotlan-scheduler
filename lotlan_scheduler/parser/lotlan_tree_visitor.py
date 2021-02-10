""" Contains LotlanTreeVisitor """

# standard libraries
from enum import Enum
import re

# local sources
from lotlan_scheduler.model.transport.transport import Transport
from lotlan_scheduler.model.transport.template import Template
from lotlan_scheduler.model.transport.instance import Instance
from lotlan_scheduler.model.transport.task import Task

from lotlan_scheduler.api.transportorder_step import TransportOrderStep
from lotlan_scheduler.api.transportorder import TransportOrder
from lotlan_scheduler.api.location import Location
from lotlan_scheduler.api.event import Event

# globals defines
from lotlan_scheduler.defines import (TRIGGERED_BY_KEY, FINISHED_BY_KEY, REPEAT_KEY,
                     ON_DONE_KEY, TRANSPORT_ORDER_KEY, LOCATION_KEY)

from lotlan_scheduler.parser.LoTLanParserVisitor import LoTLanParserVisitor

class OptionaStatement(Enum):
    '''
        Enum to set the type of the optional statement when returned
    '''
    TRIGGERED_BY = 1
    FINISHED_BY = 2
    ON_DONE = 3


class LotlanTreeVisitor(LoTLanParserVisitor):
    '''
        Uses visitor pattern from antlr to traverse the parse tree
        and store program information in a Transport object
    '''

    def __init__(self, error_listener):
        super()
        self.context_object = {}
        self.error_listener = error_listener

    # Visit a parse tree produced by TaskParser#program.
    def visitProgram(self, ctx):
        # Create Program
        self.cp = Transport()
        self.cp.context_object = self.context_object

        if ctx.children:
            for child in ctx.children:
                program_component = self.visit(child)  # Get object Template|Instance|Task|TOS

                # append appropiatly into the corresponding list
                if isinstance(program_component, Template):
                    if program_component.name not in self.cp.templates:
                        self.cp.templates[program_component.name] = (program_component)
                    else:
                        msg = "There is already an template with the same name defined"
                        self.error_listener.print_error(msg, child.start.line, child.start.column, 1)
                if isinstance(program_component, Instance):
                    if program_component.name not in self.cp.instances:
                        self.cp.instances[program_component.name] = (program_component)
                    else:
                        msg = "There is already an instance with the same name defined"
                        self.error_listener.print_error(msg, child.start.line, child.start.column, 1)
                if isinstance(program_component, Task):
                    if program_component.name not in self.cp.tasks:
                        self.cp.tasks[program_component.name] = (program_component)
                    else:
                        msg = "There is already a task with the same name defined"
                        self.error_listener.print_error(msg, child.start.line, child.start.column, 1)
                if isinstance(program_component, TransportOrderStep):
                    if program_component.name not in self.cp.transport_order_steps:
                        self.cp.transport_order_steps[program_component.name] = (program_component)
                    else:
                        msg = "There is already a transport order step with the same name defined"
                        self.error_listener.print_error(msg, child.start.line, child.start.column, 1)

        # Add tos for transport order to task
        for task in self.cp.tasks.values():
            to = task.transport_order
            if to is not None:
                try:
                    to.pickup_tos = self.cp.transport_order_steps[to.pickup_tos.name]
                    to.delivery_tos = self.cp.transport_order_steps[to.delivery_tos.name]
                except KeyError:
                    pass

        for tos in self.cp.transport_order_steps.values():
            event_instances = {}
            for instance in self.cp.instances.values():
                if instance.template_name == "Event":
                    event_instances[instance.name] = instance

            self.get_events_from_tos(tos.triggered_by_statements, event_instances, tos.triggered_by)
            self.get_events_from_tos(tos.finished_by_statements, event_instances, tos.finished_by)

        return self.cp

    def get_events_from_tos(self, expression, events, event_list, value=None, comparator=None):
        if type(expression) == str and expression != "" and expression in events:
            if value is None:
                value = True
            if comparator is None:
                comparator = "=="

            logical_name = expression
            physical_name = events[logical_name].keyval["name"]
            event_type = events[logical_name].keyval["type"]
    
            event_list.append(Event(logical_name, physical_name, event_type, comparator, value))

        elif type(expression) == dict:
            if len(expression) == 2:
                self.get_events_from_tos(expression["value"], events, event_list, value=False, comparator="!")
            elif len(expression) == 3:
                if expression["binOp"] == ".":
                    self.get_events_from_tos(str(expression["left"] + "." + str(expression["right"])), events, event_list)
                elif expression["left"] == "(" and expression["right"] == ")":
                    self.get_events_from_tos(expression["binOp"], events, event_list)
                elif type(expression["right"]) == str:
                    self.get_events_from_tos(str(expression["left"]), events, event_list, value=expression["right"], comparator=expression["binOp"])
                else:
                    self.get_events_from_tos(expression["left"], events, event_list)
                    self.get_events_from_tos(expression["right"], events, event_list)

    # Visit a parse tree produced by TaskParser#template
    def visitTemplate(self, ctx):
        t = Template()
        t.name = self.visitTemplateStart(ctx.templateStart())
        t.context = ctx

        keyval = []
        for child in ctx.memberVariable():
            variable_content = self.visitMemberVariable(child)
            keyval.append(variable_content[0])
        t.keyval = keyval

        return t

    # Visit a parse tree produced by TaskParser#templateStart
    def visitTemplateStart(self, ctx):
        return ctx.TEMPLATE().getText().split(" ")[1]

    # Visit a parse tree produced by TaskParser#instance
    def visitInstance(self, ctx):
        instance = Instance()

        # Retreive Template and Instance name
        names = self.visitInstanceStart(ctx.instanceStart())

        instance.template_name = names[0]
        instance.name = names[1]
        instance.context = ctx

        keyval = {}
        for child in ctx.memberVariable():
            variable_content = self.visitMemberVariable(child)

            variable = variable_content[0]
            value = variable_content[1]
            value = value.replace('"', "")

            keyval[variable] = value

            if variable in instance.context_dict:
                print("multiple definitions of variable " + variable)
            else:
                instance.context_dict[variable] = child
        instance.keyval = keyval

        return instance

    # Visit a parse tree produced by TaskParser#instanceStart
    def visitInstanceStart(self, ctx):
        template_name = ctx.INSTANCE().getText().split(" ")[0]
        instance_name = ctx.STARTS_WITH_LOWER_C_STR().getText()

        return (template_name, instance_name)

    # Visit a parse tree produced by TaskParser#memberVariable.
    def visitMemberVariable(self, ctx):
        assignment_str = ctx.ASSIGNMENT().getText()

        p = re.compile(r'\w+')
        variable_name = p.search(assignment_str).group(0)

        return (variable_name, self.visitValue(ctx.value()))

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
        return ctx.STARTS_WITH_LOWER_C_STR().getText()

    # Visit a parse tree produced by TaskParser#tosStatements.
    def visitTosStatement(self, ctx, tos):
        context_dict = tos.context_dict

        if ctx.optTosStatement():
            values = self.visitOptTosStatement(ctx.optTosStatement())
            context = ctx.optTosStatement()

            if values[1] == OptionaStatement.TRIGGERED_BY:
                if TRIGGERED_BY_KEY not in context_dict:
                    tos.triggered_by_statements = values[0]
                    context_dict[TRIGGERED_BY_KEY] = context
                else:
                    msg = "TriggeredBy is definied multiple times"
                    self.error_listener.print_error(msg, context.start.line, context.start.column, len("TriggeredBy"))
            elif values[1] == OptionaStatement.FINISHED_BY:
                if FINISHED_BY_KEY not in context_dict:
                    tos.finished_by_statements = values[0]
                    context_dict[FINISHED_BY_KEY] = context
                else:
                    msg = "FinishedBy is definied multiple times"
                    self.error_listener.print_error(msg, context.start.line, context.start.column, len("FinishedBy"))
            elif values[1] == OptionaStatement.ON_DONE:
                if ON_DONE_KEY not in context_dict:
                    tos.on_done = values[0]
                    context_dict[ON_DONE_KEY] = context
                else:
                    msg = "OnDone is definied multiple times"
                    self.error_listener.print_error(msg, context.start.line, context.start.column, len("OnDone"))
        elif ctx.locationStatement():
            if LOCATION_KEY not in context_dict:
                tos.location = self.visitLocationStatement(ctx.locationStatement())
                context_dict[LOCATION_KEY] = ctx.locationStatement()
            else:
                context = ctx.locationStatement()
                msg = "Location is definied multiple times"
                self.error_listener.print_error(msg, context.start.line, context.start.column, len("Location"))
        elif ctx.parameterStatement():
            parameters = self.visitParameterStatement(ctx.parameterStatement())
            tos.parameters = parameters

    def visitParameterStatement(self, ctx):
        parameters = []
        for parameter in ctx.STARTS_WITH_LOWER_C_STR():
            parameters.append(parameter.getText())
        return parameters

    # Visit a parse tree produced by TaskParser#Location Statement.
    def visitLocationStatement(self, ctx):
        location = Location(ctx.STARTS_WITH_LOWER_C_STR().getText(), "", "")
        return location

    # Visit a parse tree produced by TaskParser#optTosStatement.
    def visitOptTosStatement(self, ctx):
        childs = ctx.children
        for i in range(len(ctx.children)):
            if childs[i] == ctx.eventStatement():
                return self.visitEventStatement(ctx.eventStatement())
            elif childs[i] == ctx.onDoneStatement():
                return self.visitOnDoneStatement(ctx.onDoneStatement())

    def visitEventStatement(self, ctx):
        if ctx.TRIGGERED_BY():
            return (self.visitExpression(ctx.expression()), OptionaStatement.TRIGGERED_BY)
        elif ctx.FINISHED_BY():
            return (self.visitExpression(ctx.expression()), OptionaStatement.FINISHED_BY)

    def visitOnDoneStatement(self, ctx):
        on_done = []
        for task in ctx.STARTS_WITH_LOWER_C_STR():
            on_done.append(task.getText())
        return (on_done, OptionaStatement.ON_DONE)

    # Visit a parse tree produced by TaskParser.
    def visitTask(self, ctx):
        ti = Task()
        ti.name = self.visitTaskStart(ctx.taskStart())
        ti.context = ctx

        for child in ctx.taskStatement():
            self.visitTaskStatement(child, ti)
        return ti

    # Visit a parse tree produced by TaskParser#taskStart.
    def visitTaskStart(self, ctx):
        return ctx.STARTS_WITH_LOWER_C_STR().getText()

    # Visit a parse tree produced by TaskParser#taskStatement.
    def visitTaskStatement(self, ctx, task_info):
        context_dict = task_info.context_dict

        if(ctx.repeatStatement()):
            repeat_stmt = self.visitRepeatStatement(ctx.repeatStatement())
            if REPEAT_KEY not in context_dict:
                context_dict[REPEAT_KEY] = ctx.repeatStatement()
                task_info.repeat = repeat_stmt
            else:
                context = ctx.repeatStatement()
                msg = "Repeat was defined multiple times!"
                self.error_listener.print_error(msg, context.start.line, context.start.column, len("Repeat"))
        elif ctx.optTosStatement():
            values = self.visitOptTosStatement(ctx.optTosStatement())
            context = ctx.optTosStatement()

            if values[1] == OptionaStatement.TRIGGERED_BY:
                if TRIGGERED_BY_KEY not in context_dict:
                    task_info.triggered_by = values[0]
                    task_info.context_dict[TRIGGERED_BY_KEY] = ctx.optTosStatement()
                else:
                    msg = "TriggeredBy is definied multiple times"
                    self.error_listener.print_error(msg, context.start.line, context.start.column, len("TriggeredBy"))
            elif values[1] == OptionaStatement.FINISHED_BY:
                if FINISHED_BY_KEY not in context_dict:
                    task_info.finished_by = values[0]
                    task_info.context_dict[FINISHED_BY_KEY] = ctx.optTosStatement()
                else:
                    msg = "FinishedBy is definied multiple times"
                    self.error_listener.print_error(msg, context.start.line, context.start.column, len("FinishedBy"))
            elif values[1] == OptionaStatement.ON_DONE:
                if ON_DONE_KEY not in context_dict:
                    task_info.on_done = values[0]
                    context_dict[ON_DONE_KEY] = ctx.optTosStatement()
                else:
                    msg = "OnDone is definied multiple times"
                    self.error_listener.print_error(msg, context.start.line, context.start.column, len("OnDone"))
        elif ctx.transportOrder():
            if TRANSPORT_ORDER_KEY not in context_dict:
                task_info.transport_order = self.visitTransportOrder(ctx.transportOrder())
                context_dict[TRANSPORT_ORDER_KEY] = ctx.optTosStatement()
            else:
                context = ctx.transportOrder()
                msg = "TransportOrder was defined multiple times"
                self.error_listener.print_error(msg, context.start.line, context.start.column, len("Transport"))

    # Visit a parse tree produced by TaskParser#transportOrder.
    def visitTransportOrder(self, ctx):
        transport_order = TransportOrder()

        childs = ctx.children
        for i in range(len(childs)):
            if childs[i] == ctx.fromStatement():
                self.visitFromStatement(ctx.fromStatement(), transport_order)
            elif childs[i] == ctx.toStatement():
                self.visitToStatement(ctx.toStatement(), transport_order)
        return transport_order

    def visitFromStatement(self, ctx, transport_order):
        transport_order.pickup_tos.name = ctx.STARTS_WITH_LOWER_C_STR().getText()
        parameters = ctx.parameters()
        if parameters is not None:
            for parameter in parameters.children:
                if parameter.getText() != ",":
                    transport_order.from_parameters.append(parameter.getText())

    def visitToStatement(self, ctx, transport_order):
        transport_order.delivery_tos.name = ctx.STARTS_WITH_LOWER_C_STR().getText()
        parameters = ctx.parameters()
        if parameters is not None:
            for parameter in parameters.children:
                if parameter.getText() != ",":
                    transport_order.to_parameters.append(parameter.getText())

    def visitParameters(self, ctx):
        parameters = []
        if ctx:
            for parameter in ctx:
                parameters.append(parameter.getText())
        return parameters

    def visitRepeatStatement(self, ctx):
        return ctx.INTEGER().getText()

    # Visit a parse tree produced by TaskParser#expression.
    def visitExpression(self, ctx):
        length = len(ctx.children)

        if length == 1:  # Terminal,  returns TERMINAL
            ele = self._getContent(ctx.children[0])
            return ele
        if length == 2:  # UnOperation, returns {unop: !, value: EXPRESSION}
            unOp = self._getContent(ctx.children[0])
            ele = self._getContent(ctx.children[1])
            return dict(unop=unOp, value=ele)

        if length == 3:  # binOperation:, returns {op: (==|!=|<=|..|), left: EXPRESSION, right:EXPRESSION}
            left = self._getContent(ctx.children[0])
            binOp = self._getContent(ctx.children[1])
            right = self._getContent(ctx.children[2])
            return dict(binOp=binOp, left=left, right=right)

        return None

    def _getContent(self, child):
        ele = self.visit(child)
        # If None, then an instance.value is used!
        if ele is None:
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
