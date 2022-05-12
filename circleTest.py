
def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


def midPointCircleDraw(x_center, y_center, r, img):
	x = r
	y = 0
	
	# Find the first points in the 4 cardinal directions, 
	# uses the radius to move over

	# (r + x_center, y_center)
	# (-r + x_center, y_center)
	# (x_center, r + y_center)
	# (x_center, -r + y_center)
	img.put("#ffffff", (r + x_center, y_center))
	img.put("#ffffff", (-r + x_center, y_center))
	img.put("#ffffff", (x_center, r + y_center))
	img.put("#ffffff", (x_center, -r + y_center))
	
	# Initializing the value of P
	P = 1 - r

	while x > y:
	
		y += 1
		
		# Mid-point inside or on the perimeter
		if P <= 0:
			P = P + 2 * y + 1
			
		# Mid-point outside the perimeter
		else:		
			x -= 1
			P = P + 2 * y - 2 * x + 1
		
		print(f"({x}, {y}) -> {P}")
		
		# All the perimeter points have
		# already been printed
		if (x < y):
			break
		
		# Printing the generated point its reflection
		# in the other octants after translation

		# (x + x_center, y + y_center)
		# (-x + x_center, y + y_center)
		# (x + x_center, -y + y_center)
		# (-x + x_center, -y + y_center)
		
		img.put(rgb_to_hex((255 - y*2, 0, 0)), (x + x_center, y + y_center))
		img.put(rgb_to_hex((255 - y*2, 0, 0)), (-x + x_center, y + y_center))
		img.put(rgb_to_hex((255 - y*2, 0, 0)), (x + x_center, -y + y_center))
		img.put(rgb_to_hex((255 - y*2, 0, 0)), (-x + x_center, -y + y_center))
		
		# If the generated point on the line x = y then
		# the perimeter points have already been printed
		if x != y:
			# (y + x_center, x + y_center)
			# (-y + x_center, x + y_center)
			# (y + x_center, -x + y_center)
			# (-y + x_center, -x + y_center)
			
			img.put(rgb_to_hex((0, 0, 255 - y*2)), (y + x_center, x + y_center))
			img.put(rgb_to_hex((0, 0, 255 - y*2)), (-y + x_center, x + y_center))
			img.put(rgb_to_hex((0, 0, 255 - y*2)), (y + x_center, -x + y_center))
			img.put(rgb_to_hex((0, 0, 255 - y*2)), (-y + x_center, -x + y_center))
		# break
							
# Driver Code
if __name__ == '__main__':
	from tkinter import Tk, Canvas, PhotoImage, mainloop
	from math import sin

	WIDTH, HEIGHT = 640, 480

	window = Tk()
	canvas = Canvas(window, width=WIDTH, height=HEIGHT, bg="#000000")
	canvas.pack()
	img = PhotoImage(width=WIDTH, height=HEIGHT)
	canvas.create_image((WIDTH/2, HEIGHT/2), image=img, state="normal")

	midPointCircleDraw(int(WIDTH/2), int(HEIGHT/2), 100, img)
	# midPointCircleDraw(int(WIDTH/2), int(HEIGHT/2), 100, img)
	window.mainloop()

