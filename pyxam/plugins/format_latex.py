# Author: Eric Buss <ebuss@ualberta.ca> 2016
import re
import options
import formatter
import filters
import collections


signature = 'latex foramt', 'ejrbuss', 'LaTeX markup format for creating documents with scientific and mathematical notation'


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
    def def_prompt(token):
        if token.name != 'question':
            return
        definition = token.definition[0].definition
        title, prompt = definition.pop(0), []
        while len(definition) > 0 and (not hasattr(definition[0], 'name') or definition[0].name in ['$', 'img', 'verbatim']):
            prompt.append(definition.pop(0))
        definition.insert(0, formatter.Token('prompt', prompt, None, ''))
        definition.insert(0, title)
        return token

    # Run inner function recursively on the ast
    filters.apply_function(intermediate.ast, def_prompt, 'question')
    return intermediate


def composer_postprocessor(composed):
    if options.state.solutions():
        composed = re.sub(r'(?:^|[^\\%])\\documentclass\[', r'\documentclass[answers,', composed)
        composed = re.sub(r'(?:^|[^\\%])\\documentclass{', r'\documentclass[answers]{', composed)
    return composed


def load():
    formatter.add_format(
        name='latex',
        extensions=['tex'],
        description=signature[2],
        parser_preprocessor=parser_preprocessor,
        parser_postprocessor=parser_postprocessor,
        composer_postprocessor=composer_postprocessor,
        left_paren='{',
        right_paren='}',
        # Use an OrderedDict to preserve token order
        format=collections.OrderedDict([
            ('comment', ['%', (), '\n']),
            ('commentblock', ['\\begin{comment}', (), '\\end{comment}', '.']),
            ('$', ['$', (), '$', '.']),
            ('questions', ['\\begin{questions}', (), '\\end{questions}', '.']),
            ('solution', ['\\begin{solution}', (), '\\end{solution}', '.']),
            ('img', ['\\includegraphics[width= \linewidth]{', (), '}', '.']),
            ('choices', ['\\begin{choices}', (), '\\end{choices}', '.']),
            ('choice', ['\\choice ', (), r'(\\choice)|(\\CorrectChoice)']),
            ('correctchoice', ['\\CorrectChoice ', (), r'(\\choice)|(\\CorrectChoice)']),
            ('verbatim', ['\\begin{verbatim}', (), '\\end{verbatim}', '.']),
            ('question', ['\\titled', (), end]),
            ('multichoice', [['title'], (), ['choices'], (), '$']),
            ('shortanswer', [['title'], (), ['solution'], (), '$']),
            ('truefalse', [['title'], (), ['choices'], '$']),
            ('essay', [['title'], (), '$']),
            ('title', ['question{', (), '}', '.']),
            ('unknownarg', ['{', (), '}', '.']),
            ('unknown', ['\\', (), '\\s+']),
        ])
    )
    # Return signature
    return signature


def unload():
    pass



