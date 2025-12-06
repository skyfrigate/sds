"""Node classes for linear data structures.

This module provides node implementations specifically designed for linear
data structures such as linked lists, stacks, and queues.

Classes
-------
SimpleNode
    Node for singly linked lists with a single forward reference.
DoublyNode
    Node for doubly linked lists with both forward and backward references.

Examples
--------
Using SimpleNode:

>>> from sds.linear.node import SimpleNode
>>> node1 = SimpleNode(1)
>>> node2 = SimpleNode(2)
>>> node1.next = node2
>>> node1.next.data
2

Using DoublyNode:

>>> from sds.linear.node import DoublyNode
>>> node1 = DoublyNode(1)
>>> node2 = DoublyNode(2)
>>> node1.next = node2
>>> node2.prev is node1
True

Notes
-----
These nodes inherit from the abstract Node class in core.node and use
the _refs list internally to store references, exposing them through
specific properties (next, prev).

See Also
--------
sds.core.node : Abstract base Node class.
sds.linear.list : List implementations using these nodes.
"""

from typing import Any, Optional, cast

from ..core.node import Node

__all__ = ["SimpleNode", "DoublyNode"]


class SimpleNode(Node):
    """A node for singly linked lists.

    Each node contains data and a reference to the next node in the sequence.
    This is the basic building block for singly linked lists, stacks, queues,
    and other linear data structures.

    Internally uses _refs[0] to store the next node reference.

    Parameters
    ----------
    data : Any
        The data to store in the node.
    next_node : SimpleNode or None, optional
        Reference to the next node in the list. Default is None.

    Attributes
    ----------
    data : Any
        The data stored in the node (inherited from Node).
    next : SimpleNode or None
        Reference to the next node (property accessing _refs[0]).
    parent : Node or None
        Reference to parent node (inherited from Node).

    Examples
    --------
    Create a simple node:

    >>> node = SimpleNode(42)
    >>> node.data
    42
    >>> node.next is None
    True

    Create a chain of nodes:

    >>> node3 = SimpleNode(3)
    >>> node2 = SimpleNode(2, node3)
    >>> node1 = SimpleNode(1, node2)
    >>> node1.data
    1
    >>> node1.next.data
    2
    >>> node1.next.next.data
    3

    Modify node data and links:

    >>> node = SimpleNode(42)
    >>> node.data = 100
    >>> node.data
    100
    >>> node.next = SimpleNode(200)
    >>> node.next.data
    200

    Notes
    -----
    This class uses __slots__ for memory efficiency. The next reference
    is stored in _refs[0] and exposed via a property.

    See Also
    --------
    DoublyNode : Node with bidirectional links.
    sds.core.node.Node : Abstract base class.
    """

    __slots__ = ()  # No additional slots, inherits from Node

    def __init__(self, data: Any, next_node: Optional["SimpleNode"] = None):
        """Initialize a new simple node.

        Parameters
        ----------
        data : Any
            The data to store in the node.
        next_node : SimpleNode or None, optional
            The next node in the list. Default is None.
        """
        super().__init__(data)
        # Initialize _refs with one slot for next
        if next_node is not None:
            self._refs.append(next_node)
        else:
            self._refs.append(None)

    @property
    def next(self) -> Optional["SimpleNode"]:
        """Get or set the next node in the list.

        Returns
        -------
        SimpleNode or None
            The next node in the list, or None if this is the last node.

        Examples
        --------
        >>> node1 = SimpleNode(1)
        >>> node2 = SimpleNode(2)
        >>> node1.next = node2
        >>> node1.next.data
        2

        Notes
        -----
        This property accesses _refs[0].
        """

        return cast(Optional["SimpleNode"], self._refs[0])

    @next.setter
    def next(self, node: Optional["SimpleNode"]) -> None:
        """Set the next node in the list.

        Parameters
        ----------
        node : SimpleNode or None
            The node to set as next, or None to indicate end of list.

        Notes
        -----
        This setter updates _refs[0] and does NOT automatically set
        the parent reference (lists don't typically use parent pointers).
        """
        # Allow setting to None to clear next

        self._refs[0] = node

    def __repr__(self) -> str:
        """Return a detailed string representation of the node.

        Returns
        -------
        str
            String representation in the form "SimpleNode(data)".

        Examples
        --------
        >>> node = SimpleNode(42)
        >>> repr(node)
        'SimpleNode(42)'
        >>> node = SimpleNode("hello")
        >>> repr(node)
        "SimpleNode('hello')"
        """
        return f"SimpleNode({self._data!r})"

    def __str__(self) -> str:
        """Return a simple string representation of the node's data.

        Returns
        -------
        str
            String representation of the data.

        Examples
        --------
        >>> node = SimpleNode(42)
        >>> str(node)
        '42'
        >>> print(node)
        42
        """
        return str(self._data)


