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

"""LRU Cache data structure.

A Least Recently Used (LRU) cache stores a bounded number of key-value pairs.
When the cache reaches its capacity and a new key must be inserted, the entry
that has not been accessed for the longest time is evicted.

Classes
-------
_LRUNode
    Internal doubly-linked list node.
LRUCache
    O(1) get/put LRU cache backed by a doubly-linked list and a hash map.

Examples
--------
Basic usage:

>>> cache = LRUCache(capacity=3)
>>> cache.put(1, "one")
>>> cache.put(2, "two")
>>> cache.put(3, "three")
>>> cache.get(1)
'one'
>>> cache.put(4, "four")   # evicts key 2 (least recently used)
>>> cache.get(2) is None
True
>>> cache.get(4)
'four'

Checking capacity and eviction order:

>>> cache = LRUCache(capacity=2)
>>> cache.put("a", 1)
>>> cache.put("b", 2)
>>> cache.get("a")         # "a" becomes most recently used
1
>>> cache.put("c", 3)      # evicts "b"
>>> "b" in cache
False
>>> "a" in cache
True

Notes
-----
Time Complexity:
- get: O(1)
- put: O(1)
- __contains__: O(1)
- __len__: O(1)
- evictions_count: O(1)

Space Complexity: O(capacity).

The implementation uses two sentinel nodes (``_head`` and ``_tail``) for the
doubly-linked list so that insertion and removal never need to check for
None neighbours.

References
----------
.. [1] Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009).
       *Introduction to Algorithms* (3rd ed.), Chapter 11.
       MIT Press.
.. [2] LeetCode problem 146 — LRU Cache (canonical interview problem).
       https://leetcode.com/problems/lru-cache/
"""

from typing import Any, Iterator, Optional

from .interfaces import AbstractLRUCache

__all__ = ["LRUCache"]

# ---------------------------------------------------------------------------
# Internal node
# ---------------------------------------------------------------------------


class _LRUNode:
    """Doubly-linked list node for LRUCache.

    Parameters
    ----------
    key : Any
        Cache key stored in this node.
    value : Any
        Associated value.
    """

    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: Any = None, value: Any = None) -> None:
        self.key = key
        self.value = value
        self.prev: Optional["_LRUNode"] = None
        self.next: Optional["_LRUNode"] = None


# ---------------------------------------------------------------------------
# LRUCache
# ---------------------------------------------------------------------------


