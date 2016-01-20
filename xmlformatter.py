# Author: Eric Buss <ebuss@ualberta.ca> 2016
# Module Imports


from formatter import *


# XML Formatter


# Processor
def xml_processor(buffer):
    buffer = re.sub(r'\$', '$$', buffer)
    buffer = re.sub(r'(\t\t\t<file name="" encoding="base64"></file>\n)', '', buffer)
    return buffer


# Base list
base = ['\t<question type="', Type, '">\n',
                    '\t\t<name>\n',
                    '\t\t\t<text>', Name, '</text>\n',
                    '\t\t</name>\n',
                    '\t\t<questiontext format="html">\n',
                    '\t\t\t<text><![CDATA[', Text, '\n'
                    '\t\t\t\t<img alt="Embedded Image" src="data:image/png;base64,', Image, '" \n',
                    '\t\t\t]]></text>\n',
                    '\t\t</questiontext>\n']
# Format
xml = {'essay': base + ['\t\t<answer fraction="0">\n',
                    '\t\t\t<text></text>\n',
                    '\t\t</answer>\n',
                    '\t</question>\n'],
                'shortanswer': base + ['\t\t<answer fraction="100">\n',
                    '\t\t\t<text>', Solution,'</text>\n',
                    '\t\t\t<feedback><text>Correct</text></feedback>\n'
                    '\t\t</answer>\n',
                    '\t</question>\n'],
                'numerical': base + ['\t\t<answer fraction="100">\n',
                    '\t\t\t<text>', Solution, '</text>\n',
                    '\t\t\t<feedback><text>Correct</text></feedback>\n'
                    '\t\t</answer>\n',
                    '\t</question>\n'],
                'truefalse': base + [Truefalse,
                    '\t</question>\n'],
                'multichoice': base + [Answers,
                    '\t\t<shuffleanswers>1</shuffleanswers>\n'
                    '\t\t<single>true</single>\n'
                    '\t</question>\n'],
                'answer': ['\t\t<answer fraction="', Fraction,'">\n',
                    '\t\t\t<text>', Choice, '</text>\n',
                    '\t\t\t<feedback><text>', Feedback, '</text></feedback>\n',
                    '\t\t</answer>\n'],
                'processor': xml_processor
}