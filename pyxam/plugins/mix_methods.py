# Author: Eric Buss <ebuss@ualberta.ca> 2016
"""
# Plugin mix_methods

"""
import random
import exporter


# Mix methods by ejrbuss: adds sequence and random mixing methods
signature = 'mix methods', 'ejrbuss', 'adds sequence and random mixing methods'


def sequence_mix(versions, data):
    """

    :param versions:
    :param data:
    :return:
    """
    # Mix data
    for n, row in enumerate(data):
        exporter.mix(n % versions, row)


def random_mix(versions, data):
    """

    :param versions:
    :param data:
    :return:
    """
    # Mix data
    for row in data:
        exporter.mix(random.randint(versions), row)


def load():
    # Add sequence method
    exporter.add_method('sequence', sequence_mix)
    # Add random mix
    exporter.add_method('random', random_mix)
    # Return signature
    return signature
