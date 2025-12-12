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

"""Directed and undirected graph implementations.

This module provides graph implementations focused on edge directionality:
- DirectedGraph: edges have explicit direction (source → target)
- UndirectedGraph: edges are bidirectional with strict validation

Both classes handle unweighted graphs. For weighted versions, see weighted.py.

Classes
-------
DirectedGraph
    Directed graph with separate in/out adjacency lists.
UndirectedGraph
    Undirected graph that explicitly rejects directed edges.

Examples
--------
Create a directed graph:

>>> from sds.graph import DirectedGraph, GraphNode, DirectedEdge
>>> g = DirectedGraph()
>>> n1 = GraphNode("A", "n1")
>>> n2 = GraphNode("B", "n2")
>>> g.add_node(n1)
>>> g.add_node(n2)
>>> g.add_edge(DirectedEdge(n1, n2))
>>> g.has_edge(n1, n2)
True
>>> g.has_edge(n2, n1)  # Direction matters!
False

Create an undirected graph with validation:

>>> from sds.graph import UndirectedGraph, Edge
>>> g = UndirectedGraph()
>>> g.add_node(n1)
>>> g.add_node(n2)
>>> g.add_edge(Edge(n1, n2))
>>> g.has_edge(n1, n2) and g.has_edge(n2, n1)  # Bidirectional
True

Directed edges are rejected in UndirectedGraph:

>>> g.add_edge(DirectedEdge(n1, n2))
Traceback (most recent call last):
    ...
TypeError: UndirectedGraph requires undirected Edge, not DirectedEdge

Notes
-----
DirectedGraph uses two adjacency lists for efficient in/out degree queries.
UndirectedGraph is a validated wrapper around Graph from graph.py.

For weighted graphs, see:
- WeightedGraph: undirected with weights
- WeightedDirectedGraph: directed with weights

See Also
--------
sds.graphs.graph : Base Graph class (unweighted, undirected).
sds.graphs.weighted : Weighted graph implementations.
"""

from collections import deque
from typing import Dict, Iterator, List, Optional, Set

from .edge import DirectedEdge, Edge
from .graph import Graph
from .interfaces import AbstractDirectedGraph
from .node import GraphNode

__all__ = ["DirectedGraph", "UndirectedGraph"]


