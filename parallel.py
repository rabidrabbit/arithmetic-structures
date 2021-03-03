"""
Searches for arithmetic structures given a graph.
"""

from dask.distributed import Client, as_completed, wait
import dask.array as da
import matplotlib.pyplot as plt
import networkx as nx
import numpy as numpy
from math import gcd
from functools import reduce
from itertools import product, islice, chain

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

def is_arithmetic_structure(adjancency_matrix, start_condition, min_weight, max_weight, repeat_number):
    """
    Determines if a given graph is an arithmetic structure and returns a boolean.
    An arithmetic structure occurs when:
    (1) The weight of a vertex divides the total sum of its neighbors' weights
    (2) The numbers used have no common factor (besides 1)
    """
    solutions = []
    product_generator = product(range(min_weight, max_weight + 1), repeat=repeat_number)

    for c in product_generator:
        combination = start_condition + c

        # Prune combinations that have a factor (other than 1) dividing each number
        if reduce(gcd, combination) != 1:
            continue

        weights = numpy.array(combination).astype(float)
        total_neighbor_weight_sums = adjancency_matrix.dot(weights)
        fail_flag = False

        for i in range(len(total_neighbor_weight_sums)):
            total_sum = int(total_neighbor_weight_sums[i])
            node_weight = int(weights[i])

            # Verify that the weight of a vertex divides the total sum of its neighbors' weights
            if total_sum % node_weight:
                fail_flag = True
                break

        if not fail_flag:
            solutions.append(combination)

    return solutions

def parallel_exhausitive_search(graph, client, min_weight = 1, max_weight = 10):
    """
    Exhaustively searches for arithmetical structures by using combinations with repetitions on the list [min_weight..max_weight].
    Let n denote the number of vertices. Then, there are (max_weight - min_weight + 1)^n possible combinations.
    A parallel implementation of the exhaustive search algorithm.
    """
    futures = []
    solutions = []

    print(client)
    batch_size = 10**3

    adjancency_matrix = nx.adjacency_matrix(graph)

    for i in range(min_weight, max_weight+1):
        future = client.submit(is_arithmetic_structure, adjancency_matrix, (i,), min_weight, max_weight, graph.number_of_nodes() - 1)
        futures.append(future)

    wait(futures)
    solutions = [item for sublist in client.gather(futures) for item in sublist]

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
    client = Client()
    G = nx.balanced_tree(2, 3)
    solutions = parallel_exhausitive_search(G, max_weight=30, client=client)
    print(solutions)

    # for s in solutions:
    #     set_weights(G, s)
    #     print(s, end='')
    #     print(" is smooth? %r" % (is_smooth_graph(G)))

    # Draw graph to screen/save to file
    initialize_node_weights(G)
    labels = {n:n for n in G.nodes}
    nx.draw(G, with_labels=True, labels=labels)
    plt.savefig("dummy.png")
