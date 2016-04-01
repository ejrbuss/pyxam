# Author: Eric Buss <ebuss@ualberta.ca> 2016
"""
# Module util_classes

Provides utility classes and functinos to other Modules.
"""
import inspect


class Map(dict):
    """
    A custom dictionary which can be accessed with index notation and function notation. Taken from a
    [stackoverflow](http://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary)
    post by [epool](http://stackoverflow.com/users/845296/epool). Example usage:
    ```python
        # Can construct using a dictionary/named args
        m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
        # Access using function notation
        assert(m.firstname() == 'Eduardo')
        # Access using index notation
        assert(m['lastname'] == 'Pool')
    ```

    """
    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v
        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    # Magic

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]


def same_caller(cache={}):
    """

    :param cache:
    :return:
    """
    caller, caller_caller = inspect.stack()[1][3], inspect.stack()[2][3]
    same = caller in cache and cache[caller] == caller_caller
    cache[caller] = caller_caller
    return same