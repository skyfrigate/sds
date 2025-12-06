"""Concrete linked list implementations.

This module provides concrete implementations of all linked list variants.
These are fundamental linear data structures where elements are connected via
references (links) rather than being stored contiguously in memory.

Classes
-------
LinkedList
    Singly linked list where each node points to the next node.
DoublyLinkedList
    Doubly linked list where each node points to both next and previous nodes.
CircularLinkedList
    Circular singly linked list where the tail points back to the head.

Examples
--------
Using a singly linked list:

>>> from sds.linear.list import LinkedList
>>> lst = LinkedList()
>>> lst.append(1)
>>> lst.append(2)
>>> lst.prepend(0)
>>> list(lst)
[0, 1, 2]

Using a doubly linked list:

>>> from sds.linear.list import DoublyLinkedList
>>> dll = DoublyLinkedList()
>>> dll.append(1)
>>> dll.append(2)
>>> list(dll)
[1, 2]
>>> list(reversed(dll))
[2, 1]

Using a circular linked list:

>>> from sds.linear.list import CircularLinkedList
>>> cll = CircularLinkedList()
>>> cll.append(1)
>>> cll.append(2)
>>> cll.append(3)
>>> cll.rotate(1)
>>> list(cll)
[2, 3, 1]

Notes
-----
Linked lists provide O(1) insertion/deletion at the beginning, but O(n) for
random access. Choose linked lists when you need frequent insertions/deletions
and don't need random access.

See Also
--------
sds.linear.interfaces : Abstract base class for linked lists.
sds.linear.stack : Stack implementation.
sds.linear.queue : Queue implementations.
"""

from typing import Any, Iterator, Optional, cast

from ..core.exceptions import (
    EmptyStructureError,
)
from ..core.exceptions import IndexStructureError as SDSIndexError
from .interfaces import AbstractLinkedList
from .node import DoublyNode, SimpleNode


