# Author: Eric Buss <ebuss@ualberta.ca> 2016
# Python Imports


import re
import os
import base64


# Module Imports


import fileutil
import exporter
import templater

# Global Variables


# Lazy Enum for Tokens
Name, Text, Type, Solution, Choice, Answer, Answers, Truefalse, Fraction, Feedback, Figure, Image = range(12)

# Choice counter
choice_index = 0


# Question Class


class Question:

    def __init__(self, buffer):
        """
        Takes a string and parses out the relevant information for a question including the name of the question, any
        multiple choice choices, true false values, the text of the question itself, and the type of the question.

        :param buffer: The string to parsed
        :return: The Question object
        """
        self.type = 'essay'
        self.choices = []
        self.name = find(r'\\titledquestion\{(.*?)\}', buffer)
        self.solution = find(r'\\begin\{solution\}(.*?)\\end\{solution\}', buffer)
        self.solution = find(r'\\CorrectChoice(.*?)\\', buffer, str(self.solution))
        choice = find(r'\\tf(.*?)\\', buffer)
        if choice != '':
            self.type = 'truefalse'
            self.solution = choice.startswith('\\tf[T]')
            self.text = re.sub(r'(\[[TF]\])', '', choice)
            self.choices = ['True', 'False']
        choice = find(r'\\choice(.*?)\\', buffer)
        while choice != '':
            buffer = buffer.replace('\\choice', '\\_choice', 1)
            self.type = 'multichoice'
            self.choices.append(choice)
            choice = find(r'\\choice(.*?)\\', buffer)
        self.figure = find(r'\\includegraphics\[.*?\]\{(.*?)\}', buffer)
        if os.path.isfile(fileutil.TEMP + '/' + self.figure):
            exporter.ghost_script(self.figure)
            self.figure = self.figure[:-3] + 'png'
            with open(fileutil.TEMP + '/' + self.figure, 'rb') as data:
                self.image = base64.b64encode(data.read()).decode()
        else:
            self.image = ''
        if self.type == 'essay' and self.solution != '':
            self.type = 'shortanswer'
        if self.type == 'multichoice':
            self.choices.append(self.solution)
        self.text = re.sub(r'(\\begin\{.*?\}.*\\end\{.*?\})|(\\.*?\{.*?\})|(\\[^\\]*)', '', buffer, flags=re.DOTALL).strip()


def find(regex, buffer, default=''):
    """

    :param regex:
    :param buffer:
    :param default:
    :return:
    """
    m = re.search(regex, buffer, re.DOTALL)
    if m is not None:
        m = m.group(1).strip()
    else:
        m = default
    return m


def parse(buffer):
    """
    Parse the questions from a string and return them as a list.

    :param buffer: The string to aprse
    :return: The list of questions
    """
    questions = []
    question_sections = templater.section_match(buffer, 'questions')
    for section in question_sections:
        buffers = [m.group(1) for m in re.finditer(
                r'(((\\question)|(\\titledquestion)).*?)(?=(\\question)|(\\titledquestion)|($))',
                section.content, re.DOTALL)]
        for buffer in buffers:
            questions.append(Question(buffer))
    return questions


def format(format, questions):
    """
    Checks that formats have all been initialized and then builds the questions.

    Raises FormatterError if any format has not been initialized

    :param format: A dictionary with all the necessary formats
    :param questions: The questions to format
    :return: A string representation of the questions
    """
    global choice_index
    choice_index = 0
    buffer = ''
    for question in questions:
        buffer += format['processor'](fill(format, question, question.type))
    return buffer


def fill(format, question, type, correct=False):
    """
    Fill a given form based off a question.

    :param form: The form to fill
    :param question: The question to use
    :param correct: Whether Fraction and Feedback tokens should be considered correct
    :return: The filled form as a string
    """
    global choice_index
    buffer = ''
    for token in format[type]:
        if isinstance(token, str):
            buffer += token
        elif token is Name:
            buffer += str(question.name)
        elif token is Text:
            buffer += str(question.text)
        elif token is Type:
            buffer += str(question.type)
        elif token is Solution:
            buffer += str(question.solution)
        elif token is Figure:
            buffer += str(question.figure)
        elif token is Image:
            buffer += str(question.image)
        elif token is Answer:
            buffer += fill(format, question, 'answer', False)
        elif token is Fraction:
            buffer += '100' if correct else '0'
        elif token is Feedback:
            buffer += 'Correct' if correct else 'Incorrect'
        elif token is Choice:
            buffer += str(question.choices[choice_index])
            choice_index += 1
        elif token is  Answers:
            for _ in range(len(question.choices) - 1):
                buffer += fill(format, question, 'answer', False)
            buffer += fill(format, question, 'answer', True)
        elif token is  Truefalse:
            if question.solution:
                buffer += fill(format, question, 'answer', True)
                buffer += fill(format, question, 'answer', False)
            else:
                buffer += fill(format, question, 'answer', False)
                buffer += fill(format, question, 'answer', True)
    return buffer