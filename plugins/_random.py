from random import seed
from options import add_option

plugin = {
    'name': 'random config',
    'author': 'ejrbuss',
    'description': 'Sets seed for Python random'
}


def load():
    seed(add_option('random', '-rng', 'Set the seed for rng', 1234, int))
    return plugin


def unload():
    pass
