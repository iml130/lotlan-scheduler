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
                print("Template name at line {} is already used by an other template!".format(template.name.context.start.line) + " File: " + self.filePath)
                return False
            else:
                templateNameCounts[template.name.value] = 1
        return True

    def checkInstances(self, givenTree):
        instanceNameCounts = {}
        for instance in givenTree.instances.values():

            # check if there is more than one instance with the same name
            if instanceNameCounts.get(instance.name.value) != None:
                print("Instance name at line {} is already used by an other instance!".format(instance.name.context.start.line) + " File: " + self.filePath)
                return False
            else:
                instanceNameCounts[instance.name.value] = 1

            templateName = instance.templateName.value
            template = self.getTemplate(givenTree, templateName)

            # check if corresponding template exists
            if template == None:
                print("The instance '{}' at line {} refers to a template that does not exists!".format(instance.name.value, instance.name.context.start.line) + " File: " + self.filePath)
                return False
            # check if the instance variables match with the corresponding template
            else:
                for variable in instance.keyval:
                    variableType = variable.value
                    typeFound = False
                    for tempVariableType in template.keyval:
                        if variableType == tempVariableType.value:
                            typeFound = True
                    if typeFound == False:
                        print("The attribute type {} in line {} was not defined in the corresponding template!".format(variableType, variable.context.start.line) + " File: " + self.filePath)
                        return False
        return True

    def getTemplate(self, templates, templateName):
        for temp in self.templates.values():
            if templateName == temp.name.value:
                return temp
        return None

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
            if self.checkTriggeredBy(tos.triggeredBy) == False: 
                return False
            # Check FinishedBy
            if self.checkFinishedBy(tos.finishedBy) == False:
                return False
        return True

    def getInstance(self, instanceName):
        for instance in self.givenTree.instances.values():
            if instanceName == instance.name.value:
                return instance
        return None

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
            if self.checkTriggeredBy(task.triggeredBy) == False: 
                return False
            # Check FinishedBy
            if self.checkFinishedBy(task.triggeredBy) == False:
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
                print("Task: {} in line {} refers to an unknown TransportOrderStep in TransportOrder: {}"
                    .format(task.name.value, task.name.context.start.line, task.transportOrders[i].value.pickupFrom.value) + " File: " + self.filePath)
                return False
            
            # To check
            if self.checkIfTransportOrderStepsPresent(givenTree, task.transportOrders[i].value.deliverTo.value) == False:
                print("Task: {} refers to an unknown TransportOrderStep in TransportOrder: {}".format(task.name.value, task.transportOrders[i].value.deliverTo.value) + " File: " + self.filePath)
                return False

    def checkOnDone(self, task, givenTree):
        for i in range(len(task.onDone)):
            if self.checkIfTaskPresent(givenTree, task.onDone[i].value) == False:
                print("Task: {} on line {} refers to an unknown OnDone-Task: {}".format(task.name.value, task.name.context.start.line, task.onDone[i].value) + " File: " + self.filePath)
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

    # TODO
    def checkTriggeredBy(self, expressions):
        for exp in expressions:
            self.checkExpression(exp.value, True)
        return True

    def checkExpression(self, expression, firstCall):
        if type(expression) == str:
            # instance name
            if expression[0].islower():
                # its the only element so check if its a time instance
                if firstCall == True:
                    if self.isTimeInstance(expression) == True:
                        print("There is only a time instance, thats correct")
                    # there is only a event instance check if its type is boolean
                    else:
                        instance = self.getInstance(expression)
                        if instance == None:
                            print(expression + " doesnt exists!")
                        else:
                            if self.hasInstanceType(instance, "boolean") == False:
                                print(expression + " has no booelan type so it cant get parsed as single statement!")
                            else:
                                print("Single event as boolean is correct!")
                else:
                    pass # TODO
            else:
                pass # TODO
        elif type(expression) == dict:
            if len(expression) == 2:
                print("unop")
            else:
                print("binOp")

    # Returns false if its not a time instance or an instance at all
    def isTimeInstance(self, instanceName):
        instance = self.getInstance(instanceName)
        if instance != None and instance.templateName.value == "Time": 
            return True
        return False

    def hasInstanceType(self, instance, typeName):
        for keyval in instance.keyval.values():
            if keyval.value == '"' + typeName + '"':
                return True
        return False

    def checkFinishedBy(self, expression):
        return True

    def checkRepeat(self, task):
        # TODO: Check if Repeat is used more than once in the task
        return True