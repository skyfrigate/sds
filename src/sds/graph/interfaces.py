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

"""Abstract base classes for graph data structures.

This module provides abstract interfaces that define the contract for graph
implementations. All graph classes should inherit from these abstractions.

Classes
-------
AbstractGraph
    Base interface for all graph types.
AbstractDirectedGraph
    Interface for directed graphs.
AbstractUndirectedGraph
    Interface for undirected graphs.
AbstractWeightedGraph
    Interface for weighted graphs.

Examples
--------
These are abstract classes and cannot be instantiated directly:

>>> from sds.graph.interfaces import AbstractGraph
>>> graph = AbstractGraph()  # doctest: +SKIP
Traceback (most recent call last):
    ...
TypeError: Can't instantiate abstract class

Implementations must provide all abstract methods:

>>> class MyGraph(AbstractGraph):
...     # Must implement all abstract methods
...     pass

Notes
-----
These interfaces ensure consistency across different graph implementations
and enable polymorphic usage of graph structures.

See Also
--------
sds.core.interfaces : Core collection interfaces.
sds.graphs.graph : Concrete graph implementations.
"""

from abc import ABC, abstractmethod
from typing import Iterator, List, Optional

from ..core.interfaces import Collection
from .edge import DirectedEdge, Edge, WeightedDirectedEdge, WeightedEdge
from .node import GraphNode

__all__ = [
    "AbstractGraph",
    "AbstractDirectedGraph",
    "AbstractUndirectedGraph",
    "AbstractWeightedGraph",
]


