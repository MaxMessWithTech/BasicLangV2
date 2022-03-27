from utils import decInterp, mathHandler, blcolors


class Print:
    def __init__(self, line) -> None:
        self.line = line
        self.fixLine = self.removeDeclaration(self.fixLine(line))

    # This is called during runtime
    def run(self, varAddCallback, varGetCallback, funcCallback):
        editLine, dataTypes, valid = decInterp.decInterp(self.fixLine, varGetCallback)

        # This removes ALL quotation marks,
        # if I eventually want to add support for \" then this will need to be changed
        print(editLine)

    @staticmethod
    def removeDeclaration(line):
        return line.replace('print(', "").replace(')', "")

    @staticmethod
    def fixLine(line):
        line = line.replace("\t", "")
        return line.replace("\n", "")
