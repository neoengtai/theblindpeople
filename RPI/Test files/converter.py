#Converts .json files to .csv files
#.json contains an array of a 4 value set

import json

filename = input("Enter filename: ")

f = open(filename+".json", "r")
xcel = open(filename+".csv", "w")

values = json.load(f)

xcel.write("Time,x,y,z\n")

for val in values:
	xcel.write("%.6f,%.8f,%.8f,%.8f\n" % (val[0],val[1],val[2],val[3]))
	# xcel.write("%.8f,%.8f,%.8f\n" % (val[0],val[1],val[2]))

f.close()
xcel.close()