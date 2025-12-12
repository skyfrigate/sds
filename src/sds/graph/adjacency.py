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

"""Adjacency-based graph implementations (matrix and list).

This module provides explicit adjacency-based representations of graphs:
- AdjacencyListGraph: explicit list-based representation
- AdjacencyMatrixGraph: 2D matrix representation for dense graphs

While Graph already uses adjacency lists internally, these classes make
the representation explicit and optimized for specific use cases.

Classes
-------
AdjacencyListGraph
    Graph with explicit adjacency list representation.
AdjacencyMatrixGraph
    Graph using 2D matrix for adjacency representation.

Examples
--------
Create an adjacency list graph:

>>> from sds.graph import AdjacencyListGraph, GraphNode, Edge
>>> g = AdjacencyListGraph()
>>> n1 = GraphNode("A", "n1")
>>> n2 = GraphNode("B", "n2")
>>> g.add_node(n1)
>>> g.add_node(n2)
>>> g.add_edge(Edge(n1, n2))
>>> g.has_edge(n1, n2)
True

Create an adjacency matrix graph:

>>> mg = AdjacencyMatrixGraph(max_nodes=10)
>>> mg.add_node(n1)
>>> mg.add_node(n2)
>>> mg.add_edge(Edge(n1, n2))
>>> mg.get_matrix()[0][1]  # Matrix representation
1

Notes
-----
AdjacencyListGraph is memory-efficient for sparse graphs.
AdjacencyMatrixGraph is efficient for dense graphs with O(1) edge lookup.

See Also
--------
sds.graph.graph : Base Graph class using adjacency lists.
sds.graph.directed : Directed and undirected graph implementations.
"""

from collections import deque
from typing import Dict, Iterator, List, Optional, Set

from .edge import Edge
from .interfaces import AbstractGraph
from .node import GraphNode

__all__ = ["AdjacencyListGraph", "AdjacencyMatrixGraph"]


