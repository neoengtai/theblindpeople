import FeedbackGiver as fg
import time

myFG = fg.FeedbackGiver()

#test case for distance feedback 
num = 98
myFG.audioFeedback(myFG.dataToString(1,num))
time.sleep(1)
#test case for direction feedback 
myFG.audioFeedback(myFG.dataToString(0,25))
time.sleep(1)
myFG.audioFeedback(myFG.dataToString(0,60))
time.sleep(1)
myFG.audioFeedback(myFG.dataToString(0,-25))
time.sleep(1)
myFG.audioFeedback(myFG.dataToString(0,-60))
time.sleep(1)
myFG.audioFeedback(myFG.dataToString(0,0))
time.sleep(1)
myFG.audioFeedback("enter starting and ending location")
