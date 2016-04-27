# Author: Eric Buss <ebuss@ualberta.ca> 2016
"""
# Plugin format_latex

Formatter plugin for importing and exporting LaTeX.
"""
import re
import util
import options
import filters
import fileutil
import collections
import parser_composer


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
    if options.state.format() not in ['tex', 'pdf', 'dvi']:
        src = re.sub(r'\\includegraphics.*?{', '\\includegraphics[width= \linewidth]{', src)
    return src


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
            definition.insert(0, util.Map({'name': 'prompt', 'definition': prompt}))
            definition.insert(0, title)
            return token
        except AttributeError:
            raise(parser_composer.FormatError('Malformed question token definition:' + parser_composer.str_token(token)))

    # Run inner function recursively on the ast
    filters.apply_function(intermediate.ast, def_prompt, 'question', partial=False)
    return intermediate


def composer_preprocessor(intermediate):
    intermediate.ast = filters.wrap_lists(intermediate.ast)
    return intermediate


def composer_postprocessor(source):
    """
    Adds the necessary boilerplate commands to the LaTeX file if they are not present as well as enables solutions if
    the option is set. Performs some rough formatting.

    :param source: The source to transform
    :return: The transformed source
    """
    if not '\\documentclass' in source:
        source = '\\documentclass[12pt]{exam}\\usepackage[pdftex]{graphicx}\\begin{document}' + source + '\\end{document}'
    if options.state.solutions():
        source = re.sub(r'\\documentclass\[', r'\documentclass[answers,', source)
        source = re.sub(r'\\documentclass{', r'\documentclass[answers]{', source)
    source = re.sub(
        r'\\includegraphics\[(.*?)\]\{(.*?)\}',
        lambda m : '\\includegraphics[' + m.group(1) + ']{' + fileutil.find_file(m.group(2)) + '}',
        source
    )
    source = re.sub(r'(\n(((\\%)|[^%\n])*))\\include', r'\1\n\n\\include', source)
    return source


def load():
    """
    Loads the tex formatter.
    """
    parser_composer.add_format(
        name='tex',
        extensions=['tex', 'LaTeX', 'latex'],
        description=signature[2],
        parser_preprocessor=parser_preprocessor,
        parser_postprocessor=parser_postprocessor,
        composer_preprocessor=composer_preprocessor,
        composer_postprocessor=composer_postprocessor,
        left_paren='{',
        right_paren='}',
        # Use an OrderedDict to preserve token order
        format=collections.OrderedDict([
            ('comment', ['%', (), '\n']),
            ('commentblock', ['\\begin{comment}', (), '\\end{comment}', '.']),
            ('$$', ['$$', (), '$$', '.']),
            ('$', ['$', (), '$', '.']),
            ('questions', ['\\begin{questions}', (), '\\end{questions}', '.']),
            ('solution', ['\\begin{solution}', (), '\\end{solution}', '.']),
            ('img', ['\\includegraphics[width= \linewidth]{', (), '}', '.']),
            ('choices', ['\\begin{choices}', (), '\\end{choices}', '.']),
            ('choice', ['\\choice ', (), r'(\\choice)|(\\CorrectChoice)']),
            ('correctchoice', ['\\CorrectChoice ', (), r'(\\choice)|(\\CorrectChoice)']),
            ('verbatim', ['\\begin{verbatim}', (), '\\end{verbatim}', '.']),
            ('verbython', ['\\begin{verbatim}', (), '\\end{verbatim}', '.']),
            ('verbhtml', ['\\begin{verbatim}\\end{verbatim}', '.']),
            ('verbblock', ['\\begin{verbatim}', (), '\\end{verbatim}', '.']),
            ('newpage', ['\\clearpage', '.']),
            ('h3', ['\\textbf{', (), '} \\\\', '.']),
            ('h2', ['\\subsection*{', (), '}', '.']),
            ('h1', ['\\section*{', (), '}', '.']),
            ('list', [' \\begin{description} ', (), ' \\end{description} ', '.']),
            ('listitem', ['\item ', (), '\n']),
            ('newline', ['\\\\', '.']),
            ('center', ['\\begin{center}', (), '\\end{center}', '.']),
            ('question', ['\\titled', (), end]),
            ('multichoice', [['title'], (), ['choices'], (), '$']),
            ('shortanswer', [['title'], (), ['solution'], (), '$']),
            ('truefalse', [['title'], (), ['choices'], '$']),
            ('essay', [['title'], (), '$']),
            ('title', ['question{', (), '}', '.']),
            ('center', ['\\begin{center}', (), '\\end{center}', '.']),
            ('emphasis2', ['\\textbf{', (), '}', '.']),
            ('emphasis1', ['\\textit{', (), '}', '.']),
            ('unknown', ['\\', (), '\\s+'])
        ])
    )
    return signature



