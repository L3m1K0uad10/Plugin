import ast
import json
import tokenize # library for tokenizing the code
from io import StringIO # library for input/output string

from utils.helpers import find_all


class CommentExtractor(ast.NodeVisitor):
    def __init__(self):
        self.comments = []

    def visit_Expr(self, node):
        if isinstance(node.value, ast.Str):
            self.comments.append(node.value.s)
        self.generic_visit(node)

    def extract_comments(self, code):
        # StringIO is used to convert the code string into a file-like object
        tokens = tokenize.generate_tokens(StringIO(code).readline) # tokenize the code
        for token in tokens:
            if token.type == tokenize.COMMENT: # check if the token is a comment
                self.comments.append(token.string)
        return self.comments
    

class CommentDetails:
    def __init__(self, code):
        self.code = code
        self.comments = {
            "single comment": {},
            "inline comment": {},
            "multiline comment": {}
        }
        self.extract_comments()

    def extract_comments(self):
        tokens = tokenize.generate_tokens(StringIO(self.code).readline) # gets the information of the tokens like start and end position
        #print(tokens)
        """ line_comments = {}
        multiline_comments = []
        current_multiline = None """

        for token in tokens:
            #print(token)
            if token.type == tokenize.COMMENT:
                self.comments["single comment"][len(self.comments["single comment"]) + 1] = {
                    "line": token.start[0],
                    "start_col": token.start[1],
                    "end_col": token.end[1]
                }
            elif token.type == tokenize.STRING:
                if token.string.startswith(('"""', "'''")):
                    # check if the possibility of nested strings that contain comment-like content
                    # for that we will check if it is preceded by an arithmetic operator or an assignment operator

                    if token.string.endswith(('"""', "'''")) and "\n" not in token.string:
                        precedent =  token.line[token.start[1] - 3 : token.start[1]] # get the 3 characters before the start of the string for checking the possibility of nested strings

                        if precedent != "":
                            if "+ - * / = ( [ {".find(precedent) == -1:
                                self.comments["inline comment"][len(self.comments["inline comment"]) + 1] = {
                                    "line": token.start[0],
                                    "start_col": token.start[1],
                                    "end_col": token.end[1]
                                }
                        else:
                            self.comments["inline comment"][len(self.comments["inline comment"]) + 1] = {
                                "line": token.start[0],
                                "start_col": token.start[1],
                                "end_col": token.end[1]
                            }
                    else:
                        precedent =  token.line[token.start[1] - 3 : token.start[1]] # get the 3 characters before the start of the string for checking the possibility of nested strings

                        if precedent != "":
                            if "+ - * / = ( [ {".find(precedent) == -1:
                                self.comments["multiline comment"][len(self.comments["multiline comment"]) + 1] = {
                                    "start_line": token.start[0],
                                    "end_line": token.end[0]
                                }
                        else:
                            self.comments["multiline comment"][len(self.comments["multiline comment"]) + 1] = {
                                "start_line": token.start[0],
                                "end_line": token.end[0]
                            }    

    def get_details(self):
        return self.comments
    

if __name__ == "__main__":
    # Example usage
    code = """
# simple addition
result = 5 + 5
print(result) # printing result
\"\"\"multiline comment\"\"\"
'''multiline comment2'''
print("# this is for testing comment")
\"\"\"
nothing is wrong it just a project
\"\"\"

# nested multi-line comments
    '''
        This is another multi-line comment.
        It also contains a nested multi-line comment.
    \"\"\"
        Nested multi-line comment inside another multi-line comment.
    \"\"\"
    '''

# nested strings that contain comment-like content 
nested_string = '''
This is a multi-line string inside a function.
It contains another string that looks like a comment.
\"\"\"
Nested string inside a multi-line string.
\"\"\"
\"\"\"
Another nested string inside a multi-line string.
\"\"\"
Deeply nested string inside another nested string.
\"\"\"
\"\"\"
'''
"""

    details = CommentDetails(code)
    print(json.dumps(details.get_details(), indent = 4))


{
    "single comment": {
        "1": {
            "line": 2,
            "start_col": 0,
            "end_col": 17
        },
        "2": {
            "line": 4,
            "start_col": 14,
            "end_col": 31
        }
    },
    "inline comment": {
        "1": {
            "line": 5,
            "start_col": 0,
            "end_col": 22
        },
        "2": {
            "line": 6,
            "start_col": 0,
            "end_col": 22
        },
    },
    "multi-line comment": {
        "1": {
            "start_line": 8,
            "end_line": 10
        }
    }
}

