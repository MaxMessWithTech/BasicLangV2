import imp
from interpreter.utils import decInterp
from time import sleep
from interpreter.utils.blcolors import blcolors


# draw(x1, y1, x2, y2, color)
# draw(0, 0, 100, 100, (255, 255, 255))
class DrawCircle:
    def __init__(self, line, headless=False, sendCommandCallback=None) -> None:
        self.line = line
        self.fixedLine = self.removeDeclaration(self.fixLine(line))
        self.sendCommandCallback = sendCommandCallback
        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0
        self.color = (255, 255, 255)
        # self.setVars(self.fixedLine)

    # This is called during runtime
    def run(self, varAddCallback, varGetCallback, funcCallback):
        editLine, dataTypes, valid = decInterp.decInterp(self.fixedLine, varGetCallback, self.sendError, returnSplitLine=True)
        if self.setVars(editLine):
            # Check to see if we can even do anything
            if not self.sendCommandCallback:
                self.sendError(
                    f"{blcolors.CYAN}[{blcolors.BOLD}Draw{blcolors.CLEAR}{blcolors.CYAN}]" +
                    f"{blcolors.CYAN}  Currently in terminal mode!{blcolors.CLEAR}"
                )
                return
            # If this is in a production env, then send draw command
            self.sendCommandCallback("draw", {
                'x1': self.x1,
                'y1': self.y1,
                'x2': self.x2,
                'y2': self.y2,
                'color': self.color
            })

    @staticmethod
    def removeDeclaration(line):
        # THIS IS GONNA BECOME A PROBLEM, 
        # BUT I DON'T WANNA ADDRESS IT EVERYWHERE (Even though it's broken everywhere)
        for x in range(len(line)):
            if line[::-1][x] == ")":
                break

        return line[:len(line)-x-1].replace('draw(', "")
    
    def setVars(self, line) -> bool:
        split = line.split("\r\n")

        # Should Look like: 
        # ['', x1, ',', y1, ',', x2, ',', y2, ',', '(', red, ',', green, ',', blue, ')']
        if len(split) == 16:
            self.x1 = int(split[1])
            self.y1 = int(split[3])
            self.x2 = int(split[5])
            self.y2 = int(split[7])
            self.color = (int(split[10]), int(split[12]), int(split[14]))
            # print(f"({self.x1}, {self.y1}), ({self.x2}, {self.y2}) -> {self.color}")
        else:
            self.sendError(f"{blcolors.RED}[{blcolors.BOLD}Draw{blcolors.CLEAR}{blcolors.RED}]" +
                    f"{blcolors.RED}  INVALID DRAW NUMBER OF ARGUMENTS: {repr(self.fixedLine)}{blcolors.CLEAR}")

            return False

        return True

    @staticmethod
    def fixLine(line):
        line = line.replace("\t", "")
        return line.replace("\n", "")
    
    def sendError(self, msg):
        if self.sendCommandCallback:
            self.sendCommandCallback("error", msg)
        else:
            print(msg)
