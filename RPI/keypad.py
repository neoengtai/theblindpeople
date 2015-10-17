#+------------+----+----+----+----+----+----+----+
#| KEYPAD PIN | D  | E  | F  | G  | H  | J  | K  |
#+------------+----+----+----+----+----+----+----+
#| GPIO PIN   | 22 | 27 | 17 | 18 | 25 | 24 | 23 |
#+------------+----+----+----+----+----+----+----+

# External module imports
import RPi.GPIO as GPIO
import time
 
class keypad():
	# CONSTANTS   
	KEYPAD = [
	[1,2,3],
	[4,5,6],
	[7,8,9],
	["*",0,"#"]
	]

	#GPIO pin
	ROW         = [23,24,25,18]	#Keypad rows pin: K,J,H,G
	COLUMN      = [17,27,22]	#Keypad cols pin: F,E,D

	def __init__(self):
		GPIO.setmode(GPIO.BCM)

	def getKey(self):

		# Set all columns as output low
		for j in range(len(self.COLUMN)):
			GPIO.setup(self.COLUMN[j], GPIO.OUT)
			GPIO.output(self.COLUMN[j], GPIO.LOW)

		# Set all rows as input
		for i in range(len(self.ROW)):
			GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)

		# Scan rows for pushed key/button
		# A valid key press should set "rowVal"  between 0 and 3.
		rowVal = -1
		for i in range(len(self.ROW)):
			tmpRead = GPIO.input(self.ROW[i])
			if tmpRead == 0:
				rowVal = i

		# if rowVal is not 0 thru 3 then no button was pressed and we can exit
		if rowVal <0 or rowVal>3:
			self.exit()
			return

		# Convert columns to input
		for j in range(len(self.COLUMN)):
			GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

		# Switch the i-th row found from scan to output
		GPIO.setup(self.ROW[rowVal], GPIO.OUT)
		GPIO.output(self.ROW[rowVal], GPIO.HIGH)
 
		# Scan columns for still-pushed key/button
		# A valid key press should set "colVal"  between 0 and 2.
		colVal = -1
		for j in range(len(self.COLUMN)):
			tmpRead = GPIO.input(self.COLUMN[j])
			if tmpRead == 1:
				colVal=j

		# if colVal is not 0 thru 2 then no button was pressed and we can exit
		if colVal<0 or colVal>2:
			self.exit()
			return
 	
		# Return the value of the key pressed
		self.exit()
		return self.KEYPAD[rowVal][colVal]

	def exit(self):
		# Reinitialize all rows and columns as input at exit
		for i in range(len(self.ROW)):
			GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
		for j in range(len(self.COLUMN)):
			GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)
   
	#return user input after '#' is being pressed
	def getUserInput(self):	     
		# Loop while waiting for a keypress
		digit = None
		input = ""
		
		while 1:
			digit = self.getKey()
			if digit is "#":
				return input
			elif digit is not None:
				input += str(digit)
				time.sleep(1)
			
