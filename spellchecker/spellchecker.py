"""Module for execute spell checking."""
import os
import os.path
import re
import sys

import click
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords


STOP_WORDS = set(stopwords.words('english'))
PUNKT = {',', '.', ':', "'", '-', '>', '+', '', '|', '(', ')', '<'}
STARTS_ENDS = r'^[\.,\'*`]*|[\.,\'*`]*$'
REPLACE = r'[\.\-_]'


@click.command()
@click.argument('path', type=click.Path(exists=True))
@click.argument('dict_path', type=click.Path(exists=True, dir_okay=False))
def cli(path, dict_path):
    """Command-line interface for YAMLchecker."""
    sys.exit(spell_check(path, dict_path))


def spell_check(path, dict_path):
    """Read all yaml files in the directory and verify spell.

    :param str path: Path to test cases.
    :param str dict_path: Path to dictionary.

    :return: Number of errors.
    :rtype: int
    """
    if os.path.isdir(path):
        file_list = os.listdir(path)
        file_list = filter(lambda x: x.endswith(('.yaml', '.yml')), file_list)
    else:
        file_list = [path]
    dictionary = load_dictionary(dict_path)
    error_count = 0
    for file_name in file_list:
        if os.path.isdir(path):
            full_path = os.path.join(path, file_name)
        else:
            full_path = file_name
        error_count += speller(full_path, dictionary)
    return error_count


def speller(file_path, dictionary):
    """Spell checker for text.

    :param str file_path: Path to file.
    :param str dictionary: Dictionary.

    :return: Number of errors.
    :rtype: int
    """
    with open(file_path) as file:
        text = file.read()
    error_count = 0
    for s_count, s in enumerate(text.split('\n'), 1):
        for word in nltk.word_tokenize(s.replace('/', ' ')):
            word = word.strip()
            word = re.sub(STARTS_ENDS, '', word)
            prep_word = word.lower()
            if not wn.synsets(prep_word) and prep_word:
                if (prep_word in STOP_WORDS) or (prep_word in PUNKT) or re.search(dictionary, prep_word)\
                        or re.sub(REPLACE, '', prep_word).isdigit():
                    continue
                else:
                    print(f'{file_path}:{s_count}: Word "{word}" is missing')
                    error_count += 1
    return error_count


def load_dictionary(path):
    """Load dictionary.

    :param str path: Path to dictionary.

    :return: Dictionary.
    :rtype: str
    """
    with open(path) as file:
        text = file.read()
    return text.replace('\n', '|')


if __name__ == '__main__':
    cli()
