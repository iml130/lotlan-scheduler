from CreateTreeTaskParserVisitor import CompleteProgram
from CreateTreeTaskParserVisitor import Instance
from CreateTreeTaskParserVisitor import TaskInfo
from CreateTreeTaskParserVisitor import Template
from CreateTreeTaskParserVisitor import TransportOrder

import copy

class SemanticValidator:
    def __init__(self, logPath, filePath, templates):
        self.logPath = logPath
        self.filePath = filePath
        self.templates = templates
        self.givenTree = None
        self.errorCount = 0

    def isValid(self, givenTree):
        self.givenTree = givenTree
        return (self.checkTemplates(givenTree) 
                and self.checkInstances(givenTree) 
                and self.checkTransportOrderSteps(givenTree)
                and self.checkTasks(givenTree))

    def checkTemplates(self, givenTree):
        templateNameCounts = {}
        for template in givenTree.templates.values():
            # check if there is more than one template with the same name
            if templateNameCounts.get(template.name.value) != None:
                print("The Template name '{}' at line {} is already used by an other template! File: {}".format(template.name.value, template.name.context.start.line, self.filePath))
                return False
            else:
                templateNameCounts[template.name.value] = 1
        return True

    def checkInstances(self, givenTree):
        instanceNameCounts = {}
        for instance in givenTree.instances.values():
            # check if there is more than one instance with the same name
            if instanceNameCounts.get(instance.name.value) != None:
                print("The Instance name '{}' at line {} is already used by an other instance! File: {}".format(instance.name.value, instance.name.context.start.line, self.filePath))
                return False
            else:
                instanceNameCounts[instance.name.value] = 1

            templateName = instance.templateName.value
            template = self.getTemplate(givenTree, templateName)

            # check if the corresponding template exists
            if template == None:
                print("The Instance '{}' at line {} refers to a template that does not exist! File: {}".format(instance.name.value, instance.name.context.start.line, self.filePath))
                return False
            # check if the instance variables match with the corresponding template
            else:
                if self.templateAttributeExists(template, instance) == False or self.templateAttributeDefinied(template, instance) == False:
                    print("template and instance dont match")
                    return False
        return True

    # check if all attributes in the given instance are definied in the template
    def templateAttributeExists(self, template, instance):
        for attribute in instance.keyval:
            typeFound = False
            for tempAttributeType in template.keyval:
                if attribute.value == tempAttributeType.value:
                    typeFound = True
            if typeFound == False:
                print("The attribute '{}' in instance '{}' was not defined in the corresponding template!".format(attribute.value, instance.name.value) + " File: " + self.filePath)
        
    # check if all attributes definied in the template are set in instance
    def templateAttributeDefinied(self, template, instance):
        for attribute in template.keyval:
            typeFound = False
            for instanceAttribute in instance.keyval:
                if attribute.value == instanceAttribute.value:
                    typeFound = True
            if typeFound == False:
                print("The attribute '{}' from the corresponding template was not definied in instance '{}' in line {} !".format(attribute.value, instance.name.value, instance.context.start.line) + " File: " + self.filePath)
        return True

    def checkTransportOrderSteps(self, givenTree):
        tosNameCounts = {}
        for tos in givenTree.transportOrderSteps.values():
            # Check if there is more than one tos with the same name
            if tosNameCounts.get(tos.name.value) != None:
                print("TransportOrderStep name at line {} is already used by an other TransportOrderStep!".format(tos.name.context.start.line) + " File: " + self.filePath)
                return False
            else:
                tosNameCounts[tos.name.value] = 1

            # Check if instance exists and if its a location
            locationName = tos.location.value
            location = self.getInstance(locationName)
            if location == None:
                print("The location '{}' in TransportOrderStep '{}' could not be found!".format(locationName, tos.name.value) + " File: " + self.filePath)
                return False
            else:
                if location.templateName.value != "Location":
                    print("The instance '{}' in TransportOrderStep '{}' is not a Location Instance but an '{}' instance!".format(locationName, tos.name.value, location.templateName.value) + " File: " + self.filePath)
                    return False

            # Check OnDone
            if self.checkOnDone(tos, givenTree) == False:
                return False
            # Check TriggeredBy
            if self.checkExpressions(tos.triggeredBy) == False: 
                return False
            # Check FinishedBy
            if self.checkExpressions(tos.finishedBy) == False:
                return False
        return True

    def checkTasks(self, givenTree):
        taskNameCounts = {}
        for task in givenTree.taskInfos.values():
            # Check if there is more than one task with the same name
            if taskNameCounts.get(task.name.value) != None:
                print("Task name at line {} is already used by an other task!".format(task.name.context.start.line) + " File: " + self.filePath)
                return False
            else:
                taskNameCounts[task.name.value] = 1

            # Check TransportOrders
            if self.checkTransportOrders(task, givenTree) == False: 
                return False
            # Check OnDone
            if self.checkOnDone(task, givenTree) == False:
                return False
            # Check TriggeredBy
            if self.checkExpressions(task.triggeredBy) == False: 
                return False
            # Check FinishedBy
            if self.checkExpressions(task.finishedBy) == False:
                return False
            # Check Repeat
            if self.checkRepeat(task) == False:
                return False
        return True

    def checkTransportOrders(self, task, givenTree):
        # TODO: Check if TransportOrderStep is used more than once in the task
        for i in range(len(task.transportOrders)):
            # From check
            if self.checkIfTransportOrderStepsPresent(givenTree, task.transportOrders[i].value.pickupFrom.value) == False:
                print("Task '{}' in line {} refers to an unknown TransportOrderStep in TransportOrder '{}'"
                    .format(task.name.value, task.name.context.start.line, task.transportOrders[i].value.pickupFrom.value) + " File: " + self.filePath)
                return False
            
            # To check
            if self.checkIfTransportOrderStepsPresent(givenTree, task.transportOrders[i].value.deliverTo.value) == False:
                print("Task '{}' refers to an unknown TransportOrderStep in TransportOrder '{}'".format(task.name.value, task.transportOrders[i].value.deliverTo.value) + " File: " + self.filePath)
                return False

    def checkOnDone(self, task, givenTree):
        for i in range(len(task.onDone)):
            if self.checkIfTaskPresent(givenTree, task.onDone[i].value) == False:
                print("Task '{}' in line {} refers to an unknown OnDone-Task '{}'".format(task.name.value, task.name.context.start.line, task.onDone[i].value) + " File: " + self.filePath)
                return False

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

    def checkExpressions(self, expressions):
        for exp in expressions:
            self.checkExpression(exp.value, exp.context)
        return True
    
    def checkRepeat(self, task):
        if len(task.repeat) > 1:
            print("There are multiple Repeat definitions in Task '{}' in line {}. File: {}".format(task.name.value, task.context.start.line, self.filePath))
            return False
        return True

    def checkExpression(self, expression, context): 
        if type(expression) == str:
            self.checkSingleExpression(expression)
        elif type(expression) == dict:
            if len(expression) == 2:
                self.checkUnaryOperation(expression)
            else:
                self.checkBinaryOperation(expression, context)

    def checkSingleExpression(self, expression):
        if self.isTimeInstance(expression) == True:
            return True
        # there is only a event instance check if its type is boolean
        elif self.isEventInstance(expression) == True:
            instance = self.getInstance(expression)
            if self.hasInstanceType(instance, "Boolean") == False:
                print("'" + expression + "' has no booelan type so it cant get parsed as single statement!File: {}".format(self.filePath))
        else:
            print("The given expression is not related to a time or event instance!" + " File: " + self.filePath)

    def checkUnaryOperation(self, expression):
        if self.isEventInstance(expression) == True:
            instance = self.getInstance(expression)
            if self.hasInstanceType(instance, "Boolean") == False:
                print(expression + " has no booelan type so it cant get parsed as single statement!" + " File: " + self.filePath)
        return self.isBooleanExpression(expression["value"])

    def checkBinaryOperation(self, expression, context):
         # check if the left side of the expression is an event instance
        left = expression["left"]
        if self.isEventInstance(left) == False:
            print("The given Instance {} in the binary Operation is not an instance of type event!".format(left) + " File: " + self.filePath)
        else:
            eventType = self.getAttributeValue(self.getInstance(left), "type")
            right = expression["right"]
            if self.isBooleanExpression(right) == False:
                print(expression)
                print(right)
                print("Right side is not a boolean in line {}".format(context.start.line))

    # Check if the given expression can be resolved to a boolean expression
    def isBooleanExpression(self, expression):
        if type(expression) == str:
            return self.isCondition(expression)
        elif type(expression) == dict:
            if len(expression) == 2:
                return self.isBooleanExpression(expression["value"])
            else:
                if expression["left"] == "(" and expression["right"] == ")":
                    return self.isBooleanExpression(expression["binOp"])
                else:
                    return (self.isBooleanExpression(expression["left"]) and self.isBooleanExpression(expression["right"]))

    def isCondition(self, expression):
        return  (self.isEventInstance(expression) 
                or self.strIsInt(expression)
                or self.strIsFloat(expression) 
                or expression in ["True", "true", "False", "false"])

    # Help Functions

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

    # Returns false if its not a time instance or an instance at all
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