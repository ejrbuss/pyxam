from formatter import add_format
from formatter import Token
from collections import OrderedDict
from itertools import takewhile

plugin = {
    'name': 'moodle format',
    'author': 'ejrbuss',
    'description': 'Format for viewing files in moodle'
}

fmt = OrderedDict([
            ('comment', ['<!--', (), '-->', '.']),
            ('$', ['$$', (), '$$', '.']),
            ('questions', ['<?xml version="1.0" ?> <quiz>', (), '</quiz>', '.']),
            ('title', ['<name> <text>', (), '</text> </name>', '.']),
            ('prompt', ['<questiontext format="html"> <text> <![CDATA[', (), ']]> </text> </questiontext>', '.']),
            ('solution', ['<answer fraction="100"> <text>', (), '</text> <feedback> <text> Correct </text> </feedback> </answer>', '.']),
            ('img', ['<img alt="Embedded Image" src="data:image/png;base64,', (), '">', '.']),
            ('choice', ['<answer fraction="0"> <text>', (), '</text> <feedback> <text> Incorrect </text> </feedback> </answer>', '.']),
            ('correctchoice', ['<answer fraction="100"> <text>', (), '</text> <feedback> <text> Correct </text> </feedback> </answer>', '.']),
            ('shuffle', ['<shuffleanswers>1</shuffleanswers> <single>true</single>', (), '.']),
            ('essay', ['<question type="essay">', (), '</question>', '']),
            ('shortanswer', ['<question type="shortanswer">', ['title'], (), '</question>', '']),
            ('numerical', ['<question type="numerical">', ['title'], (), '</question>', '']),
            ('truefalse', ['<question type="truefalse">', ['title'], (), '</question>', '']),
            ('multichoice', ['<question type="multichoice">', ['title'], (), '</question>', '']),
        ])


def processor(ast):
    return ast


def composer_preprocessor(intermediate):
    intermediate.ast = [token for token in intermediate.ast if hasattr(token, 'name') and token.name == 'questions']
    return intermediate


def load():
    add_format({
        'extensions': ['moodle', 'xml'],
        'description': plugin['description'],
        'parser_preprocessor': processor,
        'parser_postprocessor': processor,
        'composer_preprocessor': composer_preprocessor,
        'composer_postprocessor': processor,
        'format': fmt
    })
    return plugin


def unload():
    pass



