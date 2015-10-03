import math

def calculateStepDistance(averagePacing, headingMoved, northAt):

	#averagePacing is distance per step
	xTravel = 0
	yTravel = 0
	
	for heading in headingMoved:
		if heading < 0:
			heading = heading + 360
		headingInMap =((northAt + heading) % 360)
		distX = math.sin(math.radians(headingInMap)) * averagePacing
		distY = math.cos(math.radians(headingInMap)) * averagePacing
		xTravel = xTravel + distX
		yTravel = yTravel + distY
	
	#print("xTravel", xTravel)
	#print("yTravel", yTravel)
	
	return xTravel, yTravel
#this is a test
#calculateStepDistance(50,[90,0,90,0,180,270],0)