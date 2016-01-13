# Pyxam
Pyxam is a spiritual reacration of the R exam package for python. An open source solution for combining LaTeX documents with Python source code and additional options to generate high quality exam forms. Pyxam serves three key purposes:

- Pipeline compiling code, adding the results to documents and then compiling LaTeX
- Provide key features needed for exams, such as question reordering, inserting student information, and keeping track of answer keys
- Make exporting into a variety of formats including PDF and Moodle easier than ever

This document gives a basic overview of the current version of Pyxam and also serves as a light design document for future additions. For more detailed instructions on how to get the most out of Pyxam check out the example files in the /examples directory found in the main github directory.  

### Version
0.2.1       

### Dependencies
Pyxam requires a set of open source software to be used and run succesfully. Though a central goal of Pyxam is to keep the program simple and lightweight such dependencies are unavoidable. In order to run Pyxam you will need the following:

- A LaTeX compiler and the examclass 
    - For windows users try [MikTex](http://miktex.org/)
    - For unix users try [TeX Live](https://www.tug.org/texlive/) 
- [Python](https://www.python.org/downloads/) 3.4 or greater
- [Perl](https://www.perl.org/get.html) 5 or greater
- [Matplotlib](http://matplotlib.org/users/installing.html) library for Python

Internally Pyxam includes the source for a few other key pieces of software. No special attention is required to make these work. These include:

- [Pweave](http://mpastell.com/pweave/) for parsing Python code and generating images
- [texfot](https://www.ctan.org/pkg/texfot?lang=en) for managing the output of LaTeX compilers

### Installation
Installation is as simple as pulling the files from [GitHub](https://github.com/balancededge/pyxam/tree/master). Either go to the webpage and click Download Zip or use the command line. If you have [git](https://git-scm.com/downloads) installed all you need to do get the source is enter:
```sh
$ git clone https://github.com/balancededge/pyxam pyxam
$ cd pyxam
```
Currently Pyxam has no Setup script so after this step you are done.

### Running Pyxam
If Python 3 is in your PATH as `python3 ` Pyxam can be run from the command line like so:
```sh
$ ./pyxam.py [options] <template file>
```
Otherwise you need to run Pyxam under Python:
```sh
$ python pyxam.py [options] <template file>
```
Pyxam can also be called by another Python program. There is currently no formal API however pyxam can be run with default options by the following code:
```python
import pyxam                                # Import pyxam module
options = pyxam.pyxamopts.PyxamOptions()    # Get a default options object
options.template = '<template file>'        # Add your template file
pyxam.core.pyxam(options)                   # Run the options
```
To change options from the default you can use `options.<option name> = value` to configure pyxam. The option names correspond to the options found in the following sections. Here is an example configuration:
```python
options.solutions = True
options.number = 3
options.out = '~/exams/exam2016'
```

### Using Pyxam
Pyxam works by parsing a LaTeX template file, configuring a set of options, and then running your file through a Python parser and exporter. In order to add python code to your LaTeX file you need to use the following syntax:
```LaTeX
\documentclass{article}
\begin{document}
<<>>=
s = 'Hello World'   # Python code between <<>>= and @ will be run and displayed verbatim
@
<<echo=False>>=
s                   # You can use the echo argument to silence bits of code
@
<% s += '!' %>      % This code is silent 
<%= s %>            % This code is not 
\Pexpr{s}           % This code functions the same as the block above
\end{document}
```
If you used Pyxam on the above document and exported to .tex you would get:
```LaTeX
\documentclass{article}
\begin{document}
\begin{verbatim}
s = 'Hello World'   # Python code between <<>>= and @ will be run and displayed verbatim
\end{verbatim}
% This code is silent 
Hello World!           % This code is not 
Hello World!           % This code functions the same as the block above
\end{document}
```
For more detailed examples of what is  possible check out the [Pweave website](http://mpastell.com/pweave/) which is what powers this process under the hood. In addition to Python code Pyxam includes a number of exam specific options that are accessible by a combination of exam line options and LaTeX commands. 

### Importing Questions
You can import questions into your template file by using the compand \Pimport. Questions can be imported individually or in bulk. Question paths are specified either absolutely or relative to the template file. An example import:
```LaTeX
% This will replace this command with the contents of question1.tex
\Pimport{questions/question1.tex}   
% This will replace this command with the contents of question2.tex or question3.tex
\Pimport{questions/question2.tex|questions/question3.tex}
% This will replace this command with a random .tex file from /questions
\Primport{questions}
% This will replace this command with a random selection of 7 questions from /questions
\Pimport[7]{questions}
```
***Option***  
**sample**  
Usage `pyxam.py -smp <an integer value>`  
By default import commands only import a single question file. This default behavior can be changed with the sample option. The value specified will become the new default. Any questions imported with a speficied number of imports will still prefer their argument over the new default. 

### Mix Class List
Pyxam can take a CSV list of student names or student names and numbers and mix them in with exported exams. When this happens the students name will be appended to the exam name if only the name is avaiable and the student number will be appended if both are available. Trailing commas will be dealt with. A student list should be specified in one of the following ways:
```
first_name last_name                or          first_name last_name, student_number
first_name last_name                            first_name last_name, student_number
first_name last_name                            first_name last_name, student_number
...                                             ...
```
In addtion to producing a set of exams with student names or numbers appended to files importing a student list can also make changes to a template file itself. Using the LaTeX command below student information can be specified:
```LaTeX
% This will be replaced with the student's name
\Pconst{STUDENT}
% This will be replaced with the student's number
\Pconst{STUDNUM}
```

***Options***  
**population**  
Usage: `pyxam.py -p <CSV file>`  
Specify a class list to mix in with the generated exams.   
**method**  
Usage: `pyxam.py -m <method>`  
Specify the method used when mixing in a class list. The random method will distribute the exams to students completely randomly. The sequence method will loop through the exams dealing them out in an evenly distributed manner. By default exams are sequenced. 

### Versions
Pyxam can be used to generate different versions of the same exam. Each version will have its Python code parsed independently as well as potentially have different questions imported in different orders. To keep track of exam versions exams are numbered starting at 1. The version number and title can be written to the template itself using the following LaTeX commands:
```LaTeX
% Specify the version of the exam
\Pconst{VERSION}
% Specify the name of the exam
\Pconst{TITLE}
```
Exams are generated with a set random seed, so if you ever lose your exams you can safely rebuild your various versions so long as your code runs the same and you run Pyxam in the same configuration.

***Options***  
**alphabetize**  
Usage `pyxam.py -a`  
Use letters rather than numbers for the versioning. For example exam1.pdf will become examA.pdf. This will change both the export names and the replacements done to the template.  
**title**  
Usage: `pyxam.py -t <title>`  
Specify the title of the exam. By default exams are named 'exam'.  

### Other Options
Pyxam offers a large range of other configuration options and in order to make using them easier they can be specified and saved within your template document using the LaTeX command \Parg. Below is an example:
```Latex
% Specify arguments exactly as you would on the command line
\Parg{-a -t 'Spring Quiz' -n 3}
```
This command would mean anytime you run `pyxam.py <template file>` with the above in your template file your default options would change so that versions are lettered, the exam name is Spring Quiz and the number of exams produced will be 3. These arguments can be overidden at anytime simply by specifying them at the command line.

***Options***  
**template**  
Usage: `pyxam.py <template file>`  
This file specifies the primary LaTeX file for Pyxam to parse. This is the only required argument.  
**out**  
Usage: `pyxam.py -o <output directory>`  
Specify the path to a directory for Pyxam to use as the final location of exported files. By default this  will be a folder named /out in the same directory as the provided template file.    
**temp**  
Usage: `pyxam.py -tmp <temp directory>`  
Specify the path to a directory for Pyxam to use a temporary location for storing files. This folder will be removed along with its contents when Pyxam finishes. By default this will be a folder named /temp in the same directory as the provided template file.  
**figure**  
Usge: `pyxam.py -fig <figure directory>`  
When exporting to a format that requires a resources directory use this to specify the path to the exported resources. By default this will be a folder named /figures in the same directory as the provided template file.  
**number**  
Usage `pyxam.py -n <an integer value>`  
The number of exams to generate. Assuming your exams make use of random numbers or question rearrangment this will allow you to quickly create different exam versions.  
**format**  
Usage: `pyxam.py -f <format>`  
Specify the output format for Pyxam. By default Pyxam will export a .tex file. Avaialble formats include:
- **tex** A weaved copy of your original template file
- **html** An html formatted copy of your original template file*
- **pdf** A pdf version of your original template file
- **dvi** A dvi version of your original template file  

\*This format currently has some problems  
**shell**  
Usage: `pyxam.py -shl <shell>`  
Specify the shell to run the code through. By default this is Python. The other options include matlab, octave, and julia however they have not been tested.  
**clean**  
Usage: `pyxam.py -c>`  
Disable LaTeX cleanup. This is not currently implemented.  
**matplotlib**  
Usage: `pyxam.py -mpl`  
Disable the matplotlib library when parsing python code. This option is simply passed on to Pweave.  
**interactive**  
Usage: `pyxam.py -i <shell>`  
By default LaTeX compilation is run through texfot in order to reduce but not eliminate the amount of console output produced. This is extremely necessary when creating a large number of exams. When attempting to debug a LaTeX document however you may desire the default interactive LaTeX output. This flag disables texfot.  
**logging**  
Usage: `pyxam.py -l`  
This command can only be used on the command line. This enables logging messages throughout the Pyxam process. This is useful for debugging.  
**debug**  
Usage: `pyxam.py -d`  
By default the temporary directory is immediately deleted when Pyxam finishes, enabling debug mode leaves the temp folder undeleted. This is useful for debugging.
### Todos
The current planned feature list for the first release in rough order of expected completion:
- A full example set to act as tutorials and testing for mathematical exporting and formatting
- A Moodle XML export option
- Add a warning if the temp directory already exists
- First Name and last name specification on class lists along with smarting parsing of CSV files
- Reordering of multiple choice answers
- Quiet form of Pexpr{} so that the <%%> syntax can be dropped
- Adjustment of command matching so that '\\}' will be ignored during matching and replaced with '}' once matching is complete, this will help in an edge case where a } occurs in a python string
- Improvement to HTML export
- Testing of Matlab and Octave support
- Lacheck integration to help debug LaTex
- Well defined API, methods with clear arguments
- Well defined plugins, exporters, selectors, constants, etc.
- Aesthetic improvements, icon, custom argparse, ascii art, etc.
- Setup file 

### Contact
Pyxam is currently maintained by Eric Buss at the University of Alberta.  
You can reach him at ebuss@ualberta.ca

### License
Pyxam is not currently licensed. It is planned as open source software.  
Pweave is offered under its own licence provided in /pweave/LICENSE.TXT  
Texfot is offered under its own license provided in /texfot/texfot.pdf