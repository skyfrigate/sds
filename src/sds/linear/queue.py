"""Queue implementations (FIFO and variants).

This module provides queue implementations including FIFO queue, double-ended
queue (deque), and priority queue.

Classes
-------
Queue
    FIFO (First In First Out) queue implementation.
Deque
    Double-ended queue allowing operations at both ends.
PriorityQueue
    Queue where elements are dequeued based on priority.

Examples
--------
Using a FIFO queue:

>>> from sds.linear.queue import Queue
>>> q = Queue()
>>> q.enqueue(1)
>>> q.enqueue(2)
>>> q.dequeue()
1

Using a deque:

>>> from sds.linear.queue import Deque
>>> dq = Deque()
>>> dq.add_rear(1)
>>> dq.add_front(0)
>>> list(dq)
[0, 1]

Using a priority queue:

>>> from sds.linear.queue import PriorityQueue
>>> pq = PriorityQueue()
>>> pq.enqueue(5)
>>> pq.enqueue(1)
>>> pq.enqueue(3)
>>> pq.dequeue()
1

Notes
-----
Queues are useful for:
- Task scheduling and job queues
- Breadth-first search algorithms
- Request handling and buffering
- Message passing systems

See Also
--------
sds.linear.stack : LIFO data structure.
sds.linear.list : List implementations used internally.
"""

from typing import Any, Callable, Iterator, Optional, cast

from ..core.exceptions import EmptyStructureError
from ..core.interfaces import LinearCollection
from ..core.node import Node
from . import SimpleNode
from .list import DoublyLinkedList, LinkedList


class Queue(LinearCollection):
    """A Queue (FIFO - First In First Out) implementation.

    A queue is a linear data structure that follows the FIFO principle:
    the first element added is the first one to be removed.

    This implementation uses a LinkedList internally.

    Attributes
    ----------
    size : int
        The number of elements in the queue (read-only property).

    Time Complexity
    ---------------
    - Enqueue: O(n) with basic LinkedList
    - Dequeue: O(1)
    - Front: O(1)
    - Search: O(n)

    Examples
    --------
    Create and use a queue:

    >>> queue = Queue()
    >>> queue.enqueue(1)
    >>> queue.enqueue(2)
    >>> queue.enqueue(3)
    >>> queue.dequeue()
    1
    >>> queue.front()
    2

    Notes
    -----
    All operations at the front are O(1), but enqueue is O(n) due to the
    basic LinkedList implementation. For better performance, consider using
    a circular buffer or DoublyLinkedList with tail pointer.

    See Also
    --------
    Deque : Double-ended queue with O(1) operations at both ends.
    Stack : LIFO data structure.
    """

    def __init__(self):
        """Initialize an empty queue."""
        self._list = LinkedList()

    @property
    def size(self) -> int:
        """Get the number of elements in the queue.

        Returns
        -------
        int
            The number of elements currently in the queue.

        Examples
        --------
        >>> queue = Queue()
        >>> queue.size
        0
        >>> queue.enqueue(1)
        >>> queue.size
        1

        See Also
        --------
        __len__ : Returns the same value.
        """
        return len(self._list)

    def __len__(self) -> int:
        """Return the number of elements in the queue."""
        return len(self._list)

    def is_empty(self) -> bool:
        """Return True if the queue is empty."""
        return self._list.is_empty()

    def clear(self) -> None:
        """Remove all elements from the queue."""
        self._list.clear()

    def __iter__(self) -> Iterator[Any]:
        """Iterate over elements from front to rear."""
        return iter(self._list)

    def __contains__(self, item: Any) -> bool:
        """Return True if item is in the queue."""
        return item in self._list

    def __repr__(self) -> str:
        """Return a detailed string representation."""
        elements = ", ".join(repr(item) for item in self)
        return f"Queue([{elements}])"

    def __str__(self) -> str:
        """Return a simple string representation."""
        if self.is_empty():
            return "Queue: []"
        elements = " <- ".join(str(item) for item in self)
        return f"Queue (front to rear): [{elements}]"

    def enqueue(self, item: Any) -> None:
        """Add an item to the rear of the queue.

        Parameters
        ----------
        item : Any
            The item to enqueue.

        Examples
        --------
        >>> queue = Queue()
        >>> queue.enqueue(1)
        >>> queue.enqueue(2)
        >>> list(queue)
        [1, 2]

        Notes
        -----
        Time complexity: O(n)
        """
        self._list.append(item)

    def dequeue(self) -> Any:
        """Remove and return the front item from the queue.

        Returns
        -------
        Any
            The item at the front of the queue.

        Raises
        ------
        EmptyStructureError
            If the queue is empty.

        Examples
        --------
        >>> queue = Queue()
        >>> queue.enqueue(1)
        >>> queue.enqueue(2)
        >>> queue.dequeue()
        1

        Notes
        -----
        Time complexity: O(1)
        """
        if self.is_empty():
            raise EmptyStructureError("Cannot dequeue from empty queue")
        return self._list.remove_first()

    def front(self) -> Any:
        """Return the front item without removing it.

        Returns
        -------
        Any
            The item at the front of the queue.

        Raises
        ------
        EmptyStructureError
            If the queue is empty.

        Notes
        -----
        Time complexity: O(1)
        """
        if self.is_empty():
            raise EmptyStructureError("Cannot peek at empty queue")
        return self._list[0]

    def rear(self) -> Any:
        """Return the rear item without removing it.

        Returns
        -------
        Any
            The item at the rear of the queue.

        Raises
        ------
        EmptyStructureError
            If the queue is empty.

        Notes
        -----
        Time complexity: O(n)
        """
        if self.is_empty():
            raise EmptyStructureError("Cannot peek at empty queue")
        return self._list[len(self._list) - 1]

    def add(self, item: Any) -> None:
        """Add an item to the queue (enqueues by default)."""
        self.enqueue(item)

    def remove(self, item: Any) -> Any:
        """Remove an item from the queue.

        Note: This violates the FIFO principle.
        """
        return self._list.remove(item)


