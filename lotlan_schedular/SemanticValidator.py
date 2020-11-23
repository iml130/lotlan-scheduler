# globals defines
from lotlan_schedular.defines import TRIGGERED_BY_KEY, FINISHED_BY_KEY, ON_DONE_KEY, LOCATION_KEY


class SemanticValidator:
    '''
        Executes static semantic checks for given lotlan tree
    '''

    def __init__(self, file_path, tree, templates, used_in_extension, error_listener):
        self.file_path = file_path
        self.templates = templates
        self.tree = tree
        self.used_in_extension = used_in_extension
        self.error_listener = error_listener

    def validate(self):
        self.check_instances()
        self.check_transport_order_steps()
        self.check_tasks()

    # Instance Check
    def check_instances(self):
        for instance in self.tree.instances.values():
            template_name = instance.template_name
            template = self.get_template(self.tree, template_name)

            # check if the corresponding template exists
            if template is None:
                msg = "The Instance '{}' refers to a template that does not exist".format(instance.name)
                context_start = instance.context.start
                self.error_listener.print_error(msg, context_start.line, context_start.column,
                                                len(instance.name), False)
            # check if the instance variables match with the corresponding template
            else:
                self.check_if_template_attribute_exists(template, instance)
                self.check_if_template_attribute_definied(template, instance)

    # check if all attributes in the given instance are definied in the template
    def check_if_template_attribute_exists(self, template, instance):
        for instance_attribute in instance.keyval:
            attribute_found = False
            for template_attribute in template.keyval:
                if instance_attribute == template_attribute:
                    attribute_found = True
            if attribute_found is False:
                msg = "The attribute '{}' in instance '{}' was not defined in the corresponding template".format(
                    instance_attribute, instance.name)

                variable_context = instance.context_dict[instance_attribute]
                self.error_listener.print_error(msg, variable_context.start.line, variable_context.start.column,
                                                len(instance_attribute), False)

    # check if all attributes definied in the template are set in instance
    def check_if_template_attribute_definied(self, template, instance):
        for template_attribute in template.keyval:
            attribute_found = False
            for instance_attribute in instance.keyval:
                if template_attribute == instance_attribute:
                    attribute_found = True
            if attribute_found is False:
                msg = "The attribute '{}' from the corresponding template was not definied in instance '{}'".format(
                    template_attribute, instance.name)
                self.error_listener.print_error(msg, instance.context.start.line, instance.context.start.column,
                                                len(template_attribute), False)

    # TransportOrderStep Check
    def check_transport_order_steps(self):
        for tos in self.tree.transport_order_steps.values():
            context_dict = tos.context_dict

            self.check_locations(tos)
            self.check_on_done(tos)

            if TRIGGERED_BY_KEY in context_dict:
                self.check_expression(tos.triggered_by_statements, context_dict[TRIGGERED_BY_KEY])
            if FINISHED_BY_KEY in context_dict:
                self.check_expression(tos.finished_by_statements, context_dict[FINISHED_BY_KEY])

    def check_locations(self, tos):
        context_dict = tos.context_dict

        if LOCATION_KEY in context_dict:
            location = tos.location
            locationInstance = self.get_instance(location.logical_name)
            location_context = context_dict[LOCATION_KEY]

            if locationInstance is None:
                msg = "The location instance '{}' in TransportOrderStep '{}' could not be found".format(
                       location.logical_name, tos.name)
                self.error_listener.print_error(msg, location_context.start.line, location_context.start.column,
                                                len(location.logical_name), False)
            elif locationInstance.template_name != "Location":
                msg = ("The instance '{}' in TransportOrderStep '{}' is"
                       "not a 'Location' instance but a '{}' instance").format(
                        location.logical_name, tos.name, locationInstance.template_name)
                self.error_listener.print_error(msg, location_context.start.line, location_context.start.column,
                                                len(location.logical_name), False)

    # Task Check
    def check_tasks(self):
        for task in self.tree.tasks.values():
            context_dict = task.context_dict

            self.check_transport_orders(task)
            self.check_repeat_or_on_done(task)
            self.check_on_done(task)
            if TRIGGERED_BY_KEY in task.context_dict:
                self.check_expression(task.triggered_by, context_dict[TRIGGERED_BY_KEY])
            if FINISHED_BY_KEY in task.context_dict:
                self.check_expression(task.finished_by, context_dict[FINISHED_BY_KEY])

    def check_transport_orders(self, task):
        if task.transport_order is not None:
            # From check
            if self.check_if_tos_is_present(task.transport_order.to_step_from.name) is False:
                msg = "Task '{}' refers to an unknown TransportOrderStep in 'from': '{}' ".format(
                    task.name, task.transport_order.to_step_from.name)
                self.error_listener.print_error(msg, task.context.start.line, task.context.start.column,
                                                len(task.transport_order.to_step_from.name), False)
            else:
                tos = self.get_transport_order_step(task.transport_order.to_step_from.name)
                if len(task.transport_order.from_parameters) != len(tos.parameters):
                    msg = "From has not the same amount of parameters as the transport order step!"
                    self.error_listener.print_error(msg, task.context.start.line, task.context.start.column,
                                                    len(task.transport_order.to_step_from.name), False)

            # To check
            if self.check_if_tos_is_present(task.transport_order.to_step_to.name) is False:
                msg = "Task '{}' refers to an unknown TransportOrderStep in 'to' '{}'".format(
                    task.name, task.transport_order.to_step_to.name)
                self.error_listener.print_error(msg, task.context.start.line, task.context.start.column,
                                                len(task.transport_order.to_step_to.name), False)
            else:
                tos = self.get_transport_order_step(task.transport_order.to_step_to.name)
                if len(task.transport_order.to_parameters) != len(tos.parameters):
                    msg = "To has not the same amount of parameters as the transport order step!"
                    self.error_listener.print_error(msg, task.context.start.line, task.context.start.column,
                                                    len(task.transport_order.to_step_from.name), False)

    def check_on_done(self, task_or_tos):
        context_dict = task_or_tos.context_dict
        for onDoneTask in task_or_tos.on_done:
            if self.check_if_task_is_present(onDoneTask) is False:
                msg = "The task name '{}' in the OnDone statement refers to an unknown Task".format(onDoneTask)
                self.error_listener.print_error(msg, context_dict[ON_DONE_KEY].start.line,
                                                context_dict[ON_DONE_KEY].start.column, len(onDoneTask), False)

    def check_repeat_or_on_done(self, task):
        if task.repeat and task.on_done:
            msg = ("The task '{}' has both OnDone and Repeat statements."
                   "It is only allowed to have either of them").format(task.name)
            self.error_listener.print_error(msg, task.context.start.line, task.context.start.column,
                                            len(task.name), False)

    def check_expressions(self, expressions, task_or_tos):
        if len(expressions) > 1:
            msg = "There is more than one TriggeredBy or FinishedBy Statement in '{}'".format(task_or_tos.name)
            self.error_listener.print_error(msg, task_or_tos.context.start.line, task_or_tos.context.start.column,
                                            len(task_or_tos.name), False)
        elif len(expressions) == 1:
            self.check_expression(expressions[0].value, expressions[0].context)

    def check_expression(self, expression, context):
        if type(expression) == str:
            self.check_single_expression(expression, context)
        elif type(expression) == dict:
            if len(expression) == 2:
                self.check_unary_operation(expression, context)
            else:
                self.check_binary_operation(expression, context)

    def check_single_expression(self, expression, context):
        if self.is_template_instance(expression, "Event") is True:
            instance = self.get_instance(expression)
            if self.has_instance_type(instance, "Boolean") is False:
                msg = "'" + expression + "' has no booelan type so it cant get parsed as single statement"
                self.error_listener.print_error(msg, context.start.line, context.start.column, 1, False)
        elif self.is_template_instance(expression, "Time") is False:
            msg = "The given expression is not related to a time or event instance"
            self.error_listener.print_error(msg, context.start.line, context.start.column, 1, False)

    def check_unary_operation(self, expression, context):
        if self.is_boolean_expression(expression["value"]) is False:
            msg = "The given expression couldnt be resolved to a boolean so it cant get parsed as a single statement"
            self.error_listener.print_error(msg, context.start.line, context.start.column,
                                            len(expression["value"]), False)

    def check_binary_operation(self, expression, context):
        # check if the left side of the expression is an event instance
        left = expression["left"]
        right = expression["right"]

        if expression["binOp"] == ".":
            if self.check_if_task_is_present(expression["left"]) is False:
                msg = "The task given in the expression is not defined"
                self.error_listener.print_error(msg, context.start.line,
                                                context.start.column, len(expression["left"]), False)
        else:
            if self.is_boolean_expression(right) is False:
                msg = "The right side is not a boolean expression "
                self.error_listener.print_error(msg, context.start.line, context.start.column, len(right), False)
            if self.is_boolean_expression(left) is False:
                msg = "The left side is not a boolean expression"
                self.error_listener.print_error(msg, context.start.line, context.start.column, len(left), False)

    # Check if the given expression can be resolved to a boolean expression
    def is_boolean_expression(self, expression):
        if type(expression) == str:
            return self.is_condition(expression)
        elif type(expression) == dict:
            if len(expression) == 2:
                return self.is_boolean_expression(expression["value"])
            else:
                # an expression enclosed by parenthesis has the key binOp in the dict
                if expression["left"] == "(" and expression["right"] == ")":
                    return self.is_boolean_expression(expression["binOp"])
                else:
                    return (self.is_boolean_expression(expression["left"]) and
                            self.is_boolean_expression(expression["right"]))

    # Check if the given expression is a condition, event instances are interpreted as booleans
    def is_condition(self, expression):
        return (self.is_template_instance(expression, "Event")
                or self.is_template_instance(expression, "Constraint")
                or self.string_is_int(expression)
                or self.string_is_float(expression)
                or expression in ["True", "true", "False", "false"]
                or str.startswith(expression, '"') and str.endswith(expression, '"'))

    # Helper functions

    # Get Template from given templateName
    def get_template(self, templates, template_name):
        for temp in self.templates.values():
            if template_name == temp.name:
                return temp
        return None

    # Get Instance from given instanceName
    def get_instance(self, instance_name):
        for instance in self.tree.instances.values():
            if instance_name == instance.name:
                return instance
        return None

    def get_transport_order_step(self, tos_name):
        for tos in self.tree.transport_order_steps.values():
            if tos_name == tos.name:
                return tos
        return None

    def is_template_instance(self, instance_name, template_name):
        instance = self.get_instance(instance_name)
        if instance is not None and instance.template_name == template_name:
            return True
        return False

    def has_instance_type(self, instance, type_name):
        for keyval in instance.keyval.values():
            if keyval == type_name:
                return True
        return False

    def get_attribute_value(self, instance, attribute_name):
        for key in instance.keyval:
            if key == attribute_name:
                return instance.keyval[key]
        return None

    def check_if_tos_is_present(self, instance_name):
        for tos_name in self.tree.transport_order_steps:
            if instance_name == tos_name:
                return True
        return False

    def check_if_task_is_present(self, instance_name):
        for task in self.tree.tasks:
            if instance_name == task:
                return True
        return False

    def string_is_int(self, str):
        try:
            int(str)
            return True
        except ValueError:
            return False

    def string_is_float(self, str):
        try:
            float(str)
            return True
        except ValueError:
            return False
