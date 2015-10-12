import pygame

class audioFeedback:
 
	def __init__(self):
        	pygame.mixer.init()
        		
	def playSound(self,feedbackString):
		#convert to lowercase
		self.feedbackString = feedbackString.lower()
		
		#split the string and play the sound
		for sound in self.feedbackString.split(' '):
			pygame.mixer.music.load("../voice/" + sound + ".wav")
			pygame.mixer.music.play()
			while pygame.mixer.music.get_busy() == True:
				continue
