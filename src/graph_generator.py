import networkx as nx
import utils as u

S = 103154                   # Seed
P = [0.125, 0.25, 0.5, 0.75] # Edge Probabilities
N = [4, 256, 1]              # Vertices [start, stop, step]

if __name__  == '__main__':

    for p in P:
        
        for n in [i for i in range(*N)]:

            G = nx.fast_gnp_random_graph(n, p, seed=S)
            u.write_graph(G, n, p, folder='../graphs')