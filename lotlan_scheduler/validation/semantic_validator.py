""" This module contains the SemanticValidator class """

# local sources
import lotlan_scheduler.helpers as helpers

# globals defines
from lotlan_scheduler.defines import TRIGGERED_BY_KEY, FINISHED_BY_KEY, ON_DONE_KEY, LOCATION_KEY

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

    def check_instances(self):
        """ Executes semantic checks for all instances """
        error_found = False
        for instance in self.tree.instances.values():
            template_name = instance.template_name
            template = helpers.get_template(self.templates, template_name)

            # check if the corresponding template exists
            if template is None:
                msg = ("The Instance '{}' refers to a template" +
                       "that does not exist").format(instance.name)
                context_start = instance.context.start
                self.error_listener.print_error(msg, context_start.line, context_start.column,
                                                len(instance.name), False)
                error_found = True
            # check if the instance variables match with the corresponding template
            else:
                if (not self.check_if_template_attribute_exists(template, instance) or
                    not self.check_if_template_attribute_definied(template, instance)):
                    error_found = True
        return not error_found

    def check_if_template_attribute_exists(self, template, instance):
        """ Check if all attributes in the given instance are definied in the template """
        for instance_attribute in instance.keyval:
            attribute_found = False
            for template_attribute in template.keyval:
                if instance_attribute == template_attribute:
                    attribute_found = True
            if attribute_found is False:
                msg = ("The attribute '{}' in instance '{}' was not defined " +
                       "in the corresponding template").format(instance_attribute, instance.name)

                variable_context = instance.context_dict[instance_attribute]
                self.error_listener.print_error(msg, variable_context.start.line,
                                                variable_context.start.column,
                                                len(instance_attribute), False)
                return False
        return True

    def check_if_template_attribute_definied(self, template, instance):
        """ Check if all attributes definied in the template are set in instance """
        for template_attribute in template.keyval:
            attribute_found = False
            for instance_attribute in instance.keyval:
                if template_attribute == instance_attribute:
                    attribute_found = True
            if attribute_found is False:
                msg = ("The attribute '{}' from the corresponding template was not" +
                       "definied in instance '{}'").format(template_attribute, instance.name)
                self.error_listener.print_error(msg, instance.context.start.line,
                                                instance.context.start.column,
                                                len(template_attribute), False)
                return False
        return True

    def check_transport_order_steps(self):
        """ Executes checks for all TransportOrderSteps """
        error_found = False
        for tos in self.tree.transport_order_steps.values():
            context_dict = tos.context_dict

            if not self.check_locations(tos) or not self.check_on_done(tos):
                error_found = True

            if TRIGGERED_BY_KEY in context_dict:
                if not self.check_expression(tos.triggered_by_statements,
                                             context_dict[TRIGGERED_BY_KEY]):
                    error_found = True
            if FINISHED_BY_KEY in context_dict:
                if not self.check_expression(tos.finished_by_statements,
                                             context_dict[FINISHED_BY_KEY]):
                    error_found = True
        return not error_found

    def check_locations(self, tos):
        """ Executes semantic checks for all location instances """
        context_dict = tos.context_dict

        if LOCATION_KEY in context_dict:
            location = tos.location
            location_instance = helpers.get_instance(self.tree.instances, location.logical_name)
            location_context = context_dict[LOCATION_KEY]

            if location_instance is None:
                msg = ("The location instance '{}' in TransportOrderStep '{}'" +
                      "could not be found").format(location.logical_name, tos.name)
                self.error_listener.print_error(msg, location_context.start.line,
                                                location_context.start.column,
                                                len(location.logical_name), False)
                return False
            elif location_instance.template_name != "Location":
                msg = ("The instance '{}' in TransportOrderStep '{}' is "
                       "not a 'Location' instance but a '{}' instance").format(
                        location.logical_name, tos.name, location_instance.template_name)
                self.error_listener.print_error(msg, location_context.start.line,
                                                location_context.start.column,
                                                len(location.logical_name), False)
                return False

        return True

    def check_tasks(self):
        """ Executes semantic checks for all Tasks """
        error_found = False
        for task in self.tree.tasks.values():
            context_dict = task.context_dict

            if (not self.check_transport_orders(task) or
                not self.check_repeat_or_on_done(task) or
                not self.check_on_done(task)):
                error_found = True
            if TRIGGERED_BY_KEY in task.context_dict:
                if not self.check_expression(task.triggered_by, context_dict[TRIGGERED_BY_KEY]):
                    error_found = True
            if FINISHED_BY_KEY in task.context_dict:
                if self.check_expression(task.finished_by, context_dict[FINISHED_BY_KEY]):
                    error_found = True
        return not error_found

    def check_transport_orders(self, task):
        """ Executes semantic checks for all TransportOrders """
        if task.transport_order is not None:
            # From check
            if self.check_if_tos_is_present(task.transport_order.pickup_tos.name) is False:
                msg = "Task '{}' refers to an unknown TransportOrderStep in 'from': '{}' ".format(
                    task.name, task.transport_order.pickup_tos.name)
                self.error_listener.print_error(msg, task.context.start.line,
                                                task.context.start.column,
                                                len(task.transport_order.pickup_tos.name), False)
                return False

            tos = helpers.get_transport_order_step(self.tree.transport_order_steps,
                                                   task.transport_order.pickup_tos.name)
            if len(task.transport_order.from_parameters) != len(tos.parameters):
                msg = "From has not the same amount of parameters as the transport order step!"
                self.error_listener.print_error(msg, task.context.start.line,
                                                task.context.start.column,
                                                len(task.transport_order.pickup_tos.name), False)
                return False

            # To check
            if self.check_if_tos_is_present(task.transport_order.delivery_tos.name) is False:
                msg = "Task '{}' refers to an unknown TransportOrderStep in 'to' '{}'".format(
                    task.name, task.transport_order.delivery_tos.name)
                self.error_listener.print_error(msg, task.context.start.line,
                                                task.context.start.column,
                                                len(task.transport_order.delivery_tos.name), False)
                return False

            tos = helpers.get_transport_order_step(self.tree.transport_order_steps,
                                                   task.transport_order.delivery_tos.name)
            if len(task.transport_order.to_parameters) != len(tos.parameters):
                msg = "To has not the same amount of parameters as the transport order step!"
                self.error_listener.print_error(msg, task.context.start.line,
                                                task.context.start.column,
                                                len(task.transport_order.delivery_tos.name), False)
                return False
        return True

    def check_on_done(self, task_or_tos):
        """ Checks if the task in on done refers to a known task """
        context_dict = task_or_tos.context_dict
        error_found = False
        for on_done_task in task_or_tos.on_done:
            if self.check_if_task_is_present(on_done_task) is False:
                msg = ("The task name '{}' in the OnDone statement refers " +
                      "to an unknown Task").format(on_done_task)
                self.error_listener.print_error(msg, context_dict[ON_DONE_KEY].start.line,
                                                context_dict[ON_DONE_KEY].start.column,
                                                len(on_done_task), False)
                error_found = True
        return not error_found

    def check_repeat_or_on_done(self, task):
        """ Checks if a task has both repeat and ondone statements """
        if task.repeat and task.on_done:
            msg = ("The task '{}' has both OnDone and Repeat statements."
                   "It is only allowed to have either of them").format(task.name)
            self.error_listener.print_error(msg, task.context.start.line,
                                            task.context.start.column,
                                            len(task.name), False)
            return False
        return True

    def check_expressions(self, expressions, task_or_tos):
        """ Executes checks to test given expressions """
        if len(expressions) > 1:
            msg = ("There is more than one TriggeredBy or FinishedBy " +
                   "Statement in '{}'").format(task_or_tos.name)
            self.error_listener.print_error(msg, task_or_tos.context.start.line,
                                            task_or_tos.context.start.column,
                                            len(task_or_tos.name), False)
            return False
        if (len(expressions) == 1 and
            not self.check_expression(expressions[0].value, expressions[0].context)):
            return False
        return True

    def check_expression(self, expression, context):
        """ Executes checks to test given expression """
        if isinstance(expression, str):
            if not self.check_single_expression(expression, context):
                return False
        elif isinstance(expression, dict):
            if len(expression) == 2:
                if not self.check_unary_operation(expression, context):
                    return False
            else:
                if not self.check_binary_operation(expression, context):
                    return False
        return True

    def check_single_expression(self, expression, context):
        """
            Checks if a single expression is a valid expression
            example for a single expr.: 'buttonPressed'
        """
        if helpers.is_template_instance(self.tree.instances, expression, "Event") is True:
            instance = helpers.get_instance(self.tree.instances, expression)
            if helpers.has_instance_type(instance, "Boolean") is False:
                msg = ("'" + expression +
                       "' has no booelan type so it cant get parsed as single statement")
                self.error_listener.print_error(msg, context.start.line,
                                                context.start.column, 1, False)
                return False
        elif helpers.is_template_instance(self.tree.instances, expression, "Time") is False:
            if expression not in ["True", "true", "False", "false"]:
                msg = "The given expression is not related to a time or event instance"
                self.error_listener.print_error(msg, context.start.line,
                                                context.start.column, 1, False)
                return False
        return True

    def check_unary_operation(self, expression, context):
        """
            Checks if a unary expression is a valid expression
            example for an unary expr.: !buttonPressed
        """
        if self.is_boolean_expression(expression["value"]) is False:
            msg = ("The given expression couldnt be resolved to " +
                   "a boolean so it cant get parsed as a single statement")
            self.error_listener.print_error(msg, context.start.line, context.start.column,
                                            len(expression["value"]), False)
            return False
        return True

    def check_binary_operation(self, expression, context):
        """
            Checks if a binary expression is a valid expression
            example for a binary expr.: 'buttonPressed and !buttonPressed2'
        """
        left = expression["left"]
        right = expression["right"]

        if expression["binOp"] == ".":
            if self.check_if_task_is_present(expression["left"]) is False:
                msg = "The task given in the expression is not defined"
                self.error_listener.print_error(msg, context.start.line,
                                                context.start.column,
                                                len(expression["left"]), False)
                return False
        else:
            if self.is_boolean_expression(right) is False:
                msg = "The right side is not a boolean expression "
                self.error_listener.print_error(msg, context.start.line,
                                                context.start.column, len(right), False)
                return False
            if self.is_boolean_expression(left) is False:
                msg = "The left side is not a boolean expression"
                self.error_listener.print_error(msg, context.start.line,
                                                context.start.column, len(left), False)
                return False
        return True

    def is_boolean_expression(self, expression):
        """ Checks if the given expression can be resolved to a boolean expression """
        if isinstance(expression, str):
            return self.is_condition(expression)
        if isinstance(expression, dict):
            if len(expression) == 2:
                return self.is_boolean_expression(expression["value"])

            # an expression enclosed by parenthesis has the key binOp in the dict
            if expression["left"] == "(" and expression["right"] == ")":
                return self.is_boolean_expression(expression["binOp"])

            return (self.is_boolean_expression(expression["left"]) and
                    self.is_boolean_expression(expression["right"]))
        return False

    def is_condition(self, expression):
        """ Checks if the given expression is a condition """
        return (helpers.is_template_instance(self.tree.instances, expression, "Event")
                or helpers.is_template_instance(self.tree.instances, expression, "Constraint")
                or helpers.string_is_int(expression)
                or helpers.string_is_float(expression)
                or expression in ["True", "true", "False", "false"]
                or str.startswith(expression, '"') and str.endswith(expression, '"'))

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