class Deque(LinearCollection):
    """A Deque (Double-ended queue) implementation.

    A deque allows insertion and deletion at both ends efficiently.

    This implementation uses a DoublyLinkedList internally for O(1) operations
    at both ends.

    Attributes
    ----------
    size : int
        The number of elements in the deque (read-only property).

    Time Complexity
    ---------------
    - Add front/rear: O(1)
    - Remove front/rear: O(1)
    - Peek front/rear: O(1)
    - Search: O(n)

    Examples
    --------
    >>> deque = Deque()
    >>> deque.add_rear(1)
    >>> deque.add_front(0)
    >>> deque.add_rear(2)
    >>> list(deque)
    [0, 1, 2]

    See Also
    --------
    Queue : FIFO queue with operations at one end.
    """

    def __init__(self):
        """Initialize an empty deque."""
        self._list = DoublyLinkedList()

    @property
    def size(self) -> int:
        """Get the number of elements in the deque."""
        return len(self._list)

    def __len__(self) -> int:
        """Return the number of elements in the deque."""
        return len(self._list)

    def is_empty(self) -> bool:
        """Return True if the deque is empty."""
        return self._list.is_empty()

    def clear(self) -> None:
        """Remove all elements from the deque."""
        self._list.clear()

    def __iter__(self) -> Iterator[Any]:
        """Iterate over elements from front to rear."""
        return iter(self._list)

    def __reversed__(self) -> Iterator[Any]:
        """Iterate over elements from rear to front."""
        return reversed(self._list)

    def __contains__(self, item: Any) -> bool:
        """Return True if item is in the deque."""
        return item in self._list

    def __repr__(self) -> str:
        """Return a detailed string representation."""
        elements = ", ".join(repr(item) for item in self)
        return f"Deque([{elements}])"

    def __str__(self) -> str:
        """Return a simple string representation."""
        if self.is_empty():
            return "Deque: []"
        elements = " <-> ".join(str(item) for item in self)
        return f"Deque (front to rear): [{elements}]"

    def add_front(self, item: Any) -> None:
        """Add an item to the front of the deque.

        Parameters
        ----------
        item : Any
            The item to add.

        Notes
        -----
        Time complexity: O(1)
        """
        self._list.prepend(item)

    def add_rear(self, item: Any) -> None:
        """Add an item to the rear of the deque.

        Parameters
        ----------
        item : Any
            The item to add.

        Notes
        -----
        Time complexity: O(1)
        """
        self._list.append(item)

    def remove_front(self) -> Any:
        """Remove and return the front item.

        Returns
        -------
        Any
            The item at the front.

        Raises
        ------
        EmptyStructureError
            If the deque is empty.

        Notes
        -----
        Time complexity: O(1)
        """
        if self.is_empty():
            raise EmptyStructureError("Cannot remove from empty deque")
        return self._list.remove_first()

    def remove_rear(self) -> Any:
        """Remove and return the rear item.

        Returns
        -------
        Any
            The item at the rear.

        Raises
        ------
        EmptyStructureError
            If the deque is empty.

        Notes
        -----
        Time complexity: O(1)
        """
        if self.is_empty():
            raise EmptyStructureError("Cannot remove from empty deque")
        return self._list.remove_last()

    def peek_front(self) -> Any:
        """Return the front item without removing it.

        Returns
        -------
        Any
            The item at the front.

        Raises
        ------
        EmptyStructureError
            If the deque is empty.

        Notes
        -----
        Time complexity: O(1)
        """
        if self.is_empty():
            raise EmptyStructureError("Cannot peek at empty deque")
        return self._list[0]

    def peek_rear(self) -> Any:
        """Return the rear item without removing it.

        Returns
        -------
        Any
            The item at the rear.

        Raises
        ------
        EmptyStructureError
            If the deque is empty.

        Notes
        -----
        Time complexity: O(1)
        """
        if self.is_empty():
            raise EmptyStructureError("Cannot peek at empty deque")
        return self._list[-1]

    def add(self, item: Any) -> None:
        """Add an item to the deque (adds to rear by default)."""
        self.add_rear(item)

    def remove(self, item: Any) -> Any:
        """Remove the first occurrence of an item."""
        return self._list.remove(item)

    # Convenience aliases
    def append(self, item: Any) -> None:
        """Alias for add_rear."""
        self.add_rear(item)

    def appendleft(self, item: Any) -> None:
        """Alias for add_front."""
        self.add_front(item)

    def pop(self) -> Any:
        """Alias for remove_rear."""
        return self.remove_rear()

    def popleft(self) -> Any:
        """Alias for remove_front."""
        return self.remove_front()


