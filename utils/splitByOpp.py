from utils.operators import operatorList
import re


# Splits the line-up into its individual values, so it can find the Vars
# Ex:   "Test Var: " + testVar + " " + testVar3 -> 
#       ['"TestVar:"', '+', 'testVar', '+', '" "', '+', 'testVar3']
def splitByOpp(line) -> list:
    """
    --Split By Operator--

    Splits the line-up into its individual values, so it can find the Vars
    Ex:     "Test Var: " + testVar + " " + testVar3 ->
            ['"TestVar:"', '+', 'testVar', '+', '" "', '+', 'testVar3']
    """

    allIndices = list()
    for opp in operatorList:
        res = [i for i in range(len(line)) if line.startswith(opp, i)]
        for index in res:
            allIndices.append({index, opp})

    out = list()
    lastIndex = -1
    for index, opp in allIndices:
        out.append(line[lastIndex + 1:index])
        out.append(line[index:index + len(opp)])
        lastIndex = index + len(opp) - 1
    # REPLACE HERE GETS RID OF ":"
    out.append(line[lastIndex + 1:].replace(":", ""))

    return out