class LinkedList(AbstractLinkedList):
    """A singly linked list implementation.

    A linked list is a linear collection where each element (node) contains
    data and a reference to the next node in the sequence. This implementation
    uses a head pointer to track the beginning of the list.

    Attributes
    ----------
    head : Node or None
        The first node in the list (read-only property).
    size : int
        The number of elements in the list (read-only property).

    Time Complexity
    ---------------
    - Access by index: O(n)
    - Search: O(n)
    - Insert at beginning (prepend): O(1)
    - Insert at end (append): O(n)
    - Delete at beginning: O(1)
    - Delete at end: O(n)

    Examples
    --------
    Create and populate a list:

    >>> lst = LinkedList()
    >>> lst.append(1)
    >>> lst.append(2)
    >>> lst.append(3)
    >>> len(lst)
    3

    Access elements:

    >>> lst[0]
    1
    >>> lst[-1]
    3

    Iterate over elements:

    >>> for item in lst:
    ...     print(item)
    1
    2
    3

    Modify the list:

    >>> lst.prepend(0)
    >>> lst.insert_at(2, 1.5)
    >>> list(lst)
    [0, 1, 1.5, 2, 3]

    Notes
    -----
    This implementation maintains only a head pointer, which means append
    operations are O(n). For better performance with frequent appends,
    consider using DoublyLinkedList which maintains both head and tail pointers.

    See Also
    --------
    DoublyLinkedList : Linked list with bidirectional traversal and O(1) append.
    CircularLinkedList : Variant where the last node points back to the first.
    """

    def __init__(self):
        """Initialize an empty singly linked list."""
        super().__init__()
        self._head: Optional[SimpleNode] = None

    @property
    def head(self) -> Optional[SimpleNode]:
        """Get the first node in the list.

        Returns
        -------
        Node or None
            The first node, or None if the list is empty.

        Examples
        --------
        >>> lst = LinkedList()
        >>> lst.head is None
        True
        >>> lst.append(1)
        >>> lst.head.data
        1

        Notes
        -----
        This property is read-only. To modify the list, use methods like
        prepend(), append(), or insert_at().
        """
        return self._head

    def clear(self) -> None:
        """Remove all elements from the list.

        Examples
        --------
        >>> lst = LinkedList()
        >>> lst.append(1)
        >>> lst.append(2)
        >>> len(lst)
        2
        >>> lst.clear()
        >>> len(lst)
        0
        >>> lst.is_empty()
        True

        Notes
        -----
        Time complexity: O(1)
        This operation simply resets the head pointer, allowing garbage
        collection to clean up the nodes.
        """
        self._head = None
        self._size = 0

    def __iter__(self) -> Iterator[Any]:
        """Iterate over the elements in the list.

        Yields
        ------
        Any
            Elements from the list in order from head to tail.

        Examples
        --------
        >>> lst = LinkedList()
        >>> lst.append(1)
        >>> lst.append(2)
        >>> lst.append(3)
        >>> for item in lst:
        ...     print(item)
        1
        2
        3
        >>> list(lst)
        [1, 2, 3]

        Notes
        -----
        Time complexity: O(n) for complete iteration
        Space complexity: O(1)
        """
        current = self._head
        while current is not None:
            yield current.data
            current = current.next

    def __contains__(self, item: Any) -> bool:
        """Return True if item is in the list.

        Parameters
        ----------
        item : Any
            The item to search for.

        Returns
        -------
        bool
            True if the item is found, False otherwise.

        Examples
        --------
        >>> lst = LinkedList()
        >>> lst.append(1)
        >>> lst.append(2)
        >>> 1 in lst
        True
        >>> 3 in lst
        False

        Notes
        -----
        Time complexity: O(n)
        This performs a linear search through the list.
        """
        for data in self:
            if data == item:
                return True
        return False

    def __repr__(self) -> str:
        """Return a detailed string representation of the list.

        Returns
        -------
        str
            String in the form "LinkedList([item1, item2, ...])".

        Examples
        --------
        >>> lst = LinkedList()
        >>> lst.append(1)
        >>> lst.append(2)
        >>> repr(lst)
        'LinkedList([1, 2])'
        """
        elements = ", ".join(repr(item) for item in self)
        return f"LinkedList([{elements}])"

    def __str__(self) -> str:
        """Return a simple string representation of the list.

        Returns
        -------
        str
            String showing the list structure with arrows.

        Examples
        --------
        >>> lst = LinkedList()
        >>> lst.append(1)
        >>> lst.append(2)
        >>> str(lst)
        '[1 -> 2]'
        >>> print(lst)
        [1 -> 2]
        """
        elements = " -> ".join(str(item) for item in self)
        return f"[{elements}]" if elements else "[]"

    def __getitem__(self, index: int) -> Any:
        """Get the item at the specified index.

        Parameters
        ----------
        index : int
            The index (supports negative indexing).

        Returns
        -------
        Any
            The item at the specified index.

        Raises
        ------
        IndexError
            If the index is out of range.

        Examples
        --------
        >>> lst = LinkedList()
        >>> lst.append(10)
        >>> lst.append(20)
        >>> lst.append(30)
        >>> lst[0]
        10
        >>> lst[1]
        20
        >>> lst[-1]
        30

        Notes
        -----
        Time complexity: O(n)
        """
        node = self._get_node(index)
        return node.data

    def __setitem__(self, index: int, value: Any) -> None:
        """Set the item at the specified index.

        Parameters
        ----------
        index : int
            The index (supports negative indexing).
        value : Any
            The new value.

        Raises
        ------
        IndexError
            If the index is out of range.

        Examples
        --------
        >>> lst = LinkedList()
        >>> lst.append(10)
        >>> lst.append(20)
        >>> lst[0] = 100
        >>> lst[0]
        100

        Notes
        -----
        Time complexity: O(n)
        """
        node = self._get_node(index)
        node.data = value

    def _get_node(self, index: int) -> SimpleNode:
        """Get the node at the specified index.

        This is an internal helper method used by __getitem__ and __setitem__.

        Parameters
        ----------
        index : int
            The index (supports negative indexing).

        Returns
        -------
        Node
            The node at the specified index.

        Raises
        ------
        IndexError
            If the list is empty or index is out of range.

        Notes
        -----
        Time complexity: O(n)
        """
        if self.is_empty():
            raise SDSIndexError("List is empty")

        # Handle negative indices
        if index < 0:
            index += self._size

        if index < 0 or index >= self._size:
            raise SDSIndexError(
                f"Index {index} out of range for list of size {self._size}"
            )

        # After the emptiness and bounds checks above, head must be non-None
        current: SimpleNode = cast(SimpleNode, self._head)
        for _ in range(index):
            # We remain within bounds, so next is guaranteed non-None
            current = cast(SimpleNode, current.next)

        return current

    def prepend(self, item: Any) -> None:
        """Add an item to the beginning of the list.

        Parameters
        ----------
        item : Any
            The item to add.

        Examples
        --------
        >>> lst = LinkedList()
        >>> lst.prepend(3)
        >>> lst.prepend(2)
        >>> lst.prepend(1)
        >>> list(lst)
        [1, 2, 3]

        Notes
        -----
        Time complexity: O(1)
        """
        new_node = SimpleNode(item, self._head)
        self._head = new_node
        self._size += 1

    def append(self, item: Any) -> None:
        """Add an item to the end of the list.

        Parameters
        ----------
        item : Any
            The item to add.

        Examples
        --------
        >>> lst = LinkedList()
        >>> lst.append(1)
        >>> lst.append(2)
        >>> lst.append(3)
        >>> list(lst)
        [1, 2, 3]

        Notes
        -----
        Time complexity: O(n)
        This implementation must traverse the entire list to find the end.
        """
        new_node = SimpleNode(item)

        if self.is_empty():
            self._head = new_node
        else:
            # list not empty -> _head is not None
            current: SimpleNode = cast(SimpleNode, self._head)
            while current.next is not None:
                current = cast(SimpleNode, current.next)
            current.next = new_node

        self._size += 1

    def insert_at(self, index: int, item: Any) -> None:
        """Insert an item at the specified index.

        Parameters
        ----------
        index : int
            The index where to insert (0 <= index <= size).
        item : Any
            The item to insert.

        Raises
        ------
        IndexError
            If the index is out of range.

        Examples
        --------
        >>> lst = LinkedList()
        >>> lst.append(1)
        >>> lst.append(3)
        >>> lst.insert_at(1, 2)
        >>> list(lst)
        [1, 2, 3]

        Notes
        -----
        Time complexity: O(n)
        """
        if index < 0:
            index += self._size

        if index < 0 or index > self._size:
            raise SDSIndexError(f"Index {index} out of range for insertion")

        if index == 0:
            self.prepend(item)
        else:
            prev_node = self._get_node(index - 1)
            new_node = SimpleNode(item, prev_node.next)
            prev_node.next = new_node
            self._size += 1

    def remove_first(self) -> Any:
        """Remove and return the first item from the list.

        Returns
        -------
        Any
            The removed item.

        Raises
        ------
        EmptyStructureError
            If the list is empty.

        Examples
        --------
        >>> lst = LinkedList()
        >>> lst.append(1)
        >>> lst.append(2)
        >>> lst.remove_first()
        1
        >>> list(lst)
        [2]

        Notes
        -----
        Time complexity: O(1)
        """
        if self.is_empty():
            raise EmptyStructureError("Cannot remove from empty list")

        # Non-empty implies _head is not None
        head: SimpleNode = cast(SimpleNode, self._head)
        data = head.data
        self._head = head.next
        self._size -= 1
        return data

    def remove_last(self) -> Any:
        """Remove and return the last item from the list.

        Returns
        -------
        Any
            The removed item.

        Raises
        ------
        EmptyStructureError
            If the list is empty.

        Examples
        --------
        >>> lst = LinkedList()
        >>> lst.append(1)
        >>> lst.append(2)
        >>> lst.remove_last()
        2
        >>> list(lst)
        [1]

        Notes
        -----
        Time complexity: O(n)
        Must traverse to find the second-to-last node.
        """
        if self.is_empty():
            raise EmptyStructureError("Cannot remove from empty list")

        if self._size == 1:
            return self.remove_first()

        # At least two nodes exist
        current: SimpleNode = cast(SimpleNode, self._head)
        # Move until current is the penultimate node
        while True:
            nxt: SimpleNode = cast(SimpleNode, current.next)
            if nxt.next is None:
                break
            current = nxt

        data = cast(SimpleNode, current.next).data
        current.next = None
        self._size -= 1
        return data

    def remove(self, item: Any) -> Any:
        """Remove the first occurrence of an item from the list.

        Parameters
        ----------
        item : Any
            The item to remove.

        Returns
        -------
        Any
            The removed item.

        Raises
        ------
        EmptyStructureError
            If the list is empty.
        ValueError
            If the item is not found.

        Examples
        --------
        >>> lst = LinkedList()
        >>> lst.append(1)
        >>> lst.append(2)
        >>> lst.append(3)
        >>> lst.remove(2)
        2
        >>> list(lst)
        [1, 3]

        Notes
        -----
        Time complexity: O(n)
        """
        if self.is_empty():
            raise EmptyStructureError("Cannot remove from empty list")

        head: SimpleNode = cast(SimpleNode, self._head)
        if head.data == item:
            return self.remove_first()

        current: SimpleNode = cast(SimpleNode, self._head)
        while current.next is not None:
            nxt: SimpleNode = cast(SimpleNode, current.next)
            if nxt.data == item:
                data = nxt.data
                current.next = nxt.next
                self._size -= 1
                return data
            current = nxt

        raise ValueError(f"Item {item} not found in list")

    def remove_at(self, index: int) -> Any:
        """Remove and return the item at the specified index.

        Parameters
        ----------
        index : int
            The index of the item to remove.

        Returns
        -------
        Any
            The removed item.

        Raises
        ------
        EmptyStructureError
            If the list is empty.
        IndexError
            If the index is out of range.

        Examples
        --------
        >>> lst = LinkedList()
        >>> lst.append(1)
        >>> lst.append(2)
        >>> lst.append(3)
        >>> lst.remove_at(1)
        2
        >>> list(lst)
        [1, 3]

        Notes
        -----
        Time complexity: O(n)
        """
        if self.is_empty():
            raise EmptyStructureError("Cannot remove from empty list")

        if index < 0:
            index += self._size

        if index < 0 or index >= self._size:
            raise SDSIndexError(f"Index {index} out of range")

        if index == 0:
            return self.remove_first()

        prev_node = self._get_node(index - 1)
        target: SimpleNode = cast(SimpleNode, prev_node.next)
        data = target.data
        prev_node.next = target.next
        self._size -= 1
        return data

    def find(self, item: Any) -> int:
        """Find the index of the first occurrence of an item.

        Parameters
        ----------
        item : Any
            The item to find.

        Returns
        -------
        int
            The index of the item, or -1 if not found.

        Examples
        --------
        >>> lst = LinkedList()
        >>> lst.append(10)
        >>> lst.append(20)
        >>> lst.append(30)
        >>> lst.find(20)
        1
        >>> lst.find(99)
        -1

        Notes
        -----
        Time complexity: O(n)
        """
        current = self._head
        index = 0

        while current is not None:
            if current.data == item:
                return index
            current = current.next
            index += 1

        return -1

    def reverse(self) -> None:
        """Reverse the list in place.

        Examples
        --------
        >>> lst = LinkedList()
        >>> lst.append(1)
        >>> lst.append(2)
        >>> lst.append(3)
        >>> list(lst)
        [1, 2, 3]
        >>> lst.reverse()
        >>> list(lst)
        [3, 2, 1]

        Notes
        -----
        Time complexity: O(n)
        Space complexity: O(1)
        """
        prev = None
        current = self._head

        while current is not None:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node

        self._head = prev


