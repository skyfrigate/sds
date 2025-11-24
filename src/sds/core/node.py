"""Node classes for linked data structures."""

from typing import Any, Optional


class Node:
    """A node in a singly linked list.

    Attributes:
        data: The data stored in the node
        next: Reference to the next node in the list
    """

    __slots__ = ("data", "next")

    def __init__(self, data: Any, next_node: Optional["Node"] = None):
        """Initialize a new node.

        Args:
            data: The data to store in the node
            next_node: The next node in the list (default: None)
        """
        self.data = data
        self.next = next_node

    def __repr__(self) -> str:
        """Return a string representation of the node."""
        return f"Node({self.data!r})"

    def __str__(self) -> str:
        """Return a string representation of the node."""
        return str(self.data)


class DoublyNode:
    """A node in a doubly linked list.

    Attributes:
        data: The data stored in the node
        next: Reference to the next node in the list
        prev: Reference to the previous node in the list
    """

    __slots__ = ("data", "next", "prev")

    def __init__(
        self,
        data: Any,
        next_node: Optional["DoublyNode"] = None,
        prev_node: Optional["DoublyNode"] = None,
    ):
        """Initialize a new doubly linked node.

        Args:
            data: The data to store in the node
            next_node: The next node in the list (default: None)
            prev_node: The previous node in the list (default: None)
        """
        self.data = data
        self.next = next_node
        self.prev = prev_node

    def __repr__(self) -> str:
        """Return a string representation of the node."""
        return f"DoublyNode({self.data!r})"

    def __str__(self) -> str:
        """Return a string representation of the node."""
        return str(self.data)
