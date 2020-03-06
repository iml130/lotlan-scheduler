__author__ = "Maximilian Hörstrup"
__version__ = "0.0.1"
__maintainer__ = "Maximilian Hörstrup"

class Instance(object):
    def __init__(self):
        self.name = None # String of the Instances Name
        self.templateName = None # String of the Instances origin Template
        self.keyval = {} # Dictionary of attributes with set value
        self.context = None

    def __repr__(self):
        return "Template: {} \n Attributes: {} \n".format(self.templateName, self.keyval)