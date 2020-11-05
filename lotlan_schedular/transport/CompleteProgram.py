class CompleteProgram(object):
    '''
        Holds information about all building blocks of the TaskLanguage
    '''
    def __init__(self):
        self.templates = {}
        self.instances = {}
        self.transport_order_steps = {}
        self.tasks = {}

    def __repr__(self):
        return (("Templates: {} \n Instances: {} \n TransportOrderSteps: {} \n TaskInfos: {}")
                .format(self.templates, self.instances, self.transport_order_steps, self.tasks))
