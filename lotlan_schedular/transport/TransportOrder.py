class TransportOrder(object):
    '''
        Represents a TransportOrder and all its data
    '''

    def __init__(self):
        self.tos_from = None
        self.tos_to = None
        self.pickup_from = ""
        self.deliver_to = ""
        self.from_parameters = []
        self.to_parameters = []

    def __repr__(self):
        return (("\t PickupFrom: {} \n\t Parameters: {} \n\t DelieverTo: {} \n\t Parameters: {}")
                .format(self.pickup_from, self.from_parameters, self.deliver_to, self.to_parameters))
