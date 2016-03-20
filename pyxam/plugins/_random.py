# Author: Eric Buss <ebuss@ualberta.ca> 2016
import random
import options


signature = 'random config', 'ejrbuss', 'Set the seed for Python random'


def load():
    # Set seed to option value
    if options.add_option('random', '-rng', 'Set the seed for rng', 0, int):
        random.seed(options.state.random())
    # Return signature
    return signature


def unload():
    pass
