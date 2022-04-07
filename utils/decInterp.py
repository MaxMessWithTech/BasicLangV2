from typing import Tuple

from utils.blcolors import blcolors
from utils.splitByOpp import splitByOpp
from utils.removeSpacesNotInStr import removeSpacesNotInStr
from utils.operators import operatorList, conditionalOperators
from utils.mathHandler import stringToMath
from utils.trueFalse import trueFalse

DEBUG = False


def decInterp(line, getVars) -> Tuple[str, list, bool]:
    """
    --Declaration Interpreter--
    Inputs: line(str) - Current Value, getVars(def) - call back
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

        # Checks for a number
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

        # Check for a conditional operator
        elif splitLine[x] in conditionalOperators:
            dataTypes.append("conditional")

        # Check for an operator
        elif splitLine[x] in operatorList:
            # Nothing needs to be changed because of the way the splitByOpp function works

            # Check to make sure that if it's a string, it's using "+"
            if "str" in dataTypes and splitLine[x] != "+":
                valid = False

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

    # If it's a number, keep the operators
    if valid and "numb" in dataTypes:
        output = ""
        for line in splitLine:
            output = output + line

        output = stringToMath(output)
    # If it's an if statement, keep the operators
    elif valid and "conditional" in dataTypes:
        value = trueFalse(splitLine, getVars)
        if value is None:
            output = ""
            for line in splitLine:
                output = output + line
            print(
                f"{blcolors.RED}[{blcolors.BOLD}Conditional Interpreter{blcolors.CLEAR}{blcolors.RED}]" +
                f"{blcolors.RED}  INVALID IF STATEMENT: {repr(output)}{blcolors.CLEAR}"
            )
            output = str(False)
        else:
            output = str(value)
    # If it's a string, don't keep the operators
    else:
        output = ""
        for line in splitLine:
            if line not in operatorList:
                output = output + line
        # This removes ALL quotation marks,
        # if I eventually want to add support for \" then this will need to be changed
        output = output.replace('"', "")

    # Check to see if they are different types, if so throw an error
    if not valid:
        print(
            f"{blcolors.RED}[{blcolors.BOLD}Declaration Interpreter{blcolors.CLEAR}{blcolors.RED}]" +
            f"{blcolors.RED}  INVALID CONCATENATION OF DIFFERENT TYPES:  {output}{blcolors.CLEAR}"
        )

    return output, dataTypes, valid
