
# Module formatter

***
**get_extension**()

Get the output extension


**returns**  The output extension

***
**parse**()

source to ast


**returns** 

***
**compose**(*intermediates*)


ast to source


`intermediates` 


**returns** 

***
**pack**(*token, fmt*)


Convert a token into a string using the following rules:
- If the token name is contained in the format:
    - Append every pure string in that format
    - Append every tuple or list as the packed content of the token
- If the token name is not contained in the format
    - Append the packed content of the token


`token` 


`fmt` 


**returns** 

***
**add_format**(*fmt*)


Check format signature before adding.
Insert into formats at all valid extensions.
Convert format list to Token list.


`fmt`  The format map


**returns**  None

***
**unpack**(*token, fmt, tail=False*)


Convert format list to a regex using the following rules:
- Convert pure strings to pure strings within the regex with all regex characters escapted
- Convert empty tuples to non-greedy character grabbers (.*?)
- Convert lists to recursively obtain the regex of the token contained within that list
- Throw an error for any other input
If a tail prefix the regex with a start of string whitespace regex and append a end of string or
the last entry in the format list regex


`token`  The token to build the regex for


`fmt`  The reference format


`tail`  Whether the regex should have a prefix and postfix applied


**returns**  The regex

***
**resolve**(*src, fmt*)


Convert a string source into an abstract syntax tree (ast). A format containing a list of valid
tokens must be provided. Any string sequences that cannot be matched will be returned as
raw characters


`src`  The source to convert into an ast


`fmt`  The format providing the tokens


**returns**  The ast

***
**determine**(*src, fmt*)


Determine what token a specific string sequence begins with. If no token can be found in the given
template a raw character is returned off the top.


`src`  The string sequence


`fmt`  The format providing the tokens


**returns**  The matched token, The unmatched sequence

***
**check**(*token, src, fmt, debug=False*)





`token` 


`src` 


`fmt` 


`debug` 


**returns** 
