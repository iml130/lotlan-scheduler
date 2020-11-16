import sys
import os
sys.path.append(os.path.abspath('../lotlan_schedular'))

from lotlan_schedular.api.materialflow import MaterialFlow
from lotlan_schedular.schedular import LotlanSchedular

import unittest
import codecs
import xmlrunner

class TestSchedular(unittest.TestCase):
    def test_validate(self):
        valid_string = codecs.open("etc/tests/Valid/HelloTask.tl", "r", encoding='utf8').read()
        invalid_syntax_string_ = codecs.open("etc/tests/Invalid/Syntax/CommaAfterLastParameter.tl", "r", encoding='utf8').read()
        invalid_semantic_string = codecs.open("etc/tests/Invalid/Semantic/OnDoneAndRepeat.tl", "r", encoding='utf8').read()

        schedular = LotlanSchedular("")
        try:
            schedular.validate(valid_string)
        except Exception:
            self.fail("Validate failed")

        self.assertRaises(ValueError, schedular.validate, invalid_syntax_string_)
        self.assertRaises(ValueError, schedular.validate, invalid_semantic_string)

    def test_init_method(self):
        lotlan_with_one_mf = codecs.open("etc/examples/Scheduling/001_simple_task.tl", "r", encoding='utf8').read()
        lotlan_with_two_mfs = codecs.open("etc/examples/Scheduling/006_two_tasks.tl", "r", encoding='utf8').read()

        schedular = LotlanSchedular(lotlan_with_one_mf)
        material_flows = schedular.get_materialflows()
        self.assertEqual(len(material_flows), 1)

        schedular = LotlanSchedular(lotlan_with_two_mfs)
        material_flows = schedular.get_materialflows()
        self.assertEqual(len(material_flows), 2)


if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'), failfast=False, buffer=False, catchbreak=False)
