""" Contains unit tests for the scheduler class """

# standard libraries
import sys
import os
import unittest
import codecs

# 3rd party packages
import xmlrunner

sys.path.append(os.path.abspath('../lotlan_scheduler'))

# local sources
from lotlan_scheduler.api.materialflow import MaterialFlow
from lotlan_scheduler.scheduler import LotlanScheduler

class TestScheduler(unittest.TestCase):
    """ Test Scheduler methods """
    def test_validate(self):
        scheduler = LotlanScheduler("")

        lotlan_file = codecs.open("etc/tests/Valid/HelloTask.tl", "r", encoding="utf8")
        valid_string = lotlan_file.read()
        try:
            scheduler.validate(valid_string)
        except ValueError:
            self.fail("Validate failed")
        lotlan_file.close()

        lotlan_file = codecs.open("etc/tests/Invalid/Syntax/CommaAfterLastParameter.tl",
                                  "r", encoding="utf8")
        invalid_syntax_string_ = lotlan_file.read()
        self.assertRaises(ValueError, scheduler.validate, invalid_syntax_string_)
        lotlan_file.close()

        lotlan_file = codecs.open("etc/tests/Invalid/Semantic/OnDoneAndRepeat.tl",
                                  "r", encoding="utf8")
        invalid_semantic_string = lotlan_file.read()
        self.assertRaises(ValueError, scheduler.validate, invalid_semantic_string)
        lotlan_file.close()

    def test_init_method(self):
        lotlan_file = codecs.open("etc/examples/Scheduling/001_simple_task.tl",
                                  "r", encoding="utf8")
        lotlan_with_one_mf = lotlan_file.read()

        scheduler = LotlanScheduler(lotlan_with_one_mf)
        material_flows = scheduler.get_materialflows()
        self.assertEqual(len(material_flows), 1)
        lotlan_file.close()

        lotlan_file = codecs.open("etc/examples/Scheduling/006_two_tasks.tl",
                                  "r", encoding="utf8")
        lotlan_with_two_mfs = lotlan_file.read()

        scheduler = LotlanScheduler(lotlan_with_two_mfs)
        material_flows = scheduler.get_materialflows()
        self.assertEqual(len(material_flows), 2)
        lotlan_file.close()


if __name__ == "__main__":
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output="test-reports"),
                  failfast=False, buffer=False, catchbreak=False)
