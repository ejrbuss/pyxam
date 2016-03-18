# Author: Eric Buss <ebuss@ualberta.ca> 2016
import random
import options


# Plugin signature
plugin = {
    'name': 'random config',
    'author': 'ejrbuss',
    'description': 'Sets seed for Python random'
}


def load():
    # Set seed to option value
    if options.add_option('random', '-rng', 'Set the seed for rng', 0, int):
        random.seed(options.state.random())
    # Return signature
    return plugin


def unload():
    pass
