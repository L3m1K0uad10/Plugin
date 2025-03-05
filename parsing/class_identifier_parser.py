import ast 
import builtins
import keyword
import json

from .utils.helpers import find_all


"""  
NOTE: better check whether the code is error free, 
and throw an error if it does before any further processing
"""


code = '''
class Person:
    def __init__(self, name):
        self.name = name
    def display(self):
        print(self.name)

p1 = Person("Lemi")
p1.display() 
'''

class ClassIdentifierExtractor(ast.NodeVisitor):
    def __init__(self):
        self.identifiers = set()  
        self.builtins = set(dir(builtins))
        self.keywords = keyword.kwlist

    """ def visit_Name(self, node):
        if isinstance(node.ctx, (ast.Store, ast.Load)):  
            if node.id not in self.builtins and node.id not in self.keywords:
                self.identifiers.add(node.id)
        self.generic_visit(node)   """

    def visit_ClassDef(self, node):
        self.identifiers.add(node.name)
        self.generic_visit(node)

    def get_identifiers(self):
        return self.identifiers
    

parsed_code = ast.parse(code)
"""ast.dump(parsed_code, indent = 4)"""

extractor = ClassIdentifierExtractor()
extractor.visit(parsed_code)

extracted_identifiers = extractor.get_identifiers()

#print("Extracted class identifiers:", extracted_identifiers)



class ClassIdentifierDetails:
    identifiers = []
    def __init__(self, instructions:list, identifiers:set):
        self.instructions = instructions
        self.identifiers = identifiers
    
    def _occurence(self):
        for i, instruction in enumerate(self.instructions):
            tokens_occurences = find_all(instruction) # returns a dictionary of the occurence of all 

            dict_ = {}
            
            for identifier in self.identifiers:
                if identifier in tokens_occurences.keys():
                    dict_[identifier] = tokens_occurences[identifier]

            if len(dict_) != 0:
                dict_["line"] = i
                ClassIdentifierDetails.identifiers.append(dict_)
        
        return ClassIdentifierDetails.identifiers
    
    def get_detail(self):
        self._occurence()

        json_data = {}
        count = 0

        for line_identifiers in ClassIdentifierDetails.identifiers:
            for identifier in self.identifiers:
                if identifier in line_identifiers.keys():
                    for i in range(len(line_identifiers[identifier])):
                        if identifier not in json_data.keys():
                            json_data[identifier] = {
                                1:  { 
                                    "line": line_identifiers["line"],
                                    "start_col": list(line_identifiers[identifier])[i],
                                    "end_col": list(line_identifiers[identifier])[i] + len(identifier) - 1
                                }
                            }
                        else:
                            count = len(json_data[identifier]) + 1
                            json_data[identifier][count] = {
                                "line": line_identifiers["line"],
                                "start_col": list(line_identifiers[identifier])[i],
                                "end_col": list(line_identifiers[identifier])[i] + len(identifier) - 1
                            }
                count = 0

        return json_data
    
splitted_code = code.split("\n")
identifier_details = ClassIdentifierDetails(splitted_code, extracted_identifiers)
#res = variable_details.add()
json_details = identifier_details.get_detail()

print(ClassIdentifierDetails.identifiers)
print("\n")
print(json.dumps(json_details, indent = 4))