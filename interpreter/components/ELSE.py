from interpreter.utils.decInterp import decInterp
from interpreter.utils.blcolors import blcolors

class Else:
    def __init__(self, line, headless=False) -> None:
        self.line = line
        self.fixedLine = ""
        self.lines = list()
        self.comp = list()
        self.headless = headless

    def compile(self):
        from interpreter.utils.interpretObj import interpretObj

        parents = list()
        lastParent = None  # Keeps track of the last object to add to
        firstIndent = -1

        # Loop through all the lines and add to the right list or obj
        for line in self.lines:
            fixedLine = line.replace("\t", "").replace("\n", "")
            indent = self.getIndent(line)

            self.printLn(f"Reading line: {fixedLine}, with an indent: {indent}.")

            # If it's the first line we're reading, assume that this is the indent of the children
            if firstIndent == -1:
                firstIndent = indent

            if indent > firstIndent:
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
                obj = interpretObj(fixedLine, self.headless)
                if obj:
                    # CASE FOR ELSE - Need to inherit value of the previous statement
                    if type(obj) == Else:
                        obj.setFixedLine(lastParent.line)
                    self.comp.append(obj)
                    lastParent = obj

        # Loop Through all the parents that were created
        for parent in parents:
            parent.compile()

    # This is called during runtime
    def run(self, varAddCallback, varGetCallback, funcCallback):
        # CHECK IF TRUE
        # editLine should return either "True" or "False"
        
        editLine, dataTypes, valid = decInterp(self.fixedLine, varGetCallback)

        if editLine == "False":
            for obj in self.comp:
                obj.run(varAddCallback, varGetCallback, funcCallback)

    def setFixedLine(self, line):
        self.line = line
        self.fixedLine = self.removeDeclaration(self.fixLine(line))

    def addLine(self, line):
        self.lines.append(line)

    @staticmethod
    def getIndent(line):
        return line.count("\t")

    @staticmethod
    def removeDeclaration(line):
        return line.replace('if(', "").replace(')', "")

    @staticmethod
    def fixLine(line):
        line = line.replace("\t", "")
        return line.replace("\n", "")

    def printLn(self, text):
        if not self.headless:
            print(
                f"{blcolors.BLUE}[{blcolors.BOLD}COMPILER at {blcolors.UNDERLINE}" +
                f"ELSE STATEMENT ({self.fixedLine}){blcolors.CLEAR}{blcolors.BLUE}]" +
                f"{blcolors.BLUE}  {text}{blcolors.CLEAR}"
            )