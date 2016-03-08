# Author: Eric Buss <ebuss@ualberta.ca> 2016
import options
import formatter
import collections
import filters
import re


# Plugin signature
plugin = {
    'name': 'html format',
    'author': 'ejrbuss',
    'description': 'Format for viewing files in html'
}


def composer_preprocessor(intermediate):
    def fix_html(token):
        token.definition[0] = token.definition[0].replace('<', '&#60;').replace('\n', '<br />\n').replace(' '*4, '&emsp;'*2)
        return token
    intermediate.ast = filters.promote(intermediate.ast, 'questions')
    intermediate.ast = filters.img64(intermediate.ast)
    intermediate.ast = filters.apply_function(intermediate.ast, fix_html, 'verbatim')
    return intermediate


def composer_postprocessor(src):
    # Regex replacements
    src = re.sub(r'\\sqrt\{(.*?)\}', r'&radic;\1', src)
    # String replacements
    src = src.replace('\\theta',    '&theta;')
    src = src.replace('\\pi',       '&pi;')
    src = src.replace('\\omega',    '&omega;')
    src = src.replace('\\phi',      '&phi;')
    src = src.replace('\\emptyset', '&phi;')
    src = src.replace('\\int_',     '&int;')
    src = src.replace('\\sum_',     '&sum;')
    if options.state.solutions():
        src = src.replace('display:none', '')
        src = src.replace('display:visible', 'display:none')
    if not src.startswith('<!DOCTYPE html>'):
        return '<!DOCTYPE html><html><body>\n' + src + '\n</body></html>'
    return src


def load():
    formatter.add_format({
        'extensions': ['html', 'html'],
        'description': plugin['description'],
        # Assign processors
        'parser_preprocessor': filters.pass_through,
        'parser_postprocessor': filters.pass_through,
        'composer_preprocessor': composer_preprocessor,
        'composer_postprocessor': composer_postprocessor,
        # Use an OrderedDict to preserve token order
        'format': collections.OrderedDict([
            ('comment', ['<!--', (), '-->', '.']),
            ('$', ['<span class="$"style="font-family:times"><i> ', (), ' </i></span>', '.']),
            ('title', ['<br /><br /><b>', (), '</b><br />', '.']),
            ('solution', ['<span style="display:none"><br /><b>', (), '</b><br /></span>', '.']),
            ('img', ['<img alt="Embedded Image" src="data:image/png;base64,', (), '">', '.']),
            ('choice', ['<br /> __ ', (), '<br />', '.']),
            ('correctchoice', ['<br /><span style="display:visible">__</span><span style="display:none"> &#10003;</span> ', (), '<br />', '.']),
            ('tolerance', ['+/-[', (), ']', '.']),
            ('verbatim', ['<p style="font-family:monospace;padding:1em"><b>', (), '</b></p>', '.']),
            ('true', ['<br /> __ True<br />', '.']),
            ('false', ['<br /> __ False<br />', '.']),
        ])
    })
    # Return signature
    return plugin


def unload():
    pass