class DoublyNode(Node):
    """A node for doubly linked lists.

    Each node contains data and references to both the next and previous nodes
    in the sequence. This allows for bidirectional traversal of the list.

    Internally uses _refs[0] for next and _refs[1] for prev.

    Parameters
    ----------
    data : Any
        The data to store in the node.
    next_node : DoublyNode or None, optional
        Reference to the next node in the list. Default is None.
    prev_node : DoublyNode or None, optional
        Reference to the previous node in the list. Default is None.

    Attributes
    ----------
    data : Any
        The data stored in the node (inherited from Node).
    next : DoublyNode or None
        Reference to the next node (property accessing _refs[0]).
    prev : DoublyNode or None
        Reference to the previous node (property accessing _refs[1]).
    parent : Node or None
        Reference to parent node (inherited from Node).

    Examples
    --------
    Create a simple doubly linked node:

    >>> node = DoublyNode(42)
    >>> node.data
    42
    >>> node.next is None
    True
    >>> node.prev is None
    True

    Create a bidirectional chain:

    >>> node1 = DoublyNode(1)
    >>> node2 = DoublyNode(2)
    >>> node3 = DoublyNode(3)
    >>> node1.next = node2
    >>> node2.prev = node1
    >>> node2.next = node3
    >>> node3.prev = node2

    Traverse forward:

    >>> node1.next.data
    2
    >>> node1.next.next.data
    3

    Traverse backward:

    >>> node3.prev.data
    2
    >>> node3.prev.prev.data
    1

    Notes
    -----
    This class uses __slots__ for memory efficiency. When building
    bidirectional chains, you must manually maintain the symmetry
    between prev and next references.

    See Also
    --------
    SimpleNode : Node with unidirectional link.
    sds.core.node.Node : Abstract base class.
    """

    __slots__ = ()  # No additional slots, inherits from Node

    def __init__(
        self,
        data: Any,
        next_node: Optional["DoublyNode"] = None,
        prev_node: Optional["DoublyNode"] = None,
    ):
        """Initialize a new doubly linked node.

        Parameters
        ----------
        data : Any
            The data to store in the node.
        next_node : DoublyNode or None, optional
            The next node in the list. Default is None.
        prev_node : DoublyNode or None, optional
            The previous node in the list. Default is None.
        """
        super().__init__(data)
        # Initialize _refs with two slots: [next, prev]
        self._refs.append(next_node)
        self._refs.append(prev_node)

    @property
    def next(self) -> Optional["DoublyNode"]:
        """Get or set the next node in the list.

        Returns
        -------
        DoublyNode or None
            The next node in the list, or None if this is the last node.

        Examples
        --------
        >>> node1 = DoublyNode(1)
        >>> node2 = DoublyNode(2)
        >>> node1.next = node2
        >>> node1.next.data
        2

        Notes
        -----
        This property accesses _refs[0].
        """

        return cast(Optional["DoublyNode"], self._refs[0])

    @next.setter
    def next(self, node: Optional["DoublyNode"]) -> None:
        """Set the next node in the list.

        Parameters
        ----------
        node : DoublyNode or None
            The node to set as next, or None to indicate end of list.

        Notes
        -----
        This setter updates _refs[0] and does not automatically update
        the prev reference of the target node. You must manually maintain
        bidirectional consistency.
        """

        self._refs[0] = node

    @property
    def prev(self) -> Optional["DoublyNode"]:
        """Get or set the previous node in the list.

        Returns
        -------
        DoublyNode or None
            The previous node in the list, or None if this is the first node.

        Examples
        --------
        >>> node1 = DoublyNode(1)
        >>> node2 = DoublyNode(2)
        >>> node2.prev = node1
        >>> node2.prev.data
        1

        Notes
        -----
        This property accesses _refs[1].
        """

        return cast(Optional["DoublyNode"], self._refs[1])

    @prev.setter
    def prev(self, node: Optional["DoublyNode"]) -> None:
        """Set the previous node in the list.

        Parameters
        ----------
        node : DoublyNode or None
            The node to set as previous, or None to indicate start of list.

        Notes
        -----
        This setter updates _refs[1] and does not automatically update
        the next reference of the target node. You must manually maintain
        bidirectional consistency.
        """

        self._refs[1] = node

    def __repr__(self) -> str:
        """Return a detailed string representation of the node.

        Returns
        -------
        str
            String representation in the form "DoublyNode(data)".

        Examples
        --------
        >>> node = DoublyNode(42)
        >>> repr(node)
        'DoublyNode(42)'
        >>> node = DoublyNode("hello")
        >>> repr(node)
        "DoublyNode('hello')"
        """
        return f"DoublyNode({self._data!r})"

    def __str__(self) -> str:
        """Return a simple string representation of the node's data.

        Returns
        -------
        str
            String representation of the data.

        Examples
        --------
        >>> node = DoublyNode(42)
        >>> str(node)
        '42'
        >>> print(node)
        42
        """
        return str(self._data)
