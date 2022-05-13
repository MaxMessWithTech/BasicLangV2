def midPoint(X1, Y1, X2, Y2, img):
	# calculate dx & dy
	dx = X2 - X1
	dy = Y2 - Y1
 
	# initial value of decision parameter d
	d = dy - (dx/2)
	x = X1
	y = Y1

	if dy <= dx:
		d = dy - (dx/2)
		
		# plot initial given point
		img.put("#ffffff", (x, y))
		
		# iterate through value of X
		while(x < X2):
			x = x + 1

			# 'E' is chosen
			if d < 0:
				d = d + dy
			# 'NE' is chosen
			else:
				d = d + dy - dx
				y = y+1
			img.put("#ffffff", (x, y))

	elif dx <= dy:
		d = dx - (dy/2)
		
		# plot initial given point
		img.put("#ffffff", (x, y))
		
		# iterate through value of X
		while y < Y2:
			y= y + 1

			# 'E' is chosen
			if d < 0:
				d = d + dx
			# 'NE' is chosen
			else:
				d = d + dx - dy
				x= x+1
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

	midPoint(0, 0, 50, 100, img)
	midPoint(0, 0, 50, 50, img)
	window.mainloop()
