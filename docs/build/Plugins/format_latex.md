**parser_preprocessor**(*src*)


Swaps all instances of \question with \titledquestion{question} to help translate to other formats.


`src`  The template source


**returns**  The modified source

***
**parser_postprocessor**(*intermediate*)


Because LaTeX has no defined Prompt the first string, equations, and images found in a question are put under a
prompt Token.


`intermediate`  An intermediate parse object


**returns**  A modified intermediate
