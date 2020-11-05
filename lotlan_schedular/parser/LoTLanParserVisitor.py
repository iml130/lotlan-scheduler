# Generated from LoTLanParser.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .LoTLanParser import LoTLanParser
else:
    from LoTLanParser import LoTLanParser

# This class defines a complete generic visitor for a parse tree produced by LoTLanParser.

class LoTLanParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by LoTLanParser#program.
    def visitProgram(self, ctx:LoTLanParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LoTLanParser#template.
    def visitTemplate(self, ctx:LoTLanParser.TemplateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LoTLanParser#templateStart.
    def visitTemplateStart(self, ctx:LoTLanParser.TemplateStartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LoTLanParser#instance.
    def visitInstance(self, ctx:LoTLanParser.InstanceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LoTLanParser#instanceStart.
    def visitInstanceStart(self, ctx:LoTLanParser.InstanceStartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LoTLanParser#memberVariable.
    def visitMemberVariable(self, ctx:LoTLanParser.MemberVariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LoTLanParser#value.
    def visitValue(self, ctx:LoTLanParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LoTLanParser#transportOrderStep.
    def visitTransportOrderStep(self, ctx:LoTLanParser.TransportOrderStepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LoTLanParser#tosStart.
    def visitTosStart(self, ctx:LoTLanParser.TosStartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LoTLanParser#tosStatement.
    def visitTosStatement(self, ctx:LoTLanParser.TosStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LoTLanParser#locationStatement.
    def visitLocationStatement(self, ctx:LoTLanParser.LocationStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LoTLanParser#optTosStatement.
    def visitOptTosStatement(self, ctx:LoTLanParser.OptTosStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LoTLanParser#eventStatement.
    def visitEventStatement(self, ctx:LoTLanParser.EventStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LoTLanParser#onDoneStatement.
    def visitOnDoneStatement(self, ctx:LoTLanParser.OnDoneStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LoTLanParser#parameterStatement.
    def visitParameterStatement(self, ctx:LoTLanParser.ParameterStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LoTLanParser#task.
    def visitTask(self, ctx:LoTLanParser.TaskContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LoTLanParser#taskStart.
    def visitTaskStart(self, ctx:LoTLanParser.TaskStartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LoTLanParser#taskStatement.
    def visitTaskStatement(self, ctx:LoTLanParser.TaskStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LoTLanParser#constraintsStatement.
    def visitConstraintsStatement(self, ctx:LoTLanParser.ConstraintsStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LoTLanParser#transportOrder.
    def visitTransportOrder(self, ctx:LoTLanParser.TransportOrderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LoTLanParser#fromStatement.
    def visitFromStatement(self, ctx:LoTLanParser.FromStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LoTLanParser#toStatement.
    def visitToStatement(self, ctx:LoTLanParser.ToStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LoTLanParser#parameters.
    def visitParameters(self, ctx:LoTLanParser.ParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LoTLanParser#repeatStatement.
    def visitRepeatStatement(self, ctx:LoTLanParser.RepeatStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LoTLanParser#expression.
    def visitExpression(self, ctx:LoTLanParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LoTLanParser#binOperation.
    def visitBinOperation(self, ctx:LoTLanParser.BinOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LoTLanParser#unOperation.
    def visitUnOperation(self, ctx:LoTLanParser.UnOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LoTLanParser#con.
    def visitCon(self, ctx:LoTLanParser.ConContext):
        return self.visitChildren(ctx)



del LoTLanParser