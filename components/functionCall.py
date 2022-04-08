class FunctionCall:
    def __init__(self, line, headless=False, sendCommandCallback=None):
        self.name = self.fixLine(line.replace("()", ""))
        self.sendCommandCallback = sendCommandCallback

    def run(self, varSetCallback, varGetCallback, funcCallback):
        funcCallback(self.name)
    

    @staticmethod
    def fixLine(line):
        line = line.replace("\t", "")
        return line.replace("\n", "")