class PriorityQueue(LinearCollection):
    """A Priority Queue implementation using a sorted linked list.

    Elements are dequeued in order of their priority (lowest value = highest priority by default).

    Attributes
    ----------
    size : int
        The number of elements in the queue (read-only property).

    Time Complexity
    ---------------
    - Enqueue: O(n) - must find correct position
    - Dequeue: O(1) - always remove from front
    - Peek: O(1)

    Examples
    --------
    >>> pq = PriorityQueue()
    >>> pq.enqueue(5)
    >>> pq.enqueue(1)
    >>> pq.enqueue(3)
    >>> pq.dequeue()
    1
    >>> pq.dequeue()
    3

    See Also
    --------
    Queue : FIFO queue without priorities.
    """

    def __init__(self, reverse: bool = False, key: Optional[Callable] = None):
        """Initialize an empty priority queue.

        Parameters
        ----------
        reverse : bool, optional
            If True, higher values have higher priority. Default is False.
        key : callable, optional
            Function to extract priority from items. Default is identity.
        """
        # Head points to a SimpleNode chain
        self._head: Optional[SimpleNode] = None
        self._size: int = 0
        self._reverse = reverse
        self._key = key if key else lambda x: x

    @property
    def size(self) -> int:
        """Get the number of elements in the queue."""
        return self._size

    def __len__(self) -> int:
        """Return the number of elements in the queue."""
        return self._size

    def is_empty(self) -> bool:
        """Return True if the queue is empty."""
        return self._size == 0

    def clear(self) -> None:
        """Remove all elements from the queue."""
        self._head = None
        self._size = 0

    def __iter__(self) -> Iterator[Any]:
        """Iterate over elements in priority order."""
        current: Optional[SimpleNode] = self._head
        while current is not None:
            yield current.data
            current = current.next

    def __contains__(self, item: Any) -> bool:
        """Return True if item is in the queue."""
        current: Optional[SimpleNode] = self._head
        while current is not None:
            if current.data == item:
                return True
            current = current.next
        return False

    def __repr__(self) -> str:
        """Return a detailed string representation."""
        elements = ", ".join(repr(item) for item in self)
        return f"PriorityQueue([{elements}])"

    def __str__(self) -> str:
        """Return a simple string representation."""
        if self.is_empty():
            return "PriorityQueue: []"
        elements = " -> ".join(str(item) for item in self)
        return f"PriorityQueue (highest to lowest priority): [{elements}]"

    def _compare(self, a: Any, b: Any) -> bool:
        """Compare two items based on priority."""
        priority_a = self._key(a)
        priority_b = self._key(b)

        if self._reverse:
            return priority_a > priority_b
        else:
            return priority_a < priority_b

    def enqueue(self, item: Any) -> None:
        """Add an item to the queue based on its priority.

        Parameters
        ----------
        item : Any
            The item to enqueue.

        Notes
        -----
        Time complexity: O(n)
        """
        new_node = SimpleNode(item)

        if self._head is None or self._compare(item, self._head.data):
            new_node.next = self._head
            self._head = new_node
        else:
            current: SimpleNode = self._head
            while current.next is not None and not self._compare(
                item, current.next.data
            ):
                # mypy knows current.next is SimpleNode here by narrowing
                current = cast(SimpleNode, current.next)

            new_node.next = current.next
            current.next = new_node

        self._size += 1

    def dequeue(self) -> Any:
        """Remove and return the item with highest priority.

        Returns
        -------
        Any
            The item with highest priority.

        Raises
        ------
        EmptyStructureError
            If the queue is empty.

        Notes
        -----
        Time complexity: O(1)
        """
        if self.is_empty():
            raise EmptyStructureError("Cannot dequeue from empty priority queue")

        head: SimpleNode = cast(SimpleNode, self._head)
        data = head.data
        self._head = head.next
        self._size -= 1
        return data

    def peek(self) -> Any:
        """Return the item with highest priority without removing it.

        Returns
        -------
        Any
            The item with highest priority.

        Raises
        ------
        EmptyStructureError
            If the queue is empty.

        Notes
        -----
        Time complexity: O(1)
        """
        if self.is_empty():
            raise EmptyStructureError("Cannot peek at empty priority queue")
        return cast(Node, self._head).data

    def add(self, item: Any) -> None:
        """Add an item to the queue (enqueues by default)."""
        self.enqueue(item)

    def remove(self, item: Any) -> Any:
        """Remove a specific item from the queue."""
        if self.is_empty():
            raise EmptyStructureError("Cannot remove from empty priority queue")

        head: SimpleNode = cast(SimpleNode, self._head)
        if head.data == item:
            return self.dequeue()

        current: SimpleNode = head
        while current.next is not None:
            nxt: SimpleNode = cast(SimpleNode, current.next)
            if nxt.data == item:
                data = nxt.data
                current.next = nxt.next
                self._size -= 1
                return data
            current = nxt

        raise ValueError(f"Item {item} not found in queue")


