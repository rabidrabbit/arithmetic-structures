"""
Searches for arithmetic structures given a graph.
"""

import matplotlib.pyplot as plt
import networkx as nx
from math import gcd
from functools import reduce
from itertools import product

def get_weight(graph, node):
    return graph.nodes[node]['weight']

def is_arithmetic_structure(graph):
    """
    Determines if a given graph is an arithmetic structure and returns a boolean.
    An arithmetic structure occurs when:
    (1) The weight of a vertex divides the total sum of its neighbors' weights
    (2) The numbers used have no common factor
    """
    for node in graph.nodes:
        neighbors = G.neighbors(node)
        
        # Verify that the weight of a vertex divides the total sum of its neighbors' weights
        total_weight_sum = 0
        for neighbor in neighbors:
            total_weight_sum += get_weight(graph, neighbor)
        if total_weight_sum % get_weight(graph, node):
            return False

        # Verify that there is no factor that divides each number used
        if reduce(gcd, [graph.nodes[n]['weight'] for n in graph.nodes]) != 1:
            return False

    return True

def initialize_node_weights(graph):
    """
    Sets (in-place) the weight attribute to be one for all nodes of a given graph.
    """
    for node in graph.nodes:
        graph.nodes[node]['weight'] = 1

def set_weights(graph, weights):
    """
    Given a graph and list of weights [(node_id, weight)], sets (in-place) the weights of each node.
    """
    for i in range(len(weights)):
        graph.nodes[list(graph.nodes)[i]]['weight'] = weights[i]

def exhausitive_search(graph, min_weight = 1, max_weight = 25):
    """
    Exhaustively searches for arithmetical structures by using combinations with repetitions on the list [min_weight..max_weight].
    """
    initialize_node_weights(graph)
    solutions = []

    for combination in product(range(min_weight, max_weight + 1), repeat=graph.number_of_nodes()):
        set_weights(graph, combination)
        if is_arithmetic_structure(graph):
            solutions.append(combination)

    return solutions

if __name__ == "__main__":
    G = nx.complete_graph(4)
    solutions = exhausitive_search(G)
    print(solutions)
    print(len(solutions))

    # Draw graph to screen/save to file
    labels = {n: G.nodes[n]['weight'] for n in G.nodes}
    nx.draw(G, with_labels=True, labels=labels)
    plt.savefig("dummy.png")
