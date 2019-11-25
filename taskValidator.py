from CreateTreeTaskParserVisitor import CompleteProgram
from CreateTreeTaskParserVisitor import Instance
from CreateTreeTaskParserVisitor import TaskInfo
from CreateTreeTaskParserVisitor import Template
from CreateTreeTaskParserVisitor import TransportOrder

import copy


def isValid(givenTree):
    # try and catch this for the Value False
    return _validate(givenTree, [])


def _validate(givenTree, retreivedInfo):

    for instance in givenTree.instances.values():
        # Check if template is defined
        if instance.templateName not in givenTree.templates:
            raise Exception("Template {} is not defined in TaskLanguage".format(instance.templateName))
        
        # Check if Attrs are set.
        # NOTE Instance can set more like specified in template here
        t = givenTree.templates[instance.templateName]
        for i in t.keyval:
            if i not in instance.keyval:
                raise Exception("Instace: {} does not set the Attribute: {}".format(instance.templateName, i))


    for task in givenTree.taskInfos.values():
        # Check OnDone
        for i in range(len(task.onDone)):
            if _checkIfTaskPresent(givenTree, task.onDone[i]) is False:
                raise Exception("Task: {} refers to an unknown OnDone-Task: {}".format(task.name, task.onDone[i]))

        # Check TransportOrders
        for i in range(len(task.transportOrders)):
            # Fromm check
            if _checkIfTransportOrderStepsPresent(givenTree, task.transportOrders[i].fromm) is False:
                raise Exception("Task: {} refers to an unknown TransportOrderStep in TransportOrder: {}".format(task.name, task.transportOrders[i].fromm))
            
            # To check
            if _checkIfTransportOrderStepsPresent(givenTree, task.transportOrders[i].to) is False:
                    raise Exception("Task: {} refers to an unknown TransportOrderStep in TransportOrder: {}".format(task.name, task.transportOrders[i].to))


        # TODO Trigger Semantic-Checking
 
    return True




def _checkIfTaskPresent(givenTree, taskName):
    for _tN in givenTree.taskInfos:
        if taskName == _tN:
            return True
    return False

def _checkIfTransportOrderStepsPresent(givenTree, instanceName):
    for _iN in givenTree.transportOrderSteps:
        if instanceName == _iN:
            return True
    return False