# Commands

Commands are special strings that appear after `pyxam!` in comments of template files. These commands are written in
comments so that their appearance is universal regardless of the format they appear in. When a command is found the
entire comment is replaced with the return value of the command. Creating your own function is easy:
```python
# Create a command function
def hello_world_command():
    """
    Command description
    """
    print('Hello World')
    return ''
# Add the command
bang.add_command('hello_world', hello_world_command)
```
Usage in a file would look something like:
```
# pyxam!hello_world
```