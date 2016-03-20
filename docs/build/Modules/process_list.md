**ready**()



**returns**  True as long as there are items in the process list

***
**append**(*process*)


Append a process to the end of the process list, or if the provided argument is a list, append all the items to
the process list.


`process` 


**returns**  None

***
**run_after**(*process, hook*)


Add a hook to run after a given process.


`process`  The string name of the process to hook


`hook`  A function to run


**returns**  None

***
**run_before**(*process, hook*)


Add a hook to run before a given process.


`process`  The string name of the process to hook


`hook`  A function to run


**returns**  None

***
**consume**(*arg=None*)


Run the next process in the process list with any provided arguments.


`arg`  Arguments


**returns**  Arguments for the next process
