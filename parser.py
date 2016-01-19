# Author: Eric Buss <ebuss@ualberta.ca> 2016
# Python Imports


import re


# Module Imports


import fileutil
import templater


# Global Variables


# XML formatting for essay
XML_ESSAY = ['\t<question type="essay">\n',
            '\t\t<name>\n',
            '\t\t\t<text>', None, '</text>\n',
            '\t\t</name>\n',
            '\t\t<questiontext format="html">\n',
            '\t\t\t<text>$$$', None, '$$$</text>\n',
            '\t\t</questiontext>\n',
            '\t\t<answer fraction="0">\n',
            '\t\t\t<text></text>\n',
            '\t\t</answer>\n',
            '\t</question>\n']


# XML formatting for shortanswer
XML_SHORT = ['\t<question type="shortanswer">\n',
            '\t\t<name>\n',
            '\t\t\t<text>', None, '</text>\n',
            '\t\t</name>\n',
            '\t\t<questiontext format="html">\n',
            '\t\t\t<text>$$$', None, '$$$</text>\n',
            '\t\t</questiontext>\n',
            '\t\t<answer fraction="100">\n',
            '\t\t\t<text>$$$', None ,'$$$</text>\n',
            '\t\t\t<feedback><text>Correct</text></feedback>\n'
            '\t\t</answer>\n',
            '\t</question>\n']


# XML formatting for numerical
XML_NUM = ['\t<question type="numerical">\n',
            '\t\t<name>\n',
            '\t\t\t<text>', None, '</text>\n',
            '\t\t</name>\n',
            '\t\t<questiontext format="html">\n',
            '\t\t\t<text>$$$', None, '$$$</text>\n',
            '\t\t</questiontext>\n',
            '\t\t<answer fraction="100">\n',
            '\t\t\t<text>', None , '</text>\n',
            '\t\t\t<feedback><text>Correct</text></feedback>\n'
            '\t\t</answer>\n',
            '\t</question>\n']


# XML formatting for true or false
XML_TorF = ['\t<question type="truefalse">\n',
            '\t\t<name>\n',
            '\t\t\t<text>', None, '</text>\n',
            '\t\t</name>\n',
            '\t\t<questiontext format="html">\n',
            '\t\t\t<text>$$$', None, '$$$</text>\n',
            '\t\t</questiontext>\n',
            '\t\t<answer fraction="', None, '">\n',
            '\t\t\t<text>True</text>\n',
            '\t\t\t<feedback><text>', None, '</text></feedback>\n'
            '\t\t</answer>\n',
            '\t\t<answer fraction="', None, '">\n',
            '\t\t\t<text>False</text>\n',
            '\t\t\t<feedback><text>', None, '</text></feedback>\n'
            '\t\t</answer>\n',
            '\t</question>\n']


# XML formatting for multiple choice
XML_MULTI = ['\t<question type="essay">\n',
            '\t\t<name>\n',
            '\t\t\t<text>', None, '</text>\n',
            '\t\t</name>\n',
            '\t\t<questiontext format="html">\n',
            '\t\t\t<text>$$$', None, '$$$</text>\n',
            '\t\t</questiontext>\n',
            None,
            '\t</question>\n']


# XML formatting for a question
XML_ANS = ['\t\t<answer fraction="', None ,'">\n',
            '\t\t\t<text>', None, '</text>\n',
            '\t\t\t<feedback><text>', None, '</text></feedback>\n',
            '\t\t</answer>\n']


# Class Tokens


class FLAGS:
    name = 0
    text = 1
    answer = 2
    fraction = 0
    feedback = 2


# Question Class


