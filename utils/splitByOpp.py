from utils.operators import operatorList


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
    # line = line.replace(" ", "")
    out = list()
    lastIndex = -1
    for x in range(len(line)):
        if line[x] in operatorList:
            out.append(line[lastIndex + 1:x])
            out.append(line[x])
            lastIndex = x
    out.append(line[lastIndex + 1:])
    return out
