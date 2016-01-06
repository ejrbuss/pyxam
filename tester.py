#!/usr/bin/env python3
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
# Constants
#

CONST_TMP = 'examples/testing'
CONST_STR = 'Hello World!'
CONST_SOLUTION_POSTFIX = '_solution'

#
# Main
#

def main():
    _unittest.main()

#
# Unit Tests
#

class test_pyxam_methods(_unittest.TestCase):

    # tex_match tests

    def test_tex_match_1(self):
        prefix = 'prefix'
        buffer = '\\' + prefix + '{' + CONST_STR + '}'
        self.assertEqual(_pyxam.tex_match(buffer, prefix), None) 

    # read tests

    def test_read_1(self):
        self.assertEqual(_pyxam.read('examples/Hello World.tex'),
                         CONST_STR)
    def test_read_2(self):
        self.assertRaises(FileNotFoundError, _pyxam.read, '^^^')
                         
    def test_read_3(self):
        self.assertRaises(IsADirectoryError, _pyxam.read, 'examples')

    # write tests

    def test_write_1(self):
        _pyxam.write(CONST_TMP, CONST_STR, False)
        self.assertEqual(_pyxam.read(CONST_TMP + '.tex'), CONST_STR)
        _pyxam.remove_file(CONST_TMP + '.tex')

    def test_write_2(self):
        _pyxam.write(CONST_TMP, CONST_STR, True)
        self.assertEqual(_pyxam.read(CONST_TMP + '.tex'), CONST_STR)
        self.assertEqual(_pyxam.read(CONST_TMP + CONST_SOLUTION_POSTFIX +
                                     '.tex'), '\\printanswers\n' + CONST_STR)
        _pyxam.remove_file(CONST_TMP + '.tex')
        _pyxam.remove_file(CONST_TMP + CONST_SOLUTION_POSTFIX + '.tex')

    # remove_file tests

    def test_remove_file_1(self):
        _pyxam.write(CONST_TMP, CONST_STR, False)
        _pyxam.remove_file(CONST_TMP + '.tex')
        self.assertRaises(FileNotFoundError, _pyxam.read, CONST_TMP + 
                                                        '.tex')

    def test_remove_file_2(self):
        self.assertRaises(FileNotFoundError, _pyxam.remove_file,
                          '^^^')

    def test_remove_file_3(self):
        self.assertRaises(IsADirectoryError, _pyxam.remove_file,
                          'examples')
    # rmove_dir tests

    def test_remove_dir_1(self):
        _pyxam.create_tmp_dir(CONST_TMP)
        _pyxam.remove_dir(CONST_TMP)
        self.assertRaises(FileNotFoundError, _pyxam.read, CONST_TMP)

    def test_remove_dir_2(self):
        self.assertRaises(FileNotFoundError, _pyxam.remove_dir, '^^^')

    def test_remove_dir_3(self):
        self.assertRaises(NotADirectoryError, _pyxam.remove_dir, 
                          'examples/Hello World.tex')

    # create_tmp_dir tests
    
   # def test_create_tmp_dir(self):
    


#
# Examples
#

if __name__ == '__main__':
    main()
