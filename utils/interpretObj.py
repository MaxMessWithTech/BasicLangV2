from components.print import Print
from components.functionCall import FunctionCall
from components.var import Var
from utils.blcolors import blcolors

# This is a list, it does things, don't question it future Max
# "()" is for functions
typesOfObjects = ["print", "delay", "if", "else", "if else", "()", "="]
objects = [Print, None, None, None, None, FunctionCall, Var]


# PURPOSE - This is gonna figure out which object should be created 
#           as I'm stupid and this is annoying
def interpretObj(line):
    obj = None
    for type in typesOfObjects:
        if type in line:
            try:
                obj = objects[typesOfObjects.index(type)](line)
            except TypeError:
                pass

    if obj is None:
        print(
            f"{blcolors.RED}{blcolors.BOLD}ERROR at interpretObj() [Creates Object From String]" +
            f"{blcolors.CLEAR}{blcolors.RED} -> Object call of \"{line}\" is invalid and doesn't exist" +
            blcolors.CLEAR)
    return obj