# Copyright 2024-2025, skyfrigate, biface
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

"""Skip List probabilistic sorted data structure.

A skip list is a probabilistic alternative to balanced trees. It achieves
O(log n) expected time for search, insertion, and deletion by layering
multiple linked lists of decreasing density on top of a base sorted list.

Classes
-------
_SkipListNode
    Internal node holding a key, a value, and a forward-pointer array.
SkipList
    Publicly usable skip list with configurable max level and probability.

Examples
--------
Basic usage:

>>> sl = SkipList()
>>> sl.insert(3, "three")
>>> sl.insert(1, "one")
>>> sl.insert(2, "two")
>>> sl.search(2)
'two'
>>> 1 in sl
True
>>> sl.delete(2)
True
>>> list(sl)
[1, 3]

Custom parameters:

>>> sl = SkipList(max_level=8, probability=0.25)
>>> for k in range(10):
...     sl.insert(k)
>>> len(sl)
10

Notes
-----
Time Complexity (average, p=0.5):
- insert: O(log n)
- delete: O(log n)
- search: O(log n)
- __contains__: O(log n)
- __iter__: O(n)

Space Complexity: O(n log n) expected (forward-pointer arrays).

The height of each node is chosen by repeated Bernoulli trials with
probability *p*. The expected number of levels is O(log_{1/p} n), giving
O(log n) average-case performance for p = 0.5.

References
----------
.. [1] Pugh, W. (1990). "Skip Lists: A Probabilistic Alternative to
       Balanced Trees". Communications of the ACM, 33(6), 668-676.
       https://dl.acm.org/doi/10.1145/78973.78977
.. [2] OpenDSA — Skip Lists chapter.
       https://opendsa-server.cs.vt.edu/ODSA/Books/Everything/html/SkipList.html
"""

import random
from typing import Any, Iterator, Optional

from .interfaces import AbstractSkipList

__all__ = ["SkipList"]

# ---------------------------------------------------------------------------
# Internal node
# ---------------------------------------------------------------------------

_SENTINEL_KEY: object = object()  # unique sentinel, smaller than any real key


class _SkipListNode:
    """Internal node for SkipList.

    Holds a key, an optional value, and a fixed-size array of forward
    pointers — one per level from 0 (base list) to *level* (inclusive).

    Parameters
    ----------
    key : Any
        Comparable key stored in this node.
    level : int
        Height of this node (number of forward-pointer slots - 1).
    value : Any, optional
        Associated payload.
    """

    __slots__ = ("key", "value", "forward")

    def __init__(self, key: Any, level: int, value: Any = None) -> None:
        self.key = key
        self.value = value
        # forward[i] points to the next node at level i
        self.forward: list[Optional["_SkipListNode"]] = [None] * (level + 1)


# ---------------------------------------------------------------------------
# SkipList
# ---------------------------------------------------------------------------


