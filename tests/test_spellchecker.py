"""Unit tests for spellchecker."""
import re
from pathlib import Path

import pytest

import spellchecker


TRUTH_FILE = 'truth.yaml'
FAIL_FILE = 'fail.yml'
DICT_FILE = 'dictionary.txt'
DIRECTORY = 'test_cases'


TRUTH_YAML = """Description: description.
Requirements: requirements id.
Steps: description and expected result for test steps.
"""

FAIL_YAML = """Decription: description.
Requirements: reqirements id.
Steps: description and expected result for test steps.
"""

DICTONARY = r'^req$'


@pytest.fixture(autouse=True)
def setup(tmpdir):
    """Setup for unit tests.

    :param py.local.path tmpdir: Fixture for path to temporary directory.
    """
    truth_file = tmpdir.join(TRUTH_FILE)
    truth_file.write(TRUTH_YAML)
    fail_file = tmpdir.join(FAIL_FILE)
    fail_file.write(FAIL_YAML)
    dictionary = tmpdir.join(DICT_FILE)
    dictionary.write(DICTONARY)
    subdir = tmpdir.mkdir(DIRECTORY)
    subdir.join('file1.yaml').write(TRUTH_YAML)
    subdir.join('file2.yml').write(FAIL_YAML)
    subdir.join('file3.txt').write(FAIL_YAML)


def test_truth_file(tmpdir):
    """Test for truth file.

    :param py.local.path tmpdir: Fixture for path to temporary directory.
    """
    file = str(tmpdir.join(TRUTH_FILE))
    dictionary = str(tmpdir.join(DICT_FILE))
    assert spellchecker.spell_check(file, dictionary) == 0


def test_fail_file(tmpdir):
    """Test for fail file.

    :param py.local.path tmpdir: Fixture for path to temporary directory.
    """
    file = str(tmpdir.join(FAIL_FILE))
    dictionary = str(tmpdir.join(DICT_FILE))
    assert spellchecker.spell_check(file, dictionary) == 2


def test_directory_with_tests(tmpdir):
    """Test spelling for directory with test cases.

    :param py.local.path tmpdir: Fixture for path to temporary directory.
    """
    directory = str(tmpdir.join(DIRECTORY))
    dictonary = str(tmpdir.join(DICT_FILE))
    assert spellchecker.spell_check(directory, dictonary) == 2


def test_speller_for_truth_file(tmpdir):
    """Test for speller function with truth file.

    :param py.local.path tmpdir: Fixture for path to temporary directory.
    """
    file = str(tmpdir.join(TRUTH_FILE))
    dictionary = re.compile(DICTONARY)
    assert spellchecker.spellchecker.speller(Path(file), dictionary) == 0


def test_speller_for_fail_file(tmpdir):
    """Test for speller function with fail file.

    :param py.local.path tmpdir: Fixture for path to temporary directory.
    """
    file = str(tmpdir.join(FAIL_FILE))
    dictionary = re.compile(DICTONARY)
    assert spellchecker.spellchecker.speller(Path(file), dictionary) == 2


def test_load_dictionary(tmpdir):
    """Test for load_dictionary function.

    :param py.local.path tmpdir: Fixture for path to temporary directory.
    """
    dictionary = str(tmpdir.join(DICT_FILE))
    assert spellchecker.spellchecker.load_dictionary(dictionary) == re.compile(DICTONARY)
