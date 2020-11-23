""" Contains unit tests for the schedular class """

# standard libraries
import sys
import os
import unittest
import codecs

# 3rd party packages
import xmlrunner

sys.path.append(os.path.abspath('../lotlan_schedular'))

# local sources
from lotlan_schedular.api.materialflow import MaterialFlow
from lotlan_schedular.schedular import LotlanSchedular

class TestSchedular(unittest.TestCase):
    """ Test Schedular methods """
    def test_validate(self):
        schedular = LotlanSchedular("")

        lotlan_file = codecs.open("etc/tests/Valid/HelloTask.tl", "r", encoding="utf8")
        valid_string = lotlan_file.read()
        try:
            schedular.validate(valid_string)
        except ValueError:
            self.fail("Validate failed")
        lotlan_file.close()

        lotlan_file = codecs.open("etc/tests/Invalid/Syntax/CommaAfterLastParameter.tl",
                                  "r", encoding="utf8")
        invalid_syntax_string_ = lotlan_file.read()
        self.assertRaises(ValueError, schedular.validate, invalid_syntax_string_)
        lotlan_file.close()

        lotlan_file = codecs.open("etc/tests/Invalid/Semantic/OnDoneAndRepeat.tl",
                                  "r", encoding="utf8")
        invalid_semantic_string = lotlan_file.read()
        self.assertRaises(ValueError, schedular.validate, invalid_semantic_string)
        lotlan_file.close()

    def test_init_method(self):
        lotlan_file = codecs.open("etc/examples/Scheduling/001_simple_task.tl",
                                  "r", encoding="utf8")
        lotlan_with_one_mf = lotlan_file.read()

        schedular = LotlanSchedular(lotlan_with_one_mf)
        material_flows = schedular.get_materialflows()
        self.assertEqual(len(material_flows), 1)
        lotlan_file.close()

        lotlan_file = codecs.open("etc/examples/Scheduling/006_two_tasks.tl",
                                  "r", encoding="utf8")
        lotlan_with_two_mfs = lotlan_file.read()

        schedular = LotlanSchedular(lotlan_with_two_mfs)
        material_flows = schedular.get_materialflows()
        self.assertEqual(len(material_flows), 2)
        lotlan_file.close()


if __name__ == "__main__":
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output="test-reports"),
                  failfast=False, buffer=False, catchbreak=False)
