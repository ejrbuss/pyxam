# Author: Eric Buss <ebuss@ualberta.ca> 2016
import options
import formatter
import collections
import filters
import re

signature = 'html format', 'ejrbuss', 'Format for viewing and producing html files'

css = """
<style>
body {
    margin: 0;
    background: #E7E9E8;
}
img {
    display: block;
    margin: 0 auto;
}
.questions {
    padding: 4em;
    width: 50%;
    display: block;
    margin: 0 auto;
    background: #FFFFFF;
}
.latex {
    font-style: italic;
    font-family: times;
    font-size: 1.1em;
}
.title {
    font-weight: bold;
    padding: 1em;
    padding-left: 0;
}
.solution {
    width: 100%;
    border: 2px solid #278857;
    padding: 0.5em;
    margin: 0.5em;
}
.solution:before {
    content: 'Solution: ';
    font-weight: bold;
}
.choice:before {
    content:  '___';
    font-weight: bold;
    padding: 1em;
    line-height: 2em;
}
.correctchoice:before {
    content:  ' \\2713';
    font-weight: bold;
    padding: 1em;
    line-height: 2em;
    color: #278857;
}
.verbatim {
    margin: 1em;
    background: #F7F7F7;
    font-family: monospace;
    font-size: 1.1em;
    padding: 1em;
    white-space: pre;
    display: block;
    unicode-bidi: embed;
    line-height: 2em;
}
.True {

}
.False {

}
</style>
"""
math = {
    '\\theta':      '&theta;',
    '\\pi':         '&pi;',
    '\\tau':        '&tau;',
    '\\omega':      '&omega;',
    '\\phi':        '&phi;',
    '\\emptyset':   '&phi;',
    '\\int_':       '&int;',
    '\\sum_':       '&sum;',
    '+/-':          '&#177;'
}


def composer_preprocessor(intermediate):
    def fix_html(token):
        token.definition[0] = token.definition[0].replace('<', '&#60;').replace(' '*4, '&emsp;'*2)
        return token
    intermediate.ast = filters.promote(intermediate.ast, 'questions')
    intermediate.ast = filters.img64(intermediate.ast)
    intermediate.ast = filters.apply_function(intermediate.ast, fix_html, 'verbatim')
    return intermediate


def composer_postprocessor(src):
    # Regex replacements
    src = re.sub(r'\\sqrt\{(.*?)\}', r'&radic;\1', src)
    # String replacements
    for symbol in math:
        src = src

    if options.state.solutions():
        src = src.replace('display:none', '')
        src = src.replace('display:visible', 'display:none')
    if not src.startswith('<!DOCTYPE html>'):
        return '<!DOCTYPE html><html>' + css + '<body>' + src + '\n</body></html>'
    return src


def load():
    formatter.add_format({
        'extensions': ['html', 'html'],
        'description': signature[1],
        # Assign processors
        'parser_preprocessor': filters.pass_through,
        'parser_postprocessor': filters.pass_through,
        'composer_preprocessor': composer_preprocessor,
        'composer_postprocessor': composer_postprocessor,
        'left_paren': '<div',
        'right_paren': '</div>',
        # Use an OrderedDict to preserve token order
        'format': collections.OrderedDict([
            ('comment', ['<!--', (), '-->', '.']),
            ('questions', ['<div class="questions">', (), '</div>', '.']),
            ('$', ['<span class="latex"> ', (), ' </span>', '.']),
            ('title', ['<div class="title">', (), '</div>', '.']),
            ('solution', ['<div class="solution">', (), '</div>', '.']),
            ('img', ['<img alt="Embedded Image" src="data:image/png;base64,', (), '">', '.']),
            ('choice', ['<div class="choice">', (), '</div>', '.']),
            ('correctchoice', ['<div class="correctchoice">', (), '</div>', '.']),
            ('tolerance', [' tolerance ', (), '.']),
            ('verbatim', ['<div class="verbatim">', (), '</div>', '.']),
            ('true', ['<div class=True>True</div>', '.']),
            ('false', ['<div class=False>False</div>', '.']),
        ])
    })
    # Return signature
    return signature


def unload():
    pass