class SkipList(AbstractSkipList):
    """Probabilistic sorted data structure with O(log n) expected operations.

    A skip list organises elements in a sorted base linked list while
    maintaining express lanes at higher levels for fast traversal. Each
    node is promoted to the next level with probability *p*, independently.

    Parameters
    ----------
    max_level : int
        Maximum number of levels (inclusive). Must be ≥ 1.
        A value of 16 handles up to ~65 000 elements at p=0.5 with high
        probability; 32 covers billions of elements.
    probability : float
        Promotion probability per level. Must be in (0.0, 1.0).
        p=0.5 gives the classic O(log₂ n) behaviour.

    Attributes
    ----------
    max_level : int
        Maximum height of any node (read-only).
    probability : float
        Geometric promotion probability (read-only).
    level : int
        Current highest occupied level (0-indexed).

    Raises
    ------
    ValueError
        If ``max_level < 1`` or ``probability`` is not in (0, 1).

    Examples
    --------
    Insert, search, delete:

    >>> sl = SkipList()
    >>> sl.insert(10, "ten")
    >>> sl.insert(5, "five")
    >>> sl.insert(20, "twenty")
    >>> sl.search(5)
    'five'
    >>> sl.search(99) is None
    True
    >>> 10 in sl
    True
    >>> sl.delete(5)
    True
    >>> sl.delete(99)
    False
    >>> list(sl)
    [10, 20]

    Iteration in sorted order:

    >>> sl = SkipList()
    >>> for k in [3, 1, 4, 1, 5]:
    ...     sl.insert(k)
    >>> list(sl)
    [1, 3, 4, 5]

    Notes
    -----
    Duplicate keys: a second ``insert(k, v)`` **updates** the value
    associated with *k* rather than inserting a second node. Keys must
    support ``<`` and ``==``.
    """

    def __init__(
        self,
        max_level: int = 16,
        probability: float = 0.5,
    ) -> None:
        """Initialise an empty skip list.

        Parameters
        ----------
        max_level : int
            Maximum node height (default 16).
        probability : float
            Per-level promotion probability (default 0.5).

        Raises
        ------
        ValueError
            If ``max_level < 1`` or ``probability`` not in (0, 1).

        Examples
        --------
        >>> sl = SkipList(max_level=8, probability=0.25)
        >>> len(sl)
        0

        Notes
        -----
        Time complexity: O(max_level).
        """
        if max_level < 1:
            raise ValueError(f"max_level must be at least 1, got {max_level}")
        if not (0.0 < probability < 1.0):
            raise ValueError(f"probability must be in (0.0, 1.0), got {probability}")

        self._max_level = max_level
        self._probability = probability
        self._level = 0  # current highest level in use (0-indexed)
        self._length = 0

        # Sentinel head node: key=_SENTINEL_KEY, height=max_level
        self._head = _SkipListNode(_SENTINEL_KEY, max_level)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def max_level(self) -> int:
        """Maximum height of any node.

        Returns
        -------
        int
            Value passed at construction.
        """
        return self._max_level

    @property
    def probability(self) -> float:
        """Per-level promotion probability.

        Returns
        -------
        float
            Value passed at construction.
        """
        return self._probability

    @property
    def level(self) -> int:
        """Current highest occupied level (0-indexed).

        Returns
        -------
        int
            Grows as elements are inserted up to ``max_level``.
        """
        return self._level

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _random_level(self) -> int:
        """Draw a random height for a new node.

        Repeatedly flips a biased coin (prob *p*) until tails or
        ``max_level`` is reached.

        Returns
        -------
        int
            Random level in ``[0, max_level]``.
        """
        lvl = 0
        while (  # nosec B311
            random.random() < self._probability and lvl < self._max_level  # nosec B311
        ):
            lvl += 1
        return lvl

    def _find_update(self, key: Any) -> list[Optional[_SkipListNode]]:
        """Collect the rightmost predecessor node at each level.

        Traverses from the highest level down, recording the last node
        whose successor's key is less than *key*. These are the nodes
        whose ``forward`` pointers must be updated on insert/delete.

        Parameters
        ----------
        key : Any
            Target key for the traversal.

        Returns
        -------
        list[_SkipListNode | None]
            update[i] is the predecessor at level i.
        """
        update: list[Optional[_SkipListNode]] = [None] * (self._max_level + 1)
        current = self._head

        for i in range(self._level, -1, -1):
            nxt = current.forward[i]
            while nxt is not None and nxt.key < key:
                current = nxt
                nxt = current.forward[i]
            update[i] = current

        return update

    # ------------------------------------------------------------------
    # AbstractSkipList interface
    # ------------------------------------------------------------------

    def is_empty(self) -> bool:
        """Return True if the skip list contains no elements.

        Returns
        -------
        bool
            True if length is 0.

        Notes
        -----
        Time complexity: O(1).
        """
        return self._length == 0

    def clear(self) -> None:
        """Remove all elements from the skip list.

        Resets the sentinel head and tail pointers and drops all nodes.

        Notes
        -----
        Time complexity: O(1) — just resets pointers; GC handles nodes.
        """
        self._head = _SkipListNode(_SENTINEL_KEY, self._max_level)
        self._level = 0
        self._length = 0

    def insert(self, key: Any, value: Any = None) -> None:
        """Insert or update a key-value pair.

        If *key* already exists, its associated value is updated in place.
        Otherwise, a new node is inserted at a randomly chosen height.

        Parameters
        ----------
        key : Any
            Comparable key. Must support ``<`` and ``==``.
        value : Any, optional
            Payload to associate with *key*.

        Examples
        --------
        >>> sl = SkipList()
        >>> sl.insert(1, "one")
        >>> sl.insert(1, "ONE")   # update
        >>> sl.search(1)
        'ONE'
        >>> len(sl)
        1

        Notes
        -----
        Time complexity: O(log n) average.
        """
        update = self._find_update(key)
        node0 = update[0]
        current = node0.forward[0] if node0 is not None else None

        # Key already present — update value only
        if current is not None and current.key == key:
            current.value = value
            return

        # New key — draw a random level and splice in
        new_level = self._random_level()

        if new_level > self._level:
            # Extend update[] for the new levels, pointing to head
            for i in range(self._level + 1, new_level + 1):
                update[i] = self._head
            self._level = new_level

        new_node = _SkipListNode(key, new_level, value)

        for i in range(new_level + 1):
            new_node.forward[i] = update[i].forward[i]  # type: ignore[union-attr]
            update[i].forward[i] = new_node  # type: ignore[union-attr]

        self._length += 1

    def delete(self, key: Any) -> bool:
        """Remove the node with the given key.

        Parameters
        ----------
        key : Any
            Key to remove.

        Returns
        -------
        bool
            True if the key was found and removed, False otherwise.

        Examples
        --------
        >>> sl = SkipList()
        >>> sl.insert(5)
        >>> sl.delete(5)
        True
        >>> sl.delete(5)
        False

        Notes
        -----
        Time complexity: O(log n) average.
        """
        update = self._find_update(key)
        node0 = update[0]
        current = node0.forward[0] if node0 is not None else None

        if current is None or current.key != key:
            return False

        # Unlink the node at each level
        for i in range(self._level + 1):
            if update[i] is None or update[i].forward[i] is not current:  # type: ignore[union-attr]
                break
            update[i].forward[i] = current.forward[i]  # type: ignore[union-attr]

        # Shrink level if top levels are now empty
        while self._level > 0 and self._head.forward[self._level] is None:
            self._level -= 1

        self._length -= 1
        return True

    def search(self, key: Any) -> Optional[Any]:
        """Return the value associated with *key*, or None if absent.

        Parameters
        ----------
        key : Any
            Key to search for.

        Returns
        -------
        Any or None
            Associated value, or None if not found.

        Examples
        --------
        >>> sl = SkipList()
        >>> sl.insert(7, "seven")
        >>> sl.search(7)
        'seven'
        >>> sl.search(99) is None
        True

        Notes
        -----
        Time complexity: O(log n) average.
        """
        current = self._head
        for i in range(self._level, -1, -1):
            nxt = current.forward[i]
            while nxt is not None and nxt.key < key:
                current = nxt
                nxt = current.forward[i]

        candidate: Optional[_SkipListNode] = current.forward[0]
        if candidate is not None and candidate.key == key:
            return candidate.value
        return None

    def __contains__(self, key: Any) -> bool:
        """Test whether *key* is in the skip list.

        Parameters
        ----------
        key : Any
            Key to test.

        Returns
        -------
        bool
            True if the key is present.

        Examples
        --------
        >>> sl = SkipList()
        >>> sl.insert(3)
        >>> 3 in sl
        True
        >>> 99 in sl
        False

        Notes
        -----
        Time complexity: O(log n) average.
        """
        return self._exact_key_exists(key)

    def _exact_key_exists(self, key: Any) -> bool:
        """Return True if *key* exists even when its value is None."""
        current = self._head
        for i in range(self._level, -1, -1):
            nxt = current.forward[i]
            while nxt is not None and nxt.key < key:
                current = nxt
                nxt = current.forward[i]
        candidate: Optional[_SkipListNode] = current.forward[0]
        return candidate is not None and bool(candidate.key == key)

    def __len__(self) -> int:
        """Return the number of key-value pairs.

        Returns
        -------
        int
            Number of elements in the skip list.

        Examples
        --------
        >>> sl = SkipList()
        >>> len(sl)
        0
        >>> sl.insert(1)
        >>> len(sl)
        1
        """
        return self._length

    def __iter__(self) -> Iterator[Any]:
        """Iterate over keys in sorted ascending order.

        Yields
        ------
        Any
            Keys in sorted order (level-0 traversal).

        Examples
        --------
        >>> sl = SkipList()
        >>> for k in [3, 1, 2]:
        ...     sl.insert(k)
        >>> list(sl)
        [1, 2, 3]

        Notes
        -----
        Time complexity: O(n).
        """
        current = self._head.forward[0]
        while current is not None:
            yield current.key
            current = current.forward[0]

    # ------------------------------------------------------------------
    # Additional helpers
    # ------------------------------------------------------------------

    def items(self) -> Iterator[tuple[Any, Any]]:
        """Iterate over (key, value) pairs in sorted key order.

        Yields
        ------
        tuple[Any, Any]
            ``(key, value)`` pairs in ascending key order.

        Examples
        --------
        >>> sl = SkipList()
        >>> sl.insert(2, "b")
        >>> sl.insert(1, "a")
        >>> list(sl.items())
        [(1, 'a'), (2, 'b')]

        Notes
        -----
        Time complexity: O(n).
        """
        current = self._head.forward[0]
        while current is not None:
            yield current.key, current.value
            current = current.forward[0]

    def min_key(self) -> Any:
        """Return the smallest key, or None if empty.

        Returns
        -------
        Any or None
            Minimum key.

        Examples
        --------
        >>> sl = SkipList()
        >>> sl.min_key() is None
        True
        >>> sl.insert(5)
        >>> sl.insert(2)
        >>> sl.min_key()
        2

        Notes
        -----
        Time complexity: O(1) — first node in the base list.
        """
        node = self._head.forward[0]
        return node.key if node is not None else None

    def max_key(self) -> Any:
        """Return the largest key, or None if empty.

        Returns
        -------
        Any or None
            Maximum key.

        Examples
        --------
        >>> sl = SkipList()
        >>> sl.max_key() is None
        True
        >>> sl.insert(5)
        >>> sl.insert(2)
        >>> sl.max_key()
        5

        Notes
        -----
        Time complexity: O(n) — traverses the base list to the end.
        For O(1) max access, maintain a tail pointer (not implemented here).
        """
        current = self._head
        while current.forward[0] is not None:
            nxt_node = current.forward[0]
            if nxt_node is None:
                break
            current = nxt_node
        return current.key if current is not self._head else None

    # ------------------------------------------------------------------
    # Dunder methods
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        """Return a detailed string representation.

        Returns
        -------
        str
            ``SkipList(length=n, level=k, max_level=m, probability=p)``.

        Examples
        --------
        >>> sl = SkipList(max_level=8, probability=0.5)
        >>> repr(sl)
        'SkipList(length=0, level=0, max_level=8, probability=0.5)'
        """
        return (
            f"SkipList(length={self._length}, level={self._level}, "
            f"max_level={self._max_level}, probability={self._probability})"
        )

    def __str__(self) -> str:
        """Return a concise string representation.

        Returns
        -------
        str
            Human-readable summary.

        Examples
        --------
        >>> sl = SkipList()
        >>> sl.insert(1)
        >>> sl.insert(2)
        >>> str(sl)
        'SkipList: 2 elements, levels=0..16'
        """
        return f"SkipList: {self._length} elements, " f"levels=0..{self._max_level}"
