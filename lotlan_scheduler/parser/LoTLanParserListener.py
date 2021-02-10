# Generated from LoTLanParser.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .LoTLanParser import LoTLanParser
else:
    from LoTLanParser import LoTLanParser

# This class defines a complete listener for a parse tree produced by LoTLanParser.
class LoTLanParserListener(ParseTreeListener):

    # Enter a parse tree produced by LoTLanParser#program.
    def enterProgram(self, ctx:LoTLanParser.ProgramContext):
        pass

    # Exit a parse tree produced by LoTLanParser#program.
    def exitProgram(self, ctx:LoTLanParser.ProgramContext):
        pass


    # Enter a parse tree produced by LoTLanParser#template.
    def enterTemplate(self, ctx:LoTLanParser.TemplateContext):
        pass

    # Exit a parse tree produced by LoTLanParser#template.
    def exitTemplate(self, ctx:LoTLanParser.TemplateContext):
        pass


    # Enter a parse tree produced by LoTLanParser#templateStart.
    def enterTemplateStart(self, ctx:LoTLanParser.TemplateStartContext):
        pass

    # Exit a parse tree produced by LoTLanParser#templateStart.
    def exitTemplateStart(self, ctx:LoTLanParser.TemplateStartContext):
        pass


    # Enter a parse tree produced by LoTLanParser#instance.
    def enterInstance(self, ctx:LoTLanParser.InstanceContext):
        pass

    # Exit a parse tree produced by LoTLanParser#instance.
    def exitInstance(self, ctx:LoTLanParser.InstanceContext):
        pass


    # Enter a parse tree produced by LoTLanParser#instanceStart.
    def enterInstanceStart(self, ctx:LoTLanParser.InstanceStartContext):
        pass

    # Exit a parse tree produced by LoTLanParser#instanceStart.
    def exitInstanceStart(self, ctx:LoTLanParser.InstanceStartContext):
        pass


    # Enter a parse tree produced by LoTLanParser#memberVariable.
    def enterMemberVariable(self, ctx:LoTLanParser.MemberVariableContext):
        pass

    # Exit a parse tree produced by LoTLanParser#memberVariable.
    def exitMemberVariable(self, ctx:LoTLanParser.MemberVariableContext):
        pass


    # Enter a parse tree produced by LoTLanParser#value.
    def enterValue(self, ctx:LoTLanParser.ValueContext):
        pass

    # Exit a parse tree produced by LoTLanParser#value.
    def exitValue(self, ctx:LoTLanParser.ValueContext):
        pass


    # Enter a parse tree produced by LoTLanParser#transportOrderStep.
    def enterTransportOrderStep(self, ctx:LoTLanParser.TransportOrderStepContext):
        pass

    # Exit a parse tree produced by LoTLanParser#transportOrderStep.
    def exitTransportOrderStep(self, ctx:LoTLanParser.TransportOrderStepContext):
        pass


    # Enter a parse tree produced by LoTLanParser#tosStart.
    def enterTosStart(self, ctx:LoTLanParser.TosStartContext):
        pass

    # Exit a parse tree produced by LoTLanParser#tosStart.
    def exitTosStart(self, ctx:LoTLanParser.TosStartContext):
        pass


    # Enter a parse tree produced by LoTLanParser#tosStatement.
    def enterTosStatement(self, ctx:LoTLanParser.TosStatementContext):
        pass

    # Exit a parse tree produced by LoTLanParser#tosStatement.
    def exitTosStatement(self, ctx:LoTLanParser.TosStatementContext):
        pass


    # Enter a parse tree produced by LoTLanParser#locationStatement.
    def enterLocationStatement(self, ctx:LoTLanParser.LocationStatementContext):
        pass

    # Exit a parse tree produced by LoTLanParser#locationStatement.
    def exitLocationStatement(self, ctx:LoTLanParser.LocationStatementContext):
        pass


    # Enter a parse tree produced by LoTLanParser#optTosStatement.
    def enterOptTosStatement(self, ctx:LoTLanParser.OptTosStatementContext):
        pass

    # Exit a parse tree produced by LoTLanParser#optTosStatement.
    def exitOptTosStatement(self, ctx:LoTLanParser.OptTosStatementContext):
        pass


    # Enter a parse tree produced by LoTLanParser#eventStatement.
    def enterEventStatement(self, ctx:LoTLanParser.EventStatementContext):
        pass

    # Exit a parse tree produced by LoTLanParser#eventStatement.
    def exitEventStatement(self, ctx:LoTLanParser.EventStatementContext):
        pass


    # Enter a parse tree produced by LoTLanParser#onDoneStatement.
    def enterOnDoneStatement(self, ctx:LoTLanParser.OnDoneStatementContext):
        pass

    # Exit a parse tree produced by LoTLanParser#onDoneStatement.
    def exitOnDoneStatement(self, ctx:LoTLanParser.OnDoneStatementContext):
        pass


    # Enter a parse tree produced by LoTLanParser#parameterStatement.
    def enterParameterStatement(self, ctx:LoTLanParser.ParameterStatementContext):
        pass

    # Exit a parse tree produced by LoTLanParser#parameterStatement.
    def exitParameterStatement(self, ctx:LoTLanParser.ParameterStatementContext):
        pass


    # Enter a parse tree produced by LoTLanParser#task.
    def enterTask(self, ctx:LoTLanParser.TaskContext):
        pass

    # Exit a parse tree produced by LoTLanParser#task.
    def exitTask(self, ctx:LoTLanParser.TaskContext):
        pass


    # Enter a parse tree produced by LoTLanParser#taskStart.
    def enterTaskStart(self, ctx:LoTLanParser.TaskStartContext):
        pass

    # Exit a parse tree produced by LoTLanParser#taskStart.
    def exitTaskStart(self, ctx:LoTLanParser.TaskStartContext):
        pass


    # Enter a parse tree produced by LoTLanParser#taskStatement.
    def enterTaskStatement(self, ctx:LoTLanParser.TaskStatementContext):
        pass

    # Exit a parse tree produced by LoTLanParser#taskStatement.
    def exitTaskStatement(self, ctx:LoTLanParser.TaskStatementContext):
        pass


    # Enter a parse tree produced by LoTLanParser#constraintsStatement.
    def enterConstraintsStatement(self, ctx:LoTLanParser.ConstraintsStatementContext):
        pass

    # Exit a parse tree produced by LoTLanParser#constraintsStatement.
    def exitConstraintsStatement(self, ctx:LoTLanParser.ConstraintsStatementContext):
        pass


    # Enter a parse tree produced by LoTLanParser#transportOrder.
    def enterTransportOrder(self, ctx:LoTLanParser.TransportOrderContext):
        pass

    # Exit a parse tree produced by LoTLanParser#transportOrder.
    def exitTransportOrder(self, ctx:LoTLanParser.TransportOrderContext):
        pass


    # Enter a parse tree produced by LoTLanParser#fromStatement.
    def enterFromStatement(self, ctx:LoTLanParser.FromStatementContext):
        pass

    # Exit a parse tree produced by LoTLanParser#fromStatement.
    def exitFromStatement(self, ctx:LoTLanParser.FromStatementContext):
        pass


    # Enter a parse tree produced by LoTLanParser#toStatement.
    def enterToStatement(self, ctx:LoTLanParser.ToStatementContext):
        pass

    # Exit a parse tree produced by LoTLanParser#toStatement.
    def exitToStatement(self, ctx:LoTLanParser.ToStatementContext):
        pass


    # Enter a parse tree produced by LoTLanParser#parameters.
    def enterParameters(self, ctx:LoTLanParser.ParametersContext):
        pass

    # Exit a parse tree produced by LoTLanParser#parameters.
    def exitParameters(self, ctx:LoTLanParser.ParametersContext):
        pass


    # Enter a parse tree produced by LoTLanParser#repeatStatement.
    def enterRepeatStatement(self, ctx:LoTLanParser.RepeatStatementContext):
        pass

    # Exit a parse tree produced by LoTLanParser#repeatStatement.
    def exitRepeatStatement(self, ctx:LoTLanParser.RepeatStatementContext):
        pass


    # Enter a parse tree produced by LoTLanParser#expression.
    def enterExpression(self, ctx:LoTLanParser.ExpressionContext):
        pass

    # Exit a parse tree produced by LoTLanParser#expression.
    def exitExpression(self, ctx:LoTLanParser.ExpressionContext):
        pass


    # Enter a parse tree produced by LoTLanParser#binOperation.
    def enterBinOperation(self, ctx:LoTLanParser.BinOperationContext):
        pass

    # Exit a parse tree produced by LoTLanParser#binOperation.
    def exitBinOperation(self, ctx:LoTLanParser.BinOperationContext):
        pass


    # Enter a parse tree produced by LoTLanParser#unOperation.
    def enterUnOperation(self, ctx:LoTLanParser.UnOperationContext):
        pass

    # Exit a parse tree produced by LoTLanParser#unOperation.
    def exitUnOperation(self, ctx:LoTLanParser.UnOperationContext):
        pass


    # Enter a parse tree produced by LoTLanParser#con.
    def enterCon(self, ctx:LoTLanParser.ConContext):
        pass

    # Exit a parse tree produced by LoTLanParser#con.
    def exitCon(self, ctx:LoTLanParser.ConContext):
        pass



del LoTLanParser