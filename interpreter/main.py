import sys
from os.path import exists
from interpreter.components.code import Code
from interpreter.utils.blcolors import blcolors


if __name__ == "__main__":
    if sys.argv[1] == "help":
        print(
            f"{blcolors.CYAN}\r\n----------------------\r\n{blcolors.BOLD}Basic Lang\r\n" +
            f"{blcolors.CLEAR}{blcolors.CYAN}Created by: Max Miller\r\n----------------------\r\n{blcolors.CLEAR}"
        )

    fileName = sys.argv[1]
    file_exists = exists(fileName)
    if file_exists:
        file = open(fileName, "r")
        if "headless" in sys.argv:
            codeObj = Code(file.readlines(), headless=True)
        else:
            codeObj = Code(file.readlines())
        codeObj.compile()
        codeObj.run()
    else:
        print(f"{blcolors.RED}Invalid filename: {repr(fileName)}{blcolors.CLEAR}")
else:
    def run(file, sendCommandCallback=None):
        codeObj = Code(file.readlines(), headless=True, sendCommandCallback=sendCommandCallback)
        codeObj.compile()
        codeObj.run()
