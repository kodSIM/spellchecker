"""Unit tests for spellchecker."""
import re
from pathlib import Path

import pytest

import spellchecker


TRUTH_FILE = """Description: description.
Requirements: requirements id.
Steps: description and expected result for test steps.
"""

FAIL_FILE = """Decription: description.
Requirements: reqirements id.
Steps: description and expected result for test steps.
"""

DICTONARY = r'^req$'


def create_dictionary(tmpdir):
    file = tmpdir.join('dictionary.txt')
    file.write(DICTONARY)
    return str(file)


def create_truth_file(tmpdir):
    file = tmpdir.join('file.yml')
    file.write(TRUTH_FILE)
    return str(file)


def create_fail_file(tmpdir):
    file = tmpdir.join('file.yml')
    file.write(FAIL_FILE)
    return str(file)


def test_truth_file(tmpdir):
    file = create_truth_file(tmpdir)
    dictionary = create_dictionary(tmpdir)
    assert spellchecker.spell_check(file, dictionary) == 0


def test_fail_file(tmpdir):
    file = create_fail_file(tmpdir)
    dictionary = create_dictionary(tmpdir)
    assert spellchecker.spell_check(file, dictionary) == 2


def test_speller_for_truth_file(tmpdir):
    file = create_truth_file(tmpdir)
    dictionary = create_dictionary(tmpdir)
    assert spellchecker.spellchecker.speller(Path(file), dictionary) == 0


def test_load_dictionary(tmpdir):
    dictionary = create_dictionary(tmpdir)
    assert spellchecker.spellchecker.load_dictionary(dictionary) == re.compile(r'^req$')
