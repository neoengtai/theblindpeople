import serial
import time
import obstacleAvoid as oa

ACK = 0x05		#acknowledge 0xDB = 219
SYN = 0x16		#handshake start
SYNFIN = 0x02		#handshake end
MSGACK = 0x06		#acknowledge data sent 0xAB
RESET = 0x18		#reset handshake for arduino	

def readData(sp):
#return appended string	
#1st read num of devices
	concatData = ""
	numBytes = sp.readline()
	numBytes = str(numBytes,"UTF-8")
	for i in range(0,int(numBytes)):
		data = sp.readline()
		concatData += str(data,"UTF-8")
		#print ("device data:", data)
	sp.write(bytes(chr(MSGACK), "UTF-8"))
	return concatData
		
def sendHandshake(sp): 
	sp.write(bytes(chr(SYN),"UTF-8"))
	
	recv_data = sp.read()
	#print ("recv_data:",recv_data)

	if (ord(recv_data) == ACK):
		sp.write(bytes(chr(SYNFIN),"UTF-8"))
		sp.write(bytes(chr(RESET),"UTF-8"))
		time.sleep(1)
		return 1
	else:
		return 0	

def recvHandshake(sp):

	recv_data = sp.read()
	#print ("recv_data:",recv_data)
	if (ord(recv_data) == SYNFIN):
		print ("SYN successful")
		return 1
	else:
		print ("recvHandshake Fail")
		return 0	
				

def initPort():
	sp = serial.Serial("/dev/ttyAMA0",baudrate = 9600,timeout=None) #ZY rmb to change timeout for testing purposes. 
	return sp

def sendData(sp,data):	
	if(sendHandshake(sp) != 1):
		print ("Unable to initialize handshake")
		return 0
	else:
		sp.write(bytes(str(data),"UTF-8"))
		print ("Data: ",data)
		if (ord(sp.read()) == MSGACK):
			print ("MSGACK RECV")
		return 1

def recvData(sp):
	while 1:
		if(recvHandshake(sp) != 1):
			print ("Unable to init handshake")
		else:
			return readData(sp)

def testRecv():
	serialPort = initPort()
	dataXfer = 0
	while 1:
		recv_data= serialPort.read()
		if (ord(recv_data) != SYN):
			print ("NOT SYN")
		else:
			print ("IS SYN")
			serialPort.write(bytes(chr(ACK),"UTF-8"))
			dataXfer = recvHandshake(serialPort)
		if (dataXfer == 1):
			#print ("display data received:",readData(serialPort))
			devData = readData(serialPort)
			oa.obstacleAvoid(devData)
			dataXfer = 0	

def testSend():
	serialPort = initPort()
	while 1:
		if sendHandshake(serialPort) == 1:
			print("Handshake complete")
		#data = "hello\n" sendData(serialPort,data)		
testSend()
#testRecv()
