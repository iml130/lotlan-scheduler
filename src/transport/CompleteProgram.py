__author__ = "Maximilian Hörstrup"
__version__ = "0.0.1"
__maintainer__ = "Maximilian Hörstrup"

class CompleteProgram(object):
    def __init__(self):
        self.templates = {} # All defined templates
        self.instances = {} # All defined instances
        self.transportOrderSteps = {} # All defined TaskOrderSteps
        self.taskInfos = {} # All defined tasks

    def __repr__(self):
        return (("Templates: {} \n Instances: {} \n TransportOrderSteps: {} \n TaskInfos: {}")
                .format(self.templates, self.instances, self.transportOrderSteps, self.taskInfos))

# Each class holds ContextObjects which contain  the value(e.g. the name as string) and the context from antlr
class ContextObject(object):
    def __init__(self, value, context):
        self.value = value
        self.context = context

    def __repr__(self):
        return self.value.__repr__()