# Author: Eric Buss <ebuss@ualberta.ca> 2016
"""
# Plugin format_markdown

A small plugin for exporting markdown to HTML. This plugin does not support exams written in markdown.
"""
import parser_composer
import collections


signature = 'markdown format', 'ejrbuss', 'Format for producing and viewing files in markdown'


def load():
    """
    Loads the markdown format.
    """
    parser_composer.add_format(
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
    return signature

