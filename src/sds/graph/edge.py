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

"""Edge classes for graph data structures.

This module provides edge implementations for connecting nodes in graph
structures. Edges can be directed or undirected, and weighted or unweighted.

Classes
-------
Edge
    Base class for undirected, unweighted edges.
DirectedEdge
    Edge with a direction from source to target.
WeightedEdge
    Edge with an associated weight value.
WeightedDirectedEdge
    Edge that is both weighted and directed.

Examples
--------
Create an undirected edge:

>>> from sds.graph.node import GraphNode
>>> from sds.graph.edge import Edge
>>> node1 = GraphNode("A", "n1")
>>> node2 = GraphNode("B", "n2")
>>> edge = Edge(node1, node2)
>>> edge.connects(node1, node2)
True

Create a directed edge:

>>> from sds.graph.edge import DirectedEdge
>>> directed = DirectedEdge(node1, node2)
>>> directed.source.id
'n1'
>>> directed.target.id
'n2'

Create a weighted edge:

>>> from sds.graph.edge import WeightedEdge
>>> weighted = WeightedEdge(node1, node2, weight=5.0)
>>> weighted.weight
5.0

Notes
-----
Edges reference GraphNode objects but do not modify them. The graph structure
is maintained by the Graph class which manages collections of nodes and edges.

See Also
--------
sds.graphs.node : GraphNode class for graph vertices.
sds.graphs.graph : Graph implementations using edges.
"""

from typing import Any, Optional

from .node import GraphNode

__all__ = ["Edge", "DirectedEdge", "WeightedEdge", "WeightedDirectedEdge"]


