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


def parser_postprocessor(intermediate):
    """
    Because LaTeX has no defined Prompt the first string, equations, and images found in a question are put under a
    prompt Token.
    :param intermediate: An intermediate parse object
    :return: A modified intermediate
    """
    def def_prompt(token):
        try:
            definition = token.definition[0].definition
            title, prompt = definition.pop(0), []
            while len(definition) > 0 and (not hasattr(definition[0], 'name') or definition[0].name in ['$', 'img', 'verbatim']):
                prompt.append(definition.pop(0))
            definition.insert(0, formatter.Token('prompt', prompt, None, ''))
            definition.insert(0, title)
            return token
        except AttributeError:
            raise(formatter.FormatError('Malformed question token definition:' + str(token)))

    # Run inner function recursively on the ast
    filters.apply_function(intermediate.ast, def_prompt, 'question', exact=True)
    return intermediate


def composer_preprocessor(intermediate):
    """
    Applies the following filters to the tree:
     - Promotes the questions token

    :param intermediate:
    :return: The modified tree
    """

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
        parser_postprocessor=parser_postprocessor,
        composer_preprocessor=composer_preprocessor,
        composer_postprocessor=composer_postprocessor,
        format=collections.OrderedDict([
            ('comment', ['#', (), '\n']),
            ('commentblock', ['#+BEGIN_COMMENT ', (), '#+END_COMMENT']),
            ('commentblocktree', ['* COMMENT ', (), '\*']),
            ('$', ['$', (), '$', '.']),
            ('questions', ['* ?', (), '$']),
            ('question', ['** ', (), '\n\*\*[^*]']),
            ('solution', ['*** Solution', (), '\n\*\*\*[^*]']),
            ('img', ['\\includegraphics[width= \linewidth]{', (), '}', '.']),
            ('choice', ['- [ ]', (), '- \[']),
            ('correctchoice', ['- [X]', (), '- \[']),
            ('multichoice', [['title'], (), ['choice', 'correctchoice'], (), '$']),
            ('shortanswer', [['title'], (), ['solution'], '$']),
            ('essay', [['title'], (), '$']),
            ('title', ['?', (), '\n'])
        ])
    )
    return signature



