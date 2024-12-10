from typing import Optional, List
import pytest
import networkx as nx
import orbit_count
import subprocess
import os
from pathlib import Path
import numpy as np
import tempfile
import gc
import memory_profiler



def _edge_list_reindexed(graph: nx.Graph, node_list: Optional[List] = None, edge_list: Optional[List] = None) -> np.ndarray:
    node_iter = node_list if node_list is not None else graph.nodes()
    id2idx = {str(u): idx for idx, u in enumerate(node_iter)}

    edge_iter = edge_list if edge_list is not None else graph.edges()
    edges = [[id2idx[str(u)], id2idx[str(v)]] for u, v in edge_iter]
    return np.array(edges, dtype=int)


def _baseline_implementation(orca_executable: Path, graph: nx.Graph, orbit_type: str, graphlet_size: int, node_list: Optional[List] = None, edge_list: Optional[List] = None) -> np.ndarray:
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
    edge_list = list(graph.edges)
    if orbit_type == "node":
        counts = orbit_count.node_orbit_counts(graph, graphlet_size=graphlet_size, node_list=node_list)
    elif orbit_type == "edge":
        counts = orbit_count.edge_orbit_counts(graph, graphlet_size=graphlet_size, edge_list=edge_list)
    baseline_counts = _baseline_implementation(orca_executable=orca_executable, graph=graph, orbit_type=orbit_type, graphlet_size=graphlet_size, node_list=node_list, edge_list=edge_list)
    assert baseline_counts.shape == counts.shape
    assert np.allclose(baseline_counts, counts)


@pytest.mark.parametrize("graphlet_size", [4, 5])
@pytest.mark.parametrize("seed", [0, 1, 2, 3, 4, 5, 6])
@pytest.mark.parametrize("n,p", [(100, 0.05), (100, 0.1), (16, 0.1), (16, 0.2), (32, 0.02)])
def test_node_list(n, p, graphlet_size, seed):
    graph = nx.erdos_renyi_graph(n, p, seed=seed)
    node_list = list(graph.nodes)
    rng = np.random.default_rng(seed)
    perm = rng.permutation(n)
    node_list_perm = [node_list[idx] for idx in perm]
    
    res1 = orbit_count.node_orbit_counts(graph, graphlet_size=graphlet_size, node_list=node_list)
    res2 = orbit_count.node_orbit_counts(graph, graphlet_size=graphlet_size, node_list=node_list_perm)
    
    assert np.allclose(res1[perm], res2)


@pytest.mark.parametrize("graphlet_size", [4, 5])
@pytest.mark.parametrize("seed", [0, 1, 2, 3, 4, 5, 6])
@pytest.mark.parametrize("n,p", [(100, 0.05), (100, 0.1), (16, 0.1), (16, 0.2), (32, 0.02)])
def test_edge_list(n, p, graphlet_size, seed):
    graph = nx.erdos_renyi_graph(n, p, seed=seed)
    edge_list = list(graph.edges)
    rng = np.random.default_rng(seed)
    perm = rng.permutation(graph.number_of_edges())
    edge_list_perm = [edge_list[idx] for idx in perm]

    
    res1 = orbit_count.edge_orbit_counts(graph, graphlet_size=graphlet_size, edge_list=edge_list)
    res2 = orbit_count.edge_orbit_counts(graph, graphlet_size=graphlet_size, edge_list=edge_list_perm)
    
    assert np.allclose(res1[perm], res2)


@pytest.mark.parametrize("orbit_type", ["node", "edge"])
@pytest.mark.parametrize("graphlet_size", [4, 5])
def test_memory_leak(orbit_type, graphlet_size):
    """
    Unit test to detect potential memory leaks when calling a C++ function
    """
    # Number of iterations to test for memory leaks
    iterations = 10_000
    
    graph = nx.erdos_renyi_graph(64, 0.2, seed=0)

    # Track memory usage before the test
    gc.collect()  # Ensure garbage collection before measuring
    mem_before = memory_profiler.memory_usage()[0]
    
    # Call the C++ function multiple times
    for _ in range(iterations):
        if orbit_type == "node":
            result = orbit_count.node_orbit_counts(graph, graphlet_size=graphlet_size)
        else:
            result = orbit_count.edge_orbit_counts(graph, graphlet_size=graphlet_size)
    
    # Collect garbage and measure memory after test
    gc.collect()
    mem_after = memory_profiler.memory_usage()[0]
    
    # Calculate memory increase
    memory_increase = mem_after - mem_before
    
    # Set an acceptable memory increase threshold (in MB)
    acceptable_increase = 5  
    
    # Assert that memory increase is within the acceptable threshold
    assert memory_increase < acceptable_increase, \
        f"Potential memory leak detected. Memory increased by {memory_increase} MB"
