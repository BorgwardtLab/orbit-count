from typing import Optional, List
import networkx as nx
import numpy as np

from _orca import motif_counts


def _edge_list_reindexed(graph: nx.Graph, node_list: Optional[List] = None) -> np.ndarray:
    node_iter = node_list if node_list is not None else graph.nodes()
    id2idx = {str(u): idx for idx, u in enumerate(node_iter)}

    edges = [[id2idx[str(u)], id2idx[str(v)]] for u, v in graph.edges()]
    return np.array(edges, dtype=int)


def node_orbit_counts(graph: nx.Graph, graphlet_size: int = 4, node_list: Optional[List] = None) -> np.ndarray:
    return motif_counts("node", graphlet_size, graph.number_of_nodes(), _edge_list_reindexed(graph, node_list))


def edge_orbit_counts(graph: nx.Graph, graphlet_size: int = 4, node_list: Optional[List] = None) -> np.ndarray:
    return motif_counts("edge", graphlet_size, graph.number_of_nodes(), _edge_list_reindexed(graph, node_list))


