# Formats

Pyxam uses formats to parse files and compose them. They are simultanesouly the most complex and most powerful structure
in Pyxam. When parsing a format will be matched based on a provided list of compatible file extensions.Then the file will
have tokenized based off a set of tokens provided by the format. When exporting a tree of tokens is converted into raw
text by writing out your provided tokens. This means that a format specification allows that format to be imported into
any other format and exported into from any other format. An example of what a basic formatter looks like:
```python
# Add a format
formatter.add_format({
    # The name of the format
    'name': 'Format name',
    # A list of compatible extensions
    'extensions': ['extension'],
    # A set of processors that are run before and after the parsing/composing processes
    # They pass_through filter is a filter that does nothing to the input
    'parser_preprocessor': filter.pass_through,
    'parser_postprocessor': filter.pass_through,
    'composer_preprocessor': filter.pass_through,
    'composer_postprocessor': filter.pass_through,
    # Optional arguments that specify a right and left parentheses to respect when parsing
    'left_paren': '{',
    'right_paren': '}',
    # The list of tokens that specify this format
    # This is often specified with an OrderedDict if the order in parsing attempts are made 
    # is important.
    'format': collections.OrderedDict([
        # A token is composed of a name and a list which defines it.
        # This definition can contain strings. These will be matched directly.
        # The last item in the definition is a regex that speicifies the end of the token.
        # Whatever matches this regex will not be considered part of the token.
        ('basic token', ['Matches this string', '.']),
        # An empty tuple matches arbitrary content.
        # This content could be other tokens or just a pure string
        ('input', ['<tag denoting start of input>', (), '<tag denoting end>', '.']),
        # A token can reference other tokens and require they be a part of their content.
        # This reference is denoted by placing the token name inside a list.
        ('basic token and input', [['basic token'], ['input'], '.']),
        # If multiple token names are given in a list this acts as an or statement
        ('basic token or input' [['basic token', 'input'], '.']),
        # The tokens $ and verbatim are special because their contents are always raw strings
        # even if their content matches another token.
        ('$', ['The Following string will be raw', (), '.'])
    ])
})
```
Once a format is specified it can be used to construct an AST. The parsed and composed AST are viewable if the `-d`
debug option is given. They appear in the temporary folder. An example AST:
```
[
questions:
	question:
		multichoice:
			title:
				question
			prompt:
				Which of the following are even?
			choices:
				correctchoice:
					0
				choice:
					-45
				correctchoice:
					12
]
```
The `filters.py` file contains functions for working with the AST to prepare if for other formats.