# Author: Eric Buss <ebuss@ualberta.ca> 2016
"""
# Plugin _options

This plugin is considered a core plugin (indicated by the underscore in its name) it should only be replaced or removed
if the user knows what they are doing.



This plugin defines the core set of command line options used by Pyxam. In addition to adding these options _options
also manages a few commands:
 - `solutions` if provided will cause _options to hook a rerun function to the end of the process list
 - `version` if provided will cause _options to print the version number then exit
 - `list` if provided will cause _options to print all formats then exit
 - `help` if provided will cause _options to pritn all options then exit
The [plugin_loader](%/Modules/plugin_loader) will always load _options last so that other Plugins that add formats or
options can be seen by _options.

"""
import process_list
import formatter
import options
import pyxam

# option config by ejrbuss: The default options for pyxam
signature = 'option config', 'ejrbuss', 'The default options for pyxam'


def load():
    """
    Loads the following [options](%/Modules/options.html):
     - `out -o` Set the output directory
     - `tmp -tmp` Set the temporary directory
     - `figure -fig` Set the figure directory
     - `number -n` Set the number of exams to generate
     - `title -t` Set the title of the exam
     - `format -f` Set the format of the exam
     - `shell -shl` Set the shell used to weave the exam
     - `method -m` Set the selection method for population mixing
     - `population -p` Set the class list
     - `alphabetize -a` Enable lettered versioning
     - `debug -d` Disable file cleanup
     - `solutions -s` Enable solutions
     - `version -v` Show the version number
     - `list -ls` List all available formats
     - `help -h` Show a help message
     Manages the `solutions`, `version`, `list`, and `help` commands as explained above.

    :return: plugin signature
    """
    #                   NAME           FLAG    DESCRIPTION                            DEFAULT    TYPE
    options.add_option('out',         '-o',   'Set the output directory',            'out',      str)
    options.add_option('tmp',         '-tmp', 'Set the temporary directory',         'tmp',      str)
    options.add_option('figure',      '-fig', 'Set the figure directory',            'fig',      str)
    options.add_option('number',      '-n',   'Set the number of exams to generate', 1,          int)
    options.add_option('title',       '-t',   'Set the title of the exam',           'exam',     str)
    options.add_option('format',      '-f',   'Set export format',                   'tex',      str)
    options.add_option('shell',       '-shl', 'Set shell used to weave the exam',    'python',   str)
    options.add_option('method',      '-m',   'Set selection method for CSVs',       'sequence', str)
    options.add_option('population',  '-p',   'Set class list',                      None,       str)
    options.add_option('alphabetize', '-a',   'Enable lettered versioning',          False,      bool)
    options.add_option('debug',       '-d',   'Disable file cleanup',                False,      bool)
    # Run once and produce solutions then run again widthout solutions
    if options.add_option('solutions',   '-s',   'Enable soultions',                 False,      bool):
        process_list.run_before('goodbye', rerun)
    # Display version number via the welcome message then exit
    if options.add_option('version','-v',   'Show the version number',             False,      bool):
        if options.state.api():
            pyxam.welcome()
    # Display a list of all available formats then exit
    elif options.add_option('list',   '-ls',  'List all available formats',          False,      bool):
        formats = set(fmt['extensions'][0] for key, fmt in formatter.formats.items())
        for fmt in set(formats):
            print(formatter.formats[fmt]['extensions'][0] + ':\n\t' + formatter.formats[fmt]['description'])
    # Display a help message then exit
    elif options.add_option('help',     '-h',   'Show a help message',                 False,      bool):
        div = '-' * max(len(line) for line in options.get_help().split('\n'))
        print('\n'.join([div, 'Pyxam Options'.center(len(div)), div, options.get_help(), div]))
    # Return signature
    else:
        return signature
    # Exit
    exit()


def rerun():
    """
    Reruns pyxam with the solutions flag disabled if previously enabled. This is hooked to the
    [process_list](%/Modules/process_list.html) when the solutions flag is set so that two sets of exams are produced,
    one with solutions and one without. This function exits on close.
    """
    args = pyxam.store_args()
    if '--solutions' in args:
        args.remove('--solutions')
    if '-solutions' in args:
        args.remove('-solutions')
    if '-s' in args:
        args.remove('-s')
    pyxam.start(args, options.state.api())
    exit()




