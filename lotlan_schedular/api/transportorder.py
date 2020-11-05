from lotlan_schedular.api.transportorder_step import TransportOrderStep


class TransportOrder:
    def __init__(self, uuid, to_step_from, to_step_to, task_name):
        self.uuid = uuid
        self.to_step_from = to_step_from
        self.to_step_to = to_step_to
        self.task_name = task_name

    @classmethod
    def create_to(cls, uuid, task, events, locations):
        to = task.transport_order

        to_step_from = TransportOrderStep.create_tos(to.tos_from, events, locations)
        to_step_to = TransportOrderStep.create_tos(to.tos_to, events, locations)

        return TransportOrder(uuid, to_step_from, to_step_to, task.name)

    def __str__(self):
        return (("\n UUID: {}\n To_Step_From: \t\t {} \n To_Step_To: \t\t {} \n\t")
                .format(self.uuid, self.to_step_from, self.to_step_to))

    def __repr__(self):
        return (("\n UUID: {}\n To_Step_From: \t\t {} \n To_Step_To: \t\t {} \n\t")
                .format(self.uuid, self.to_step_from, self.to_step_to))
