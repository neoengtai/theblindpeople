def routingInstructions(path, currentPosition, northAt):
	#Path contains the intermediate nodes that the user is currently travelling through
	
	distX = 0;
	distY = 0;
	reachedNode = 0; #1 means reached the node
	distToDest = 0
	mapAngleToDest = 0
	direction = 0

	#Orientation Variables
	rightToLeft = 0
	leftToRight = 0
	upToDown = 0
	downToUp = 0

	#Get the coordinates of the nodes in the path
	count = 0
	for value in path:
		if (count == 0):
			sourceX = value['x']
			sourceY = value['y']
			count = count + 1
		elif (count == 1):
			destX = value['x']
			destY = value['y']
			count = count + 1

	print ("sourceX:", sourceX, "\n")
	print ("destX:", destX, "\n")
	print ("sourceY:", sourceY, "\n")
	print ("destY:", destY, "\n")
	#Get general direction of travel
	#Horizontal
	if (sourceY == destY):
		if (sourceX > destX):
			rightToLeft = 1
			print ("Right to left!\n")
		elif (sourceX < destX):
			leftToRight = 1
			print ("Left to right!\n")
		elif (sourceX == destX):
			reachedNode = 1
			
	#Vertical
	elif (sourceX == destX):
		if (sourceY > destY):
			upToDown = 1
			print ("Up to down!\n")
		elif (sourceY < destY):
			downToUp = 1
			print ("Down to up!\n")
		elif (sourceY == destY):
			reachedNode = 1
			
	#Calculate distance and direction
	if (reachedNode == 1):
		print ("REACH LOH")
	#Case Travel from left to right
	elif (leftToRight == 1):
		if (currentPosition['y'] > destY):
			distX = destX - currentPosition['x']
			distY = currentPosition['y'] - destY
			distToDest = math.hypot(distX,distY)
			mapAngleToDest = 90 + math.atan2(distY, distX)
			print ("CurrY bigger than destY\n")
			print ("Distance:", distToDest, "\n")
			print ("MapAngle", mapAngleToDest, "\n")
		elif (currentPosition['y'] < destY):
			distX = destX - currentPosition['x']
			distY = destY - currentPosition['y']
			distToDest = math.hypot(distX,distY)
			mapAngleToDest = 90 - math.atan2(distY, distX)
			print ("CurrY smaller than destY\n")
			print ("Distance:", distToDest, "\n")
			print ("MapAngle", mapAngleToDest, "\n")
		elif (currentPosition ['y'] == destY):
			distX = destX - currentPosition['x']
			distY = 0
			distToDest = math.hypot(distX,distY)
			mapAngleToDest = 90
			print ("CurrY equal than destY\n")
			print ("Distance:", distToDest, "\n")
			print ("MapAngle", mapAngleToDest, "\n")
	#Case travel from right to left
	elif (rightToLeft == 1):
		if (currentPosition['y'] > destY):
			distX = currentPosition['x'] - destX
			distY = currentPosition['y'] - destY
			distToDest = math.hypot(distX,distY)
			mapAngleToDest = 270 - math.atan2(distY, distX)
			print ("CurrY bigger than destY\n")
			print ("Distance:", distToDest, "\n")
			print ("MapAngle", mapAngleToDest, "\n")
		elif (currentPosition['y'] < destY):
			distX = currentPosition['x'] - destX
			distY = destY - currentPosition['y']
			distToDest = math.hypot(distX,distY)
			mapAngleToDest = 270 + math.atan2(distY, distX)
			print ("CurrY smaller than destY\n")
			print ("Distance:", distToDest, "\n")
			print ("MapAngle", mapAngleToDest, "\n")
		elif (currentPosition ['y'] == destY):
			distX = currentPosition['x'] - destX
			distY = 0
			distToDest = math.hypot(distX,distY)
			mapAngleToDest = 270
			print ("CurrY equal than destY\n")
			print ("Distance:", distToDest, "\n")
			print ("MapAngle", mapAngleToDest, "\n")
	#Case travel from up to down
	elif (upToDown == 1):
		if (currentPosition['x'] > destX):
			distX = currentPosition['x'] - destX
			distY = currentPosition['y'] - destY
			distToDest = math.hypot(distX,distY)
			mapAngleToDest = 180 + math.atan2(distX, distY)
			print ("CurrX bigger than destX\n")
			print ("Distance:", distToDest, "\n")
			print ("MapAngle", mapAngleToDest, "\n")
		elif (currentPosition ['x'] < destX):
			distX = destX - currentPosition['x']
			distY = currentPosition['y'] - destY
			distToDest = math.hypot(distX,distY)
			mapAngleToDest = 180 - math.atan2(distX, distY)
			print ("CurrX smaller than destX\n")
			print ("Distance:", distToDest, "\n")
			print ("MapAngle", mapAngleToDest, "\n")
		elif (currentPosition ['x'] == destX):
			distX = 0
			distY = currentPosition['y'] - destY
			distToDest = math.hypot(distX,distY)
			mapAngleToDest = 180
			print ("CurrX equal than destX\n")
			print ("Distance:", distToDest, "\n")
			print ("MapAngle", mapAngleToDest, "\n")
	#Case travel from down to up
	elif (downToUp == 1):
		if (currentPosition['x'] > destX):
			distX = currentPosition['x'] - destX
			distY = destY - currentPosition['y']
			distToDest = math.hypot(distX,distY)
			mapAngleToDest = 360 - math.atan2(distX, distY)
			print ("CurrX bigger than destX\n")
			print ("Distance:", distToDest, "\n")
			print ("MapAngle", mapAngleToDest, "\n")
		elif (currentPosition ['x'] < destX):
			distX = destX - currentPosition['x']
			distY = destY - currentPosition['y']
			distToDest = math.hypot(distX,distY)
			mapAngleToDest = math.atan2(distX, distY)
			print ("CurrX smaller than destX\n")
			print ("Distance:", distToDest, "\n")
			print ("MapAngle", mapAngleToDest, "\n")
		elif (currentPosition ['x'] == destX):
			distX = 0
			distY = destY - currentPosition['y']
			distToDest = math.hypot(distX,distY)
			mapAngleToDest = 0
			print ("CurrX equal than destX\n")
			print ("Distance:", distToDest, "\n")
			print ("MapAngle", mapAngleToDest, "\n")
	#Get actual direction and compare it with compass to give direction
	direction = (360 - northAt + mapAngleToDest) % 360
	#run the compass function to find the direction user is facing
	
	
 
