import math
from calculateAngle import calculateAngle

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
	
	angle = calculateAngle(currX, currY, tempNode['x'], tempNode['y'], northAt)
	
	angle = angle - heading
	
	if angle > 180:
		angle = angle - 360
	
	return (shortestDistance, angle)