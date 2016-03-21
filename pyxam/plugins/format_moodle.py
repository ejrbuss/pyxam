# Author: Eric Buss <ebuss@ualberta.ca> 2016\
import xml.dom.minidom
import re
import formatter
import collections
import filters


signature = 'moodle foramt', 'ejrbuss', 'Foramt for producing and viewing moodle xml files'
# Plugin signature

fmt_truefalse =  '<answer fraction="{}"><text>true</text><feedback><text>Correct</text></feedback></answer>\n \
                    <answer fraction="{}"><text>false</text><feedback><text>Incorrect</text></feedback></answer>'


def composer_preprocessor(intermediate):
    """
    Promote questions to top level of the ast
    :param intermediate: An intermediate parse object
    :return: A modified intermediate
    """
    def fix_html(token):
        token.definition[0] = token.definition[0].replace('<', '&#60;').replace('\n', '<br />\n').replace(' '*4, '&emsp;'*2)
        return token

    def fix_solutions(token):
        token.definition[0] = '<text>' + token.definition[0] + '</text>'
        return token
    intermediate.ast = filters.promote(intermediate.ast, 'questions')
    intermediate.ast = filters.img64(intermediate.ast)
    intermediate.ast = filters.apply_function(intermediate.ast, fix_html, 'verbatim')
    intermediate.ast = filters.apply_function(intermediate.ast, fix_solutions, 'solution')
    return intermediate


def composer_postprocessor(source):
    source = xml.dom.minidom.parseString(source).toprettyxml()
    source = re.sub(r'\t', '     ', source)
    source = re.sub(r'(\n *\n)', '\n', source)
    return source

def load():
    formatter.add_format({
        'extensions': ['moodle', 'xml'],
        'description': signature[1],
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
            ('solution', ['<answer fraction="100">', (), '<feedback> <text> Correct </text> </feedback> </answer>', '.']),
            ('img', ['<img alt="Embedded Image" src="data:image/png;base64,', (), '">', '.']),
            ('choice', ['<answer fraction="0"> <text>', (), '</text> <feedback> <text>Incorrect</text> </feedback> </answer>', '.']),
            ('correctchoice', ['<answer fraction="100"> <text>', (), '</text> <feedback> <text>Correct</text> </feedback> </answer>', '.']),
            ('verbatim', ['<p style="font-family:monospace;padding:1em"><b>', (), '</b></p>', '.']),
            ('true', [fmt_truefalse.format('100', '0'), '.']),
            ('false', [fmt_truefalse.format('0', '100'), '.']),
            ('essay', ['<question type="essay">', (), '</question>', '']),
            ('tolerance', ['<tolerance>', (), '</tolerance><tolerancetype>1</tolerancetype>', '.']),
            ('shortanswer', ['<question type="shortanswer">', ['title'], (), '</question>', '.']),
            ('truefalse', ['<question type="truefalse">', ['title'], (), '</question>', '.']),
            ('multichoice', ['<question type="multichoice">', ['title'], (), '<shuffleanswers>1</shuffleanswers></question>', '.']),
            ('multiselect', ['<question type="multichoice"><single>false</single>', ['title'], (), '<shuffleanswers>1</shuffleanswers></question>', '.']),
            ('numerical', ['<question type="numerical">', ['title'], (), '</question>', '.']),
            ('calculated', ['<question type="calculatedsimple">', ['title'], (), '</question>', '.']),
            ('params', ['<dataset_definitions>', (), '</dataset_definitions>', '.']),
            ('param', ['<dataset_definition><status><text>private</text></status>', (), '</dataset_definition>', '.']),
            ('paramname', ['<name><text>', (), '</text></name><distribution><text>uniform</text></distribution>', '.']),
            ('parammax', ['<maximum><text>', (), '</text></maximum>', '.']),
            ('parammin', ['<minimum><text>', (), '</text></minimum>', '.']),
            ('paramdec', ['<decimals><text>', (), '</text></decimals>', '.']),
            ('itemcount', ['<itemcount>', (), '</itemcount>', '.']),
            ('items', ['<dataset_items>', (), '</dataset_items>', '.']),
            ('itemnumber', ['<dataset_item><number>', (), '</number>', '.']),
            ('itemvalue', ['<value>', (), '</value></dataset_item>', '.']),
            ('decimal', ['<correctanswerformat>1</correctanswerformat><correctanswerlength>', (), '</correctanswerlength>', '.'])
        ])
    })
    # Return signature
    return signature


def unload():
    pass


