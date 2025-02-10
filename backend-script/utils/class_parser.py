import re 

# NOTE: code for python language


def get_class_identifier(token_pos, class_token, instruction):
    """ 
    returns a class identifier's positions, start and end col
    """

    identifier_start_pos = token_pos + (len(class_token) - 1) + 2 

    lbracket = instruction.find("(")
    colon = instruction.find(":")

    if lbracket != -1:
        identifier_end_pos  = lbracket - 1 
    elif colon != -1:
        identifier_end_pos  = colon - 1 

    return identifier_start_pos, identifier_end_pos 


def get_class_token(instruction, class_token):
    """
    return the starting position of a class token  
    """

    match = re.search(rf'\b{class_token}', instruction)
    position = match.start() if match else -1

    return position


def is_class(instruction, class_token):
    """
    takes an instruction and scanns it to identify
    is there is a possibility that there may have 
    a class defined in it.  
    """
    match = re.search(rf'\b{class_token}', instruction)
    position = match.start() if match else -1

    if position != -1:
        return True 
    else:
        return False


def find_class_identifier(instructions):
    """  
    instructions is a List of code line instruction
    """

    class_data = []
    count = 0
    class_token = "class"

    for i, instruction in enumerate(instructions):
        if is_class(instruction, class_token):
            pos = get_class_token(instruction, class_token)
            start_col, end_col = get_class_identifier(pos, class_token, instruction)
            count += 1

            class_data.append({
                "id": count,
                "type": "class identifier",
                "line": i,
                "start_col": start_col,
                "end_col": end_col
            })

    return class_data



"""  ALGORITHM FOR PYTHON CODES

1 - check for the presence of the "class" keyword
2 - check vocabulary class definition:
    "class" is preceding either by an indentation(for nested class) or nothing

if 1 && 2:
    return the class identifier detail

NOTE: why we are not going to consider the case that there might have
commented class definition, because anyway the comment will be translated
later in the process too, for the project's sake.
"""


code = """
# definining an object
class Person:
    def __init__(self, name, nationality, age):
        self.name = name
        self.nationality = nationality
        self.age = age

    def info(self):
        print(f"name: {self.name}")
        print(f"nationality: {self.nationality}")
        print(f"age: {self.age}")

person1 = Person("Stephen", "Zambian", 21)
person1.info()
"""

code2 = """
# definining an object
class Person:
    def __init__(self, name, nationality, age):
        self.name = name
        self.nationality = nationality
        self.age = age

    def info(self):
        print(f"name: {self.name}")
        print(f"nationality: {self.nationality}")
        print(f"age: {self.age}")

    class School:
        def __init__(self, name, location, course):
            self.name = name 
            self.location = location
            self.course = course

person1 = Person("Stephen", "Zambian", 21)
person1.info()
"""

code_splitted = code2.strip().split("\n")

res = find_class_identifier(code_splitted)
for r in res:
    print(r)