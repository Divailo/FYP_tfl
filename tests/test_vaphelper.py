import unittest
import vaphelper  # class to be tested
import os.path  # to get path of the file being tested


class VapHelperTest(unittest.TestCase):

    # Tests the vaphelper functions when handling empty files
    # Should return error codes : -1 or empty objects/arrays
    def test_no_cyclelength_provided(self):
        _filepath = os.path.abspath('emptyfile.vap')
        cycle_length = vaphelper.get_cycle_length_from_vap(_filepath)
        self.assertEqual(cycle_length, -1)

    def test_no_plans_provided(self):
        _filepath = os.path.abspath('emptyfile.vap')
        plans = vaphelper.get_stage_lenghts_from_vap(_filepath, 3)
        # len(cycl
        self.assertEqual(len(plans), 0)
        self.assertEqual(plans, [])

    #

    # Tests the vaphelper functions when handling files with the desired keys but no values provided
    # Should return error codes : -1 or empty object/arrays
    def test_no_value_for_cyclelength(self):
        _filepath = os.path.abspath('vap_with_keys_no_values.vap')
        cycle_length = vaphelper.get_cycle_length_from_vap(_filepath)
        self.assertEqual(cycle_length, -1)

    def test_no_value_for_plans(self):
        _filepath = os.path.abspath('vap_with_keys_no_values.vap')
        plans = vaphelper.get_stage_lenghts_from_vap(_filepath, 3)
        self.assertEqual(len(plans), 0)
        self.assertEqual(plans, [])

    #

    # Tests the vaphelper functions when the file has data keys and values, but are not inside the required sections
    # That's why nothing should be returned
    # Should return error codes : -1 or empty objects/arrays
    def test_cyclelength_no_content_with_comments(self):
        _filepath = os.path.abspath('vap_with_keys_values_no_section.vap')
        cycle_length = vaphelper.get_cycle_length_from_vap(_filepath)
        self.assertEqual(cycle_length, -1)

    def test_plans_correct_no_content_with_comments(self):
        _filepath = os.path.abspath('vap_with_keys_values_no_section.vap')
        plans = vaphelper.get_stage_lenghts_from_vap(_filepath, 3)
        self.assertEqual(len(plans), 0)
        self.assertEqual(plans, [])

    #

    # Tests the vaphelper functions when the file has the data required, but it is commented out
    # Should return error codes : -1 or empty objects/arrays
    def test_cyclelength_commented_nocontent(self):
        _filepath = os.path.abspath('commented_badvapfile.vap')
        cycle_length = vaphelper.get_cycle_length_from_vap(_filepath)
        self.assertEqual(cycle_length, -1)

    def test_plans_commented_nocontent(self):
        _filepath = os.path.abspath('commented_badvapfile.vap')
        plans = vaphelper.get_stage_lenghts_from_vap(_filepath, 3)
        self.assertEqual(len(plans), 0)
        self.assertEqual(plans, [])

    #

    # Tests the vaphelper functions when the file has double of the data required, one commented, one not
    # In the specific test the values that have to be returned are:
    # CycleLength = 40
    # Plans = [4, 16, 28]
    def test_cyclelength_correct_with_comments(self):
        _filepath = os.path.abspath('commented_goodvapfile.vap')
        cycle_length = vaphelper.get_cycle_length_from_vap(_filepath)
        self.assertEqual(cycle_length, 40)

    def test__plans_correct_with_comments(self):
        _filepath = os.path.abspath('commented_goodvapfile.vap')
        max_stage = 3
        plans = vaphelper.get_stage_lenghts_from_vap(_filepath, max_stage)
        self.assertEqual(len(plans), max_stage)
        self.assertEqual(plans, [4,16,28])

    #

    # Tests the vaphelper functions when the desired data is between comment sections
    # In the specific test the values that have to be returned are:
    # CycleLength = 72
    # Plans = [9, 24, 56]
    def test_cyclelength_correct_documented(self):
        _filepath = os.path.abspath('goodvapfile_documented.vap')
        cycle_length = vaphelper.get_cycle_length_from_vap(_filepath)
        self.assertEqual(cycle_length, 72)

    def test__plans_correct_documented(self):
        _filepath = os.path.abspath('goodvapfile_documented.vap')
        max_stages = 3
        plans = vaphelper.get_stage_lenghts_from_vap(_filepath, max_stages)
        self.assertEqual(len(plans), max_stages)
        self.assertEqual(plans, [9,24,56])

    #

    # Tests the vaphelper functions when handling correctly structured files
    # In the specific test the values that have to be returned are:
    # CycleLength = 72
    # Plans = [9, 24, 56]
    def test_cyclelength_correct(self):
        _filepath = os.path.abspath('goodvapfile.vap')
        cycle_length = vaphelper.get_cycle_length_from_vap(_filepath)
        self.assertEqual(cycle_length, 72)

    def test_plans_correct(self):
        _filepath = os.path.abspath('goodvapfile.vap')
        max_stages = 3
        plans = vaphelper.get_stage_lenghts_from_vap(_filepath, max_stages)
        self.assertEqual(len(plans), max_stages)
        self.assertEqual(plans, [9,24,56])

    #

if __name__ == '__main__':
    unittest.main()
