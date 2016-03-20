**compile_**(*option, value=None*)


Set the value field of an option with the correct type and/or retrieve the compiled value of the option.
The compiled value is the default if no value hs been provided by the current or past callers.


`option`  The option to compile


`value`  The value to try and set, when None the value is not set


**returns**  The compiled value

***
**add_option**(*name, flag, description, default, type_, value=None*)


Add an option.


`name`  The name of the option


`flag`  The flag for the option


`description`  A description of the option


`default`  The default value of the option


`type_`  The type of the option


`value`  A value, defaults to None


**returns**  The value of the option after parsing any hanging options

***
**load_options**(*options*)


Load options provided as a list in command line syntax.


`options`  A list of options to load


**returns**  None

***
**load_template**()

Load the template option. Expects to be the last option loaded.


**returns**  None

***
**get_help**()

Get a string representing the help message for all options currently added.


**returns**  The help string
