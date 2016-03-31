# Author: Eric Buss <ebuss@ualberta.ca> 2016
"""
# Plugin format_org

Adds support import export format support for org mode files
"""
import re
import formatter
import collections
import filters


signature = 'org mode foramt', 'ejrbuss', 'Format for producing and viewing org mode files'


def composer_preprocessor(intermediate):
    """
    Applies the following filters to the tree:
     - Promotes the questions token

    :param intermediate:
    :return: The modified tree
    """
    intermediate.ast = filters.promote(intermediate.ast, 'questions')
    return intermediate


def composer_postprocessor(source):
    """
    Performs a number of formatting changes to the output org file:
     - Capital blocks are moved to a newline
     - Capital blocks with whitespace other than newlines and then content have their content moved to newlines
     - Consecutive newlines are reduced to a single newlines
     - Any newlines that appear at the start of the src are removed
     - Newlines followed by whitespace are changed to just newlines

    :param source: The source to format
    :return: The formatted source
    """
    source = re.sub(r'(\*+ +[A-Z]+)', r'\n\1', source)
    source = re.sub(r'(\*+ +[A-Z]+ +)(?=[^\n]+)', r'\1\n', source)
    source = re.sub(r'(\*+ +QUESTION +)\n', r'\1', source)
    source = re.sub(r'\n+', '\n', source)
    source = re.sub(r' +', ' ', source)
    source = re.sub(r'^\n', '', source)
    source = re.sub(r'\n ', '\n', source)
    return source


def load():
    """
    Adds the org format to the [formatter](%/Modules/Formatter.html).

    :return: plugin signature
    """
    formatter.add_format(
        name='org',
        extensions=['org'],
        description=signature[2],
        composer_preprocessor=composer_preprocessor,
        composer_postprocessor=composer_postprocessor,
        format=collections.OrderedDict([
            ('comment', ['#', (), '\n']),
            ('commentblock', ['#+BEGIN_COMMENT ', (), '#+END_COMMENT']),
            ('commentblocktree', ['* COMMENT ', (), '\*']),
            ('$', ['$', (), '$', '.']),
            ('questions', ['* QUESTIONS', (), r'\n\s*\*\s']),
            ('question', ['** QUEST', (), '\n\s*\*\*\s']),
            ('solution', ['*** SOLUTION ', (), '\*']),
            ('img', ['**** IMG ', (), '\*']),
            ('prompt', ['*** PROMPT ', (), '\*+ [^VI]']),
            ('choices', ['*** CHOICES ', (), '$']),
            ('choice', ['- [ ]', (), '- \[']),
            ('correctchoice', ['- [X]', (), '- \[']),
            ('tolerance', ['**** TOLERANCE ', (), '\*']),
            ('verbatim', ['**** VERB ', (), '\*']),
            ('true', ['*** TRUE ', (), '\n']),
            ('false', ['*** FALSE ', (), '\n']),
            ('multichoice', [['title'], ['prompt'], ['choices'], '$']),
            ('shortanswer', [['title'], ['prompt'], ['solution'], '$']),
            ('truefalse', [['title'], ['prompt'], ['true', 'false'], '$']),
            ('essay', [['title'], ['prompt'], '$']),
            ('title', ['ION ', (), '\n']),
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



