from CreateTreeTaskParserVisitor import CompleteProgram
from CreateTreeTaskParserVisitor import Instance
from CreateTreeTaskParserVisitor import TaskInfo
from CreateTreeTaskParserVisitor import Template
from CreateTreeTaskParserVisitor import TransportOrder

import copy



def isValid(givenTree):
    _tree = copy.deepcopy(givenTree)
    # try and catch this for the Value False
    return _validate(_tree, [])


def _validate(givenTree, retreivedInfo):

    for instanceName, instance in givenTree.instances.iteritems():  
        # Check if template is defined
        if instance.templateName not in givenTree.templates:
            raise Exception("Template {} is not defined in TaskLanguage".format(instance.templateName))
        
        # Check if Attrs are set.
        # NOTE Instance can set more like specified in template here
        t = givenTree.templates[instance.templateName]
        for i in t.keyval:
            if i not in instance.keyval:
                raise Exception("Instace: {} does not set the Attribute: {}".format(instance.templateName, i))


    for taskName, task in givenTree.taskInfos.iteritems():
        # Check OnDone
        for i in range(len(task.onDone)):
            if _checkIfTaskPresent(givenTree, task.onDone[i]) is False:
                raise Exception("Task: {} refers to an unknown OnDone-Task: {}".format(task.name, task.onDone[i]))

        # Check TransportOrders
        for i in range(len(task.transportOrders)):
            # Fromm check
            for j in range(len(task.transportOrders[i].fromm)):
                print task.transportOrders[i].fromm[j]
                if _checkIfInstancePresent(givenTree, task.transportOrders[i].fromm[j]) is False:
                    raise Exception("Task: {} refers to an unknown Instance in TransportOrder: {}".format(task.name, task.transportOrders[i].fromm[j]))
            
            # To check
            if _checkIfInstancePresent(givenTree, task.transportOrders[i].to) is False:
                    raise Exception("Task: {} refers to an unknown Instance in TransportOrder: {}".format(task.name, task.transportOrders[i].to))


        # TODO Trigger Semantic-Checking
 
    return True




def _checkIfTaskPresent(givenTree, taskName):
    for _tN, _t in givenTree.taskInfos.iteritems():
        if taskName == _tN:
            return True
    return False

def _checkIfInstancePresent(givenTree, instanceName):
    for _iN, _t in givenTree.instances.iteritems():
        if instanceName == _iN:
            return True
    return False