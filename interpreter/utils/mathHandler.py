from interpreter.utils.blcolors import blcolors


def stringToMath(string):
    try:
        return eval(string)
    except:
        print(
            f"{blcolors.RED}[{blcolors.BOLD}Math Handler{blcolors.CLEAR}{blcolors.RED}]" +
            f"{blcolors.RED}  INCORRECTLY IDENTIFIED {repr(string)} AS MATHEMATICAL{blcolors.CLEAR}"
        )
        return f"{blcolors.RED}[{blcolors.BOLD}Declaration Interpreter{blcolors.CLEAR}{blcolors.RED}]{blcolors.CLEAR}"


def printLn(text):
    print(
        f"{blcolors.MAGENTA}[{blcolors.BOLD}Math Handler{blcolors.CLEAR}{blcolors.MAGENTA}]" +
        f"{blcolors.MAGENTA}  {text}{blcolors.CLEAR}"
    )
