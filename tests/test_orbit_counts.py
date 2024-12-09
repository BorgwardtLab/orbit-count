from typing import Optional, List
import pytest
import networkx as nx
import orbit_count
import subprocess
import os
from pathlib import Path
import numpy as np
import tempfile

def _edge_list_reindexed(graph: nx.Graph, node_list: Optional[List] = None) -> np.ndarray:
    node_iter = node_list if node_list is not None else graph.nodes()
    id2idx = {str(u): idx for idx, u in enumerate(node_iter)}

    edges = [[id2idx[str(u)], id2idx[str(v)]] for u, v in graph.edges()]
    return np.array(edges, dtype=int)


def _baseline_implementation(orca_executable: Path, graph: nx.Graph, orbit_type: str, graphlet_size: int, node_list: Optional[List] = None):
    in_tmp, in_fname = tempfile.mkstemp()
    out_tmp, out_fname = tempfile.mkstemp()
    try:
        os.close(in_tmp)
        os.close(out_tmp)
        with open(in_fname, "w") as in_tmp:
            in_tmp.write(
                str(graph.number_of_nodes()) + " " + str(graph.number_of_edges()) + "\n"
            )
            for u, v in _edge_list_reindexed(graph, node_list):
                in_tmp.write(str(u) + " " + str(v) + "\n")
        subprocess.check_output([orca_executable, orbit_type, str(graphlet_size), in_fname, out_fname])
        with open(out_fname, "r") as out_tmp:
            counts = [[int(item) for item in line.split(" ")] for line in out_tmp.readlines()]
    finally:
        os.unlink(in_fname)

    return np.array(counts)


@pytest.mark.parametrize("orbit_type", ["node", "edge"])
@pytest.mark.parametrize("graphlet_size", [4, 5])
@pytest.mark.parametrize("seed", [0, 1, 2, 3, 4, 5, 6])
@pytest.mark.parametrize("n,p", [(100, 0.05), (100, 0.1), (16, 0.1), (16, 0.2), (32, 0.02)])
def test_erdos_renyi(orca_executable, orbit_type, n, p, graphlet_size, seed):
    graph = nx.erdos_renyi_graph(n, p, seed=seed)
    node_list = list(graph.nodes)
    if orbit_type == "node":
        counts = orbit_count.node_orbit_counts(graph, graphlet_size=graphlet_size, node_list=node_list)
    elif orbit_type == "edge":
        counts = orbit_count.edge_orbit_counts(graph, graphlet_size=graphlet_size, node_list=node_list)
    baseline_counts = _baseline_implementation(orca_executable=orca_executable, graph=graph, orbit_type=orbit_type, graphlet_size=graphlet_size, node_list=node_list)
    assert baseline_counts.shape == counts.shape
    assert np.allclose(baseline_counts, counts)