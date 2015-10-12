import sys, getopt

sys.path.append('.')
import RTIMU
import os.path
import time
import math
import StepDetector as sd

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

poll_interval = imu.IMUGetPollInterval()

# # Calibrating absolute magnitude of gravity
# input("Press enter to calibrate...")
# gravity = 1 	#dummy value
# s_time = time.time()
# magnitudeSum = 0
# count= 0
# while True:
# 	if imu.IMURead():
# 		count += 1
# 		accel = imu.getAccel()
# 		magnitudeSum += math.sqrt(accel[0]**2 + accel[1]**2 + accel[2]**2)
# 	if (time.time() - s_time	> 5):
# 		gravity = magnitudeSum / count
# 		break
# print("Average gravity magnitude = %f" % gravity)

##Tool to view sensor data
input ("Press enter to continue...")
count = 0
while True:
	if imu.IMURead():
		print (imu.getIMUData()['timestamp'])
		# data = imu.getIMUData()
		# r,p,y = data["fusionPose"][0],data["fusionPose"][1],data["fusionPose"][2]
		# x,y,z = data["accel"][0],data["accel"][1],data["accel"][2]
		# #compensate gravity
		# pureX = gravity*math.sin(p) + x
		# pureY = gravity*math.sin(r) - y
		# pureZ = gravity*math.cos(r)*math.cos(r) - z
		# print("PX:%.6f PY:%.6f PZ:%.6f " % (pureX,pureY,pureZ))

		# if count >= 125:
			# data = imu.getIMUData()
			# fusionPose = data["fusionPose"]
			# print("r: %5f p: %5f y: %5f" % (math.degrees(fusionPose[0]), 
			#         math.degrees(fusionPose[1]), math.degrees(fusionPose[2])))
			# print ("Gyro: %.5f %.5f %.5f" % imu.getGyro())
			#print ("Acc: %.5f %.5f %.5f" % imu.getAccel())
			# print ("Compass: %.5f %.5f %.5f" % imu.getCompass())
	# 		count = 0
	# count+=1
	#time.sleep(poll_interval*1.0/1000.0)