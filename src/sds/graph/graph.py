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

"""Graph implementation using adjacency list representation.

This module provides a concrete implementation of an undirected, unweighted
graph using adjacency lists for efficient storage and traversal.

Classes
-------
Graph
    Undirected graph with adjacency list representation.

Examples
--------
Create and populate a graph:

>>> from sds.graph import Graph, GraphNode, Edge
>>> g = Graph()
>>> n1 = GraphNode("A", "n1")
>>> n2 = GraphNode("B", "n2")
>>> g.add_node(n1)
>>> g.add_node(n2)
>>> g.add_edge(Edge(n1, n2))
>>> g.node_count()
2
>>> g.edge_count()
1

Check connectivity:

>>> g.is_connected()
True
>>> g.degree(n1)
1

Iterate over nodes and edges:

>>> list(g.nodes())  # doctest: +SKIP
[GraphNode(id='n1', data='A'), GraphNode(id='n2', data='B')]
>>> for edge in g.edges():
...     print(edge)  # doctest: +SKIP
n1 -- n2

Notes
-----
This implementation uses adjacency lists which are efficient for sparse graphs.
Time complexity:
- add_node: O(1)
- add_edge: O(1)
- has_edge: O(degree(node))
- neighbors: O(degree(node))
- is_connected: O(V + E) with caching

See Also
--------
DirectedGraph : Directed graph implementation.
WeightedGraph : Weighted graph implementation.
"""

from collections import deque
from typing import Dict, Iterator, List, Optional, Set

from .edge import Edge
from .interfaces import AbstractGraph
from .node import GraphNode

__all__ = ["Graph"]


