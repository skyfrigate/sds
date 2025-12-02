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

"""Heap implementations.

This module provides heap (binary heap) implementations including min-heap,
max-heap, and priority queue structures. Heaps are complete binary trees
that maintain a heap property ordering.

Classes
-------
MinHeap
    Min-heap where parent is smaller than children.
MaxHeap
    Max-heap where parent is larger than children.
HeapPriorityQueue
    Optimized priority queue implemented as a min-heap.

Examples
--------
Using a Min-Heap:

>>> from sds.tree.heap import MinHeap
>>> heap = MinHeap()
>>> heap.insert(5)
>>> heap.insert(3)
>>> heap.insert(7)
>>> heap.peek()
3
>>> heap.extract()
3
>>> list(heap)
[5, 7]

Using a Max-Heap:

>>> from sds.tree.heap import MaxHeap
>>> heap = MaxHeap()
>>> heap.insert(5)
>>> heap.insert(3)
>>> heap.insert(7)
>>> heap.peek()
7

Using a Heap-based Priority Queue:

>>> from sds.tree.heap import HeapPriorityQueue
>>> pq = HeapPriorityQueue()
>>> pq.enqueue("task1", priority=5)
>>> pq.enqueue("task2", priority=1)
>>> pq.dequeue()
('task2', 1)

Notes
-----
Heaps are implemented using a list/array representation for efficiency.
In this representation:
- Parent of node at index i is at index (i-1)//2
- Left child of node at index i is at index 2*i+1
- Right child of node at index i is at index 2*i+2

Time Complexity:
- Insert: O(log n)
- Extract: O(log n)
- Peek: O(1)
- Heapify: O(n)

See Also
--------
sds.tree.binary : Binary tree implementations.
"""

from typing import Any, Iterator, List, Optional, Tuple

from ..core.exceptions import EmptyStructureError
from ..core.interfaces import Collection

__all__ = ["MinHeap", "MaxHeap", "HeapPriorityQueue"]


