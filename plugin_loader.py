import logging
import os
from importlib.machinery import SourceFileLoader


class PluginError(Exception):
    pass


_plugins = {}


def load_plugins():
    plugins = [plugin[:-3] for plugin in os.listdir('plugins') if plugin.endswith('.py')]
    plugins.insert(0, plugins.pop(plugins.index('_logging')))   # Put logging at the start of list
    plugins.append(plugins.pop(plugins.index('_options')))      # Put options at the end of the list
    for plugin in plugins:
       # try:
            #load(SourceFileLoader('plugins.' + plugin, 'plugins/' + plugin + '.py').load_module().load())
            #print(plist)
            exec('import plugins.{}; load(plugins.{}.load())'.format(plugin, plugin))
            logging.info('Loaded ' + plugin)
        #except AttributeError:
        #    raise PluginError('Failed to load ' + plugin + ': plugin has no load function')
        #except PluginError:
        #    raise PluginError('Failed to load ' + plugin + ': plugin returned an invalid plugin signature')


def unload_plugins():
    plugins = sorted((plugin[:-3] for plugin in os.listdir('plugins') if plugin.endswith('.py')))
    for plugin in plugins:
        try:
            exec('import plugins.{}; plugins.{}.unload()'.format(plugin, plugin))
            logging.info('Unloaded ' + plugin)
        except AttributeError:
            raise PluginError('Failed to unload ' + plugin + ': plugin has no unload function')


def load(plugin):
    if ('name' and 'author' and 'description') in plugin:
        _plugins[plugin['name']] = {plugin['author']: plugin}
    else:
        raise PluginError()