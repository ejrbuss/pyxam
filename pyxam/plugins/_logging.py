# Author: Eric Buss <ebuss@ualberta.ca> 2016
import logging
import options

signature = 'logging config', 'ejrbuss', 'The default logging configuration for pyxam'

# Logging option description
description = 'Set the logging level for pyxam\n{}: DEBUG\n{}: INFO\n{}: WARNING\n{}: CRITICAL'.format(
    logging.DEBUG, logging.INFO, logging.WARNING, logging.CRITICAL
)

# Default logging level
DEFAULT = logging.DEBUG

def load():
    """
    Sets the logging the logging configuration for Pyxam
    :return:
    """
    options.add_option('logging', '-l', description, DEFAULT, int)
    # Set logging configuration
    logging.basicConfig(format='%(levelname)s@%(module)s.%(funcName)s(): %(message)s', level=options.state.logging())
    # Log configuration
    logging.info('Logging configured with level {}'.format(logging.getLevelName(options.state.logging())))
    # Return signature
    return signature


def unload():
    pass
