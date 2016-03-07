# Author: Eric Buss <ebuss@ualberta.ca> 2016
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
    plugins = [plugin[:-3] for plugin in os.listdir('plugins') if plugin.endswith('.py')]
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
        except PluginError:
            raise PluginError('Failed to load ' + plugin + ': plugin returned an invalid plugin signature')
        except TypeError:
            raise
            raise PluginError('Faield to laod ' + plugin + ': plugin returned None')
    # Display plugin list and exit
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
    plugins = sorted((plugin[:-3] for plugin in os.listdir('plugins') if plugin.endswith('.py')))
    for plugin in plugins:
        try:
            exec('import plugins.{}; plugins.{}.unload()'.format(plugin, plugin))
            logging.info('Unloaded ' + plugin)
        except AttributeError:
            raise PluginError('Failed to unload ' + plugin + ': plugin has no unload function')


def load(signature):
    """
    Called on the return value of a plugin. Should return a valid signature.
    :param signature: The return value of the plugin's load function
    :return: None
    """
    if ('name' and 'author' and 'description') in signature:
        # Store plugins by author name to help prevent collisions
        _plugins[signature['name']] = {signature['author']: signature}
    else:
        raise PluginError()