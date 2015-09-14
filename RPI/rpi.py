import urllib.request, urllib.parse, json
import math
from dijkstra import dijkstra

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
		node['linkTo'] = node['linkTo'].split(', ')
	
	return decoded

maps = {}
places = {"Source": None, "Destination": None}

for place in places:
	while places[place] is None:
		map = None
		building = input (place + " building: ")
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

print (places)