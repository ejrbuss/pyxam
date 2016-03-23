
# Module pyxam

This is the primary script for Pyxam. This script can be run from the command line with Pyxam's options or run in api
mode from another python script. This script also checks Python dependencies for:

`matplotlib` Needed for generating figure images

`numpy` Needed for generating figure images


***
**welcome**()

    
    Prints the Pyxam title and version number when not in api mode.
    
***
**goodbye**()

    
    Prints a goodbye message when not in api mode.
    
***
**start**(*args, api=True*)


    
    Start Pyxam with a set of options.

    <br />`args`  A list of options provided in command line syntax
    <br />`api`  A flag indicating if Pyxam is being called as an api

    Start adds all needed processes to the option list and then loops % pyxam!link process_list.consume until there are
    no processes left.
    