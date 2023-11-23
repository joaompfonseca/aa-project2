import networkx as nx
import utils as u

def n_unconvered_edges(G: nx.Graph, node: int, unconvered_edges: set):
    """
    Return the number of uncovered edges incident to the given node.
    """
    n_unconvered_edges = 0
    for u, v in G.edges(node):
        if (u, v) in unconvered_edges or (v, u) in unconvered_edges:
            n_unconvered_edges += 1
    return n_unconvered_edges

def mvc_greedy_highest_incidence(G: nx.Graph):
    """
    Greedy algorithm for the minimum vertex cover problem.
    Keep adding the node with the most uncovered edges to the vertex cover.
    Return when all edges are covered.
    """
    mvc_val = 0
    mvc_set = set()
    mvc_ops = 0 # Number of operations

    unconvered_edges = set(G.edges)
    nodes = set(G.nodes)

    while unconvered_edges:
        mvc_ops += 1

        # Find the node with the most incident uncovered edges
        node = max(nodes, key=lambda node: n_unconvered_edges(G, node, unconvered_edges))
        mvc_ops += len(nodes) # Number of operations in the max function

        # Add the node to the vertex cover
        mvc_val += 1
        mvc_set.add(node)

        # Remove the node from the list of nodes
        nodes.remove(node)

        # Remove all edges incident to the node from the uncovered edges set
        unconvered_edges = {(u,v) for u,v in unconvered_edges if (u, v) not in G.edges(node) or (v, u) not in G.edges(node)}
    
    return mvc_val, mvc_set, mvc_ops
    

if __name__  == '__main__':

    G = u.read_graph(10, 0.125, folder='../graphs')
    print(mvc_greedy_highest_incidence(G))
    u.draw(G)