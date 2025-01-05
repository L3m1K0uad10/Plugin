COMMENT_SYNTAX = {
    "python": {"single_line": ["#"], "multi_line": ["'''", '"""']},
    "javascript": {"single_line": ["//"], "multi_line": ["/* */"]}
}

def look_for_quotes(data, open_quote=None):
    """
    Identify all quote positions (both single, double, and triple quotes), handling escaped quotes and multiline quotes.
    Tracks open multiline quotes across lines.
    
    Parameters:
    - data (str): The current line of code.
    - open_quote (str): Tracks any currently open multiline quote (''' or \"\"\").

    Returns:
    - list: A list of quote positions in the line.
    - str: The updated state of open_quote (None if no multiline quote is open).
    """
    quotes_list = []
    i = 0

    while i < len(data):
        char = data[i]

        # Handle escaped quotes (e.g., \" or \')
        if char == "\\" and i + 1 < len(data) and data[i + 1] in ('"', "'"):
            i += 2
            continue

        # Handle triple quotes (''' or """)
        if char in ('"', "'") and i + 2 < len(data) and data[i:i+3] in ("'''", '"""'):
            triple_quote = data[i:i+3]
            if open_quote is None:  # Starting a new multiline quote
                open_quote = triple_quote
                quotes_list.append(i)  # Start of triple quote
                i += 3
                continue
            elif open_quote == triple_quote:  # Ending the current multiline quote
                quotes_list.append(i + 2)  # End of triple quote
                open_quote = None
                i += 3
                continue

        # Handle single and double quotes (e.g., " or ')
        if char in ('"', "'") and open_quote is None:  # Starting a new quote
            quotes_list.append(i)  # Start of quote
            open_quote = char
        elif char in ('"', "'") and open_quote == char:  # Ending the current quote
            quotes_list.append(i)  # End of quote
            open_quote = None

        i += 1

    # Return the list of quotes and the current state of open_quote
    return quotes_list, open_quote


def is_within_quotes(index, quotes_list):
    """
    Check if an index is within a pair of quotes.

    Parameters:
    - index (int): The position in the string to check.
    - quotes_list (list): A list of quote positions, alternating between open and close.
                          Example: [2, 5, 10, 15] -> '["..."]' and '["..."]'

    Returns:
    - bool: True if the index is within a quoted region, False otherwise.
    """
    # Ensure quotes_list has matching open-close pairs
    if len(quotes_list) % 2 != 0:
        # Unmatched quote, but continue processing
        quotes_list = quotes_list[:-1]  # Ignore the unmatched opening quote

    for i in range(0, len(quotes_list), 2):  # Step through open-close pairs
        if quotes_list[i] <= index <= quotes_list[i + 1]:
            return True
    return False


def check_for_single_line_comment(line, syntax, quotes_list):
    """
    Find the position of a single-line comment in a line, ignoring those inside quotes.

    Parameters:
    - line (str): The line of code to check for comments.
    - syntax (dict): A dictionary containing the "single_line" comment delimiters.
                     Example: {"single_line": ["#"]}
    - quotes_list (list): A list of quote positions (open-close pairs) in the line.

    Returns:
    - int: The position of the single-line comment, or -1 if no valid comment is found.
    """
    for comment_symbol in syntax["single_line"]:
        position = line.find(comment_symbol)
        
        # If comment symbol is found and is not within quotes, return its position
        if position != -1 and not is_within_quotes(position, quotes_list):
            return position
    
    # No single-line comment found
    return -1


def check_for_multiline_comment(line, quotes_list):
    """Detect multiline comments in Python."""
    multiline_delimiters = ["'''", '"""']
    for delimiter in multiline_delimiters:
        start_pos = line.find(delimiter)
        end_pos = line.rfind(delimiter)

        if start_pos != -1 and end_pos != -1 and not is_within_quotes(start_pos, quotes_list) and not is_within_quotes(end_pos, quotes_list):
            # Both start and end in the same line
            return delimiter, start_pos

        if start_pos != -1 and not is_within_quotes(start_pos, quotes_list):
            return delimiter, start_pos

        if end_pos != -1 and not is_within_quotes(end_pos, quotes_list):
            return delimiter, end_pos

    return None, None


def find_comment(data, language="python"):
    syntax = COMMENT_SYNTAX.get(language, {})
    comments_data = []
    is_inside_multiline = False
    current_delimiter = None
    multiline_start_line = None
    open_quote = None  # Tracks if inside a multiline quote
    count = 0

    for i, line in enumerate(data):
        # Get quotes list and update open_quote state
        quotes_list, open_quote = look_for_quotes(line, open_quote)

        # Check for single-line comments
        single_line_pos = check_for_single_line_comment(line, syntax, quotes_list)
        if single_line_pos != -1:
            count += 1
            comments_data.append({
                "id": count,
                "type": "single_line",
                "line": i,
                "col-1": single_line_pos,
                "col-2": len(line) - 1
            })

        # Check for multiline comments
        delimiter, position = check_for_multiline_comment(line, quotes_list)
        if delimiter:
            if not is_inside_multiline:
                is_inside_multiline = True
                current_delimiter = delimiter
                multiline_start_line = i
            elif delimiter == current_delimiter:
                is_inside_multiline = False
                comments_data.append({
                    "id": count,
                    "type": "multi_line",
                    "start_line": multiline_start_line,
                    "end_line": i,
                    "start_col": position,
                    "end_col": len(line) - 1
                })
                count += 1

    return comments_data