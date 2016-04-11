# Author: Eric Buss <ebuss@ualberta.ca> 2016
import parser_composer
import collections


signature = 'org mode format', 'ejrbuss', 'Format for producing and viewing org mode files'


def load():

    parser_composer.add_format(
        name='orghtml',
        extensions=['orghtml'],
        description=signature[2],
        format=collections.OrderedDict([
            ('h3', ['***', (), '\n']),
            ('h2', ['**', (), '\n']),
            ('h1', ['*', (), '\n']),
            ('listitem', ['- ', (), '(- )|\*']),
            ('verblock', ['```', (), '```', '.']),
            ('hr', ['-----', '.']),
            ('emphasis2', ['``', (), '``', '.']),
            ('emphasis1', ['`', (), '`', '.']),
            ('verbexpr', ['~', (), '~', '.']),
            ('newline', ['<br />', '.'])
        ])
    )
    return signature

# TODO finish