
# Module bang

This module pre processes the template file and runs all inline commands prior to weaving.

Commands can be thought of in the same way as preprocessor directives in c. These commands will define a command which
if seen in the template file will be replaced with the return values of a function specified by the command. Commands
can have arguments but importantly are not reprocessed. All commands should appear in a comment block of the format
being worked with and must be preceeded with the `pyxam!` prefix.

An example usage of a mock command named `cmd`:

```
This is template file
# This is a normal comment
Some more text
# pyxam!cmd
That last comment was a command
```

***
**add_command**(*name, command*)



Add a name, command pair to commands

`name`  The name of the command
`command`  The command function

This function is meant to be used by plugin files in order to add commands. Commands must take an argument which is
whatever portion of the comment was not part of the command call. Here is an example implementation of a mock
command `Hello World` which replaces all instances of `pyxam!hello world` with `Hello World!!!`:

```python
import bang

**hello_world**(*args*)


    return 'Hello World!!!'

bang.add_command('hello world', hello_world)
```

***
**run_commands**()


Parses the template, runs all matched commands. The result of the command replaces the command call in the template.
The resulting string is copied to the tmp directory and the template option is pointed towards the new file
