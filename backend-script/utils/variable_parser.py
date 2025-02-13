import keyword
# print(keyword.kwlist)
# print(keyword.softkwlist)


class Tokenizer:
    """  
    special Tokenizer designed to take as attribute a string sentence as 
    well as a list of string sentence

    designed for my use specifics

    return tokens
    return tokens occurence
    """
    def __init__(self, string:str|list):
        self.string = string

    def tokenize(self):
        if type(self.string) == str:
            tokens = self.string.split(" ")
        else: # it's definitely going to be a list then
            tokens = []
            for string in self.string:
                inner_tokens = string.split(" ")
                for token in inner_tokens:
                    tokens.append(token)

        return tokens
    
    def count_token(self, tokens):
        count = {}
        for token in tokens: # don't need to worry about repetitive token count, because it's a dict, each time it will refer to the key which obviously going to update it to the exact count again
            count[token] = tokens.count(token)

        return count
    

class VariableParser:
    """  
    takes a list of tokens as arguments and returns a list of variable 

    NOTE: it's all done on the basics of code parsing
    """
    def __init__(self, tokens:list):
        self.tokens = tokens 
        self.variables = []






#text = "GOD has always been there."
''' 
text = """yours is the kingdom and the power
forever
and evermore amen"""
'''
code = '''
def get_func_identifier(token_pos, func_token, instruction):
    """ 
    returns a function identifier's positions, start and end col
    """

    identifier_start_pos = token_pos + (len(func_token) - 1) + 2 

    # let's find the occurence position of ( 
    lbracket = instruction.find("(")

    identifier_end_pos  = lbracket - 1 

    return identifier_start_pos, identifier_end_pos 
'''

obj = Tokenizer(code.split("\n"))
tokens = obj.tokenize()

print(tokens)
counts = obj.count_token(tokens)
print(counts)



"""  
PROBLEM: find all the variable declared, used in a code

INPUT: code instructions list

OUTPUT: list of variables dict

SOLUTION: - tokenize each instruction present in the INPUT
                return tokens
          - count the frequency/occurence of each tokens in the entire INPUT
                BEFORE CLEAN TOKEN e.g "instruction.find(tag) ==> instruction, find(), tag
                return dict details of tokens count
          - figure out which among the tokens are variables and
                return the details
                how it can be done?:
                    - some variable, class attribute will start with self.
                    - a variable should not be a keyword, therefore filter accordingly
                    - ...

POSSIBLE VARIABLE: x , isStudent, count, n, y, doc etc...

NOT VARIABLE: True, input, list etc... at least in python




POSSIBLE TOKEN CLEANING CASE TO HANDLE:
Here are the possible cases in which we can find and extract variables
    1. Simple Assignment
        fruits = []  # 'fruits' is a variable

    2. Method Calls/Function Calls
        fruits.append(fruit)  # 'fruits' and 'fruit' are variables

    3. Tuple or Multiple Assignment
        x, y = 5, 10  # 'x' and 'y' are variables



"""