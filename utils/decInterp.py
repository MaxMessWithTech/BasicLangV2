from utils.blcolors import blcolors
from utils.splitByOpp import splitByOpp
from utils.removeSpacesNotInStr import removeSpacesNotInStr
from utils.operators import operatorList

DEBUG = False


def decInterp(line, getVars) -> str:
    """
    --Declaration Interpreter--

    Finding Var references and replaces them with their value in the line
    """

    varList = getVars()
    splitLine = splitByOpp(line)

    for x in range(len(splitLine)):
        # Checks for a string
        if splitLine[x].find('"') != -1:
            splitLine[x] = removeSpacesNotInStr(splitLine[x])

        # Checks for a number
        elif splitLine[x].replace(" ", "").isnumeric():
            splitLine[x] = splitLine[x].replace(" ", "")

        # Checks for a var
        elif splitLine[x] not in operatorList:
            splitLine[x] = splitLine[x].replace(" ", "")
            # THIS IS SUPER INEFFICIENT - IF THINGS ARE SLOW, THIS IS PROBABLY A PROBLEM
            for var in varList:
                if var.name == splitLine[x]:
                    splitLine[x] = var.value
                    break
            else:
                # !!ERROR!! VAR DOESN'T EXIST
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
    if DEBUG:
        print(
            f"{blcolors.MAGENTA}[{blcolors.BOLD}Declaration Interpreter{blcolors.CLEAR}{blcolors.MAGENTA}]" +
            f"{blcolors.MAGENTA}  Returning output: {output}{blcolors.CLEAR}"
        )
    return output
