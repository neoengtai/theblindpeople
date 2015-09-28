import pygame
	
def audioFeedback(feedbackString):

	pygame.mixer.init()
	for sound in feedbackString:
		pygame.mixer.music.load(sound + ".wav")
		pygame.mixer.music.play()
		while pygame.mixer.music.get_busy() == True:
			continue
	
audioFeedback(("one", "two", "three", "centimeters"))