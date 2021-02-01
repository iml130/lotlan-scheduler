""" Contains Transport class """

class Transport(object):
    '''
        Holds information about everything defined in a LoTLan file
    '''
    def __init__(self):
        self.templates = {}
        self.instances = {}
        self.transport_order_steps = {}
        self.tasks = {}

    def __repr__(self):
        return (("Templates: {} \n Instances: {} \n TransportOrderSteps: {} \n TaskInfos: {}")
                .format(self.templates, self.instances, self.transport_order_steps, self.tasks))
