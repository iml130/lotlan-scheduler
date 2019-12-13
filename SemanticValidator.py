from CreateTreeTaskParserVisitor import CompleteProgram
from CreateTreeTaskParserVisitor import Instance
from CreateTreeTaskParserVisitor import TaskInfo
from CreateTreeTaskParserVisitor import Template
from CreateTreeTaskParserVisitor import TransportOrder

import copy

class SemanticValidator:
    def __init__(self, logPath):
        self.logPath = logPath
    
    def isValid(self, givenTree):
        # try and catch this for the Value False
        return self.validate(givenTree, [])


    def validate(self, givenTree, retreivedInfo):

        for instance in givenTree.instances.values():
            # Check if template is defined
            if instance.templateName not in givenTree.templates:
                print("Template {} is not defined in TaskLanguage".format(instance.templateName), file=open(self.logPath, 'a'))
                return False

            # Check if Attrs are set.
            # NOTE Instance can set more like specified in template here
            t = givenTree.templates[instance.templateName]
            for i in t.keyval:
                if i not in instance.keyval:
                    print("Instance: {} does not set the Attribute: {}".format(instance.templateName, i), file=open(self.logPath, 'a'))
                    return False


        for task in givenTree.taskInfos.values():
            # Check OnDone
            for i in range(len(task.onDone)):
                if self.checkIfTaskPresent(givenTree, task.onDone[i]) is False:
                    print("Task: {} refers to an unknown OnDone-Task: {}".format(task.name, task.onDone[i]), file=open(self.logPath, 'a'))
                    return False

            # Check TransportOrders
            for i in range(len(task.transportOrders)):
                # Fromm check
                if self.checkIfTransportOrderStepsPresent(givenTree, task.transportOrders[i].pickupFrom) is False:
                    print("Task: {} refers to an unknown TransportOrderStep in TransportOrder: {}".format(task.name, task.transportOrders[i].pickupFrom), file=open(self.logPath, 'a'))
                    return False
                
                # To check
                if self.checkIfTransportOrderStepsPresent(givenTree, task.transportOrders[i].deliverTo) is False:
                    print("Task: {} refers to an unknown TransportOrderStep in TransportOrder: {}".format(task.name, task.transportOrders[i].deliverTo), file=open(self.logPath, 'a'))
                    return False
        return True

    def checkIfTaskPresent(self, givenTree, taskName):
        for _tN in givenTree.taskInfos:
            if taskName == _tN:
                return True
        return False

    def checkIfTransportOrderStepsPresent(self, givenTree, instanceName):
        for _iN in givenTree.transportOrderSteps:
            if instanceName == _iN:
                return True
        return False