from utils.splitByOpp import splitByOpp

# Finding Var references and replaces them with their value in the line
def figureOutVars(line, getVars):
    """
    vars = getVars()
    for var in vars:
        if var.name in line:
            print(f"Found {var.name} in {line}")"""
    
    print(repr(line))
    print(re.split(operators, repr(line)))
    for seg in re.split(operators, repr(line)):
        print(seg)