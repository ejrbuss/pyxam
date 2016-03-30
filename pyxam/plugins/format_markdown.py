# Author: Eric Buss <ebuss@ualberta.ca> 2016
import formatter
import collections
import filters


signature = 'markdown format', 'ejrbuss', 'Format for producing and viewing files in markdown'


def load():
    formatter.add_format(
        name='markdown',
        extensions=['md'],
        description=signature[2],
        # Use an OrderedDict to preserve token order
        format=collections.OrderedDict([
            ('h3', ['###', (), '\n']),
            ('h2', ['##', (), '\n']),
            ('h1', ['#', (), '\n']),
            ('listitem', [' - ', (), '\n']),
            ('hr', ['***', '\s']),
            ('emphasis3', ['***', (), '***', '.']),
            ('emphasis2', ['**', (), '**', '.']),
            ('emphasis1', ['*', (), '*', '.']),
            ('verbython', ['```python', (), '```', '.']),
            ('verbblock', ['```', (), '```', '.']),
            ('verbexpr', ['`', (), '`', '.'])
        ])
    )
    # Return signature
    return signature


def unload():
    pass