class AdjacencyListGraph(AbstractGraph):
    """Explicit adjacency list graph implementation.

    This implementation makes adjacency list representation explicit,
    storing neighbors for each node in a dictionary of sets. While
    similar to the base Graph class, this version emphasizes the
    adjacency list structure.

    Parameters
    ----------
    allow_multi_edges : bool, optional
        If True, allows multiple edges between same nodes. Default is False.

    Attributes
    ----------
    allow_multi_edges : bool
        Whether multiple edges are allowed (read-only property).

    Examples
    --------
    Create and use adjacency list graph:

    >>> g = AdjacencyListGraph()
    >>> n1 = GraphNode("A", "n1")
    >>> n2 = GraphNode("B", "n2")
    >>> g.add_node(n1)
    >>> g.add_node(n2)
    >>> g.add_edge(Edge(n1, n2))
    >>> list(g.get_adjacency_list("n1"))
    ['n2']

    Notes
    -----
    Time Complexity:
    - add_node: O(1)
    - add_edge: O(1) amortized
    - has_edge: O(1) amortized
    - neighbors: O(degree)

    Space Complexity: O(V + E)
    Memory-efficient for sparse graphs.

    See Also
    --------
    Graph : Base graph implementation.
    AdjacencyMatrixGraph : Matrix-based representation.
    """

    def __init__(self, allow_multi_edges: bool = False) -> None:
        """Initialize an empty adjacency list graph.

        Parameters
        ----------
        allow_multi_edges : bool, optional
            Allow multiple edges between same nodes. Default is False.
        """
        super().__init__()
        self._allow_multi_edges = allow_multi_edges
        self._nodes: Dict[str, GraphNode] = {}
        self._adjacency_list: Dict[str, Set[str]] = {}
        self._edges: List[Edge] = []
        self._connectivity_cache: Optional[bool] = None
        self._cache_valid = False

    @property
    def allow_multi_edges(self) -> bool:
        """Check if multigraph mode is enabled."""
        return self._allow_multi_edges

    def _invalidate_cache(self) -> None:
        """Invalidate cached properties."""
        self._connectivity_cache = None
        self._cache_valid = False

    def get_adjacency_list(self, node_id: str) -> Set[str]:
        """Get the adjacency list for a specific node.

        Parameters
        ----------
        node_id : str
            ID of the node.

        Returns
        -------
        Set[str]
            Set of neighbor node IDs.

        Raises
        ------
        ValueError
            If node is not in the graph.

        Examples
        --------
        >>> g = AdjacencyListGraph()
        >>> n1 = GraphNode("A", "n1")
        >>> n2 = GraphNode("B", "n2")
        >>> g.add_node(n1)
        >>> g.add_node(n2)
        >>> g.add_edge(Edge(n1, n2))
        >>> "n2" in g.get_adjacency_list("n1")
        True
        """
        if node_id not in self._nodes:
            raise ValueError(f"Node {node_id} not in graph")
        return self._adjacency_list[node_id].copy()

    def add_node(self, node: GraphNode) -> None:
        """Add a node to the graph."""
        if not isinstance(node, GraphNode):
            raise TypeError(f"Expected GraphNode, got {type(node).__name__}")
        if node.id in self._nodes:
            raise ValueError(f"Node {node.id} already exists in graph")
        self._nodes[node.id] = node
        self._adjacency_list[node.id] = set()
        self._invalidate_cache()

    def remove_node(self, node: GraphNode) -> None:
        """Remove a node and all its incident edges."""
        if node.id not in self._nodes:
            raise ValueError(f"Node {node.id} not in graph")
        self._edges = [e for e in self._edges if not e.incident_to(node)]
        neighbors = self._adjacency_list[node.id].copy()
        for neighbor_id in neighbors:
            self._adjacency_list[neighbor_id].discard(node.id)
        del self._nodes[node.id]
        del self._adjacency_list[node.id]
        self._invalidate_cache()

    def has_node(self, node: GraphNode) -> bool:
        """Check if node exists in the graph."""
        return node.id in self._nodes

    def add_edge(self, edge: Edge) -> None:
        """Add an edge to the graph."""
        if not isinstance(edge, Edge):
            raise TypeError(f"Expected Edge, got {type(edge).__name__}")
        if not self.has_node(edge.node1):
            raise ValueError(f"Node {edge.node1.id} not in graph")
        if not self.has_node(edge.node2):
            raise ValueError(f"Node {edge.node2.id} not in graph")
        if not self._allow_multi_edges and self.has_edge(edge.node1, edge.node2):
            raise ValueError(
                f"Edge between {edge.node1.id} and {edge.node2.id} already exists"
            )
        self._edges.append(edge)
        self._adjacency_list[edge.node1.id].add(edge.node2.id)
        self._adjacency_list[edge.node2.id].add(edge.node1.id)
        self._invalidate_cache()

    def remove_edge(self, edge: Edge) -> None:
        """Remove an edge from the graph."""
        if edge not in self._edges:
            raise ValueError(
                f"Edge between {edge.node1.id} and {edge.node2.id} not in graph"
            )
        self._edges.remove(edge)
        n1_id, n2_id = edge.node1.id, edge.node2.id
        has_other = any(e.connects(edge.node1, edge.node2) for e in self._edges)
        if not has_other:
            self._adjacency_list[n1_id].discard(n2_id)
            self._adjacency_list[n2_id].discard(n1_id)
        self._invalidate_cache()

    def has_edge(self, node1: GraphNode, node2: GraphNode) -> bool:
        """Check if an edge exists between two nodes."""
        if not self.has_node(node1) or not self.has_node(node2):
            return False
        return node2.id in self._adjacency_list[node1.id]

    def get_edge(self, node1: GraphNode, node2: GraphNode) -> Optional[Edge]:
        """Get the edge between two nodes."""
        for edge in self._edges:
            if edge.connects(node1, node2):
                return edge
        return None

    def neighbors(self, node: GraphNode) -> Iterator[GraphNode]:
        """Get all neighbors of a node."""
        if not self.has_node(node):
            raise ValueError(f"Node {node.id} not in graph")
        for neighbor_id in self._adjacency_list[node.id]:
            yield self._nodes[neighbor_id]

    def degree(self, node: GraphNode) -> int:
        """Get the degree of a node."""
        if not self.has_node(node):
            raise ValueError(f"Node {node.id} not in graph")
        if not self._allow_multi_edges:
            return len(self._adjacency_list[node.id])
        return sum(1 for e in self._edges if e.incident_to(node))

    def nodes(self) -> Iterator[GraphNode]:
        """Get all nodes in the graph."""
        yield from self._nodes.values()

    def edges(self) -> Iterator[Edge]:
        """Get all edges in the graph."""
        yield from self._edges

    def node_count(self) -> int:
        """Get the number of nodes."""
        return len(self._nodes)

    def edge_count(self) -> int:
        """Get the number of edges."""
        return len(self._edges)

    def is_connected(self) -> bool:
        """Check if the graph is connected."""
        if self._cache_valid and self._connectivity_cache is not None:
            return self._connectivity_cache
        result = self._check_connectivity()
        self._connectivity_cache = result
        self._cache_valid = True
        return result

    def _check_connectivity(self) -> bool:
        """Check connectivity using BFS."""
        if self.is_empty() or self.node_count() == 1:
            return True
        start_node = next(iter(self._nodes.values()))
        visited: Set[str] = set()
        queue: deque[GraphNode] = deque([start_node])
        visited.add(start_node.id)
        while queue:
            current = queue.popleft()
            for neighbor in self.neighbors(current):
                if neighbor.id not in visited:
                    visited.add(neighbor.id)
                    queue.append(neighbor)
        return len(visited) == self.node_count()

    def get_node_by_id(self, node_id: str) -> Optional[GraphNode]:
        """Get a node by its ID."""
        return self._nodes.get(node_id)

    def is_empty(self) -> bool:
        """Check if the graph is empty."""
        return len(self._nodes) == 0

    def clear(self) -> None:
        """Remove all nodes and edges."""
        self._nodes.clear()
        self._adjacency_list.clear()
        self._edges.clear()
        self._invalidate_cache()

    def __len__(self) -> int:
        """Return the number of nodes."""
        return self.node_count()

    def __contains__(self, node: GraphNode) -> bool:
        """Check if node is in the graph."""
        return self.has_node(node)

    def __iter__(self) -> Iterator[GraphNode]:
        """Iterate over nodes."""
        return self.nodes()

    def __repr__(self) -> str:
        """Return detailed string representation."""
        return (
            f"AdjacencyListGraph(nodes={self.node_count()}, "
            f"edges={self.edge_count()}, multi_edges={self._allow_multi_edges})"
        )

    def __str__(self) -> str:
        """Return simple string representation."""
        return (
            f"AdjacencyListGraph: {self.node_count()} nodes, "
            f"{self.edge_count()} edges"
        )


