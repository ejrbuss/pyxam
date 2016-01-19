# Author: Eric Buss <ebuss@ualberta.ca> 2016
# Python Imports


import io
import os
import unittest


# Module Imports


import core
import exporter
import fileutil
import logger
import parser
import populationmixer
import pyxamopts
import templater
import weaver


# Global Variables


# Set this to True to see logs from running the tester
DEBUG = False
# Test string
STR = 'Hello World!'
# Test file
TST = 'examples/test.txt'
# Test invalid file
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
        core.DEPENDENCIES = [[NAF]]
        self.assertRaises(SystemExit, core.check_dependencies)

    def test_make_solutions(self):
        self.assertEqual(core.make_solutions('\\documentclass{'), '\\documentclass[answers]{')


class ExporterTester(unittest.TestCase):

    def test(self):
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
        self.assertRaises(PermissionError if os.name == 'nt' else IsADirectoryError, fileutil.read, 'test')
        fileutil.remove(fileutil.TEMP)
        self.assertRaises(FileNotFoundError, fileutil.read, 'test' )

    def test_make_out(self):
        fileutil.make_out('test')
        self.assertRaises(PermissionError if os.name == 'nt' else IsADirectoryError, fileutil.read, 'test')
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


class ParserTester(unittest.TestCase):

    def test_Question(self):
        question = parser.Question(
                '\\titledquestion{name}\ntext\\begin{choices}\n\\CorrectChoice A\n\\choice B\n'
                '\\choice C\n\\end{choices}')
        self.assertEqual(question.name, 'name')
        self.assertEqual(question.text, 'text')
        self.assertEqual(question.choices, ['B', 'C'])
        self.assertEqual(question.solution, 'A')
        self.assertEqual(question.type, 'multichoice')


