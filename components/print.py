from utils import declorationInterpreter, mathHandler

class Print:
    def __init__(self, line) -> None:
        self.line = line
        self.fixLine = self.removeDecloration(self.fixLine(line))
    
    def run(self, varAddCallback, varGetCallback, funcCallback):
        declorationInterpreter.declorationInterpreter(self.fixLine, varGetCallback)
        mathHandler.stringToMath(self.fixLine)
        if self.fixLine.count('"') == 2:
            print(self.convertString(self.fixLine))

    @staticmethod
    def convertString(line):
        return line.replace('"', "")

    @staticmethod
    def removeDecloration(line):
        return line.replace('print(', "").replace(')', "")

    @staticmethod
    def fixLine(line):
        line = line.replace("\t", "")
        return line.replace("\n", "")
