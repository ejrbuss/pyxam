# Author: Eric Buss <ebuss@ualberta.ca> 2016
"""
# Plugin format_moodle

Plugin for importing and exporting moodle xml files.
"""
import xml.dom.minidom
import parser_composer
import collections
import filters


signature = 'moodle format', 'ejrbuss', 'Format for producing and viewing moodle xml files'


def composer_preprocessor(intermediate):
    """
    Performs the following modifications to the intermediate:
     - Promote questions token to top level of the ast
     - Converts images to a base64 encoded string to appear directly in the HTML source
     - Add text tags around the solution if they are not already present

    :param intermediate: An intermediate parse object
    :return: A modified intermediate
    """
    def fix_solutions(token):
        if not filters.has_name(token) and token.definition[0].startswith('<text>'):
            token.definition = ['<text>'] + token.definition + ['</text>']
        return token

    intermediate.ast = filters.promote(intermediate.ast, 'questions')
    intermediate.ast = filters.img64(intermediate.ast)
    intermediate.ast = filters.apply_function(intermediate.ast, fix_solutions, 'solution')
    return intermediate


def composer_postprocessor(source):
    """
    Formats the xml to help readability.

    :param source: The source to transform
    :return: The transformed source
    """
    return xml.dom.minidom.parseString(source).toprettyxml()


def load():
    """
    Loads the moodle xml format.
    """
    parser_composer.add_format(
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
            ('verbatim', ['<pre class="verbatim">', (), '</pre>', '.']),
            ('essay', ['<question type="essay">', (), '</question>', '']),
            ('tolerance', ['<tolerance>', (), '</tolerance><tolerancetype>1</tolerancetype>', '.']),
            ('shortanswer', ['<question type="shortanswer">', ['title'], (), '</question>', '.']),
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
    return signature





