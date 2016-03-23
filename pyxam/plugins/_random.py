# Author: Eric Buss <ebuss@ualberta.ca> 2016
"""
# Plugin _random

This plugin is considered a core plugin (indicated by the underscore in its name) it should only be replaced or removed
if the user knows what they are doing.



This plugin allows the random seed to be set.
"""
import random
import options


# random config by ejrbuss: Set the seed for Python random
signature = 'random config', 'ejrbuss', 'Set the seed for Python random'


def load():
    """
    Adds the following [option](%/Modules/options.html):
     - `random -rnd` Set the seed for rng

    :return: plugin signature
    """
    # Set seed to option value
    if options.add_option('random', '-rng', 'Set the seed for rng', 0, int):
        random.seed(options.state.random())
    # Return signature
    return signature
