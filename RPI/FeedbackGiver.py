import math
import pygame

class FeedbackGiver():
	def __init__(self):
		pygame.mixer.init()
	
	def playSound(self, feedbackString):
		#convert to lowercase
		self.feedbackString = feedbackString.lower()
		
		#split the string and play the sound
		for sound in self.feedbackString.split(' '):
			pygame.mixer.music.load("./voice/" + sound + ".wav")
			pygame.mixer.music.play()
			while pygame.mixer.music.get_busy() == True:
				continue
	
	#Returns direction in degree
	def getDirection(self, currentX, currentY, nodeX, nodeY, northAt):
	
		#calculate distance
		diffX = nodeX - currentX
		diffY = nodeY - currentY
		
		angleRad = math.atan2(diffX, diffY)
		
		angleDeg = ((angleRad/math.pi) * 180)
		
		angleDegPositive = ((angleDeg + 360) %360)
		
		direction = (angleDegPositive - northAt + 360) % 360
		
		return direction
	
	def pathfinding (self, path, northAt, currX, currY, heading):	
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
		angle = self.getDirection(currX, currY, tempNode['x'], tempNode['y'], northAt)

		difference = angle - heading
		
		if difference > 180:
			difference -= 360
		elif difference < -180:
			difference += 360
		
		return (shortestDistance, difference)
