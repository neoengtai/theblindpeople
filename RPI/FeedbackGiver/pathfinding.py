import math
from . import calculateAngle

def pathfinding (path, northAt, currX, currY, heading):	
	shortestDistance = None;
	
	for node in path:
		separation = math.hypot((node['x']- currX),(node['y'] - currY))
		if (shortestDistance is None):
			shortestDistance = separation
			tempNode = node
		else:
			if (separation <= shortestDistance):
				shortestDistance = separation
				tempNode = node
	
	print ("To node: ", tempNode["nodeId"])
	angle = calculateAngle(currX, currY, tempNode['x'], tempNode['y'], northAt)

	difference = angle - heading
	
	if difference > 180:
		difference -= 360
	elif difference < -180:
		difference += 360
	
	return (shortestDistance, difference)