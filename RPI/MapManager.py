import urllib.request, urllib.parse, json, math

class MapManager:
	CACHE_DIR = "MapCache/"
	def __init__(self, mode):
		# mode -> 0: Offline, 1: Online
		self.mode = mode
		self.maps = {}

	def parse_map (self, raw_map):
		#Change all strings to integer, split linkTo into list
		nodes = raw_map['map']
		for node in nodes:
			node['x'] = int(node['x'])
			node['y'] = int(node['y'])
			node['linkTo'] = [id.strip() for id in node['linkTo'].split(',')]
		
		return raw_map

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
			rawMap = None

			if self.mode == "Online":
				#Download the map
				params = urllib.parse.urlencode({"Building" : building, "Level" : level})
				response = urllib.request.urlopen("http://showmyway.comp.nus.edu.sg/getMapInfo.php?%s" % params)
				rawMap = json.loads(response.read().decode("utf-8"))
			elif self.mode == "Offline":
				filename = "B"+str(building)+"L"+str(level)+".json"
				try:
					f = open(self.CACHE_DIR+filename, "r")
					rawMap = json.load(f)
					f.close()
				except IOError:
					pass

			if rawMap is not None:
				parsed = self.parse_map(rawMap)
				if parsed['info'] is not None:
					#Insert map into the collection
					if building in self.maps:
						self.maps[building].update({level : parsed})
					else:
						self.maps.update({building : {level : parsed}})
					ret = parsed
		return ret