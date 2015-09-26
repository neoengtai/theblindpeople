import MapManager as mm
import dijkstra

myMM = mm.MapManager()

places = {"Source": None, "Destination": None}

for place in places:
	while places[place] is None:
		building = input (place + " building: ")
		level = input (place + " level: ")
		
		if not level.isdigit():
			print ("Please enter a valid number")
			continue
			
		if myMM.get_map(building, level) is None:
			print ("Cannot find map!")
			continue
			
		nodeId = input(place + " nodeId: ")
		if myMM.get_node(building,level,nodeId) is None:
			print ("Invalid node!")
			continue
		else:
			places.update({place : (building, level, nodeId)})
			
adj_list = myMM.generate_adj_list(places["Source"][0],places["Source"][1])
if bool(adj_list):
	shortest_path = dijkstra.dijkstra(adj_list, places["Source"][2], places["Destination"][2])
	print (shortest_path)