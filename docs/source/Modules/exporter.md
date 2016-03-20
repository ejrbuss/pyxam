
# Module exporter

This module is responsible for copying files from the tmp directory to the out directory, calling the selector, and
reading any csv population data associated with this Pyxam call.

The stages of the export process are managed with file extensions. All files that end with .cmp (short for compiled)
will be renamed with either a number or letter depending on whether the `alphabetize` flag has been set and the
extension .mix. These files are then passed to the selector for mixing along with csv data. The selector is expected to
add any necessary .mix files. At this point all .mix files are copied to the out directory with the extension specified
by the compile format.

***
**export**()

Mix the composed files with the specified selector then copy all mixed files to the out directory with the
appropriate names. If any files are in the figure directory they are copied out as well.

***
**csv_read**(*file*)


Attempts to read the provided CSV file.



`file`  The csv file to read


**returns**  a list of dictionaries containing `number` and `name` entries

***
**add_selector**(*name, selector*)


Add a selector to the selector list.



`name`  The name of the selector being added


`selector`  The selector to add
