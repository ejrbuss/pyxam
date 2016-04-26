# Pyxam
Pyxam is a recreation of the R exam package functionality in python. After development details? head over to the [docs](https://rawgit.com/balancededge/pyxam/master/docs/build/0_Overview.html).

## Overview.
Pyxam is Framework for streamlining the exam generation process. Pyxam provides tools that allow you to:
 - Include code in questions
 - Translate between multiple formats
 - Create multiple versions
 - Interweave meta data such as student names and numbers

Though Pyxam offers a great deal of flexibility it comes at the cost of complexity. Using pyxam can be confusing at first and this readme aims to help you understand the process at the top level.

### What Pyxam Does
Every time you run a template file through Pyxam something like this process will occur.
 - All the python files in your `pyxam/plugins` folder are loaded, each file can modify the pyxam process, add options, formats etc.
 - Your command line options are parsed 
 - The file structure for the process is determined, this means finding the absolute path to the template file as well as creating a temporary directory (by default tmp) and an output directory (by default out)
 - For every version that you specified a copy of the template file will be copied into the temporary directory along with the code from `pyxam/inline.py`
 - If a student list is provided these versions will be copied however many times is needed to provide an exam for each student
 - Each of these files is run through [Pweave](http://mpastell.com/pweave/) 
 - The files are then parsed based on the file extension
 - And reconstructed based on the provided output format
 - Finally the finished files are copied to the out directory and the temporary directory is deleted

Many of these steps will change depending on your options. For instance when converting a file to pdf a number of steps get added by the `pyxam/plugins/format_pdf.py` plugin to this process. 

## Dependencies
Pyxam has a number of software requirements*:
 - You will need a LaTeX compiler which can be run from the command line with:
 ```
 $ pdflatex [options] file
 ```
 - The [exam package](https://www.ctan.org/pkg/exam?lang=en) for LaTeX
 - The [minted package](https://www.ctan.org/pkg/minted?lang=en) for LaTeX
 - The [lineo package](https://www.ctan.org/pkg/lineno?lang=en) for LaTeX
 - [Python 3](https://www.python.org/) or later

Additionally if you try to run Pyxam without any of the following Python modules you will be asked to pip install them:
 - [Numpy](http://www.numpy.org/)
 - [Matplotlib](http://matplotlib.org/)
 - [Pweave](http://mpastell.com/pweave/)
 
*Checkout [this](https://www.sharelatex.com/learn/Choosing_a_LaTeX_Compiler) page if you do not already have a LaTeX compiler installed.

## Installation
To install Pyxam download the files from Github either by cloning the repository:
```
$ git clone https://github.com/balancededge/pyxam
```
Or by using the Github web interface and clicking the Download ZIP button in the upper right. After the project is 
cloned or the zip is unzipped navigate to the top level directory containing `setup.py`. In the command line run:
```
$ ./setup.py install
```
You may need to run the script with python and/or under superuser (sudo). Installing Pyxam will make the program 
available at the commandline via the bash script `pyxam` as well as any other python script by using `import pyxam`
## Updating
In order to update pyxam simply pull the project again from Github:
```
$ git pull
```
And run the setup file again.
## Running Pyxam
Pyxam is command line tool. Its basic usage looks like:
```
$ pyxam [options] template
```
Note that there is not strict ordering on the options or template. Options can appear before or after the file or even both. Options can be flags, such as the `solutions` flag which simply toggles the creation of a solutions file for formats that support it. Or options can speciify variables such as the ` out` option which sets the output directory. Variables such as paths can be given as absolute paths or paths relative to the current working directory.
### Typical Output
In this section we will look at the output of a typical pyxam usage. In this example we are converting the LaTeX standard file to PDF as well as requesting two different versions of the file.
```
$ pyxam --number 2 --format pdf pyxam_tex_standard.tex 
```
When run from the command line Pyxam will display this title message along with its version number.
```
    ____                           
   / __ \__  ___  ______ _____ ___ 
  / /_/ / / / / |/_/ __ `/ __ `__ \ 
 / ____/ /_/ />  </ /_/ / / / / / /
/_/    \__, /_/|_|\__,_/_/ /_/ /_/ 
      /____/ 

        Latex Exam Generation. v0.3.5 
```
As explained in the overview section the first thing Pyxam does is load its plugin files so as you might expect the first informative piece of text relates to plugins. Here we get confirmation that 11 plugin files were loaded.
```
Successfully loaded 11 plugins.
```
Next we recieve a message telling us that the template file was succesfully run through [Pweave](http://mpastell.com/pweave/).
```
Template successfully weaved.
```
After weaving all the options are loaded from the command line and the template file and so it is safe to show the user the status table. The status table displays all the current value of options for the pyxam process. 
```
==========================================STATUS TABLE=========================================
 Name         Value
===============================================================================================
 recomps      1 
 noweave      False 
 api          False 
 help         False 
 method       sequence 
 population   None 
 version      False 
 docs         False 
 figure       /home/usr/pyxam/examples/tmp/fig 
 debug        False 
 plugins      False 
 logging      30 
 solutions    False 
 tmp          /home/usr/pyxam/examples/tmp 
 title        pyxam_standard 
 number       2 
 template     /home/usr/pyxam/examples/pyxam_tex_standard.tex 
 format       pdf 
 cwd          /home/usr/pyxam/examples/tmp 
 list         False 
 alphabetize  False 
 htmltemplate /usr/lib/python/site-packages/Pyxam/pyxam/templates/exam.html 
 shell        python 
 out          /home/usr/pyxam/examples/out 
 gitdocs      False 
===============================================================================================
```
After the status the format used to parse and reconstruct the file are provided.
```
Using tex format to parse /home/ebuss/pyxam/examples/tmp/v1.tex
Using tex format to parse /home/ebuss/pyxam/examples/tmp/v2.tex
Successfully parsed tex.

Successfully composed tex.
```
Because we specified PDF as the output format an additional set of messages tell us how many files will be compiled and when compiling is finished. Because we specified two versions two files need to be compiled.
```
Compiling 2 files.
Finished compiling.
```
If everthing was succesful you will see a goodbye message.
```
Thanks for using Pyxam, have a nice day!
```
### Debugging
Running a file through Pyxam requires a lot of things to be *correct*. This is difficult particularly with so many pieces of software working together. In the case of the last example any Python in the template file needed to be able to pass through [Pweave](http://mpastell.com/pweave/) without a hitch, the LaTeX had to be parseable by Pyxam, and compilable by your LaTeX compiler. When debugging the first step you should take is to look at what step in the process the failure occured. If for instance you do not even see the title displayed chances are you are using a faulty plugin. If you see the title but no status table chances are there is an error in the code of your template file. If the file is parsed but not composed chances are you are trying to use language features not supported by Pyxam.

If these steps fail to help you find a solution the next step is to enable the debug flag and start logging:
```
$ pyxam --number 2 --format pdf pyxam_tex_standard.tex --debug --logging 10 
```
The debug flag will prevent Pyxam from cleaning up temporary files and logging will display extra messages to help you understand exactly what Pyxam is up to. If the issue was in the PDF compiling stage you will now be able to see the .tex file that was being compiled along with its respective .log and .aux. If the issue occured earlier you can open up the temporary directory and checkout the parsed-ast and composed-ast files which provide a human readable view of the tree your template file was parsed into.
## Question Structure
Pyxam primarily translates documents between LaTeX, Org Mode, and Moodle XML, as such the question types are tailored to what is easily supported by all three of these formats. Formats like org mode has some custom syntax which must be used in order to use Pyxam. Below is a brief description of each question type. Along with the description is a depiction of the basic structure of the question type. This structure is based off the parsing process and is similar to what you would see if you opend the parsed-ast or composed-ast files mentioned in the debug section.
### Essay
The essay question is the simplest type of question supported by Pyxam. It has the following structure:
```
essay:
    title:
        the question title
    prompt:
        the question prompt
```
In LaTeX this would look something like:
```LaTeX
\titledquestion{the question title}
    the question prompt
```
And in org mode it would look something like:
```org
** ?:: the question title
the question prompt
```
### Shortanwser
Shortanswer questions are the most common and useful question type. They come in three varieties, `shortanswer`, `numerical`, and `calculated`. By default when exporting to a format like PDF all three of these behave very similarily. However when exporting to Moodle these formats allow for additional features. Numerical and Calulated Questions allow for a tolerance option which allows users to enter in answers that are slightly off the given solution. The calculated question also allows for Moodle questions to be different for different students. For details on using these features of shortanswer questions checkout the section on Inline Pyxam. The structure of a shortanswer question is as follows:
```
shortanswer:
    title:
        the question title
    prompt:
        the question prompt
    solution:
        the question solution
```
In LaTeX this would look something like:
```LaTeX
\titledquestion{the question title}
    the question prompt
    \begin{solution}
        the question solution
    \end{solution}
```
And in org mode it would look something like:
```org
** ?:: the question title
the question prompt
*** solution
the question solution
```
### Multiple choice
Multiple choice questions are a simple format that also allow for the creation of true false questions and multiselect questions. The basic structure of a multiple choice questions looks like:
```
multichoice:
    title:
        the question title
    prompt:
        the question prompt
    choices:
        choice: 
            a choice
        choice: 
            a choice
        correctchoice: 
            the correct choice
```
In LaTeX this would look something like:
```LaTeX
\titledquestion{the question title}
    the question prompt
    \begin{choices}
        \choice a choice
        \choice a choice
        \CorrectChoice the correct choice
    \end{choices}
```
And in org mode it would look something like:
```org
** ?:: the question title
the question prompt
*** choices
- [ ] a choice
- [ ] a choice
- [X] the correct choice
```
## Using Pyxam
This section covers all of the core features of Pyxam along with the command line options which control them. The command line options are given with their verbose form followed by their compact form. These two way of providing the options can be freely interchanged. As an example here is the explanation of the help option:

`--help -h`  
Displays a list of all the options along with a short description of each.
### Weaving Python Code
Code in Pyxam template files is provided using the [noweb](https://www.cs.tufts.edu/~nr/noweb/) format. This means code can be given in chunks or blocks. Below are a couple simple examples.
```python
<<>>=
print('I am a chunk')
@
Whereas <%= 'I am an inline block' %>.
```
`--noweave -w`  
This option allows you to disable weaving, this is useful for documents where you have no intention of including code.

`--shell -shl [language]`  
This option allows you to specify that the code in your document is something other than Pyxam. Check your version of Pweave to see what other langauges are supported. Currenty python, matlab, and octave are all supported.
### Inline Pyxam
Before your template file is run `pyxam/inline.py` is copied into the start of your file. This file provides a set of built in file relative constants and functions that can help in your code. For more detailed examples look at `examples/python_examples.tex` and `examples/pyxam_tex_standard.tex`.

**Constants**  
In order to print a pyxam constant it should be placed in an echoed noweb block as the constants are not function calls, only variables.
```python
<%=
# Will echo the exam number, the version as an integer numbered from 0
pyxam.number 
# Will echo the exam version, either a number from 1 or a letter
pyxam.version 
# Will echo the student's first name if available. If no first name could be found in your csv 
# a blank will be echoed. If this is a default version or solution the placeholder from 
# config.py will be used to fill this blank
pyxam.student_first_name
# Will echo the student's last name following the same rules as the first name
pyxam.student_last_name
# If your csv file contians the student name in one block you can get their name with this
# constant
pyxam.student_name
# Will echo the studen't number if available or the config.py placeholder if this is a default
# version or solution
pyxam.student_number
%>
```
**Functions**  
Functions should be called in an unechoed noweb block as function call `print` to produce their output.
```python
<%
# Will import the contents of another file which will be weaved seperately
pyxam.import_questions('path/to/your/question/file', 'can/take/multiple/args')
# Will set options as if they were entered from the command line
pyxam.args('--debug')
# Will print out the provided strings in a random order
pyxam.shuffle('1', '2', '3', '4')
# When provided in a solutions block will create a numerical question 
pyxam.numerical(solution=12, tolerance=2, percent=True)
# When provided in a solutions block will create a calcualted question
pyxam.calculated(equation='{a} / {b}', tolerance=0.1)
# In order for calculated question to work in Moodle a dataset must be provided
pyxam.dataset(a, b)
# Will categorize all of the following questions
pyxam.categorize(course='a course', category='a category')
# Wildcards can be used to generate random numbers
pyxam.wildcard(min=0, max=100, n=12, decimals=1)
# Wildcardsc an be specified using sets
pyxam.wildcard(set=[1, 2, 3, 4])
 %>
 ```
### Exam Versions
Your template file can be used to create many different versions of the original file. The following options control these versions.

`--solutions -s`  
Enabling this flag will result in a solution document being produced for every version you create.

`--number -n [Number of versions]`  
The number option set the number of exam versions to produce. Though every student's exam will be weaved seperately every exam version shares a random seed meaning two student's with the same version will produce the same exam even if weaved seperately.

`--alphabetize -a`  
By default versions are specified with numbers starting from 1. Setting the alphabetize flag will change the versions to capital letters starting from A.
### Mixing Class Lists
You can provide a CSV file along with your template file to create unique exam copies for individual students. Setting up how to parse your individual CSV file is detailed in the Configuration section.

`--population -p [CSV file]`  
This option allows you to specify a CSV file to mix your template with. Student name and numbers will attempted to be parsed from the file and for every student found a version will be assigned and a document produced.

`--method -m [sequence or random]`  
You can specify how the rows in your CSV file correspond to exam versions using the method option. By default the exams will simply repeat in sequence until every student has a version. There also exists an option to use a RNG to assign student's version. If you are interested in creating your own mixing algorithim check out the mixing methods section of the documentation.
### Formats
Formats provide Pyxam with a definition for importing and exporting to that format. There are a couple exception to this rule such as PDF and DVI which only allow for exporting.

`--format -f [output format]`  
Use the format option to specify which file format you wish to export to.

`--list -ls`  
You can list all of the available formats along with a short description using this option.

`--htmltemplate -htt [html template file]`  
When exporting to HTML your generated HTML gets inserted into an HTML template file which provides some basic structure and CSS. You can specify the path to your own HTML template file using this option.

### Documentation and Plugins
Pyxam comes with options for automatically generating documentation for its core modules as well as plugins which you may have just added. 

`--plugins -plg`  
This option lists all succesfully loaded plugins along with their author and a short description.

`--docs -docs`  
This option will compile a set of HTML documentation pages for pyxam in the `docs/build` directory. These files can then be opened and viewed on your computer locally. 

`--gitdocs -gdocs`  
This option is used when the documentation pages will be uploaded to github and fixes the links to work with rawgit.

### Other Options
`--title -t [exam title]`  
Use this option to specify the exam title. This tile will appear before the exam version number and student name/number. The formatting for the rest of the exam name can be customized used `pyxam/config.py`.

`--version -v`  
This option will dispaly the Pyxam title and version number.

`--debug -d`  
As mentioned in the debug section this option prevents Pyxam from deleting the temporary directory and any files in the output directory that are typically cleaned up.

`--logging -l`  
As mentioned in the debug section this option allows you to set the logging level of Pyxam.

`--out -o`  
This option allows you to set the path to the output directory.

`--tmp -t`  
This option allows you to set the path to the temporary directory.

`--figure -fig`  
This option allows you to set the path to the figure directory.

`--recomps -r`  
In some cases LaTeX files need to be compiled more than once. Use this option to set the number of recompilations that occur.

`--api -api`  
By default when Pyxam is called from python code it is in api mode. When in api mode no messages will be displayed. This mode can be enabled from the command line with this option.

## Configuration
The file `pyxam/config.py` can be used to set a wide variety of configuration options. This primarily this includes the default values of the options mentioned above. Additionally it includes:
 - Default file paths for Pyxam
 - Default filters for parsing (advanced)
 - Filename and question solution formats
 - Student data placeholders
 - CSV column identifiers.

While most of the config optiosn are self explanatory some are a little more involved. The Filename formats for instance are a formattable string. They are made up of literal characters and curly brackets which denote variables to be inserted. For example:
```python
filename = 'v{version}_{name}_{number}'
```
When given version='A', name='Smith', and number='1234' will produce:
```
v_A_smith_1234
```
Placeholders will replace their respective constant with their value in default exam versions and solution files. CSV column identifiers are used to parse CSV files. Take the column headers that identify the first/last name of your students, id numbers, etc. and turn them to all lowercase and remove all whitespace. Add these strings to the respective column lists. Your CSV file will not be correctly parsed.

## Limitations
Pyxam uses an extremely limited context free grammar that does not support regex based tokens. This parsing mechanism is sufficient for many markup languages however there are many features of languages like LaTeX which cannot be easily supported with this system. As such all of the supported formats are closer to limited subverions of their related formats than full versions. Do not expect more than basic functionality without adding to the respective format plugin yourself.

When exporting to Moodle it is important to understand the different point at which processing can occur. There are two points. When the file is weaved and when the file is viewed in Moodle. There is a great deal of flexibility when weaving the file, different figures can be produces, the questions can be reordered, etc. Moodle provides a much smaller toolset. The calculated question and reordering of multiple choice defines the primary ways of introducing changes between question versions. Multiple choice questions will be reordered automatically, but creating a calculated question that is different for every student requires thought and time putting together the `pyxam.calculated()` call necessary to make that process work.

## Example Files
 - [pyxam_tex_standard.tex](https://github.com/balancededge/pyxam/blob/master/examples/pyxam_tex_standard.tex) An example of all the standard question types in LaTeX 
 - [pyxam_org_standard.org](https://github.com/balancededge/pyxam/blob/master/examples/pyxam_org_standard.org) An example of all the standard question types in ORG mode
 - [python_examples.tex](https://github.com/balancededge/pyxam/blob/master/examples/python_examples.tex) A simple introduction to Python in a LaTeX file
 - [python_examples.org](https://github.com/balancededge/pyxam/blob/master/examples/python_examples.org) A simple introduction to Python in an ORG mode file
 - [noweb_examples.tex](https://github.com/balancededge/pyxam/blob/master/examples/noweb_examples.tex) Examples of the different code options when using Pyxam with LaTeX
 - [noweb_examples.org](https://github.com/balancededge/pyxam/blob/master/examples/noweb_examples.org) Examples of the different code options when using Pyxam with ORG mode
 - [matlab_example.tex](https://github.com/balancededge/pyxam/blob/master/examples/matlab_example.tex) An example of using matlab/octave code with LaTeX
 - [matlab_example.org](https://github.com/balancededge/pyxam/blob/master/examples/matlab_example.org) An example of using matlab/octave code with ORG mode
 - [exam_example.tex](https://github.com/balancededge/pyxam/blob/master/examples/exam_example.tex) A comprehensive example file in LaTeX
 - [exam_example.org](https://github.com/balancededge/pyxam/blob/master/examples/exam_example.org) A comprehensive example file in ORG mode

## Building HTML 
In addition to Pyxam's use as an exam generator it can also assist in turning markup files into HTML. Here is a simplified code example of what is occuring in Pyxam's docs plugin:
```python
for markdown_file in docs_source:
    pyxam.start(markdown_file, '-f', 'HTML', '-o', docs_build)
```
This sort of scripting can be used to quickly generate a set of HTML pages. By specifying your own template file you can control what your HTML will be copied into. Add in some file management and you have the basis for creating simple static webpages. For a more detailed example implementation checkout `pyxam/plugins/docs.py`.

## Contact
Address question/concerns and bug fixes to author Eric Buss at ebuss@ualberta.ca
