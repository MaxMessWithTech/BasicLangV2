def midPoint(X1, Y1, X2, Y2, img):
	# calculate dx & dy
	dx = X2 - X1
	dy = Y2 - Y1
 
	# initial value of decision parameter d
	d = dy - (dx/2)
	x = X1
	y = Y1
 
	# Plot initial given point
	print(f"({x}, {y})")
	img.put("#ffffff", (x, y))

	while (x < X2):
		x = x + 1
		# E or East is chosen
		if(d < 0):
			d = d + dy
 
		# NE or North East is chosen
		else:
			d = d + (dy - dx)
			y = y + 1

		# Plot intermediate points
		print(f"({x}, {y})")
		img.put("#ffffff", (x, y))
	 
 
# Driver program
 
if __name__=='__main__':
	from tkinter import Tk, Canvas, PhotoImage, mainloop
	from math import sin

	WIDTH, HEIGHT = 640, 480

	window = Tk()
	canvas = Canvas(window, width=WIDTH, height=HEIGHT, bg="#000000")
	canvas.pack()
	img = PhotoImage(width=WIDTH, height=HEIGHT)
	canvas.create_image((WIDTH/2, HEIGHT/2), image=img, state="normal")

	X1 = 0
	Y1 = 0
	X2 = WIDTH
	Y2 = HEIGHT
	midPoint(X1, Y1, X2, Y2, img)
	window.mainloop()
