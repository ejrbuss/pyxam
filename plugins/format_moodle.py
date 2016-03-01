# Author: Eric Buss <ebuss@ualberta.ca> 2016
import formatter
import collections
import filters


# Plugin signature
plugin = {
    'name': 'moodle format',
    'author': 'ejrbuss',
    'description': 'Format for viewing files in moodle'
}


shuffle = '<shuffleanswers>1</shuffleanswers> <single>true</single>'


def composer_preprocessor(intermediate):
    """
    Filter out all top level tokens aside from questions.
    :param intermediate: An intermediate parse object
    :return: A modified intermediate
    """
    intermediate.ast = [token for token in intermediate.ast if hasattr(token, 'name') and token.name == 'questions']
    return intermediate


def load():
    formatter.add_format({
        'extensions': ['moodle', 'xml'],
        'description': plugin['description'],
        # Assign processors
        'parser_preprocessor': filters.pass_through,
        'parser_postprocessor': filters.pass_through,
        'composer_preprocessor': composer_preprocessor,
        'composer_postprocessor': filters.pass_through,
        'seperator': '\n',
        # Use an OrderedDict to preserve token order
        'format': collections.OrderedDict([
            ('comment', ['<!--', (), '-->', '.']),
            ('$', ['$$', (), '$$', '.']),
            ('questions', ['<?xml version="1.0" ?> <quiz>', (), '</quiz>', '.']),
            ('title', ['<name> <text>', (), '</text> </name>', '.']),
            ('prompt', ['<questiontext format="html"> <text> <![CDATA[', (), ']]> </text> </questiontext>', '.']),
            ('solution', ['<answer fraction="100"> <text>', (), '</text> <feedback> <text> Correct </text> </feedback> </answer>', '.']),
            ('img', ['<img alt="Embedded Image" src="data:image/png;base64,', (), '">', '.']),
            ('choice', ['<answer fraction="0"> <text>', (), '</text> <feedback> <text> Incorrect </text> </feedback> </answer>', '.']),
            ('correctchoice', ['<answer fraction="100"> <text>', (), '</text> <feedback> <text> Correct </text> </feedback> </answer>', '.']),
            ('essay', ['<question type="essay">', (), '</question>', '']),
            ('shortanswer', ['<question type="shortanswer">', ['title'], (), '</question>', '']),
            ('numerical', ['<question type="numerical">', ['title'], (), '</question>', '']),
            ('truefalse', ['<question type="truefalse">', ['title'], (), '</question>', '']),
            ('multichoice', ['<question type="multichoice">', ['title'], (), shuffle, '</question>', '']),
        ])
    })
    # Return signature
    return plugin


def unload():
    pass