class Question:

    def __init__(self, buffer):
        """
        Takes a string and parses out the relevant information for a question including the name of the question, any
        multiple choice choices, true false values, the text of the question itself, and the type of the question.

        :param buffer: The string to parsed
        :return: The Question object
        """
        self.name = ''
        self.solution = ''
        self.choices = []
        copy = buffer[:]
        for current in range(len(buffer)):
            forward = str(buffer[current:])
            if buffer[current] == '\\':
                if forward.startswith('\\question'):
                    self.name = ''
                    copy = copy.replace('\\question', '')
                elif forward.startswith('\\titledquestion'):
                    self.name = re.search(r'\\titledquestion\{(.*?)\}', forward).group(1)
                    copy = copy.replace('\\titledquestion{' + self.name + '}', '')
                elif forward.startswith('\\tf'):
                    self.choices.append(re.search(r'\\tf(.*?)\\', forward, re.DOTALL).group(1))
                    copy = copy.replace('\\tf' + self.choices[-1], '')
                elif forward.startswith('\\choice'):
                    self.choices.append(re.search(r'\\choice((.*?)\\)', forward, re.DOTALL).group(1))
                    copy = copy.replace('\\choice' + self.choices[-1], '')
                elif forward.startswith('\\CorrectChoice'):
                    self.solution = re.search(r'\\CorrectChoice(.*?)\\', forward, re.DOTALL).group(1)
                    copy = copy.replace('\\CorrectChoice' + self.solution, '')
                elif forward.startswith('\\begin{Solution}'):
                    self.solution = re.search(r'\\begin\{Solution\}(.*?)\\end\{Solution\}', re.DOTALL).group(1)
                    copy = copy.replace('\\begin{Solution}' + self.solution + '\\end{Solution}', '')
        copy = copy.replace('\\begin{choices}', '')
        copy = copy.replace('\\end{choices}', '')
        self.text = copy.strip()
        self.name = self.name.strip()
        self.solution = self.solution.strip()
        self.choices = [choice.strip() for choice in self.choices]
        if len(self.choices) > 1:
            self.type = 'multichoice'
        elif len(self.choices) == 1:
            self.type = 'truefalse'
            self.solution = self.choices[0].startswith('\\tf[T]')
            self.text = re.sub(r'(\[[TF]\])', '', self.choices[0])
        elif re.match(r'[+-0-9.]+', self.solution):
            self.type = 'numerical'
        elif self.solution == '':
            self.type = 'essay'
        else:
            self.type = 'shortanswer'

    def to_xml(self):
        buffer = ''
        xml = []
        if self.type == 'essay':
            xml = XML_ESSAY
            for item in xml:
                buffer += str(item)
            return buffer
        elif self.type == 'shortanswer':
            xml = XML_SHORT
            insert(xml, FLAGS.answer, self.solution)
        elif self.type == 'numerical':
            xml = XML_NUM
            insert(xml, FLAGS.answer, self.solution)
        elif self.type == 'truefalse':
            xml = XML_TorF
            if self.solution:
                insert(xml, FLAGS.answer, 100)
                insert(xml, FLAGS.answer + 1, 'Correct')
                insert(xml, FLAGS.answer + 2, 0)
                insert(xml, FLAGS.answer + 3, 'Incorrect')
            else:
                insert(xml, FLAGS.answer, 0)
                insert(xml, FLAGS.answer + 1, 'Incorrect')
                insert(xml, FLAGS.answer + 2, 100)
                insert(xml, FLAGS.answer + 3, 'Correct')
        elif self.type == 'multichoice':
            xml = XML_MULTI
            answers = []
            answer = XML_ANS[:]
            for choice in self.choices:
                answer = XML_ANS[:]
                insert(answer, FLAGS.fraction, 0 )
                insert(answer, FLAGS.text, choice )
                insert(answer, FLAGS.feedback, 'Incorrect' )
                answers.append(answer)
            answer = XML_ANS[:]
            insert(answer, FLAGS.fraction, 100 )
            insert(answer, FLAGS.text, self.solution )
            insert(answer, FLAGS.feedback, 'Correct' )
            answers.append(answer)
            answers.append('\t\t<shuffleanswers>1</shuffleanswers>\n')
            answers.append('\t\t<single>true</single>\n')
            insert(xml, FLAGS.answer, answers)
        insert(xml, FLAGS.name, self.name)
        insert(xml, FLAGS.text, self.text)
        for item in xml:
            buffer += str(item)
        return buffer


def insert(format, index, item):
    for i in range(len(format)):
        if format[i] is None:
            if index == 0:
                if isinstance(item, list):
                    format = format[:i] + format[i + 1:]
                    item.reverse()
                    for sub_item in item:
                        format.insert(i, sub_item)
                else:
                    format[i] = item
                return
            else :
                index -= 1


def parse(path):
    questions = []
    question_sections = templater.section_match(fileutil.read(path), 'questions')
    for section in question_sections:
        buffers = re.findall(r'(((\\question)|(\\titledquestion))((.*?)|(\\end\{([^q].*?\})))*)((\\question)|(\\titledquestion)|(\\end\{questions\}))',
                               section.block, re.DOTALL)
        for buffer in buffers:
            questions.append(Question(buffer[0]))
    return questions







