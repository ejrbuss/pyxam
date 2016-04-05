# Author: Eric Buss <ebuss@ualberta.ca> 2016
"""
# Module exporter

This module is responsible for copying files from the tmp directory to the out directory, calling the method, and
reading any csv population data associated with this Pyxam call.



The stages of the export process are managed with file extensions. All files that end with .cmp (short for compiled)
will be renamed with either a number or letter depending on whether the `alphabetize` flag has been set and the
extension .mix. These files are then passed to the method for mixing along with csv data. The method is expected to
add any necessary .mix files. At this point all .mix files are copied to the out directory with the extension specified
by the compile format.
"""
import os
import options
import fileutil
import formatter


# A map of all currently loaded methods
_methods = {}


def export():

    # Export files
    for file in fileutil.with_extension('.cmp'):
        fileutil.move(
            file,
            options.state.out() + '/' +
            options.state.title() + '_' +
            os.path.basename(file[:-4]) +
            ('_solutions' if options.state.solutions() else '') +
            '.' + formatter.get_extension()
        )
    # Export figures
    fileutil.copy_figure()

#TODO finish