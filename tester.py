#!/usr/bin/env python
# Author: Eric Buss <ebuss@ualberta.ca>

"""
Tester for pyxam
"""

#
# Imports
#

import unittest as _unittest
import pyxam as _pyxam

#
# Main
#

def main():
    _unittest.main()

#
# Unit Tests
#

class TestPyxamMethods(_unittest.TestCase):

    # read tests

    def test_read_1(self):
        self.assertEqual(_pyxam.read('examples/Hello World.tex')
                         , 'Hello World!')
    def test_read_2(self):
        self.assertRaises(FileNotFoundError, _pyxam.read, '^^^')
                         
    def test_read_3(self):
        self.assertRaises(PermissionError, _pyxam.read, 'examples')

    # write tests

    def test_write(self):
        self.assertEqual('foo'.upper(), 'FOO')
#
# Examples
#

if __name__ == '__main__':
    main()
