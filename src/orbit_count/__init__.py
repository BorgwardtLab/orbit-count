import networkx as nx
import numpy as np

from _orca import motif_counts


def _edge_list_reindexed(graph: nx.Graph) -> np.ndarray:
    idx = 0
    id2idx = dict()
    for u in graph.nodes():
        id2idx[str(u)] = idx
        idx += 1

    edges = []
    for u, v in graph.edges():
        edges.append([id2idx[str(u)], id2idx[str(v)]])
    return np.array(edges, dtype=int)


def node_orbit_counts(graph: nx.Graph, graphlet_size: int = 4) -> np.ndarray:
    return motif_counts("node", graphlet_size, graph.number_of_nodes(), _edge_list_reindexed(graph))


def edge_orbit_counts(graph: nx.Graph, graphlet_size: int = 4) -> np.ndarray:
    return motif_counts("edge", graphlet_size, graph.number_of_nodes(), _edge_list_reindexed(graph))


