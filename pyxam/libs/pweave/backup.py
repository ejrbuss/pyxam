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
        self.name = ''
        self.figure = ''
        self.image = ''
        self.solution = ''
        self.choices = []
        # Parse

        for current in range(len(buffer)):
            forward = str(buffer[current:])
            if buffer[current] == '\\':
                if forward.startswith('\\question'):
                    self.name = ''
                elif forward.startswith('\\titledquestion'):
                    self.name = re.search(r'\\titledquestion\{(.*?)\}', forward).group(1).strip()
                elif forward.startswith('\\choice'):
                    self.choices.append(re.search(r'\\choice(.*?)\\', forward, re.DOTALL).group(1).strip())
                elif forward.startswith('\\CorrectChoice'):
                    self.solution = re.search(r'\\CorrectChoice(.*?)\\', forward, re.DOTALL).group(1).strip()
                elif forward.startswith('\\begin{solution}'):
                    self.solution = re.search(r'\\begin\{solution\}(.*?)\\end\{solution\}', forward, re.DOTALL).group(1).strip()
                elif forward.startswith('\\tf'):
                    self.choices.append(re.search(r'\\tf(.*?)\\', forward, re.DOTALL).group(1))
                    self.solution = self.choices[0].startswith('\\tf[T]')
                elif forward.startswith('\\begin{figure}[htpb]'):
                    self.figure = re.search(r'\\includegraphics\[.*?\]\{(.*?)\}', forward, re.DOTALL).group(1).strip()
                    exporter.ghost_script(self.figure)
                    self.image = self.figure[:-3] + 'png'
                    with open(fileutil.TEMP + '/' + self.image, 'rb') as data:
                        self.image = base64.b64encode(data.read()).decode()
                    self.figure = str(os.path.basename(self.figure))
        # Remove commands
        self.text = re.sub(r'(\\begin\{.*?\}.*\\end\{.*?\})', '', buffer, flags=re.DOTALL)
        self.text = re.sub(r'(\\.*?\{.*?\})', '', self.text)
        self.text = re.sub(r'(\\[^\\]*)', '', self.text, flags=re.DOTALL).strip()
        # Find type
        if len(self.choices) > 1:
            self.type = 'multichoice'
            self.choices.append(self.solution)
        elif re.match(r'[+-0-9.]+', str(self.solution)):
            self.type = 'numerical'
        elif self.solution == '':
            self.type = 'essay'
        elif len(self.choices) == 1:
            self.type = 'truefalse'
            self.text = re.sub(r'(\[[TF]\])', '', self.choices[0])
            self.choices = ['True', 'False']
        else:
            self.type = 'shortanswer'


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