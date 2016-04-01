# The Process List 
The process list is the highest level of the Pyxam process. The process list is simply a list of functions that are run
one after the other until the list is empty. Once empty Pyxam is finished and the program exits. This process list can be
changed at any time. You can add new functions to the list, remove functino, and reorder them at any point when Pyxam is
running. Additionally the return value of a function in the process list is used as the arguments for the next function
allowing information to be easily passed from one function to the next or transformed in between.  

The base process list along with a short description of each function is provided below:
 - `load_options` loads the command line options
 - `welcome` displays a welcome message
 - `load_plugins` loads all available plugins
 - `build_files` fixes paths and builds all necessary files
 - `run_commands` prepossesses commands in the template (see [bang](%/Modules/bang.html))
 - `post_status` posts the current state of all options
 - `weave` runs any inline code within the template
 - `parse` reads the template document into an intermediate format (see [formatter](%/Modules/formatter.py))
 - `compose` converts the intermediate format into the output format
 - `export` moves files from the tmp directory to the final out directory
 - `cleanup` removes all temporary files
 - `unload_plugins` unloads all available plugins
 - `goodbye` display a goodbye message

In order to hook into the process list there are three helper functions provided. These functions use the name of
processes to identify where you want to insert into the process list.
```python
# Run after another function
process_list.run_after('welcome', my_function)
# Run before another function
process_list.run_before('export', my_function)
# Inserting relative to your already inserted function will insert relative the first occurence
proces_list.run_before('my_function', my_function)
# Append a process or a list of processes to the end of the process list
process_list.append(my_function)
process_list.append([my_function, my_function])
```