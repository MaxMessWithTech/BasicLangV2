from utils.operators import conditionalOperators, equalityOperators

def trueFalse(splitLine) -> bool:
    print(splitLine)
    
    # Find opperators
    oppIndices = list()
    for x in range(len(splitLine)):
        if splitLine[x] in conditionalOperators:
            opp = conditionalOperators[conditionalOperators.index(splitLine[x])]
            oppIndices.append({'index': x, 'opp': opp})
    print(f"trueFalse: {oppIndices}")

    """
    print(f"trueFalse: {oppIndices}")
    newSplitLine = list()
    for x in range(1, len(oppIndices)):
        print(splitLine[oppIndices[x - 1]: oppIndices[x]])
        newSplitLine.append(splitLine[oppIndices[x - 1] + 1: oppIndices[x]])
        newSplitLine.append(splitLine[oppIndices[x]])
    """

    out = list()
    lastIndex = -1
    for indexDict in oppIndices:
        out.append(splitLine[lastIndex + 1:indexDict['index']])
        out.append(splitLine[indexDict['index']])
        # print(out)
        lastIndex = indexDict['index'] - 1
    # REPLACE HERE GETS RID OF ":"
    out.append(splitLine[lastIndex + 1:])

    print(f"trueFalse: {out}")
    

    return True
    