class PopulationmixerTester(unittest.TestCase):

    def test_selector(self):
        selector = populationmixer.Selector([1,2,3,4], populationmixer.METHOD_LIST[1])
        self.assertEqual(selector.next(), 1)
        self.assertEqual(selector.next(), 2)
        self.assertEqual(selector.next(), 3)
        self.assertEqual(selector.next(), 4)
        self.assertEqual(selector.next(), 1)

    def test_insert_data(self):
        fileutil.make_temp('test3')
        fileutil.write_temp('test.tex', '\Pconst{STUDENT}')
        populationmixer.insert_data('test.tex', [STR])
        self.assertEqual(fileutil.read_temp('test-Hello World!.tex'), STR)
        fileutil.remove_temp()


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

    def test_command(self):
        command = templater.Command('\\command[arg]{content}', 0, 22)
        self.assertEqual(command.block, '\\command[arg]{content}')
        self.assertEqual(command.arg, 'arg')
        self.assertEqual(command.name, 'command')
        self.assertEqual(command.content, 'content')

    def test_command_clear(self):
        buffer = STR + '\\command[arg]{content}' + STR
        command = templater.Command(buffer, len(STR) + 0, len(STR) + 22)
        self.assertEqual(command.clear(buffer), STR + STR)

    def test_command_rewrap(self):
        buffer = STR + '\\command[arg]{content}' + STR
        command = templater.Command(buffer, len(STR) + 0, len(STR) + 22)
        self.assertEqual(command.rewrap(buffer, '1', '2'), STR + '1content2' + STR)

    def test_command_replace(self):
        buffer = STR + '\\command[arg]{content}' + STR
        command = templater.Command(buffer, len(STR) + 0, len(STR) + 22)
        self.assertEqual(command.replace(buffer, STR), STR + STR + STR)

    def test_section(self):
        section = templater.Section('\\begin[arg]{section}content\\end{section}', 0, 40)
        self.assertEqual(section.block, '\\begin[arg]{section}content\\end{section}')
        self.assertEqual(section.arg, 'arg')
        self.assertEqual(section.name, 'section')
        self.assertEqual(section.content, 'content')

    def test_section_clear(self):
        buffer = STR + '\\begin[arg]{section}content\\end{section}' + STR
        section = templater.Section(buffer, len(STR) + 0, len(STR) + 40)
        self.assertEqual(section.clear(buffer), STR + STR)

    def test_section_insert(self):
        buffer = STR + '\\begin{section}content\\end{section}' + STR
        section = templater.Section(buffer, len(STR) + 0, len(STR) + 35)
        self.assertEqual(section.insert(buffer, STR), STR + '\\begin{section}\n' + STR + '\n\\end{section}' + STR)

    def test_section_replace(self):
        buffer = STR + '\\begin[arg]{section}content\\end{section}' + STR
        section = templater.Section(buffer, len(STR) + 0, len(STR) + 40)
        self.assertEqual(section.replace(buffer, STR), STR + STR + STR)

    def test_pre_process(self):
        options = templater.pre_process('\\Parg{-n 3}')
        self.assertEqual( options.number, 3)
        self.assertEqual( options.sample, None)

    def test_pimport(self):
        fileutil.write(TST, STR)
        self.assertEqual(templater.pimport('\\Pimport{' + TST + '}', 1), '\n' + STR)

    def test_walk(self):
        self.assertEqual(templater.walk(TST), [TST])

    def test_rearrange(self):
        self.assertEqual(templater.shuffle(
                '\\begin{choices}\n\\CorrectChoice A\n\\choice B\n\\end{choices}', True),
        '\\begin{choices}\n\\choice B\n\\CorrectChoice A\n\\end{choices}')

    def test_parse_constant(self):
        self.assertEqual(templater.parse_constant('\\Pconst{STR}', 'STR', STR), STR)

    def test_clean(self):
        self.assertEqual(templater.clean(STR + '\\Parg{}'), STR)

    def test_cmmand_match(self):
        buffer = STR + '\\command[arg]{content}' + STR + '\n%' + '\\command[arg]{content}' + STR + '\n' + \
                 '\\command[arg]{content}'
        requests = templater.command_match(buffer, 'command')
        self.assertEqual(len(requests), 2)
        for request in requests:
            self.assertEqual(request.block, '\\command[arg]{content}')
            self.assertEqual(request.arg, 'arg')
            self.assertEqual(request.name, 'command')
            self.assertEqual(request.content, 'content')

    def test_section_match(self):
        buffer = STR + '\\begin[arg]{section}content\ncontent\\end{section}' + STR + '\n%' + \
                 '\\begin[arg]{section}content\ncontent\\end{section}' + STR + '\n' + \
                 '\\begin[arg]{section}content\ncontent\\end{section}'
        requests = templater.section_match(buffer, 'section')
        self.assertEqual(len(requests), 2)
        for request in requests:
            self.assertEqual(request.block, '\\begin[arg]{section}content\ncontent\\end{section}')
            self.assertEqual(request.arg, 'arg')
            self.assertEqual(request.name, 'section')
            self.assertEqual(request.content, 'content\ncontent')

    def test_verb_1(self):
        buffer = '\\verb' + STR
        self.assertEqual(templater.protect(buffer), ' ' * (len('\\verb') + len('Hello')) + ' World!')

    def test_verb_2(self):
        buffer = '\\verb! ' + STR
        self.assertEqual(templater.protect(buffer), ' ' * len('\\verb! Hello') + ' World!')

    def test_verb_3(self):
        buffer = '\\begin{verbatim}\n' + STR + '\n\\end{verbatim}\\end{verbatim}' + STR
        self.assertEqual(templater.protect(buffer), ' ' * len('\\begin{verbatim}\n' + STR + '\n\\end{verbatim}') +
                         '\\end{verbatim}' + STR)


class WeaverTester(unittest.TestCase):

    def test_weave(self):
        fileutil.make_temp('examples', True)
        fileutil.write(TST, '\Pexpr{4}')
        weaver.weave('test.txt', 'figure', 'python')
        self.assertEqual(fileutil.read_temp('test.tex'), '4\n')
        fileutil.remove('figure')
        fileutil.remove('examples/test.tex')
        fileutil.write(TST, STR)
        return

if __name__ == '__main__':
    init()