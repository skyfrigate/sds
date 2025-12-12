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

"""Weighted graph implementations.

This module provides graph implementations with numeric edge weights:
- WeightedGraph: undirected graph with weighted edges
- WeightedDirectedGraph: directed graph with weighted edges

Classes
-------
WeightedGraph
    Undirected weighted graph.
WeightedDirectedGraph
    Directed graph with weighted edges.

Examples
--------
Create a weighted undirected graph:

>>> from sds.graph.weighted import WeightedGraph, GraphNode, WeightedEdge
>>> g = WeightedGraph()
>>> n1 = GraphNode("A", "n1")
>>> n2 = GraphNode("B", "n2")
>>> g.add_node(n1)
>>> g.add_node(n2)
>>> g.add_edge(WeightedEdge(n1, n2, weight=10.0))
>>> g.get_edge_weight(n1, n2)
10.0

Create a weighted directed graph:

>>> from sds.graph.weighted import WeightedDirectedGraph, WeightedDirectedEdge
>>> dg = WeightedDirectedGraph()
>>> dg.add_node(n1)
>>> dg.add_node(n2)
>>> dg.add_edge(WeightedDirectedEdge(n1, n2, weight=5.0))
>>> dg.get_edge_weight(n1, n2)
5.0
>>> dg.in_degree(n2)
1

Notes
-----
Both classes support multi-edges via allow_multi_edges parameter.
Weights must be numeric (int or float).

See Also
--------
sds.graph.graph : Base unweighted graph.
sds.graph.directed : Unweighted directed/undirected graphs.
"""

from collections import deque
from typing import Dict, Iterator, List, Optional, Set

from .edge import DirectedEdge, WeightedDirectedEdge, WeightedEdge
from .interfaces import AbstractDirectedGraph, AbstractWeightedGraph
from .node import GraphNode

__all__ = ["WeightedGraph", "WeightedDirectedGraph"]


