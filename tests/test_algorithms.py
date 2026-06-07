import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_structures import Graph, BinarySearchTree
from src.brute_force import BruteForce
from src.greedy import Greedy

@pytest.fixture
def mock_environment():
    """Creates a controlled mini-scenario of 4 cities (A, B, C, D) for collision testing"""
    g = Graph()
    bst = BinarySearchTree()
    
    cidades = [
        ("A", "Alpha", 1.0, 100, 5000),
        ("B", "Bravo", 9.5, 100, 5000),
        ("C", "Charlie", 2.0, 100, 5000),
        ("D", "Delta", 8.5, 100, 5000)
    ]
    
    for cid in cidades:
        g.add_municipality(*cid)
        bst.insert(cid)
        
    rotas = [
        ("A", "B", 10.0), ("B", "A", 10.0),
        ("A", "C", 5.0),  ("C", "A", 5.0),
        ("B", "D", 5.0),  ("D", "B", 5.0),
        ("C", "D", 15.0), ("D", "C", 15.0)
    ]
    
    for u, v, peso in rotas:
        g.add_edge(u, v, peso)
        
    return g, bst

def test_cross_validation_algorithms(mock_environment):
    """Performs cross-validation, confirming that the algorithms deliver logical routes"""
    g, bst = mock_environment
    
    fb_finder = BruteForce(g)
    gr_finder = Greedy(g)
    
    origem = "A"
    destino = "D"
    
    resultado_fb = fb_finder.find_best_path(origem, destino)
    
    resultado_gr = gr_finder.find_best_path(origem, destino, bst, 8.0)
    
    assert resultado_fb['cost'] == 15.0
    assert resultado_fb['path'] == ["A", "B", "D"]
    assert resultado_fb['evaluated_paths'] > 0
    
    assert resultado_gr['cost'] == 12.0
    assert resultado_gr['path'] == ["A", "B", "D"]
    assert resultado_gr['evaluated_nodes'] > 0