class DoublyLinkedList(AbstractLinkedList):
    """A doubly linked list implementation.

    A doubly linked list is a linear collection where each element (node) contains
    data and references to both the next and previous nodes in the sequence.
    This implementation maintains both head and tail pointers for efficient
    operations at both ends.

    Attributes
    ----------
    head : DoublyNode or None
        The first node in the list (read-only property).
    tail : DoublyNode or None
        The last node in the list (read-only property).
    size : int
        The number of elements in the list (read-only property).

    Time Complexity
    ---------------
    - Access by index: O(n), optimized to O(n/2) by starting from nearest end
    - Search: O(n)
    - Insert at beginning (prepend): O(1)
    - Insert at end (append): O(1)
    - Delete at beginning: O(1)
    - Delete at end: O(1)

    Examples
    --------
    Create and populate a list:

    >>> dll = DoublyLinkedList()
    >>> dll.append(1)
    >>> dll.append(2)
    >>> dll.append(3)
    >>> len(dll)
    3

    Bidirectional traversal:

    >>> list(dll)
    [1, 2, 3]
    >>> list(reversed(dll))
    [3, 2, 1]

    Efficient operations at both ends:

    >>> dll.prepend(0)
    >>> dll.append(4)
    >>> dll.remove_first()
    0
    >>> dll.remove_last()
    4
    >>> list(dll)
    [1, 2, 3]

    Notes
    -----
    The doubly linked structure allows for O(1) operations at both ends and
    enables backward traversal. This comes at the cost of additional memory
    per node (for the prev pointer) and more complex link management.

    See Also
    --------
    LinkedList : Singly linked list with simpler structure.
    Deque : Uses doubly linked list for double-ended queue operations.
    """

    def __init__(self):
        """Initialize an empty doubly linked list."""
        super().__init__()
        self._head: Optional[DoublyNode] = None
        self._tail: Optional[DoublyNode] = None

    @property
    def head(self) -> Optional[DoublyNode]:
        """Get the first node in the list.

        Returns
        -------
        DoublyNode or None
            The first node, or None if the list is empty.

        Examples
        --------
        >>> dll = DoublyLinkedList()
        >>> dll.head is None
        True
        >>> dll.append(1)
        >>> dll.head.data
        1

        Notes
        -----
        This property is read-only.
        """
        return self._head

    @property
    def tail(self) -> Optional[DoublyNode]:
        """Get the last node in the list.

        Returns
        -------
        DoublyNode or None
            The last node, or None if the list is empty.

        Examples
        --------
        >>> dll = DoublyLinkedList()
        >>> dll.tail is None
        True
        >>> dll.append(1)
        >>> dll.append(2)
        >>> dll.tail.data
        2

        Notes
        -----
        This property is read-only.
        """
        return self._tail

    def clear(self) -> None:
        """Remove all elements from the list.

        Examples
        --------
        >>> dll = DoublyLinkedList()
        >>> dll.append(1)
        >>> dll.append(2)
        >>> dll.clear()
        >>> dll.is_empty()
        True

        Notes
        -----
        Time complexity: O(1)
        """
        self._head = None
        self._tail = None
        self._size = 0

    def __iter__(self) -> Iterator[Any]:
        """Iterate over the elements in forward direction.

        Yields
        ------
        Any
            Elements from head to tail.

        Examples
        --------
        >>> dll = DoublyLinkedList()
        >>> dll.append(1)
        >>> dll.append(2)
        >>> dll.append(3)
        >>> list(dll)
        [1, 2, 3]

        Notes
        -----
        Time complexity: O(n) for complete iteration
        """
        current = self._head
        while current is not None:
            yield current.data
            current = current.next

    def __reversed__(self) -> Iterator[Any]:
        """Iterate over the elements in backward direction.

        Yields
        ------
        Any
            Elements from tail to head.

        Examples
        --------
        >>> dll = DoublyLinkedList()
        >>> dll.append(1)
        >>> dll.append(2)
        >>> dll.append(3)
        >>> list(reversed(dll))
        [3, 2, 1]

        Notes
        -----
        Time complexity: O(n) for complete iteration
        """
        current = self._tail
        while current is not None:
            yield current.data
            current = current.prev

    def __contains__(self, item: Any) -> bool:
        """Return True if item is in the list.

        Parameters
        ----------
        item : Any
            The item to search for.

        Returns
        -------
        bool
            True if found, False otherwise.

        Examples
        --------
        >>> dll = DoublyLinkedList()
        >>> dll.append(1)
        >>> 1 in dll
        True
        >>> 2 in dll
        False

        Notes
        -----
        Time complexity: O(n)
        """
        for data in self:
            if data == item:
                return True
        return False

    def __repr__(self) -> str:
        """Return a detailed string representation.

        Returns
        -------
        str
            String in the form "DoublyLinkedList([item1, item2, ...])".

        Examples
        --------
        >>> dll = DoublyLinkedList()
        >>> dll.append(1)
        >>> dll.append(2)
        >>> repr(dll)
        'DoublyLinkedList([1, 2])'
        """
        elements = ", ".join(repr(item) for item in self)
        return f"DoublyLinkedList([{elements}])"

    def __str__(self) -> str:
        """Return a simple string representation.

        Returns
        -------
        str
            String showing bidirectional structure.

        Examples
        --------
        >>> dll = DoublyLinkedList()
        >>> dll.append(1)
        >>> dll.append(2)
        >>> str(dll)
        '[1 <-> 2]'
        """
        elements = " <-> ".join(str(item) for item in self)
        return f"[{elements}]" if elements else "[]"

    def __getitem__(self, index: int) -> Any:
        """Get the item at the specified index.

        Parameters
        ----------
        index : int
            The index (supports negative indexing).

        Returns
        -------
        Any
            The item at the specified index.

        Raises
        ------
        IndexError
            If the index is out of range.

        Examples
        --------
        >>> dll = DoublyLinkedList()
        >>> dll.append(10)
        >>> dll.append(20)
        >>> dll[0]
        10
        >>> dll[-1]
        20

        Notes
        -----
        Time complexity: O(n), optimized to O(n/2) by starting from nearest end
        """
        node = self._get_node(index)
        return node.data

    def __setitem__(self, index: int, value: Any) -> None:
        """Set the item at the specified index.

        Parameters
        ----------
        index : int
            The index (supports negative indexing).
        value : Any
            The new value.

        Raises
        ------
        IndexError
            If the index is out of range.

        Examples
        --------
        >>> dll = DoublyLinkedList()
        >>> dll.append(10)
        >>> dll[0] = 100
        >>> dll[0]
        100

        Notes
        -----
        Time complexity: O(n), optimized to O(n/2)
        """
        node = self._get_node(index)
        node.data = value

    def _get_node(self, index: int) -> DoublyNode:
        """Get the node at the specified index.

        Optimizes by starting from head or tail depending on index.

        Parameters
        ----------
        index : int
            The index (supports negative indexing).

        Returns
        -------
        DoublyNode
            The node at the specified index.

        Raises
        ------
        IndexError
            If the list is empty or index is out of range.

        Notes
        -----
        Time complexity: O(n/2) due to bidirectional optimization
        """
        if self.is_empty():
            raise SDSIndexError("List is empty")

        # Handle negative indices
        if index < 0:
            index += self._size

        if index < 0 or index >= self._size:
            raise SDSIndexError(
                f"Index {index} out of range for list of size {self._size}"
            )

        # Optimize: start from head or tail depending on index
        if index < self._size // 2:
            # Start from head (non-empty ensured by checks above)
            current: DoublyNode = cast(DoublyNode, self._head)
            for _ in range(index):
                current = cast(DoublyNode, current.next)
        else:
            # Start from tail
            current = cast(DoublyNode, self._tail)
            for _ in range(self._size - index - 1):
                current = cast(DoublyNode, current.prev)

        return current

    def prepend(self, item: Any) -> None:
        """Add an item to the beginning of the list.

        Parameters
        ----------
        item : Any
            The item to add.

        Examples
        --------
        >>> dll = DoublyLinkedList()
        >>> dll.prepend(3)
        >>> dll.prepend(2)
        >>> dll.prepend(1)
        >>> list(dll)
        [1, 2, 3]

        Notes
        -----
        Time complexity: O(1)
        """
        new_node = DoublyNode(item, next_node=self._head)

        if self.is_empty():
            self._tail = new_node
        else:
            head: DoublyNode = cast(DoublyNode, self._head)
            head.prev = new_node

        self._head = new_node
        self._size += 1

    def append(self, item: Any) -> None:
        """Add an item to the end of the list.

        Parameters
        ----------
        item : Any
            The item to add.

        Examples
        --------
        >>> dll = DoublyLinkedList()
        >>> dll.append(1)
        >>> dll.append(2)
        >>> dll.append(3)
        >>> list(dll)
        [1, 2, 3]

        Notes
        -----
        Time complexity: O(1)
        """
        new_node = DoublyNode(item, prev_node=self._tail)

        if self.is_empty():
            self._head = new_node
        else:
            tail: DoublyNode = cast(DoublyNode, self._tail)
            tail.next = new_node

        self._tail = new_node
        self._size += 1

    def insert_at(self, index: int, item: Any) -> None:
        """Insert an item at the specified index.

        Parameters
        ----------
        index : int
            The index where to insert.
        item : Any
            The item to insert.

        Raises
        ------
        IndexError
            If the index is out of range.

        Examples
        --------
        >>> dll = DoublyLinkedList()
        >>> dll.append(1)
        >>> dll.append(3)
        >>> dll.insert_at(1, 2)
        >>> list(dll)
        [1, 2, 3]

        Notes
        -----
        Time complexity: O(n)
        """
        if index < 0:
            index += self._size

        if index < 0 or index > self._size:
            raise SDSIndexError(f"Index {index} out of range for insertion")

        if index == 0:
            self.prepend(item)
        elif index == self._size:
            self.append(item)
        else:
            next_node = self._get_node(index)
            prev_node = cast(DoublyNode, next_node.prev)
            new_node = DoublyNode(item, next_node=next_node, prev_node=prev_node)
            prev_node.next = new_node
            next_node.prev = new_node
            self._size += 1

    def remove_first(self) -> Any:
        """Remove and return the first item from the list.

        Returns
        -------
        Any
            The removed item.

        Raises
        ------
        EmptyStructureError
            If the list is empty.

        Examples
        --------
        >>> dll = DoublyLinkedList()
        >>> dll.append(1)
        >>> dll.append(2)
        >>> dll.remove_first()
        1
        >>> list(dll)
        [2]

        Notes
        -----
        Time complexity: O(1)
        """
        if self.is_empty():
            raise EmptyStructureError("Cannot remove from empty list")

        head: DoublyNode = cast(DoublyNode, self._head)
        data = head.data
        self._head = head.next

        if self._head is None:
            self._tail = None
        else:
            cast(DoublyNode, self._head).prev = None

        self._size -= 1
        return data

    def remove_last(self) -> Any:
        """Remove and return the last item from the list.

        Returns
        -------
        Any
            The removed item.

        Raises
        ------
        EmptyStructureError
            If the list is empty.

        Examples
        --------
        >>> dll = DoublyLinkedList()
        >>> dll.append(1)
        >>> dll.append(2)
        >>> dll.remove_last()
        2
        >>> list(dll)
        [1]

        Notes
        -----
        Time complexity: O(1)
        """
        if self.is_empty():
            raise EmptyStructureError("Cannot remove from empty list")

        tail: DoublyNode = cast(DoublyNode, self._tail)
        data = tail.data
        self._tail = tail.prev

        if self._tail is None:
            self._head = None
        else:
            cast(DoublyNode, self._tail).next = None

        self._size -= 1
        return data

    def remove(self, item: Any) -> Any:
        """Remove the first occurrence of an item from the list.

        Parameters
        ----------
        item : Any
            The item to remove.

        Returns
        -------
        Any
            The removed item.

        Raises
        ------
        EmptyStructureError
            If the list is empty.
        ValueError
            If the item is not found.

        Examples
        --------
        >>> dll = DoublyLinkedList()
        >>> dll.append(1)
        >>> dll.append(2)
        >>> dll.append(3)
        >>> dll.remove(2)
        2
        >>> list(dll)
        [1, 3]

        Notes
        -----
        Time complexity: O(n)
        """
        if self.is_empty():
            raise EmptyStructureError("Cannot remove from empty list")

        current = self._head

        while current is not None:
            if current.data == item:
                # Update links
                if current.prev is not None:
                    current.prev.next = current.next
                else:
                    self._head = current.next

                if current.next is not None:
                    current.next.prev = current.prev
                else:
                    self._tail = current.prev

                self._size -= 1
                return current.data

            current = current.next

        raise ValueError(f"Item {item} not found in list")

    def remove_at(self, index: int) -> Any:
        """Remove and return the item at the specified index.

        Parameters
        ----------
        index : int
            The index of the item to remove.

        Returns
        -------
        Any
            The removed item.

        Raises
        ------
        EmptyStructureError
            If the list is empty.
        IndexError
            If the index is out of range.

        Examples
        --------
        >>> dll = DoublyLinkedList()
        >>> dll.append(1)
        >>> dll.append(2)
        >>> dll.append(3)
        >>> dll.remove_at(1)
        2
        >>> list(dll)
        [1, 3]

        Notes
        -----
        Time complexity: O(n)
        """
        if self.is_empty():
            raise EmptyStructureError("Cannot remove from empty list")

        if index < 0:
            index += self._size

        if index < 0 or index >= self._size:
            raise SDSIndexError(f"Index {index} out of range")

        if index == 0:
            return self.remove_first()
        elif index == self._size - 1:
            return self.remove_last()

        node = self._get_node(index)
        # Since index is neither first nor last, both prev and next exist
        prev_node: DoublyNode = cast(DoublyNode, node.prev)
        next_node: DoublyNode = cast(DoublyNode, node.next)
        prev_node.next = next_node
        next_node.prev = prev_node
        self._size -= 1
        return node.data

    def find(self, item: Any) -> int:
        """Find the index of the first occurrence of an item.

        Parameters
        ----------
        item : Any
            The item to find.

        Returns
        -------
        int
            The index of the item, or -1 if not found.

        Examples
        --------
        >>> dll = DoublyLinkedList()
        >>> dll.append(10)
        >>> dll.append(20)
        >>> dll.append(30)
        >>> dll.find(20)
        1
        >>> dll.find(99)
        -1

        Notes
        -----
        Time complexity: O(n)
        """
        current = self._head
        index = 0

        while current is not None:
            if current.data == item:
                return index
            current = current.next
            index += 1

        return -1

    def reverse(self) -> None:
        """Reverse the list in place.

        Examples
        --------
        >>> dll = DoublyLinkedList()
        >>> dll.append(1)
        >>> dll.append(2)
        >>> dll.append(3)
        >>> list(dll)
        [1, 2, 3]
        >>> dll.reverse()
        >>> list(dll)
        [3, 2, 1]

        Notes
        -----
        Time complexity: O(n)
        Space complexity: O(1)
        """
        current = self._head
        self._head, self._tail = self._tail, self._head

        while current is not None:
            # Swap next and prev
            current.next, current.prev = current.prev, current.next
            current = current.prev  # Move to next (which is now prev)