class AdjacencyMatrixGraph(AbstractGraph):
    """Graph implementation using adjacency matrix representation.

    Uses a 2D matrix to store edge information. Efficient for dense graphs
    with O(1) edge lookup but requires O(V²) space.

    Parameters
    ----------
    max_nodes : int, optional
        Maximum number of nodes the graph can hold. Default is 100.
    allow_multi_edges : bool, optional
        If True, matrix stores edge counts. Default is False.

    Attributes
    ----------
    max_nodes : int
        Maximum capacity (read-only property).
    allow_multi_edges : bool
        Whether multiple edges are allowed (read-only property).

    Examples
    --------
    Create a matrix graph:

    >>> g = AdjacencyMatrixGraph(max_nodes=5)
    >>> n1 = GraphNode("A", "n1")
    >>> n2 = GraphNode("B", "n2")
    >>> g.add_node(n1)
    >>> g.add_node(n2)
    >>> g.add_edge(Edge(n1, n2))
    >>> g.get_matrix()[0][1]
    1

    Notes
    -----
    Time Complexity:
    - add_node: O(1)
    - add_edge: O(1)
    - has_edge: O(1)
    - neighbors: O(V)

    Space Complexity: O(V²)
    Best for dense graphs where V is bounded.

    See Also
    --------
    AdjacencyListGraph : List-based representation (better for sparse graphs).
    """

    def __init__(self, max_nodes: int = 100, allow_multi_edges: bool = False) -> None:
        """Initialize an empty adjacency matrix graph.

        Parameters
        ----------
        max_nodes : int, optional
            Maximum number of nodes. Default is 100.
        allow_multi_edges : bool, optional
            Allow multiple edges. Default is False.
        """
        super().__init__()
        if max_nodes <= 0:
            raise ValueError("max_nodes must be positive")
        self._max_nodes = max_nodes
        self._allow_multi_edges = allow_multi_edges
        self._matrix: List[List[int]] = [[0] * max_nodes for _ in range(max_nodes)]
        self._nodes: Dict[str, GraphNode] = {}
        self._node_indices: Dict[str, int] = {}
        self._index_to_node: Dict[int, str] = {}
        self._next_index = 0
        self._edges: List[Edge] = []
        self._connectivity_cache: Optional[bool] = None
        self._cache_valid = False

    @property
    def max_nodes(self) -> int:
        """Get the maximum number of nodes."""
        return self._max_nodes

    @property
    def allow_multi_edges(self) -> bool:
        """Check if multigraph mode is enabled."""
        return self._allow_multi_edges

    def _invalidate_cache(self) -> None:
        """Invalidate cached properties."""
        self._connectivity_cache = None
        self._cache_valid = False

    def get_matrix(self) -> List[List[int]]:
        """Get a copy of the adjacency matrix.

        Returns
        -------
        List[List[int]]
            Copy of the adjacency matrix.

        Examples
        --------
        >>> g = AdjacencyMatrixGraph(max_nodes=3)
        >>> n1 = GraphNode("A", "n1")
        >>> n2 = GraphNode("B", "n2")
        >>> g.add_node(n1)
        >>> g.add_node(n2)
        >>> g.add_edge(Edge(n1, n2))
        >>> matrix = g.get_matrix()
        >>> matrix[0][1]
        1
        """
        return [row[: self._next_index] for row in self._matrix[: self._next_index]]

    def add_node(self, node: GraphNode) -> None:
        """Add a node to the graph."""
        if not isinstance(node, GraphNode):
            raise TypeError(f"Expected GraphNode, got {type(node).__name__}")
        if node.id in self._nodes:
            raise ValueError(f"Node {node.id} already exists in graph")
        if self._next_index >= self._max_nodes:
            raise ValueError(f"Graph is full. Maximum {self._max_nodes} nodes allowed")
        self._nodes[node.id] = node
        self._node_indices[node.id] = self._next_index
        self._index_to_node[self._next_index] = node.id
        self._next_index += 1
        self._invalidate_cache()

    def remove_node(self, node: GraphNode) -> None:
        """Remove a node and all its incident edges."""
        if node.id not in self._nodes:
            raise ValueError(f"Node {node.id} not in graph")
        idx = self._node_indices[node.id]

        # Remove edges involving this node
        self._edges = [e for e in self._edges if not e.incident_to(node)]

        # Clear matrix row and column
        for i in range(self._next_index):
            self._matrix[idx][i] = 0
            self._matrix[i][idx] = 0

        # Compact the matrix by shifting rows/columns
        if idx < self._next_index - 1:
            # Shift rows up
            for i in range(idx, self._next_index - 1):
                for j in range(self._next_index):
                    self._matrix[i][j] = self._matrix[i + 1][j]

            # Shift columns left
            for i in range(self._next_index):
                for j in range(idx, self._next_index - 1):
                    self._matrix[i][j] = self._matrix[i][j + 1]

            # Update indices for shifted nodes
            for i in range(idx + 1, self._next_index):
                node_id = self._index_to_node[i]
                self._node_indices[node_id] = i - 1
                self._index_to_node[i - 1] = node_id

        # Remove node
        del self._nodes[node.id]
        del self._node_indices[node.id]
        del self._index_to_node[self._next_index - 1]
        self._next_index -= 1
        self._invalidate_cache()

    def has_node(self, node: GraphNode) -> bool:
        """Check if node exists in the graph."""
        return node.id in self._nodes

    def add_edge(self, edge: Edge) -> None:
        """Add an edge to the graph."""
        if not isinstance(edge, Edge):
            raise TypeError(f"Expected Edge, got {type(edge).__name__}")
        if not self.has_node(edge.node1):
            raise ValueError(f"Node {edge.node1.id} not in graph")
        if not self.has_node(edge.node2):
            raise ValueError(f"Node {edge.node2.id} not in graph")

        idx1 = self._node_indices[edge.node1.id]
        idx2 = self._node_indices[edge.node2.id]

        if not self._allow_multi_edges and self._matrix[idx1][idx2] > 0:
            raise ValueError(
                f"Edge between {edge.node1.id} and {edge.node2.id} already exists"
            )

        self._edges.append(edge)
        self._matrix[idx1][idx2] += 1
        self._matrix[idx2][idx1] += 1
        self._invalidate_cache()

    def remove_edge(self, edge: Edge) -> None:
        """Remove an edge from the graph."""
        if edge not in self._edges:
            raise ValueError(
                f"Edge between {edge.node1.id} and {edge.node2.id} not in graph"
            )

        idx1 = self._node_indices[edge.node1.id]
        idx2 = self._node_indices[edge.node2.id]

        self._edges.remove(edge)
        self._matrix[idx1][idx2] = max(0, self._matrix[idx1][idx2] - 1)
        self._matrix[idx2][idx1] = max(0, self._matrix[idx2][idx1] - 1)
        self._invalidate_cache()

    def has_edge(self, node1: GraphNode, node2: GraphNode) -> bool:
        """Check if an edge exists between two nodes."""
        if not self.has_node(node1) or not self.has_node(node2):
            return False
        idx1 = self._node_indices[node1.id]
        idx2 = self._node_indices[node2.id]
        return self._matrix[idx1][idx2] > 0

    def get_edge(self, node1: GraphNode, node2: GraphNode) -> Optional[Edge]:
        """Get the edge between two nodes."""
        for edge in self._edges:
            if edge.connects(node1, node2):
                return edge
        return None

    def neighbors(self, node: GraphNode) -> Iterator[GraphNode]:
        """Get all neighbors of a node."""
        if not self.has_node(node):
            raise ValueError(f"Node {node.id} not in graph")
        idx = self._node_indices[node.id]
        for i in range(self._next_index):
            if self._matrix[idx][i] > 0:
                neighbor_id = self._index_to_node[i]
                yield self._nodes[neighbor_id]

    def degree(self, node: GraphNode) -> int:
        """Get the degree of a node."""
        if not self.has_node(node):
            raise ValueError(f"Node {node.id} not in graph")
        idx = self._node_indices[node.id]
        return sum(self._matrix[idx][i] for i in range(self._next_index))

    def nodes(self) -> Iterator[GraphNode]:
        """Get all nodes in the graph."""
        yield from self._nodes.values()

    def edges(self) -> Iterator[Edge]:
        """Get all edges in the graph."""
        yield from self._edges

    def node_count(self) -> int:
        """Get the number of nodes."""
        return len(self._nodes)

    def edge_count(self) -> int:
        """Get the number of edges."""
        return len(self._edges)

    def is_connected(self) -> bool:
        """Check if the graph is connected."""
        if self._cache_valid and self._connectivity_cache is not None:
            return self._connectivity_cache
        result = self._check_connectivity()
        self._connectivity_cache = result
        self._cache_valid = True
        return result

    def _check_connectivity(self) -> bool:
        """Check connectivity using BFS."""
        if self.is_empty() or self.node_count() == 1:
            return True
        start_node = next(iter(self._nodes.values()))
        visited: Set[str] = set()
        queue: deque[GraphNode] = deque([start_node])
        visited.add(start_node.id)
        while queue:
            current = queue.popleft()
            for neighbor in self.neighbors(current):
                if neighbor.id not in visited:
                    visited.add(neighbor.id)
                    queue.append(neighbor)
        return len(visited) == self.node_count()

    def get_node_by_id(self, node_id: str) -> Optional[GraphNode]:
        """Get a node by its ID."""
        return self._nodes.get(node_id)

    def is_empty(self) -> bool:
        """Check if the graph is empty."""
        return len(self._nodes) == 0

    def clear(self) -> None:
        """Remove all nodes and edges."""
        self._nodes.clear()
        self._node_indices.clear()
        self._index_to_node.clear()
        self._matrix = [[0] * self._max_nodes for _ in range(self._max_nodes)]
        self._edges.clear()
        self._next_index = 0
        self._invalidate_cache()

    def __len__(self) -> int:
        """Return the number of nodes."""
        return self.node_count()

    def __contains__(self, node: GraphNode) -> bool:
        """Check if node is in the graph."""
        return self.has_node(node)

    def __iter__(self) -> Iterator[GraphNode]:
        """Iterate over nodes."""
        return self.nodes()

    def __repr__(self) -> str:
        """Return detailed string representation."""
        return (
            f"AdjacencyMatrixGraph(nodes={self.node_count()}, "
            f"edges={self.edge_count()}, max_nodes={self._max_nodes}, "
            f"multi_edges={self._allow_multi_edges})"
        )

    def __str__(self) -> str:
        """Return simple string representation."""
        return (
            f"AdjacencyMatrixGraph: {self.node_count()}/{self._max_nodes} nodes, "
            f"{self.edge_count()} edges"
        )
