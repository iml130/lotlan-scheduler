import sys
import os
sys.path.append(os.path.abspath('../lotlan_schedular'))

from antlr4 import InputStream, CommonTokenStream

from lotlan_schedular.SemanticValidator import SemanticValidator
from lotlan_schedular.ThrowErrorListener import ThrowErrorListener
from lotlan_schedular.TaskLanguageTest import load_templates
from lotlan_schedular.defines import TEMPLATE_STRING, TRIGGERED_BY_KEY
from lotlan_schedular.parser.LoTLanLexer import LoTLanLexer
from lotlan_schedular.parser.LoTLanParser import LoTLanParser
from lotlan_schedular.parser.CreateTreeTaskParserVisitor import CreateTreeTaskParserVisitor

import unittest
import codecs
import xmlrunner


class TestSemanticValidation(unittest.TestCase):
    def setUp(self):
        self.templates = load_templates(TEMPLATE_STRING)
        self.complete_program = None
        
    def get_semantic_validator_from_string(self, lotlan_string):
        lexer = LoTLanLexer(InputStream(lotlan_string))
        token_stream = CommonTokenStream(lexer)
        parser = LoTLanParser(token_stream)
        error_listener = ThrowErrorListener("", False, token_stream)
        visitor = CreateTreeTaskParserVisitor(error_listener)
        tree = parser.program()
        t = visitor.visit(tree)

        semantic_validator = SemanticValidator("", t, self.templates, False, error_listener)
        self.complete_program = semantic_validator.tree
        return semantic_validator

    def test_check_instances(self):
        valid_string = codecs.open("etc/tests/Valid/HelloTask.tl", "r", encoding='utf8').read()
        semantic_validator = self.get_semantic_validator_from_string(valid_string)
        self.assertEqual(semantic_validator.check_instances(), True)

        file_path = "etc/tests/Invalid/Semantic/UnknownTemplate.tl"
        invalid_string = codecs.open(file_path, "r", encoding='utf8').read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        self.assertEqual(semantic_validator.check_instances(), False)

        file_path = "etc/tests/Invalid/Semantic/TempAttributeDoesntExist.tl"
        invalid_string = codecs.open(file_path, "r", encoding='utf8').read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        self.assertEqual(semantic_validator.check_instances(), False)

        file_path = "etc/tests/Invalid/Semantic/TempAttributeNotDefined.tl"
        invalid_string = codecs.open(file_path, "r", encoding='utf8').read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        self.assertEqual(semantic_validator.check_instances(), False)

    def test_check_if_template_attribute_exists(self):
        valid_string = codecs.open("etc/tests/Valid/HelloTask.tl", "r", encoding='utf8').read()
        semantic_validator = self.get_semantic_validator_from_string(valid_string)

        instance = self.complete_program.instances["pickupItem"]
        template = self.templates["Location"]
        self.assertEqual(semantic_validator.check_if_template_attribute_exists(template, instance), True)

        file_path = "etc/tests/Invalid/Semantic/TempAttributeDoesntExist.tl"
        invalid_string = codecs.open(file_path, "r", encoding='utf8').read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        
        instance = self.complete_program.instances["location1"]
        template = self.templates["Location"]
        self.assertEqual(semantic_validator.check_if_template_attribute_exists(template, instance), False)

    def test_check_if_template_attribute_definied(self):
        valid_string = codecs.open("etc/tests/Valid/HelloTask.tl", "r", encoding='utf8').read()
        semantic_validator = self.get_semantic_validator_from_string(valid_string)

        instance = self.complete_program.instances["pickupItem"]
        template = self.templates["Location"]
        self.assertEqual(semantic_validator.check_if_template_attribute_definied(template, instance), True)

        file_path = "etc/tests/Invalid/Semantic/TempAttributeNotDefined.tl"
        invalid_string = codecs.open(file_path, "r", encoding='utf8').read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)

        instance = self.complete_program.instances["location1"]
        template = self.templates["Location"]
        self.assertEqual(semantic_validator.check_if_template_attribute_definied(template, instance), False)

    def test_check_transport_order_steps(self):
        valid_string = codecs.open("etc/tests/Valid/HelloTask.tl", "r", encoding='utf8').read()
        semantic_validator = self.get_semantic_validator_from_string(valid_string)
        self.assertEqual(semantic_validator.check_transport_order_steps(), True)

        file_path = "etc/tests/Invalid/Semantic/TosLocationHasOtherType.tl"
        invalid_string = codecs.open(file_path, "r", encoding='utf8').read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        self.assertEqual(semantic_validator.check_transport_order_steps(), False)

        file_path = "etc/tests/Invalid/Semantic/TosLocationNotAnInstance.tl"
        invalid_string = codecs.open(file_path, "r", encoding='utf8').read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        self.assertEqual(semantic_validator.check_transport_order_steps(), False)

        file_path = "etc/tests/Invalid/Semantic/TosLocationNotAnInstance.tl"
        invalid_string = codecs.open(file_path, "r", encoding='utf8').read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        self.assertEqual(semantic_validator.check_transport_order_steps(), False)

    def test_check_locations(self):
        valid_string = codecs.open("etc/tests/Valid/HelloTask.tl", "r", encoding='utf8').read()
        semantic_validator = self.get_semantic_validator_from_string(valid_string)
        tos = self.complete_program.transport_order_steps["loadStorage"]
        self.assertEqual(semantic_validator.check_locations(tos), True)

        file_path = "etc/tests/Invalid/Semantic/TosLocationHasOtherType.tl"
        invalid_string = codecs.open(file_path, "r", encoding='utf8').read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        tos = self.complete_program.transport_order_steps["loadStorage"]
        self.assertEqual(semantic_validator.check_locations(tos), False)

        file_path = "etc/tests/Invalid/Semantic/TosLocationNotAnInstance.tl"
        invalid_string = codecs.open(file_path, "r", encoding='utf8').read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        tos = self.complete_program.transport_order_steps["loadStorage"]
        self.assertEqual(semantic_validator.check_locations(tos), False)

    def test_check_tasks(self):
        valid_string = codecs.open("etc/tests/Valid/HelloTask.tl", "r", encoding='utf8').read()
        semantic_validator = self.get_semantic_validator_from_string(valid_string)
        self.assertEqual(semantic_validator.check_tasks(), True)

        file_path = "etc/tests/Invalid/Semantic/UnknownTaskInFrom.tl"
        invalid_string = codecs.open(file_path, "r", encoding='utf8').read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        self.assertEqual(semantic_validator.check_tasks(), False)

        file_path = "etc/tests/Invalid/Semantic/UnknownTaskInTo.tl"
        invalid_string = codecs.open(file_path, "r", encoding='utf8').read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        self.assertEqual(semantic_validator.check_tasks(), False)

        file_path = "etc/tests/Invalid/Semantic/ParameterAmountDoesntMatch.tl"
        invalid_string = codecs.open(file_path, "r", encoding='utf8').read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        self.assertEqual(semantic_validator.check_tasks(), False)

        file_path = "etc/tests/Invalid/Semantic/OnDoneAndRepeat.tl"
        invalid_string = codecs.open(file_path, "r", encoding='utf8').read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        self.assertEqual(semantic_validator.check_tasks(), False)

        file_path = "etc/tests/Invalid/Semantic/TaskUnknownOnDoneTask.tl"
        invalid_string = codecs.open(file_path, "r", encoding='utf8').read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        self.assertEqual(semantic_validator.check_tasks(), False)

    def test_check_transport_orders(self):
        valid_string = codecs.open("etc/tests/Valid/HelloTask.tl", "r", encoding='utf8').read()
        semantic_validator = self.get_semantic_validator_from_string(valid_string)
        task = self.complete_program.tasks["helloTask"]
        self.assertEqual(semantic_validator.check_transport_orders(task), True)

        file_path = "etc/tests/Invalid/Semantic/UnknownTaskInFrom.tl"
        invalid_string = codecs.open(file_path, "r", encoding='utf8').read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        task = self.complete_program.tasks["helloTask"]
        self.assertEqual(semantic_validator.check_transport_orders(task), False)

        file_path = "etc/tests/Invalid/Semantic/UnknownTaskInTo.tl"
        invalid_string = codecs.open(file_path, "r", encoding='utf8').read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        task = self.complete_program.tasks["helloTask"]
        self.assertEqual(semantic_validator.check_transport_orders(task), False)

        file_path = "etc/tests/Invalid/Semantic/ParameterAmountDoesntMatch.tl"
        invalid_string = codecs.open(file_path, "r", encoding='utf8').read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        task = self.complete_program.tasks["helloTask"]
        self.assertEqual(semantic_validator.check_transport_orders(task), False)

    def test_check_on_done(self):
        valid_string = codecs.open("etc/tests/Valid/HelloTask.tl", "r", encoding='utf8').read()
        semantic_validator = self.get_semantic_validator_from_string(valid_string)
        self.assertEqual(semantic_validator.check_instances(), True)

        file_path = "etc/tests/Invalid/Semantic/TosUnknownOnDoneTask.tl"
        invalid_string = codecs.open(file_path, "r", encoding='utf8').read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        tos = self.complete_program.transport_order_steps["unloadWorkstation1"]
        self.assertEqual(semantic_validator.check_on_done(tos), False)

        file_path = "etc/tests/Invalid/Semantic/TaskUnknownOnDoneTask.tl"
        invalid_string = codecs.open(file_path, "r", encoding='utf8').read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        task = self.complete_program.tasks["helloTask"]
        self.assertEqual(semantic_validator.check_on_done(task), False)

    def test_check_repeat_or_on_done(self):
        valid_string = codecs.open("etc/tests/Valid/HelloTask.tl", "r", encoding='utf8').read()
        semantic_validator = self.get_semantic_validator_from_string(valid_string)
        task = self.complete_program.tasks["helloTask"]
        self.assertEqual(semantic_validator.check_repeat_or_on_done(task), True)

        file_path = "etc/tests/Invalid/Semantic/OnDoneAndRepeat.tl"
        invalid_string = codecs.open(file_path, "r", encoding='utf8').read()
        semantic_validator = self.get_semantic_validator_from_string(invalid_string)
        task = self.complete_program.tasks["helloTask"]
        self.assertEqual(semantic_validator.check_repeat_or_on_done(task), False)

    def test_check_expression(self):
        valid_string = codecs.open("etc/tests/Valid/HelloTaskTriggeredBy.tl", "r", encoding='utf8').read()
        semantic_validator = self.get_semantic_validator_from_string(valid_string)

        context = self.complete_program.tasks["helloTask"].context_dict[TRIGGERED_BY_KEY]

        self.assertEqual(semantic_validator.check_expression("triggerGetNewMaterial", context), True)
        self.assertEqual(semantic_validator.check_expression("True", context), True)
        self.assertEqual(semantic_validator.check_expression({"left":"triggerGetNewMaterial", "right":"False", "binOp":"=="}, context), True)

        expression = {"left":{"left":"triggerGetNewMaterial", "right":"True", "binOp":"!="}, "right":"False", "binOp":"=="}
        self.assertEqual(semantic_validator.check_expression(expression, context), True)

        self.assertEqual(semantic_validator.check_expression("5", context), False)
        self.assertEqual(semantic_validator.check_expression("5.0", context), False)
        self.assertEqual(semantic_validator.check_expression('"string"', context), False)
        self.assertEqual(semantic_validator.check_expression({"left":"event", "right":"False", "binOp":"=="}, context), False)

        expression = {"left":"helloTask", "right":"isDone", "binOp":"."}
        self.assertEqual(semantic_validator.check_binary_operation(expression, context), True)

    def test_check_single_expression(self):
        valid_string = codecs.open("etc/tests/Valid/HelloTaskTriggeredBy.tl", "r", encoding='utf8').read()
        semantic_validator = self.get_semantic_validator_from_string(valid_string)
        context = self.complete_program.tasks["helloTask"].context_dict[TRIGGERED_BY_KEY]
        self.assertEqual(semantic_validator.check_single_expression("triggerGetNewMaterial", context), True)

        self.assertEqual(semantic_validator.check_single_expression("not_an_expression", context), False)
        self.assertEqual(semantic_validator.check_single_expression("10", context), False)
    
    def test_check_unary_operation(self):
        valid_string = codecs.open("etc/tests/Valid/HelloTaskTriggeredBy.tl", "r", encoding='utf8').read()
        semantic_validator = self.get_semantic_validator_from_string(valid_string)
        context = self.complete_program.tasks["helloTask"].context_dict[TRIGGERED_BY_KEY]

        expression = {"unop": "!", "value": "triggerGetNewMaterial"}
        self.assertEqual(semantic_validator.check_unary_operation(expression, context), True)

        expression = {"unop": "!", "value": {"left":"triggerGetNewMaterial", "right":"False", "binOp":"=="}}
        self.assertEqual(semantic_validator.check_unary_operation(expression, context), True)

        expression = {"unop": "!", "value": "not_an_expression"}
        self.assertEqual(semantic_validator.check_unary_operation(expression, context), False)


    def test_check_binary_operation(self):
        valid_string = codecs.open("etc/tests/Valid/HelloTaskTriggeredBy.tl", "r", encoding='utf8').read()
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

    def test_is_boolean_expression(self):
        valid_string = codecs.open("etc/tests/Valid/HelloTaskTriggeredBy.tl", "r", encoding='utf8').read()
        semantic_validator = self.get_semantic_validator_from_string(valid_string)
        
        self.assertEqual(semantic_validator.is_boolean_expression("triggerGetNewMaterial"), True)
        self.assertEqual(semantic_validator.is_boolean_expression("5"), True)
        self.assertEqual(semantic_validator.is_boolean_expression("5.0"), True)
        self.assertEqual(semantic_validator.is_boolean_expression('"string"'), True)
        self.assertEqual(semantic_validator.is_boolean_expression("True"), True)
        self.assertEqual(semantic_validator.is_boolean_expression({"left":"triggerGetNewMaterial", "right":"False", "binOp":"=="}), True)

        expression = {"left":{"left":"triggerGetNewMaterial", "right":"True", "binOp":"!="}, "right":"False", "binOp":"=="}
        self.assertEqual(semantic_validator.is_boolean_expression(expression), True)

        self.assertEqual(semantic_validator.is_boolean_expression({"left":"event", "right":"False", "binOp":"=="}), False)

    def test_is_condition(self):
        valid_string = codecs.open("etc/tests/Valid/HelloTaskTriggeredBy.tl", "r", encoding='utf8').read()
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

if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'), failfast=False, buffer=False, catchbreak=False)
