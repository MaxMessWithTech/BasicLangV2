import sys
from os.path import exists
from interpreter.utils.blcolors import blcolors
from interpreter import main

from tkinter import Tk, Canvas, PhotoImage, mainloop
from math import sin

WIDTH, HEIGHT = 640, 480

window = Tk()
canvas = Canvas(window, width=WIDTH, height=HEIGHT, bg="#000000")
canvas.pack()
img = PhotoImage(width=WIDTH, height=HEIGHT)
canvas.create_image((WIDTH/2, HEIGHT/2), image=img, state="normal")

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def testCallback(cmd, data, **kwargs):
    if cmd == "error" or cmd == "debug":
            print(f"{blcolors.YELLOW}[{cmd}]: {data}{blcolors.CLEAR}")
    elif cmd == "draw":
        for cord in data['cords']:
            # print(cord)
            img.put(
                rgb_to_hex((data['color']['r'], data['color']['g'], data['color']['b'])), 
                (cord['x'], cord['y'])
            )
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

        window.mainloop()
    else:
        print(f"{blcolors.RED}Invalid filename: {repr(fileName)}{blcolors.CLEAR}")