class WeightedGraph(AbstractWeightedGraph):
    """Weighted undirected graph implementation.

    A weighted graph where each edge has a numeric weight. The graph
    maintains both the graph structure and edge weights efficiently.

    Parameters
    ----------
    allow_multi_edges : bool, optional
        If True, allows multiple weighted edges between same nodes.
        Default is False.

    Attributes
    ----------
    allow_multi_edges : bool
        Whether multiple edges are allowed (read-only property).

    See Also
    --------
    WeightedDirectedGraph : For directed weighted graphs.
    Graph : For unweighted graphs.
    """

    def __init__(self, allow_multi_edges: bool = False) -> None:
        """Initialize an empty weighted graph."""
        super().__init__()
        self._allow_multi_edges = allow_multi_edges
        self._nodes: Dict[str, GraphNode] = {}
        self._adjacency: Dict[str, Set[str]] = {}
        self._edges: List[WeightedEdge] = []
        self._connectivity_cache: Optional[bool] = None
        self._total_weight_cache: Optional[float] = None
        self._cache_valid = False

    @property
    def allow_multi_edges(self) -> bool:
        """Check if multi-graph mode is enabled."""
        return self._allow_multi_edges

    def _invalidate_cache(self) -> None:
        """Invalidate cached properties."""
        self._connectivity_cache = None
        self._total_weight_cache = None
        self._cache_valid = False

    def add_node(self, node: GraphNode) -> None:
        """Add a node to the graph."""
        if not isinstance(node, GraphNode):
            raise TypeError(f"Expected GraphNode, got {type(node).__name__}")
        if node.id in self._nodes:
            raise ValueError(f"Node {node.id} already exists in graph")
        self._nodes[node.id] = node
        self._adjacency[node.id] = set()
        self._invalidate_cache()

    def remove_node(self, node: GraphNode) -> None:
        """Remove a node and all its incident edges."""
        if node.id not in self._nodes:
            raise ValueError(f"Node {node.id} not in graph")
        self._edges = [e for e in self._edges if not e.incident_to(node)]
        neighbors = self._adjacency[node.id].copy()
        for neighbor_id in neighbors:
            self._adjacency[neighbor_id].discard(node.id)
        del self._nodes[node.id]
        del self._adjacency[node.id]
        self._invalidate_cache()

    def has_node(self, node: GraphNode) -> bool:
        """Check if node exists in the graph."""
        return node.id in self._nodes

    def add_edge(self, edge: WeightedEdge) -> None:  # type: ignore[override]
        """Add a weighted edge to the graph."""
        if isinstance(edge, DirectedEdge):
            raise TypeError(
                "WeightedGraph requires undirected WeightedEdge, "
                f"not {type(edge).__name__}"
            )
        if not isinstance(edge, WeightedEdge):
            raise TypeError(f"Expected WeightedEdge, got {type(edge).__name__}")
        if not self.has_node(edge.node1):
            raise ValueError(f"Node {edge.node1.id} not in graph")
        if not self.has_node(edge.node2):
            raise ValueError(f"Node {edge.node2.id} not in graph")
        if not self._allow_multi_edges and self.has_edge(edge.node1, edge.node2):
            raise ValueError(
                f"Edge between {edge.node1.id} and {edge.node2.id} already exists. "
                "Use allow_multi_edges=True for multigraph."
            )
        self._edges.append(edge)
        self._adjacency[edge.node1.id].add(edge.node2.id)
        self._adjacency[edge.node2.id].add(edge.node1.id)
        self._invalidate_cache()

    def remove_edge(self, edge: WeightedEdge) -> None:  # type: ignore[override]
        """Remove a weighted edge from the graph."""
        if edge not in self._edges:
            raise ValueError(
                f"Edge between {edge.node1.id} and {edge.node2.id} not in graph"
            )
        self._edges.remove(edge)
        n1_id, n2_id = edge.node1.id, edge.node2.id
        has_other = any(e.connects(edge.node1, edge.node2) for e in self._edges)
        if not has_other:
            self._adjacency[n1_id].discard(n2_id)
            self._adjacency[n2_id].discard(n1_id)
        self._invalidate_cache()

    def has_edge(self, node1: GraphNode, node2: GraphNode) -> bool:
        """Check if an edge exists between two nodes."""
        if not self.has_node(node1) or not self.has_node(node2):
            return False
        return node2.id in self._adjacency[node1.id]

    def get_edge(self, node1: GraphNode, node2: GraphNode) -> Optional[WeightedEdge]:
        """Get the weighted edge between two nodes."""
        for edge in self._edges:
            if edge.connects(node1, node2):
                return edge
        return None

    def get_edge_weight(self, node1: GraphNode, node2: GraphNode) -> Optional[float]:
        """Get the weight of the edge between two nodes."""
        edge = self.get_edge(node1, node2)
        return edge.weight if edge else None

    def total_weight(self) -> float:
        """Calculate the total weight of all edges."""
        if self._cache_valid and self._total_weight_cache is not None:
            return self._total_weight_cache
        total = sum(edge.weight for edge in self._edges)
        self._total_weight_cache = total
        self._cache_valid = True
        return total

    def incident_edges(
        self, node: GraphNode
    ) -> List[WeightedEdge | WeightedDirectedEdge]:
        """Get all weighted edges incident to a node."""
        if not self.has_node(node):
            raise ValueError(f"Node {node.id} not in graph")
        return [edge for edge in self._edges if edge.incident_to(node)]

    def neighbors(self, node: GraphNode) -> Iterator[GraphNode]:
        """Get all neighbors of a node."""
        if not self.has_node(node):
            raise ValueError(f"Node {node.id} not in graph")
        for neighbor_id in self._adjacency[node.id]:
            yield self._nodes[neighbor_id]

    def degree(self, node: GraphNode) -> int:
        """Get the degree of a node."""
        if not self.has_node(node):
            raise ValueError(f"Node {node.id} not in graph")
        if not self._allow_multi_edges:
            return len(self._adjacency[node.id])
        else:
            return sum(1 for e in self._edges if e.incident_to(node))

    def nodes(self) -> Iterator[GraphNode]:
        """Get all nodes in the graph."""
        yield from self._nodes.values()

    def edges(self) -> Iterator[WeightedEdge]:
        """Get all weighted edges in the graph."""
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
        result = self._check_connectivity_bfs()
        self._connectivity_cache = result
        self._cache_valid = True
        return result

    def _check_connectivity_bfs(self) -> bool:
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
        self._adjacency.clear()
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
            f"WeightedGraph(nodes={self.node_count()}, "
            f"edges={self.edge_count()}, multi_edges={self._allow_multi_edges})"
        )

    def __str__(self) -> str:
        """Return simple string representation."""
        return f"WeightedGraph: {self.node_count()} nodes, {self.edge_count()} edges"


