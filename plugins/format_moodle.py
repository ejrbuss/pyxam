from formatter import add_format

plugin = {
    'name': 'moodle format',
    'author': 'ejrbuss',
    'description': 'Format for viewing files in moodle'
}


def processor(ast):
    return ast

def composer_posprocessor(composed):
    return '<quiz>\n' + composed + '\n</quiz>'


def load():
    add_format({
        'extensions': ['moodle', 'xml'],
        'description': plugin['description'],
        'parser_preprocessor': processor,
        'parser_postprocessor': processor,
        'composer_preprocessor': processor,
        'composer_postprocessor': composer_posprocessor,
        'format': {
            'comment': ['<!--', (), '-->', '.'],
            'equation': ['$$', (), '$$', '.'],
            'question': ['<question ', (), '</question>', '.'],
            'type': ['type="', (), '">', '.'],
            'title': ['<name> <text>', (), '</text> </name>', '.'],
            'prompt': ['<questiontext format="html"> <text> <![CDATA[', (), ']]> </text> </questiontext>', '.'],
            'solution': ['<answer fraction="100"> <text>', (), '</text> <feedback> <text> Correct </text> </feedback> </answer>', '.'],
            'img': ['<img alt="Embedded Image" src="data:image/png;base64,', (), '">', '.'],
            'choice': ['<answer fraction="0"> <text>', (), '</text> <feedback> <text> Incorrect </text> </feedback> </answer>', '.'],
            'correctchoice': ['<answer fraction="100"> <text>', (), '</text> <feedback> <text> Correct </text> </feedback> </answer>', '.'],
            'shuffle': ['<shuffleanswers>1</shuffleanswers> <single>true</single>', (), '.'],
        }
    })
    return plugin


def unload():
    pass



