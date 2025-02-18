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
        self.details = {
            "single comment": {},
            "inline comment": {},
            "multi-line comment": {}
        }
        self.extractor = CommentExtractor()
        self.comments = self.extractor.extract_comments(code)
        self.process_comments()
    
    def process_comments(self):
        lines = self.code.split('\n')
        for i, line in enumerate(lines):
            for comment in self.comments:
                if comment in line:
                    start_col = line.index(comment)
                    end_col = start_col + len(comment)
                    if line.strip().startswith(comment):
                        self.details["single comment"][len(self.details["single comment"]) + 1] = {
                            "line": i + 1,
                            "start_col": start_col,
                            "end_col": end_col
                        }
                    else:
                        self.details["inline comment"][len(self.details["inline comment"]) + 1] = {
                            "line": i + 1,
                            "start_col": start_col,
                            "end_col": end_col
                        }

        multi_line_comments = self.extract_multi_line_comments()
        for idx, (start_line, end_line) in enumerate(multi_line_comments):
            self.details["multi-line comment"][idx + 1] = {
                "start_line": start_line,
                "end_line": end_line
            }
    
    def extract_multi_line_comments(self):
        multi_line_comments = []
        in_comment = False
        start_line = 0
        lines = self.code.split('\n')
        for i, line in enumerate(lines):
            if '"""' in line or "'''" in line:
                if not in_comment:
                    in_comment = True
                    start_line = i + 1
                else:
                    in_comment = False
                    end_line = i + 1
                    multi_line_comments.append((start_line, end_line))
        return multi_line_comments

    def get_details(self):
        return self.details
    


if __name__ == "__main__":
    code = """
# This is a comment
# This is another comment
print("Hello, world!")

''' This is a multi-line comment
This is another line of the comment
'''

"# This is a string, not a comment"

x = 5 # This is an inline comment # it continues
"""
    code2 = """
# simple addition
result = 5 + 5
print(result) # printing result
\"\"\"multiline comment\"\"\"
'''multiline comment2'''
print("# this is for testing comment")
\"\"\"
nothing is wrong it just a project
\"\"\"
"""
    """ parsed_code = ast.parse(code)

    extractor = CommentExtractor()
    extractor.visit(parsed_code)

    extracted_comments = extractor.extract_comments(code)

    print("Extracted comments:", extracted_comments)

    comment_details = CommentDetails(code.split("\n"), extracted_comments)
    print(comment_details.get_detail())  """

    details = CommentDetails(code2)
    print(json.dumps(details.get_details(), indent = 4))


{
    "single comment": {
        1: {
            "line": 1,
            "start_col": 0,
            "end_col": 15
        },
        2: {
            "line": 3,
            "start_col": 14,
            "end_col": 29
        }
    },
    "inline comment": {
        1: {
            "line": 4,
            "start_col": 0,
            "end_col": 22
        },
        2: {
            "line": 5,
            "start_col": 10,
            "end_col": 23
        }
    },
    "multi-line comment": {
        1: {
            "start_line": 7,
            "end_line": 9
        }
    }
}