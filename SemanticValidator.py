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
        return (self.checkTemplates(givenTree) 
                and self.checkInstances(givenTree) 
                and self.checkTransportOrderSteps(givenTree)
                and self.checkTasks(givenTree))

    def checkTemplates(self, givenTree):
        return True

    def checkInstances(self, givenTree):
        instanceNameCounts = {}
        for instance in givenTree.instances.values():
            if instanceNameCounts.get(instance.name.value) != None:
                print("Instance name at line {} is already definied!".format(instance.name.context.start.line))
            else:
                instanceNameCounts[instance.name.value] = 1

        return True

    def checkTransportOrderSteps(self, givenTree):
        return True

    def checkTasks(self, givenTree):
        for task in givenTree.taskInfos.values():
            # Check OnDone
            for i in range(len(task.onDone)):
                if self.checkIfTaskPresent(givenTree, task.onDone[i].value) is False:
                    print("Task: {} on line {} refers to an unknown OnDone-Task: {}".format(task.name.value, task.name.context.start.line, task.onDone[i].value), file=open(self.logPath, 'a'))
                    return False
                    
            # TODO: Check TriggeredBy
            # TODO: Check FinishedBy
            # TODO: Check Repeat

            # Check TransportOrders
            for i in range(len(task.transportOrders)):
                # From check
                if self.checkIfTransportOrderStepsPresent(givenTree, task.transportOrders[i].value.pickupFrom.value) is False:
                    print("Task: {} refers to an unknown TransportOrderStep in TransportOrder: {}".format(task.name.value, task.transportOrders[i].value.pickupFrom.value), file=open(self.logPath, 'a'))
                    return False
                
                # To check
                if self.checkIfTransportOrderStepsPresent(givenTree, task.transportOrders[i].value.deliverTo.value) is False:
                    print("Task: {} refers to an unknown TransportOrderStep in TransportOrder: {}".format(task.name.value, task.transportOrders[i].value.deliverTo.value), file=open(self.logPath, 'a'))
                    return False
        return True

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