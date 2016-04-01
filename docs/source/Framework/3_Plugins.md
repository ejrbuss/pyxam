# Plugins

Plugins are python files that are loaded dynamically during the `load_plugin` process and can run whatever code they
like during that time. To add a plugin simply add a `.py` file to the `plugins` folder. In order for the plugin to load
however it needs to have the proper signature. All plugins must have a `load` and `unload` function nd their `load`
function must return a signature with some meta information. This is to help ensure that only plugins are in the plugins
folder and automatically build documentation and command line options. An example of a simple plugin:
```python
# Plugin signature
plugin = {
        'name': 'example plugin',
        'author': 'ejrbuss',
        'description': 'An example plugin'
}

def load():
    # Put your plugin code here
    return plugin
    
def unload():
    pass
```