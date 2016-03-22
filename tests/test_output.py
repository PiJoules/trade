#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test suite for checking strategy results.
"""

import unittest
import os
import subprocess

TEST_DIR = os.path.dirname(os.path.realpath(__file__))


class BaseTestCases:
    """Namespace for base test case classes."""

    class TestOutput(unittest.TestCase):
        """Base unit test class."""

        ARGS = ""

        def setUp(self):
            """Attempt to make the outputs dir first."""
            try:
                os.makedirs(os.path.join(TEST_DIR, "outputs"))
            except FileExistsError:
                # No problem if dir exists
                pass

        def test_output(self):
            """Test the expected output is found."""
            input_file = os.path.join(TEST_DIR, "inputs", self.INPUT)
            output_file = os.path.join(TEST_DIR, "outputs",
                                       self.__class__.__name__ + ".txt")
            script = os.path.join(TEST_DIR, "strategies", self.STRATEGY)
            cmd = "python {} {} {} > {}".format(
                script, input_file, self.ARGS, output_file)
            expected_output = os.path.join(TEST_DIR, "expected_outputs",
                                           self.EXPECTED)
            result = subprocess.check_call(cmd, shell=True)

            # Make sure command called successfully
            self.assertEqual(result, 0)

            # Compare file contents
            with open(output_file, "r") as output:
                with open(expected_output, "r") as expected:
                    for line in output:
                        line2 = expected.readline()
                        self.assertEqual(line, line2)


#####################################################
# Tests for sample strategies below to test outputs
#
# Tests are made by essentially calling the script containing
# the strategy from the command line.
# Properties:
#     INPUT (str): Input file(s) for the script.
#     STRATEGY (str): Script name under tests/strategies/ dir
#     EXPECTED (str): Expected output file under tests/expected_outputs/
#####################################################


class TestSimple(BaseTestCases.TestOutput):
    """Test case for simple output."""

    INPUT = "orcl_2000.jsonl.gz"
    STRATEGY = "simple.py"
    EXPECTED = "simple.txt"


class TestSMA(BaseTestCases.TestOutput):
    """Test case for sma output."""

    INPUT = "orcl_2000.jsonl.gz"
    STRATEGY = "sma.py"
    EXPECTED = "sma.txt"


class TestRSI(BaseTestCases.TestOutput):
    """Test case for rsi output."""

    INPUT = "orcl_2000.jsonl.gz"
    STRATEGY = "rsi.py"
    EXPECTED = "rsi.txt"


class TestSMAStrategy(BaseTestCases.TestOutput):
    """Test case for rsi output."""

    INPUT = "orcl_2000.jsonl.gz"
    STRATEGY = "smastrategy.py"
    EXPECTED = "smastrategy.txt"


if __name__ == "__main__":
    unittest.main()