class PriorityItem:
    """Helper class for creating items with explicit priorities.

    Examples
    --------
    >>> pq = PriorityQueue()
    >>> pq.enqueue(PriorityItem("Task 1", 5))
    >>> pq.enqueue(PriorityItem("Task 2", 1))
    >>> pq.dequeue().data
    'Task 2'
    """

    def __init__(self, data: Any, priority: float):
        """Initialize a priority item.

        Parameters
        ----------
        data : Any
            The data to store.
        priority : float
            The priority value.
        """
        self.data = data
        self.priority = priority

    def __repr__(self) -> str:
        return f"PriorityItem(data={self.data!r}, priority={self.priority})"

    def __str__(self) -> str:
        return f"{self.data} (priority: {self.priority})"

    def __lt__(self, other: "PriorityItem") -> bool:
        if not isinstance(other, PriorityItem):
            raise NotImplementedError
        return self.priority < other.priority

    def __le__(self, other: "PriorityItem") -> bool:
        if not isinstance(other, PriorityItem):
            raise NotImplementedError
        return self.priority <= other.priority

    def __gt__(self, other: "PriorityItem") -> bool:
        if not isinstance(other, PriorityItem):
            raise NotImplementedError
        return self.priority > other.priority

    def __ge__(self, other: "PriorityItem") -> bool:
        if not isinstance(other, PriorityItem):
            raise NotImplementedError
        return self.priority >= other.priority

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PriorityItem):
            raise NotImplementedError
        return self.priority == other.priority
