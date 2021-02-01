""" Contains Instance class """

class Instance(object):
    '''
        Represents an Instance and all its data
    '''
    def __init__(self):
        self.name = None
        self.template_name = None
        self.keyval = {}  # Dictionary of attributes with set value
        self.context = None
        self.context_dict = {}

    def __repr__(self):
        return "Template: {} \n Attributes: {} \n".format(self.template_name, self.keyval)
