import imp
from interpreter.utils import decInterp
from time import sleep
from interpreter.utils.blcolors import blcolors

class Delay:
    def __init__(self, line, headless=False, sendCommandCallback=None) -> None:
        self.line = line
        self.fixedLine = self.removeDeclaration(self.fixLine(line))
        self.sendCommandCallback = sendCommandCallback

    # This is called during runtime
    def run(self, varAddCallback, varGetCallback, funcCallback):
        editLine, dataTypes, valid = decInterp.decInterp(self.fixedLine, varGetCallback, self.sendError)
        # print(f"Delay -> dataTypes: {dataTypes}")

        if len(dataTypes) != 1 or dataTypes[0] != "numb":
            self.sendError(
                f"{blcolors.RED}[{blcolors.BOLD}delay{blcolors.CLEAR}{blcolors.RED}]" +
                f"{blcolors.RED}  INVALID TYPE WITH VALUE OF {self.fixedLine}, MUST BE AN INTEGER FOR DELAY{blcolors.CLEAR}"
            )
            return

        # This removes ALL quotation marks,
        # if I eventually want to add support for \" then this will need to be changed
        if self.sendCommandCallback:
            self.sendCommandCallback("delay", editLine)
        else:
            sleep(editLine)

    @staticmethod
    def removeDeclaration(line):
        return line.replace('delay(', "").replace(')', "")

    @staticmethod
    def fixLine(line):
        line = line.replace("\t", "")
        return line.replace("\n", "")
    
    def sendError(self, msg):
        if self.sendCommandCallback:
            self.sendCommandCallback("error", msg)
        else:
            print(msg)
