**parser_preprocessor**(*src*)


    
    Swaps all instances of \question with \titledquestion{question} to help translate to other formats.
    <br />`src`  The template source
    **<br />returns&nbsp;**  The modified source
    
***
**parser_postprocessor**(*intermediate*)


    
    Because LaTeX has no defined Prompt the first string, equations, and images found in a question are put under a
    prompt Token.
    <br />`intermediate`  An intermediate parse object
    **<br />returns&nbsp;**  A modified intermediate
    