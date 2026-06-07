import heapq

class Greedy:
    def __init__(self, graph_obj):
        self.graph = graph_obj.get_graph()
        self.evaluated_nodes = 0
    
    def find_best_path(self, origin, destination, bst_high_risk, risk_threshold=8.0):
        """Finds the shortest path using a Greedy approach (Dijkstra's Algorithm)"""
        self.evaluated_nodes = 0

        high_risk_nodes = bst_high_risk.search_range(risk_threshold, 100.0)
        high_risk_ids = {node_data[0] for node_data in high_risk_nodes}

        accumulated_costs = {origin: 0.0}
        predecessors = {origin: None}

        priority_queue = [(0.0, origin)]
        visited = set()

        while priority_queue:
            current_cost, current_node = heapq.heappop(priority_queue)

            if current_cost > accumulated_costs.get(current_node, float('inf')):
                continue

            visited.add(current_node)
            self.evaluated_nodes += 1

            if current_node == destination:
                break
            
            neighbors = self.graph.get(current_node, [])

            for neighbor_id, edge_weight in neighbors:
                if neighbor_id not in visited:
                    adjusted_weight = edge_weight
                    if neighbor_id in high_risk_ids:
                        adjusted_weight = edge_weight * 0.5
                    
                    new_cost = current_cost + adjusted_weight
                    
                    if new_cost < accumulated_costs.get(neighbor_id, float('inf')):
                        accumulated_costs[neighbor_id] = new_cost
                        predecessors[neighbor_id] = current_node
                        heapq.heappush(priority_queue, (new_cost, neighbor_id))
        
        if destination not in accumulated_costs:
            return {
                "path": None,
                "cost": float('inf'),
                "evaluated_nodes": self.evaluated_nodes
            }
        
        path = []
        current = destination
        while current is not None:
            path.append(current)
            current = predecessors[current]
        path.reverse()

        return {
            "path": path,
            "cost": accumulated_costs[destination],
            "evaluated_nodes": self.evaluated_nodes
        }
    
    def find_minimum_spanning_tree(self, start_node=None):
        """
        Find the Minimum Spanning Tree (MST) using Prim's Algorithm
        Returns the list of edges that make up the MST and the total infrastructure cost
        """
        if not self.graph:
            return {"mst_edges": [], "total_cost": 0.0, "evaluated_nodes": 0}
        
        if start_node is None:
            start_node = next(iter(self.graph))
        
        mst_edges = []
        visited = set([start_node])
        total_cost = 0.0
        self.evaluated_nodes = 0

        priority_queue = []

        for neighbor_id, edge_weight in self.graph.get(start_node, []):
            heapq.heappush(priority_queue, (edge_weight, start_node, neighbor_id))
        
        while priority_queue and len(visited) < len(self.graph):
            weight, u, v = heapq.heappop(priority_queue)

            if v in visited:
                continue

            visited.add(v)
            mst_edges.append((u, v))
            total_cost += weight
            self.evaluated_nodes += 1

            for neighbor_id, edge_weight in self.graph.get(v, []):
                if neighbor_id not in visited:
                    heapq.heappush(priority_queue, (edge_weight, v, neighbor_id))

        return {
            "mst_edges": mst_edges,
            "total_cost": total_cost,
            "evaluated_nodes": self.evaluated_nodes
        }
    