from interpreter.utils.decInterp import decInterp
from interpreter.utils.blcolors import blcolors


class Var:
    def __init__(self, line, headless=False, sendCommandCallback=None):
        self.line = line
        self.name = ""
        self.value = ""
        self.sendCommandCallback = sendCommandCallback
    
    def run(self, varAddCallback, varGetCallback, funcCallback):
        self.name = self.line.replace(" ", "")[:self.line.replace(" ", "").index("=")]
        rawVal = self.line.replace(" ", "")[self.line.replace(" ", "").index("=") + 1:]

        if "=" in rawVal:
            self.sendError(f"{blcolors.RED}[{blcolors.BOLD}Declaration Interpreter (Var){blcolors.CLEAR}{blcolors.RED}]" +
                f"{blcolors.RED}  INVALID VARIABLE DECLARATION: {repr(self.line)}{blcolors.CLEAR}")

        self.value = decInterp(rawVal, varGetCallback, self.sendError)[0][0]
        # print(f"name: {self.name}, value: {self.value}")
        varAddCallback(self)

    def setValue(self, rawVal, varGetCallback):
        self.value = decInterp(rawVal, varGetCallback, self.sendError)[0][0]

    def sendError(self, msg):
        if self.sendCommandCallback:
            self.sendCommandCallback("error", msg)
        else:
            print(msg)
    
    def sendError(self, msg):
        if self.sendCommandCallback:
            self.sendCommandCallback("error", msg)
        else:
            print(msg)

    def __repr__(self):
        return f"Var(name=\"{self.name}\", value=\"{self.value}\")"

    @property
    def declaration(self):
        return "="
