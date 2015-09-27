import MapManager as mm
import dijkstra
import pathfinding as pf

#CHANGE THE VALUE HERE FOR TYPE1 OR TYPE2 TEST
TEST_TYPE = 2

myMM = mm.MapManager()

places = {"Source": None, "Destination": None}

for k,v in places.items():
	while v is None:
		building = input (k + " building: ")
		level = input (k + " level: ")
		
		if not level.isdigit():
			print ("Please enter a valid number")
			continue
			
		if myMM.get_map(building, level) is None:
			print ("Cannot find map!")
			continue
			
		nodeId = input(k + " nodeId: ")
		if myMM.get_node(building,level,nodeId) is None:
			print ("Invalid node!")
			continue
		else:
			v = (building, level, nodeId)
			places.update({k : v})
			
building = places["Source"][0]
level = places["Source"][1]
srcNode = places["Source"][2]
destNode = places["Destination"][2]

adj_list = myMM.generate_adj_list(building,level)
if bool(adj_list):
	shortest_path = dijkstra.dijkstra(adj_list, srcNode, destNode)
	print (shortest_path)

	#Only for the prototype testing
	if TEST_TYPE == 2:
		nodes = []
		northAt = int(myMM.get_map(building, level)["info"]["northAt"])

		#Get details of all nodes in the path
		for node in shortest_path:
			nodes.append(myMM.get_node(building, level, node))

		while (1):
			currX = int(input("Current X: "))
			currY = int(input("Current Y: "))
			heading = int(input("Heading: "))
			
			rv = pf.pathfinding(nodes, northAt, currX, currY, heading)
			
			print ("Direction: (%.1f, %.1f)" %  (rv[1], rv[0]))
else:
	print("No path found.")