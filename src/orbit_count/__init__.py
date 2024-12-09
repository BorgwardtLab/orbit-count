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


