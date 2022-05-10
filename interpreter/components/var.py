from interpreter.utils.decInterp import decInterp


class Var:
    def __init__(self, line, headless=False, sendCommandCallback=None):
        self.line = line
        self.name = ""
        self.value = ""
        self.sendCommandCallback = sendCommandCallback
    
    def run(self, varAddCallback, varGetCallback, funcCallback):
        self.name = self.line[:self.line.index("=")].replace(" ", "")
        self.value = decInterp(self.line[self.line.index("=") + 1:], varGetCallback, self.sendError)[0]
        varAddCallback(self)

    def sendError(self, msg):
        if self.sendCommandCallback:
            self.sendCommandCallback("error", msg)
        else:
            print(msg)
