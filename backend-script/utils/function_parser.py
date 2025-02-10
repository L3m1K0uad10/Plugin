import re 

# NOTE: code for python language


def get_func_identifier(token_pos, func_token, instruction):
    """ 
    returns a function identifier's positions, start and end col
    """

    identifier_start_pos = token_pos + (len(func_token) - 1) + 2 # going on the assumption that after def there is one whitespace before the identifier starts
                                                                # and that the func token it self has a considerable length in this case 3
    # let's find the occurence position of ( 
    lbracket = instruction.find("(")

    identifier_end_pos  = lbracket - 1 # going on the assumption that the identifier and the open bracket are not separated

    return identifier_start_pos, identifier_end_pos 


def get_func_token(instruction, func_token):
    """
    return the starting position of a function token  
    """

    match = re.search(rf'\b{func_token}', instruction)
    position = match.start() if match else -1

    return position


def is_func(instruction, func_token):
    """
    takes an instruction and scanns it to identify
    is there is a possibility that there may have 
    a function defined in it.  
    """
    match = re.search(rf'\b{func_token}', instruction)
    position = match.start() if match else -1

    if position != -1:
        return True 
    else:
        return False


def find_function(instructions):
    """  
    instructions is a List of code line instruction
    """

    function_data = []
    count = 0
    func_token = "def"

    for i, instruction in enumerate(instructions):
        if is_func(instruction, func_token):
            pos = get_func_token(instruction, func_token)
            start_col, end_col = get_func_identifier(pos, func_token, instruction)
            count += 1

            function_data.append({
                "id": count,
                "type": "function identifier",
                "line": i,
                "start_col": start_col,
                "end_col": end_col
            })

    return function_data



"""  ALGORITHM FOR PYTHON CODES

1 - check for the presence of the "def" keyword
2 - check vocabulary function definition:
    "def" is preceding either by an indentation or nothing

if 1 && 2:
    return the function identifier detail
"""


code = """
# function for computing factorial
def factorial(num):
    if num == 1 or num == 0:
        return 1
    return num * factorial(num - 1)

def combination(n, k):
    if n < k:
        return
    res = (factorial(n)) / (factorial(k) * factorial(n - k))
    return res

n = 4
print(f"factorial of {n} is {factorial(n)}")
print(f"C(4, 2) is {combination(4, 2)}")

"""
code_splitted = code.strip().split("\n")

res = find_function(code_splitted)
for r in res:
    print(r)