#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test the output of the stratgy.
"""

import unittest
import os
import filecmp

from trade import Feed, max_vals
from strategies.sma.strategy import SMAStrategy

TEST_DIR = os.path.dirname(os.path.realpath(__file__))


class TestOutput(unittest.TestCase):
    """Test the output is correct."""

    def setUp(self):
        # Create output dir and file
        try:
            output_dir = os.path.join(TEST_DIR, "outputs")
            os.makedirs(output_dir)
        except FileExistsError:
            # No problem if dir exists
            pass
        self.__output_dir = output_dir

    def test_backtest(self):
        """Test the expected backtest output is found."""
        # Outpus
        output_file = os.path.join(self.__output_dir, "backtest.txt")

        # Inputs
        input_file = os.path.join(TEST_DIR, "inputs", "orcl_2000.jsonl.gz")

        # Expected
        expected_file = os.path.join(TEST_DIR, "expected_outputs",
                                     "backtest.txt")

        feed = Feed(input_file)
        strategy = SMAStrategy(feed, 20, 1000, silent=True,
                               files=[output_file])
        strategy.run()

        # Check total value
        self.assertEqual("{:.2f}".format(strategy.total_value), "1081.25")

        # Check file contents
        self.assertTrue(
            filecmp.cmp(output_file, expected_file),
            "{} and {} are not equal.".format(output_file, expected_file))

    def test_ideal_vals(self):
        """Test the expected ideal window size is found."""
        # Inputs
        input_file = os.path.join(TEST_DIR, "inputs", "orcl_2000.jsonl.gz")

        max_val, max_val_args = max_vals(
            SMAStrategy, [input_file], range(10, 31), 1000, silent=True)
        return
        self.assertEqual(str(max_val), "1106.875")
        self.assertEqual(max_val_args, ((22, 1000), {'silent': True}))


if __name__ == "__main__":
    unittest.main()

