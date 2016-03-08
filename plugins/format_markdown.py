# Author: Eric Buss <ebuss@ualberta.ca> 2016
import formatter
import collections
import filters


# Plugin signature
plugin = {
    'name': 'markdown format',
    'author': 'ejrbuss',
    'description': 'Format for viewing files in markdown'
}


def load():
    formatter.add_format({
        'extensions': ['md', 'md'],
        'description': plugin['description'],
        # Assign processors
        'parser_preprocessor': filters.pass_through,
        'parser_postprocessor': filters.pass_through,
        'composer_preprocessor': filters.pass_through,
        'composer_postprocessor': filters.pass_through,
        # Use an OrderedDict to preserve token order
        'format': collections.OrderedDict([
            ('comment', ['<!--', (), '-->', '.']),
            ('$', ['<span class="$"><i>', (), '</i></span>', '.']),
            ('title', ['<br /><b>', (), '</b><br />', '.']),
            ('img', ['<img alt="Embedded Image" src="data:image/png;base64,', (), '">', '.']),
            ('choice', ['<br /> __ ', (), '<br />', '.']),
            ('correctchoice', ['<br /> __ ', (), '<br />', '.']),
            ('verbatim', ['<p style="font-family:monospace;padding:1em"><b>', (), '</b></p>', '.']),
            ('true', [' __ True', '.']),
            ('false', [' __ False', '.']),
        ])
    })
    # Return signature
    return plugin


def unload():
    pass



