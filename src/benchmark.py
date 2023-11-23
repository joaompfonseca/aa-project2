import networkx as nx
import time
import utils as u
import mvc_brute_force as bf
import mvc_greedy as gr
import mvc_randomized as rd

P = [0.125, 0.25, 0.5, 0.75]  # Edge Probabilities
N = [4, 256, 1]               # Vertices [start, stop, step]

PK = [0.125, 0.25, 0.5, 0.75] # Percentages of k

GN = ['SWtinyG']              # Internet Graph Names

def benchmark(G, algorithm):
    """
    Benchmark the given algorithm on the given graph.
    """
    ts = time.time()
    mvc_val, mvc_set, mvc_ops = algorithm(G)
    te = time.time()
    return mvc_val, f'"{",".join(map(str, list(mvc_set)))}"', mvc_ops, te - ts

if __name__  == '__main__':

    header = ['n', 'mvc_val', 'mvc_set', 'ops', 'time']

    # Generated Graphs
    
    for p in P:

        d_brute_force = []
        d_greedy_highest_incidence = []
        
        for n in [i for i in range(*N)]:

            G = u.read_graph(n, p, '../graphs')
            print(f'Graph: n={n}, p={p:.3f}.')

            if n < 30:
                res = benchmark(G, bf.mvc_brute_force)
                print(f'Brute-Force: done in {res[3]} seconds.')
                d_brute_force.append([n, *res])

            res = benchmark(G, gr.mvc_greedy_highest_incidence)
            print(f'Greedy, Highest Incidence: done in {res[3]} seconds.')
            d_greedy_highest_incidence.append([n, *res])
       
            print()

        u.write_benchmark(header, d_brute_force, 'brute-force', p, '../benchmarks')
        u.write_benchmark(header, d_greedy_highest_incidence, 'greedy-highest-incidence', p, '../benchmarks')

    for pk in PK: # Percentage of k

        for p in P: # Edge probability
        
            d_randomized_decreasing = []
    
            for n in [i for i in range(*N) if i < 30]: # Number of vertices
            
                G = u.read_graph(n, p, '../graphs')
                print(f'Graph: n={n}, p={p:.3f}.')
    
                res = benchmark(G, lambda G: rd.mvc_randomized_decreasing(G, percent_k=pk))
                print(f'Randomized, Decreasing, pk={pk:.3f}: done in {res[3]} seconds.')
                d_randomized_decreasing.append([n, *res])
    
                print()
    
            u.write_benchmark(header, d_randomized_decreasing, f'randomized-decreasing-pk{pk:.3f}', p, '../benchmarks')
    
    # Internet Graphs
    
    for gn in GN: # Graph name
        
        G = u.read_graph_internet('../graphs_internet', gn)
        n = G.number_of_nodes()
        e = G.number_of_edges()
        print(f'Graph {gn}: n={n}, e={e}.')
        
        res = benchmark(G, bf.mvc_brute_force)
        print(f'Brute-Force: done in {res[3]} seconds.')
        d_brute_force = [[n, *res]]
        
        u.write_benchmark_internet(header, d_brute_force, 'brute-force', gn, '../benchmarks_internet')

        res = benchmark(G, gr.mvc_greedy_highest_incidence)
        print(f'Greedy, Highest Incidence: done in {res[3]} seconds.')
        d_greedy_highest_incidence = [[n, *res]]
        
        u.write_benchmark_internet(header, d_greedy_highest_incidence, 'greedy-highest-incidence', gn, '../benchmarks_internet')
        
        for pk in PK: # Percentage of k
                
            res = benchmark(G, lambda G: rd.mvc_randomized_decreasing(G, percent_k=pk))
            print(f'Randomized, Decreasing, pk={pk:.3f}: done in {res[3]} seconds.')
            d_randomized_decreasing = [[n, *res]]
        
            u.write_benchmark_internet(header, d_randomized_decreasing, f'randomized-decreasing-pk={pk:.3f}', gn, '../benchmarks_internet')
        
        print()
    