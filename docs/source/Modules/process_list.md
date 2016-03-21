
# Module process_list

This module manages the Pyxam process list which is a consecutive set of functions that are run in order. This process
list can be changed during runtime via a number of function calls.

***
**ready**()


**<br />returns &nbsp;**  True as long as there are items in the process list

***
**append**(*process*)



Append a process to the end of the process list, or if the provided argument is a list, append all the items to
the process list.
`process` 
**<br />returns &nbsp;**  None

***
**run_after**(*process, hook*)



Add a hook to run after a given process.
`process`  The string name of the process to hook
`hook`  A function to run
**<br />returns &nbsp;**  None

***
**run_before**(*process, hook*)



Add a hook to run before a given process.
`process`  The string name of the process to hook
`hook`  A function to run
**<br />returns &nbsp;**  None

***
**consume**(*arg=None*)



Run the next process in the process list with any provided arguments.
`arg`  Arguments
**<br />returns &nbsp;**  Arguments for the next process

***
**clear**()


Clears the process list of all waiting processes.
