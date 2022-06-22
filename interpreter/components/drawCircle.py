from interpreter.utils import decInterp
from interpreter.utils.blcolors import blcolors


# draw(x1, y1, x2, y2, color)
# draw(0, 0, 100, 100, (255, 255, 255))
class DrawCircle:
	_decloration = "draw.drawCircle("

	def __init__(self, line, headless=False, sendCommandCallback=None) -> None:
		self.line = line
		self.fixedLine = self.removeDeclaration(self.fixLine(line))
		self.sendCommandCallback = sendCommandCallback
		self.x = 0
		self.y = 0
		self.r = 0
		self.color = (255, 255, 255)
		# self.setVars(self.fixedLine)

	# This is called during runtime
	def run(self, varAddCallback, varGetCallback, funcCallback):
		editLine, dataTypes, valid = decInterp.decInterp(self.fixedLine, varGetCallback, self.sendError, returnSplitLine=True)
		if self.setVars(editLine):
			# Check to see if we can even do anything
			if not self.sendCommandCallback:
				self.sendError(
					f"{blcolors.CYAN}[{blcolors.BOLD}Draw Circle{blcolors.CLEAR}{blcolors.CYAN}]" +
					f"{blcolors.CYAN}  Currently in terminal mode!{blcolors.CLEAR}"
				)
				return
			
			pointArray = self.createPointArray()
			# print(pointArray)
			# If this is in a production env, then send draw command
			self.sendCommandCallback("draw", {
				'cords': pointArray,
				'color': self.color
			})
	
	def createPointArray(self):
		out = list()
		if self.x < 0 or self.y < 0:
			self.sendError(
				f"{blcolors.RED}[{blcolors.BOLD}Draw Circle{blcolors.CLEAR}{blcolors.RED}]" +
				f"{blcolors.RED}  Invalid definition: {repr(self.fixedLine)}{blcolors.CLEAR}"
			)
			return out

		x = self.r
		y = 0
		x_center = self.x
		y_center = self.y
		
		# Find the first points in the 4 cardinal directions, 
		# uses the radius to move over

		# (r + x_center, y_center)
		# (-r + x_center, y_center)
		# (x_center, r + y_center)
		# (x_center, -r + y_center)
		out.append({'x': self.r + x_center, 'y': y_center})
		out.append({'x': -self.r + x_center, 'y': y_center})
		out.append({'x': x_center, 'y': self.r + y_center})
		out.append({'x': x_center, 'y': -self.r + y_center})
		
		# Initializing the value of P
		P = 1 - self.r

		while x > y:
		
			y += 1
			
			# Mid-point inside or on the perimeter
			if P <= 0:
				P = P + 2 * y + 1
				
			# Mid-point outside the perimeter
			else:		
				x -= 1
				P = P + 2 * y - 2 * x + 1
			
			# print(f"({x}, {y}) -> {P}")
			
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
			
			out.append({'x': x + x_center, 'y': y + y_center})
			out.append({'x': -x + x_center, 'y': y + y_center})
			out.append({'x': x + x_center, 'y': -y + y_center})
			out.append({'x': -x + x_center, 'y': -y + y_center})
			
			# If the generated point on the line x = y then
			# the perimeter points have already been printed
			if x != y:
				# (y + x_center, x + y_center)
				# (-y + x_center, x + y_center)
				# (y + x_center, -x + y_center)
				# (-y + x_center, -x + y_center)
				
				out.append({'x': y + x_center, 'y': x + y_center})
				out.append({'x': -y + x_center, 'y': x + y_center})
				out.append({'x': y + x_center, 'y': -x + y_center})
				out.append({'x': -y + x_center, 'y': -x + y_center})
		return out

	def removeDeclaration(self, line):
		# THIS IS GONNA BECOME A PROBLEM, 
		# BUT I DON'T WANNA ADDRESS IT EVERYWHERE (Even though it's broken everywhere)
		for x in range(len(line)):
			if line[::-1][x] == ")":
				break

		return line[:len(line)-x-1].replace(self._decloration, "")
	
	def setVars(self, split) -> bool:

		# Should Look like: 
		# ['', x, ',', y, ',', r, ',', '(', red, ',', green, ',', blue, ')']
		if len(split) == 4:
			self.x = int(split[0])
			self.y = int(split[1])
			self.r = int(split[2])
			self.color = {'r': int(split[3][0]), 'g': int(split[3][1]), 'b': int(split[3][2])}
			# print(f"({self.x1}, {self.y1}), ({self.x2}, {self.y2}) -> {self.color}")
		else:
			self.sendError(f"{blcolors.RED}[{blcolors.BOLD}Draw Circle{blcolors.CLEAR}{blcolors.RED}]" +
					f"{blcolors.RED}  INVALID DRAW NUMBER OF ARGUMENTS: {repr(self.fixedLine)}{blcolors.CLEAR}")

			return False

		return True

	@staticmethod
	def fixLine(line):
		line = line.replace("\t", "")
		return line.replace("\n", "")
	
	def sendError(self, msg):
		if self.sendCommandCallback:
			self.sendCommandCallback("error", msg)
		else:
			print(msg)
