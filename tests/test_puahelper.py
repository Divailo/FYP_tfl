import unittest
import puahelper  # class to be tested
import os.path  # to get path of the file being tested


class PuaHelperTest(unittest.TestCase):
    # Tests for unbreakable loops
    # The provided file to test with contains absolutely no content
    # Should return empty objects or error codes (-1)

    def test_readandmap_for_unbreakable_loop1(self):
        _filepath = os.path.abspath('emptyfile.pua')
        mapped_objects = puahelper.read_and_map_signalgroups_from_pua(_filepath)
        self.assertEqual(mapped_objects, {})

    def test_getstages_for_unbreakable_loop1(self):
        _filepath = os.path.abspath('emptyfile.pua')
        phases_in_stages = puahelper.get_phases_in_stages_from_pua(_filepath)
        self.assertEqual(phases_in_stages, {})

    def test_getstartingstage_for_unbreakable_loop1(self):
        _filepath = os.path.abspath('emptyfile.pua')
        starting_stage = puahelper.get_starting_stage_from_pua(_filepath)
        self.assertEqual(starting_stage, -1)

    #

    # Tests for unbreakable loops again
    # This time tests work with files that have the keys required of each scrappable section
    # but no key to show where the actual content starts
    # Should return empty objects or error codes (-1)

    def test_readandmap_for_unbreakable_loop2(self):
        _filepath = os.path.abspath('halfemptyfile.pua')
        mapped_objects = puahelper.read_and_map_signalgroups_from_pua(_filepath)
        self.assertEqual(mapped_objects, {})

    def test_getstages_for_unbreakable_loop2(self):
        _filepath = os.path.abspath('halfemptyfile.pua')
        phases_in_stages = puahelper.get_phases_in_stages_from_pua(_filepath)
        self.assertEqual(phases_in_stages, {})

    def test_getstartingstage_for_unbreakable_loop2(self):
        _filepath = os.path.abspath('halfemptyfile.pua')
        starting_stage = puahelper.get_starting_stage_from_pua(_filepath)
        self.assertEqual(starting_stage, -1)

    #

    # Tests if the functions return no content
    # on a file that is correctly formatted but has no actual content

    def test_readandmap_nocontent(self):
        _filepath = os.path.abspath('emptycontentpuafile.pua')
        mapped_objects = puahelper.read_and_map_signalgroups_from_pua(_filepath)
        self.assertEqual(mapped_objects, {})

    def test_getstages_nocontent(self):
        _filepath = os.path.abspath('emptycontentpuafile.pua')
        phases_in_stages = puahelper.get_phases_in_stages_from_pua(_filepath)
        self.assertEqual(phases_in_stages, {})

    def test_getstartingstage_nocontent(self):
        _filepath = os.path.abspath('emptycontentpuafile.pua')
        starting_stage = puahelper.get_starting_stage_from_pua(_filepath)
        self.assertEqual(starting_stage, -1)

    #

    # Tests if the functions return no content when the data is in a comments section

    def test_readandmap_commented_nocontent(self):
        _filepath = os.path.abspath('commented_badpuafile.pua')
        mapped_objects = puahelper.read_and_map_signalgroups_from_pua(_filepath)
        self.assertEqual(mapped_objects, {})

    def test_getstages_commented_nocontent(self):
        _filepath = os.path.abspath('commented_badpuafile.pua')
        phases_in_stages = puahelper.get_phases_in_stages_from_pua(_filepath)
        self.assertEqual(phases_in_stages, {})

    def test_getstartingstage_commented_nocontent(self):
        _filepath = os.path.abspath('commented_badpuafile.pua')
        starting_stage = puahelper.get_starting_stage_from_pua(_filepath)
        self.assertEqual(starting_stage, -1)

    #

    # Tests if the functions return the correct content on double (first in comments, then actual good content)
    # Expected results
    # 3 signal groups: A->1; B->2; C->3;
    # 3 stages: 1->A; 2->B; 3->C
    # Startgin Stage = 1

    def test_readandmap_commented_goodfile(self):
        _filepath = os.path.abspath('commented_goodpuafile.pua')
        mapped_objects = puahelper.read_and_map_signalgroups_from_pua(_filepath)
        self.assertEqual(len(mapped_objects), 3)
        self.assertEqual(mapped_objects['1'], 'A')
        self.assertEqual(mapped_objects['2'], 'B')
        self.assertEqual(mapped_objects['3'], 'C')

    def test_getstages_commented_goodfile(self):
        _filepath = os.path.abspath('commented_goodpuafile.pua')
        phases_in_stages = puahelper.get_phases_in_stages_from_pua(_filepath)
        self.assertEqual(len(phases_in_stages), 3)
        self.assertEqual(phases_in_stages['A'], [1])
        self.assertEqual(phases_in_stages['B'], [2])
        self.assertEqual(phases_in_stages['C'], [3])

    def test_getstartingstage_commented_goodfile(self):
        _filepath = os.path.abspath('commented_goodpuafile.pua')
        starting_stage = puahelper.get_starting_stage_from_pua(_filepath)
        self.assertEqual(starting_stage, 1)

    #

    # Tests the functions to return correct values
    # On a file that is correctly formatted and has valid content
    # The content is separated by TABS
    # 3 signal groups: A->1; B->2; C->3;
    # 3 stages: 1->A; 2->B; 3->C
    # Startgin Stage = 1

    def test_readandmap_correctvalues_tabs(self):
        _filepath = os.path.abspath('goodpuafile.pua')
        mapped_objects = puahelper.read_and_map_signalgroups_from_pua(_filepath)
        self.assertEqual(len(mapped_objects), 3)
        self.assertEqual(mapped_objects['1'], 'A')
        self.assertEqual(mapped_objects['2'], 'B')
        self.assertEqual(mapped_objects['3'], 'C')

    def test_getstages_correctvalues_tabs(self):
        _filepath = os.path.abspath('goodpuafile.pua')
        phases_in_stages = puahelper.get_phases_in_stages_from_pua(_filepath)
        self.assertEqual(len(phases_in_stages), 3)
        self.assertEqual(phases_in_stages['A'], [1, 3])
        self.assertEqual(phases_in_stages['B'], [2])
        self.assertEqual(phases_in_stages['C'], [3])

    def test_getstartingstage_correctvalues_tabs(self):
        _filepath = os.path.abspath('goodpuafile.pua')
        starting_stage = puahelper.get_starting_stage_from_pua(_filepath)
        self.assertEqual(starting_stage, 1)

    #

    # Tests the functions to return correct values
    # On a file that is correctly formatted and has valid content
    # The content is separated by SPACES
    # 2 signal groups: V1->1; P2->2;
    # 2 stages: 1->V1; 2->P2
    # Startgin Stage = 1

    def test_readandmap_correctvalues_lines(self):
        _filepath = os.path.abspath('pelican.pua')
        mapped_objects = puahelper.read_and_map_signalgroups_from_pua(_filepath)
        self.assertEqual(len(mapped_objects), 2)
        self.assertEqual(mapped_objects['1'], 'V1')
        self.assertEqual(mapped_objects['2'], 'P2')

    def test_getstages_correctvalues_lines(self):
        _filepath = os.path.abspath('pelican.pua')
        phases_in_stages = puahelper.get_phases_in_stages_from_pua(_filepath)
        self.assertEqual(len(phases_in_stages), 2)
        self.assertEqual(phases_in_stages['V1'], [1])
        self.assertEqual(phases_in_stages['P2'], [2])

    def test_getstartingstage_correctvalues_lines(self):
        _filepath = os.path.abspath('pelican.pua')
        starting_stage = puahelper.get_starting_stage_from_pua(_filepath)
        self.assertEqual(starting_stage, 1)

    #

if __name__ == '__main__':
    unittest.main()
