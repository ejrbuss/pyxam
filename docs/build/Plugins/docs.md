
# Plugin docs

The docs plugin is used to build the documentation for Pyxam quickly and easily from a combination of documentation
source files and python docstrings. All documentation is written in markdown and then converted to HTML by this plugin.

***
**load**()

Loads the doc plugin.

**localdocs** `-ld`, `-localdocs`, `--localdocs` *(bool) False*

This flag determines whether documentation pages will link to repo pages or to files on your local computer.

**docs** `-docs`, `--docs` *(bool) False*

If this option is supplied Pyxam's docs are rebuilt. Docs are built by:
 - Finding the paths to the documentation source, module files, and plugin files
 - Copying all docstrings from module files and plugin files to the documentation source directory
 - Converting all markdown files in the documentation source directory to HTML
 - Perform post processing to add a javascript search bar and sidebar along with minor changes to HTML
 - Copying those files to the documentation build directory
It can be useful to regenerate the docs if you have added a new Plugin and want to read its documentation.

***
**get_docs**(*docs, directory*)


Copies all python docstrings from directory to docs.



`docs`  The directory where the docstrings will be copied to


`directory`  The directory whose python files while be scraped for docstrings

***
**compile_docs**(*docs*)


Converts all markdown files found in docs to HTML and then copies them to the build directory. All folders are run
recursively.



`docs`  The documentation directory to compile


**returns**  test

***
**compile_doc**(*doc*)


Converts the given file from markdown to HTML and then copies it to the build directory.



`doc`  The file to compile
