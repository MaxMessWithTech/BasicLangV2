import copy
from components.function import Function
from utils.blcolors import blcolors
from utils.thereBeACommentInOurMidst import handleComment
from components.var import Var


class Code:
    def __init__(self, lines):
        self.lines = lines
        self.comp = list()
        self.runFuncComp = Function("run")
        self.vars = list()
    
    # PURPOSE: Convert file lines to objects
    def compile(self):
        self.compHeader()

        for lineIndex in range(len(self.lines)):
            self.lines[lineIndex] = handleComment(self.lines[lineIndex])
        self.lines = self.removeBlankLines(self.lines)

        curFunc = None
        for line in self.lines:
            indent = self.getIndent(line)
            fixedLine = self.fixLine(line)
            if indent == 0 and fixedLine.find(":") != -1:
                if curFunc:
                    self.comp.append(curFunc)
                name = fixedLine.replace(":", "")
                if name == "run":
                    curFunc = self.runFuncComp
                else:
                    curFunc = Function(name)
                # self.printLn("IT'S A FUNCTION!!")
            elif indent != 0:
                curFunc.addLine(line)
            self.printLn(f"Reading line: {self.fixLine(fixedLine)}, with an indent: {indent}.")
        self.comp.append(curFunc)

        for func in self.comp:
            func.compile()

    # PURPOSE: Run File
    def run(self):
        self.runHeader()
        self.runFuncComp.run(self.addVar, self.getVar, self.runFunc)
        self.runFooter()
            
    def addVar(self, var):
        self.vars.append(var)
    
    def getVar(self, varName=""):
        if varName != "":
            for var in self.vars:
                if var.name == varName:
                    return var
        return self.vars

    def runFunc(self, name):
        for func in self.comp:
            if func.name == name:
                func.run(self.addVar, self.getVar, self.runFunc)

    # !!USELESS!! Require tabs for input, instead of converting
    # PURPOSE: Convert 4 spaces tabs
    def tabConvert(self, _lines):
        lines = copy.deepcopy(_lines)
        for line in lines:
            while line.find("    ") != -1:
                line = repr(line).replace("    ", "\t")
        return lines

    @staticmethod
    def getIndent(line):
        return line.count("\t")
    
    @staticmethod
    def fixLine(line):
        line = line.replace("\t", "")
        return line.replace("\n", "")
    
    def removeBlankLines(self, _lines):
        lines = copy.copy(_lines)
        newLines = list()
        for line in lines:
            
            if self.fixLine(line) != "":
                newLines.append(line)
        return newLines

    @staticmethod
    def compHeader():
        print(f"-----------------------------")
        print(f"{blcolors.CYAN}{blcolors.BOLD}BASIC LANG{blcolors.CLEAR}")
        print("Created by: Max Miller")
        print(f"-----------------------------")

    @staticmethod
    def runHeader():
        print(f"\r\n{blcolors.GREEN}{blcolors.BOLD}------Running------{blcolors.CLEAR}\r\n")
    
    @staticmethod
    def runFooter():
        print(f"\r\n{blcolors.GREEN}{blcolors.BOLD}--------End--------{blcolors.CLEAR}")


    @staticmethod
    def printLn(text):
        print(
            f"{blcolors.BLUE}[{blcolors.BOLD}COMPILER at {blcolors.UNDERLINE}" + 
            f"BASE{blcolors.CLEAR}{blcolors.BLUE}]" + 
            f"{blcolors.BLUE}  {text}{blcolors.CLEAR}"
        )

"""
Compilation:
1) Read file
    a) line -> Obj
    b) Obj -> list of Obj

** Problem VARS EXIST
** Problem If statements EXIST

Runtime:
1) Go through list of objs and call run, passing though all vars


DECLORATION STYLING!!!!!!!!!!

Functions:  "funcName:"
If:         "if (test == "hello"):"
Print       "print("hello world")"

"""