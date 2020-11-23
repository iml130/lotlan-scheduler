from lotlan_schedular.api.transportorder_step import TransportOrderStep


class TransportOrder:
    def __init__(self):
        self.uuid = ""
        self.to_step_from = TransportOrderStep()
        self.to_step_to = TransportOrderStep()
        self.from_parameters = []
        self.to_parameters = []
        self.task_name = ""

    def __str__(self):
        return (("\n UUID: {}\n To_Step_From: \t\t {} \n To_Step_To: \t\t {} \n\t")
                .format(self.uuid, self.to_step_from, self.to_step_to))

    def __repr__(self):
        return (("\n UUID: {}\n To_Step_From: \t\t {} \n To_Step_To: \t\t {} \n\t")
                .format(self.uuid, self.to_step_from, self.to_step_to))
