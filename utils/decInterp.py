from typing import Tuple

from utils.blcolors import blcolors
from utils.splitByOpp import splitByOpp
from utils.removeSpacesNotInStr import removeSpacesNotInStr
from utils.operators import operatorList

DEBUG = False


def decInterp(line, getVars) -> Tuple[str, list, bool]:
    """
    --Declaration Interpreter--
    Returns: Formatted Line(str), Data Type(list), valid(bool)

    Finding Var references and replaces them with their value in the line
    """

    # getVars gets a list with all the currently defined vars in runtime
    varList = getVars()
    splitLine = splitByOpp(line)
    dataTypes = list()  # Keeps track of the data types of every value
    valid = True  # Stays True until we find a var of a different type

    # ! CHECK FOR: str and int - EVENTUALLY: list, float, and bool
    for x in range(len(splitLine)):
        # Checks for a string
        if splitLine[x].find('"') != -1:
            if "str" not in dataTypes and len(dataTypes) != 0 and valid:
                valid = False
            dataTypes.append("str")

            splitLine[x] = removeSpacesNotInStr(splitLine[x])

        # Checks for a number CURRENTLY ASSUMES IT'S AN INT
        elif splitLine[x].replace(" ", "").isnumeric():
            if "numb" not in dataTypes and len(dataTypes) != 0 and valid:
                valid = False
            dataTypes.append("numb")

            splitLine[x] = splitLine[x].replace(" ", "")

        # Checks for a var
        elif splitLine[x] not in operatorList:

            splitLine[x] = splitLine[x].replace(" ", "")
            # THIS IS SUPER INEFFICIENT - IF THINGS ARE SLOW, THIS IS PROBABLY A PROBLEM
            for var in varList:
                if var.name == splitLine[x]:
                    splitLine[x] = var.value

                    # Since type() gives a weird string, this converts it
                    if type(var.value) is str:
                        varType = "str"
                    elif type(var.value) is int or type(var.value) is float:
                        varType = "numb"
                    else:
                        varType = None
                    if varType not in dataTypes and len(dataTypes) != 0 and valid:
                        valid = False
                    dataTypes.append(varType)
                    break
            else:
                # !!ERROR!! VAR DOESN'T EXIST
                valid = False
                dataTypes.append(None)

                print(
                    f"{blcolors.RED}[{blcolors.BOLD}Declaration Interpreter{blcolors.CLEAR}{blcolors.RED}]" +
                    f"{blcolors.RED}  Var by name of {repr(splitLine[x])} doesn't exist!{blcolors.CLEAR}"
                )
                splitLine[x] = f"{blcolors.RED}[{blcolors.BOLD}ERROR{blcolors.CLEAR}{blcolors.RED}]{blcolors.CLEAR}"

        # Check for an operator
        elif splitLine[x] in operatorList:
            # Nothing needs to be changed because of the way the splitByOpp function works
            pass

        else:
            # !!ERROR!! INVALID DATA TYPE
            print(
                f"{blcolors.RED}[{blcolors.BOLD}Declaration Interpreter{blcolors.CLEAR}{blcolors.RED}]" +
                f"{blcolors.RED}  INVALID DATA TYPE:  {repr(splitLine[x])}{blcolors.CLEAR}"
            )
            splitLine[x] = f"{blcolors.RED}[{blcolors.BOLD}ERROR{blcolors.CLEAR}{blcolors.RED}]{blcolors.CLEAR}"
    
    # Rebuild string
    # THIS IS ALSO NOT GREAT, OH WELL
    output = ""
    for line in splitLine:
        output = output + line

    # Check to see if they are different types, if so throw an error
    if not valid:
        print(
            f"{blcolors.RED}[{blcolors.BOLD}Declaration Interpreter{blcolors.CLEAR}{blcolors.RED}]" +
            f"{blcolors.RED}  INVALID CONCATENATION OF DIFFERENT TYPES:  {output}{blcolors.CLEAR}"
        )

    if DEBUG:
        print(
            f"{blcolors.MAGENTA}[{blcolors.BOLD}Declaration Interpreter{blcolors.CLEAR}{blcolors.MAGENTA}]" +
            f"{blcolors.MAGENTA}  Returning output: {output}{blcolors.CLEAR}"
        )
    return output, dataTypes, valid
