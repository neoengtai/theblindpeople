#+------------+----+----+----+----+----+----+----+
#| KEYPAD PIN | D  | E  | F  | G  | H  | J  | K  |
#+------------+----+----+----+----+----+----+----+
#| GPIO PIN   | 22 | 27 | 17 | 18 | 25 | 24 | 23 |
#+------------+----+----+----+----+----+----+----+

# External module imports
import RPi.GPIO as GPIO
import time

class Keypad:
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
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.OUT)
            GPIO.output(self.COLUMN[j], GPIO.LOW)
        for i in range(len(self.ROW)):
            GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def getKey(self):
        found = False
        row,column = None, None
        for j in range(len(self.COLUMN)):
            if not found:
                GPIO.output(self.COLUMN[j],GPIO.HIGH)
                for i in range(len(self.ROW)):
                    if GPIO.input(self.ROW[i]) == 1:
                        column = j
                        row = i
                        found = True
                        break
                GPIO.output(self.COLUMN[j],GPIO.LOW)

        if row is not None and column is not None:
            return self.KEYPAD[row][column]

    #return user input after '#' is being pressed      
    def getUserInput(self):	     
        # Loop while waiting for a keypress
        digit = None
        input = ""
        while 1:
            digit = self.getKey()
            if digit == "#":
                return input
            elif digit is not None:
                input += str(digit)
                time.sleep(1)

    def dummyGetKey(self):
        return input()

kp = Keypad()
while True:
    print (kp.getKey())
    time.sleep(0.05)