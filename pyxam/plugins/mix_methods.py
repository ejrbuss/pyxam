# Author: Eric Buss <ebuss@ualberta.ca> 2016
"""
# Plugin mix_methods
Adds mixing methods to the [exporter](%/Modules/exporter.html).
"""
import random
import exporter


signature = 'mix methods', 'ejrbuss', 'adds sequence and random mixing methods'


def sequence_mix(versions, data):
    """
    Repeatedly loops through the versions alongside the data until every student is assigned an exam.
    :param versions: The number of exam versions
    :param data: An array of student data
    """
    # Mix data
    for n, row in enumerate(data):
        exporter.mix(n % versions, row)


def random_mix(versions, data):
    """
    Selects a random exam for each row of data.
    :param versions: The number of exam versions
    :param data: An array of student data
    """
    # Mix data
    for row in data:
        exporter.mix(random.randint(versions), row)


def load():
    """
    Adds the sequence and random mixing methods to the exporter.

    :return: plugin signature
    """
    # Add sequence method
    exporter.add_method('sequence', sequence_mix)
    # Add random mix
    exporter.add_method('random', random_mix)
    # Return signature
    return signature