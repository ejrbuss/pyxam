#!/usr/bin/env python3
import os
import setuptools


def isfile(path):
    return os.path.isfile(path) and not os.path.basename(path).startswith('.')


def isdir(path):
    print(os.path.basename(path))
    return os.path.isdir(path) and not os.path.basename(path).startswith('.')


def listdir(path):
    if isdir(path):
        return [os.path.join(path, p) for p in os.listdir(path) if not p.startswith('.')]
    return []


def get_data_files():
    paths = list()
    paths.append((os.path.join('pyxam', 'templates'), listdir(os.path.join('pyxam', 'templates'))))
    paths.append((os.path.join('docs', 'build'), []))
    docs = listdir(os.path.join('docs', 'source'))
    paths.append((os.path.join('docs', 'source'), [path for path in docs if isfile(path)]))
    for path in docs:
        if isdir(path):
            paths.append((os.path.join('docs', 'source', os.path.basename(path)), [p for p in listdir(path) if isfile(p)]))
    return paths


setuptools.setup(
    name='Pyxam',
    entry_points={'console_scripts': ['pyxam = pyxam.pyxam:main']},
    version='0.3.5',
    author='Eric Buss',
    author_email='ebuss@ualberta.ca',
    url='https://github.com/balancededge/pyxam',
    packages=['pyxam', os.path.join('pyxam', 'plugins')],
    data_files=get_data_files(),
    description='Recreation of the R exam package functionality in python',
    long_description=open('README.md').read(),
)



