"""Abstract base classes defining interfaces for data structures.

This module provides the foundational abstract base classes (ABCs) that define
the interfaces for all data structures in the sds library. These interfaces
ensure a consistent API across different implementations.

The hierarchy is:
- Collection: Base interface for all collections
- LinearCollection: Interface for linear data structures (lists, stacks, queues)

Classes
-------
Collection
    Abstract base class for all collections.
LinearCollection
    Abstract base class for linear data structures.

Examples
--------
Implementing a simple collection:

>>> from sds.core.interfaces import Collection
>>> class MyCollection(Collection):
...     def __init__(self):
...         self._items = []
...     def __len__(self):
...         return len(self._items)
...     def is_empty(self):
...         return len(self._items) == 0
...     def clear(self):
...         self._items.clear()
...     def __iter__(self):
...         return iter(self._items)
...     def __contains__(self, item):
...         return item in self._items

Notes
-----
All classes in this module are abstract base classes and cannot be instantiated
directly. They must be subclassed with concrete implementations of all abstract
methods.

See Also
--------
sds.linear : Linear data structure implementations.
sds.trees : Tree data structure implementations.
sds.graphs : Graph data structure implementations.
"""

from abc import ABC, abstractmethod
from typing import Any, Iterator


class Collection(ABC):
    """Abstract base class for all collections.

    Defines the minimal interface that all data structures must implement.
    This includes operations for querying size, checking emptiness, clearing,
    iterating, and checking membership.

    All concrete data structures in the sds library should inherit from this
    class or one of its subclasses.

    Methods
    -------
    __len__()
        Return the number of elements in the collection.
    is_empty()
        Return True if the collection is empty.
    clear()
        Remove all elements from the collection.
    __iter__()
        Return an iterator over the collection.
    __contains__(item)
        Return True if item is in the collection.
    __bool__()
        Return True if the collection is not empty.

    Examples
    --------
    Create a concrete implementation:

    >>> from sds.core.interfaces import Collection
    >>> class SimpleList(Collection):
    ...     def __init__(self):
    ...         self._data = []
    ...     def __len__(self):
    ...         return len(self._data)
    ...     def is_empty(self):
    ...         return len(self._data) == 0
    ...     def clear(self):
    ...         self._data.clear()
    ...     def __iter__(self):
    ...         return iter(self._data)
    ...     def __contains__(self, item):
    ...         return item in self._data
    ...     def add(self, item):
    ...         self._data.append(item)

    Use the collection:

    >>> lst = SimpleList()
    >>> lst.is_empty()
    True
    >>> lst.add(1)
    >>> lst.is_empty()
    False
    >>> len(lst)
    1
    >>> 1 in lst
    True

    Notes
    -----
    This class uses the Abstract Base Class (ABC) mechanism from the abc module.
    Attempting to instantiate Collection directly will raise a TypeError.

    The __bool__ method is implemented as a concrete method that delegates to
    is_empty(), so subclasses don't need to override it.

    See Also
    --------
    LinearCollection : Extended interface for linear data structures.
    """

    @abstractmethod
    def __len__(self) -> int:
        """Return the number of elements in the collection.

        Returns
        -------
        int
            The number of elements currently in the collection.

        Examples
        --------
        >>> collection = MyCollection()
        >>> len(collection)
        0
        >>> collection.add(1)
        >>> len(collection)
        1

        Notes
        -----
        This method enables the use of Python's built-in len() function.
        Implementations should return the count in O(1) time when possible.
        """
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        """Return True if the collection is empty, False otherwise.

        Returns
        -------
        bool
            True if the collection contains no elements, False otherwise.

        Examples
        --------
        >>> collection = MyCollection()
        >>> collection.is_empty()
        True
        >>> collection.add(1)
        >>> collection.is_empty()
        False

        Notes
        -----
        This is often more efficient and clearer than checking len(collection) == 0.
        Implementations should return the result in O(1) time.
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """Remove all elements from the collection.

        After this operation, the collection will be empty and len(collection)
        will return 0.

        Examples
        --------
        >>> collection = MyCollection()
        >>> collection.add(1)
        >>> collection.add(2)
        >>> len(collection)
        2
        >>> collection.clear()
        >>> len(collection)
        0
        >>> collection.is_empty()
        True

        Notes
        -----
        This operation should be implemented efficiently, ideally in O(1) time
        by simply resetting internal references rather than removing elements
        one by one.
        """
        pass

    @abstractmethod
    def __iter__(self) -> Iterator[Any]:
        """Return an iterator over the collection.

        Returns
        -------
        Iterator[Any]
            An iterator that yields elements from the collection.

        Examples
        --------
        >>> collection = MyCollection()
        >>> collection.add(1)
        >>> collection.add(2)
        >>> collection.add(3)
        >>> for item in collection:
        ...     print(item)
        1
        2
        3
        >>> list(collection)
        [1, 2, 3]

        Notes
        -----
        This method enables the use of Python's iteration protocol.
        The order of iteration is implementation-dependent and should be
        documented in concrete subclasses.
        """
        pass

    @abstractmethod
    def __contains__(self, item: Any) -> bool:
        """Return True if item is in the collection, False otherwise.

        Parameters
        ----------
        item : Any
            The item to search for in the collection.

        Returns
        -------
        bool
            True if the item is found, False otherwise.

        Examples
        --------
        >>> collection = MyCollection()
        >>> collection.add(1)
        >>> 1 in collection
        True
        >>> 2 in collection
        False

        Notes
        -----
        This method enables the use of Python's 'in' operator.
        The time complexity is implementation-dependent but is typically O(n)
        for unsorted collections and O(log n) or O(1) for sorted or hashed
        collections.
        """
        pass

    def __bool__(self) -> bool:
        """Return True if the collection is not empty, False otherwise.

        This method is implemented concretely and delegates to is_empty().
        Subclasses typically don't need to override this method.

        Returns
        -------
        bool
            True if the collection contains at least one element, False if empty.

        Examples
        --------
        >>> collection = MyCollection()
        >>> bool(collection)
        False
        >>> if not collection:
        ...     print("Collection is empty")
        Collection is empty
        >>> collection.add(1)
        >>> bool(collection)
        True
        >>> if collection:
        ...     print("Collection has items")
        Collection has items

        Notes
        -----
        This method enables truthiness testing of collections in conditional
        statements. An empty collection is considered False, a non-empty
        collection is considered True.
        """
        return not self.is_empty()


class LinearCollection(Collection):
    """Abstract base class for linear data structures.

    Extends Collection with operations specific to linear structures such as
    lists, stacks, queues, and deques. Linear collections maintain elements
    in a sequence with defined positions.

    Methods
    -------
    add(item)
        Add an item to the collection.
    remove(item)
        Remove and return an item from the collection.

    All methods from Collection are also available:
        __len__, is_empty, clear, __iter__, __contains__, __bool__

    Examples
    --------
    Create a concrete linear collection:

    >>> from sds.core.interfaces import LinearCollection
    >>> class SimpleStack(LinearCollection):
    ...     def __init__(self):
    ...         self._data = []
    ...     def __len__(self):
    ...         return len(self._data)
    ...     def is_empty(self):
    ...         return len(self._data) == 0
    ...     def clear(self):
    ...         self._data.clear()
    ...     def __iter__(self):
    ...         return iter(self._data)
    ...     def __contains__(self, item):
    ...         return item in self._data
    ...     def add(self, item):
    ...         self._data.append(item)
    ...     def remove(self, item):
    ...         return self._data.pop()

    Use the linear collection:

    >>> stack = SimpleStack()
    >>> stack.add(1)
    >>> stack.add(2)
    >>> stack.remove()
    2
    >>> stack.remove()
    1

    Notes
    -----
    This class extends Collection and inherits all its abstract methods.
    Concrete implementations must provide implementations for all abstract
    methods from both Collection and LinearCollection.

    The semantics of add() and remove() are intentionally generic to allow
    different linear structures to implement them according to their specific
    behavior (e.g., LIFO for stacks, FIFO for queues).

    See Also
    --------
    Collection : Base interface for all collections.
    sds.linear.LinkedList : Concrete linear collection implementation.
    sds.linear.Stack : LIFO linear collection.
    sds.linear.Queue : FIFO linear collection.
    """

    @abstractmethod
    def add(self, item: Any) -> None:
        """Add an item to the collection.

        The specific behavior (where the item is added) depends on the concrete
        implementation. For example:
        - Stack: adds to the top
        - Queue: adds to the rear
        - List: typically adds to the end

        Parameters
        ----------
        item : Any
            The item to add to the collection.

        Examples
        --------
        >>> collection = MyLinearCollection()
        >>> collection.add(1)
        >>> collection.add(2)
        >>> len(collection)
        2

        Notes
        -----
        This method should not raise an exception for typical usage.
        If the collection has a maximum capacity, implementations should
        raise FullStructureError when attempting to add to a full collection.

        See Also
        --------
        remove : Remove an item from the collection.
        """
        pass

    @abstractmethod
    def remove(self, item: Any) -> Any:
        """Remove and return an item from the collection.

        The specific behavior (which item is removed) depends on the concrete
        implementation. For example:
        - Stack: removes from the top (most recently added)
        - Queue: removes from the front (least recently added)
        - List: removes the specified item

        Parameters
        ----------
        item : Any
            The item to remove. The interpretation depends on the implementation:
            - For some structures (like lists), this is the value to find and remove
            - For others (like stacks/queues), this parameter might be ignored

        Returns
        -------
        Any
            The removed item.

        Raises
        ------
        EmptyStructureError
            If the collection is empty.
        ValueError
            If the item is not found (for structures that search for a specific item).

        Examples
        --------
        >>> collection = MyLinearCollection()
        >>> collection.add(1)
        >>> collection.add(2)
        >>> collection.remove(1)
        1
        >>> len(collection)
        1

        Notes
        -----
        Implementations should document their specific removal behavior clearly.

        For structures with specific removal semantics (Stack, Queue), consider
        providing more specific methods (pop, dequeue) that delegate to this
        method.

        See Also
        --------
        add : Add an item to the collection.
        """
        pass
