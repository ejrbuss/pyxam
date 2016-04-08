# Pyxam Docs

This is the code documentation for the Pyxam Exam module. For details on installation and usage checkout the
[readme](https://github.com/balancededge/pyxam).

### Overview

Pyxam is a python library for building exams. Central to this task are three major features, format flexibility, version
independence, and python code weaving. Format flexibility means allowing exams to be written in a variety of formats and
easily exported to others. This may mean writing an exam in LaTeX and then exporting to HTM or writing an exam in Emacs
org mode and then exporting to Moodle. Version independence means providing ways of providing version specific
information within an exam. For instance you may want to include student information (such as their name or student
number). You may also want to generate different exam versions where questions have different parameters and answers,
but you do not want every student to have a different exam as that is to difficult to mark, instead you only want three
exams. Pyxam makes accomplishing this task easy. Python code weaving means that you can write Python code write in your
document and it will be run to produce specific parts of your exam. Access to an entire program language when creating
a document provides infinite flexibility so Pyxam provides a small API to help simplify the process.


 
This code documentation is broken into a few major sections. The [Getting Started](%/1_Getting_Started.html) page is where
you will want to head if you are new to Pyxam. The [Framework](%/Framework/0_index.html) pages provide an overview of the
general structure of Pyxam from a conceptual level. The [Changelog](%/Changelog/0_index.html) pages provide details on
version changes. The Modules and Plugin pages provide API documentation and links to source for the codebase itself. You
can search any of this content using the search bar on the side which will only show pages that match your search.


### Content

<!-- table -->



### Thanks

Pyxam is inspired by the [R exam package](https://cran.r-project.org/web/packages/exams/index.html) which used
[Sweave](https://www.statistik.lmu.de/~leisch/Sweave/), a tool for running inline R code in LaTeX documents, to generate
exams. Pyxam aims to bring similar functionality to inline Python code using [Pweave](http://mpastell.com/pweave/), a tool
that emulates Sweave for Python. Without the great work by these other parties Pyxam would not have been created.

