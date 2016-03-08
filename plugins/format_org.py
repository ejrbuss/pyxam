# Author: Eric Buss <ebuss@ualberta.ca> 2016
import formatter
import collections
import filters


# Plugin signature
plugin = {
    'name': 'org mode format',
    'author': 'ejrbuss',
    'description': 'Format for viewing files in org mode'
}


def composer_preprocessor(intermediate):
    intermediate.ast = filters.promote(intermediate.ast, 'questions')
    return intermediate


def load():
    formatter.add_format({
        'extensions': ['org', 'org'],
        'description': plugin['description'],
        # Assign processors
        'parser_preprocessor': filters.pass_through,
        'parser_postprocessor': filters.pass_through,
        'composer_preprocessor': composer_preprocessor,
        'composer_postprocessor': filters.pass_through,
        # Use an OrderedDict to preserve token order
        'format': collections.OrderedDict([
            ('comment', ['#', (), '\n']),
            ('commentblock', ['#+BEGIN_COMMENT ', (), '#+END_COMMENT']),
            ('commentblocktree', ['* COMMENT ', (), '\n \*']),
            ('$', ['$', (), '$', '.']),
            ('questions', [' * QUESTIONS ', (), '\n \* ']),
            ('solution', [' *** SOLUTION ', (), '\n \*']),
            ('img', [' **** IMG ', (), '\n \*']),
            ('prompt', [' *** PROMPT ', (), '\n \*\*\* ']),
            ('choices', [' *** CHOICES ', (), '\n \*']),
            ('choice', [' - [ ]', (), '\n \*']),
            ('correctchoice', [' - [X] ', (), '\n \*']),
            ('tolerance', [' **** TOLERANCE ', (), '\n \*']),
            ('verbatim', [' **** VERB ', (), '\n \*']),
            ('true', [' *** TRUE ', (), '\n \*']),
            ('false', [' *** FALSE ', (), '\n \*']),
            ('question', [' ** QUESTION ', (), '\n \*']),
            ('multichoice', [['title'], (), ['choices'], (), '$']),
            ('shortanswer', [['title'], (), ['solution'], (), '$']),
            ('truefalse', [['title'], (), ['true', 'false'], (), '$']),
            ('essay', [['title'], (), '$']),
            ('title', [' *** TITLE ', (), '\n \*']),
        ])
    })
    # Return signature
    return plugin


def unload():
    pass



