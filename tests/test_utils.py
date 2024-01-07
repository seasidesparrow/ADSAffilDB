import json
import os
import unittest

from adsaffildb import utils

# from unittest.mock import patch


class TestUtils(unittest.TestCase):
    def setUp(self):
        stubdata_dir = os.path.join(os.path.dirname(__file__), "stubdata/")
        self.inputdir = os.path.join(stubdata_dir, "input")
        self.outputdir = os.path.join(stubdata_dir, "output")
        self.maxDiff = None

    def test_read_parent_child(self):
        # get input data
        infile = os.path.join(self.inputdir, "test_parent_child.dat")
        test_data = utils.read_affid_dict(infile)

        # get expected data
        expected_data = os.path.join(self.outputdir, "test_parent_child.json")
        with open(expected_data, "r") as fj:
            expected_data = json.load(fj)

        self.assertEqual(test_data, expected_data)

        # non-existent file will raise an exception
        with self.assertRaises(utils.AffIdDictException):
            utils.read_affid_dict("/non_existent_file")

    def test_read_match_dict(self):
        # Valid file: matched id, a tab, and the affiliation string
        # get input data
        infile = os.path.join(self.inputdir, "test_good_match.dat")
        test_data = utils.read_match_dict(infile)

        # get expected data
        expected_data = os.path.join(self.outputdir, "test_good_match.json")
        with open(expected_data, "r") as fj:
            expected_data = json.load(fj)

        self.assertEqual(test_data, expected_data)

        # non-existent file will raise an exception
        with self.assertRaises(utils.MatchDictException):
            utils.read_match_dict("/another_non_existent_file")


#    @patch('utils.logger')
#    def test_read_invalid_match_file(self, mock_logger):
#        # Invalid file: matched id, two blank spaces, and the affil string
#        bad_infile = os.path.join(self.inputdir, "test_bad_match.dat")
#        test_data = utils.read_match_dict(bad_infile)
#        print(test_data)
#        print(mock_logger)
#        mock_logger.assert_called_once()