class WeightedDirectedGraph(AbstractDirectedGraph, AbstractWeightedGraph):
    """Directed graph with weighted edges.

    Combines direction tracking (from DirectedGraph) with edge weights
    (from WeightedGraph). Uses two adjacency lists for efficient in/out
    degree queries and stores edge weights.

    Parameters
    ----------
    allow_multi_edges : bool, optional
        If True, allows multiple weighted edges from same source to target.
        Default is False.

    Attributes
    ----------
    allow_multi_edges : bool
        Whether multiple edges are allowed (read-only property).

    See Also
    --------
    WeightedGraph : For undirected weighted graphs.
    DirectedGraph : For unweighted directed graphs.
    """

    def __init__(self, allow_multi_edges: bool = False) -> None:
        """Initialize an empty weighted directed graph."""
        super().__init__()
        self._allow_multi_edges = allow_multi_edges
        self._nodes: Dict[str, GraphNode] = {}
        self._out_adjacency: Dict[str, Set[str]] = {}
        self._in_adjacency: Dict[str, Set[str]] = {}
        self._edges: List[WeightedDirectedEdge] = []
        self._connectivity_cache: Optional[bool] = None
        self._acyclic_cache: Optional[bool] = None
        self._total_weight_cache: Optional[float] = None
        self._cache_valid = False

    @property
    def allow_multi_edges(self) -> bool:
        """Check if multi-digraph mode is enabled."""
        return self._allow_multi_edges

    def _invalidate_cache(self) -> None:
        """Invalidate cached properties."""
        self._connectivity_cache = None
        self._acyclic_cache = None
        self._total_weight_cache = None
        self._cache_valid = False

    def add_node(self, node: GraphNode) -> None:
        """Add a node to the graph."""
        if not isinstance(node, GraphNode):
            raise TypeError(f"Expected GraphNode, got {type(node).__name__}")
        if node.id in self._nodes:
            raise ValueError(f"Node {node.id} already exists in graph")
        self._nodes[node.id] = node
        self._out_adjacency[node.id] = set()
        self._in_adjacency[node.id] = set()
        self._invalidate_cache()

    def remove_node(self, node: GraphNode) -> None:
        """Remove a node and all its incident edges."""
        if node.id not in self._nodes:
            raise ValueError(f"Node {node.id} not in graph")
        self._edges = [
            e for e in self._edges if e.source.id != node.id and e.target.id != node.id
        ]
        for source_id in self._in_adjacency[node.id]:
            self._out_adjacency[source_id].discard(node.id)
        for target_id in self._out_adjacency[node.id]:
            self._in_adjacency[target_id].discard(node.id)
        del self._nodes[node.id]
        del self._out_adjacency[node.id]
        del self._in_adjacency[node.id]
        self._invalidate_cache()

    def has_node(self, node: GraphNode) -> bool:
        """Check if node exists in the graph."""
        return node.id in self._nodes

    def add_edge(self, edge: WeightedDirectedEdge) -> None:  # type: ignore[override]
        """Add a weighted directed edge to the graph."""
        if not isinstance(edge, WeightedDirectedEdge):
            raise TypeError(f"Expected WeightedDirectedEdge, got {type(edge).__name__}")
        if not self.has_node(edge.source):
            raise ValueError(f"Source node {edge.source.id} not in graph")
        if not self.has_node(edge.target):
            raise ValueError(f"Target node {edge.target.id} not in graph")
        if not self._allow_multi_edges and self.has_edge(edge.source, edge.target):
            raise ValueError(
                f"Edge from {edge.source.id} to {edge.target.id} already exists. "
                "Use allow_multi_edges=True for multi-digraph."
            )
        self._edges.append(edge)
        self._out_adjacency[edge.source.id].add(edge.target.id)
        self._in_adjacency[edge.target.id].add(edge.source.id)
        self._invalidate_cache()

    def remove_edge(self, edge: WeightedDirectedEdge) -> None:  # type: ignore[override]
        """Remove a weighted directed edge from the graph."""
        if edge not in self._edges:
            raise ValueError(
                f"Edge from {edge.source.id} to {edge.target.id} not in graph"
            )
        self._edges.remove(edge)
        source_id, target_id = edge.source.id, edge.target.id
        has_other = any(
            e.source.id == source_id and e.target.id == target_id for e in self._edges
        )
        if not has_other:
            self._out_adjacency[source_id].discard(target_id)
            self._in_adjacency[target_id].discard(source_id)
        self._invalidate_cache()

    def has_edge(self, node1: GraphNode, node2: GraphNode) -> bool:
        """Check if a directed edge exists from node1 to node2."""
        if not self.has_node(node1) or not self.has_node(node2):
            return False
        return node2.id in self._out_adjacency[node1.id]

    def get_edge(
        self, node1: GraphNode, node2: GraphNode
    ) -> Optional[WeightedDirectedEdge]:
        """Get the weighted directed edge from node1 to node2."""
        for edge in self._edges:
            if edge.source.id == node1.id and edge.target.id == node2.id:
                return edge
        return None

    def get_edge_weight(self, node1: GraphNode, node2: GraphNode) -> Optional[float]:
        """Get the weight of the edge from node1 to node2."""
        edge = self.get_edge(node1, node2)
        return edge.weight if edge else None

    def total_weight(self) -> float:
        """Calculate the total weight of all edges."""
        if self._cache_valid and self._total_weight_cache is not None:
            return self._total_weight_cache
        total = sum(edge.weight for edge in self._edges)
        self._total_weight_cache = total
        self._cache_valid = True
        return total

    def incident_edges(
        self, node: GraphNode
    ) -> List[WeightedEdge | WeightedDirectedEdge]:
        """Get all weighted edges incident to a node."""
        if not self.has_node(node):
            raise ValueError(f"Node {node.id} not in graph")
        return [
            edge
            for edge in self._edges
            if edge.source.id == node.id or edge.target.id == node.id
        ]

    def neighbors(self, node: GraphNode) -> Iterator[GraphNode]:
        """Get all successors (outgoing neighbors) of a node."""
        return self.successors(node)

    def degree(self, node: GraphNode) -> int:
        """Get total degree of a node (in-degree + out-degree)."""
        if not self.has_node(node):
            raise ValueError(f"Node {node.id} not in graph")
        if not self._allow_multi_edges:
            return len(self._in_adjacency[node.id]) + len(self._out_adjacency[node.id])
        else:
            return sum(
                1
                for e in self._edges
                if e.source.id == node.id or e.target.id == node.id
            )

    def in_degree(self, node: GraphNode) -> int:
        """Get in-degree of a node (number of incoming edges)."""
        if not self.has_node(node):
            raise ValueError(f"Node {node.id} not in graph")
        if not self._allow_multi_edges:
            return len(self._in_adjacency[node.id])
        else:
            return sum(1 for e in self._edges if e.target.id == node.id)

    def out_degree(self, node: GraphNode) -> int:
        """Get out-degree of a node (number of outgoing edges)."""
        if not self.has_node(node):
            raise ValueError(f"Node {node.id} not in graph")
        if not self._allow_multi_edges:
            return len(self._out_adjacency[node.id])
        else:
            return sum(1 for e in self._edges if e.source.id == node.id)

    def predecessors(self, node: GraphNode) -> Iterator[GraphNode]:
        """Get all predecessors (nodes with edges to this node)."""
        if not self.has_node(node):
            raise ValueError(f"Node {node.id} not in graph")
        for predecessor_id in self._in_adjacency[node.id]:
            yield self._nodes[predecessor_id]

    def successors(self, node: GraphNode) -> Iterator[GraphNode]:
        """Get all successors (nodes with edges from this node)."""
        if not self.has_node(node):
            raise ValueError(f"Node {node.id} not in graph")
        for successor_id in self._out_adjacency[node.id]:
            yield self._nodes[successor_id]

    def is_acyclic(self) -> bool:
        """Check if the graph is acyclic (DAG)."""
        if self._cache_valid and self._acyclic_cache is not None:
            return self._acyclic_cache
        result = self._check_acyclic_dfs()
        self._acyclic_cache = result
        self._cache_valid = True
        return result

    def _check_acyclic_dfs(self) -> bool:
        """Check if graph is acyclic using DFS with coloring."""
        color: Dict[str, int] = {node_id: 0 for node_id in self._nodes}

        def has_cycle_from(node_id: str) -> bool:
            color[node_id] = 1
            for successor_id in self._out_adjacency[node_id]:
                if color[successor_id] == 1:
                    return True
                if color[successor_id] == 0:
                    if has_cycle_from(successor_id):
                        return True
            color[node_id] = 2
            return False

        for node_id in self._nodes:
            if color[node_id] == 0:
                if has_cycle_from(node_id):
                    return False
        return True

    def nodes(self) -> Iterator[GraphNode]:
        """Get all nodes in the graph."""
        yield from self._nodes.values()

    def edges(self) -> Iterator[WeightedDirectedEdge]:
        """Get all weighted directed edges in the graph."""
        yield from self._edges

    def node_count(self) -> int:
        """Get the number of nodes."""
        return len(self._nodes)

    def edge_count(self) -> int:
        """Get the number of edges."""
        return len(self._edges)

    def is_connected(self) -> bool:
        """Check if the graph is weakly connected."""
        if self._cache_valid and self._connectivity_cache is not None:
            return self._connectivity_cache
        result = self._check_weak_connectivity()
        self._connectivity_cache = result
        self._cache_valid = True
        return result

    def _check_weak_connectivity(self) -> bool:
        """Check weak connectivity using BFS."""
        if self.is_empty() or self.node_count() == 1:
            return True
        start_node = next(iter(self._nodes.values()))
        visited: Set[str] = set()
        queue: deque[GraphNode] = deque([start_node])
        visited.add(start_node.id)
        while queue:
            current = queue.popleft()
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
        """Get a node by its ID."""
        return self._nodes.get(node_id)

    def is_empty(self) -> bool:
        """Check if the graph is empty."""
        return len(self._nodes) == 0

    def clear(self) -> None:
        """Remove all nodes and edges."""
        self._nodes.clear()
        self._out_adjacency.clear()
        self._in_adjacency.clear()
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
            f"WeightedDirectedGraph(nodes={self.node_count()}, "
            f"edges={self.edge_count()}, multi_edges={self._allow_multi_edges})"
        )

    def __str__(self) -> str:
        """Return simple string representation."""
        return (
            f"WeightedDirectedGraph: {self.node_count()} nodes, "
            f"{self.edge_count()} edges"
        )
