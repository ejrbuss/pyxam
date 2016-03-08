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

fmt_truefalse =  '<answer fraction="{}"><text>true</text><feedback><text>Correct</text></feedback></answer>\n \
                    <answer fraction="{}"><text>false</text><feedback><text>Incorrect</text></feedback></answer>'
shuffle = '<shuffleanswers>1</shuffleanswers>'


def composer_preprocessor(intermediate):
    """
    Promote questions to top level of the ast
    :param intermediate: An intermediate parse object
    :return: A modified intermediate
    """
    def fix_html(token):
        token.definition[0] = token.definition[0].replace('<', '&#60;').replace('\n', '<br />\n').replace(' '*4, '&emsp;'*2)
        return token
    intermediate.ast = filters.promote(intermediate.ast, 'questions')
    intermediate.ast = filters.img64(intermediate.ast)
    intermediate.ast = filters.apply_function(intermediate.ast, fix_html, 'verbatim')
    return intermediate


def composer_postprocessor(composed):
    """

    :param composed:
    :return:
    """
    composed = composed.replace('<tolerance>', '</text><tolerance>')
    composed = composed.replace('</tolerancetype></text>', '</tolerancetype>')
    return composed


def load():
    formatter.add_format({
        'extensions': ['moodle', 'xml'],
        'description': plugin['description'],
        # Assign processors
        'parser_preprocessor': filters.pass_through,
        'parser_postprocessor': filters.pass_through,
        'composer_preprocessor': composer_preprocessor,
        'composer_postprocessor': composer_postprocessor,
        # Use an OrderedDict to preserve token order
        'format': collections.OrderedDict([
            ('comment', ['<!--', (), '-->', '.']),
            ('$', ['$$', (), '$$', '.']),
            ('questions', ['<?xml version="1.0" ?> <quiz>', (), '</quiz>', '.']),
            ('title', ['<name> <text>', (), '</text> </name>', '.']),
            ('prompt', ['<questiontext format="html"> <text> <![CDATA[', (), ']]> </text> </questiontext>', '.']),
            ('solution', ['<answer fraction="100"> <text>', (), '</text> <feedback> <text> Correct </text> </feedback> </answer>', '.']),
            ('img', ['<img alt="Embedded Image" src="data:image/png;base64,', (), '">', '.']),
            ('choice', ['<answer fraction="0"> <text>', (), '</text> <feedback> <text>Incorrect</text> </feedback> </answer>', '.']),
            ('correctchoice', ['<answer fraction="100"> <text>', (), '</text> <feedback> <text>Correct</text> </feedback> </answer>', '.']),
            ('verbatim', ['<p style="font-family:monospace;padding:1em"><b>', (), '</b></p>', '.']),
            ('true', [fmt_truefalse.format('100', '0'), '.']),
            ('false', [fmt_truefalse.format('0', '100'), '.']),
            ('essay', ['<question type="essay">', (), '</question>', '']),
            ('tolerance', ['<tolerance>', (), '</tolerance>\n<tolerancetype>1</tolerancetype>', '.']),
            ('shortanswer', ['<question type="shortanswer">', ['title'], (), '</question>', '.']),
            ('truefalse', ['<question type="truefalse">', ['title'], (), '</question>', '.']),
            ('multichoice', ['<question type="multichoice">', ['title'], (), shuffle, '</question>', '.']),
            ('multiselect', ['<question type="multichoice"><single>false</single>', ['title'], (), shuffle, '</question>', '.']),
            ('numerical', ['<question type="numerical">', ['title'], (), '</question>', '.']),
        ])
    })
    # Return signature
    return plugin


def unload():
    pass



