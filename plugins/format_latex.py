from formatter import add_format

# TODO Finish Latex format

plugin = {
    'name': 'latexformat',
    'author': 'ejrbuss',
    'description': 'LaTeX markup format for creating documents with scientific and mathematical notation'
}


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
        'format': {
            ''
            'comment': ['%', (), '\n'],
            'title' : ['\\title{', (), '}', '[^\\s]*\\'],
            'author': ['\\author{', (), '}', '[^\\s]*\\'],
            'question': ['\\question ', (), '(\\[^\\s]*question)|(\\end{questions})'],
            'solution': ['\\begin{solution}', (), '\\end{solution}', ''],
            'choice': ['\\choice ', (), '[^\\s]*\\'],
            'correctchoice': ['\\CorrectChoice ', (), '[^\\s]*\\'],
        }
    })
    return plugin


def unload():
    pass



