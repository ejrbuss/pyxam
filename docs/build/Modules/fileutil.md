
# Module fileutil

This Module provides helper functions to other modules for working with files.

***
**build_files**()

Find the absolute file path for the template, tmp directory, and out directory and update thir options to point to
their absolute path. Create the tmp and out directories if necessary. Warns user if tmp is going to be overridden
as this may delete files. Changes the current working directory to tmp.

***
**cleanup**()

When not in debug mode remove all temporary folders.

***
**with_extension**(*extension*)


Find all files in the current working directory that match the given extension.



`extension`  The extension to match



**returns**  a list of files that end in the provided extension

***
**read**(*file*)


Read a string from a file.



`file`  The relative or absolute path to the file to read


**returns**  The string contents of the file

***
**write**(*file, src*)


Write a string to a file.



`file`  The relative or absolute path to the file to write to


`src`  The string to write to the file

***
**copy_figure**()

Copy the figure directory to the out directory along with its children.

***
**remove**(*file*)


Remove a file or directory. If removing a directory all contents of that directory will also be removed.



`file`  The relative or absolute path for the file or directory or directory to remove

***
**is_bin**(*file*)


Check if a file is a binary file.



`file`  The file to check


**returns**  True if the file is a binary file
