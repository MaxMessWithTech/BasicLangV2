import copy
from utils.blcolors import blcolors
from utils.figureOutMyShit import figureOutShit

class Function:
    def __init__(self, name):
        self.lines = list()
        self.name = name
        self.comp = list()

    # PURPOSE: Convert file lines to objects
    def compile(self):
        for line in self.lines:
            fixedLine = self.fixLine(line)
            indent = self.getIndent(line)
            self.printLn(f"Reading line: {fixedLine}, with an indent: {indent}.")
            # This finds the object, I was angry programing, don't question it
            self.comp.append(figureOutShit(fixedLine))

    # PURPOSE: Run Functions
    def run(self, varSetCallback, varGetCallback, funcCallback):
        for obj in self.comp:
            obj.run(varSetCallback, varGetCallback, funcCallback)

    @staticmethod
    def getIndent(line):
        return line.count("\t")

    @staticmethod
    def fixLine(line):
        line = line.replace("\t", "")
        return line.replace("\n", "")

    def addLine(self, line):
        self.lines.append(line)

    def printLn(self, text):
        print(
            f"{blcolors.BLUE}[{blcolors.BOLD}COMPILER at {blcolors.UNDERLINE}" + 
            f"FUNCTION ({self.name}){blcolors.CLEAR}{blcolors.BLUE}]" + 
            f"{blcolors.BLUE}  {text}{blcolors.CLEAR}"
        )
