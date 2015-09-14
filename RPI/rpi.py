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
def get_graph (data):
	decoded = json.loads(data.read().decode("utf-8"))
	nodes = decoded['map']
	
	for node in nodes:
		node['x'] = int(node['x'])
		node['y'] = int(node['y'])
		node['nodeId'] = int(node['nodeId'])
		node['linkTo'] = [int(id) for id in node['linkTo'].split(', ')]
		
	return nodes

params = urllib.parse.urlencode({"Building" : "COM1", "Level" : 2})
response = urllib.request.urlopen("http://showmyway.comp.nus.edu.sg/getMapInfo.php?%s" % params)
graph = get_graph(response)
	
adj_list = generate_adj_list(graph)

shortest = dijkstra(adj_list, 2, 11)

print (shortest)