import serial
import time

ACK = 0x05		#acknowledge 0xDB = 219
SYN = 0x16		#handshake start
SYNFIN = 0x02		#handshake end
MSGACK = 0x06		#acknowledge data sent 0xAB

sendDataFlag = 1	#flag for sending data

def readData(sp):
#return appended string	
#1st read num of devices
	concatData = ""
	numBytes = sp.readline()
	print "numBytes:",numBytes
	for i in range(0,int(numBytes)):
		data = sp.readline()
		concatData += (data + '\n')
		print "device data:", data
	sp.write(chr(MSGACK))
	return concatData
		
def sendHandshake(sp): 
	sp.write(chr(SYN))
	
	recv_data = sp.read()
	print "recv_data:",recv_data

	if (recv_data == chr(ACK)):
		sp.write(chr(SYNFIN))
    		return 1
	else:
		return 0	

def recvHandshake(sp):

	recv_data = sp.read()
	print "recv_data:",recv_data
	if (recv_data == chr(SYNFIN)):
		print "SYN successful"
		return 1
	else:
		print "recvHandshake Fail"
		return 0	
				

def initPort():
	sp = serial.Serial("/dev/ttyAMA0",baudrate = 9600,timeout=None) #ZY rmb to change timeout for testing purposes. 
	return sp

def sendData(sp,data):	
	if(sendHandshake(sp) != 1):
		print "Unable to initialize handshake"
		return 0
	else:
		sp.write(str(data))
		print "Data: ",data
		if (sp.read() == chr(MSGACK)):
			print "MSGACK RECV"
		return 1

def recvData(sp):
	while 1:
		if(recvHandshake(sp) != 1):
			print "Unable to init handshake"
		else:
			return readData(sp)

def testRecv():
	serialPort = initPort()
	dataXfer = 0
	while 1:
		recv_data= serialPort.read()
		if (recv_data != chr(SYN)):
			print "NOT SYN"
		else:
			print "IS SYN"
			serialPort.write(chr(ACK))
			dataXfer = recvHandshake(serialPort)
		if (dataXfer == 1):
			print "display data received:",readData(serialPort)
			dataXfer = 0	

def testSend():
	serialPort = initPort()
	while 1:
		
		data = "hello Asshole\n"
		sendData(serialPort,data)
		
testSend()
