# Author: Eric Buss <ebuss@ualberta.ca> 2016
# Python Imports


import io
import os
import unittest


# Global Variables


DEBUG = False # Set this to True to see logs from running the tester


# Module Imports


import core
import exporter
import fileutil
import logger
import populationmixer
import pyxamopts
import templater
import weaver


STR = 'Hello World!'
TST = 'examples/test.txt'
NAF = '\\\\'


def init():
    if not DEBUG:
        logger.DEBUG = logger.LEVEL.SILENT
    unittest.main()


class CoreTester(unittest.TestCase):

    def test_index_1(self):
        options = pyxamopts.PyxamOptions()
        self.assertEqual(core.index(3, options), '4')

    def test_index_2(self):
        options = pyxamopts.PyxamOptions()
        options.alphabetize = True
        self.assertEqual(core.index(6, options), 'G')

    def test_check_dependencies(self):
        core.DEPENDENCIES = [NAF]
        self.assertRaises(SystemExit, core.check_dependencies)

    def test_make_solutions(self):
        self.assertEqual(core.make_solutions('\\documentclass{'), '\\documentclass[answers]{')


class ExporterTester(unittest.TestCase):

    def test1(self):
        return


class FileutilTester(unittest.TestCase):

    def test_read_1(self):
        fileutil.write(TST, STR)
        self.assertEqual(fileutil.read(TST), STR)

    def test_read_2(self):
        self.assertRaises(FileNotFoundError, fileutil.read, NAF )

    def test_write(self):
        fileutil.write(TST, STR)
        self.assertEqual(fileutil.read(TST), STR)

    def test_remove(self):
        fileutil.remove(TST)
        self.assertRaises(FileNotFoundError, fileutil.read, TST )
        fileutil.write(TST, STR)

    def test_make_temp(self):
        fileutil.make_temp('test')
        self.assertRaises(PermissionError if os.name == 'nt' else FileNotFoundError, fileutil.read, 'test')
        fileutil.remove(fileutil.TEMP)
        self.assertRaises(FileNotFoundError, fileutil.read, 'test' )

    def test_make_out(self):
        fileutil.make_out('test')
        self.assertRaises(PermissionError if os.name == 'nt' else FileNotFoundError, fileutil.read, 'test')
        fileutil.remove(fileutil.OUT)
        self.assertRaises(FileNotFoundError, fileutil.read, 'test' )

    def test_copy_out(self):
        fileutil.make_temp('test_temp')
        fileutil.make_out('test_out')
        fileutil.write_temp('test.txt', STR)
        fileutil.copy_out('test.txt')
        self.assertEqual(fileutil.read(fileutil.OUT + '/' + 'test.txt'), STR)
        fileutil.remove(fileutil.TEMP)
        fileutil.remove(fileutil.OUT)

    def test_remove_temp(self):
        fileutil.make_temp('test')
        fileutil.remove_temp()
        self.assertRaises(FileNotFoundError, fileutil.read, 'test')

    def test_read_write_temp(self):
        fileutil.make_temp('test')
        fileutil.write_temp('test.txt', STR)
        self.assertEqual(fileutil.read_temp('test.txt'), STR)
        fileutil.remove('test')


class LoggerTester(unittest.TestCase):

    def test_log(self):
        cache = logger.DEBUG
        logger.DEBUG = logger.LEVEL.INFO
        logger.OUT = io.StringIO()
        logger.log('test', STR)
        self.assertEqual(logger.OUT.getvalue(), 'INFO@test:\n\t' + STR + '\n')
        logger.DEBUG = cache

    def test_to_file(self):
        cache = logger.DEBUG
        logger.DEBUG = logger.LEVEL.INFO
        logger.OUT = io.StringIO()
        logger.log('test', STR)
        logger.to_file('test', 'test')
        self.assertEqual(fileutil.read('test/test'), 'INFO@test:\n\t' + STR + '\n')
        fileutil.remove('test')
        logger.DEBUG = cache


class PopulationmixerTester(unittest.TestCase):

    def test1(self):
        return


class PyxamoptsTester(unittest.TestCase):

    def test_check(self):
        opts = pyxamopts.PyxamOptions()
        defaults = pyxamopts.PyxamOptions()
        opts.template = STR
        defaults.number = 10
        opts.number = None
        pyxamopts.check(opts, defaults)
        self.assertEqual(defaults.template, STR)
        self.assertEqual(defaults.number, 10)
        return


class TemplaterTester(unittest.TestCase):

    def test_pre_process(self):
        options = templater.pre_process('\\Parg{-n 3}')
        self.assertEqual( options.number, 3)
        self.assertEqual( options.sample, None)

    def test_pimport(self):
        fileutil.write(TST, STR)
        self.assertEqual(templater.pimport('\\Pimport{' + TST + '}', 1), '\n' + STR)

    def test_walk(self):
        self.assertEqual(templater.walk(TST), [TST])

    def test_parse_constant(self):
        self.assertEqual(templater.parse_constant('\\Pconst{STR}', 'STR', STR), STR)

    def test_clean(self):
        self.assertEqual(templater.clean(STR + '\\Parg{}'), STR)

    def test_tex_match(self):
        buffer = '\\' + STR + '{' + STR + '}'
        pairs = templater.tex_match(buffer, STR)
        self.assertEqual(buffer[pairs[0][0]:pairs[0][1]], STR)


class WeaverTester(unittest.TestCase):

    def test_weave(self):
        fileutil.make_temp('examples')
        fileutil.write(TST, '\Pexpr{4}')
        weaver.weave('test.txt', False, 'figure', 'python')
        self.assertEqual(fileutil.read_temp('test.tex'), '4\n')
        fileutil.remove('figure')
        fileutil.remove('examples/test.tex')
        fileutil.write(TST, STR)
        return

if __name__ == '__main__':
    init()