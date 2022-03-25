from components.code import Code


if __name__ == "__main__":
    file = open("./script.bsl", "r")
    codeObj = Code(file.readlines())
    codeObj.compile()
    codeObj.run()