class Edge:
    """Base class for undirected, unweighted edges.

    An edge connects two nodes in an undirected graph. The edge has no
    inherent direction, so (u, v) is equivalent to (v, u).

    Parameters
    ----------
    node1 : GraphNode
        First node connected by the edge.
    node2 : GraphNode
        Second node connected by the edge.
    data : Any, optional
        Additional data associated with the edge. Default is None.

    Attributes
    ----------
    node1 : GraphNode
        First node (read-only property).
    node2 : GraphNode
        Second node (read-only property).
    data : Any
        Additional edge data (read-only property).

    Examples
    --------
    >>> from sds.graph.node import GraphNode
    >>> n1 = GraphNode("A", "n1")
    >>> n2 = GraphNode("B", "n2")
    >>> edge = Edge(n1, n2)
    >>> edge.connects(n1, n2)
    True
    >>> edge.connects(n2, n1)  # Undirected
    True

    Store additional data:

    >>> edge = Edge(n1, n2, data={"type": "friend"})
    >>> edge.data
    {'type': 'friend'}

    Notes
    -----
    Edges are immutable after creation. Use __slots__ for memory efficiency.
    """

    __slots__ = ("_node1", "_node2", "_data")

    def __init__(
        self,
        node1: GraphNode,
        node2: GraphNode,
        data: Optional[Any] = None,
        allow_self_loop: bool = False,
    ) -> None:
        """Initialize an undirected edge.

        Parameters
        ----------
        node1 : GraphNode
            First node.
        node2 : GraphNode
            Second node.
        data : Any, optional
            Additional data. Default is None.
        allow_self_loop : bool, optional
            Allow self-loops. Default is False.

        Raises
        ------
        TypeError
            If node1 or node2 is not a GraphNode.
        ValueError
            If node1 and node2 are the same and allow_self_loop is False.
        """
        if not isinstance(node1, GraphNode):
            raise TypeError(f"node1 must be GraphNode, got {type(node1)}")
        if not isinstance(node2, GraphNode):
            raise TypeError(f"node2 must be GraphNode, got {type(node2)}")
        if node1.id == node2.id and not allow_self_loop:
            raise ValueError(
                "Self-loops not allowed. Set allow_self_loop=True to enable."
            )

        self._node1 = node1
        self._node2 = node2
        self._data = data

    @property
    def node1(self) -> GraphNode:
        """Get the first node.

        Returns
        -------
        GraphNode
            The first node.
        """
        return self._node1

    @property
    def node2(self) -> GraphNode:
        """Get the second node.

        Returns
        -------
        GraphNode
            The second node.
        """
        return self._node2

    @property
    def data(self) -> Any:
        """Get the edge data.

        Returns
        -------
        Any
            The edge data.
        """
        return self._data

    def connects(self, node_a: GraphNode, node_b: GraphNode) -> bool:
        """Check if edge connects two specific nodes.

        For undirected edges, order doesn't matter.

        Parameters
        ----------
        node_a : GraphNode
            First node to check.
        node_b : GraphNode
            Second node to check.

        Returns
        -------
        bool
            True if edge connects node_a and node_b.

        Examples
        --------
        >>> n1 = GraphNode("A", "n1")
        >>> n2 = GraphNode("B", "n2")
        >>> edge = Edge(n1, n2)
        >>> edge.connects(n1, n2)
        True
        >>> edge.connects(n2, n1)
        True
        """
        return {self._node1.id, self._node2.id} == {node_a.id, node_b.id}

    def incident_to(self, node: GraphNode) -> bool:
        """Check if edge is incident to a node.

        Parameters
        ----------
        node : GraphNode
            Node to check.

        Returns
        -------
        bool
            True if edge touches the node.

        Examples
        --------
        >>> n1 = GraphNode("A", "n1")
        >>> n2 = GraphNode("B", "n2")
        >>> n3 = GraphNode("C", "n3")
        >>> edge = Edge(n1, n2)
        >>> edge.incident_to(n1)
        True
        >>> edge.incident_to(n3)
        False
        """
        return node.id in {self._node1.id, self._node2.id}

    def other_node(self, node: GraphNode) -> GraphNode:
        """Get the other node connected by this edge.

        Parameters
        ----------
        node : GraphNode
            One of the nodes in the edge.

        Returns
        -------
        GraphNode
            The other node.

        Raises
        ------
        ValueError
            If node is not part of this edge.

        Examples
        --------
        >>> n1 = GraphNode("A", "n1")
        >>> n2 = GraphNode("B", "n2")
        >>> edge = Edge(n1, n2)
        >>> edge.other_node(n1).id
        'n2'
        >>> edge.other_node(n2).id
        'n1'
        """
        if node.id == self._node1.id:
            return self._node2
        elif node.id == self._node2.id:
            return self._node1
        else:
            raise ValueError(f"Node {node.id} is not part of this edge")

    def is_self_loop(self) -> bool:
        """Check if this edge is a self-loop.

        Returns
        -------
        bool
            True if the edge connects a node to itself.

        Examples
        --------
        >>> n1 = GraphNode("A", "n1")
        >>> loop = Edge(n1, n1, allow_self_loop=True)
        >>> loop.is_self_loop()
        True
        >>> n2 = GraphNode("B", "n2")
        >>> edge = Edge(n1, n2)
        >>> edge.is_self_loop()
        False
        """
        return self._node1.id == self._node2.id

    def __eq__(self, other: object) -> bool:
        """Check equality based on connected nodes.

        Parameters
        ----------
        other : object
            Object to compare with.

        Returns
        -------
        bool
            True if edges connect the same nodes (order-independent).

        Examples
        --------
        >>> n1 = GraphNode("A", "n1")
        >>> n2 = GraphNode("B", "n2")
        >>> e1 = Edge(n1, n2)
        >>> e2 = Edge(n2, n1)
        >>> e1 == e2
        True
        """
        if not isinstance(other, Edge):
            return False
        return {self._node1.id, self._node2.id} == {
            other._node1.id,
            other._node2.id,
        }

    def __hash__(self) -> int:
        """Return hash based on connected nodes.

        Returns
        -------
        int
            Hash value (order-independent for undirected edges).
        """
        return hash(frozenset({self._node1.id, self._node2.id}))

    def __repr__(self) -> str:
        """Return detailed string representation.

        Returns
        -------
        str
            String representation.

        Examples
        --------
        >>> n1 = GraphNode("A", "n1")
        >>> n2 = GraphNode("B", "n2")
        >>> edge = Edge(n1, n2)
        >>> repr(edge)
        "Edge(n1 -- n2)"
        """
        return f"Edge({self._node1.id} -- {self._node2.id})"

    def __str__(self) -> str:
        """Return simple string representation.

        Returns
        -------
        str
            String representation.

        Examples
        --------
        >>> n1 = GraphNode("A", "n1")
        >>> n2 = GraphNode("B", "n2")
        >>> edge = Edge(n1, n2)
        >>> str(edge)
        'n1 -- n2'
        """
        return f"{self._node1.id} -- {self._node2.id}"


