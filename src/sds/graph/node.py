# Copyright 2024-205, skyfrigate, biface
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

"""Node class for graph data structures.

This module provides the node implementation specifically designed for graph
structures. Unlike tree and list nodes that store references to other nodes
internally, graph nodes do not use the _refs list. Instead, graph connections
are managed through separate Edge objects and the Graph class itself.

Classes
-------
GraphNode
    Node for graphs where connections are managed externally via Edge objects.

Examples
--------
Using GraphNode:

>>> from sds.graph.node import GraphNode
>>> node1 = GraphNode(1, "node1")
>>> node2 = GraphNode(2, "node2")
>>> node1.data
1
>>> node1.id
'node1'

Notes
-----
GraphNode inherits from the abstract Node class but does not use the _refs
list. Graph connections are established through Edge objects that reference
GraphNodes.

See Also
--------
sds.core.node : Abstract base Node class.
sds.graphs.edge : Edge classes for graph connections.
sds.graphs.graph : Graph implementations using GraphNode.
"""

import uuid
from typing import Any, Optional

from ..core.node import Node

__all__ = ["GraphNode"]


class GraphNode(Node):
    """A node for graph data structures.

    Graph nodes are simple containers for data with a unique identifier.
    Unlike tree or list nodes, they do not maintain references to other nodes
    internally. Instead, connections between nodes are managed by Edge objects
    and the Graph class.

    The _refs list inherited from Node is not used by GraphNode.

    Parameters
    ----------
    data : Any
        The data to store in the node.
    node_id : str or None, optional
        Unique identifier for the node. If None, a UUID is generated automatically.
        Default is None.

    Attributes
    ----------
    data : Any
        The data stored in the node (inherited from Node).
    id : str
        Unique identifier for the node (read-only property).
    parent : Node or None
        Inherited from Node but typically not used in graphs.

    Examples
    --------
    Create nodes with automatic IDs:

    >>> node1 = GraphNode("A")
    >>> node2 = GraphNode("B")
    >>> node1.data
    'A'
    >>> len(node1.id) > 0
    True

    Create nodes with explicit IDs:

    >>> node1 = GraphNode("A", "node_a")
    >>> node2 = GraphNode("B", "node_b")
    >>> node1.id
    'node_a'
    >>> node2.id
    'node_b'

    Nodes can store any type of data:

    >>> node = GraphNode({"name": "Alice", "age": 30}, "user_1")
    >>> node.data
    {'name': 'Alice', 'age': 30}

    Notes
    -----
    This class uses __slots__ for memory efficiency. The _refs list is
    inherited but remains empty - graph structure is managed externally
    through Edge objects.

    GraphNode does not maintain connections to other nodes directly. Use
    the Graph class and Edge objects to define and manage graph structure.

    See Also
    --------
    sds.core.node.Node : Abstract base class.
    sds.graphs.edge.Edge : Edge class for graph connections.
    """

    __slots__ = ("_id",)  # Additional slot for node ID

    def __init__(self, data: Any, node_id: Optional[str] = None):
        """Initialize a new graph node.

        Parameters
        ----------
        data : Any
            The data to store in the node.
        node_id : str or None, optional
            Unique identifier for the node. If None, a UUID is generated.
            Default is None.

        Examples
        --------
        Create node with automatic ID:

        >>> node = GraphNode(42)
        >>> isinstance(node.id, str)
        True

        Create node with custom ID:

        >>> node = GraphNode(42, "my_node")
        >>> node.id
        'my_node'
        """
        super().__init__(data)
        self._id = node_id if node_id is not None else str(uuid.uuid4())
        # _refs remains empty for GraphNode - connections via Edge objects

    @property
    def id(self) -> str:
        """Get the unique identifier of the node.

        Returns
        -------
        str
            The unique identifier for this node.

        Examples
        --------
        >>> node = GraphNode("A", "node_a")
        >>> node.id
        'node_a'

        Notes
        -----
        This property is read-only. The ID is set at initialization and
        cannot be changed afterward.
        """
        return self._id

    def __repr__(self) -> str:
        """Return a detailed string representation of the node.

        Returns
        -------
        str
            String representation in the form "GraphNode(id=..., data=...)".

        Examples
        --------
        >>> node = GraphNode(42, "node1")
        >>> repr(node)
        "GraphNode(id='node1', data=42)"
        >>> node = GraphNode("hello", "node2")
        >>> repr(node)
        "GraphNode(id='node2', data='hello')"
        """
        return f"GraphNode(id={self._id!r}, data={self._data!r})"

    def __str__(self) -> str:
        """Return a simple string representation of the node.

        Returns
        -------
        str
            String showing ID and data.

        Examples
        --------
        >>> node = GraphNode(42, "node1")
        >>> str(node)
        'node1: 42'
        >>> print(node)
        node1: 42
        """
        return f"{self._id}: {self._data}"

    def __eq__(self, other: object) -> bool:
        """Check equality based on node ID.

        Two GraphNodes are considered equal if they have the same ID.

        Parameters
        ----------
        other : object
            The object to compare with.

        Returns
        -------
        bool
            True if other is a GraphNode with the same ID, False otherwise.

        Examples
        --------
        >>> node1 = GraphNode("A", "id1")
        >>> node2 = GraphNode("B", "id1")  # Same ID, different data
        >>> node1 == node2
        True
        >>> node3 = GraphNode("A", "id2")
        >>> node1 == node3
        False

        Notes
        -----
        Equality is based solely on the node ID, not the data.
        This allows nodes to be used in sets and as dictionary keys.
        """
        if not isinstance(other, GraphNode):
            return False
        return self._id == other._id

    def __hash__(self) -> int:
        """Return hash based on node ID.

        Returns
        -------
        int
            Hash value of the node ID.

        Examples
        --------
        >>> node1 = GraphNode("A", "id1")
        >>> node2 = GraphNode("B", "id1")
        >>> hash(node1) == hash(node2)
        True

        Notes
        -----
        This allows GraphNodes to be used in sets and as dictionary keys.
        Hash is based on the ID, so nodes with the same ID have the same hash.
        """
        return hash(self._id)
