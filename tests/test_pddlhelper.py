import unittest
import pddlhelper
import os.path


class PddlToVissimTestCase(unittest.TestCase):
    def test_badfile(self):
        _filepath = os.path.join(os.path.dirname(__file__), 'bad_sample_pddl.pddl')
        new_timing = pddlhelper.get_new_stages_information(_filepath)
        self.assertEqual(
            new_timing, {})

    def test_goodfile(self):
        _filepath = os.path.join(os.path.dirname(__file__), 'plan_example.pddl')
        new_timing = pddlhelper.get_new_stages_information(_filepath)
        self.assertEqual(
            new_timing, {'junction_G': ['35', '40', '45', '80'],
                         'junction_E': ['35', '45', '80']})


class JsonToPddlTestCase(unittest.TestCase):
    def test_create_junction_section(self):
        create_section = pddlhelper._create_signal_controller_section("Junction_A")
        self.assertEqual(create_section, ';; Junction_A\n')

    def test_current_stage(self):
        curr_stage = pddlhelper._make_current_stage_line(1, "Junction_A")
        self.assertEqual(curr_stage, '\t(= (current_stage Junction_A) 10)\n')

    def test_max_stage(self):
        max_stage = pddlhelper._make_max_stage_line(3, "Junction_A")
        self.assertEqual(max_stage, '\t(= (max_stage Junction_A) 30)\n')

    def test_phases_in_stages(self):
        map_to_test = {'l_1': [1], 'l_2': [2]}
        phases_in_stages = pddlhelper._make_phase_in_stage_lines(map_to_test, "Junction_A")
        self.assertEqual(phases_in_stages,
                         '\t(= (phase_in_stage l_2 Junction_A) 20)\n\t(= (phase_in_stage l_1 Junction_A) 10)\n')

    def test_sample_json(self):
        _filepath = os.path.join(os.path.dirname(__file__), 'sample_json.txt')
        lines = pddlhelper._generate_pddl_lines(_filepath)
        self.assertEqual(lines, [u';; Junction_A\n',
                                 u'\t(= (current_stage Junction_A) 10)\n',
                                 u'\t(= (max_stage Junction_A) 30)\n',
                                 u'\t(= (phase_in_stage l_2 Junction_A) 10)\n'
                                 u'\t(= (phase_in_stage l_3 Junction_A) 20)\n'
                                 u'\t(= (phase_in_stage l_1 Junction_A) 10)\n'
                                 u'\t(= (phase_in_stage l_4 Junction_A) 20)\n'])

    def test_error_current_stage(self):
        curr_stage = pddlhelper._make_current_stage_line(-1, "Junction_A")
        self.assertEqual(curr_stage, '\t' + pddlhelper.START_COMMENT_KEY + ' NO INFROMATION FOR '
                         + pddlhelper.CURR_STAGE_KEY + 'Junction_A' + '\n')

    def test_error_max_stage(self):
        max_stage = pddlhelper._make_max_stage_line(-1, "Junction_A")
        self.assertEqual(max_stage, '\t' + pddlhelper.START_COMMENT_KEY + ' NO INFROMATION FOR '
                         + pddlhelper.MAX_STAGE_KEY + 'Junction_A' + '\n')

    def test_error_phases_in_stages(self):
        map_to_test = {}
        phases_in_stages = pddlhelper._make_phase_in_stage_lines(map_to_test, "Junction_A")
        self.assertEqual(phases_in_stages, '\t' + pddlhelper.START_COMMENT_KEY + ' NO INFROMATION FOR '
                         + pddlhelper.PHASE_IN_STAGE_KEY + 'Junction_A' + '\n')


if __name__ == '__main__':
    unittest.main()
