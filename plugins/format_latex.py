import re
from formatter import add_format
from formatter import Token
from filters import promote_nested
from collections import OrderedDict

# TODO Finish Latex format

plugin = {
    'name': 'latexformat',
    'author': 'ejrbuss',
    'description': 'LaTeX markup format for creating documents with scientific and mathematical notation'
}

end = r'(\\question)|(\\titledquestion)|(\\end{questions})'

def processor(ast):
    return ast


def parser_preprocessor(src):
    src = src.replace('\\question', '\\titledquestion{question}')
    src = promote_nested(src, '\\fullwidth', '{', '}')
    return src


def parser_postprocessor(intermediate):
    def process(definition, question):
        for token in definition:
            if hasattr(token, 'definition'):
                process(token.definition, token.name in ['essay', 'shortanswer', 'multichoice'])
        if question:
            title, prompt = None, []
            while len(definition) > 0 and (not hasattr(definition[0], 'name') or definition[0].name in ['$', 'img', 'title']):
                if hasattr(definition[0], 'name') and definition[0].name == 'title':
                    title = definition.pop(0)
                else:
                    prompt.append(definition.pop(0))
            definition.insert(0, Token('prompt', prompt, None, ''))
            if title is not None:
                definition.insert(0, title)
    process(intermediate.ast, False)
    return intermediate


def load():
    add_format({
        'extensions': ['latex', 'tex'],
        'description': plugin['description'],
        'parser_preprocessor': parser_preprocessor,
        'parser_postprocessor': parser_postprocessor,
        'composer_preprocessor': processor,
        'composer_postprocessor': processor,
        'format': OrderedDict([
            ('comment', ['%', (), '\n']),
            ('$', ['$', (), '$', '.']),
            ('questions', ['\\begin{questions}', (), '\\end{questions}', '.']),
            ('points', ['[', (), ']', '.']),
            ('title', ['question{', (), '}', '.']),
            #'prompt', ['<questiontext format="html"> <text> <![CDATA[', (), ']]> </text> </questiontext>', '.']),
            ('solution', ['\\begin{solution}', (), '\\end{solution}', '.']),
            ('img', ['\\includegraphics{', (), '}' '.']),
            ('choices', ['\\begin{choices}', (), '\\end{choices}', '.']),
            ('choice', ['\\choice ', (), r'(\\choice)|(\\CorrectChoice)']),
            ('correctchoice', ['\\CorrectChoice ', (), r'(\\choice)|(\\CorrectChoice)']),
            #'shuffle', ['<shuffleanswers>1</shuffleanswers> <single>true</single>', (), '.']),
            ('multichoice', ['\\titled', ['title'], (), ['choices'], (), end]),
            ('shortanswer', ['\\titled', ['title'], (), ['solution'], (), end]),
            #'titlednumerical', [['titled'], (), ['solution'], end]),
            #'titledtruefalse', [['titled'], (), '</question>', end]),
            ('essay', ['\\titled', ['title'], (), end]),
            ('unknownarg', ['{', (), '}', '\\s+']),
            ('unknown', ['\\', (), '\\s+|\{'])
        ])
    })
    return plugin


def unload():
    pass



