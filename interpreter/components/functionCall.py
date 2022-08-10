class FunctionCall:
    _declaration = "()"

    def __init__(self, line, usePackages=list, headless=False, sendCommandCallback=None):
        self.name = self.fixLine(line.replace("()", ""))
        self.sendCommandCallback = sendCommandCallback

    def run(self, varSetCallback, varGetCallback, funcCallback):
        funcCallback(self.name)
    

    @staticmethod
    def fixLine(line):
        line = line.replace("\t", "")
        return line.replace("\n", "")

    def sendError(self, msg):
        if self.sendCommandCallback:
            self.sendCommandCallback("error", msg)
        else:
            print(msg)

    @property
    def declaration(self):
        return "()"
