import unittest
import pddlhelper
import os.path

class PddlHelperTestCase(unittest.TestCase):
    def test_badfile(self):
        _filepath = os.path.join(os.path.dirname(__file__), 'sample_pddl.txt')
        new_timing = pddlhelper.get_new_stages_information(_filepath)
        self.assertEqual(
            new_timing, {})

    def test_goodfile(self):
        _filepath = os.path.join(os.path.dirname(__file__), 'plan_example.pddl')
        new_timing = pddlhelper.get_new_stages_information(_filepath)
        self.assertEqual(
            new_timing, {'junction_G': ['35', '40', '45', '80'],
                         'junction_E': ['35', '45', '80']})


if __name__ == '__main__':
    unittest.main()
