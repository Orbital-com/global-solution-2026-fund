class Graph:
    def __init__(self):
        self.adjacency_list = {}
        self.vertices = {}
    
    def add_municipality(self, municipality_id, name, risk_index, service_cost, population):
        """Adds a municipality to the graph"""

        vertex = (municipality_id, name, risk_index, service_cost, population)
        self.vertices[municipality_id] = vertex

        if municipality_id not in self.adjacency_list:
            self.adjacency_list[municipality_id] = []
    
    def add_edge(self, source_id, destination_id, weight):
        """
        Adds a route (edge) between two municipalities
        The weight equals the travel distance (km)
        """
        if source_id in self.adjacency_list and destination_id in self.adjacency_list:
            self.adjacency_list[source_id].append((destination_id, weight))
        else:
            raise ValueError("Source or destination municipality not registered in the graph.")
    
    def get_graph(self):
        """Returns the exact adjacency dictionary structure requested"""
        return self.adjacency_list

class Node:
    def __init__ (self, municipality_tuple):
        self.data = municipality_tuple
        self.risk = municipality_tuple[2]
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__ (self):
        self.root = None
    
    def insert(self, municipality_tuple):
        """Inserts a municipality maintaining the BST property (left < parent < right)"""
        if self.root is None:
            self.root = Node(municipality_tuple)
        else:
            self._insert_recursive(self.root, municipality_tuple)
        
    def _insert_recursive(self, node, municipality_tuple):
        risk = municipality_tuple[2]
        if risk < node.risk:
            if node.left is None:
                node.left = Node(municipality_tuple)
            else:
                self._insert_recursive(node.left, municipality_tuple)
        elif risk > node.risk:
            if node.right is None:
                node.right = Node(municipality_tuple)
            else:
                self._insert_recursive(node.right, municipality_tuple)
        else:
            if node.right is None:
                node.right = Node(municipality_tuple)
            else:
                self._insert_recursive(node.right, municipality_tuple)
    
    def search_range(self, r_min, r_max):
        """Returns all municipalities with a risk index in the [r_min, r_max] range"""
        results = []
        self._search_range_recursive(self.root, r_min, r_max, results)
        return results

    def _search_range_recursive(self, node, r_min, r_max, results):
        if node is None:
            return

        if node.risk > r_min:
            self._search_range_recursive(node.left, r_min, r_max, results)
        
        if r_min <= node.risk <= r_max:
            results.append(node.data)

        if node.risk < r_max:
            self._search_range_recursive(node.right, r_min, r_max, results)
    
    def in_order_path(self):
        """Returns municipalities in ascending order of risk"""
        results = []
        self._in_order_recursive(self.root, results)
        return results
    
    def _in_order_recursive(self, node, results):
        if node is not None:
            self._in_order_recursive(node.left, results)
            results.append(node.data)
            self._in_order_recursive(node.right, results)

    def height(self):
        """Calculates the height of the tree"""
        return self._height_recursive(self.root)

    def _height_recursive(self, node):
        if node is None:
            return -1
        left_height = self._height_recursive(node.left)
        right_height = self._height_recursive(node.right)
        return 1 + max(left_height, right_height)

    def remove(self, municipality_id):
        """
        Removes a node by ID and rebalances pointers
        """

        target_node = self._find_by_id(self.root, municipality_id)
        if target_node is None:
            return False
        
        target_risk = target_node.risk
        self.root = self._remove_recursive(self.root, target_risk, municipality_id)
        return True

    def _find_by_id(self, node, municipality_id):
        """Helper to find a node by ID (O(N) time since it's not the sorting key)"""
        if node is None:
            return None
        if node.data[0] == municipality_id:
            return node
        
        left_search = self._find_by_id(node.left, municipality_id)
        if left_search:
            return left_search
        return self._find_by_id(node.right, municipality_id)
    
    def _remove_recursive(self, node, risk, municipality_id):
        if node is None:
            return node
        
        if risk < node.risk:
            node.left = self._remove_recursive(node.left, risk, municipality_id)
        elif risk > node.risk:
            node.right = self._remove_recursive(node.right, risk, municipality_id)
        else:
            if node.data[0] != municipality_id:
                node.right = self._remove_recursive(node.right, risk, municipality_id)
                return node
            
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            
            temp = self._get_min_value_node(node.right)
            node.data = temp.data
            node.risk = temp.risk
            node.right = self._remove_recursive(node.right, temp.risk, temp.data[0])
        
        return node
    
    def _get_min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current
