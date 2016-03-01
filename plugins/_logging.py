# Author: Eric Buss <ebuss@ualberta.ca> 2016
import logging
import options


# Plugin signature
plugin = {
        'name': 'logging config',
        'author': 'ejrbuss',
        'description': 'The default logging configuration for pyxam'
}
# Logging option description
description = 'Set the logging level for pyxam\n{}: DEBUG\n{}: INFO\n{}: WARNING\n{}: CRITICAL'.format(
    logging.DEBUG, logging.INFO, logging.WARNING, logging.CRITICAL
)


def load():
    # Add logging option
    options.add_option('logging', '-l', description, logging.DEBUG, int)
    # Set logging configuration
    logging.basicConfig(format='%(levelname)s@%(module)s.%(funcName)s(): %(message)s', level=options.state.logging())
    # Log configuration
    logging.info('Logging configured with level {}'.format(logging.getLevelName(options.state.logging())))
    # Return signature
    return plugin


def unload():
    pass