class LRUCache(AbstractLRUCache):
    """Least Recently Used cache with O(1) get and put.

    The cache holds at most *capacity* key-value pairs. When full, the
    entry that has not been accessed (via ``get`` or ``put``) for the
    longest time is evicted on the next ``put``.

    Internally, a doubly-linked list maintains access order (most recent
    at the tail, least recent at the head) while a dict maps keys to list
    nodes for O(1) random access.

    Parameters
    ----------
    capacity : int
        Maximum number of entries. Must be ≥ 1.

    Attributes
    ----------
    capacity : int
        Maximum number of entries (read-only).
    evictions_count : int
        Total number of entries evicted since creation (read-only).

    Raises
    ------
    ValueError
        If ``capacity < 1``.

    Examples
    --------
    >>> cache = LRUCache(capacity=2)
    >>> cache.put(1, "one")
    >>> cache.put(2, "two")
    >>> cache.get(1)
    'one'
    >>> cache.put(3, "three")   # evicts key 2
    >>> cache.get(2) is None
    True
    >>> len(cache)
    2

    Notes
    -----
    - ``__contains__`` does **not** update recency; only ``get`` and ``put``
      move an entry to the most-recently-used position.
    - Keys must be hashable. Values may be any Python object, including None.
    - Updating an existing key via ``put`` refreshes its recency position.
    """

    def __init__(self, capacity: int) -> None:
        """Initialise an empty LRU cache.

        Parameters
        ----------
        capacity : int
            Maximum number of entries. Must be ≥ 1.

        Raises
        ------
        ValueError
            If ``capacity < 1``.

        Examples
        --------
        >>> cache = LRUCache(capacity=5)
        >>> len(cache)
        0

        Notes
        -----
        Time complexity: O(1).
        """
        if capacity < 1:
            raise ValueError(f"capacity must be at least 1, got {capacity}")
        self._capacity = capacity
        self._evictions = 0
        # key → node
        self._map: dict[Any, _LRUNode] = {}

        # Sentinel head (LRU end) and tail (MRU end)
        self._head = _LRUNode()
        self._tail = _LRUNode()
        self._head.next = self._tail
        self._tail.prev = self._head

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def capacity(self) -> int:
        """Maximum number of entries.

        Returns
        -------
        int
            Value passed at construction.
        """
        return self._capacity

    @property
    def evictions_count(self) -> int:
        """Total number of evictions performed since creation.

        Returns
        -------
        int
            Monotonically increasing counter.

        Examples
        --------
        >>> cache = LRUCache(capacity=1)
        >>> cache.put(1, "a")
        >>> cache.put(2, "b")   # evicts 1
        >>> cache.evictions_count
        1
        """
        return self._evictions

    # ------------------------------------------------------------------
    # Internal list operations (O(1))
    # ------------------------------------------------------------------

    def _remove(self, node: _LRUNode) -> None:
        """Unlink *node* from the doubly-linked list."""
        prev = node.prev
        nxt = node.next
        if prev is not None:
            prev.next = nxt
        if nxt is not None:
            nxt.prev = prev

    def _append_tail(self, node: _LRUNode) -> None:
        """Insert *node* just before the tail sentinel (MRU position)."""
        prev = self._tail.prev
        if prev is not None:
            prev.next = node
        node.prev = prev
        node.next = self._tail
        self._tail.prev = node

    def _move_to_tail(self, node: _LRUNode) -> None:
        """Move an existing *node* to the MRU position."""
        self._remove(node)
        self._append_tail(node)

    def _evict_lru(self) -> None:
        """Remove the least recently used node (first after head sentinel)."""
        lru = self._head.next
        if lru is self._tail:
            return  # empty list — should not happen in normal flow
        self._remove(lru)  # type: ignore[arg-type]
        del self._map[lru.key]  # type: ignore[union-attr]
        self._evictions += 1

    # ------------------------------------------------------------------
    # AbstractLRUCache interface
    # ------------------------------------------------------------------

    def is_empty(self) -> bool:
        """Return True if the cache contains no entries.

        Returns
        -------
        bool
            True if len(self) == 0.

        Notes
        -----
        Time complexity: O(1).
        """
        return len(self._map) == 0

    def __iter__(self) -> "Iterator[Any]":
        """Iterate over keys from least recently used to most recently used.

        Yields
        ------
        Any
            Keys in LRU → MRU order.

        Notes
        -----
        Time complexity: O(n).
        """
        node = self._head.next
        while node is not None and node is not self._tail:
            yield node.key
            node = node.next

    def get(self, key: Any) -> Optional[Any]:
        """Return the value for *key* and mark it as most recently used.

        Parameters
        ----------
        key : Any
            Key to look up.

        Returns
        -------
        Any or None
            The stored value, or None if *key* is not in the cache.

        Examples
        --------
        >>> cache = LRUCache(capacity=2)
        >>> cache.put("a", 1)
        >>> cache.get("a")
        1
        >>> cache.get("missing") is None
        True

        Notes
        -----
        Time complexity: O(1).
        """
        node = self._map.get(key)
        if node is None:
            return None
        self._move_to_tail(node)
        return node.value

    def put(self, key: Any, value: Any) -> None:
        """Insert or update a key-value pair.

        If *key* already exists its value is updated and it is moved to the
        most-recently-used position. If the cache is at capacity, the least
        recently used entry is evicted before the new entry is inserted.

        Parameters
        ----------
        key : Any
            Hashable key.
        value : Any
            Value to store.

        Examples
        --------
        >>> cache = LRUCache(capacity=2)
        >>> cache.put(1, "one")
        >>> cache.put(1, "ONE")   # update
        >>> cache.get(1)
        'ONE'
        >>> len(cache)
        1

        Notes
        -----
        Time complexity: O(1).
        """
        if key in self._map:
            node = self._map[key]
            node.value = value
            self._move_to_tail(node)
            return

        if len(self._map) >= self._capacity:
            self._evict_lru()

        node = _LRUNode(key, value)
        self._map[key] = node
        self._append_tail(node)

    def __contains__(self, key: Any) -> bool:
        """Test whether *key* is currently in the cache.

        Does **not** update the recency order.

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
        >>> cache = LRUCache(capacity=2)
        >>> cache.put(1, "a")
        >>> 1 in cache
        True
        >>> 99 in cache
        False

        Notes
        -----
        Time complexity: O(1).
        """
        return key in self._map

    def __len__(self) -> int:
        """Return the number of entries currently stored.

        Returns
        -------
        int
            Number of live entries (≤ capacity).

        Examples
        --------
        >>> cache = LRUCache(capacity=5)
        >>> cache.put(1, "a")
        >>> cache.put(2, "b")
        >>> len(cache)
        2

        Notes
        -----
        Time complexity: O(1).
        """
        return len(self._map)

    # ------------------------------------------------------------------
    # Additional helpers
    # ------------------------------------------------------------------

    def peek(self, key: Any) -> Optional[Any]:
        """Return the value for *key* without updating recency.

        Unlike ``get``, this method does not move the entry to the
        most-recently-used position.

        Parameters
        ----------
        key : Any
            Key to look up.

        Returns
        -------
        Any or None
            Stored value, or None if absent.

        Examples
        --------
        >>> cache = LRUCache(capacity=2)
        >>> cache.put(1, "a")
        >>> cache.put(2, "b")
        >>> cache.peek(1)       # does not promote key 1
        'a'

        Notes
        -----
        Time complexity: O(1).
        """
        node = self._map.get(key)
        return node.value if node is not None else None

    def keys(self) -> list[Any]:
        """Return all keys from least recently used to most recently used.

        Returns
        -------
        list[Any]
            Keys ordered LRU → MRU.

        Examples
        --------
        >>> cache = LRUCache(capacity=3)
        >>> cache.put(1, "a")
        >>> cache.put(2, "b")
        >>> cache.put(3, "c")
        >>> cache.get(1)        # 1 becomes MRU
        'a'
        >>> cache.keys()        # LRU first
        [2, 3, 1]

        Notes
        -----
        Time complexity: O(n).
        """
        result = []
        node = self._head.next
        while node is not None and node is not self._tail:
            result.append(node.key)
            node = node.next
        return result

    def items(self) -> Iterator[tuple[Any, Any]]:
        """Iterate over ``(key, value)`` pairs from LRU to MRU.

        Yields
        ------
        tuple[Any, Any]
            ``(key, value)`` in LRU → MRU order.

        Examples
        --------
        >>> cache = LRUCache(capacity=2)
        >>> cache.put("a", 1)
        >>> cache.put("b", 2)
        >>> list(cache.items())
        [('a', 1), ('b', 2)]

        Notes
        -----
        Time complexity: O(n).
        """
        node = self._head.next
        while node is not None and node is not self._tail:
            yield node.key, node.value
            node = node.next

    def delete(self, key: Any) -> bool:
        """Remove the entry with the given key.

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
        >>> cache = LRUCache(capacity=2)
        >>> cache.put(1, "a")
        >>> cache.delete(1)
        True
        >>> cache.delete(1)
        False

        Notes
        -----
        Time complexity: O(1).
        """
        node = self._map.get(key)
        if node is None:
            return False
        self._remove(node)
        del self._map[key]
        return True

    def clear(self) -> None:
        """Remove all entries from the cache.

        The ``evictions_count`` is **not** incremented for cleared entries.

        Examples
        --------
        >>> cache = LRUCache(capacity=3)
        >>> cache.put(1, "a")
        >>> cache.clear()
        >>> len(cache)
        0

        Notes
        -----
        Time complexity: O(n).
        """
        self._map.clear()
        self._head.next = self._tail
        self._tail.prev = self._head

    # ------------------------------------------------------------------
    # Dunder methods
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        """Return a detailed string representation.

        Returns
        -------
        str
            ``LRUCache(capacity=n, size=m, evictions=k)``.

        Examples
        --------
        >>> cache = LRUCache(capacity=3)
        >>> repr(cache)
        'LRUCache(capacity=3, size=0, evictions=0)'
        """
        return (
            f"LRUCache(capacity={self._capacity}, "
            f"size={len(self)}, "
            f"evictions={self._evictions})"
        )

    def __str__(self) -> str:
        """Return a concise string representation.

        Returns
        -------
        str
            Human-readable summary.

        Examples
        --------
        >>> cache = LRUCache(capacity=3)
        >>> cache.put(1, "a")
        >>> str(cache)
        'LRUCache: 1/3 entries'
        """
        return f"LRUCache: {len(self)}/{self._capacity} entries"
