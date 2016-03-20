
# Module filters

This module provides helper functions for transforming a Pyxam parse tree.

***
**remove_name**(*ast, name*)


Remove all tokens with a given name along with all their sub tokens. Tokens will be removed recursively from the
provided tree



`ast`  The tree to walk and remove tokens from


`name`  The token name to remove


**returns**  The modified tree

***
**recursive_filter**(*fn, node*)


Filters a list and recursively filters any sublists attached to the node.



`fn`  The filter function


`node`  The starting node


**returns**  the filtered node

***
**apply_function**(*ast, fn, name*)


Applies a transform function to all nodes of the tre that match the name given. The function is applied recursively
to every part of the tree.



`ast`  The tree to transform


`fn`  The function to apply


`name`  The token name to apply the function to


**returns**  the modified tre

***
**pass_through**(*intermediate*)


A dummy function that simply returns its provided intermediate.



`intermediate`  The intermediate


**returns**  the intermediate

***
**pop_unknowns**(*ast*)


Replace every unknown token with the its definition tokens. This process is applied recursively and all popped
tokens are also processed for unknowns



`ast`  The tree whose unknowns are being popped


**returns**  the modified tree

***
**img64**(*ast*)


Convert image file paths to base64 representations of those images.



`ast`  The tree whose images will be converted


**returns**  The modified tree

***
**homogenize_strings**(*ast*)


Combine consecutive string tokens into a single string. Applied recursively.



`ast`  The tree whose strings tokens are combined


**returns**  The modified tree

***
**promote**(*ast, name*)


Finds the first instance (based on a depth first search) of a token with the matching name.



`ast`  The tree to be searched


`name`  The token name to find


**returns**  the subtree starting at the matching token

***
**transform_questions**(*ast*)


Performs a number of transformations to questions in the tree. These include converting shortanswer questions to
numerical questions, multichoice questions to multiselect questions, and numerical questions to calculated
questions. Applied recursively.



`ast`  The tree to modify


**returns**  the modified tree

***
**to_numerical**(*question*)


Transforms shortanswer token definitions from
```
solution:
    $:
        var = answer \pm tolerance
```
to
```
solution:
    answer
    tolerance:
        tolerance
```


`question`  The question to transform

***
**to_multiselect**(*question*)


Transforms multichoice token definitions from
```
choices:
    correctchoice:
        choice
    correctchoice:
        choice
```
to
```
single: false
choices:
    correctchoice:
        choice
    correctchoice:
        choice
```


`question`  The question to transform

***
**to_calculated**(*question*)


Transforms numerical token definitions from
```
solution:
    answer
    tolerance:
        tolerance
```
to
```
solution:
    answer
    tolerance:
        tolerance
    params:
        param:
            name
            maximum:
                value
            minimum:
                value
            decimal:
                value
                formatter.Token('tolerance', [tolerance], None, ''))
```


`question`  The question to transform
