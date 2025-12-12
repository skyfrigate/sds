# Copyright 2024-2025, skyfrigate, biface
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Graph data structures module.

This module provides comprehensive graph data structures including nodes, edges,
and various graph implementations (directed, undirected, weighted) with different
internal representations (adjacency lists and matrices).

Structure
---------
The module is organized into several components:

- **Nodes**: GraphNode class for representing vertices
- **Edges**: Edge classes (directed/undirected, weighted/unweighted)
- **Interfaces**: Abstract base classes defining graph contracts
- **Graph implementations**: Concrete classes for different graph types
- **Representations**: Adjacency list and matrix-based implementations

Submodules
----------
node
    Graph node implementations with unique identifiers.
edge
    Edge classes for connecting nodes (directed, weighted variants).
interfaces
    Abstract base classes for graph types.
graph
    Base unweighted, undirected graph implementation.
directed
    Directed and explicitly undirected graph implementations.
weighted
    Weighted graph implementations (directed and undirected).
adjacency
    Explicit adjacency list and matrix graph representations.

Node Classes
------------
GraphNode
    Node class for graphs with unique identifiers and arbitrary data.

Edge Classes
------------
Edge
    Base undirected, unweighted edge connecting two nodes.
DirectedEdge
    Edge with explicit direction from source to target.
WeightedEdge
    Undirected edge with associated numeric weight.
WeightedDirectedEdge
    Edge that is both weighted and directed.

Graph Implementations
---------------------
Graph
    Base undirected, unweighted graph using adjacency lists.
DirectedGraph
    Directed graph with separate in/out adjacency tracking.
UndirectedGraph
    Explicitly undirected graph with edge type validation.
WeightedGraph
    Undirected graph with weighted edges.
WeightedDirectedGraph
    Directed graph with weighted edges.
AdjacencyListGraph
    Explicit adjacency list representation.
AdjacencyMatrixGraph
    Matrix-based representation for dense graphs.

Abstract Interfaces
-------------------
AbstractGraph
    Base interface for all graph types.
AbstractDirectedGraph
    Interface for directed graphs with in/out degree operations.
AbstractUndirectedGraph
    Interface for undirected graphs.
AbstractWeightedGraph
    Interface for weighted graphs with weight operations.

Examples
--------
Create a simple undirected graph:

>>> from sds.graph import Graph, GraphNode, Edge
>>> g = Graph()
>>> n1 = GraphNode("Paris", "paris")
>>> n2 = GraphNode("London", "london")
>>> g.add_node(n1)
>>> g.add_node(n2)
>>> g.add_edge(Edge(n1, n2))
>>> g.is_connected()
True

Create a directed graph:

>>> from sds.graph import DirectedGraph, DirectedEdge
>>> dg = DirectedGraph()
>>> dg.add_node(n1)
>>> dg.add_node(n2)
>>> dg.add_edge(DirectedEdge(n1, n2))
>>> dg.has_edge(n1, n2)
True
>>> dg.has_edge(n2, n1)  # Direction matters
False

Create a weighted graph:

>>> from sds.graph import WeightedGraph, WeightedEdge
>>> wg = WeightedGraph()
>>> wg.add_node(n1)
>>> wg.add_node(n2)
>>> wg.add_edge(WeightedEdge(n1, n2, weight=344.0))  # km
>>> wg.get_edge_weight(n1, n2)
344.0

Use adjacency matrix for dense graphs:

>>> from sds.graph import AdjacencyMatrixGraph
>>> mg = AdjacencyMatrixGraph(max_nodes=100)
>>> mg.add_node(n1)
>>> mg.add_node(n2)
>>> mg.add_edge(Edge(n1, n2))
>>> matrix = mg.get_matrix()
>>> matrix[0][1]
1

Implementation Notes
--------------------
**Memory Efficiency:**
- AdjacencyListGraph and Graph: O(V + E) - best for sparse graphs
- AdjacencyMatrixGraph: O(V²) - best for dense graphs

**Time Complexity:**
- Edge lookup: O(1) for matrix, O(degree) for lists
- Add edge: O(1) amortized for both
- Neighbors: O(V) for matrix, O(degree) for lists

**Design Patterns:**
- All graph classes inherit from appropriate abstract interfaces
- Edges are immutable after creation
- Nodes use unique IDs for fast lookup
- Caching is used for expensive operations (connectivity, cycles)

**Type Safety:**
- Full mypy strict mode compliance
- Clear separation between directed/undirected edges
- Type checking prevents mixing incompatible edge types

Notes
-----
The graph module uses __slots__ for memory efficiency and supports
comprehensive type checking with mypy in strict mode. All classes follow
NumPy documentation standards.

Graph structure is managed separately from nodes - edges connect nodes
but do not modify node objects. This allows flexible graph manipulation
without corrupting node data.

For graph algorithms (DFS, BFS, shortest paths, etc.), see the
sds.algorithms.graph_algorithms module.

See Also
--------
sds.core : Core data structure interfaces.
sds.tree : Tree data structures.
sds.linear : Linear data structures (stacks, queues).
sds.algorithms.graph_algorithms : Graph traversal and pathfinding algorithms.

References
----------
.. [1] Cormen, T. H., et al. (2009). Introduction to Algorithms, 3rd ed.
       MIT Press. Chapter 22: Elementary Graph Algorithms.
.. [2] Sedgewick, R., & Wayne, K. (2011). Algorithms, 4th ed.
       Addison-Wesley. Chapter 4: Graphs.
"""

from .adjacency import AdjacencyListGraph, AdjacencyMatrixGraph
from .directed import DirectedGraph, UndirectedGraph
from .edge import DirectedEdge, Edge, WeightedDirectedEdge, WeightedEdge
from .graph import Graph
from .interfaces import (
    AbstractDirectedGraph,
    AbstractGraph,
    AbstractUndirectedGraph,
    AbstractWeightedGraph,
)
from .node import GraphNode
from .weighted import WeightedDirectedGraph, WeightedGraph

__all__ = [
    # Node
    "GraphNode",
    # Edges
    "Edge",
    "DirectedEdge",
    "WeightedEdge",
    "WeightedDirectedEdge",
    # Graphs - Basic
    "Graph",
    "DirectedGraph",
    "UndirectedGraph",
    # Graphs - Weighted
    "WeightedGraph",
    "WeightedDirectedGraph",
    # Graphs - Adjacency Representations
    "AdjacencyListGraph",
    "AdjacencyMatrixGraph",
    # Interfaces
    "AbstractGraph",
    "AbstractDirectedGraph",
    "AbstractUndirectedGraph",
    "AbstractWeightedGraph",
]

__version__ = "0.1.0"