class DirectedGraph(AbstractDirectedGraph):
    """Directed graph using adjacency list representation.

    A directed graph has edges with explicit direction from source to target.
    This implementation maintains separate adjacency lists for incoming and
    outgoing edges for efficient degree queries.

    Parameters
    ----------
    allow_multi_edges : bool, optional
        If True, allows multiple edges from same source to same target.
        Default is False (simple directed graph).

    Attributes
    ----------
    allow_multi_edges : bool
        Whether multiple edges are allowed (read-only property).

    Examples
    --------
    Create a simple directed graph:

    >>> g = DirectedGraph()
    >>> n1 = GraphNode("A", "n1")
    >>> n2 = GraphNode("B", "n2")
    >>> g.add_node(n1)
    >>> g.add_node(n2)
    >>> g.add_edge(DirectedEdge(n1, n2))
    >>> g.out_degree(n1)
    1
    >>> g.in_degree(n1)
    0

    Create a multi-digraph:

    >>> mg = DirectedGraph(allow_multi_edges=True)
    >>> mg.add_node(n1)
    >>> mg.add_node(n2)
    >>> mg.add_edge(DirectedEdge(n1, n2, data="edge1"))
    >>> mg.add_edge(DirectedEdge(n1, n2, data="edge2"))
    >>> mg.edge_count()
    2

    Check for cycles:

    >>> g.add_node(GraphNode("C", "n3"))
    >>> g.add_edge(DirectedEdge(n2, GraphNode("C", "n3")))
    >>> g.is_acyclic()
    True

    Notes
    -----
    Time Complexity:
    - add_node: O(1)
    - remove_node: O(in_degree + out_degree + E)
    - add_edge: O(1) or O(out_degree) if checking duplicates
    - in_degree/out_degree: O(1) amortized
    - predecessors/successors: O(degree)
    - is_acyclic: O(V + E) with caching

    Space Complexity: O(V + E)

    See Also
    --------
    Graph : For undirected graphs.
    AbstractDirectedGraph : Interface definition.
    """

    def __init__(self, allow_multi_edges: bool = False) -> None:
        """Initialize an empty directed graph.

        Parameters
        ----------
        allow_multi_edges : bool, optional
            Allow multiple edges between same source/target. Default is False.

        Examples
        --------
        >>> g = DirectedGraph()
        >>> g.is_empty()
        True

        >>> mg = DirectedGraph(allow_multi_edges=True)
        >>> mg.allow_multi_edges
        True
        """
        super().__init__()
        self._allow_multi_edges = allow_multi_edges
        self._nodes: Dict[str, GraphNode] = {}

        # Separate adjacency lists for in and out edges
        self._out_adjacency: Dict[str, Set[str]] = {}  # source -> targets
        self._in_adjacency: Dict[str, Set[str]] = {}  # target -> sources

        self._edges: List[DirectedEdge] = []

        # Caching for expensive operations
        self._connectivity_cache: Optional[bool] = None
        self._acyclic_cache: Optional[bool] = None
        self._cache_valid = False

    @property
    def allow_multi_edges(self) -> bool:
        """Check if multi-digraph mode is enabled.

        Returns
        -------
        bool
            True if multiple edges are allowed.

        Examples
        --------
        >>> g = DirectedGraph()
        >>> g.allow_multi_edges
        False
        """
        return self._allow_multi_edges

    def _invalidate_cache(self) -> None:
        """Invalidate cached properties after graph modification."""
        self._connectivity_cache = None
        self._acyclic_cache = None
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
        >>> g = DirectedGraph()
        >>> n1 = GraphNode("A", "n1")
        >>> g.add_node(n1)
        >>> g.has_node(n1)
        True

        Notes
        -----
        Time complexity: O(1)
        """
        if not isinstance(node, GraphNode):
            raise TypeError(f"Expected GraphNode, got {type(node).__name__}")

        if node.id in self._nodes:
            raise ValueError(f"Node {node.id} already exists in graph")

        self._nodes[node.id] = node
        self._out_adjacency[node.id] = set()
        self._in_adjacency[node.id] = set()
        self._invalidate_cache()

    def remove_node(self, node: GraphNode) -> None:
        """Remove a node and all its incident edges.

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
        >>> g = DirectedGraph()
        >>> n1 = GraphNode("A", "n1")
        >>> n2 = GraphNode("B", "n2")
        >>> g.add_node(n1)
        >>> g.add_node(n2)
        >>> g.add_edge(DirectedEdge(n1, n2))
        >>> g.remove_node(n1)
        >>> g.edge_count()
        0

        Notes
        -----
        Time complexity: O(in_degree + out_degree + E)
        """
        if node.id not in self._nodes:
            raise ValueError(f"Node {node.id} not in graph")

        # Remove all edges involving this node
        self._edges = [
            e for e in self._edges if e.source.id != node.id and e.target.id != node.id
        ]

        # Update adjacency lists for neighbors
        for source_id in self._in_adjacency[node.id]:
            self._out_adjacency[source_id].discard(node.id)

        for target_id in self._out_adjacency[node.id]:
            self._in_adjacency[target_id].discard(node.id)

        # Remove node
        del self._nodes[node.id]
        del self._out_adjacency[node.id]
        del self._in_adjacency[node.id]
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
        >>> g = DirectedGraph()
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

    def add_edge(self, edge: DirectedEdge) -> None:  # type: ignore[override]
        """Add a directed edge to the graph.

        Parameters
        ----------
        edge : DirectedEdge
            Directed edge to add.

        Raises
        ------
        TypeError
            If edge is not a DirectedEdge.
        ValueError
            If source or target node is not in graph, or if edge already
            exists in simple directed graph.

        Examples
        --------
        >>> g = DirectedGraph()
        >>> n1 = GraphNode("A", "n1")
        >>> n2 = GraphNode("B", "n2")
        >>> g.add_node(n1)
        >>> g.add_node(n2)
        >>> g.add_edge(DirectedEdge(n1, n2))
        >>> g.has_edge(n1, n2)
        True
        >>> g.has_edge(n2, n1)
        False

        Notes
        -----
        Time complexity: O(1) for multi-digraph, O(out_degree) for simple.
        """
        if not isinstance(edge, DirectedEdge):
            raise TypeError(f"Expected DirectedEdge, got {type(edge).__name__}")

        # Validate nodes exist
        if not self.has_node(edge.source):
            raise ValueError(f"Source node {edge.source.id} not in graph")
        if not self.has_node(edge.target):
            raise ValueError(f"Target node {edge.target.id} not in graph")

        # Check for duplicate edges in simple graph
        if not self._allow_multi_edges and self.has_edge(edge.source, edge.target):
            raise ValueError(
                f"Edge from {edge.source.id} to {edge.target.id} already exists. "
                "Use allow_multi_edges=True for multi-digraph."
            )

        # Add edge
        self._edges.append(edge)

        # Update adjacency lists
        self._out_adjacency[edge.source.id].add(edge.target.id)
        self._in_adjacency[edge.target.id].add(edge.source.id)

        self._invalidate_cache()

    def remove_edge(self, edge: Edge) -> None:
        """Remove a directed edge from the graph.

        Parameters
        ----------
        edge : Edge
            Edge to remove (must be DirectedEdge for proper direction).

        Raises
        ------
        ValueError
            If edge is not in the graph.

        Examples
        --------
        >>> g = DirectedGraph()
        >>> n1 = GraphNode("A", "n1")
        >>> n2 = GraphNode("B", "n2")
        >>> g.add_node(n1)
        >>> g.add_node(n2)
        >>> e = DirectedEdge(n1, n2)
        >>> g.add_edge(e)
        >>> g.remove_edge(e)
        >>> g.has_edge(n1, n2)
        False

        Notes
        -----
        Time complexity: O(E) to find edge, O(1) to update adjacency.
        """
        # Check membership against directed edges list
        if edge not in self._edges:
            # If the provided edge is not a DirectedEdge, try to locate the
            # corresponding directed edge instance before failing.
            if isinstance(edge, DirectedEdge):
                raise ValueError(
                    f"Edge from {edge.node1.id} to {edge.node2.id} not in graph"
                )
            match = next(
                (
                    e
                    for e in self._edges
                    if e.source.id == edge.node1.id and e.target.id == edge.node2.id
                ),
                None,
            )
            if match is None:
                raise ValueError(
                    f"Edge from {edge.node1.id} to {edge.node2.id} not in graph"
                )
            # Remove the matched directed edge
            self._edges.remove(match)
            source_id = match.source.id
            target_id = match.target.id
        else:
            # Safe remove only when the exact DirectedEdge object is present
            # in the underlying List[DirectedEdge]
            if isinstance(edge, DirectedEdge):
                self._edges.remove(edge)
                source_id = edge.source.id
                target_id = edge.target.id
            else:
                # Edge is undirected but equals() succeeded against DirectedEdge
                # list membership check above (unlikely since __eq__ is class-specific),
                # still resolve ids from undirected view.
                # Fallback to remove by identity via a search
                match = next(
                    (
                        e
                        for e in self._edges
                        if e.source.id == edge.node1.id and e.target.id == edge.node2.id
                    ),
                    None,
                )
                if match is not None:
                    self._edges.remove(match)
                    source_id = match.source.id
                    target_id = match.target.id
                else:
                    # Should not happen after membership check, but keep safe
                    raise ValueError(
                        f"Edge from {edge.node1.id} to {edge.node2.id} not in graph"
                    )

        has_other_edge = any(
            isinstance(e, DirectedEdge)
            and e.source.id == source_id
            and e.target.id == target_id
            for e in self._edges
        )

        if not has_other_edge:
            self._out_adjacency[source_id].discard(target_id)
            self._in_adjacency[target_id].discard(source_id)

        self._invalidate_cache()

    def has_edge(self, node1: GraphNode, node2: GraphNode) -> bool:
        """Check if a directed edge exists from node1 to node2.

        Parameters
        ----------
        node1 : GraphNode
            Source node.
        node2 : GraphNode
            Target node.

        Returns
        -------
        bool
            True if edge from node1 to node2 exists.

        Examples
        --------
        >>> g = DirectedGraph()
        >>> n1 = GraphNode("A", "n1")
        >>> n2 = GraphNode("B", "n2")
        >>> g.add_node(n1)
        >>> g.add_node(n2)
        >>> g.add_edge(DirectedEdge(n1, n2))
        >>> g.has_edge(n1, n2)
        True
        >>> g.has_edge(n2, n1)  # Direction matters
        False

        Notes
        -----
        Time complexity: O(1) amortized using adjacency set.
        """
        if not self.has_node(node1) or not self.has_node(node2):
            return False
        return node2.id in self._out_adjacency[node1.id]

    def get_edge(self, node1: GraphNode, node2: GraphNode) -> Optional[Edge]:
        """Get the directed edge from node1 to node2.

        Parameters
        ----------
        node1 : GraphNode
            Source node.
        node2 : GraphNode
            Target node.

        Returns
        -------
        Edge or None
            The directed edge if it exists, None otherwise.
            For multi-digraphs, returns first edge found.

        Examples
        --------
        >>> g = DirectedGraph()
        >>> n1 = GraphNode("A", "n1")
        >>> n2 = GraphNode("B", "n2")
        >>> g.add_node(n1)
        >>> g.add_node(n2)
        >>> e = DirectedEdge(n1, n2, data="test")
        >>> g.add_edge(e)
        >>> found = g.get_edge(n1, n2)
        >>> found.data
        'test'

        Notes
        -----
        Time complexity: O(E) in worst case.
        """
        for edge in self._edges:
            if isinstance(edge, DirectedEdge):
                if edge.source.id == node1.id and edge.target.id == node2.id:
                    return edge
        return None

    def neighbors(self, node: GraphNode) -> Iterator[GraphNode]:
        """Get all successors (outgoing neighbors) of a node.

        For directed graphs, neighbors() returns successors by convention.

        Parameters
        ----------
        node : GraphNode
            Node to get neighbors for.

        Yields
        ------
        GraphNode
            Successor nodes.

        Raises
        ------
        ValueError
            If node is not in the graph.

        Examples
        --------
        >>> g = DirectedGraph()
        >>> n1 = GraphNode("A", "n1")
        >>> n2 = GraphNode("B", "n2")
        >>> n3 = GraphNode("C", "n3")
        >>> g.add_node(n1)
        >>> g.add_node(n2)
        >>> g.add_node(n3)
        >>> g.add_edge(DirectedEdge(n1, n2))
        >>> g.add_edge(DirectedEdge(n1, n3))
        >>> sorted([n.id for n in g.neighbors(n1)])
        ['n2', 'n3']

        Notes
        -----
        Time complexity: O(out_degree(node))
        neighbors() is equivalent to successors() for directed graphs.
        """
        return self.successors(node)

    def degree(self, node: GraphNode) -> int:
        """Get total degree of a node (in-degree + out-degree).

        Parameters
        ----------
        node : GraphNode
            Node to get degree for.

        Returns
        -------
        int
            Total degree (number of incoming + outgoing edges).

        Raises
        ------
        ValueError
            If node is not in the graph.

        Examples
        --------
        >>> g = DirectedGraph()
        >>> n1 = GraphNode("A", "n1")
        >>> n2 = GraphNode("B", "n2")
        >>> g.add_node(n1)
        >>> g.add_node(n2)
        >>> g.add_edge(DirectedEdge(n1, n2))
        >>> g.degree(n1)  # 0 in + 1 out
        1
        >>> g.degree(n2)  # 1 in + 0 out
        1

        Notes
        -----
        Time complexity: O(1) amortized.
        For multi-digraphs, counts each edge separately.
        """
        if not self.has_node(node):
            raise ValueError(f"Node {node.id} not in graph")

        if not self._allow_multi_edges:
            return len(self._in_adjacency[node.id]) + len(self._out_adjacency[node.id])
        else:
            # For multi-digraphs, count actual edges
            return sum(
                1
                for e in self._edges
                if isinstance(e, DirectedEdge)
                and (e.source.id == node.id or e.target.id == node.id)
            )

    def in_degree(self, node: GraphNode) -> int:
        """Get in-degree of a node (number of incoming edges).

        Parameters
        ----------
        node : GraphNode
            Node to get in-degree for.

        Returns
        -------
        int
            Number of edges pointing to this node.

        Raises
        ------
        ValueError
            If node is not in the graph.

        Examples
        --------
        >>> g = DirectedGraph()
        >>> n1 = GraphNode("A", "n1")
        >>> n2 = GraphNode("B", "n2")
        >>> g.add_node(n1)
        >>> g.add_node(n2)
        >>> g.add_edge(DirectedEdge(n1, n2))
        >>> g.in_degree(n2)
        1
        >>> g.in_degree(n1)
        0

        Notes
        -----
        Time complexity: O(1) amortized.
        """
        if not self.has_node(node):
            raise ValueError(f"Node {node.id} not in graph")

        if not self._allow_multi_edges:
            return len(self._in_adjacency[node.id])
        else:
            # For multi-digraphs, count actual edges
            return sum(
                1
                for e in self._edges
                if isinstance(e, DirectedEdge) and e.target.id == node.id
            )

    def out_degree(self, node: GraphNode) -> int:
        """Get out-degree of a node (number of outgoing edges).

        Parameters
        ----------
        node : GraphNode
            Node to get out-degree for.

        Returns
        -------
        int
            Number of edges from this node.

        Raises
        ------
        ValueError
            If node is not in the graph.

        Examples
        --------
        >>> g = DirectedGraph()
        >>> n1 = GraphNode("A", "n1")
        >>> n2 = GraphNode("B", "n2")
        >>> g.add_node(n1)
        >>> g.add_node(n2)
        >>> g.add_edge(DirectedEdge(n1, n2))
        >>> g.out_degree(n1)
        1
        >>> g.out_degree(n2)
        0

        Notes
        -----
        Time complexity: O(1) amortized.
        """
        if not self.has_node(node):
            raise ValueError(f"Node {node.id} not in graph")

        if not self._allow_multi_edges:
            return len(self._out_adjacency[node.id])
        else:
            # For multi-digraphs, count actual edges
            return sum(
                1
                for e in self._edges
                if isinstance(e, DirectedEdge) and e.source.id == node.id
            )

    def predecessors(self, node: GraphNode) -> Iterator[GraphNode]:
        """Get all predecessors (nodes with edges to this node).

        Parameters
        ----------
        node : GraphNode
            Node to get predecessors for.

        Yields
        ------
        GraphNode
            Predecessor nodes.

        Raises
        ------
        ValueError
            If node is not in the graph.

        Examples
        --------
        >>> g = DirectedGraph()
        >>> n1 = GraphNode("A", "n1")
        >>> n2 = GraphNode("B", "n2")
        >>> n3 = GraphNode("C", "n3")
        >>> g.add_node(n1)
        >>> g.add_node(n2)
        >>> g.add_node(n3)
        >>> g.add_edge(DirectedEdge(n1, n3))
        >>> g.add_edge(DirectedEdge(n2, n3))
        >>> sorted([n.id for n in g.predecessors(n3)])
        ['n1', 'n2']

        Notes
        -----
        Time complexity: O(in_degree(node))
        """
        if not self.has_node(node):
            raise ValueError(f"Node {node.id} not in graph")

        for predecessor_id in self._in_adjacency[node.id]:
            yield self._nodes[predecessor_id]

    def successors(self, node: GraphNode) -> Iterator[GraphNode]:
        """Get all successors (nodes with edges from this node).

        Parameters
        ----------
        node : GraphNode
            Node to get successors for.

        Yields
        ------
        GraphNode
            Successor nodes.

        Raises
        ------
        ValueError
            If node is not in the graph.

        Examples
        --------
        >>> g = DirectedGraph()
        >>> n1 = GraphNode("A", "n1")
        >>> n2 = GraphNode("B", "n2")
        >>> n3 = GraphNode("C", "n3")
        >>> g.add_node(n1)
        >>> g.add_node(n2)
        >>> g.add_node(n3)
        >>> g.add_edge(DirectedEdge(n1, n2))
        >>> g.add_edge(DirectedEdge(n1, n3))
        >>> sorted([n.id for n in g.successors(n1)])
        ['n2', 'n3']

        Notes
        -----
        Time complexity: O(out_degree(node))
        """
        if not self.has_node(node):
            raise ValueError(f"Node {node.id} not in graph")

        for successor_id in self._out_adjacency[node.id]:
            yield self._nodes[successor_id]

    def is_acyclic(self) -> bool:
        """Check if the graph is acyclic (DAG).

        Returns
        -------
        bool
            True if graph has no cycles (is a DAG).

        Examples
        --------
        >>> g = DirectedGraph()
        >>> nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        >>> for n in nodes:
        ...     g.add_node(n)
        >>> g.add_edge(DirectedEdge(nodes[0], nodes[1]))
        >>> g.add_edge(DirectedEdge(nodes[1], nodes[2]))
        >>> g.is_acyclic()
        True

        Add cycle:

        >>> g.add_edge(DirectedEdge(nodes[2], nodes[0]))
        >>> g.is_acyclic()
        False

        Notes
        -----
        Time complexity: O(V + E) with caching.
        Uses DFS with coloring to detect back edges.
        """
        if self._cache_valid and self._acyclic_cache is not None:
            return self._acyclic_cache

        result = self._check_acyclic_dfs()
        self._acyclic_cache = result
        self._cache_valid = True
        return result

    def _check_acyclic_dfs(self) -> bool:
        """Check if graph is acyclic using DFS with coloring.

        Returns
        -------
        bool
            True if acyclic (no back edges found).
        """
        # Color states: 0=white (unvisited), 1=gray (visiting), 2=black (done)
        color: Dict[str, int] = {node_id: 0 for node_id in self._nodes}

        def has_cycle_from(node_id: str) -> bool:
            """DFS to detect cycle from node."""
            color[node_id] = 1  # Mark as visiting (gray)

            for successor_id in self._out_adjacency[node_id]:
                if color[successor_id] == 1:  # Back edge found!
                    return True
                if color[successor_id] == 0:  # Unvisited
                    if has_cycle_from(successor_id):
                        return True

            color[node_id] = 2  # Mark as done (black)
            return False

        # Check all components
        for node_id in self._nodes:
            if color[node_id] == 0:
                if has_cycle_from(node_id):
                    return False  # Cycle found

        return True  # No cycles

    def nodes(self) -> Iterator[GraphNode]:
        """Get all nodes in the graph.

        Yields
        ------
        GraphNode
            All nodes in the graph.

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
            All directed edges in the graph.

        Notes
        -----
        Time complexity: O(E)
        """
        yield from self._edges

    def node_count(self) -> int:
        """Get the number of nodes.

        Returns
        -------
        int
            Number of nodes.

        Notes
        -----
        Time complexity: O(1)
        """
        return len(self._nodes)

    def edge_count(self) -> int:
        """Get the number of edges.

        Returns
        -------
        int
            Number of directed edges.

        Notes
        -----
        Time complexity: O(1)
        """
        return len(self._edges)

    def is_connected(self) -> bool:
        """Check if the graph is weakly connected.

        A directed graph is weakly connected if replacing all directed edges
        with undirected edges results in a connected graph.

        Returns
        -------
        bool
            True if weakly connected.

        Examples
        --------
        >>> g = DirectedGraph()
        >>> nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        >>> for n in nodes:
        ...     g.add_node(n)
        >>> g.add_edge(DirectedEdge(nodes[0], nodes[1]))
        >>> g.add_edge(DirectedEdge(nodes[1], nodes[2]))
        >>> g.is_connected()
        True

        Notes
        -----
        Time complexity: O(V + E) with caching.
        Uses BFS treating edges as undirected.
        """
        if self._cache_valid and self._connectivity_cache is not None:
            return self._connectivity_cache

        result = self._check_weak_connectivity()
        self._connectivity_cache = result
        self._cache_valid = True
        return result

    def _check_weak_connectivity(self) -> bool:
        """Check weak connectivity using BFS.

        Returns
        -------
        bool
            True if weakly connected.
        """
        if self.is_empty() or self.node_count() == 1:
            return True

        # Start from first node
        start_node = next(iter(self._nodes.values()))
        visited: Set[str] = set()
        queue: deque[GraphNode] = deque([start_node])
        visited.add(start_node.id)

        while queue:
            current = queue.popleft()

            # Visit both successors and predecessors (treat as undirected)
            for neighbor in self.successors(current):
                if neighbor.id not in visited:
                    visited.add(neighbor.id)
                    queue.append(neighbor)

            for neighbor in self.predecessors(current):
                if neighbor.id not in visited:
                    visited.add(neighbor.id)
                    queue.append(neighbor)

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

        Notes
        -----
        Time complexity: O(1)
        """
        return self._nodes.get(node_id)

    def is_empty(self) -> bool:
        """Check if the graph is empty.

        Returns
        -------
        bool
            True if graph has no nodes.

        Notes
        -----
        Time complexity: O(1)
        """
        return len(self._nodes) == 0

    def clear(self) -> None:
        """Remove all nodes and edges.

        Notes
        -----
        Time complexity: O(1)
        """
        self._nodes.clear()
        self._out_adjacency.clear()
        self._in_adjacency.clear()
        self._edges.clear()
        self._invalidate_cache()

    def __len__(self) -> int:
        """Return the number of nodes.

        Returns
        -------
        int
            Number of nodes.
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
        """
        return self.has_node(item)

    def __iter__(self) -> Iterator[GraphNode]:
        """Iterate over nodes in the graph.

        Yields
        ------
        GraphNode
            All nodes in the graph.
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
        >>> g = DirectedGraph()
        >>> repr(g)
        'DirectedGraph(nodes=0, edges=0, multi_edges=False)'
        """
        return (
            f"DirectedGraph(nodes={self.node_count()}, edges={self.edge_count()}, "
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
        >>> g = DirectedGraph()
        >>> str(g)
        'DirectedGraph: 0 nodes, 0 edges'
        """
        return f"DirectedGraph: {self.node_count()} nodes, {self.edge_count()} edges"


class UndirectedGraph(Graph):
    """Undirected graph with explicit edge type validation.

    This class extends Graph to explicitly validate that only undirected
    edges (Edge instances, not DirectedEdge) are added. While Graph also
    works with undirected edges, UndirectedGraph makes this requirement
    explicit and enforces it through type checking.

    Parameters
    ----------
    allow_multi_edges : bool, optional
        If True, allows multiple edges between the same pair of nodes.
        Default is False.

    Attributes
    ----------
    allow_multi_edges : bool
        Whether multiple edges are allowed (read-only property).

    Examples
    --------
    Create and use an undirected graph:

    >>> g = UndirectedGraph()
    >>> n1 = GraphNode("A", "n1")
    >>> n2 = GraphNode("B", "n2")
    >>> g.add_node(n1)
    >>> g.add_node(n2)
    >>> g.add_edge(Edge(n1, n2))
    >>> g.has_edge(n1, n2)
    True
    >>> g.has_edge(n2, n1)  # Bidirectional
    True

    Directed edges are rejected:

    >>> g.add_edge(DirectedEdge(n1, n2))
    Traceback (most recent call last):
        ...
    TypeError: UndirectedGraph requires undirected Edge, not DirectedEdge

    Multi-edges supported:

    >>> mg = UndirectedGraph(allow_multi_edges=True)
    >>> mg.add_node(n1)
    >>> mg.add_node(n2)
    >>> mg.add_edge(Edge(n1, n2, data="edge1"))
    >>> mg.add_edge(Edge(n1, n2, data="edge2"))
    >>> mg.edge_count()
    2

    Notes
    -----
    UndirectedGraph inherits all functionality from Graph and adds only
    edge type validation. All operations (add_node, remove_node, neighbors,
    degree, is_connected, etc.) work identically to Graph.

    Time and space complexity are identical to Graph:
    - add_edge: O(1) for multigraph, O(degree) for simple graph
    - All other operations: same as Graph

    The main benefit is semantic clarity and type safety: using
    UndirectedGraph makes it explicit that the graph must be undirected.

    See Also
    --------
    Graph : Base implementation without explicit edge type checking.
    DirectedGraph : For graphs with directed edges.
    WeightedGraph : For weighted undirected graphs.
    """

    def __init__(self, allow_multi_edges: bool = False) -> None:
        """Initialize an empty undirected graph.

        Parameters
        ----------
        allow_multi_edges : bool, optional
            Allow multiple edges between same nodes. Default is False.

        Examples
        --------
        >>> g = UndirectedGraph()
        >>> g.is_empty()
        True

        >>> mg = UndirectedGraph(allow_multi_edges=True)
        >>> mg.allow_multi_edges
        True
        """
        super().__init__(allow_multi_edges=allow_multi_edges)

    def add_edge(self, edge: Edge) -> None:
        """Add an undirected edge to the graph.

        Parameters
        ----------
        edge : Edge
            Undirected edge to add. Must be Edge, not DirectedEdge.

        Raises
        ------
        TypeError
            If edge is a DirectedEdge or not an Edge instance.
        ValueError
            If either node is not in the graph, or if edge already exists
            and multigraph mode is disabled.

        Examples
        --------
        >>> g = UndirectedGraph()
        >>> n1 = GraphNode("A", "n1")
        >>> n2 = GraphNode("B", "n2")
        >>> g.add_node(n1)
        >>> g.add_node(n2)
        >>> g.add_edge(Edge(n1, n2))
        >>> g.has_edge(n1, n2)
        True

        Directed edges are rejected:

        >>> g.add_edge(DirectedEdge(n1, n2))
        Traceback (most recent call last):
            ...
        TypeError: UndirectedGraph requires undirected Edge, not DirectedEdge

        Notes
        -----
        Time complexity: O(1) for multigraph, O(degree(node)) for simple graph.

        This method overrides Graph.add_edge() to add explicit type checking
        that rejects DirectedEdge instances.
        """
        # Check if it's a DirectedEdge (which is a subclass of Edge)
        if isinstance(edge, DirectedEdge):
            raise TypeError(
                f"UndirectedGraph requires undirected Edge, not {type(edge).__name__}"
            )

        # Delegate to parent class for actual addition
        super().add_edge(edge)

    def __repr__(self) -> str:
        """Return detailed string representation.

        Returns
        -------
        str
            String representation.

        Examples
        --------
        >>> g = UndirectedGraph()
        >>> repr(g)
        'UndirectedGraph(nodes=0, edges=0, multi_edges=False)'
        """
        return (
            f"UndirectedGraph(nodes={self.node_count()}, "
            f"edges={self.edge_count()}, multi_edges={self._allow_multi_edges})"
        )

    def __str__(self) -> str:
        """Return simple string representation.

        Returns
        -------
        str
            String representation.

        Examples
        --------
        >>> g = UndirectedGraph()
        >>> str(g)
        'UndirectedGraph: 0 nodes, 0 edges'
        """
        return f"UndirectedGraph: {self.node_count()} nodes, {self.edge_count()} edges"
