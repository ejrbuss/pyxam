import formatter

plugin = {
    'name': 'token format',
    'author': 'ejrbuss',
    'description': 'Format for viewing files as pure pyxam tokens'
}


def processor(token_tree):
    return token_tree

format_ = {
    'extensions': ['tokens', 'token'],
    'description': plugin['description'],
    'parser_preprocessor': processor,
    'parser_postprocessor': processor,
    'composer_preprocessor': processor,
    'composer_postprocessor': processor,
    'format': {
        'header': ['header: ', (), '[^\\s]*:'],
        'footer': ['footer: ', (), '[^\\s]*:'],
        'comment': ['comment: ', (), '[^\\s]*:'],
        'title' : ['title: ', (), '[^\\s]*:'],
        'author': ['author: ', (), '[^\\s]*:'],
        'type' : ['type: ', (), '[^\\s]*:'],
        'introduction': ['introduction: ', (), '[^\\s]*:'],
        'solution': ['solution: ', (), '[^\\s]*:'],
        'choice': ['choice: ', (), '[^\\s]*:'],
        'correctchoice': ['correctchoice:', (), '[^\\s]*:'],
        'prompt': ['prompt: ', (), '[^\\s]*:'],
        'question': ['question: ', (), 'question:'],
        'conclusion': ['conclusion: ', (), '[^\\s]*:'],
        'shuffle': ['shuffle: ', (), '[^\\s]*:']
    }
}


def load():
    formatter.add_format(format_)
    return plugin


def unload():
    pass



