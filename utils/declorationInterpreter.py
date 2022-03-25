from utils.blcolors import blcolors
from utils.splitByOpp import splitByOpp
from utils.removeSpacesNotInStr import removeSpacesNotInStr
from utils.operators import operatorList


# Decloration Interpreter
# Finding Var references and replaces them with their value in the line
def declorationInterpreter(line, getVars) -> str:    
    vars = getVars()
    splitLine = splitByOpp(line)
    for x in range(len(splitLine)):
        if splitLine[x].find('"') != -1:
            splitLine[x] = removeSpacesNotInStr(splitLine[x])
        elif splitLine[x].replace(" ", "").isnumeric():
            splitLine[x] = splitLine[x].replace(" ", "")
            print(
                f"{blcolors.MAGENTA}[{blcolors.BOLD}Decloration Interpreter{blcolors.CLEAR}{blcolors.MAGENTA}]" + 
                f"{blcolors.MAGENTA}  Number {repr(splitLine[x])} unhandled MAX FIX IT{blcolors.CLEAR}"
            )
        elif splitLine[x] not in operatorList:
            splitLine[x] = splitLine[x].replace(" ", "")
            # THIS IS SUPER INEFFICIENT - IF THINGS ARE SLOW, THIS IS PROBABLY A PROBLEM
            for var in vars:
                if var.name == splitLine[x]:
                    splitLine[x] = var.value
            else:
                # !!ERROR!! VAR DOESN'T EXIST
                print(
                    f"{blcolors.RED}[{blcolors.BOLD}Decloration Interpreter{blcolors.CLEAR}{blcolors.RED}]" + 
                    f"{blcolors.RED}  Var by name of {repr(splitLine[x])} doesn't exist!{blcolors.CLEAR}"
                )
    
    # Rebuild string
    # THIS IS ALSO NOT GREAT, OH WELL
    output = ""
    for line in splitLine:
        output = output + line
    return output
