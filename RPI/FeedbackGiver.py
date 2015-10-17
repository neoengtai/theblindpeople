import math
import pygame

class FeedbackGiver():

	def __init__(self):
		pygame.mixer.init()
	
	def audioFeedback(self,feedbackString):
		#feedbackString = feedbackString.lower()

		#split the string and play the sound
		for sound in feedbackString.split(' '):
			if sound.isdigit() == True:
				sound = ' '.join(list(sound))
				for number in sound.split(' '):
					self.playAudio(number)
			else:
				self.playAudio(sound)
	
	def playAudio(self, sound):
		pygame.mixer.music.load("/home/pi/theblindpeople/RPI/voice/" + sound + ".wav")
		pygame.mixer.music.play()
		while pygame.mixer.music.get_busy() == True:
			continue
	
	#Returns direction in degree
	def getAngle(self, currentX, currentY, nodeX, nodeY, northAt):
	
		#calculate distance
		diffX = nodeX - currentX
		diffY = nodeY - currentY
		
		angleRad = math.atan2(diffX, diffY)
		
		angleDeg = ((angleRad/math.pi) * 180)
		
		angleDegPositive = ((angleDeg + 360) %360)
		
		angleResult = (angleDegPositive - northAt + 360) % 360
		
		return angleResult
	
	def getDirection (self, path, northAt, currX, currY, heading):	
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
		
		#print ("To node: ", tempNode["nodeId"])
		angle = self.getAngle(currX, currY, tempNode['x'], tempNode['y'], northAt)

		#difference = angle - ((heading + 360) %360)
		difference = angle - heading
		if difference > 180:
			difference -= 360 	#left
		elif difference < -180:
			difference += 360	#right
		
		feedbackString = self.dataToString(0,difference)
		#feedbackString = feedbackString + " " + str(int(shortestDistance)) + " meters"
		self.audioFeedback(feedbackString)
		return shortestDistance
		
	# Convert data to string format for audio feedback
	# function 0 : direction
	def dataToString(self,function, data):
		result = [] 
		if function == 0:
			if data in range(-20,20):
				return "continue straight"
			elif data in range(20,65):
				return "turn slight right"
			elif data in range(65,180):
				return "turn right"
			elif data in range(-65,-20):
				return "turn slight left"
			elif data in range(-180,-65):
				return "turn left"
