def handleComment(line):
    # CHECK FOR COMMENT HERE
    if line.find("#") != -1:
        # If there is a commnet, remove the rest of the line from the compiler
        line = line[0:line.index("#")]
    return line