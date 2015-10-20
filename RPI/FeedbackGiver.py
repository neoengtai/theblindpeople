import math
import pygame

class FeedbackGiver():

	def __init__(self):
		pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffersize=4096)
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
		pygame.mixer.music.set_volume(1)
		pygame.mixer.music.play()
		while pygame.mixer.music.get_busy() == True:
			continue
	
	#Returns direction in degree
	def getAngle(self, currentX, currentY, nodeX, nodeY, northAt):
	
		#calculate distance
		diffX = nodeX - currentX
		diffY = nodeY - currentY
		
		angleRad = math.atan2(diffX, diffY)
		
		angleDeg = math.degrees(angleRad)
		
		angleDegPositive = ((angleDeg + 360) %360)
		
		angleResult = (angleDegPositive - northAt + 360) % 360
		
		return angleResult
	
	def giveDirections (self, node, northAt, currX, currY, heading, pace): 
		separation = math.hypot((node['x']- currX),(node['y'] - currY))

		# print ("To node: ", tempNode["nodeId"])
		angle = self.getAngle(currX, currY, node['x'], node['y'], northAt)

		difference = angle - ((math.degrees(heading) + 360) %360)

		if difference > 180:
			difference -= 360 #left
		elif difference < -180:
			difference += 360 #right

		audioDir = self.dataToString(0,int(difference))
		audioDist = self.dataToString(1,int(separation/pace)) + " steps"

		self.audioFeedback(audioDir+' '+audioDist)
		
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
		elif function == 1:
			return ' '.join(list(str(data)))