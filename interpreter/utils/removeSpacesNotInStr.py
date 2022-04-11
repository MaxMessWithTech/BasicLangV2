# Takes a line with spaces between operators and removes them
# while leaving the strings with spaces be
def removeSpacesNotInStr(line) -> str:
    strStart = line.index('"')
    strEnd = line.index('"', strStart + 1)
    # print(line[strStart:strEnd])
    return line[strStart:strEnd + 1]


"""
# DO NOT USE - DOES NOT WORK
def removeSpacesNotInStr(line) -> str:
    # Find strings so that we don't mess with them
    x = ""
    x.strip()
    lastEnd = 0
    while line.index('"', lastEnd) != -1:
        # Find a start and end of a string
        strStart = line.index('"', lastEnd)
        strEnd = line.index('"', strStart + 1)
        print(f"From {strStart} to {strEnd}")
        if lastEnd is strStart:
            break
        line[lastEnd:strStart].replace(" ", "")
        lastEnd = strEnd
        if lastEnd == len(line) -1:
            break
    print(f"Remove Spaces: {line}")
    return line
"""
