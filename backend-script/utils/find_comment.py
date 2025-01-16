
def track_quotes(line):
    quotes = []
    quote = None

    for index, symbol in enumerate(line):
        if symbol in ['"', "'"]:
            if quote is None:  # No open quote yet
                quote = symbol
                quotes.append(index)  # Start of quote
            elif quote == symbol:  # Closing the same type of quote
                quotes.append(index)  # End of quote
                quote = None  # Reset
    return quotes



def is_within_quotes(quotes, start_col, end_col):
    
    if len(quotes) != 0:
        if start_col >= quotes[0] and end_col <= quotes[len(quotes) - 1]:
            return True 
    else:
        return False
    
    
def prev_sequence_check(line, start):
    """  
    purpose: apply heuristic for detecting whether an assumpted comment is really a comment or a string
    """
    
    if len(line) != 0:
        if line[start - 1] not in ["=", "+"] and line[start - 2] not in ["=", "+"]:
            return True 
        else:
            return False


def find_comments(data):

    single_comment_symbol = "#"
    tracker = False # tracking the assumption of existence of inline comment
    count, flag = [0, False] # for supporting some behaviour track regarding multi-line comment
    line_tracker = None # assumpted inline line
    col_tracker = None # assumpted inline col

    comment_data = []

    """ line_data = data.split("\n") """ # this line was for testing purposes where i have to split the data into line, but normally the data pass to the function should already be splitted

    for index, line in enumerate(data):

        start_col = line.rfind(single_comment_symbol)
        end_col = len(line) - 1
        
        if tracker == False:
            if start_col != -1 and not is_within_quotes(track_quotes(line), start_col, end_col) and start_col != end_col:
                comment_data.append({
                    "id": index,
                    "type": "single line",
                    "line": index,
                    "start_col": start_col,
                    "end_col": end_col
                })
        else:
            if start_col != -1 and start_col != end_col:
                continue
            for symbol in ["'''", '"""']:
                start = line.find(symbol)
                end = line.rfind(symbol)

                if start == end:
                    end = -1

                if start != -1 and end == -1:
                    tracker = False
                    comment_data.append({
                        "id": index,
                        "type": "multiline",
                        "start": {
                            "line": line_tracker,
                            "start_col": col_tracker
                        },
                        "end": {
                            "line": index,
                            "start_col": start
                        }
                    })
                    flag = True
                    count += 1
                else:
                    continue

        if not flag:
            for symbol in ["'''", '"""']:
                start = line.find(symbol)
                end = line.rfind(symbol)

                if start == end:
                    end = -1

                if start != -1 and end != -1 and prev_sequence_check(line, start) and start != end:
                    comment_data.append({
                        "id": index,
                        "type": "inline",
                        "line": index,
                        "start_col": start,
                        "end_col": end_col
                    })
                if start != -1 and end == -1:
                    tracker = True 
                    line_tracker = index
                    col_tracker = start
        
        if count == 1:
            print(count, flag, index)
            flag = False
            count = 0
        
    return comment_data




"""
we go on the basics that a code is well written:

- check each line code data after another
- check for # or // last occurence in a line and if is not between any quotes(single, double, triple)
    return single line comment 

keep track of the quotes for further possible multi-line block check:
2 - 1 check for triple quote if there is, look for a close triple and if =, + symbol does not precede the open triple quote  
    return inline comment 
2 - 2 only one triple quote is the line data
    track T that for further possible multi-line block check
check the next line datas:
2 - 2 - 1 ignore all #, // pair double quote, single quote and escaped triple quote as they may be within a multi-line block
2 - 3 find one triple quote in the line data matching the track quote T 
    return multiline comment 
"""


if __name__ == "__main__":
    
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

    comments = find_comments(code)
    for comment in comments:
        print(comment)
