import json
import os
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import networkx as nx


def draw(G):
    nx.draw_networkx(G)
    plt.show()


def draw_solution(G, nodes, pos):
    nx.draw_networkx(G, pos=pos)
    nx.draw_networkx(G.subgraph(nodes), pos=pos, node_color="r")
    plt.show()


def write_graph(G, n, p, folder):
    data = nx.node_link_data(G)
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(f"{folder}/g_n{n:02}_p{p:.3f}.json", "w") as f:
        json.dump(data, f, indent=4)


def read_graph(n, p, folder):
    with open(f"{folder}/g_n{n:02}_p{p:.3f}.json", "r") as f:
        data = json.load(f)
    return nx.node_link_graph(data)


def read_graph_internet(folder, name):
    with open(f"{folder}/{name}.txt", "r") as f:
        data = f.readlines()
    # Ignore metadata and skip to the edges
    data = data[4:]
    # Convert to tuples
    edges = []
    for d in data:
        split = d.strip().split(" ")
        edges.append((int(split[0]), int(split[1])))
    # Create graph
    G = nx.Graph()
    G.add_edges_from(edges)
    return G


def write_benchmark(header, data, algorithm, p, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(f"{folder}/b_{algorithm}_p{p:.3f}.csv", "w") as f:
        f.write(";".join(header) + "\n")
        for d in data:
            f.write(";".join(map(str, d)) + "\n")


def write_benchmark_internet(header, data, algorithm, name, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(f"{folder}/b_{algorithm}_{name}.csv", "w") as f:
        f.write(";".join(header) + "\n")
        for d in data:
            f.write(";".join(map(str, d)) + "\n")