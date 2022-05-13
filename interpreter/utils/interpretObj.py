from interpreter.components.ELSE import Else
from interpreter.components.print import Print
from interpreter.components.delay import Delay
from interpreter.components.drawLine import DrawLine
from interpreter.components.drawCircle import DrawCircle
from interpreter.components.functionCall import FunctionCall
from interpreter.components.var import Var
from interpreter.components.IF import If
from interpreter.components.ELSEIF import ElseIf
from interpreter.utils.blcolors import blcolors

# This is a list, it does things, don't question it future Max
# "()" is for functions
typesOfObjects = ["print", "delay", "drawLine", "drawCircle", "else if", "if", "else", "()", "="]
objects = [Print, Delay, DrawLine, DrawCircle, ElseIf, If, Else, FunctionCall, Var]


# PURPOSE - This is gonna figure out which object should be created 
#           as I'm stupid and this is annoying
def interpretObj(line, errorCallback, headless=False, sendCommandCallback=None) -> any:
    """
    --Interpret Object--
    Inputs: line(str)
    Returns: object(any)

    Creates an object based on the declaration
    """

    obj = None
    for type in typesOfObjects:
        if type in line:
            try:
                obj = objects[typesOfObjects.index(type)](
                    line,
                    headless=headless, 
                    sendCommandCallback=sendCommandCallback
                )
                break
            except TypeError:
                errorCallback(
                    f"{blcolors.RED}{blcolors.BOLD}ERROR at interpretObj() [Creates Object From String]" +
                    f"{blcolors.CLEAR}{blcolors.RED} -> Object call of \"{line}\" isn't IMPLEMENTED!" +
                    blcolors.CLEAR)
                break

    if obj is None:
        errorCallback(
            f"{blcolors.RED}{blcolors.BOLD}ERROR at interpretObj() [Creates Object From String]" +
            f"{blcolors.CLEAR}{blcolors.RED} -> Object call of \"{line}\" is invalid and doesn't exist" +
            blcolors.CLEAR)
    return obj
