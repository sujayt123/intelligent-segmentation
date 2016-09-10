from DijkstraPriorityQueue import DijkstraPriorityQueue as dpq

def shortest_path(adj_list, source):
	"""
	Runs Dijkstra's algorithm on the graph represented by adj_list. 

	@param		adj_list	A dictionary mapping each node to a list of (neighbor, edge_weight)
	@param		source		the source node from which to begin our search
	@return		dist 		a dictionary mapping each node to its distance from "source"
	@return		p 			a "node to parent" mapping which can be traversed to yield the paths themselves
	"""
	dist = {}
	p = {}
	for node in adj_list:
		dist[node] = float("inf")
		p[node] = None
	dist[source] = 0

	priority_queue = dpq()
	priority_queue.build_heap([[v, k] for k, v in dist.items()])

	while len(priority_queue) > 0:
		curr = priority_queue.deleteMin()[1]
		for nbr, wt in adj_list[curr]:
			if wt + dist[curr] < dist[nbr]:
				dist[nbr] = wt + dist[curr]
				p[nbr] = curr
				priority_queue.update_priority(nbr, dist[nbr])
	return dist, p


def main():
	"""
	Executes the application.
	"""
	adj_list = {1: [(2, 15), (3, 1)],
				2: [(3, 7), (4, 1)],
				3: [(4, 19)],
				4: []}
	print shortest_path(adj_list, 1)
	

if __name__ == "__main__":
	main()