from pkg_resources import resource_string
import json
import random

config = json.loads(resource_string(__name__, 'config.json'))
n_items = len(config['media_files'])
question = config.get('question', 'Does it look natural?')
buttons = config.get('buttons', ['Yes', 'No'])


def get_media_path(idx):
    """
    Get the media file path at idx.
    The path is a concatenated string so,
    can be composed of urls or WHY.,
    not necessarily from the file system.
    """
    return '{}{}'.format(config['media_directory'],
                         config['media_files'][idx])


def get_media(idx):
    """
    Get the media file name at idx.
    Not the full path but useful as a key.
    """
    return config['media_files'][idx]


def get_shuffled_idx():
    items = range(n_items)
    random.seed()  # seed from time
    random.shuffle(items)
    return items


def question_prog(idx):
    """
    String of question and progress
    Indexed from one for friendly output.
    """
    msg = '{} ({} of {})'
    return msg.format(question, idx + 1, n_items)


print get_media(1)
print get_shuffled_idx()
