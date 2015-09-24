import urllib.request, urllib.parse, json
import math
from dijkstra import dijkstra
from pathfinding import pathfinding


# Pythagoras theorem		
def separation (v1, v2):
	return math.sqrt((v1['x'] - v2['x'])**2 + (v1['y'] - v2['y'])**2)
	
def generate_adj_list(graph):
	adj_list = {}
	
	for node in graph:
		costs = {}
		for linkTo_id in node['linkTo']:
			adj_node = get_node_by_id(graph,linkTo_id)
			if adj_node:
				costs.update({linkTo_id : separation(node, adj_node)})
		adj_list.update({node['nodeId'] : costs})
	
	return adj_list
		
def get_node_by_id (graph, id):
	for node in graph:
		if node['nodeId'] == id:
			return node
	return None

# Parse JSON 
def parse_map (raw_map):
	decoded = json.loads(raw_map.read().decode("utf-8"))
	
	#Change all strings to integer, split linkTo into list
	nodes = decoded['map']
	for node in nodes:
		node['x'] = int(node['x'])
		node['y'] = int(node['y'])
		node['linkTo'] = [id.strip() for id in node['linkTo'].split(',')]
	
	return decoded

maps = {}
places = {"Source": None, "Destination": None}

for place in places:
	while places[place] is None:
		map = None
		building = input (place + " building: ")
#Throws error if level is not number, because website does not return invalid json
		level = input (place + " level: ")
		
		if (building in maps and 
			level in maps[building]):
			#If a map already exist, just retrieve
			map = maps[building][level]
		else:
			#Download the map
			params = urllib.parse.urlencode({"Building" : building, "Level" : level})
			response = urllib.request.urlopen("http://showmyway.comp.nus.edu.sg/getMapInfo.php?%s" % params)

#TODO handle 404 errors
			map = parse_map(response)
			if map['info'] is None:
				print ("Invalid map!")
				continue
			else:
				#Insert map into the collection
				if building in maps:
					maps[building].update({level : map})
				else:
					maps.update({building : {level : map}})
		
		nodeId = input(place + " nodeId: ")
		#check if node exists
		node = get_node_by_id(map['map'], nodeId)
		if node is None:
			print ("Invalid node!")
			continue
		else:
			places.update({place : (building, level, nodeId)})

#Perform dijkstra
#Node details are in a tuple. i.e. {Source : (building, level, nodeId)}
shortest_path = None
src_building = places['Source'][0]
src_level = places['Source'][1]
src_nodeId = places['Source'][2]
dest_building = places['Destination'][0]
dest_level = places['Destination'][1]
dest_nodeId = places['Destination'][2]

#Same building, same level
if (src_building == dest_building and
	src_level == dest_level):
	
	adj_list = generate_adj_list(maps[src_building][src_level]['map'])
	shortest_path = dijkstra(adj_list, src_nodeId, dest_nodeId)
	
#Same building, different level (only up to 1 level difference)
elif (src_building == dest_building and 
		src_level != dest_level):
	print ("TODO")
	
#Different building, same level
elif (src_building != dest_building and 
		src_level == dest_level):
	print ("TODO")
	
#Different building, different level
else:
	print ("TODO")
		
print ("Shortest path: ", shortest_path)

#generate the list of nodes of the shortest path
nodes = []
for node in shortest_path:
	nodes.append(get_node_by_id(maps['COM1']['2']['map'], node))

while (1):
	currX = int(input("CurrX: "))
	currY = int(input("CurrY: "))
	heading = int(input("Heading: "))
	
	rv = pathfinding(nodes, int(maps['COM1']['2']['info']['northAt']), currX, currY, heading)
	
	print ("Dist: ", rv[0])
	print ("Turning angle: ", rv[1])