from utils.blcolors import blcolors


def stringToMath(string):
    printLn(string)

    # print(eval(string))


def printLn(text):
    print(
        f"{blcolors.MAGENTA}[{blcolors.BOLD}Math Handler{blcolors.CLEAR}{blcolors.MAGENTA}]" +
        f"{blcolors.MAGENTA}  {text}{blcolors.CLEAR}"
    )
