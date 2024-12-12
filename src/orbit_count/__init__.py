"""Python wrappers around bindings provided by _orca module.

Copyright (C) 2024  Max-Planck-Institute for Biochemistry, MLSB

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from typing import Optional, List, Collection
import networkx as nx
import numpy as np

from ._orca import batched_motif_counts as _batched_motif_counts
from ._orca import motif_counts as _motif_counts


def _edge_list_reindexed(
    graph: nx.Graph, node_list: Optional[List] = None, edge_list: Optional[List] = None
) -> np.ndarray:
    node_iter = node_list if node_list is not None else graph.nodes()
    id2idx = {str(u): idx for idx, u in enumerate(node_iter)}

    edge_iter = edge_list if edge_list is not None else graph.edges()
    edges = [[id2idx[str(u)], id2idx[str(v)]] for u, v in edge_iter]
    return np.array(edges, dtype=int)


def node_orbit_counts(
    graph: nx.Graph, graphlet_size: int = 4, node_list: Optional[List] = None
) -> np.ndarray:
    return _motif_counts(
        "node",
        graphlet_size,
        graph.number_of_nodes(),
        _edge_list_reindexed(graph, node_list=node_list),
    )


def batched_node_orbit_counts(
    graphs: Collection[nx.Graph],
    graphlet_size: int = 4,
    node_lists: Optional[Collection[List]] = None,
) -> List[np.ndarray]:
    if node_lists is not None and len(node_lists) != len(graphs):
        raise ValueError(
            "`node_lists` must either be None or have the same length as `graphs`"
        )
    else:
        node_lists = [None for _ in range(len(graphs))]

    num_nodes = np.array([g.number_of_nodes() for g in graphs], dtype=int)
    all_edge_indices = [
        _edge_list_reindexed(g, node_list=node_list)
        for g, node_list in zip(graphs, node_lists)
    ]

    all_counts = _batched_motif_counts(
        "node", graphlet_size, num_nodes, all_edge_indices
    )
    return all_counts


def edge_orbit_counts(
    graph: nx.Graph, graphlet_size: int = 4, edge_list: Optional[List] = None
) -> np.ndarray:
    return _motif_counts(
        "edge",
        graphlet_size,
        graph.number_of_nodes(),
        _edge_list_reindexed(graph, edge_list=edge_list),
    )


def batched_edge_orbit_counts(
    graphs: Collection[nx.Graph],
    graphlet_size: int = 4,
    edge_lists: Optional[Collection[List]] = None,
) -> List[np.ndarray]:
    if edge_lists is not None and len(edge_lists) != len(graphs):
        raise ValueError(
            "`edge_lists` must either be None or have the same length as `graphs`"
        )
    else:
        edge_lists = [None for _ in range(len(graphs))]

    num_nodes = np.array([g.number_of_nodes() for g in graphs], dtype=int)
    all_edge_indices = [
        _edge_list_reindexed(g, edge_list=edge_list)
        for g, edge_list in zip(graphs, edge_lists)
    ]

    all_counts = _batched_motif_counts(
        "edge", graphlet_size, num_nodes, all_edge_indices
    )
    return all_counts
