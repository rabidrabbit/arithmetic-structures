"""
Searches for arithmetic structures given a graph.
"""

import matplotlib.pyplot as plt
import networkx as nx

def is_arithmetic_structure(graph):
    """
    Determines if a given graph is an arithmetic structure and returns a boolean.
    """
    return False

def initialize_node_weights(graph):
    """
    Sets (in-place) the weight attribute to be zero for all nodes of a given graph.
    """
    for node in graph.nodes:
        graph.nodes[node]['weight'] = 0
    return None

if __name__ == "__main__":
    G = nx.path_graph(8)
    initialize_node_weights(G)
    labels = {n: G.nodes[n]['weight'] for n in G.nodes}
    nx.draw(G, with_labels=True, labels=labels)
    plt.savefig("dummy.png")
