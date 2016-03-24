# Author: Eric Buss <ebuss@ualberta.ca> 2016
import re
import formatter
import collections
import filters


signature = 'org mode foramt', 'ejrbuss', 'Format for producing and viewing org mode files'


def composer_preprocessor(intermediate):
    intermediate.ast = filters.promote(intermediate.ast, 'questions')
    intermediate.ast = filters.remove_name(intermediate.ast, 'decimal')
    intermediate.ast = filters.remove_name(intermediate.ast, 'params')
    return intermediate


def composer_postprocessor(source):
    source = re.sub(r'(\*+ +[A-Z]+)', r'\n\1', source)
    source = re.sub(r'(\*+ +[A-Z]+ +)(?=[^\n]+)', r'\1\n', source)
    source = re.sub(r'(\*+ +QUESTION +)\n', r'\1', source)
    source = re.sub(r'\n+', '\n', source)
    source = re.sub(r' +', ' ', source)
    source = re.sub(r'^\n', '', source)
    source = re.sub(r'\n ', '\n', source)
    return source


def load():
    formatter.add_format({
        'extensions': ['org', 'org'],
        'description': signature[1],
        # Assign processors
        'parser_preprocessor': filters.pass_through,
        'parser_postprocessor': filters.pass_through,
        'composer_preprocessor': composer_preprocessor,
        'composer_postprocessor': composer_postprocessor,
        # Use an OrderedDict to preserve token order
        'format': collections.OrderedDict([
            ('comment', ['#', (), '\n']),
            ('commentblock', ['#+BEGIN_COMMENT ', (), '#+END_COMMENT']),
            ('commentblocktree', ['* COMMENT ', (), '\*']),
            ('$', ['$', (), '$', '.']),
            ('questions', ['* QUESTIONS', (), '\n\s*\*\s']),
            ('solution', ['*** SOLUTION ', (), '.']),
            ('img', ['**** IMG ', (), '\*']),
            ('prompt', ['*** PROMPT ', (), '(\* CHOICES)|(\* SOLUTION)|(\* TRUE)|(\* FALSE)']),
            ('choices', ['*** CHOICES ', (), '.']),
            ('choice', [' - [ ]', (), '\n']),
            ('correctchoice', [' - [X] ', (), '\n']),
            ('tolerance', ['**** TOLERANCE ', (), '\*']),
            ('verbatim', ['**** VERB ', (), '\*']),
            ('true', ['*** TRUE ', (), '\n']),
            ('false', ['*** FALSE ', (), '\n']),
            ('multichoice', [['title'], ['prompt'], ['choices'], '$']),
            ('shortanswer', [['title'], ['prompt'], ['solution'], '$']),
            ('truefalse', [['title'], ['prompt'], ['true', 'false'], '$']),
            ('essay', [['title'], ['prompt'], '$']),
            ('title', ['** QUESTION ', (), '\n']),
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
    })
    # Return signature
    return signature


def unload():
    pass



