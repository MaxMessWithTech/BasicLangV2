import sys
from os.path import exists
from interpreter.utils.blcolors import blcolors
from interpreter import main

def testCallback(cmd, data, **kwargs):
    if cmd == "error" or cmd == "debug":
            print(f"{blcolors.YELLOW}[{cmd}]: {data}{blcolors.CLEAR}")
    else:
        print(f"{blcolors.YELLOW}{blcolors.BOLD}[Callback]{blcolors.CLEAR}" + 
            f"{blcolors.YELLOW} [{cmd}]: {repr(data)}{blcolors.CLEAR}")

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
        main.run(file, sendCommandCallback=testCallback)
    else:
        print(f"{blcolors.RED}Invalid filename: {repr(fileName)}{blcolors.CLEAR}")