class MinHeap(Collection):
    """Min-heap implementation using array representation.

    A min-heap is a complete binary tree where each parent node is
    less than or equal to its children. The minimum element is always
    at the root.

    Attributes
    ----------
    size : int
        The number of elements in the heap (read-only property).

    Examples
    --------
    Create and use a min-heap:

    >>> heap = MinHeap()
    >>> heap.insert(5)
    >>> heap.insert(3)
    >>> heap.insert(7)
    >>> heap.insert(1)
    >>> heap.peek()
    1
    >>> heap.extract()
    1
    >>> heap.peek()
    3

    Build heap from list:

    >>> heap = MinHeap([5, 3, 7, 1, 9])
    >>> heap.peek()
    1
    >>> list(heap)
    [1, 3, 5, 7, 9]

    Notes
    -----
    Time Complexity:
    - insert: O(log n)
    - extract: O(log n)
    - peek: O(1)
    - Building from list: O(n)

    Space Complexity: O(n)

    See Also
    --------
    MaxHeap : Max-heap implementation.
    PriorityQueue : Priority queue using min-heap.
    """

    def __init__(self, items: Optional[List[Any]] = None):
        """Initialize a min-heap.

        Parameters
        ----------
        items : List[Any] or None, optional
            Initial items to heapify. Default is None (empty heap).

        Examples
        --------
        >>> heap = MinHeap()
        >>> heap.is_empty()
        True

        >>> heap = MinHeap([5, 3, 7, 1])
        >>> heap.peek()
        1
        """
        self._heap: List[Any] = []
        self._size = 0

        if items:
            self._heap = items.copy()
            self._size = len(items)
            self._heapify()

    @property
    def size(self) -> int:
        """Get the number of elements in the heap.

        Returns
        -------
        int
            The number of elements.

        Examples
        --------
        >>> heap = MinHeap([1, 2, 3])
        >>> heap.size
        3
        """
        return self._size

    def _parent(self, index: int) -> int:
        """Get parent index.

        Parameters
        ----------
        index : int
            Child index.

        Returns
        -------
        int
            Parent index.
        """
        return (index - 1) // 2

    def _left_child(self, index: int) -> int:
        """Get left child index.

        Parameters
        ----------
        index : int
            Parent index.

        Returns
        -------
        int
            Left child index.
        """
        return 2 * index + 1

    def _right_child(self, index: int) -> int:
        """Get right child index.

        Parameters
        ----------
        index : int
            Parent index.

        Returns
        -------
        int
            Right child index.
        """
        return 2 * index + 2

    def _swap(self, i: int, j: int) -> None:
        """Swap two elements in the heap.

        Parameters
        ----------
        i : int
            First index.
        j : int
            Second index.
        """
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    def _sift_up(self, index: int) -> None:
        """Sift up element to maintain heap property.

        Parameters
        ----------
        index : int
            Index of element to sift up.
        """
        while index > 0:
            parent_idx = self._parent(index)
            if self._heap[index] < self._heap[parent_idx]:
                self._swap(index, parent_idx)
                index = parent_idx
            else:
                break

    def _sift_down(self, index: int) -> None:
        """Sift down element to maintain heap property.

        Parameters
        ----------
        index : int
            Index of element to sift down.
        """
        while True:
            smallest = index
            left = self._left_child(index)
            right = self._right_child(index)

            if left < self._size and self._heap[left] < self._heap[smallest]:
                smallest = left

            if right < self._size and self._heap[right] < self._heap[smallest]:
                smallest = right

            if smallest != index:
                self._swap(index, smallest)
                index = smallest
            else:
                break

    def _heapify(self) -> None:
        """Build heap from unordered array.

        Time complexity: O(n)
        """
        # Start from last non-leaf node and sift down
        for i in range(self._size // 2 - 1, -1, -1):
            self._sift_down(i)

    def insert(self, item: Any) -> None:
        """Insert an item into the heap.

        Parameters
        ----------
        item : Any
            The item to insert. Must be comparable.

        Examples
        --------
        >>> heap = MinHeap()
        >>> heap.insert(5)
        >>> heap.insert(3)
        >>> heap.peek()
        3

        Notes
        -----
        Time complexity: O(log n)
        """
        self._heap.append(item)
        self._size += 1
        self._sift_up(self._size - 1)

    def extract(self) -> Any:
        """Remove and return the minimum element.

        Returns
        -------
        Any
            The minimum element.

        Raises
        ------
        EmptyStructureError
            If the heap is empty.

        Examples
        --------
        >>> heap = MinHeap([5, 3, 7])
        >>> heap.extract()
        3
        >>> heap.extract()
        5

        Notes
        -----
        Time complexity: O(log n)
        """
        if self.is_empty():
            raise EmptyStructureError("Cannot extract from empty heap")

        min_item = self._heap[0]

        # Move last element to root
        self._heap[0] = self._heap[self._size - 1]
        self._heap.pop()
        self._size -= 1

        # Restore heap property
        if not self.is_empty():
            self._sift_down(0)

        return min_item

    def peek(self) -> Any:
        """Return the minimum element without removing it.

        Returns
        -------
        Any
            The minimum element.

        Raises
        ------
        EmptyStructureError
            If the heap is empty.

        Examples
        --------
        >>> heap = MinHeap([5, 3, 7])
        >>> heap.peek()
        3
        >>> len(heap)
        3

        Notes
        -----
        Time complexity: O(1)
        """
        if self.is_empty():
            raise EmptyStructureError("Cannot peek at empty heap")
        return self._heap[0]

    def clear(self) -> None:
        """Remove all elements from the heap.

        Examples
        --------
        >>> heap = MinHeap([5, 3, 7])
        >>> heap.clear()
        >>> heap.is_empty()
        True

        Notes
        -----
        Time complexity: O(1)
        """
        self._heap.clear()
        self._size = 0

    def __len__(self) -> int:
        """Return the number of elements in the heap.

        Returns
        -------
        int
            The number of elements.

        Examples
        --------
        >>> heap = MinHeap([1, 2, 3])
        >>> len(heap)
        3
        """
        return self._size

    def is_empty(self) -> bool:
        """Check if the heap is empty.

        Returns
        -------
        bool
            True if empty, False otherwise.

        Examples
        --------
        >>> heap = MinHeap()
        >>> heap.is_empty()
        True
        """
        return self._size == 0

    def __iter__(self) -> Iterator[Any]:
        """Iterate over heap elements (not in sorted order).

        Yields
        ------
        Any
            Elements from the heap.

        Examples
        --------
        >>> heap = MinHeap([5, 3, 7])
        >>> sorted(list(heap))
        [3, 5, 7]

        Notes
        -----
        This returns elements in heap order (array order), not sorted order.
        For sorted order, repeatedly call extract().
        """
        return iter(self._heap)

    def __contains__(self, item: Any) -> bool:
        """Check if item is in the heap.

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
        >>> heap = MinHeap([5, 3, 7])
        >>> 3 in heap
        True
        >>> 10 in heap
        False

        Notes
        -----
        Time complexity: O(n)
        """
        return item in self._heap

    def __repr__(self) -> str:
        """Return string representation.

        Returns
        -------
        str
            String representation.

        Examples
        --------
        >>> heap = MinHeap([5, 3])
        >>> repr(heap)
        'MinHeap(size=2)'
        """
        return f"MinHeap(size={self._size})"

    def __str__(self) -> str:
        """Return string showing heap contents.

        Returns
        -------
        str
            String representation.

        Examples
        --------
        >>> heap = MinHeap([5, 3, 7])
        >>> str(heap)
        'MinHeap: [3, 5, 7]'
        """
        if self.is_empty():
            return "MinHeap: []"
        return f"MinHeap: {self._heap}"


class MaxHeap(Collection):
    """Max-heap implementation using array representation.

    A max-heap is a complete binary tree where each parent node is
    greater than or equal to its children. The maximum element is
    always at the root.

    Attributes
    ----------
    size : int
        The number of elements in the heap (read-only property).

    Examples
    --------
    Create and use a max-heap:

    >>> heap = MaxHeap()
    >>> heap.insert(5)
    >>> heap.insert(3)
    >>> heap.insert(7)
    >>> heap.insert(9)
    >>> heap.peek()
    9
    >>> heap.extract()
    9
    >>> heap.peek()
    7

    Build heap from list:

    >>> heap = MaxHeap([5, 3, 7, 1, 9])
    >>> heap.peek()
    9

    Notes
    -----
    Time Complexity:
    - insert: O(log n)
    - extract: O(log n)
    - peek: O(1)
    - Building from list: O(n)

    See Also
    --------
    MinHeap : Min-heap implementation.
    """

    def __init__(self, items: Optional[List[Any]] = None):
        """Initialize a max-heap.

        Parameters
        ----------
        items : List[Any] or None, optional
            Initial items to heapify. Default is None (empty heap).

        Examples
        --------
        >>> heap = MaxHeap()
        >>> heap.is_empty()
        True

        >>> heap = MaxHeap([5, 3, 7, 1])
        >>> heap.peek()
        7
        """
        self._heap: List[Any] = []
        self._size = 0

        if items:
            self._heap = items.copy()
            self._size = len(items)
            self._heapify()

    @property
    def size(self) -> int:
        """Get the number of elements in the heap.

        Returns
        -------
        int
            The number of elements.
        """
        return self._size

    def _parent(self, index: int) -> int:
        """Get parent index."""
        return (index - 1) // 2

    def _left_child(self, index: int) -> int:
        """Get left child index."""
        return 2 * index + 1

    def _right_child(self, index: int) -> int:
        """Get right child index."""
        return 2 * index + 2

    def _swap(self, i: int, j: int) -> None:
        """Swap two elements in the heap."""
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    def _sift_up(self, index: int) -> None:
        """Sift up element to maintain heap property."""
        while index > 0:
            parent_idx = self._parent(index)
            if self._heap[index] > self._heap[parent_idx]:
                self._swap(index, parent_idx)
                index = parent_idx
            else:
                break

    def _sift_down(self, index: int) -> None:
        """Sift down element to maintain heap property."""
        while True:
            largest = index
            left = self._left_child(index)
            right = self._right_child(index)

            if left < self._size and self._heap[left] > self._heap[largest]:
                largest = left

            if right < self._size and self._heap[right] > self._heap[largest]:
                largest = right

            if largest != index:
                self._swap(index, largest)
                index = largest
            else:
                break

    def _heapify(self) -> None:
        """Build heap from unordered array."""
        for i in range(self._size // 2 - 1, -1, -1):
            self._sift_down(i)

    def insert(self, item: Any) -> None:
        """Insert an item into the heap.

        Parameters
        ----------
        item : Any
            The item to insert. Must be comparable.

        Examples
        --------
        >>> heap = MaxHeap()
        >>> heap.insert(5)
        >>> heap.insert(7)
        >>> heap.peek()
        7

        Notes
        -----
        Time complexity: O(log n)
        """
        self._heap.append(item)
        self._size += 1
        self._sift_up(self._size - 1)

    def extract(self) -> Any:
        """Remove and return the maximum element.

        Returns
        -------
        Any
            The maximum element.

        Raises
        ------
        EmptyStructureError
            If the heap is empty.

        Examples
        --------
        >>> heap = MaxHeap([5, 3, 7])
        >>> heap.extract()
        7
        >>> heap.extract()
        5

        Notes
        -----
        Time complexity: O(log n)
        """
        if self.is_empty():
            raise EmptyStructureError("Cannot extract from empty heap")

        max_item = self._heap[0]
        self._heap[0] = self._heap[self._size - 1]
        self._heap.pop()
        self._size -= 1

        if not self.is_empty():
            self._sift_down(0)

        return max_item

    def peek(self) -> Any:
        """Return the maximum element without removing it.

        Returns
        -------
        Any
            The maximum element.

        Raises
        ------
        EmptyStructureError
            If the heap is empty.

        Examples
        --------
        >>> heap = MaxHeap([5, 3, 7])
        >>> heap.peek()
        7

        Notes
        -----
        Time complexity: O(1)
        """
        if self.is_empty():
            raise EmptyStructureError("Cannot peek at empty heap")
        return self._heap[0]

    def clear(self) -> None:
        """Remove all elements from the heap."""
        self._heap.clear()
        self._size = 0

    def __len__(self) -> int:
        """Return the number of elements."""
        return self._size

    def is_empty(self) -> bool:
        """Check if the heap is empty."""
        return self._size == 0

    def __iter__(self) -> Iterator[Any]:
        """Iterate over heap elements (not in sorted order)."""
        return iter(self._heap)

    def __contains__(self, item: Any) -> bool:
        """Check if item is in the heap."""
        return item in self._heap

    def __repr__(self) -> str:
        """Return string representation."""
        return f"MaxHeap(size={self._size})"

    def __str__(self) -> str:
        """Return string showing heap contents."""
        if self.is_empty():
            return "MaxHeap: []"
        return f"MaxHeap: {self._heap}"


class HeapPriorityQueue(Collection):
    """Optimized priority queue implementation using min-heap.

    A heap-based priority queue where elements are dequeued based on priority
    (lower priority value = higher priority). This implementation uses a binary
    min-heap for efficient O(log n) operations, making it ideal for large datasets.

    **Performance Comparison:**

    This implementation is significantly faster than the linked-list based
    PriorityQueue in sds.linear.queue for large datasets:

    - HeapPriorityQueue (this class): O(log n) enqueue and dequeue
    - Linear PriorityQueue: O(n) enqueue, O(1) dequeue

    **When to use:**

    - Use this HeapPriorityQueue for performance-critical applications
    - Use linear.queue.PriorityQueue for simple, small datasets where
      code simplicity is preferred over performance

    Attributes
    ----------
    size : int
        The number of elements in the queue (read-only property).

    Examples
    --------
    Create and use a heap-based priority queue:

    >>> pq = HeapPriorityQueue()
    >>> pq.enqueue("low priority", 10)
    >>> pq.enqueue("high priority", 1)
    >>> pq.enqueue("medium priority", 5)
    >>> pq.dequeue()
    ('high priority', 1)
    >>> pq.dequeue()
    ('medium priority', 5)

    Efficient handling of large datasets:

    >>> pq = HeapPriorityQueue()
    >>> for i in range(1000, 0, -1):
    ...     pq.enqueue(f"task_{i}", i)
    >>> pq.peek()  # Always O(1)
    ('task_1', 1)

    Notes
    -----
    Time Complexity:
    - enqueue: O(log n) - significantly better than O(n) for linked list
    - dequeue: O(log n) - slightly slower than O(1), but overall better
    - peek: O(1)

    The priority is used for comparison. Lower priority values have
    higher priority in the queue (min-heap property).

    See Also
    --------
    MinHeap : Underlying min-heap implementation.
    sds.linear.queue.PriorityQueue : Simpler O(n) enqueue alternative.
    """

    def __init__(self):
        """Initialize an empty heap-based priority queue.

        Examples
        --------
        >>> pq = HeapPriorityQueue()
        >>> pq.is_empty()
        True
        """
        self._heap: List[Tuple[Any, Any]] = []
        self._size = 0

    @property
    def size(self) -> int:
        """Get the number of elements in the queue."""
        return self._size

    def _parent(self, index: int) -> int:
        """Get parent index."""
        return (index - 1) // 2

    def _left_child(self, index: int) -> int:
        """Get left child index."""
        return 2 * index + 1

    def _right_child(self, index: int) -> int:
        """Get right child index."""
        return 2 * index + 2

    def _swap(self, i: int, j: int) -> None:
        """Swap two elements."""
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    def _sift_up(self, index: int) -> None:
        """Sift up based on priority."""
        while index > 0:
            parent_idx = self._parent(index)
            # Compare priorities (second element of tuple)
            if self._heap[index][1] < self._heap[parent_idx][1]:
                self._swap(index, parent_idx)
                index = parent_idx
            else:
                break

    def _sift_down(self, index: int) -> None:
        """Sift down based on priority."""
        while True:
            smallest = index
            left = self._left_child(index)
            right = self._right_child(index)

            if left < self._size and self._heap[left][1] < self._heap[smallest][1]:
                smallest = left

            if right < self._size and self._heap[right][1] < self._heap[smallest][1]:
                smallest = right

            if smallest != index:
                self._swap(index, smallest)
                index = smallest
            else:
                break

    def enqueue(self, item: Any, priority: Any) -> None:
        """Add an item with priority to the queue.

        Parameters
        ----------
        item : Any
            The item to add.
        priority : Any
            The priority value. Must be comparable. Lower values = higher priority.

        Examples
        --------
        >>> pq = HeapPriorityQueue()
        >>> pq.enqueue("task1", 5)
        >>> pq.enqueue("task2", 1)
        >>> pq.peek()
        ('task2', 1)

        Notes
        -----
        Time complexity: O(log n) - More efficient than O(n) for large datasets
        """
        self._heap.append((item, priority))
        self._size += 1
        self._sift_up(self._size - 1)

    def dequeue(self) -> Tuple[Any, Any]:
        """Remove and return the highest priority item.

        Returns
        -------
        Tuple[Any, Any]
            A tuple of (item, priority).

        Raises
        ------
        EmptyStructureError
            If the queue is empty.

        Examples
        --------
        >>> pq = HeapPriorityQueue()
        >>> pq.enqueue("task", 1)
        >>> pq.dequeue()
        ('task', 1)

        Notes
        -----
        Time complexity: O(log n) - Balanced performance for all operations
        """
        if self.is_empty():
            raise EmptyStructureError("Cannot dequeue from empty priority queue")

        highest_priority = self._heap[0]
        self._heap[0] = self._heap[self._size - 1]
        self._heap.pop()
        self._size -= 1

        if not self.is_empty():
            self._sift_down(0)

        return highest_priority

    def peek(self) -> Tuple[Any, Any]:
        """Return the highest priority item without removing it.

        Returns
        -------
        Tuple[Any, Any]
            A tuple of (item, priority).

        Raises
        ------
        EmptyStructureError
            If the queue is empty.

        Examples
        --------
        >>> pq = HeapPriorityQueue()
        >>> pq.enqueue("task", 1)
        >>> pq.peek()
        ('task', 1)
        >>> len(pq)
        1

        Notes
        -----
        Time complexity: O(1) - Constant time access to highest priority
        """
        if self.is_empty():
            raise EmptyStructureError("Cannot peek at empty priority queue")
        return self._heap[0]

    def clear(self) -> None:
        """Remove all elements from the queue."""
        self._heap.clear()
        self._size = 0

    def __len__(self) -> int:
        """Return the number of elements."""
        return self._size

    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        return self._size == 0

    def __iter__(self) -> Iterator[Tuple[Any, Any]]:
        """Iterate over queue elements."""
        return iter(self._heap)

    def __contains__(self, item: Any) -> bool:
        """Check if item is in the queue (checks item, not priority).

        Parameters
        ----------
        item : Any
            The item to search for.

        Returns
        -------
        bool
            True if found, False otherwise.

        Notes
        -----
        Time complexity: O(n)
        """
        return any(elem[0] == item for elem in self._heap)

    def __repr__(self) -> str:
        """Return string representation."""
        return f"HeapPriorityQueue(size={self._size})"

    def __str__(self) -> str:
        """Return string showing queue contents."""
        if self.is_empty():
            return "HeapPriorityQueue: []"
        return f"HeapPriorityQueue: {self._heap}"
