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

def get_total_weight_sum(graph, nodes):
    return sum([get_weight(graph, n) for n in nodes])

def is_arithmetic_structure(graph):
    """
    Determines if a given graph is an arithmetic structure and returns a boolean.
    An arithmetic structure occurs when:
    (1) The weight of a vertex divides the total sum of its neighbors' weights
    (2) The numbers used have no common factor (besides 1)
    """
    for node in graph.nodes:
        neighbors = graph.neighbors(node)
        
        # Verify that the weight of a vertex divides the total sum of its neighbors' weights
        if get_total_weight_sum(graph, neighbors) % get_weight(graph, node):
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

def exhausitive_search(graph, min_weight = 1, max_weight = 10):
    """
    Exhaustively searches for arithmetical structures by using combinations with repetitions on the list [min_weight..max_weight].
    Let n denote the number of vertices. Then, there are (max_weight - min_weight + 1)^n possible combinations.
    """
    initialize_node_weights(graph)
    solutions = []

    for combination in product(range(min_weight, max_weight + 1), repeat=graph.number_of_nodes()):
        # Prune combinations that have a factor (other than 1) dividing each number
        if reduce(gcd, combination) != 1:
            continue

        set_weights(graph, combination)
        if is_arithmetic_structure(graph):
            solutions.append(combination)

    return solutions

def is_smooth_graph(graph):
    """
    Decides if a given graph is smooth, where no vertices can be removed while preserving an arithmetic structure.
    A vertex can be removed if its weight is equal to the total sum of its neighbors' weights. 
    """
    if not is_arithmetic_structure(graph):
        return False

    for node in graph.nodes:
        neighbors = graph.neighbors(node)

        total_neighbor_weight_sum = get_total_weight_sum(graph, neighbors)
        node_weight = get_weight(graph, node)

        if node_weight == total_neighbor_weight_sum:
            return False
    
    return True

def smooth_graph(graph):
    """
    Recursively smooths a graph and returns it.
    """
    return None

def create_bident_graph(length = 0):
    """
    Labelling the fork vertices as vx and vy, constructs a path starting from v0, which creates a bident graph.
    """
    graph = nx.path_graph(length + 2)
    graph.add_node(length + 2)
    graph.add_edge(length + 2, length)  # Create fork at the end of the path

    return graph


if __name__ == "__main__":
    G = nx.complete_graph(4)
    initialize_node_weights(G)
    # print(nx.adjacency_matrix(G).todense())
    solutions = exhausitive_search(G, max_weight=25)
    # print(solutions)
    # print(len(solutions))

    # for s in solutions:
    #     set_weights(G, s)
    #     print(s, end='')
    #     print(" is smooth? %r" % (is_smooth_graph(G)))

    # Draw graph to screen/save to file
    labels = {n: G.nodes[n]['weight'] for n in G.nodes}
    nx.draw(G, with_labels=True, labels=labels)
    plt.savefig("dummy.png")
