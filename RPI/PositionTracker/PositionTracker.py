from PositionTracker import StepCounter as sc

class PositionTracker:

	def __init__(self, x, y, avgPace):
		self.currentPositionX = x
		self.currentPositionY = y
		self.pace = avgPace
		self.steps = 0
	def setCurrentPosition(self, x ,y):
		self.currentPositionX = x
		self.currentPositionY = y
	
	def getCurrentPosition(self):
		return self.currentPositionX, self.currentPositionY
		
	def updatePosition(self, dataSet, northAt):
		headingMoved = sc.findSteps(dataSet)
		print("headings: ", headingMoved)
		self.steps += len(headingMoved)
		print("Num of steps: ",self.steps)
		xTravel, yTravel = sc.calculateStepDistance(self.pace, headingMoved, northAt)
		self.currentPositionX = self.currentPositionX + xTravel
		self.currentPositionY = self.currentPositionY + yTravel