class DirectedEdge(Edge):
    """Edge with a direction from source to target.

    A directed edge has an explicit direction from a source node to a
    target node. The edge (u, v) is different from (v, u).

    Parameters
    ----------
    source : GraphNode
        Source node (tail of the edge).
    target : GraphNode
        Target node (head of the edge).
    data : Any, optional
        Additional data. Default is None.

    Attributes
    ----------
    source : GraphNode
        Source node (read-only property).
    target : GraphNode
        Target node (read-only property).
    node1 : GraphNode
        Alias for source (inherited property).
    node2 : GraphNode
        Alias for target (inherited property).

    Examples
    --------
    >>> n1 = GraphNode("A", "n1")
    >>> n2 = GraphNode("B", "n2")
    >>> edge = DirectedEdge(n1, n2)
    >>> edge.source.id
    'n1'
    >>> edge.target.id
    'n2'
    >>> edge.connects(n1, n2)
    True
    >>> edge.connects(n2, n1)  # Direction matters
    False

    Notes
    -----
    DirectedEdge overrides connects() to respect direction.
    """

    def __init__(
        self, source: GraphNode, target: GraphNode, data: Optional[Any] = None
    ) -> None:
        """Initialize a directed edge.

        Parameters
        ----------
        source : GraphNode
            Source node.
        target : GraphNode
            Target node.
        data : Any, optional
            Additional data. Default is None.
        """
        super().__init__(source, target, data)

    @property
    def source(self) -> GraphNode:
        """Get the source node.

        Returns
        -------
        GraphNode
            The source node.
        """
        return self._node1

    @property
    def target(self) -> GraphNode:
        """Get the target node.

        Returns
        -------
        GraphNode
            The target node.
        """
        return self._node2

    def connects(self, node_a: GraphNode, node_b: GraphNode) -> bool:
        """Check if edge goes from node_a to node_b.

        For directed edges, order matters: edge must go from node_a to node_b.

        Parameters
        ----------
        node_a : GraphNode
            Expected source node.
        node_b : GraphNode
            Expected target node.

        Returns
        -------
        bool
            True if edge goes from node_a to node_b.

        Examples
        --------
        >>> n1 = GraphNode("A", "n1")
        >>> n2 = GraphNode("B", "n2")
        >>> edge = DirectedEdge(n1, n2)
        >>> edge.connects(n1, n2)
        True
        >>> edge.connects(n2, n1)
        False
        """
        return self._node1.id == node_a.id and self._node2.id == node_b.id

    def __eq__(self, other: object) -> bool:
        """Check equality respecting direction.

        Parameters
        ----------
        other : object
            Object to compare with.

        Returns
        -------
        bool
            True if edges have same source and target.
        """
        if not isinstance(other, DirectedEdge):
            return False
        return self._node1.id == other._node1.id and self._node2.id == other._node2.id

    def __hash__(self) -> int:
        """Return hash respecting direction.

        Returns
        -------
        int
            Hash value (order-dependent for directed edges).
        """
        return hash((self._node1.id, self._node2.id))

    def __repr__(self) -> str:
        """Return detailed string representation.

        Returns
        -------
        str
            String representation with arrow.
        """
        return f"DirectedEdge({self._node1.id} -> {self._node2.id})"

    def __str__(self) -> str:
        """Return simple string representation.

        Returns
        -------
        str
            String with arrow showing direction.
        """
        return f"{self._node1.id} -> {self._node2.id}"


