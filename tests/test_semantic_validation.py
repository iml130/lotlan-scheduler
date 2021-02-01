""" Contains the test for the SemanticValidation class """

# standard libraries
import sys
import os
import unittest
import codecs

# 3rd party packages
from antlr4 import InputStream, CommonTokenStream
import xmlrunner

sys.path.append(os.path.abspath("../lotlan_schedular"))

# local sources
from lotlan_schedular.validation.semantic_validator import SemanticValidator
from lotlan_schedular.validation.syntax_error_listener import SyntaxErrorListener
from lotlan_schedular.validation.task_language_test import load_templates
from lotlan_schedular.defines import TEMPLATE_STRING, TRIGGERED_BY_KEY
from lotlan_schedular.parser.LoTLanLexer import LoTLanLexer
from lotlan_schedular.parser.LoTLanParser import LoTLanParser
from lotlan_schedular.parser.lotlan_tree_visitor import LotlanTreeVisitor

class TestSemanticValidation(unittest.TestCase):
    """
        Tests if all semantic validation checks are working correctly
        so all errors are being detected and all valid files are passed through
    """
    def setUp(self):
        self.templates = load_templates(TEMPLATE_STRING)
        self.complete_program = None
    
    def get_semantic_validator_from_string(self, lotlan_string):
        lexer = LoTLanLexer(InputStream(lotlan_string))
        token_stream = CommonTokenStream(lexer)
        parser = LoTLanParser(token_stream)
        error_listener = SyntaxErrorListener("", False, token_stream)
        visitor = LotlanTreeVisitor(error_listener)
        tree = parser.program()
        t = visitor.visit(tree)

        semantic_validator = SemanticValidator("", t, self.templates, False, error_listener)
        self.complete_program = semantic_validator.tree
        return semantic_validator

    def test_check_instances(self):
        lotlan_file = codecs.open("etc/tests/Valid/HelloTask.tl", "r", encoding="utf8")
        valid_string = lotlan_file.read()
        semantic_validator = self.get_semantic_validator_from_string(valid_string)
        self.assertEqual(semantic_validator.check_instances(), True)
        lotlan_file.close()

        file_path = "etc/tests/Invalid/Semantic/UnknownTemplate.tl"
        lotlan_file = codecs.open(file_path, "r", encoding="utf8")
        invalid_string = lotlan_file.read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        self.assertEqual(semantic_validator.check_instances(), False)
        lotlan_file.close()

        file_path = "etc/tests/Invalid/Semantic/TempAttributeDoesntExist.tl"
        lotlan_file = codecs.open(file_path, "r", encoding="utf8")
        invalid_string = lotlan_file.read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        self.assertEqual(semantic_validator.check_instances(), False)
        lotlan_file.close()

        lotlan_file = codecs.open(file_path, "r", encoding="utf8")
        file_path = "etc/tests/Invalid/Semantic/TempAttributeNotDefined.tl"
        invalid_string = lotlan_file.read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        self.assertEqual(semantic_validator.check_instances(), False)
        lotlan_file.close()

    def test_check_if_template_attribute_exists(self):
        lotlan_file = codecs.open("etc/tests/Valid/HelloTask.tl", "r", encoding="utf8")
        valid_string = lotlan_file.read()
        semantic_validator = self.get_semantic_validator_from_string(valid_string)

        instance = self.complete_program.instances["pickupItem"]
        template = self.templates["Location"]
        self.assertEqual(semantic_validator.check_if_template_attribute_exists(template, instance),
                         True)
        lotlan_file.close()

        file_path = "etc/tests/Invalid/Semantic/TempAttributeDoesntExist.tl"
        lotlan_file = codecs.open(file_path, "r", encoding="utf8")
        invalid_string = lotlan_file.read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)

        instance = self.complete_program.instances["location1"]
        template = self.templates["Location"]
        self.assertEqual(semantic_validator.check_if_template_attribute_exists(template, instance),
                         False)
        lotlan_file.close()

    def test_check_if_template_attribute_definied(self):
        lotlan_file = codecs.open("etc/tests/Valid/HelloTask.tl", "r", encoding="utf8")
        valid_string = lotlan_file.read()
        semantic_validator = self.get_semantic_validator_from_string(valid_string)

        instance = self.complete_program.instances["pickupItem"]
        template = self.templates["Location"]
        self.assertEqual(
            semantic_validator.check_if_template_attribute_definied(template, instance),
            True)
        lotlan_file.close()

        file_path = "etc/tests/Invalid/Semantic/TempAttributeNotDefined.tl"
        lotlan_file = codecs.open(file_path, "r", encoding="utf8")
        invalid_string = lotlan_file.read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)

        instance = self.complete_program.instances["location1"]
        template = self.templates["Location"]
        self.assertEqual(
            semantic_validator.check_if_template_attribute_definied(template, instance),
            False)
        lotlan_file.close()

    def test_check_transport_order_steps(self):
        lotlan_file = codecs.open("etc/tests/Valid/HelloTask.tl", "r", encoding="utf8")
        valid_string = lotlan_file.read()
        semantic_validator = self.get_semantic_validator_from_string(valid_string)
        self.assertEqual(semantic_validator.check_transport_order_steps(), True)
        lotlan_file.close()

        file_path = "etc/tests/Invalid/Semantic/TosLocationHasOtherType.tl"
        lotlan_file = codecs.open(file_path, "r", encoding="utf8")
        invalid_string = lotlan_file.read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        self.assertEqual(semantic_validator.check_transport_order_steps(), False)
        lotlan_file.close()

        file_path = "etc/tests/Invalid/Semantic/TosLocationNotAnInstance.tl"
        lotlan_file = codecs.open(file_path, "r", encoding="utf8")
        invalid_string = lotlan_file.read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        self.assertEqual(semantic_validator.check_transport_order_steps(), False)
        lotlan_file.close()

        file_path = "etc/tests/Invalid/Semantic/TosLocationNotAnInstance.tl"
        lotlan_file = codecs.open(file_path, "r", encoding="utf8")
        invalid_string = lotlan_file.read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        self.assertEqual(semantic_validator.check_transport_order_steps(), False)
        lotlan_file.close()

    def test_check_locations(self):
        lotlan_file = codecs.open("etc/tests/Valid/HelloTask.tl", "r", encoding="utf8")
        valid_string = lotlan_file.read()
        semantic_validator = self.get_semantic_validator_from_string(valid_string)
        tos = self.complete_program.transport_order_steps["loadStorage"]
        self.assertEqual(semantic_validator.check_locations(tos), True)
        lotlan_file.close()

        file_path = "etc/tests/Invalid/Semantic/TosLocationHasOtherType.tl"
        lotlan_file = codecs.open(file_path, "r", encoding="utf8")
        invalid_string = lotlan_file.read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        tos = self.complete_program.transport_order_steps["loadStorage"]
        self.assertEqual(semantic_validator.check_locations(tos), False)
        lotlan_file.close()

        file_path = "etc/tests/Invalid/Semantic/TosLocationNotAnInstance.tl"
        lotlan_file = codecs.open(file_path, "r", encoding="utf8")
        invalid_string = lotlan_file.read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        tos = self.complete_program.transport_order_steps["loadStorage"]
        self.assertEqual(semantic_validator.check_locations(tos), False)
        lotlan_file.close()

    def test_check_tasks(self):
        lotlan_file = codecs.open("etc/tests/Valid/HelloTask.tl", "r", encoding="utf8")
        valid_string = lotlan_file.read()
        semantic_validator = self.get_semantic_validator_from_string(valid_string)
        self.assertEqual(semantic_validator.check_tasks(), True)
        lotlan_file.close()

        file_path = "etc/tests/Invalid/Semantic/UnknownTaskInFrom.tl"
        lotlan_file = codecs.open(file_path, "r", encoding="utf8")
        invalid_string = lotlan_file.read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        self.assertEqual(semantic_validator.check_tasks(), False)
        lotlan_file.close()

        file_path = "etc/tests/Invalid/Semantic/UnknownTaskInTo.tl"
        lotlan_file = codecs.open(file_path, "r", encoding="utf8")
        invalid_string = lotlan_file.read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        self.assertEqual(semantic_validator.check_tasks(), False)
        lotlan_file.close()

        file_path = "etc/tests/Invalid/Semantic/ParameterAmountDoesntMatch.tl"
        lotlan_file = codecs.open(file_path, "r", encoding="utf8")
        invalid_string = lotlan_file.read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        self.assertEqual(semantic_validator.check_tasks(), False)
        lotlan_file.close()

        file_path = "etc/tests/Invalid/Semantic/OnDoneAndRepeat.tl"
        lotlan_file = codecs.open(file_path, "r", encoding="utf8")
        invalid_string = lotlan_file.read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        self.assertEqual(semantic_validator.check_tasks(), False)
        lotlan_file.close()

        file_path = "etc/tests/Invalid/Semantic/TaskUnknownOnDoneTask.tl"
        lotlan_file = codecs.open(file_path, "r", encoding="utf8")
        invalid_string = lotlan_file.read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        self.assertEqual(semantic_validator.check_tasks(), False)
        lotlan_file.close()

    def test_check_transport_orders(self):
        lotlan_file = codecs.open("etc/tests/Valid/HelloTask.tl", "r", encoding="utf8")
        valid_string = lotlan_file.read()
        semantic_validator = self.get_semantic_validator_from_string(valid_string)
        task = self.complete_program.tasks["helloTask"]
        self.assertEqual(semantic_validator.check_transport_orders(task), True)
        lotlan_file.close()

        file_path = "etc/tests/Invalid/Semantic/UnknownTaskInFrom.tl"
        lotlan_file = codecs.open(file_path, "r", encoding="utf8")
        invalid_string = lotlan_file.read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        task = self.complete_program.tasks["helloTask"]
        self.assertEqual(semantic_validator.check_transport_orders(task), False)
        lotlan_file.close()

        file_path = "etc/tests/Invalid/Semantic/UnknownTaskInTo.tl"
        lotlan_file = codecs.open(file_path, "r", encoding="utf8")
        invalid_string = lotlan_file.read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        task = self.complete_program.tasks["helloTask"]
        self.assertEqual(semantic_validator.check_transport_orders(task), False)
        lotlan_file.close()

        file_path = "etc/tests/Invalid/Semantic/ParameterAmountDoesntMatch.tl"
        lotlan_file = codecs.open(file_path, "r", encoding="utf8")
        invalid_string = lotlan_file.read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        task = self.complete_program.tasks["helloTask"]
        self.assertEqual(semantic_validator.check_transport_orders(task), False)
        lotlan_file.close()

    def test_check_on_done(self):
        lotlan_file = codecs.open("etc/tests/Valid/HelloTask.tl", "r", encoding="utf8")
        valid_string = lotlan_file.read()
        semantic_validator = self.get_semantic_validator_from_string(valid_string)
        self.assertEqual(semantic_validator.check_instances(), True)
        lotlan_file.close()

        file_path = "etc/tests/Invalid/Semantic/TosUnknownOnDoneTask.tl"
        lotlan_file = codecs.open(file_path, "r", encoding="utf8")
        invalid_string = lotlan_file.read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        tos = self.complete_program.transport_order_steps["unloadWorkstation1"]
        self.assertEqual(semantic_validator.check_on_done(tos), False)
        lotlan_file.close()

        file_path = "etc/tests/Invalid/Semantic/TaskUnknownOnDoneTask.tl"
        lotlan_file = codecs.open(file_path, "r", encoding="utf8")
        invalid_string = lotlan_file.read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        task = self.complete_program.tasks["helloTask"]
        self.assertEqual(semantic_validator.check_on_done(task), False)
        lotlan_file.close()

    def test_check_repeat_or_on_done(self):
        lotlan_file = codecs.open("etc/tests/Valid/HelloTask.tl", "r", encoding="utf8")
        valid_string = lotlan_file.read()
        semantic_validator = self.get_semantic_validator_from_string(valid_string)
        task = self.complete_program.tasks["helloTask"]
        self.assertEqual(semantic_validator.check_repeat_or_on_done(task), True)
        lotlan_file.close()

        file_path = "etc/tests/Invalid/Semantic/OnDoneAndRepeat.tl"
        lotlan_file = codecs.open(file_path, "r", encoding="utf8")
        invalid_string = lotlan_file.read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        task = self.complete_program.tasks["helloTask"]
        self.assertEqual(semantic_validator.check_repeat_or_on_done(task), False)
        lotlan_file.close()

    def test_check_expression(self):
        lotlan_file = codecs.open("etc/tests/Valid/HelloTaskTriggeredBy.tl", "r", encoding="utf8")
        valid_string = lotlan_file.read()
        semantic_validator = self.get_semantic_validator_from_string(valid_string)

        context = self.complete_program.tasks["helloTask"].context_dict[TRIGGERED_BY_KEY]

        self.assertEqual(semantic_validator.check_expression("triggerGetNewMaterial", context),
                         True)
        self.assertEqual(semantic_validator.check_expression("True", context), True)

        expression = {"left":"triggerGetNewMaterial", "right":"False", "binOp":"=="}
        self.assertEqual(semantic_validator.check_expression(expression, context), True)

        expression = (
        {
            "left":
            {
                "left":"triggerGetNewMaterial", "right":"True", "binOp":"!="
            },
            "right":"False", "binOp":"=="
        })
        self.assertEqual(semantic_validator.check_expression(expression, context), True)

        self.assertEqual(semantic_validator.check_expression("5", context), False)
        self.assertEqual(semantic_validator.check_expression("5.0", context), False)
        self.assertEqual(semantic_validator.check_expression("'string'", context), False)

        expression = {"left":"event", "right":"False", "binOp":"=="}
        self.assertEqual(semantic_validator.check_expression(expression, context), False)

        expression = {"left":"helloTask", "right":"isDone", "binOp":"."}
        self.assertEqual(semantic_validator.check_binary_operation(expression, context), True)

        lotlan_file.close()

    def test_check_single_expression(self):
        lotlan_file = codecs.open("etc/tests/Valid/HelloTaskTriggeredBy.tl", "r", encoding="utf8")
        valid_string = lotlan_file.read()

        semantic_validator = self.get_semantic_validator_from_string(valid_string)
        context = self.complete_program.tasks["helloTask"].context_dict[TRIGGERED_BY_KEY]

        expression = "triggerGetNewMaterial"
        self.assertEqual(semantic_validator.check_single_expression(expression, context), True)

        self.assertEqual(semantic_validator.check_single_expression("not_an_expression", context),
                         False)
        self.assertEqual(semantic_validator.check_single_expression("10", context), False)

        lotlan_file.close()

    def test_check_unary_operation(self):
        lotlan_file = codecs.open("etc/tests/Valid/HelloTaskTriggeredBy.tl", "r", encoding="utf8")
        valid_string = lotlan_file.read()

        semantic_validator = self.get_semantic_validator_from_string(valid_string)
        context = self.complete_program.tasks["helloTask"].context_dict[TRIGGERED_BY_KEY]

        expression = {"unop": "!", "value": "triggerGetNewMaterial"}
        self.assertEqual(semantic_validator.check_unary_operation(expression, context), True)

        expression = (
        {
            "unop": "!",
            "value":
            {
                "left":"triggerGetNewMaterial",
                "right":"False",
                "binOp":"=="
            }
        })
        self.assertEqual(semantic_validator.check_unary_operation(expression, context), True)

        expression = {"unop": "!", "value": "not_an_expression"}
        self.assertEqual(semantic_validator.check_unary_operation(expression, context), False)

        lotlan_file.close()

    def test_check_binary_operation(self):
        lotlan_file = codecs.open("etc/tests/Valid/HelloTaskTriggeredBy.tl", "r", encoding="utf8")
        valid_string = lotlan_file.read()
        semantic_validator = self.get_semantic_validator_from_string(valid_string)

        context = self.complete_program.tasks["helloTask"].context_dict[TRIGGERED_BY_KEY]

        expression = {"left":"helloTask", "right":"isDone", "binOp":"."}
        self.assertEqual(semantic_validator.check_binary_operation(expression, context), True)

        expression = {"left":"triggerGetNewMaterial", "right":"False", "binOp":"=="}
        self.assertEqual(semantic_validator.check_binary_operation(expression, context), True)

        expression = {"left":"event", "right":"False", "binOp":"=="}
        self.assertEqual(semantic_validator.check_binary_operation(expression, context), False)

        expression = {"left":"not_a_task", "right":"isDone", "binOp":"."}
        self.assertEqual(semantic_validator.check_binary_operation(expression, context), False)

        lotlan_file.close()

    def test_is_boolean_expression(self):
        lotlan_file = codecs.open("etc/tests/Valid/HelloTaskTriggeredBy.tl", "r", encoding="utf8")
        valid_string = lotlan_file.read()
        semantic_validator = self.get_semantic_validator_from_string(valid_string)

        self.assertEqual(semantic_validator.is_boolean_expression("triggerGetNewMaterial"), True)
        self.assertEqual(semantic_validator.is_boolean_expression("5"), True)
        self.assertEqual(semantic_validator.is_boolean_expression("5.0"), True)
        self.assertEqual(semantic_validator.is_boolean_expression('"string"'), True)
        self.assertEqual(semantic_validator.is_boolean_expression("True"), True)

        expression = {"left":"triggerGetNewMaterial", "right":"False", "binOp":"=="}
        self.assertEqual(semantic_validator.is_boolean_expression(expression), True)

        expression = (
        {
            "left":
            {
                "left":"triggerGetNewMaterial",
                "right":"True",
                "binOp":"!="
            },
            "right":"False",
            "binOp":"=="
        })
        self.assertEqual(semantic_validator.is_boolean_expression(expression), True)

        expression = {"left":"event", "right":"False", "binOp":"=="}
        self.assertEqual(semantic_validator.is_boolean_expression(expression), False)

        lotlan_file.close()

    def test_is_condition(self):
        lotlan_file = codecs.open("etc/tests/Valid/HelloTaskTriggeredBy.tl", "r", encoding="utf8")
        valid_string = lotlan_file.read()
        semantic_validator = self.get_semantic_validator_from_string(valid_string)

        self.assertEqual(semantic_validator.is_condition("triggerGetNewMaterial"), True)
        self.assertEqual(semantic_validator.is_condition("5"), True)
        self.assertEqual(semantic_validator.is_condition("5.0"), True)
        self.assertEqual(semantic_validator.is_condition('"string"'), True)
        self.assertEqual(semantic_validator.is_condition("True"), True)
        self.assertEqual(semantic_validator.is_condition("true"), True)
        self.assertEqual(semantic_validator.is_condition("False"), True)
        self.assertEqual(semantic_validator.is_condition("false"), True)

        self.assertEqual(semantic_validator.is_condition("random_string"), False)
        self.assertEqual(semantic_validator.is_condition("!3123??"), False)

        lotlan_file.close()

if __name__ == "__main__":
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output="test-reports"),
        failfast=False, buffer=False, catchbreak=False)
