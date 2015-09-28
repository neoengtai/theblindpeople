import pygame
	
def audioFeedback(feedbackString):

	pygame.mixer.init()
	pygame.mixer.music.load(feedbackString + ".wav")
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy() == True:
		print("play music")
	
audioFeedback("testing")