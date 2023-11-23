import itertools
import networkx as nx
import utils as u

def is_vertex_cover(G: nx.Graph, nodes: tuple):
    """
    Check if the given nodes are a vertex cover for the given graph.
    """
    for u, v in G.edges:
        # If neither u nor v are in the nodes set, then the edge is not covered
        if u not in nodes and v not in nodes:
            return False
    return True

def mvc_brute_force(G: nx.Graph):
    """
    Brute force algorithm for the minimum vertex cover problem.
    Go through all possible combinations of nodes, in increasing order of size.
    Return the first combination that is a vertex cover.
    """
    mvc_val = G.number_of_nodes() # Worst case: all nodes are in the minimum vertex cover
    mvc_set = set(G.nodes)
    mvc_ops = 0 # Number of operations

    for i in range(1, G.number_of_nodes()):
        mvc_ops += 1
        
        for nodes in itertools.combinations(G.nodes, i):
            mvc_ops += 1

            if is_vertex_cover(G, nodes):
                mvc_val, mvc_set = i, set(nodes)
                break
        # MVC not found for the current i - continue to i+1
        else:
            continue 
        # MVC found for the current i - break and return
        break

    return mvc_val, mvc_set, mvc_ops
    

if __name__  == '__main__':

    G = u.read_graph(10, 0.125, folder='../graphs')
    print(mvc_brute_force(G))
    u.draw(G)