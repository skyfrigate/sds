"""Stack (LIFO) implementation.

This module provides a Stack implementation using a linked list internally.
A stack follows the Last In First Out (LIFO) principle.

Classes
-------
Stack
    LIFO data structure with push, pop, and peek operations.

Examples
--------
Using a stack:

>>> from sds.linear.stack import Stack
>>> stack = Stack()
>>> stack.push(1)
>>> stack.push(2)
>>> stack.push(3)
>>> stack.pop()
3
>>> stack.peek()
2

Notes
-----
Stacks are useful for:
- Function call management
- Undo/redo functionality
- Expression evaluation and syntax parsing
- Backtracking algorithms (DFS, maze solving)

See Also
--------
sds.linear.list : LinkedList used internally.
sds.linear.queue : FIFO data structure.
"""

from typing import Any, Iterator

from ..core.exceptions import EmptyStructureError
from ..core.interfaces import LinearCollection
from .list import LinkedList


class Stack(LinearCollection):
    """A Stack (LIFO - Last In First Out) implementation.

    A stack is a linear data structure that follows the LIFO principle:
    the last element added is the first one to be removed.

    This implementation uses a LinkedList internally for efficient O(1) operations.

    Attributes
    ----------
    size : int
        The number of elements in the stack (read-only property).

    Time Complexity
    ---------------
    - Push: O(1)
    - Pop: O(1)
    - Peek: O(1)
    - Search: O(n)

    Examples
    --------
    Create and use a stack:

    >>> stack = Stack()
    >>> stack.push(1)
    >>> stack.push(2)
    >>> stack.push(3)
    >>> len(stack)
    3

    Pop elements (LIFO order):

    >>> stack.pop()
    3
    >>> stack.pop()
    2
    >>> stack.peek()
    1

    Check if empty:

    >>> stack.is_empty()
    False
    >>> stack.clear()
    >>> stack.is_empty()
    True

    Notes
    -----
    All operations at the top of the stack are O(1). The stack cannot be
    accessed by index as this would violate the LIFO principle.

    See Also
    --------
    Queue : FIFO data structure.
    Deque : Double-ended queue allowing operations at both ends.
    """

    def __init__(self):
        """Initialize an empty stack."""
        self._list = LinkedList()

    @property
    def size(self) -> int:
        """Get the number of elements in the stack.

        Returns
        -------
        int
            The number of elements currently in the stack.

        Examples
        --------
        >>> stack = Stack()
        >>> stack.size
        0
        >>> stack.push(1)
        >>> stack.size
        1

        Notes
        -----
        This property provides O(1) access to the stack size.

        See Also
        --------
        __len__ : Returns the same value, allowing use of len(stack).
        """
        return len(self._list)

    def __len__(self) -> int:
        """Return the number of elements in the stack.

        Returns
        -------
        int
            The number of elements in the stack.

        Examples
        --------
        >>> stack = Stack()
        >>> len(stack)
        0
        >>> stack.push(1)
        >>> len(stack)
        1

        Notes
        -----
        Time complexity: O(1)
        """
        return len(self._list)

    def is_empty(self) -> bool:
        """Return True if the stack is empty.

        Returns
        -------
        bool
            True if the stack contains no elements, False otherwise.

        Examples
        --------
        >>> stack = Stack()
        >>> stack.is_empty()
        True
        >>> stack.push(1)
        >>> stack.is_empty()
        False

        Notes
        -----
        Time complexity: O(1)
        """
        return self._list.is_empty()

    def clear(self) -> None:
        """Remove all elements from the stack.

        Examples
        --------
        >>> stack = Stack()
        >>> stack.push(1)
        >>> stack.push(2)
        >>> len(stack)
        2
        >>> stack.clear()
        >>> len(stack)
        0

        Notes
        -----
        Time complexity: O(1)
        """
        self._list.clear()

    def __iter__(self) -> Iterator[Any]:
        """Iterate over elements from top to bottom.

        Yields
        ------
        Any
            Elements from the stack in LIFO order (top to bottom).

        Examples
        --------
        >>> stack = Stack()
        >>> stack.push(1)
        >>> stack.push(2)
        >>> stack.push(3)
        >>> list(stack)
        [3, 2, 1]

        Notes
        -----
        Time complexity: O(n) for complete iteration
        Iteration does not remove elements from the stack.
        """
        return iter(self._list)

    def __contains__(self, item: Any) -> bool:
        """Return True if item is in the stack.

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
        >>> stack = Stack()
        >>> stack.push(1)
        >>> stack.push(2)
        >>> 1 in stack
        True
        >>> 3 in stack
        False

        Notes
        -----
        Time complexity: O(n)
        This performs a linear search through the stack.
        """
        return item in self._list

    def __repr__(self) -> str:
        """Return a detailed string representation of the stack.

        Returns
        -------
        str
            String in the form "Stack([top, ..., bottom])".

        Examples
        --------
        >>> stack = Stack()
        >>> stack.push(1)
        >>> stack.push(2)
        >>> repr(stack)
        'Stack([2, 1])'
        """
        elements = ", ".join(repr(item) for item in self)
        return f"Stack([{elements}])"

    def __str__(self) -> str:
        """Return a simple string representation of the stack.

        Returns
        -------
        str
            String showing the stack structure from top to bottom.

        Examples
        --------
        >>> stack = Stack()
        >>> stack.push(1)
        >>> stack.push(2)
        >>> print(stack)
        Stack (top to bottom):
          [2]
          [1]
        """
        if self.is_empty():
            return "Stack: []"
        elements = list(self)
        stack_repr = "\n".join(f"  [{item}]" for item in elements)
        return f"Stack (top to bottom):\n{stack_repr}"

    def push(self, item: Any) -> None:
        """Push an item onto the top of the stack.

        Parameters
        ----------
        item : Any
            The item to push onto the stack.

        Examples
        --------
        >>> stack = Stack()
        >>> stack.push(1)
        >>> stack.push(2)
        >>> stack.peek()
        2

        Notes
        -----
        Time complexity: O(1)

        See Also
        --------
        pop : Remove and return the top item.
        peek : View the top item without removing it.
        """
        self._list.prepend(item)

    def pop(self) -> Any:
        """Remove and return the top item from the stack.

        Returns
        -------
        Any
            The item at the top of the stack.

        Raises
        ------
        EmptyStructureError
            If the stack is empty.

        Examples
        --------
        >>> stack = Stack()
        >>> stack.push(1)
        >>> stack.push(2)
        >>> stack.pop()
        2
        >>> stack.pop()
        1
        >>> stack.pop()
        Traceback (most recent call last):
            ...
        EmptyStructureError: Cannot pop from empty stack

        Notes
        -----
        Time complexity: O(1)

        See Also
        --------
        push : Add an item to the top of the stack.
        peek : View the top item without removing it.
        """
        if self.is_empty():
            raise EmptyStructureError("Cannot pop from empty stack")
        return self._list.remove_first()

    def peek(self) -> Any:
        """Return the top item without removing it.

        Returns
        -------
        Any
            The item at the top of the stack.

        Raises
        ------
        EmptyStructureError
            If the stack is empty.

        Examples
        --------
        >>> stack = Stack()
        >>> stack.push(1)
        >>> stack.push(2)
        >>> stack.peek()
        2
        >>> len(stack)  # peek doesn't remove the item
        2

        Notes
        -----
        Time complexity: O(1)
        The stack is not modified by this operation.

        See Also
        --------
        pop : Remove and return the top item.
        """
        if self.is_empty():
            raise EmptyStructureError("Cannot peek at empty stack")
        return self._list[0]

    def add(self, item: Any) -> None:
        """Add an item to the stack (pushes by default).

        This method is provided to satisfy the LinearCollection interface.
        It is equivalent to push().

        Parameters
        ----------
        item : Any
            The item to add.

        Examples
        --------
        >>> stack = Stack()
        >>> stack.add(1)
        >>> stack.add(2)
        >>> list(stack)
        [2, 1]

        Notes
        -----
        Time complexity: O(1)

        See Also
        --------
        push : Preferred method for adding to a stack.
        """
        self.push(item)

    def remove(self, item: Any) -> Any:
        """Remove an item from the stack.

        Note: This violates the LIFO principle and should be used sparingly.
        It searches through the stack and removes the first occurrence.

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
            If the stack is empty.
        ValueError
            If the item is not found.

        Examples
        --------
        >>> stack = Stack()
        >>> stack.push(1)
        >>> stack.push(2)
        >>> stack.push(3)
        >>> stack.remove(2)
        2
        >>> list(stack)
        [3, 1]

        Notes
        -----
        Time complexity: O(n)
        This operation violates the LIFO principle and should be avoided
        in typical stack usage.

        See Also
        --------
        pop : Remove the top item (proper LIFO operation).
        """
        return self._list.remove(item)
