import urllib.request, urllib.parse, json, math

class MapManager:
	def __init__(self):
		self.maps = {}

	def parse_map (self, raw_map):
		decoded = json.loads(raw_map.read().decode("utf-8"))
		
		#Change all strings to integer, split linkTo into list
		nodes = decoded['map']
		for node in nodes:
			node['x'] = int(node['x'])
			node['y'] = int(node['y'])
			node['linkTo'] = [id.strip() for id in node['linkTo'].split(',')]
		
		return decoded

	def generate_adj_list(self, building, level):
		adj_list = {}

		if (building in self.maps and level in self.maps[building]):
			map_ = self.maps[building][level]["map"]

			for node in map_:
				costs = {}
				for linkTo_id in node['linkTo']:
					adj_node = self.get_node(building, level, linkTo_id)
					if adj_node:
						diffX = node['x'] - adj_node['x']
						diffY = node['y'] - adj_node['y']
						costs.update({linkTo_id : math.hypot(diffX, diffY)})
				adj_list.update({node['nodeId'] : costs})
		
		return adj_list

	def get_node (self, building, level, nodeId):
		if (building in self.maps and level in self.maps[building]):
			map_ = self.maps[building][level]["map"]
			for node in map_:
				if node["nodeId"] == nodeId:
					return node
		
		return None

	def get_map(self, building, level):
		ret = None
		if (building in self.maps and level in self.maps[building]):
			#If a map already exist, just retrieve
			ret = self.maps[building][level]
		else:
			#Download the map
			params = urllib.parse.urlencode({"Building" : building, "Level" : level})
			response = urllib.request.urlopen("http://showmyway.comp.nus.edu.sg/getMapInfo.php?%s" % params)
			map_ = self.parse_map(response)
			if map_['info'] is not None:
				#Insert map into the collection
				if building in self.maps:
					self.maps[building].update({level : map_})
				else:
					self.maps.update({building : {level : map_}})
				ret = map_

		return ret