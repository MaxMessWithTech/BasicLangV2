from utils.operators import operatorList

def splitByOpp(line) -> list:
    out = list()
    lastIndex = 0
    for x in range(len(line)):
        if line[x] in operatorList:
            out.append(line[lastIndex:x])
            out.append(line[x])
            lastIndex = x
    return out
