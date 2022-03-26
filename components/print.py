from utils import decInterp, mathHandler


class Print:
    def __init__(self, line) -> None:
        self.line = line
        self.fixLine = self.removeDeclaration(self.fixLine(line))

    # This is called during runtime
    def run(self, varAddCallback, varGetCallback, funcCallback):
        editLine, dataTypes, valid = decInterp.decInterp(self.fixLine, varGetCallback)


        mathHandler.stringToMath(editLine)

        if self.fixLine.count('"') == 2:
            print(self.convertString(self.fixLine))

    @staticmethod
    def convertString(line):
        return line.replace('"', "")

    @staticmethod
    def removeDeclaration(line):
        return line.replace('print(', "").replace(')', "")

    @staticmethod
    def fixLine(line):
        line = line.replace("\t", "")
        return line.replace("\n", "")
