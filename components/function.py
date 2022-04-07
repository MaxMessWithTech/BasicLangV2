import copy
from components.ELSE import Else
from utils.blcolors import blcolors
from utils.interpretObj import interpretObj


class Function:
    def __init__(self, name):
        self.lines = list()
        self.name = name
        self.comp = list()

    # PURPOSE: Convert file lines to objects
    def compile(self):
        parents = list()
        lastParent = None  # Keeps track of the last object to add to

        # Loop through all the lines and add to the right list or obj
        for line in self.lines:
            fixedLine = self.fixLine(line)
            indent = self.getIndent(line)
            self.printLn(f"Reading line: {fixedLine}, with an indent: {indent}.")

            if indent > 1:
                # SEND TO OBJECT
                try:
                    lastParent.addLine(line)
                    if lastParent not in parents:
                        parents.append(lastParent)
                except AttributeError:
                    print(
                        f"{blcolors.RED}[{blcolors.BOLD}COMPILER at {blcolors.UNDERLINE}" +
                        f"FUNCTION ({self.name}){blcolors.CLEAR}{blcolors.RED}]" +
                        f"{blcolors.RED}  INVALID INDENTION AT LINE {fixedLine}, WITH INDENT OF {indent}{blcolors.CLEAR}"
                    )
            else:
                obj = interpretObj(fixedLine)
                if obj:
                    # CASE FOR ELSE - Need to inherit value of the previous statement
                    if type(obj) == Else:
                        obj.setFixedLine(lastParent.line)
                    self.comp.append(obj)
                    lastParent = obj

        # Loop Through all the parents that were created
        for parent in parents:
            parent.compile()

    # PURPOSE: Run Functions
    def run(self, varAddCallback, varGetCallback, funcCallback):
        for obj in self.comp:
            obj.run(varAddCallback, varGetCallback, funcCallback)

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
