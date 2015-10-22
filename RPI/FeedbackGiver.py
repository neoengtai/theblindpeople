import math
import pygame

class FeedbackGiver():

	def __init__(self):
		pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
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

			
