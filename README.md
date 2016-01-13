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
If Python 3 is in your PATH as ```python3 ``` Pyxam can be run from the command line like so:
```sh
$ pyxam.py [options] <template file>
```
Otherwise you need to run Pyxam under Python like so:
```sh
$ python pyxam.py [options] <template file>
```
Pyxam can also be called by another Python program. There is currently no formal API however pyxam can be run with default options with the following:
```python
import pyxam                                # Import pyxam module
options = pyxam.pyxamopts.PyxamOptions()    # Get a default options object
options.template = '<template file>'        # Add your template file
pyxam.core.pyxam(options)                   # Run the options
```
### Using Pyxam

### Todos

### Contact

### License
