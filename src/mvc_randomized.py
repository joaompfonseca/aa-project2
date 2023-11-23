import itertools
import math
import networkx as nx
import random as r
import utils as u


def is_vertex_cover(G: nx.Graph, nodes: set):
    """
    Check if the given nodes are a vertex cover for the given graph.
    """
    for u, v in G.edges:
        # If neither u nor v are in the nodes set, then the edge is not covered
        if u not in nodes and v not in nodes:
            return False
    return True


def random_subsets(nodes: list, k: int):
    """
    Generate a random subset of k nodes.
    It shuffles elements in place to generate unique random combinations without repetition.
    """
    pool = list(nodes)
    n = len(pool)
    while True:
        indices = sorted(r.sample(range(n), k))
        yield set(pool[i] for i in indices)
        while True:
            j = k - 1
            while j >= 0 and indices[j] == j + n - k:
                j -= 1
            if j < 0:
                return
            indices[j] += 1
            for m in range(j+1, k):
                indices[m] = indices[m-1] + 1
            yield set(pool[i] for i in indices)

def max_tries(n: int, k: int, percent_k: float):
    """
    Maximum number of tries for a given k.
    """
    if k < 20:
        return math.ceil(math.comb(n, k)) # Try all possible subsets because k is small
    else:
        return math.ceil(math.comb(n, k) * percent_k)


def mvc_randomized_decreasing(G: nx.Graph, percent_k = 0.1):
    """
    Randomized algorithm for the minimum vertex cover problem, using a decreasing order of k.
    It tests a percentage of the possible subsets of k nodes and checks if they are a vertex cover.
    Stops when no better solution is found for a given k, and returns the best solution found.
    """
    # No edges - empty set is the only solution
    if G.number_of_edges() == 0:
        return 0, set(), 0

    mvc_ops = 0  # Number of operations

    # Initialize variables
    n = G.number_of_nodes()
    k = n
    all_nodes = list(G.nodes)

    # Keep track of the best solution found so far
    best_mvc_val = k
    best_mvc_set = set(all_nodes)

    n_tries_k = 0  # Number of tries for the current k
    n_max_tries = max_tries(n,k,percent_k) # Maximum number of tries for the current k

    # Try to find a solution for each k in decreasing order
    while k > 0 and n_tries_k < n_max_tries:
        
        # Iterate through random subsets of k nodes
        for nodes in random_subsets(all_nodes, k):
            mvc_ops += 1

            # If the subset is a vertex cover, update best solution
            if is_vertex_cover(G, nodes):
                best_mvc_val, best_mvc_set = k, nodes
                k -= 1
                # Clean for next iteration
                n_tries_k = 0
                n_max_tries = max_tries(n,k,percent_k)
                break
            
            n_tries_k += 1
        
            # If max tries are reached, return best solution
            if n_tries_k == n_max_tries:
                break
            
    return best_mvc_val, best_mvc_set, mvc_ops

if __name__ == "__main__":
    G = u.read_graph(10, 0.125, folder="../graphs")

    mvc_val, mvc_set, mvc_ops = mvc_randomized_decreasing(G)

    print(mvc_val, mvc_set, mvc_ops)

    pos = nx.spring_layout(G)
    u.draw_solution(G, mvc_set, pos)
