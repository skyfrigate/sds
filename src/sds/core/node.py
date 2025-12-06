"""Abstract base node class for all data structures.

This module provides the foundational abstract Node class that serves as
the base for all node types used throughout the sds library. All concrete
node implementations (for lists, trees, graphs) inherit from this class.

The Node class uses a generic `_refs` list to store references to other nodes,
allowing different node types to implement specific access patterns via
properties.

Classes
-------
Node
    Abstract base class for all node types.

Examples
--------
Node is abstract and cannot be instantiated directly:

>>> from sds.core.node import Node
>>> node = Node(42)
Traceback (most recent call last):
    ...
TypeError: Can't instantiate abstract class Node

Use concrete implementations instead:

>>> from sds.linear.node import SimpleNode
>>> node = SimpleNode(42)
>>> node.data
42

Notes
-----
This is an abstract base class and must be subclassed with concrete
implementations. All node types in the library inherit from this class
to ensure a consistent interface.

See Also
--------
sds.linear.node : Node implementations for linear structures.
sds.trees.node : Node implementations for tree structures.
sds.graphs.node : Node implementations for graph structures.
"""

from abc import ABC, abstractmethod
from typing import Any, List, Optional

__all__ = ["Node"]


class Node(ABC):
    """Abstract base class for all node types.

    This class provides the foundational structure for all nodes in the sds
    library. It uses a generic `_refs` list to store references to other nodes,
    with concrete subclasses providing specific access patterns via properties.

    All node types share three core attributes:
    - _data: The value stored in the node
    - _refs: List of references to other nodes
    - _parent: Optional reference to a parent node

    Concrete subclasses define how `_refs` is interpreted:
    - SimpleNode: _refs[0] = next
    - DoublyNode: _refs[0] = next, _refs[1] = prev
    - BinaryNode: _refs[0] = left, _refs[1] = right
    - TreeNode: _refs = children list
    - GraphNode: _refs unused (connections via Edge objects)

    Parameters
    ----------
    data : Any
        The data to store in the node.

    Attributes
    ----------
    _data : Any
        The data stored in the node (read/write via property).
    _refs : List[Node]
        List of references to other nodes.
    _parent : Node or None
        Reference to the parent node (read/write via property).

    Examples
    --------
    Cannot instantiate Node directly (it's abstract):

    >>> node = Node(42)
    Traceback (most recent call last):
        ...
    TypeError: Can't instantiate abstract class Node

    Use concrete implementations:

    >>> from sds.linear.node import SimpleNode
    >>> node = SimpleNode(42)
    >>> node.data
    42

    Notes
    -----
    This class uses __slots__ for memory efficiency. The `_refs` list provides
    a unified way to store node connections, with subclasses defining specific
    access patterns through properties.

    Subclasses should:
    1. Call super().__init__(data) in their __init__
    2. Define properties for accessing _refs elements
    3. Optionally override setters to maintain parent-child consistency

    See Also
    --------
    sds.linear.node.SimpleNode : Node for singly linked lists.
    sds.linear.node.DoublyNode : Node for doubly linked lists.
    sds.trees.node.BinaryNode : Node for binary trees.
    sds.trees.node.TreeNode : Node for general trees.
    sds.graphs.node.GraphNode : Node for graphs.
    """

    __slots__ = ("_data", "_refs", "_parent")

    def __init__(self, data: Any):
        """Initialize a new node with data.

        Parameters
        ----------
        data : Any
            The data to store in the node.

        Notes
        -----
        Subclasses should call super().__init__(data) and then initialize
        their _refs list according to their specific needs.
        """
        self._data = data
        # Internal references storage. Subclasses may store Optional links
        # (e.g., next/prev can be None), so we type this accordingly.
        self._refs: List[Optional["Node"]] = []
        self._parent: Optional["Node"] = None

    @property
    def data(self) -> Any:
        """Get or set the data stored in the node.

        Returns
        -------
        Any
            The data stored in the node.

        Examples
        --------
        >>> from sds.linear.node import SimpleNode
        >>> node = SimpleNode(42)
        >>> node.data
        42
        >>> node.data = 100
        >>> node.data
        100

        Notes
        -----
        This property is defined in the abstract base class and inherited
        by all concrete node types.
        """
        return self._data

    @data.setter
    def data(self, value: Any) -> None:
        """Set the data stored in the node.

        Parameters
        ----------
        value : Any
            The new data value.
        """
        self._data = value

    @property
    def parent(self) -> Optional["Node"]:
        """Get or set the parent node.

        Returns
        -------
        Node or None
            The parent node, or None if this is a root node.

        Examples
        --------
        >>> from sds.trees.node import BinaryNode
        >>> root = BinaryNode(10)
        >>> child = BinaryNode(5)
        >>> root.left = child
        >>> child.parent is root
        True

        Notes
        -----
        The parent reference is maintained automatically when using
        setters in concrete node classes (for trees and lists).
        """
        return self._parent

    @parent.setter
    def parent(self, node: Optional["Node"]) -> None:
        """Set the parent node.

        Parameters
        ----------
        node : Node or None
            The node to set as parent, or None if this is a root.

        Notes
        -----
        This setter does not automatically update the parent's children.
        It's recommended to use the specific setters in concrete classes
        (e.g., left/right for BinaryNode) instead.
        """
        self._parent = node

    @abstractmethod
    def __repr__(self) -> str:
        """Return a detailed string representation of the node.

        Returns
        -------
        str
            String representation of the node.

        Notes
        -----
        Concrete subclasses must implement this method to provide
        appropriate string representation.
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Return a simple string representation of the node's data.

        Returns
        -------
        str
            String representation of the data.

        Notes
        -----
        Concrete subclasses must implement this method.
        """
        pass
