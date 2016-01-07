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
import csv_reader as _csv_reader

#
# Constants
#

CONST_TMP = 'examples/testing'
CONST_STR = 'Hello World!'
CONST_PREFIX = 'prefix'
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
        buffer = '\\' + CONST_PREFIX + '{' + CONST_STR + '}'
        args = _pyxam.tex_match(buffer, CONST_PREFIX)
        self.assertEqual(buffer[args[0][0]:args[0][1]], CONST_STR)

    def test_tex_match_2(self):
        self.assertEqual(_pyxam.tex_match(CONST_STR, CONST_PREFIX), [])

    def test_tex_match_3(self):
        buffer = '\\' + CONST_PREFIX + '{' + CONST_STR + '1}' + CONST_STR
        buffer = buffer + '\n\\' + CONST_PREFIX + '{' + CONST_STR + '2}'
        args = _pyxam.tex_match(buffer, CONST_PREFIX)
        self.assertEqual(buffer[args[0][0]:args[0][1]], CONST_STR + '1')
        self.assertEqual(buffer[args[1][0]:args[1][1]], CONST_STR + '2')

    def test_tex_match_4(self):
        buffer = '\\\\' + CONST_PREFIX + '{' + CONST_STR + '}'
        self.assertEqual(_pyxam.tex_match(buffer, CONST_PREFIX), [])

    def test_tex_match_5(self):
        buffer = '\\' + CONST_PREFIX + '{' + CONST_STR + '{}}'
        args = _pyxam.tex_match(buffer, CONST_PREFIX)
        self.assertEqual(buffer[args[0][0]:args[0][1]], CONST_STR + '{}')

    # read tests

    def test_read_1(self):
        self.assertEqual(_pyxam.read('examples/Hello World.tex'),
                         CONST_STR)
    def test_read_2(self):
        self.assertRaises(FileNotFoundError, _pyxam.read, '^^^')
                         
    def test_read_3(self):
        self.assertRaises(Exception, _pyxam.read, 'examples')
        # Check against Exception because depending on OS
        # IsADirectoryError or PermissionError can occur

    # write tests

    def test_write_1(self):
        _pyxam.write(CONST_TMP, CONST_STR)
        self.assertEqual(_pyxam.read(CONST_TMP + '.tex'), CONST_STR)
        _pyxam.remove_file(CONST_TMP + '.tex')

    def test_write_2(self):
        _pyxam.write(CONST_TMP, CONST_STR, s=True)
        self.assertEqual(_pyxam.read(CONST_TMP + '.tex'), CONST_STR)
        self.assertEqual(_pyxam.read(CONST_TMP + CONST_SOLUTION_POSTFIX +
                                     '.tex'), '\\printanswers\n' + CONST_STR)
        _pyxam.remove_file(CONST_TMP + '.tex')
        _pyxam.remove_file(CONST_TMP + CONST_SOLUTION_POSTFIX + '.tex')

    # remove_file tests

    def test_remove_file_1(self):
        _pyxam.write(CONST_TMP, CONST_STR)
        _pyxam.remove_file(CONST_TMP + '.tex')
        self.assertRaises(FileNotFoundError, _pyxam.read, CONST_TMP + 
                                                        '.tex')

    def test_remove_file_2(self):
        self.assertRaises(FileNotFoundError, _pyxam.remove_file,
                          '^^^')
    
    def test_remove_file_3(self):
        self.assertRaises(Exception, _pyxam.remove_file,
                          'examples')
        # Check against Exception because depending on OS
        # IsADirectoryError or PermissionError can occur
        
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

    def test_remove_dir_4(self):
        _pyxam.create_tmp_dir(CONST_TMP)
        _pyxam.write(CONST_TMP + '/' + CONST_STR + '.tex', CONST_STR)
        _pyxam.remove_dir(CONST_TMP)
        self.assertRaises(FileNotFoundError, _pyxam.read, CONST_TMP)

    # create_tmp_dir tests
    
    def test_create_tmp_dir(self):
        _pyxam.create_tmp_dir(CONST_TMP)
        self.assertRaises(Exception, _pyxam.read, CONST_TMP)
        _pyxam.remove_dir(CONST_TMP)

    # student tests

    def test_student(self):
        student = _csv_reader.student(CONST_STR, 1) 
        self.assertEqual(CONST_STR, student.name)
        self.assertEqual(1, student.number)
#
# Examples
#

if __name__ == '__main__':
    main()
