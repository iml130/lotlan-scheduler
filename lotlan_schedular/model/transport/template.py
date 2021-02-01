""" Contains Template class """

class Template(object):
    '''
        Represents a Template and all its data
    '''

    def __init__(self):
        self.name = None
        self.keyval = []
        self.context = None

    def __repr__(self):
        return "{}".format(self.keyval)
