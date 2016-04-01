# Options

Pyxam command line options are flexible and dynamic. All command line options added prior to the `_options.py` file will
be shown in the help message, and all options are parsed the moment they are available. This means you can add an option
in the same line of code where you test to see if the user has specified the option. In fact this is an intended usage
as the `add_option` function returns the value of the option. Below is an example of this design pattern:
```python
# The last two arguments are the default value and the type
if options.add_option('option_name', '-flag', 'A description', False, bool):
    # Run your plugin
```
In addition to parsing command line arguments options can also be overriden at anytime by accessing them through the
`state` object. This object maps the name of the option to a function that can be used to set the option and retrieve
its value. For example:
```python
# Add an option that gets a string from the user
options.add_option('your_name', '-yn', 'Please provide your name', 'N/A', str)
# An example of retrieving that string
name = options.state.your_name()
# An example of setting that string
options.state.your_name('Bob')
```
Options are extremely useful when trying to modify Pyxam's behavior with a plugin. Not only can you create your own and
use them as global variables, but by hooking into the process list before and after a function you can change the option
state that function runs in. This technique is used in the `format_pdf.py` plugin for example to make sure the template
file is composed as a LaTeX file despite the user specifying pdf as their output format.