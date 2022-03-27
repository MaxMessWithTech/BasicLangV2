from utils.splitByOpp import operatorList


def removeOpps(line) -> str:
    """
    --Remove Operators--

    """

    for opp in operatorList:
        line.replace(opp, "")

    return line
