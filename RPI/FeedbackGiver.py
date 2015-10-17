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
		
		print ("To node: ", tempNode["nodeId"])
		angle = self.getAngle(currX, currY, tempNode['x'], tempNode['y'], northAt)

		difference = angle - heading
		
		if difference > 180:
			difference -= 360 	#left
		elif difference < -180:
			difference += 360	#right
		
		audioDir = self.dataToString(0,difference)
		audioDist = str(shortestDistance) + "meters"
		self.audioFeedback((audioDist, audioDist))
		
	# Convert data to string format for audio feedback
	# function 0 : direction
	def dataToString(self,function, data):
		result = [] 
		if function == 0:
			if (data == 0):
				return "continue straight"
			if (data > 0 and data <= 45):
				return "turn slight right"
			elif (data > 0 and data > 45):
				return "turn right"
			elif (data < 0 and data >= -45):
				return "turn slight left"
			elif (data < 0 and data < -45):
				return "turn left"
