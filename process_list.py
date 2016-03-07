# Author: Eric Buss <ebuss@ualberta.ca> 2016


# Core Process List
_process_list = []


def ready():
    """
    :return: True as long as there are items in the process list
    """
    return bool(_process_list)


def append(process):
    """
    Append a process to the end of the process list, or if the provided argument is a list, append all the items to
    the process list.
    :param process:
    :return: None
    """
    global _process_list
    if not isinstance(_process_list, list):
        process = [process]
    _process_list += process


def run_after(process, hook):
    """
    Add a hook to run after a given process.
    :param process: The string name of the process to hook
    :param hook: A function to run
    :return: None
    """
    _process_list.insert([proc.__name__ for proc in _process_list].index(process) + 1, hook)


def run_before(process, hook):
    """
    Add a hook to run before a given process.
    :param process: The string name of the process to hook
    :param hook: A function to run
    :return: None
    """
    _process_list.insert([proc.__name__ for proc in _process_list].index(process), hook)


def consume(arg=None):
    """
    Run the next process in the process list with any provided arguments.
    :param arg: Arguments
    :return: Arguments for the next process
    """
    return _process_list.pop(0)(arg) if arg is not None else _process_list.pop(0)()