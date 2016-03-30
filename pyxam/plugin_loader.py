# Author: Eric Buss <ebuss@ualberta.ca> 2016
"""
# Module plugin_loader
"""
import config
import logging
import os
import options


class PluginError(Exception):
    pass


# A map of all currently loaded plugins
_plugins = {}


def load_plugins():
    """
    Call the load function on all plugins in the appropriate order.
    :return: None
    """
    options.add_option('plugins', '-plg', 'List all currently loaded plugins', False, bool)
    plugins = [plugin[:-3] for plugin in os.listdir(config.plugin_directory) if plugin.endswith('.py')]
    # Put logging at the start of list
    plugins.insert(0, plugins.pop(plugins.index('_logging')))
    # Put options at the end of the list
    plugins.append(plugins.pop(plugins.index('_options')))
    # Attempt to load plugins
    for plugin in plugins:
        try:
            exec('import plugins.{}; load(plugins.{}.load())'.format(plugin, plugin))
            logging.info('Loaded ' + plugin)
        except AttributeError:
            raise PluginError('Failed to load ' + plugin + ': plugin has no load function')
        except TypeError:
            raise PluginError('Failed to load ' + plugin + ': plugin returned an invalid plugin signature or was None')
    # Display plugin list and exit
    if not options.state.api():
        print('Successfully loaded', len(_plugins), ' plugins.\n')
    if options.state.plugins():
        for plugin_set in _plugins.values():
            for author, plugin in plugin_set.items():
                print('\t' + plugin['name'] + ' by ' + author + '\n\t\t' + plugin['description'])
        exit()


def unload_plugins():
    """
    Call the unload function on all plugins.
    :return: None
    """
    plugins = sorted((plugin[:-3] for plugin in os.listdir(config.plugin_directory) if plugin.endswith('.py')))
    for plugin in plugins:
        try:
            exec('import plugins.{}; plugins.{}.unload()'.format(plugin, plugin))
            logging.info('Unloaded ' + plugin)
        except AttributeError:
            pass


def load(signature):
    """
    Called on the return value of a plugin. Should return a valid signature.
    :param signature: The return value of the plugin's load function
    :return: None
    """
    name, author, description = signature
    _plugins[name] = {author: description}