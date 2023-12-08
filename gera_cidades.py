import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import networkx.algorithms.approximation as nx_app
import math

G = nx.random_geometric_graph(20, radius=0.4, seed=100)

pos = nx.get_node_attributes(G, "pos")

# Depot should be at (0,0)
pos[0] = (0.5, 0.5)

H = G.copy()
# Calculating the distances between the nodes as edge's weight.
for i in range(len(pos)):
    for j in range(i + 1, len(pos)):
        dist = math.hypot(pos[i][0] - pos[j][0], pos[i][1] - pos[j][1])
        dist = 10000*dist
        G.add_edge(i, j, weight=int(dist))

cycle = nx_app.christofides(G, weight="weight")

edge_list = list(nx.utils.pairwise(cycle))

res = [(0, 19), (1, 16), (2, 6), (3, 2), (4, 0), (5, 11), (6, 18), (7, 17), (8, 9), (9, 15), (10, 1), (11, 12), (12, 10), (13, 14), (14, 8), (15, 4), (16, 3), (17, 5), (18, 13), (19, 7)]



nx.write_weighted_edgelist(G,'cidades2', delimiter='\t')

# Draw closest edges on each node only
nx.draw_networkx_edges(H, pos, edge_color="blue", width=0.5)

# Draw the route
nx.draw_networkx(
    G,
    pos,
    with_labels=True,
    edgelist=res,
    edge_color="red",
    node_size=200,
    width=3,
)

print("The route of the traveller is:", cycle)
plt.show()
