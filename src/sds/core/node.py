"""Node classes for linked data structures.

This module provides the fundamental node classes used in linked data structures:
- Node: For singly linked lists
- DoublyNode: For doubly linked lists

Examples
--------
>>> node = Node(42)
>>> node.data
42
>>> node.next is None
True

>>> node2 = Node(10, node)
>>> node2.next.data
42
"""

from typing import Any, Optional


class Node:
    """A node in a singly linked list.

    Each node contains data and a reference to the next node in the sequence.
    This is the basic building block for singly linked lists, stacks, queues,
    and other linear data structures.

    Parameters
    ----------
    data : Any
        The data to store in the node.
    next_node : Node or None, optional
        Reference to the next node in the list. Default is None.

    Attributes
    ----------
    _data : Any
        The data stored in the node (read/write via property).
    _next : Node or None
        Reference to the next node in the list (read/write via property).

    Examples
    --------
    Create a simple node:

    >>> node = Node(42)
    >>> node.data
    42
    >>> node.next is None
    True

    Create a chain of nodes:

    >>> node3 = Node(3)
    >>> node2 = Node(2, node3)
    >>> node1 = Node(1, node2)
    >>> node1.data
    1
    >>> node1.next.data
    2
    >>> node1.next.next.data
    3

    Modify node data and links:

    >>> node = Node(42)
    >>> node.data = 100
    >>> node.data
    100
    >>> node.next = Node(200)
    >>> node.next.data
    200

    Notes
    -----
    This class uses __slots__ for memory efficiency, which means you cannot
    dynamically add new attributes to instances.

    The data and next attributes are implemented as properties backed by
    private attributes (_data and _next) to allow for future validation
    or modification of getter/setter behavior.

    See Also
    --------
    DoublyNode : Node with bidirectional links (prev and next).
    """

    __slots__ = ("_data", "_next")

    def __init__(self, data: Any, next_node: Optional["Node"] = None):
        """Initialize a new node.

        Parameters
        ----------
        data : Any
            The data to store in the node.
        next_node : Node or None, optional
            The next node in the list. Default is None.
        """
        self._data = data
        self._next = next_node

    @property
    def data(self) -> Any:
        """Get or set the data stored in the node.

        Returns
        -------
        Any
            The data stored in the node.

        Examples
        --------
        >>> node = Node(42)
        >>> node.data
        42
        >>> node.data = 100
        >>> node.data
        100
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
    def next(self) -> Optional["Node"]:
        """Get or set the next node in the list.

        Returns
        -------
        Node or None
            The next node in the list, or None if this is the last node.

        Examples
        --------
        >>> node1 = Node(1)
        >>> node2 = Node(2)
        >>> node1.next = node2
        >>> node1.next.data
        2
        """
        return self._next

    @next.setter
    def next(self, node: Optional["Node"]) -> None:
        """Set the next node in the list.

        Parameters
        ----------
        node : Node or None
            The node to set as next, or None to indicate end of list.
        """
        self._next = node

    def __repr__(self) -> str:
        """Return a detailed string representation of the node.

        Returns
        -------
        str
            String representation in the form "Node(data)".

        Examples
        --------
        >>> node = Node(42)
        >>> repr(node)
        'Node(42)'
        >>> node = Node("hello")
        >>> repr(node)
        "Node('hello')"
        """
        return f"Node({self._data!r})"

    def __str__(self) -> str:
        """Return a simple string representation of the node's data.

        Returns
        -------
        str
            String representation of the data.

        Examples
        --------
        >>> node = Node(42)
        >>> str(node)
        '42'
        >>> print(node)
        42
        """
        return str(self._data)


class DoublyNode:
    """A node in a doubly linked list.

    Each node contains data and references to both the next and previous nodes
    in the sequence. This allows for bidirectional traversal of the list.
    This is the basic building block for doubly linked lists, deques, and
    other bidirectional data structures.

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
    _data : Any
        The data stored in the node (read/write via property).
    _next : DoublyNode or None
        Reference to the next node in the list (read/write via property).
    _prev : DoublyNode or None
        Reference to the previous node in the list (read/write via property).

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
    This class uses __slots__ for memory efficiency, which means you cannot
    dynamically add new attributes to instances.

    The data, next, and prev attributes are implemented as properties backed by
    private attributes (_data, _next, and _prev) to allow for future validation
    or modification of getter/setter behavior.

    When building bidirectional chains, you must manually maintain the symmetry
    between prev and next references. For example, if you set node1.next = node2,
    you should also set node2.prev = node1.

    See Also
    --------
    Node : Node with unidirectional link (next only).
    """

    __slots__ = ("_data", "_next", "_prev")

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
        self._data = data
        self._next = next_node
        self._prev = prev_node

    @property
    def data(self) -> Any:
        """Get or set the data stored in the node.

        Returns
        -------
        Any
            The data stored in the node.

        Examples
        --------
        >>> node = DoublyNode(42)
        >>> node.data
        42
        >>> node.data = 100
        >>> node.data
        100
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
        """
        return self._next

    @next.setter
    def next(self, node: Optional["DoublyNode"]) -> None:
        """Set the next node in the list.

        Parameters
        ----------
        node : DoublyNode or None
            The node to set as next, or None to indicate end of list.

        Notes
        -----
        This setter does not automatically update the prev reference of the
        target node. You must manually maintain bidirectional consistency.
        """
        self._next = node

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
        """
        return self._prev

    @prev.setter
    def prev(self, node: Optional["DoublyNode"]) -> None:
        """Set the previous node in the list.

        Parameters
        ----------
        node : DoublyNode or None
            The node to set as previous, or None to indicate start of list.

        Notes
        -----
        This setter does not automatically update the next reference of the
        target node. You must manually maintain bidirectional consistency.
        """
        self._prev = node

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
