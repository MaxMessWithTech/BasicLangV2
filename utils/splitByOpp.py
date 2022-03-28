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
            allIndices.append({'index': index, 'opp': opp})
    
    out = list()
    lastIndex = -1
    for indexDict in allIndices:
        out.append(line[lastIndex + 1:indexDict['index']])
        out.append(line[indexDict['index']:indexDict['index'] + len(indexDict['opp'])])
        # print(out)
        lastIndex = indexDict['index'] + len(indexDict['opp']) - 1
    # REPLACE HERE GETS RID OF ":"
    out.append(line[lastIndex + 1:].replace(":", ""))

    return out