#For testing routingInstructions
import math
#Test left to right
"""
path = [ {'x': 5, 'y': 20}, {'x':25, 'y':20}]

#currY < destY
#currentPosition = { 'x':10, 'y': 5}

#currY > destY
#currentPosition = { 'x':10, 'y': 55}

#currY == destY
#currentPosition = { 'x':10, 'y': 20}
"""
#end test left to right

#Test Right to left
"""
path = [ {'x': 25, 'y': 20}, {'x':5, 'y':20}]

#currY < destY
#currentPosition = { 'x':10, 'y': 5}

#currY > destY
#currentPosition = { 'x':10, 'y': 55}

#currY == destY
#currentPosition = { 'x':10, 'y': 20}
"""
#end test right to left

#Test Up to down
"""
path = [ {'x': 20, 'y': 20}, {'x':20, 'y':5}]

#currX < destX
#currentPosition = { 'x':10, 'y': 10}

#currX > destX
#currentPosition = { 'x':55, 'y': 10}

#currX == destX
#currentPosition = { 'x':20, 'y': 10}
"""
#end test up to down

#Test down to up
"""
path = [ {'x': 20, 'y': 5}, {'x':20, 'y':20}]

#currX < destX
#currentPosition = { 'x':10, 'y': 10}

#currX > destX
#currentPosition = { 'x':55, 'y': 10}

#currX == destX
#currentPosition = { 'x':20, 'y': 10}
"""
#end test down to up

print ("calling route")
routingInstructions(path,currentPosition, 1)		
	