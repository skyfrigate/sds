"""Abstract base classes for linked list data structures.

This module provides the abstract base class for linked list implementations.
All concrete linked list types (singly, doubly, circular) inherit from this
base class to ensure a consistent interface.

Classes
-------
AbstractLinkedList
    Abstract base class defining the interface for all linked list implementations.

Examples
--------
Creating a custom linked list implementation:

>>> from sds.linear.interfaces import AbstractLinkedList
>>> class MyList(AbstractLinkedList):
...     def __init__(self):
...         super().__init__()
...         self._head = None
...         self._size = 0
...     # Implement all abstract methods...

Notes
-----
This module is part of the linear data structures package and builds upon
the generic LinearCollection interface from sds.core.interfaces.

See Also
--------
sds.core.interfaces : Generic collection interfaces.
sds.linear.list : Concrete linked list implementations.
"""

from abc import abstractmethod
from typing import Any

from ..core.interfaces import LinearCollection


class AbstractLinkedList(LinearCollection):
    """Abstract base class for linked list implementations.

    This class defines the common interface that all linked list variants
    (singly linked, doubly linked, circular) must implement. It extends
    LinearCollection with list-specific operations like indexed access,
    insertion, and specialized removal methods.

    All concrete linked list implementations should inherit from this class
    and provide implementations for all abstract methods.

    Attributes
    ----------
    size : int
        The number of elements in the list (read-only property).

    Methods
    -------
    prepend(item)
        Add an item to the beginning of the list.
    append(item)
        Add an item to the end of the list.
    insert_at(index, item)
        Insert an item at a specific index.
    remove_first()
        Remove and return the first item.
    remove_last()
        Remove and return the last item.
    remove_at(index)
        Remove and return the item at a specific index.
    find(item)
        Find the index of an item.
    reverse()
        Reverse the list in place.
    __getitem__(index)
        Get item at index.
    __setitem__(index, value)
        Set item at index.

    Examples
    --------
    Any concrete linked list can be used polymorphically:

    >>> def process_list(lst: AbstractLinkedList):
    ...     lst.append(1)
    ...     lst.prepend(0)
    ...     return len(lst)

    >>> from sds.linear.list import LinkedList, DoublyLinkedList
    >>> process_list(LinkedList())
    2
    >>> process_list(DoublyLinkedList())
    2

    Notes
    -----
    This class is abstract and cannot be instantiated directly. Concrete
    subclasses must implement all abstract methods.

    The size property is defined here but relies on subclasses to maintain
    an internal _size attribute.

    See Also
    --------
    LinearCollection : Parent interface for linear data structures.
    LinkedList : Singly linked list implementation.
    DoublyLinkedList : Doubly linked list implementation.
    CircularLinkedList : Circular linked list implementation.
    """

    def __init__(self):
        """Initialize the abstract linked list.

        Subclasses should call this via super().__init__() and then
        initialize their own internal attributes.
        """
        self._size = 0

    @property
    def size(self) -> int:
        """Get the number of elements in the list.

        This is a read-only property. The size is maintained internally
        and updated automatically by add/remove operations.

        Returns
        -------
        int
            The number of elements currently in the list.

        Examples
        --------
        >>> lst = LinkedList()
        >>> lst.size
        0
        >>> lst.append(1)
        >>> lst.size
        1

        Notes
        -----
        This property provides O(1) access to the list size without
        needing to traverse the entire list.

        See Also
        --------
        __len__ : Returns the same value, allowing use of len(list).
        """
        return self._size

    @abstractmethod
    def prepend(self, item: Any) -> None:
        """Add an item to the beginning of the list.

        Parameters
        ----------
        item : Any
            The item to add to the beginning of the list.

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
        This operation should be O(1) for all linked list implementations.

        See Also
        --------
        append : Add an item to the end of the list.
        insert_at : Insert an item at a specific position.
        """
        pass

    @abstractmethod
    def append(self, item: Any) -> None:
        """Add an item to the end of the list.

        Parameters
        ----------
        item : Any
            The item to add to the end of the list.

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
        Time complexity varies by implementation:
        - Singly linked list without tail: O(n)
        - Doubly linked list with tail: O(1)

        See Also
        --------
        prepend : Add an item to the beginning of the list.
        insert_at : Insert an item at a specific position.
        """
        pass

    @abstractmethod
    def insert_at(self, index: int, item: Any) -> None:
        """Insert an item at the specified index.

        All items at and after the specified index are shifted to the right.
        Negative indices are supported and count from the end of the list.

        Parameters
        ----------
        index : int
            The position at which to insert the item. Must satisfy
            -len(list) <= index <= len(list).
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
        >>> lst.insert_at(1, 2)  # Insert 2 between 1 and 3
        >>> list(lst)
        [1, 2, 3]

        Negative indices work from the end:

        >>> lst.insert_at(-1, 2.5)  # Insert before the last element
        >>> list(lst)
        [1, 2, 2.5, 3]

        Notes
        -----
        Time complexity is O(n) as it requires traversing to the insertion point.

        See Also
        --------
        prepend : Optimized insertion at the beginning (O(1)).
        append : Insertion at the end.
        remove_at : Remove an item at a specific index.
        """
        pass

    @abstractmethod
    def remove_first(self) -> Any:
        """Remove and return the first item from the list.

        Returns
        -------
        Any
            The item that was at the beginning of the list.

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
        This operation is O(1) for all linked list implementations.

        See Also
        --------
        remove_last : Remove the last item.
        remove_at : Remove an item at a specific index.
        prepend : Add an item to the beginning.
        """
        pass

    @abstractmethod
    def remove_last(self) -> Any:
        """Remove and return the last item from the list.

        Returns
        -------
        Any
            The item that was at the end of the list.

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
        Time complexity varies by implementation:
        - Singly linked list: O(n) - must traverse to find second-to-last node
        - Doubly linked list with tail: O(1)

        See Also
        --------
        remove_first : Remove the first item.
        remove_at : Remove an item at a specific index.
        append : Add an item to the end.
        """
        pass

    @abstractmethod
    def remove_at(self, index: int) -> Any:
        """Remove and return the item at the specified index.

        Negative indices are supported and count from the end of the list.

        Parameters
        ----------
        index : int
            The position of the item to remove. Must satisfy
            -len(list) <= index < len(list).

        Returns
        -------
        Any
            The item that was removed.

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

        Negative indices:

        >>> lst.remove_at(-1)  # Remove last item
        3
        >>> list(lst)
        [1]

        Notes
        -----
        Time complexity is O(n) as it requires traversing to the removal point.

        See Also
        --------
        remove_first : Optimized removal at the beginning (O(1)).
        remove_last : Remove the last item.
        remove : Remove by value instead of index.
        """
        pass

    @abstractmethod
    def find(self, item: Any) -> int:
        """Find the index of the first occurrence of an item.

        Parameters
        ----------
        item : Any
            The item to search for.

        Returns
        -------
        int
            The index of the first occurrence of the item, or -1 if not found.

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
        Time complexity is O(n) as it requires linear search.
        The search stops at the first match.

        See Also
        --------
        __contains__ : Check if an item exists (returns bool).
        remove : Remove the first occurrence of an item.
        """
        pass

    @abstractmethod
    def reverse(self) -> None:
        """Reverse the list in place.

        This operation modifies the list itself rather than creating a new list.

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
        Time complexity is O(n) as all links must be reversed.
        Space complexity is O(1) as reversal is done in place.

        See Also
        --------
        __reversed__ : Return a reverse iterator (for doubly linked lists).
        """
        pass

    @abstractmethod
    def __getitem__(self, index: int) -> Any:
        """Get the item at the specified index.

        This enables list-style indexing: lst[index].
        Negative indices are supported and count from the end.

        Parameters
        ----------
        index : int
            The position of the item to retrieve. Must satisfy
            -len(list) <= index < len(list).

        Returns
        -------
        Any
            The item at the specified index.

        Raises
        ------
        EmptyStructureError
            If the list is empty.
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
        Time complexity is O(n) as linked lists don't support random access.
        For doubly linked lists, the implementation may optimize by starting
        from the tail for indices in the second half of the list.

        See Also
        --------
        __setitem__ : Set the item at a specific index.
        """
        pass

    @abstractmethod
    def __setitem__(self, index: int, value: Any) -> None:
        """Set the item at the specified index.

        This enables list-style assignment: lst[index] = value.
        Negative indices are supported and count from the end.

        Parameters
        ----------
        index : int
            The position of the item to update. Must satisfy
            -len(list) <= index < len(list).
        value : Any
            The new value to store at the index.

        Raises
        ------
        EmptyStructureError
            If the list is empty.
        IndexError
            If the index is out of range.

        Examples
        --------
        >>> lst = LinkedList()
        >>> lst.append(10)
        >>> lst.append(20)
        >>> lst[0] = 100
        >>> lst[1] = 200
        >>> list(lst)
        [100, 200]

        Negative indices:

        >>> lst[-1] = 999
        >>> list(lst)
        [100, 999]

        Notes
        -----
        Time complexity is O(n) as it requires traversing to the index.

        See Also
        --------
        __getitem__ : Get the item at a specific index.
        """
        pass

    def __len__(self) -> int:
        """Return the number of elements in the list.

        This method enables the use of Python's built-in len() function.

        Returns
        -------
        int
            The number of elements in the list.

        Examples
        --------
        >>> lst = LinkedList()
        >>> len(lst)
        0
        >>> lst.append(1)
        >>> len(lst)
        1

        Notes
        -----
        This is a concrete implementation that delegates to the size property.
        Subclasses don't need to override this method.

        Time complexity is O(1).

        See Also
        --------
        size : Property that returns the same value.
        is_empty : Check if the list is empty.
        """
        return self._size

    def is_empty(self) -> bool:
        """Return True if the list is empty.

        This is a concrete implementation provided for convenience.

        Returns
        -------
        bool
            True if the list contains no elements, False otherwise.

        Examples
        --------
        >>> lst = LinkedList()
        >>> lst.is_empty()
        True
        >>> lst.append(1)
        >>> lst.is_empty()
        False

        Notes
        -----
        Time complexity is O(1).

        See Also
        --------
        __len__ : Get the number of elements.
        __bool__ : Used in boolean contexts.
        """
        return self._size == 0

    def add(self, item: Any) -> None:
        """Add an item to the list.

        This is a concrete implementation that delegates to append().
        It's provided to satisfy the LinearCollection interface.

        Parameters
        ----------
        item : Any
            The item to add.

        Examples
        --------
        >>> lst = LinkedList()
        >>> lst.add(1)
        >>> lst.add(2)
        >>> list(lst)
        [1, 2]

        Notes
        -----
        This method is equivalent to append() and is provided for
        compatibility with the LinearCollection interface.

        See Also
        --------
        append : Explicitly add to the end.
        prepend : Add to the beginning.
        """
        self.append(item)