class AbstractGraph(Collection, ABC):
    """Abstract base class for all graph implementations.

    This class defines the core interface that all graph types must implement.
    It extends Collection to provide common operations like size, emptiness,
    and iteration.

    A graph consists of nodes (vertices) connected by edges. This abstract
    class defines operations for managing both nodes and edges.

    Notes
    -----
    Concrete implementations must provide:
    - Node management (add_node, remove_node, has_node)
    - Edge management (add_edge, remove_edge, has_edge)
    - Neighbor queries (neighbors, degree)
    - Traversal support (nodes, edges)
    - Graph properties (is_connected, etc.)

    See Also
    --------
    AbstractDirectedGraph : Interface for directed graphs.
    AbstractUndirectedGraph : Interface for undirected graphs.
    """

    @abstractmethod
    def add_node(self, node: GraphNode) -> None:
        """Add a node to the graph.

        Parameters
        ----------
        node : GraphNode
            Node to add.

        Raises
        ------
        ValueError
            If node already exists in the graph.
        """
        pass

    @abstractmethod
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
        """
        pass

    @abstractmethod
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
        """
        pass

    @abstractmethod
    def add_edge(self, edge: Edge) -> None:
        """Add an edge to the graph.

        Parameters
        ----------
        edge : Edge
            Edge to add.

        Raises
        ------
        ValueError
            If edge already exists or if nodes are not in the graph.
        """
        pass

    @abstractmethod
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
        """
        pass

    @abstractmethod
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
            True if edge exists.
        """
        pass

    @abstractmethod
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
        """
        pass

    @abstractmethod
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
        """
        pass

    @abstractmethod
    def degree(self, node: GraphNode) -> int:
        """Get the degree of a node.

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
        """
        pass

    @abstractmethod
    def nodes(self) -> Iterator[GraphNode]:
        """Get all nodes in the graph.

        Yields
        ------
        GraphNode
            All nodes in the graph.
        """
        pass

    @abstractmethod
    def edges(self) -> Iterator[Edge]:
        """Get all edges in the graph.

        Yields
        ------
        Edge
            All edges in the graph.
        """
        pass

    @abstractmethod
    def node_count(self) -> int:
        """Get the number of nodes in the graph.

        Returns
        -------
        int
            Number of nodes.
        """
        pass

    @abstractmethod
    def edge_count(self) -> int:
        """Get the number of edges in the graph.

        Returns
        -------
        int
            Number of edges.
        """
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        """Check if the graph is connected.

        Returns
        -------
        bool
            True if there is a path between any two nodes.
        """
        pass

    @abstractmethod
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
        """
        pass


class AbstractDirectedGraph(AbstractGraph):
    """Abstract base class for directed graph implementations.

    A directed graph has edges with direction: an edge from u to v is
    different from an edge from v to u.

    Notes
    -----
    Directed graphs have additional concepts:
    - in-degree: number of incoming edges
    - out-degree: number of outgoing edges
    - predecessors: nodes with edges pointing to a given node
    - successors: nodes with edges from a given node

    See Also
    --------
    AbstractGraph : Base graph interface.
    AbstractUndirectedGraph : Interface for undirected graphs.
    """

    @abstractmethod
    def add_edge(self, edge: DirectedEdge) -> None:  # type: ignore[override]
        """Add a directed edge to the graph.

        Parameters
        ----------
        edge : DirectedEdge
            Directed edge to add.

        Raises
        ------
        ValueError
            If edge already exists or nodes are not in the graph.
        """
        pass

    @abstractmethod
    def in_degree(self, node: GraphNode) -> int:
        """Get the in-degree of a node (number of incoming edges).

        Parameters
        ----------
        node : GraphNode
            Node to get in-degree for.

        Returns
        -------
        int
            Number of incoming edges.

        Raises
        ------
        ValueError
            If node is not in the graph.
        """
        pass

    @abstractmethod
    def out_degree(self, node: GraphNode) -> int:
        """Get the out-degree of a node (number of outgoing edges).

        Parameters
        ----------
        node : GraphNode
            Node to get out-degree for.

        Returns
        -------
        int
            Number of outgoing edges.

        Raises
        ------
        ValueError
            If node is not in the graph.
        """
        pass

    @abstractmethod
    def predecessors(self, node: GraphNode) -> Iterator[GraphNode]:
        """Get all predecessor nodes (nodes with edges to this node).

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
        """
        pass

    @abstractmethod
    def successors(self, node: GraphNode) -> Iterator[GraphNode]:
        """Get all successor nodes (nodes with edges from this node).

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
        """
        pass

    @abstractmethod
    def is_acyclic(self) -> bool:
        """Check if the graph has no cycles.

        Returns
        -------
        bool
            True if graph is a DAG (Directed Acyclic Graph).
        """
        pass


class AbstractUndirectedGraph(AbstractGraph):
    """Abstract base class for undirected graph implementations.

    An undirected graph has edges without direction: an edge between u and v
    allows traversal in both directions.

    Notes
    -----
    In undirected graphs:
    - Edges are symmetric: (u, v) = (v, u)
    - Degree is the total number of incident edges
    - Neighbors are all nodes connected by an edge

    See Also
    --------
    AbstractGraph : Base graph interface.
    AbstractDirectedGraph : Interface for directed graphs.
    """

    pass  # Inherits all methods from AbstractGraph


class AbstractWeightedGraph(AbstractGraph):
    """Abstract base class for weighted graph implementations.

    A weighted graph has numeric weights associated with edges, representing
    costs, distances, capacities, or other metrics.

    Notes
    -----
    Weighted graphs support:
    - Edge weights for pathfinding algorithms
    - Total weight calculations
    - Weight-based operations

    Both directed and undirected graphs can be weighted.

    See Also
    --------
    AbstractGraph : Base graph interface.
    """

    @abstractmethod
    def add_edge(  # type: ignore[override]
        self, edge: WeightedEdge | WeightedDirectedEdge
    ) -> None:
        """Add a weighted edge to the graph.

        Parameters
        ----------
        edge : WeightedEdge or WeightedDirectedEdge
            Weighted edge to add.

        Raises
        ------
        ValueError
            If edge already exists or nodes are not in the graph.
        """
        pass

    @abstractmethod
    def get_edge_weight(self, node1: GraphNode, node2: GraphNode) -> Optional[float]:
        """Get the weight of an edge between two nodes.

        Parameters
        ----------
        node1 : GraphNode
            First node.
        node2 : GraphNode
            Second node.

        Returns
        -------
        float or None
            Edge weight if edge exists, None otherwise.
        """
        pass

    @abstractmethod
    def total_weight(self) -> float:
        """Calculate the total weight of all edges.

        Returns
        -------
        float
            Sum of all edge weights.
        """
        pass

    @abstractmethod
    def incident_edges(
        self, node: GraphNode
    ) -> List[WeightedEdge | WeightedDirectedEdge]:
        """Get all edges incident to a node with their weights.

        Parameters
        ----------
        node : GraphNode
            Node to get incident edges for.

        Returns
        -------
        List[WeightedEdge or WeightedDirectedEdge]
            List of incident weighted edges.

        Raises
        ------
        ValueError
            If node is not in the graph.
        """
        pass
