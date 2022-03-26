from utils import decInterp, mathHandler, blcolors, removeOpps


class Print:
    def __init__(self, line) -> None:
        self.line = line
        self.fixLine = self.removeDeclaration(self.fixLine(line))

    # This is called during runtime
    def run(self, varAddCallback, varGetCallback, funcCallback):
        editLine, dataTypes, valid = decInterp.decInterp(self.fixLine, varGetCallback)

        # If it's a number, send it to the math handler
        if valid and "numb" in dataTypes:
            print(mathHandler.stringToMath(editLine))
        # If it's a string, print the string
        elif valid and "str" in dataTypes:
            print(self.convertString(editLine))
        elif not valid:
            print(f"{blcolors.blcolors.MAGENTA}Couldn't Print: print({blcolors.blcolors.RED}{editLine}{blcolors.blcolors.MAGENTA})" +
                  f" because it contains an error.{blcolors.blcolors.CLEAR}")

    @staticmethod
    def convertString(line):
        return removeOpps.removeOpps(line.replace('"', ""))

    @staticmethod
    def removeDeclaration(line):
        return line.replace('print(', "").replace(')', "")

    @staticmethod
    def fixLine(line):
        line = line.replace("\t", "")
        return line.replace("\n", "")
