from CreateTreeTaskParserVisitor import CompleteProgram
from CreateTreeTaskParserVisitor import Instance
from CreateTreeTaskParserVisitor import TaskInfo
from CreateTreeTaskParserVisitor import Template
from CreateTreeTaskParserVisitor import TransportOrder

import copy

class SemanticValidator:
    def __init__(self, filePath, templates, usedInExtension):
        self.filePath = filePath
        self.templates = templates
        self.givenTree = None
        self.errorCount = 0
        self.usedInExtension = usedInExtension

    def isValid(self, givenTree):
        self.givenTree = givenTree

        self.checkTemplates(givenTree) 
        self.checkInstances(givenTree) 
        self.checkTransportOrderSteps(givenTree)
        self.checkTasks(givenTree)

        if self.errorCount > 0:
            return False
        return True


    # Template Check

    def checkTemplates(self, givenTree):
        templateNameCounts = {}
        for template in givenTree.templates.values():
            # check if there is more than one template with the same name
            if templateNameCounts.get(template.name.value) != None:
                msg = "The Template name '{}' is already used by an other template".format(template.name.value)
                self.printError(msg, template.name.context.start.line, template.name.context.start.column, len(template.name.value))
            else:
                templateNameCounts[template.name.value] = 1


    # Instance Check

    def checkInstances(self, givenTree):
        instanceNameCounts = {}
        for instance in givenTree.instances.values():
            # check if there is more than one instance with the same name
            if instanceNameCounts.get(instance.name.value) != None:
                msg = "The Instance name '{}' is already used by an other instance".format(instance.name.value)
                self.printError(msg, instance.name.context.start.line, instance.name.context.start.column, len(instance.name.value))
            else:
                instanceNameCounts[instance.name.value] = 1

            templateName = instance.templateName.value
            template = self.getTemplate(givenTree, templateName)

            # check if the corresponding template exists
            if template == None:
                msg = "The Instance '{}' refers to a template that does not exist".format(instance.name.value)
                self.printError(msg, instance.name.context.start.line, instance.name.context.start.column, len(instance.name.value))
            # check if the instance variables match with the corresponding template
            else:
                if self.templateAttributeExists(template, instance) == False or self.templateAttributeDefinied(template, instance) == False:
                    # TODO
                    self.errorCount = self.errorCount + 1

    # check if all attributes in the given instance are definied in the template
    def templateAttributeExists(self, template, instance):
        for attribute in instance.keyval:
            typeFound = False
            for tempAttributeType in template.keyval:
                if attribute.value == tempAttributeType.value:
                    typeFound = True
            if typeFound == False:
                msg = "The attribute '{}' in instance '{}' was not defined in the corresponding template".format(attribute.value, instance.name.value)
                self.printError(msg, instance.name.context.line, instance.name.context.column, len(attribute.name.value))
        
    # check if all attributes definied in the template are set in instance
    def templateAttributeDefinied(self, template, instance):
        for attribute in template.keyval:
            typeFound = False
            for instanceAttribute in instance.keyval:
                if attribute.value == instanceAttribute.value:
                    typeFound = True
            if typeFound == False:
                msg = "The attribute '{}' from the corresponding template was not definied in instance '{}'".format(attribute.value, instance.name.value)
                self.printError(msg, instance.context.start.line, instance.context.start.column, len(attribute.value))


    # TransportOrderStep Check

    def checkTransportOrderSteps(self, givenTree):
        tosNameCounts = {}
        for tos in givenTree.transportOrderSteps.values():
            # Check if there is more than one tos with the same name
            if tosNameCounts.get(tos.name.value) != None:
                msg = "TransportOrderStep name is already used by an other TransportOrderStep".format(tos.name.context.start.line)
                self.printError(msg, tos.name.context.start.line, tos.name.context.start.column, len(tos.name.value))
            else:
                tosNameCounts[tos.name.value] = 1

            self.checkLocation(tos)
            self.checkOnDone(tos, givenTree)
            self.checkExpressions(tos.triggeredBy) 
            self.checkExpressions(tos.finishedBy)

    def checkLocation(self, tos):
        locationName = tos.location.value
        location = self.getInstance(locationName)
        if location == None:
            msg = "The location '{}' in TransportOrderStep '{}' could not be found".format(locationName, tos.name.value)
            self.printError(msg, tos.location.context.start.line, tos.location.context.start.column, len(locationName))
        elif location.templateName.value != "Location":
            msg = "The instance '{}' in TransportOrderStep '{}' is not a Location Instance but an '{}' instance".format(locationName, tos.name.value, location.templateName.value)
            self.printError(msg, tos.location.context.start.line, tos.location.context.start.column, len(locationName))


    # Task Check

    def checkTasks(self, givenTree):
        taskNameCounts = {}
        for task in givenTree.taskInfos.values():
            # Check if there is more than one task with the same name
            if taskNameCounts.get(task.name.value) != None:
                msg = "Task name is already used by an other task".format()
                self.printError(msg, task.name.context.start.line, task.name.context.start.column, len(task.name))
            else:
                taskNameCounts[task.name.value] = 1

            self.checkTransportOrders(task, givenTree)
            self.checkOnDone(task, givenTree)
            self.checkExpressions(task.triggeredBy)
            self.checkExpressions(task.finishedBy)
            self.checkRepeat(task)

    def checkTransportOrders(self, task, givenTree):
        if len(task.transportOrders) > 1:
            msg = "Task '{}' has more than one TransportOrder".format(task.name.value)
            self.printError(msg, task.name.context.start.line, task.name.context.start.column, len(task.name.value))
        elif len(task.transportOrders) == 1:
            # From check
            if self.checkIfTransportOrderStepsPresent(givenTree, task.transportOrders[0].value.pickupFrom.value) == False:
                msg = "Task '{}' refers to an unknown TransportOrderStep in 'from': '{}' ".format(task.name.value, task.name.context.start.line, task.transportOrders[0].value.pickupFrom.value)
                self.printError(msg, task.name.context.start.line, task.name.context.start.column, len(task.transportOrders[0].value.pickupFrom.value))
            
            # To check
            if self.checkIfTransportOrderStepsPresent(givenTree, task.transportOrders[0].value.deliverTo.value) == False:
                msg = "Task '{}' refers to an unknown TransportOrderStep in TransportOrder '{}'".format(task.name.value, task.transportOrders[0].value.deliverTo.value)
                self.printError(msg, task.name.context.start.line, task.name.context.start.column, len(task.transportOrders[0].value.deliverTo.value))

    def checkIfTaskPresent(self, givenTree, taskName):
        for _tN in givenTree.taskInfos:
            if taskName == _tN.value:
                return True
        return False

    def checkIfTransportOrderStepsPresent(self, givenTree, instanceName):
        for _iN in givenTree.transportOrderSteps:
            if instanceName == _iN.value:
                return True
        return False

    def checkRepeat(self, task):
        if len(task.repeat) > 1:
            msg = "There are multiple Repeat definitions in Task '{}'".format(task.name.value)
            self.printError(msg, task.context.start.line, task.context.start.column, len(task.name.value))


    # Help Functions
    
    def checkOnDone(self, task, givenTree):
        for i in range(len(task.onDone)):
            if self.checkIfTaskPresent(givenTree, task.onDone[i].value) == False:
                msg = "Task '{}' refers to an unknown OnDone-Task '{}'".format(task.name.value, task.onDone[i].value)
                self.printError(msg, task.name.context.start.line, task.name.context.start.column, 1) 
                self.errorCount = self.errorCount + 1

    def checkExpressions(self, expressions):
        for exp in expressions:
            self.checkExpression(exp.value, exp.context)
    
    def checkExpression(self, expression, context): 
        if type(expression) == str:
            self.checkSingleExpression(expression, context)
        elif type(expression) == dict:
            if len(expression) == 2:
                self.checkUnaryOperation(expression, context)
            else:
                self.checkBinaryOperation(expression, context)

    def checkSingleExpression(self, expression, context):
        # there is only a event instance check if its type is boolean
        if self.isEventInstance(expression) == True:
            instance = self.getInstance(expression)
            if self.hasInstanceType(instance, "Boolean") == False:
                print("'" + expression + "' has no booelan type so it cant get parsed as single statement! File: {}".format(self.filePath))
                self.errorCount = self.errorCount + 1
        else:
            if self.isTimeInstance(expression) == False:
                print("The given expression in line {} is not related to a time or event instance! File: {}".format(context.start.line, self.filePath))
                self.errorCount = self.errorCount + 1

    def checkUnaryOperation(self, expression, context):
        if self.isBooleanExpression(expression["value"]) == False:
            print("'" + expression["value"] + "' in line {} is not a boolean so it cant get parsed as a single statement! File: {}".format(context.start.line, self.filePath))
            self.errorCount = self.errorCount + 1

    def checkBinaryOperation(self, expression, context):
         # check if the left side of the expression is an event instance
        left = expression["left"]
        if self.isEventInstance(left) == False:
            print("The given Instance '{}' in the binary Operation in line {} is not an instance of type event! File: {}".format(left, context.start.line, self.filePath))
            self.errorCount = self.errorCount + 1
        else:
            eventType = self.getAttributeValue(self.getInstance(left), "type")
            right = expression["right"]
            if self.isBooleanExpression(right) == False:
                print("The right side in line {} is not a boolean. File: {}".format(context.start.line, self.filePath))
                self.errorCount = self.errorCount + 1

    # Check if the given expression can be resolved to a boolean expression
    def isBooleanExpression(self, expression):
        if type(expression) == str:
            return self.isCondition(expression)
        elif type(expression) == dict:
            if len(expression) == 2:
                return self.isBooleanExpression(expression["value"])
            else:
                # an expression enclosed by parenthesis has the key binOp in the dict
                if expression["left"] == "(" and expression["right"] == ")":
                    return self.isBooleanExpression(expression["binOp"])
                else:
                    return (self.isBooleanExpression(expression["left"]) and self.isBooleanExpression(expression["right"]))

    # Check if the given expression is a condition, event instances are interpreted as booleans
    def isCondition(self, expression):
        return  (self.isEventInstance(expression) 
                or self.strIsInt(expression)
                or self.strIsFloat(expression) 
                or expression in ["True", "true", "False", "false"])

    # Get Template from given templateName
    def getTemplate(self, templates, templateName):
        for temp in self.templates.values():
            if templateName == temp.name.value:
                return temp
        return None

    # Get Instance from given instanceName
    def getInstance(self, instanceName):
        for instance in self.givenTree.instances.values():
            if instanceName == instance.name.value:
                return instance
        return None

    # Returns false if its not a time instance or an instance at all
    def isTimeInstance(self, instanceName):
        instance = self.getInstance(instanceName)
        if instance != None and instance.templateName.value == "Time": 
            return True
        return False

    # Returns false if its not a Event instance or an instance at all
    def isEventInstance(self, instanceName):
        instance = self.getInstance(instanceName)
        if instance != None and instance.templateName.value == "Event":
            return True
        return False

    def hasInstanceType(self, instance, typeName):
        for keyval in instance.keyval.values():
            if keyval.value == '"' + typeName + '"':
                return True
        return False

    def getAttributeValue(self, instance, attributeName):
        for key in instance.keyval:
                if key.value == attributeName:
                    return instance.keyval[key].value
        return None
        
    def strIsInt(self, str):
        try:
            int(str)
            return True
        except ValueError:
            return False

    def strIsFloat(self, str):
        try:
            float(str)
            return True
        except ValueError:
            return False

    def printError(self, msg, line, column, offSymbolLength):
        if self.usedInExtension == True:
            print(msg)
            print(line)
            print(column)
            print(offSymbolLength)
        else:
            print(msg)
            print("File '" + self.filePath + "', line " + str(line) + ":" + str(column))
        self.errorCount = self.errorCount + 1