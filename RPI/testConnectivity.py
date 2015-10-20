import urllib.request
from socket import timeout

def testConnection():
	connectionFlag = 0
	try:
		urllib.request.urlopen("http://www.google.com", timeout = 3)
		connectFlag = 1
		print ("Got connection!")
	except urllib.error.URLError as e:
		print ("No Connection")
	except timeout:
		print("timeout!")
	
	return connectionFlag

testConnection()		
