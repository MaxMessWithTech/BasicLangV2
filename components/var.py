from utils.decInterp import decInterp
from utils.splitByOpp import splitByOpp


class Var:
    def __init__(self, line, headless=False):
        self.line = line
        self.name = ""
        self.value = ""
    
    def run(self, varAddCallback, varGetCallback, funcCallback):
        self.name = self.line[:self.line.index("=")].replace(" ", "")
        self.value = decInterp(self.line[self.line.index("=") + 1:], varGetCallback)[0]
        varAddCallback(self)
