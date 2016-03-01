# Author: Eric Buss <ebuss@ualberta.ca> 2016
import formatter
import filters
import collections


# Plugin signature
plugin = {
    'name': 'latex format',
    'author': 'ejrbuss',
    'description': 'LaTeX markup format for creating documents with scientific and mathematical notation'
}


# Regex for recognizing the end of a question
end = r'(\\question)|(\\titledquestion)|(\\end{questions})'


def parser_preprocessor(src):
    """
    Swaps all instances of \question with \titledquestion{question} to help translate to other formats.
    :param src: The template source
    :return: The modified source
    """
    src = src.replace('\\question', '\\titledquestion{question}')
    return src


def parser_postprocessor(intermediate):
    """
    Because LaTeX has no defined Prompt the first string, equations, and images found in a question are put under a
    prompt Token.
    :param intermediate: An intermediate parse object
    :return: A modified intermediate
    """
    def def_prompt(definition, question):
        # If a prompt needs to be found
        if question:
            title, prompt = definition.pop(0), []
            while len(definition) > 0 and (not hasattr(definition[0], 'name') or definition[0].name in ['$', 'img']):
                prompt.append(definition.pop(0))
            definition.insert(0, formatter.Token('prompt', prompt, None, ''))
            definition.insert(0, title)
        # Recurse through all tokens
        for token in [token for token in definition if hasattr(token, 'definition')]:
            def_prompt(token.definition, token.name in ['essay', 'shortanswer', 'multichoice', 'numerical'])
    # Run inner function recursively on the ast
    def_prompt(intermediate.ast, False)
    return intermediate


def composer_postprocessor(composed):
    return '\\documentclass[]' + composed


def load():
    formatter.add_format({
        'extensions': ['latex', 'tex'],
        'description': plugin['description'],
        # Assign processors
        'parser_preprocessor': parser_preprocessor,
        'parser_postprocessor': parser_postprocessor,
        'composer_preprocessor': filters.pass_through,
        'composer_postprocessor': filters.pass_through,
        # Use an OrderedDict to preserve token order
        'format': collections.OrderedDict([
            ('comment', ['%', (), '\n']),
            ('commentblock', ['begin{comment}', (), 'end{comment}', '.']),
            ('$', ['$', (), '$', '.']),
            ('questions', ['\\begin{questions}', (), '\\end{questions}', '.']),
            ('points', ['[', (), ']', '.']),
            ('title', ['question{', (), '}', '.']),
            ('solution', ['\\begin{solution}', (), '\\end{solution}', '.']),
            ('img', ['\\includegraphics{', (), '}' '.']),
            ('choices', ['\\begin{choices}', (), '\\end{choices}', '.']),
            ('choice', ['\\choice ', (), r'(\\choice)|(\\CorrectChoice)']),
            ('correctchoice', ['\\CorrectChoice ', (), r'(\\choice)|(\\CorrectChoice)']),
            ('multichoice', ['\\titled', ['title'], (), ['choices'], (), end]),
            ('shortanswer', ['\\titled', ['title'], (), ['solution'], (), end]),
            ('essay', ['\\titled', ['title'], (), end]),
            ('unknownarg', ['{', (), '}', '.']),
            ('unknown', ['\\', (), '(\\s+)|(\{)']),
        ])
    })
    # Return signature
    return plugin


def unload():
    pass



