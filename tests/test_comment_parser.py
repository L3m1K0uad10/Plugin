import pytest 
import comment.comment_parser as comment



def test_extract_comments():

    code = """
# comment 1
x = 2 + 3 # comment 2
text = "# not comment 1"
text = "# not comment 2" # comment 3

cube_area = side * side

'''comment 4'''
text = '''not comment 3'''
\"""comment 5\"""
y = x - 2
stack = None
'''# comment 6'''

circle_area = pi * math.pow(radius, 2)

'''
    comment 7 starts here
    and finishes here
'''

list_ = [1, 2, 5]

\"""
    # comment 8
\"""
"""

    result = comment.find_comments(code)

    expected_result = [
        {"id": 1, "type": "single line", "line": 1, "start_col": 0, "end_col": 10},
        {"id": 2, "type": "single line", "line": 2, "start_col": 10, "end_col": 20},
        {"id": 3, "type": "single line", "line": 4, "start_col": 25, "end_col": 35},
        {"id": 4, "type": "inline", "line": 8, "start_col": 0, "end_col": 12},
        {"id": 5, "type": "inline", "line": 10, "start_col": 0, "end_col": 12},
        {"id": 6, "type": "inline", "line": 13, "start_col": 0, "end_col": 14},
        {
            "id": 7,
            "type": "multiline",
            "start": {"line": 17, "start_col": 0},
            "end": {"line": 20, "end_col": 0},
        },
        {
            "id": 8,
            "type": "multiline",
            "start": {"line": 24, "start_col": 0},
            "end": {"line": 26, "end_col": 0},
        },
    ]

    assert result == expected_result
