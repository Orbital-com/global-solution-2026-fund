class BruteForce:
    def __init__(self, graph_obj):
        self.graph = graph_obj.get_graph()

        self.recursive_calls = 0
        self.evaluated_paths = 0

        self.best_path = None
        self.min_cost = float("inf")
    
    def find_best_path(self, origin, destination):
        """Main function that the user calls to initiate the Brute Force attack"""
        self.recursive_calls = 0
        self.evaluated_paths = 0
        self.best_path = None
        self.min_cost = float('inf')

        visited = set()
        self._recursive_backtracking(origin, destination, [origin], visited, 0.0)


        return {
            "path": self.best_path,
            "cost": self.min_cost,
            "recursive_calls": self.recursive_calls,
            "evaluated_paths": self.evaluated_paths
        }
    
    def _recursive_backtracking(self, current, destination, current_path, visited, current_cost):
        """The function that does the heavy lifting of testing all possibilities using backtracking"""
        self.recursive_calls += 1

        if current == destination:
            self.evaluated_paths += 1
            if current_cost < self.min_cost:
                self.min_cost = current_cost
                self.best_path = list(current_path)
            return
        
        visited.add(current)
        neighbors = self.graph.get(current, [])
        for neighbor_id, edge_weight in neighbors:
            if neighbor_id not in visited:
                current_path.append(neighbor_id)
                self._recursive_backtracking(
                    neighbor_id,
                    destination,
                    current_path,
                    visited,
                    current_cost + edge_weight
                )
                current_path.pop()

        visited.remove(current)