#!/usr/bin/env python3
from setuptools import setup

setup(
    name='Pyxam',
    entry_points={'console_scripts': ['pyxam = pyxam.pyxam:main']},
    version='0.3.5',
    author='Eric Buss',
    author_email='ebuss@ualberta.ca',
    url='https://github.com/balancededge/pyxam',
    packages=['pyxam', 'pyxam/plugins'],
    data_files=[('pyxam/templates', ['pyxam/templates/docs.html', 'pyxam/templates/exam.html'])],

    description='Recreation of the R exam package functionality in python',
    long_description=open('README.md').read(),
)
