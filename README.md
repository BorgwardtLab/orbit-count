# Python Bindings for ORCA
This package implements python bindings for the [ORbit Counting Algorithm](https://github.com/thocevar/orca).

The original source code was modified to avoid memory leaks upon repeated function calls and allow for parallel orbit counting when provided with several graphs (using OpenMP).


## Installation
Install via pip:

`pip install orbit-count`


## Usage

This package provides two functinos, namely `node_orbit_counts` and `edge_orbit_counts`. Both functions accept networkx graphs and return numpy arrays.

```python
import networkx as nx
import orbit_count

graph = nx.erdos_renyi_graph(64, 0.2, seed=0)       # Graph with N nodes and M edges

# Graphlet size may be 4 or 5
node_count = orbit_count.node_orbit_counts(graph, graphlet_size=4)      # Returns numpy array of shape (N, 15)
edge_count = orbit_count.edge_orbit_counts(graph, graphlet_size=4)      # Returns numpy array of shape (M, 12)

# To get a specific ordering of counts, pass node_list or edge_list
node_count = orbit_count.node_orbit_counts(graph, graphlet_size=5, node_list=list(graph.nodes))
edge_count = orbit_count.edge_orbit_counts(graph, graphlet_size=5, edge_list=list(graph.edges))

# Count orbits in multiple graphs in parallel
node_count = orbit_count.batched_node_orbit_counts([nx.erdos_renyi_graph(64, 0.2, seed=i) for i in range(32)], graphlet_size=4)
edge_count = orbit_count.batched_edge_orbit_counts([nx.erdos_renyi_graph(64, 0.2, seed=i) for i in range(32)], graphlet_size=4)
```

## License
The source (i.e., the code provided in this GitHub repository) is licensed under GPL v3, as detailed in LICENSE.md.
The wheels may bundle an external implementation of OpenMP as a dynamically linked library. We refer to LICENSE.wheel.md for information on how these components are licensed.