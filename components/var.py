from utils.declorationInterpreter import declorationInterpreter
from utils.splitByOpp import splitByOpp

class Var:
    def __init__(self, line):
        self.line = line
        self.name = ""
        self.value = ""
    
    def run(self, varAddCallback, varGetCallback, funcCallback):
        self.name = self.line[:self.line.index("=")].replace(" ", "")
        self.value = declorationInterpreter(self.line[self.line.index("=") + 1:], varGetCallback)
        varAddCallback(self)
