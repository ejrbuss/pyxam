# Author: Eric Buss <ebuss@ualberta.ca> 2016\
import xml.dom.minidom
import formatter
import collections
import filters


signature = 'moodle format', 'ejrbuss', 'Format for producing and viewing moodle xml files'
# Plugin signature

fmt_truefalse =  '<answer fraction="{}"><text>true</text><feedback><text>Correct</text></feedback></answer>\n \
                    <answer fraction="{}"><text>false</text><feedback><text>Incorrect</text></feedback></answer>'
#TODO finish

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
        if not token.definition[0].startswith('<text>'):
            token.definition = ['<text>'] + token.definition + ['</text>']
        return token
    intermediate.ast = filters.promote(intermediate.ast, 'questions')
    intermediate.ast = filters.img64(intermediate.ast)
    intermediate.ast = filters.apply_function(intermediate.ast, fix_html, 'verbatim')
    intermediate.ast = filters.apply_function(intermediate.ast, fix_solutions, 'solution')
    return intermediate


def composer_postprocessor(source):
    return xml.dom.minidom.parseString(source).toprettyxml()

def load():
    formatter.add_format(
        name='moodle',
        extensions=['xml'],
        description=signature[2],
        format=collections.OrderedDict([
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
        ]),
        composer_preprocessor=composer_preprocessor,
        composer_postprocessor=composer_postprocessor
    )
    # Return signature
    return signature


def unload():
    pass



