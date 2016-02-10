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
            ('equation', ['$$', (), '$$', '.']),
            ('questions', ['<?xml version="1.0" ?> <quiz>', (), '</quiz>', '.']),
            ('title', ['<name> <text>', (), '</text> </name>', '.']),
            ('prompt', ['<questiontext format="html"> <text> <![CDATA[', (), ']]> </text> </questiontext>', '.']),
            ('solution', ['<answer fraction="100"> <text>', (), '</text> <feedback> <text> Correct </text> </feedback> </answer>', '.']),
            ('img', ['<img alt="Embedded Image" src="data:image/png;base64,', (), '">', '.']),
            ('choice', ['<answer fraction="0"> <text>', (), '</text> <feedback> <text> Incorrect </text> </feedback> </answer>', '.']),
            ('correctchoice', ['<answer fraction="100"> <text>', (), '</text> <feedback> <text> Correct </text> </feedback> </answer>', '.']),
            ('shuffle', ['<shuffleanswers>1</shuffleanswers> <single>true</single>', (), '.']),
            ('titledessay', ['<question type="essay">', (), '</question>', '']),
            ('titledshortanswer', ['<question type="shortanswer">', ['title'], (), '</question>', '']),
            ('titlednumerical', ['<question type="numerical">', ['title'], (), '</question>', '']),
            ('titledtruefalse', ['<question type="truefalse">', ['title'], (), '</question>', '']),
            ('titledmultichoice', ['<question type="multichoice">', ['title'], (), '</question>', '']),
            ('essay', ['<question type="essay">', (), '</question>\n\n', '']),
            ('shortanswer', ['<question type="shortanswer">', (), '</question>\n\n', '']),
            ('numerical', ['<question type="numerical">', (), '</question>\n\n', '']),
            ('truefalse', ['<question type="truefalse">', (), '</question>\n\n', '']),
            ('multichoice', ['<question type="multichoice">', (), '</question>\n\n', '']),
        ])


def processor(ast):
    return ast


def composer_preprocessor(intermediate):
    intermediate.ast = [token for token in intermediate.ast if is_question(token)]
    for questions in intermediate.ast:
        for question in [question for question in questions.definition if hasattr(question, 'definition')]:
            token = Token('prompt', [token for token in takewhile(is_prompt, question.definition)], None, '')
            question.definition = [token] + question.definition[len(token.definition):]
    return intermediate


def is_question(token):
    return hasattr(token, 'definition') and ('essay' or 'truefalse' or 'numerical' or 'multichoice' or 'shortanswer') in token.name


def is_prompt(token):
    return isinstance(token, str) or token.name not in fmt or \
           token.name == 'equation' or token.name == 'img' or token.name == 'comment' or token.name == 'unkown'


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



