# Pyxam
Pyxam is a spiritual reacration of the R exam package for python. An open source solution for combining LaTeX documents with Python source code and additional options to generate high quality exam forms. Pyxam serves three key purposes:

- Pipeline compiling code, adding the results to documents and then compiling LaTeX
- Provide key features needed for exams, such as question reordering, inserting student information, and keeping track of answer keys
- Make exporting into a variety of formats including PDF and Moodle easier than ever

This document gives a basic overview of the current version of Pyxam and also serves as a light design document for future additions. For more detailed instructions on how to get the most out of Pyxam check out the example files in the /examples directory found in the main github directory.  
### Version
0.2.1       
### Dependencies
Pyxam requires a set of open source software to be used and run succesfully. Though a central goal of Pyxam is to keep the program simple and lightweight such dependencies are unavoidable. In order to run Pyxam you will need the following software:

- A LaTeX compiler and the examclass 
- Python 3.4 or greater
- Perl 5 or greater
- And the Matplotlib library for Python