class WeightedEdge(Edge):
    """Edge with an associated weight value.

    A weighted edge has a numeric weight representing cost, distance,
    capacity, or other metrics.

    Parameters
    ----------
    node1 : GraphNode
        First node.
    node2 : GraphNode
        Second node.
    weight : float, optional
        Edge weight. Default is 1.0.
    data : Any, optional
        Additional data. Default is None.

    Attributes
    ----------
    weight : float
        Edge weight (read-only property).

    Examples
    --------
    >>> n1 = GraphNode("A", "n1")
    >>> n2 = GraphNode("B", "n2")
    >>> edge = WeightedEdge(n1, n2, weight=5.5)
    >>> edge.weight
    5.5

    Default weight is 1.0:

    >>> edge = WeightedEdge(n1, n2)
    >>> edge.weight
    1.0
    """

    __slots__ = ("_weight",)

    def __init__(
        self,
        node1: GraphNode,
        node2: GraphNode,
        weight: float = 1.0,
        data: Optional[Any] = None,
    ) -> None:
        """Initialize a weighted edge.

        Parameters
        ----------
        node1 : GraphNode
            First node.
        node2 : GraphNode
            Second node.
        weight : float, optional
            Edge weight. Default is 1.0.
        data : Any, optional
            Additional data. Default is None.

        Raises
        ------
        TypeError
            If weight is not numeric.
        """
        super().__init__(node1, node2, data)
        try:
            self._weight = float(weight)
        except (TypeError, ValueError) as e:
            raise TypeError(f"Weight must be numeric, got {type(weight)}") from e

    @property
    def weight(self) -> float:
        """Get the edge weight.

        Returns
        -------
        float
            The edge weight.
        """
        return self._weight

    def __repr__(self) -> str:
        """Return detailed string representation.

        Returns
        -------
        str
            String showing weight.
        """
        return f"WeightedEdge({self._node1.id} --{self._weight}-- {self._node2.id})"

    def __str__(self) -> str:
        """Return simple string representation.

        Returns
        -------
        str
            String showing weight.
        """
        return f"{self._node1.id} --{self._weight}-- {self._node2.id}"


class WeightedDirectedEdge(DirectedEdge):
    """Edge that is both weighted and directed.

    Combines the properties of DirectedEdge and WeightedEdge.

    Parameters
    ----------
    source : GraphNode
        Source node.
    target : GraphNode
        Target node.
    weight : float, optional
        Edge weight. Default is 1.0.
    data : Any, optional
        Additional data. Default is None.

    Attributes
    ----------
    weight : float
        Edge weight (read-only property).
    source : GraphNode
        Source node (read-only property).
    target : GraphNode
        Target node (read-only property).

    Examples
    --------
    >>> n1 = GraphNode("A", "n1")
    >>> n2 = GraphNode("B", "n2")
    >>> edge = WeightedDirectedEdge(n1, n2, weight=3.5)
    >>> edge.source.id
    'n1'
    >>> edge.weight
    3.5
    """

    __slots__ = ("_weight",)

    def __init__(
        self,
        source: GraphNode,
        target: GraphNode,
        weight: float = 1.0,
        data: Optional[Any] = None,
    ) -> None:
        """Initialize a weighted directed edge.

        Parameters
        ----------
        source : GraphNode
            Source node.
        target : GraphNode
            Target node.
        weight : float, optional
            Edge weight. Default is 1.0.
        data : Any, optional
            Additional data. Default is None.
        """
        super().__init__(source, target, data)
        try:
            self._weight = float(weight)
        except (TypeError, ValueError) as e:
            raise TypeError(f"Weight must be numeric, got {type(weight)}") from e

    @property
    def weight(self) -> float:
        """Get the edge weight.

        Returns
        -------
        float
            The edge weight.
        """
        return self._weight

    def __repr__(self) -> str:
        """Return detailed string representation.

        Returns
        -------
        str
            String showing direction and weight.
        """
        return (
            f"WeightedDirectedEdge({self._node1.id} "
            f"-{self._weight}-> {self._node2.id})"
        )

    def __str__(self) -> str:
        """Return simple string representation.

        Returns
        -------
        str
            String showing direction and weight.
        """
        return f"{self._node1.id} -{self._weight}-> {self._node2.id}"
