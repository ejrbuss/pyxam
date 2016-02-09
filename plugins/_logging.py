import logging
from options import state
from options import add_option


plugin = {
        'name': 'logging config',
        'author': 'ejrbuss',
        'description': 'The default logging configuration for pyxam'
    }
description = 'Set the logging level for pyxam\n{}: DEBUG\n{}: INFO\n{}: WARNING\n{}: CRITICAL'.format(
    logging.DEBUG, logging.INFO, logging.WARNING, logging.CRITICAL
)


def load():
    add_option('logging', '-l', description, logging.DEBUG, int)
    logging.basicConfig(format='%(levelname)s@%(module)s.%(funcName)s(): %(message)s', level=state.logging())
    logging.info('Logging configured with level {}'.format(logging.getLevelName(state.logging())))
    return plugin


def unload():
    pass
