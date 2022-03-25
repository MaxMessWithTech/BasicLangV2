from posixpath import split
from utils.splitByOpp import splitByOpp
from utils.removeSpacesNotInStr import removeSpacesNotInStr

# Finding Var references and replaces them with their value in the line
def figureOutVars(line, getVars) -> str:
    """
    vars = getVars()
    for var in vars:
        if var.name in line:
            print(f"Found {var.name} in {line}")"""
    
    vars = getVars()
    splitLine = splitByOpp(line)
    for x in range(len(splitLine)):
        if splitLine[x].find('"') != -1:
            splitLine[x] = removeSpacesNotInStr(splitLine[x])
        else:
            # THIS IS SUPER INEFFICIENT - IF THINGS ARE SLOW, THIS IS PROBABLY A PROBLEM
            for var in vars:
                if var.name == splitLine[x]:
                    splitLine[x] = var.value
    
    # Rebuild string
    # THIS IS ALSO NOT GREAT, OH WELL
    output = ""
    for line in splitLine:
        output = output + line
    return output