class Graph(AbstractGraph):
    """Undirected graph using adjacency list representation.

    A graph consists of nodes (vertices) connected by edges. This implementation
    uses adjacency lists to store connections, which is memory-efficient for
    sparse graphs.

    Parameters
    ----------
    allow_multi_edges : bool, optional
        If True, allows multiple edges between the same pair of nodes
        (multigraph). Default is False (simple graph).

    Attributes
    ----------
    allow_multi_edges : bool
        Whether multiple edges are allowed (read-only property).

    Examples
    --------
    Create a simple graph:

    >>> g = Graph()
    >>> n1 = GraphNode("A", "n1")
    >>> n2 = GraphNode("B", "n2")
    >>> g.add_node(n1)
    >>> g.add_node(n2)
    >>> g.add_edge(Edge(n1, n2))
    >>> g.has_edge(n1, n2)
    True

    Create a multigraph:

    >>> mg = Graph(allow_multi_edges=True)
    >>> mg.add_node(n1)
    >>> mg.add_node(n2)
    >>> mg.add_edge(Edge(n1, n2, data="edge1"))
    >>> mg.add_edge(Edge(n1, n2, data="edge2"))  # OK in multigraph
    >>> mg.edge_count()
    2

    Check connectivity:

    >>> g.is_connected()
    True
    >>> isolated = GraphNode("C", "n3")
    >>> g.add_node(isolated)
    >>> g.is_connected()
    False

    Notes
    -----
    Time Complexity:
    - add_node: O(1)
    - remove_node: O(degree(node) + E)
    - add_edge: O(1) or O(degree) if checking duplicates
    - remove_edge: O(degree(node))
    - has_edge: O(degree(node))
    - degree: O(1) amortized
    - neighbors: O(degree(node))
    - is_connected: O(V + E) with caching

    Space Complexity: O(V + E)

    See Also
    --------
    DirectedGraph : For directed graphs.
    WeightedGraph : For weighted graphs.
    """

    def __init__(self, allow_multi_edges: bool = False) -> None:
        """Initialize an empty graph.

        Parameters
        ----------
        allow_multi_edges : bool, optional
            Allow multiple edges between same nodes. Default is False.

        Examples
        --------
        >>> g = Graph()
        >>> g.is_empty()
        True

        >>> mg = Graph(allow_multi_edges=True)
        >>> mg.allow_multi_edges
        True
        """
        super().__init__()
        self._allow_multi_edges = allow_multi_edges
        self._nodes: Dict[str, GraphNode] = {}
        self._adjacency: Dict[str, Set[str]] = {}
        self._edges: List[Edge] = []

        # Caching for expensive operations
        self._connectivity_cache: Optional[bool] = None
        self._cache_valid = False

    @property
    def allow_multi_edges(self) -> bool:
        """Check if multigraph mode is enabled.

        Returns
        -------
        bool
            True if multiple edges are allowed.

        Examples
        --------
        >>> g = Graph()
        >>> g.allow_multi_edges
        False
        >>> mg = Graph(allow_multi_edges=True)
        >>> mg.allow_multi_edges
        True
        """
        return self._allow_multi_edges

    def _invalidate_cache(self) -> None:
        """Invalidate cached properties after graph modification.

        Called automatically when graph structure changes.
        """
        self._connectivity_cache = None
        self._cache_valid = False

    def add_node(self, node: GraphNode) -> None:
        """Add a node to the graph.

        Parameters
        ----------
        node : GraphNode
            Node to add.

        Raises
        ------
        TypeError
            If node is not a GraphNode.
        ValueError
            If node already exists in the graph.

        Examples
        --------
        >>> g = Graph()
        >>> n1 = GraphNode("A", "n1")
        >>> g.add_node(n1)
        >>> g.has_node(n1)
        True

        Duplicate nodes raise error:

        >>> g.add_node(n1)
        Traceback (most recent call last):
            ...
        ValueError: Node n1 already exists in graph

        Notes
        -----
        Time complexity: O(1)
        """
        if not isinstance(node, GraphNode):
            raise TypeError(f"Expected GraphNode, got {type(node).__name__}")

        if node.id in self._nodes:
            raise ValueError(f"Node {node.id} already exists in graph")

        self._nodes[node.id] = node
        self._adjacency[node.id] = set()
        self._invalidate_cache()

    def remove_node(self, node: GraphNode) -> None:
        """Remove a node and all its incident edges from the graph.

        Parameters
        ----------
        node : GraphNode
            Node to remove.

        Raises
        ------
        ValueError
            If node is not in the graph.

        Examples
        --------
        >>> g = Graph()
        >>> n1 = GraphNode("A", "n1")
        >>> n2 = GraphNode("B", "n2")
        >>> g.add_node(n1)
        >>> g.add_node(n2)
        >>> g.add_edge(Edge(n1, n2))
        >>> g.remove_node(n1)
        >>> g.has_node(n1)
        False
        >>> g.edge_count()  # Edge was also removed
        0

        Notes
        -----
        Time complexity: O(degree(node) + E)
        All edges incident to the node are also removed.
        """
        if node.id not in self._nodes:
            raise ValueError(f"Node {node.id} not in graph")

        # Remove all edges incident to this node
        self._edges = [e for e in self._edges if not e.incident_to(node)]

        # Remove from adjacency lists
        neighbors = self._adjacency[node.id].copy()
        for neighbor_id in neighbors:
            self._adjacency[neighbor_id].discard(node.id)

        # Remove node itself
        del self._nodes[node.id]
        del self._adjacency[node.id]
        self._invalidate_cache()

    def has_node(self, node: GraphNode) -> bool:
        """Check if node exists in the graph.

        Parameters
        ----------
        node : GraphNode
            Node to check.

        Returns
        -------
        bool
            True if node is in the graph.

        Examples
        --------
        >>> g = Graph()
        >>> n1 = GraphNode("A", "n1")
        >>> g.has_node(n1)
        False
        >>> g.add_node(n1)
        >>> g.has_node(n1)
        True

        Notes
        -----
        Time complexity: O(1)
        """
        return node.id in self._nodes

    def add_edge(self, edge: Edge) -> None:
        """Add an edge to the graph.

        Parameters
        ----------
        edge : Edge
            Edge to add.

        Raises
        ------
        TypeError
            If edge is not an Edge instance.
        ValueError
            If either node is not in the graph, or if edge already exists
            and multigraph mode is disabled.

        Examples
        --------
        >>> g = Graph()
        >>> n1 = GraphNode("A", "n1")
        >>> n2 = GraphNode("B", "n2")
        >>> g.add_node(n1)
        >>> g.add_node(n2)
        >>> g.add_edge(Edge(n1, n2))
        >>> g.has_edge(n1, n2)
        True

        Duplicate edges in simple graph raise error:

        >>> g.add_edge(Edge(n1, n2))
        Traceback (most recent call last):
            ...
        ValueError: Edge between n1 and n2 already exists...

        But allowed in multigraph:

        >>> mg = Graph(allow_multi_edges=True)
        >>> mg.add_node(n1)
        >>> mg.add_node(n2)
        >>> mg.add_edge(Edge(n1, n2))
        >>> mg.add_edge(Edge(n1, n2))  # OK
        >>> mg.edge_count()
        2

        Notes
        -----
        Time complexity: O(1) for multigraph, O(degree(node)) for simple graph.
        """
        if not isinstance(edge, Edge):
            raise TypeError(f"Expected Edge, got {type(edge).__name__}")

        # Validate nodes exist
        if not self.has_node(edge.node1):
            raise ValueError(f"Node {edge.node1.id} not in graph")
        if not self.has_node(edge.node2):
            raise ValueError(f"Node {edge.node2.id} not in graph")

        # Check for duplicate edges in simple graph
        if not self._allow_multi_edges and self.has_edge(edge.node1, edge.node2):
            raise ValueError(
                f"Edge between {edge.node1.id} and {edge.node2.id} already exists. "
                "Use allow_multi_edges=True for multigraph."
            )

        # Add edge
        self._edges.append(edge)

        # Update adjacency lists (bidirectional for undirected graph)
        self._adjacency[edge.node1.id].add(edge.node2.id)
        self._adjacency[edge.node2.id].add(edge.node1.id)

        self._invalidate_cache()

    def remove_edge(self, edge: Edge) -> None:
        """Remove an edge from the graph.

        Parameters
        ----------
        edge : Edge
            Edge to remove.

        Raises
        ------
        ValueError
            If edge is not in the graph.

        Examples
        --------
        >>> g = Graph()
        >>> n1 = GraphNode("A", "n1")
        >>> n2 = GraphNode("B", "n2")
        >>> g.add_node(n1)
        >>> g.add_node(n2)
        >>> e = Edge(n1, n2)
        >>> g.add_edge(e)
        >>> g.remove_edge(e)
        >>> g.has_edge(n1, n2)
        False

        Notes
        -----
        Time complexity: O(E) to find edge, O(degree) to update adjacency.
        For multigraphs, removes the first matching edge found.
        """
        if edge not in self._edges:
            raise ValueError(
                f"Edge between {edge.node1.id} and {edge.node2.id} not in graph"
            )

        self._edges.remove(edge)

        # Update adjacency lists only if no other edges exist
        # between these nodes (important for multigraphs)
        n1_id, n2_id = edge.node1.id, edge.node2.id
        has_other_edge = any(e.connects(edge.node1, edge.node2) for e in self._edges)

        if not has_other_edge:
            self._adjacency[n1_id].discard(n2_id)
            self._adjacency[n2_id].discard(n1_id)

        self._invalidate_cache()

    def has_edge(self, node1: GraphNode, node2: GraphNode) -> bool:
        """Check if an edge exists between two nodes.

        Parameters
        ----------
        node1 : GraphNode
            First node.
        node2 : GraphNode
            Second node.

        Returns
        -------
        bool
            True if edge exists (either direction for undirected graph).

        Examples
        --------
        >>> g = Graph()
        >>> n1 = GraphNode("A", "n1")
        >>> n2 = GraphNode("B", "n2")
        >>> g.add_node(n1)
        >>> g.add_node(n2)
        >>> g.has_edge(n1, n2)
        False
        >>> g.add_edge(Edge(n1, n2))
        >>> g.has_edge(n1, n2)
        True
        >>> g.has_edge(n2, n1)  # Undirected
        True

        Notes
        -----
        Time complexity: O(1) amortized using adjacency set.
        """
        if not self.has_node(node1) or not self.has_node(node2):
            return False
        return node2.id in self._adjacency[node1.id]

    def get_edge(self, node1: GraphNode, node2: GraphNode) -> Optional[Edge]:
        """Get the edge between two nodes.

        Parameters
        ----------
        node1 : GraphNode
            First node.
        node2 : GraphNode
            Second node.

        Returns
        -------
        Edge or None
            The edge if it exists, None otherwise.
            For multigraphs, returns the first edge found.

        Examples
        --------
        >>> g = Graph()
        >>> n1 = GraphNode("A", "n1")
        >>> n2 = GraphNode("B", "n2")
        >>> g.add_node(n1)
        >>> g.add_node(n2)
        >>> e = Edge(n1, n2, data="test")
        >>> g.add_edge(e)
        >>> found = g.get_edge(n1, n2)
        >>> found.data
        'test'
        >>> g.get_edge(n1, GraphNode("C", "n3")) is None
        True

        Notes
        -----
        Time complexity: O(E) in worst case.
        For multigraphs, returns first matching edge.
        """
        for edge in self._edges:
            if edge.connects(node1, node2):
                return edge
        return None

    def neighbors(self, node: GraphNode) -> Iterator[GraphNode]:
        """Get all neighbors of a node.

        Parameters
        ----------
        node : GraphNode
            Node to get neighbors for.

        Yields
        ------
        GraphNode
            Neighbor nodes.

        Raises
        ------
        ValueError
            If node is not in the graph.

        Examples
        --------
        >>> g = Graph()
        >>> n1 = GraphNode("A", "n1")
        >>> n2 = GraphNode("B", "n2")
        >>> n3 = GraphNode("C", "n3")
        >>> g.add_node(n1)
        >>> g.add_node(n2)
        >>> g.add_node(n3)
        >>> g.add_edge(Edge(n1, n2))
        >>> g.add_edge(Edge(n1, n3))
        >>> sorted([n.id for n in g.neighbors(n1)])
        ['n2', 'n3']

        Notes
        -----
        Time complexity: O(degree(node))
        """
        if not self.has_node(node):
            raise ValueError(f"Node {node.id} not in graph")

        for neighbor_id in self._adjacency[node.id]:
            yield self._nodes[neighbor_id]

    def degree(self, node: GraphNode) -> int:
        """Get the degree of a node (number of incident edges).

        Parameters
        ----------
        node : GraphNode
            Node to get degree for.

        Returns
        -------
        int
            Number of edges incident to the node.

        Raises
        ------
        ValueError
            If node is not in the graph.

        Examples
        --------
        >>> g = Graph()
        >>> n1 = GraphNode("A", "n1")
        >>> n2 = GraphNode("B", "n2")
        >>> g.add_node(n1)
        >>> g.add_node(n2)
        >>> g.degree(n1)
        0
        >>> g.add_edge(Edge(n1, n2))
        >>> g.degree(n1)
        1

        Notes
        -----
        Time complexity: O(1) amortized.
        For multigraphs, counts each edge separately.
        """
        if not self.has_node(node):
            raise ValueError(f"Node {node.id} not in graph")

        if not self._allow_multi_edges:
            return len(self._adjacency[node.id])
        else:
            # For multigraphs, count actual edges
            return sum(1 for e in self._edges if e.incident_to(node))

    def nodes(self) -> Iterator[GraphNode]:
        """Get all nodes in the graph.

        Yields
        ------
        GraphNode
            All nodes in the graph.

        Examples
        --------
        >>> g = Graph()
        >>> n1 = GraphNode("A", "n1")
        >>> n2 = GraphNode("B", "n2")
        >>> g.add_node(n1)
        >>> g.add_node(n2)
        >>> sorted([n.id for n in g.nodes()])
        ['n1', 'n2']

        Notes
        -----
        Time complexity: O(V)
        """
        yield from self._nodes.values()

    def edges(self) -> Iterator[Edge]:
        """Get all edges in the graph.

        Yields
        ------
        Edge
            All edges in the graph.

        Examples
        --------
        >>> g = Graph()
        >>> n1 = GraphNode("A", "n1")
        >>> n2 = GraphNode("B", "n2")
        >>> g.add_node(n1)
        >>> g.add_node(n2)
        >>> g.add_edge(Edge(n1, n2))
        >>> len(list(g.edges()))
        1

        Notes
        -----
        Time complexity: O(E)
        """
        yield from self._edges

    def node_count(self) -> int:
        """Get the number of nodes in the graph.

        Returns
        -------
        int
            Number of nodes.

        Examples
        --------
        >>> g = Graph()
        >>> g.node_count()
        0
        >>> g.add_node(GraphNode("A", "n1"))
        >>> g.node_count()
        1

        Notes
        -----
        Time complexity: O(1)
        """
        return len(self._nodes)

    def edge_count(self) -> int:
        """Get the number of edges in the graph.

        Returns
        -------
        int
            Number of edges.

        Examples
        --------
        >>> g = Graph()
        >>> g.edge_count()
        0
        >>> n1 = GraphNode("A", "n1")
        >>> n2 = GraphNode("B", "n2")
        >>> g.add_node(n1)
        >>> g.add_node(n2)
        >>> g.add_edge(Edge(n1, n2))
        >>> g.edge_count()
        1

        Notes
        -----
        Time complexity: O(1)
        """
        return len(self._edges)

    def is_connected(self) -> bool:
        """Check if the graph is connected.

        A graph is connected if there is a path between any two nodes.

        Returns
        -------
        bool
            True if graph is connected, False otherwise.
            Empty graph is considered connected.

        Examples
        --------
        >>> g = Graph()
        >>> g.is_connected()  # Empty graph
        True

        >>> n1 = GraphNode("A", "n1")
        >>> g.add_node(n1)
        >>> g.is_connected()  # Single node
        True

        >>> n2 = GraphNode("B", "n2")
        >>> g.add_node(n2)
        >>> g.is_connected()  # Two isolated nodes
        False

        >>> g.add_edge(Edge(n1, n2))
        >>> g.is_connected()  # Connected
        True

        Notes
        -----
        Time complexity: O(V + E) with caching.
        Uses BFS to check connectivity.
        Result is cached until graph structure changes.
        """
        if self._cache_valid and self._connectivity_cache is not None:
            return self._connectivity_cache

        result = self._check_connectivity_bfs()
        self._connectivity_cache = result
        self._cache_valid = True
        return result

    def _check_connectivity_bfs(self) -> bool:
        """Check connectivity using BFS.

        Returns
        -------
        bool
            True if connected.
        """
        if self.is_empty():
            return True

        if self.node_count() == 1:
            return True

        # Start BFS from first node
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

        # Graph is connected if all nodes were visited
        return len(visited) == self.node_count()

    def get_node_by_id(self, node_id: str) -> Optional[GraphNode]:
        """Get a node by its ID.

        Parameters
        ----------
        node_id : str
            ID of the node to retrieve.

        Returns
        -------
        GraphNode or None
            The node if found, None otherwise.

        Examples
        --------
        >>> g = Graph()
        >>> n1 = GraphNode("A", "n1")
        >>> g.add_node(n1)
        >>> found = g.get_node_by_id("n1")
        >>> found.data
        'A'
        >>> g.get_node_by_id("n999") is None
        True

        Notes
        -----
        Time complexity: O(1)
        """
        return self._nodes.get(node_id)

    def is_empty(self) -> bool:
        """Check if the graph is empty (no nodes).

        Returns
        -------
        bool
            True if graph has no nodes.

        Examples
        --------
        >>> g = Graph()
        >>> g.is_empty()
        True
        >>> g.add_node(GraphNode("A", "n1"))
        >>> g.is_empty()
        False

        Notes
        -----
        Time complexity: O(1)
        """
        return len(self._nodes) == 0

    def clear(self) -> None:
        """Remove all nodes and edges from the graph.

        Examples
        --------
        >>> g = Graph()
        >>> n1 = GraphNode("A", "n1")
        >>> g.add_node(n1)
        >>> g.clear()
        >>> g.is_empty()
        True

        Notes
        -----
        Time complexity: O(1)
        """
        self._nodes.clear()
        self._adjacency.clear()
        self._edges.clear()
        self._invalidate_cache()

    def __len__(self) -> int:
        """Return the number of nodes in the graph.

        Returns
        -------
        int
            Number of nodes.

        Examples
        --------
        >>> g = Graph()
        >>> len(g)
        0
        >>> g.add_node(GraphNode("A", "n1"))
        >>> len(g)
        1
        """
        return self.node_count()

    def __contains__(self, item: GraphNode) -> bool:
        """Check if node is in the graph.

        Parameters
        ----------
        node : GraphNode
            Node to check.

        Returns
        -------
        bool
            True if node is in the graph.

        Examples
        --------
        >>> g = Graph()
        >>> n1 = GraphNode("A", "n1")
        >>> n1 in g
        False
        >>> g.add_node(n1)
        >>> n1 in g
        True
        """
        return self.has_node(item)

    def __iter__(self) -> Iterator[GraphNode]:
        """Iterate over nodes in the graph.

        Yields
        ------
        GraphNode
            All nodes in the graph.

        Examples
        --------
        >>> g = Graph()
        >>> g.add_node(GraphNode("A", "n1"))
        >>> g.add_node(GraphNode("B", "n2"))
        >>> sorted([n.id for n in g])
        ['n1', 'n2']
        """
        return self.nodes()

    def __repr__(self) -> str:
        """Return detailed string representation.

        Returns
        -------
        str
            String representation.

        Examples
        --------
        >>> g = Graph()
        >>> repr(g)
        'Graph(nodes=0, edges=0, multi_edges=False)'
        """
        return (
            f"Graph(nodes={self.node_count()}, edges={self.edge_count()}, "
            f"multi_edges={self._allow_multi_edges})"
        )

    def __str__(self) -> str:
        """Return simple string representation.

        Returns
        -------
        str
            String representation.

        Examples
        --------
        >>> g = Graph()
        >>> str(g)
        'Graph: 0 nodes, 0 edges'
        """
        return f"Graph: {self.node_count()} nodes, {self.edge_count()} edges"
