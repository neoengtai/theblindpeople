def dijkstra(graph,src,dest,visited=[],distances={},predecessors={}):
	# calculates shortest path tree that starts from src
	
	if src == dest:
		path=[]
		pred=dest
		while pred != None:
			path.append(pred)
			pred=predecessors.get(pred,None)
		return path
	else :     
		shortestPath = []
		# if it is the initial  run, initializes the cost
		if not visited: 
			distances[src]=0
        # visit the neighbours
		for neighbor in graph[src] :
			if neighbor not in visited:
				new_distance = distances[src] + graph[src][neighbor]
				if new_distance < distances.get(neighbor,float('inf')):
					distances[neighbor] = new_distance
					predecessors[neighbor] = src
        # mark as visited
		visited.append(src)
        # now that all neighbors have been visited: recurse                         
        # select the non visited node with lowest distance 'x'
        # run Dijskstra with src='x'
		unvisited={}
		for k in graph:
			if k not in visited:
				unvisited[k] = distances.get(k,float('inf'))        
		x=min(unvisited, key=unvisited.get)
		shortestPath = dijkstra(graph,x,dest,visited,distances,predecessors)
		return shortestPath