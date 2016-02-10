from formatter import add_format
from collections import OrderedDict

# TODO Finish Latex format

plugin = {
    'name': 'latexformat',
    'author': 'ejrbuss',
    'description': 'LaTeX markup format for creating documents with scientific and mathematical notation'
}

end = '(\\question)|(\\titledquestion)|(end{questions})'


def processor(ast):
    return ast


def load():
    add_format({
        'extensions': ['latex', 'tex'],
        'description': plugin['description'],
        'parser_preprocessor': processor,
        'parser_postprocessor': processor,
        'composer_preprocessor': processor,
        'composer_postprocessor': processor,
        'format': OrderedDict([
            ('comment', ['%', (), '\n']),
            ('equation', ['$', (), '$', '.']),
            ('questions', ['\\begin{questions}', (), '\\end{questions}', '.']),
            ('title', ['\\titledquestion{', (), '}', '.']),
            ('points', ['[', (), ')', '.']),
            #'prompt', ['<questiontext format="html"> <text> <![CDATA[', (), ']]> </text> </questiontext>', '.']),
            ('solution', ['\\begin{solution}', (), '\\end{solution}', '.']),
            ('img', ['\\includegraphics{', (), '}' '.']),
            ('choices', ['\\begin{choices}', (), '\\end{choices}', '.']),
            ('choice', ['\\choice ', (), '\\.+']),
            ('correctchoice', ['\\CorrectChoice ', (), '\\.+']),
            #'shuffle', ['<shuffleanswers>1</shuffleanswers> <single>true</single>', (), '.']),
            ('titledshortanswer', [['title'], (), ['solution'], end]),
            #'titlednumerical', [['titled'], (), ['solution'], end]),
            #'titledtruefalse', [['titled'], (), '</question>', end]),
            ('titledmultichoice', [['title'], (), ['choices'], end]),
            ('titledessay', [['title'], (), end]),
            ('shortanswer', ['\\question', (), ['solution'], 'end']),
            #'numerical':['\\question', (), ['solution'], 'end']),
            #'truefalse', ['<question type="truefalse">', (), '</question>', '']),
            ('multichoice', ['\\question', (), ['choices'], end]),
            ('essay', ['\\question', (), 'end']),
            ('unknown', ['\\', (), '\\s+']),
            ('unknownarg', ['{', (), '}', '\\s+'])
        ])
    })
    return plugin


def unload():
    pass



