import sys, getopt

sys.path.append('.')
import RTIMU
import os.path
import time
import math
from stepDetection import countSteps

SETTINGS_FILE = "RTIMULib"

#projection of v1 onto v2
def projection (v1, v2):
	magnitudeV2 = math.sqrt(v2[0]**2 + v2[1]**2 + v2[2]**2)
	v1dotv2 = v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]
	
	return v1dotv2/ magnitudeV2

print("Using settings file " + SETTINGS_FILE + ".ini")
if not os.path.exists(SETTINGS_FILE + ".ini"):
  print("Settings file does not exist, will be created")

s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)
print("IMU Name: " + imu.IMUName())

if (not imu.IMUInit()):
    print("IMU Init Failed")
    sys.exit(1)
else:
    print("IMU Init Succeeded");
	
imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)

##Tool to view sensor data
while True:
	opt = int(input("Get (1:Gyro, 2:Acc, 3:Compass, 4:Quit): "))
	if opt == 4:
		break
	else:
		if imu.IMURead():
			data = imu.getIMUData()
			if opt == 1:
				print ("Gyro raw: %.5f %.5f %.5f" % imu.getGyro())
			elif opt == 2:
				print ("Acc raw: %.5f %.5f %.5f" % imu.getAccel())
			elif opt == 3:
				print ("Compass raw: %.5f %.5f %.5f" % imu.getCompass())
		else:
			print ("Read error!")
			
#Collecting acc data into file for graph plotting
# poll_interval = 0.01 #poll every 10ms
# count = 0
# xyzSum = [0,0,0]

#perform zeroing on acc by averaging 500 readings
# print ("Hold the IMU in a stable position...")
# while count < 500:
	# if imu.IMURead():
		# xyzSum[0] += imu.getAccel()[0]
		# xyzSum[1] += imu.getAccel()[1]
		# xyzSum[2] += imu.getAccel()[2]
		# count += 1
		#time.sleep(poll_interval)
		
# gravity = (xyzSum[0]/500, xyzSum[1]/500, xyzSum[2]/500)
# print ("Gravity :", gravity)

# input("Press enter to start...")

# try:
	# dataList = []
	# f = open('data.csv', 'w')
	# f.write("Value\r\n")
	# while True:
		# if imu.IMURead():
			# value = projection(imu.getAccel(), gravity)
			# dataList.append(value)
			# f.write("%f\r\n" % (value))
			
# except KeyboardInterrupt:
	# print ("Saving file...")
	# f.close()
	# print ("File saved...")
	# countSteps(dataList)