class CircularLinkedList(AbstractLinkedList):
    """A circular singly linked list implementation.

    A circular linked list is a variation of a linked list where the last node
    points back to the first node, forming a circle. This implementation
    maintains a tail pointer for efficient operations at both ends.

    Attributes
    ----------
    tail : Node or None
        The last node in the list (read-only property). The head is tail.next.
    head : Node or None
        The first node in the list (read-only property). Equivalent to tail.next.
    size : int
        The number of elements in the list (read-only property).

    Time Complexity
    ---------------
    - Access by index: O(n)
    - Search: O(n)
    - Insert at beginning: O(1)
    - Insert at end: O(1)
    - Delete at beginning: O(1)
    - Delete at end: O(n)
    - Rotate: O(1)

    Examples
    --------
    Create and populate a circular list:

    >>> cll = CircularLinkedList()
    >>> cll.append(1)
    >>> cll.append(2)
    >>> cll.append(3)
    >>> len(cll)
    3

    The list is circular - tail points to head:

    >>> cll.tail.next is cll.head
    True

    Rotate the list:

    >>> cll.rotate(1)  # Move forward by 1
    >>> list(cll)
    [2, 3, 1]
    >>> cll.rotate(-1)  # Move backward by 1
    >>> list(cll)
    [1, 2, 3]

    Notes
    -----
    The circular structure means the last node's next pointer is never None
    (except for an empty list). Iteration must explicitly stop after visiting
    all nodes to avoid infinite loops.

    See Also
    --------
    LinkedList : Singly linked list without circular connection.
    DoublyLinkedList : Doubly linked list with bidirectional traversal.
    """

    def __init__(self):
        """Initialize an empty circular linked list."""
        super().__init__()
        self._tail: Optional[SimpleNode] = None

    @property
    def tail(self) -> Optional[SimpleNode]:
        """Get the last node in the list.

        Returns
        -------
        SimpleNode or None
            The last node, or None if the list is empty.

        Examples
        --------
        >>> cll = CircularLinkedList()
        >>> cll.tail is None
        True
        >>> cll.append(1)
        >>> cll.append(2)
        >>> cll.tail.data
        2
        >>> cll.tail.next.data  # Points back to head
        1

        Notes
        -----
        The head can be accessed as tail.next when the list is not empty.
        This property is read-only.
        """
        return self._tail

    @property
    def head(self) -> Optional[SimpleNode]:
        """Get the first node in the list.

        Returns
        -------
        SimpleNode or None
            The first node (tail.next), or None if the list is empty.

        Examples
        --------
        >>> cll = CircularLinkedList()
        >>> cll.head is None
        True
        >>> cll.append(1)
        >>> cll.head.data
        1

        Notes
        -----
        The head is always tail.next in a circular list.
        This property is read-only.
        """
        return self._tail.next if self._tail else None

    def clear(self) -> None:
        """Remove all elements from the list.

        Examples
        --------
        >>> cll = CircularLinkedList()
        >>> cll.append(1)
        >>> cll.append(2)
        >>> cll.clear()
        >>> cll.is_empty()
        True

        Notes
        -----
        Time complexity: O(1)
        """
        self._tail = None
        self._size = 0

    def __iter__(self) -> Iterator[Any]:
        """Iterate over the elements in the list.

        Yields
        ------
        Any
            Elements from the list in order, iterating exactly once through the circle.

        Examples
        --------
        >>> cll = CircularLinkedList()
        >>> cll.append(1)
        >>> cll.append(2)
        >>> cll.append(3)
        >>> list(cll)
        [1, 2, 3]

        Notes
        -----
        Time complexity: O(n) for complete iteration
        The iteration explicitly stops after visiting all nodes to prevent
        infinite loops.
        """
        if self.is_empty():
            return

        current: SimpleNode = cast(SimpleNode, self.head)
        for _ in range(self._size):
            yield current.data
            current = cast(SimpleNode, current.next)

    def __contains__(self, item: Any) -> bool:
        """Return True if item is in the list.

        Parameters
        ----------
        item : Any
            The item to search for.

        Returns
        -------
        bool
            True if the item is found, False otherwise.

        Examples
        --------
        >>> cll = CircularLinkedList()
        >>> cll.append(1)
        >>> cll.append(2)
        >>> 1 in cll
        True
        >>> 3 in cll
        False

        Notes
        -----
        Time complexity: O(n)
        """
        for data in self:
            if data == item:
                return True
        return False

    def __repr__(self) -> str:
        """Return a detailed string representation of the list.

        Returns
        -------
        str
            String in the form "CircularLinkedList([item1, item2, ...])".

        Examples
        --------
        >>> cll = CircularLinkedList()
        >>> cll.append(1)
        >>> cll.append(2)
        >>> repr(cll)
        'CircularLinkedList([1, 2])'
        """
        elements = ", ".join(repr(item) for item in self)
        return f"CircularLinkedList([{elements}])"

    def __str__(self) -> str:
        """Return a simple string representation of the list.

        Returns
        -------
        str
            String showing the circular structure.

        Examples
        --------
        >>> cll = CircularLinkedList()
        >>> cll.append(1)
        >>> cll.append(2)
        >>> str(cll)
        '[1 -> 2 -> (circular)]'
        """
        if self.is_empty():
            return "[]"
        elements = " -> ".join(str(item) for item in self)
        return f"[{elements} -> (circular)]"

    def __getitem__(self, index: int) -> Any:
        """Get the item at the specified index.

        Parameters
        ----------
        index : int
            The index (supports negative indexing).

        Returns
        -------
        Any
            The item at the specified index.

        Raises
        ------
        IndexError
            If the index is out of range.

        Examples
        --------
        >>> cll = CircularLinkedList()
        >>> cll.append(10)
        >>> cll.append(20)
        >>> cll.append(30)
        >>> cll[0]
        10
        >>> cll[-1]
        30

        Notes
        -----
        Time complexity: O(n)
        """
        node = self._get_node(index)
        return node.data

    def __setitem__(self, index: int, value: Any) -> None:
        """Set the item at the specified index.

        Parameters
        ----------
        index : int
            The index (supports negative indexing).
        value : Any
            The new value.

        Raises
        ------
        IndexError
            If the index is out of range.

        Examples
        --------
        >>> cll = CircularLinkedList()
        >>> cll.append(10)
        >>> cll.append(20)
        >>> cll[0] = 100
        >>> cll[0]
        100

        Notes
        -----
        Time complexity: O(n)
        """
        node = self._get_node(index)
        node.data = value

    def _get_node(self, index: int) -> SimpleNode:
        """Get the node at the specified index.

        This is an internal helper method.

        Parameters
        ----------
        index : int
            The index (supports negative indexing).

        Returns
        -------
        SimpleNode
            The node at the specified index.

        Raises
        ------
        IndexError
            If the list is empty or index is out of range.

        Notes
        -----
        Time complexity: O(n)
        """
        if self.is_empty():
            raise SDSIndexError("List is empty")

        # Handle negative indices
        if index < 0:
            index += self._size

        if index < 0 or index >= self._size:
            raise SDSIndexError(
                f"Index {index} out of range for list of size {self._size}"
            )

        current: SimpleNode = cast(SimpleNode, self.head)
        for _ in range(index):
            current = cast(SimpleNode, current.next)

        return current

    def prepend(self, item: Any) -> None:
        """Add an item to the beginning of the list.

        Parameters
        ----------
        item : Any
            The item to add.

        Examples
        --------
        >>> cll = CircularLinkedList()
        >>> cll.prepend(3)
        >>> cll.prepend(2)
        >>> cll.prepend(1)
        >>> list(cll)
        [1, 2, 3]

        Notes
        -----
        Time complexity: O(1)
        """
        new_node = SimpleNode(item)

        if self.is_empty():
            new_node.next = new_node  # Point to itself
            self._tail = new_node
        else:
            new_node.next = cast(SimpleNode, self.head)
            cast(SimpleNode, self._tail).next = new_node

        self._size += 1

    def append(self, item: Any) -> None:
        """Add an item to the end of the list.

        Parameters
        ----------
        item : Any
            The item to add.

        Examples
        --------
        >>> cll = CircularLinkedList()
        >>> cll.append(1)
        >>> cll.append(2)
        >>> cll.append(3)
        >>> list(cll)
        [1, 2, 3]

        Notes
        -----
        Time complexity: O(1)
        """
        new_node = SimpleNode(item)

        if self.is_empty():
            new_node.next = new_node  # Point to itself
            self._tail = new_node
        else:
            new_node.next = cast(SimpleNode, self.head)
            cast(SimpleNode, self._tail).next = new_node
            self._tail = new_node

        self._size += 1

    def insert_at(self, index: int, item: Any) -> None:
        """Insert an item at the specified index.

        Parameters
        ----------
        index : int
            The index where to insert (0 <= index <= size).
        item : Any
            The item to insert.

        Raises
        ------
        IndexError
            If the index is out of range.

        Examples
        --------
        >>> cll = CircularLinkedList()
        >>> cll.append(1)
        >>> cll.append(3)
        >>> cll.insert_at(1, 2)
        >>> list(cll)
        [1, 2, 3]

        Notes
        -----
        Time complexity: O(n)
        """
        if index < 0:
            index += self._size

        if index < 0 or index > self._size:
            raise SDSIndexError(f"Index {index} out of range for insertion")

        if index == 0:
            self.prepend(item)
        elif index == self._size:
            self.append(item)
        else:
            prev_node = self._get_node(index - 1)
            next_node: Optional[SimpleNode] = prev_node.next
            new_node = SimpleNode(item, next_node)
            prev_node.next = new_node
            self._size += 1

    def remove_first(self) -> Any:
        """Remove and return the first item from the list.

        Returns
        -------
        Any
            The removed item.

        Raises
        ------
        EmptyStructureError
            If the list is empty.

        Examples
        --------
        >>> cll = CircularLinkedList()
        >>> cll.append(1)
        >>> cll.append(2)
        >>> cll.remove_first()
        1
        >>> list(cll)
        [2]

        Notes
        -----
        Time complexity: O(1)
        """
        if self.is_empty():
            raise EmptyStructureError("Cannot remove from empty list")

        head: SimpleNode = cast(SimpleNode, self.head)
        data = head.data

        if self._size == 1:
            self._tail = None
        else:
            cast(SimpleNode, self._tail).next = cast(SimpleNode, head.next)

        self._size -= 1
        return data

    def remove_last(self) -> Any:
        """Remove and return the last item from the list.

        Returns
        -------
        Any
            The removed item.

        Raises
        ------
        EmptyStructureError
            If the list is empty.

        Examples
        --------
        >>> cll = CircularLinkedList()
        >>> cll.append(1)
        >>> cll.append(2)
        >>> cll.remove_last()
        2
        >>> list(cll)
        [1]

        Notes
        -----
        Time complexity: O(n)
        Must traverse to find the second-to-last node.
        """
        if self.is_empty():
            raise EmptyStructureError("Cannot remove from empty list")

        if self._size == 1:
            return self.remove_first()

        # Find second to last node
        current: SimpleNode = cast(SimpleNode, self.head)
        while current.next != self._tail:
            current = cast(SimpleNode, current.next)

        data = cast(SimpleNode, self._tail).data
        current.next = cast(SimpleNode, self.head)
        self._tail = current
        self._size -= 1
        return data

    def remove(self, item: Any) -> Any:
        """Remove the first occurrence of an item from the list.

        Parameters
        ----------
        item : Any
            The item to remove.

        Returns
        -------
        Any
            The removed item.

        Raises
        ------
        EmptyStructureError
            If the list is empty.
        ValueError
            If the item is not found.

        Examples
        --------
        >>> cll = CircularLinkedList()
        >>> cll.append(1)
        >>> cll.append(2)
        >>> cll.append(3)
        >>> cll.remove(2)
        2
        >>> list(cll)
        [1, 3]

        Notes
        -----
        Time complexity: O(n)
        """
        if self.is_empty():
            raise EmptyStructureError("Cannot remove from empty list")

        if cast(SimpleNode, self.head).data == item:
            return self.remove_first()

        current: SimpleNode = cast(SimpleNode, self.head)
        for _ in range(self._size - 1):
            nxt: SimpleNode = cast(SimpleNode, current.next)
            if nxt.data == item:
                data = nxt.data
                if nxt == self._tail:
                    self._tail = current
                current.next = nxt.next
                self._size -= 1
                return data
            current = nxt

        raise ValueError(f"Item {item} not found in list")

    def remove_at(self, index: int) -> Any:
        """Remove and return the item at the specified index.

        Parameters
        ----------
        index : int
            The index of the item to remove.

        Returns
        -------
        Any
            The removed item.

        Raises
        ------
        EmptyStructureError
            If the list is empty.
        IndexError
            If the index is out of range.

        Examples
        --------
        >>> cll = CircularLinkedList()
        >>> cll.append(1)
        >>> cll.append(2)
        >>> cll.append(3)
        >>> cll.remove_at(1)
        2
        >>> list(cll)
        [1, 3]

        Notes
        -----
        Time complexity: O(n)
        """
        if self.is_empty():
            raise EmptyStructureError("Cannot remove from empty list")

        if index < 0:
            index += self._size

        if index < 0 or index >= self._size:
            raise SDSIndexError(f"Index {index} out of range")

        if index == 0:
            return self.remove_first()

        prev_node = self._get_node(index - 1)
        target: SimpleNode = cast(SimpleNode, prev_node.next)
        data = target.data

        if target == self._tail:
            self._tail = prev_node

        prev_node.next = target.next
        self._size -= 1
        return data

    def find(self, item: Any) -> int:
        """Find the index of the first occurrence of an item.

        Parameters
        ----------
        item : Any
            The item to find.

        Returns
        -------
        int
            The index of the item, or -1 if not found.

        Examples
        --------
        >>> cll = CircularLinkedList()
        >>> cll.append(10)
        >>> cll.append(20)
        >>> cll.append(30)
        >>> cll.find(20)
        1
        >>> cll.find(99)
        -1

        Notes
        -----
        Time complexity: O(n)
        """
        if self.is_empty():
            return -1

        current: SimpleNode = cast(SimpleNode, self.head)
        for index in range(self._size):
            if current.data == item:
                return index
            current = cast(SimpleNode, current.next)

        return -1

    def reverse(self) -> None:
        """Reverse the list in place.

        Examples
        --------
        >>> cll = CircularLinkedList()
        >>> cll.append(1)
        >>> cll.append(2)
        >>> cll.append(3)
        >>> list(cll)
        [1, 2, 3]
        >>> cll.reverse()
        >>> list(cll)
        [3, 2, 1]

        Notes
        -----
        Time complexity: O(n)
        Space complexity: O(1)
        The circular structure is maintained after reversal.
        """
        if self.is_empty() or self._size == 1:
            return

        prev: SimpleNode = cast(SimpleNode, self._tail)
        current: SimpleNode = cast(SimpleNode, self.head)
        new_tail: SimpleNode = current

        for _ in range(self._size):
            next_node: SimpleNode = cast(SimpleNode, current.next)
            current.next = prev
            prev = current
            current = next_node

        self._tail = new_tail

    def rotate(self, steps: int = 1) -> None:
        """Rotate the list by moving the tail forward by steps positions.

        Positive steps rotate forward (tail moves right), negative steps
        rotate backward (tail moves left).

        Parameters
        ----------
        steps : int, optional
            Number of positions to rotate. Default is 1.
            Positive for forward, negative for backward.

        Examples
        --------
        >>> cll = CircularLinkedList()
        >>> cll.append(1)
        >>> cll.append(2)
        >>> cll.append(3)
        >>> list(cll)
        [1, 2, 3]

        Rotate forward:

        >>> cll.rotate(1)
        >>> list(cll)
        [2, 3, 1]

        Rotate backward:

        >>> cll.rotate(-1)
        >>> list(cll)
        [1, 2, 3]

        Notes
        -----
        Time complexity: O(steps % size)
        This operation is very efficient for circular lists as it only
        requires moving the tail pointer.

        Rotating by size (or multiples of size) returns to the same state.
        """
        if self.is_empty() or self._size == 1:
            return

        # Normalize steps to be within [0, size)
        steps = steps % self._size

        # Move tail forward by steps positions
        for _ in range(steps):
            self._tail = cast(SimpleNode, cast(SimpleNode, self._tail).next)
