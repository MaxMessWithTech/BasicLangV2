from interpreter.utils import decInterp


class Print:
    def __init__(self, line, headless=False, sendCommandCallback=None) -> None:
        self.line = line
        self.fixedLine = self.removeDeclaration(self.fixLine(line))
        self.sendCommandCallback = sendCommandCallback

    # This is called during runtime
    def run(self, varAddCallback, varGetCallback, funcCallback):
        editLine, dataTypes, valid = decInterp.decInterp(self.fixedLine, varGetCallback, self.sendError)

        # This removes ALL quotation marks,
        # if I eventually want to add support for \" then this will need to be changed
        if self.sendCommandCallback:
            self.sendCommandCallback("log", editLine)
        else:
            print(editLine)

    @staticmethod
    def removeDeclaration(line):
        return line.replace('print(', "").replace(')', "")

    @staticmethod
    def fixLine(line):
        line = line.replace("\t", "")
        return line.replace("\n", "")

    def sendError(self, msg):
        if self.sendCommandCallback:
            self.sendCommandCallback("error", msg)
        else:
            print(msg)
