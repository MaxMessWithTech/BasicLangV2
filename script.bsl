func:
	print("Func")
	delay(1 )
	draw(0, 0, 100, 100, (255, 255, 255))

	if(testVar + " Miller" == "Max Miller" && testVar != "Max" || "test" == "test"):
		print("hello Max!!!!")
		if(testVar + " Miller" == "Max Miller" && true == false):
			print("TRUE")
		else:
			print("FALSE")
	else:
		print("Hello... " + testVar)
	
run:
	print("Run")
	testVar = "Max"
	# print(testVar + " Miller")
	func()