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

"""Hash Table data structures with two collision-resolution strategies.

This module provides two concrete hash table implementations that share the
same ``AbstractHashTable`` interface but differ in how they handle collisions:

- **Separate chaining** (``HashTableChaining``): each slot holds a list of
  ``(key, value)`` pairs. Handles load factors > 1 without degradation.
- **Open addressing with linear probing** (``HashTableOpenAddressing``): all
  entries live in the primary array. Requires load factor < 1 and uses a
  tombstone mechanism for deletion.

Both classes resize automatically (doubling capacity) when the load factor
exceeds a configurable threshold.

Classes
-------
HashTableChaining
    Hash table using separate chaining for collision resolution.
HashTableOpenAddressing
    Hash table using open addressing (linear probing) for collision resolution.

Examples
--------
HashTableChaining:

>>> ht = HashTableChaining()
>>> ht.put("name", "Alice")
>>> ht.get("name")
'Alice'
>>> "name" in ht
True
>>> ht.delete("name")
True

HashTableOpenAddressing:

>>> ht = HashTableOpenAddressing()
>>> ht.put(1, "one")
>>> ht.put(2, "two")
>>> ht.get(1)
'one'
>>> list(ht)  # doctest: +SKIP
[1, 2]

Notes
-----
Time Complexity (average case with good hash distribution):

+-------------------+----------+----------+
| Operation         | Chaining | Open Addr|
+===================+==========+==========+
| put               | O(1)     | O(1)     |
+-------------------+----------+----------+
| get               | O(1)     | O(1)     |
+-------------------+----------+----------+
| delete            | O(1)     | O(1)     |
+-------------------+----------+----------+
| resize            | O(n)     | O(n)     |
+-------------------+----------+----------+

Worst-case is O(n) for all operations when all keys hash to the same slot.

References
----------
.. [1] Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009).
       *Introduction to Algorithms* (3rd ed.), Chapter 11.
       MIT Press.
.. [2] OpenDSA — Hashing chapter.
       https://opendsa-server.cs.vt.edu/ODSA/Books/Everything/html/HashIntro.html
"""

from typing import Any, Iterator, Optional

from .interfaces import AbstractHashTable

__all__ = ["HashTableChaining", "HashTableOpenAddressing"]

# Sentinel used by open addressing to mark deleted slots
_DELETED: object = object()

# ---------------------------------------------------------------------------
# HashTableChaining
# ---------------------------------------------------------------------------


class HashTableChaining(AbstractHashTable):
    """Hash table using separate chaining for collision resolution.

    Each slot in the internal array holds a list of ``(key, value)`` pairs.
    When multiple keys hash to the same index, they are stored together in
    the same chain (list). This strategy handles load factors above 1 without
    structural failure, though performance degrades linearly.

    Automatic resizing doubles the capacity when the load factor exceeds
    ``max_load_factor``.

    Parameters
    ----------
    capacity : int
        Initial number of slots. Must be ≥ 1. Default is 16.
    max_load_factor : float
        Threshold load factor that triggers a resize. Must be > 0.
        Default is 0.75.

    Attributes
    ----------
    capacity : int
        Current number of slots (read-only).
    load_factor : float
        Current ratio of stored entries to slots (read-only).

    Raises
    ------
    ValueError
        If ``capacity < 1`` or ``max_load_factor <= 0``.

    Examples
    --------
    >>> ht = HashTableChaining(capacity=8)
    >>> ht.put("x", 10)
    >>> ht.put("y", 20)
    >>> ht.get("x")
    10
    >>> "y" in ht
    True
    >>> ht.delete("x")
    True
    >>> len(ht)
    1

    Notes
    -----
    - Keys must be hashable (support Python's built-in ``hash()``).
    - Stored values may be any Python object, including ``None``.
    - Updating an existing key replaces its value without changing ``len()``.
    """

    def __init__(
        self,
        capacity: int = 16,
        max_load_factor: float = 0.75,
    ) -> None:
        """Initialise an empty chaining hash table.

        Parameters
        ----------
        capacity : int
            Initial number of slots (default 16).
        max_load_factor : float
            Resize threshold (default 0.75).

        Raises
        ------
        ValueError
            If ``capacity < 1`` or ``max_load_factor <= 0``.

        Examples
        --------
        >>> ht = HashTableChaining()
        >>> len(ht)
        0

        Notes
        -----
        Time complexity: O(capacity).
        """
        if capacity < 1:
            raise ValueError(f"capacity must be at least 1, got {capacity}")
        if max_load_factor <= 0:
            raise ValueError(f"max_load_factor must be positive, got {max_load_factor}")
        self._capacity = capacity
        self._max_load_factor = max_load_factor
        self._size = 0
        # Each slot: list of [key, value] pairs
        self._buckets: list[list[list[Any]]] = [[] for _ in range(capacity)]

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def capacity(self) -> int:
        """Current number of slots.

        Returns
        -------
        int
            Number of buckets in the internal array.
        """
        return self._capacity

    @property
    def load_factor(self) -> float:
        """Ratio of stored entries to available slots.

        Returns
        -------
        float
            ``len(self) / capacity``.
        """
        return self._size / self._capacity

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _index(self, key: Any) -> int:
        """Compute the bucket index for *key*."""
        return hash(key) % self._capacity

    def _resize(self) -> None:
        """Double the capacity and rehash all entries."""
        old_buckets = self._buckets
        self._capacity *= 2
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0
        for bucket in old_buckets:
            for pair in bucket:
                self.put(pair[0], pair[1])

    # ------------------------------------------------------------------
    # AbstractHashTable interface
    # ------------------------------------------------------------------

    def is_empty(self) -> bool:
        """Return True if the table contains no entries.

        Returns
        -------
        bool
            True if size is 0.

        Notes
        -----
        Time complexity: O(1).
        """
        return self._size == 0

    def clear(self) -> None:
        """Remove all entries from the table.

        Resets all buckets without changing capacity.

        Notes
        -----
        Time complexity: O(capacity).
        """
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0

    def put(self, key: Any, value: Any) -> None:
        """Insert or update a key-value pair.

        If *key* already exists its value is updated in place. Otherwise a
        new entry is appended to the appropriate chain. Triggers a resize if
        the load factor exceeds ``max_load_factor`` after insertion.

        Parameters
        ----------
        key : Any
            Hashable key.
        value : Any
            Value to store.

        Examples
        --------
        >>> ht = HashTableChaining()
        >>> ht.put("a", 1)
        >>> ht.put("a", 2)   # update
        >>> ht.get("a")
        2
        >>> len(ht)
        1

        Notes
        -----
        Time complexity: O(1) average, O(n) on resize.
        """
        idx = self._index(key)
        for pair in self._buckets[idx]:
            if pair[0] == key:
                pair[1] = value
                return
        self._buckets[idx].append([key, value])
        self._size += 1
        if self.load_factor > self._max_load_factor:
            self._resize()

    def get(self, key: Any) -> Optional[Any]:
        """Return the value for *key*, or None if absent.

        Parameters
        ----------
        key : Any
            Key to look up.

        Returns
        -------
        Any or None
            Stored value, or None if the key is not present.

        Examples
        --------
        >>> ht = HashTableChaining()
        >>> ht.put(1, "one")
        >>> ht.get(1)
        'one'
        >>> ht.get(99) is None
        True

        Notes
        -----
        Time complexity: O(1) average.
        """
        idx = self._index(key)
        for pair in self._buckets[idx]:
            if pair[0] == key:
                return pair[1]
        return None

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
        >>> ht = HashTableChaining()
        >>> ht.put(5, "five")
        >>> ht.delete(5)
        True
        >>> ht.delete(5)
        False

        Notes
        -----
        Time complexity: O(1) average.
        """
        idx = self._index(key)
        bucket = self._buckets[idx]
        for i, pair in enumerate(bucket):
            if pair[0] == key:
                bucket.pop(i)
                self._size -= 1
                return True
        return False

    def __contains__(self, key: Any) -> bool:
        """Test whether *key* is in the table.

        Parameters
        ----------
        key : Any
            Key to test.

        Returns
        -------
        bool
            True if present.

        Examples
        --------
        >>> ht = HashTableChaining()
        >>> ht.put("hello", 1)
        >>> "hello" in ht
        True
        >>> "world" in ht
        False

        Notes
        -----
        Time complexity: O(1) average.
        """
        idx = self._index(key)
        return any(pair[0] == key for pair in self._buckets[idx])

    def __len__(self) -> int:
        """Return the number of stored key-value pairs.

        Returns
        -------
        int
            Number of entries.

        Examples
        --------
        >>> ht = HashTableChaining()
        >>> ht.put(1, "a")
        >>> ht.put(2, "b")
        >>> len(ht)
        2
        """
        return self._size

    def __iter__(self) -> Iterator[Any]:
        """Iterate over all keys in unspecified order.

        Yields
        ------
        Any
            One key per stored entry.

        Examples
        --------
        >>> ht = HashTableChaining()
        >>> ht.put(1, "a")
        >>> ht.put(2, "b")
        >>> sorted(ht)
        [1, 2]

        Notes
        -----
        Time complexity: O(capacity + n).
        """
        for bucket in self._buckets:
            for pair in bucket:
                yield pair[0]

    def items(self) -> Iterator[tuple[Any, Any]]:
        """Iterate over ``(key, value)`` pairs in unspecified order.

        Yields
        ------
        tuple[Any, Any]
            ``(key, value)`` pairs.

        Examples
        --------
        >>> ht = HashTableChaining()
        >>> ht.put("a", 1)
        >>> sorted(ht.items())
        [('a', 1)]

        Notes
        -----
        Time complexity: O(capacity + n).
        """
        for bucket in self._buckets:
            for pair in bucket:
                yield pair[0], pair[1]

    def __getitem__(self, key: Any) -> Any:
        """Return value for *key*, raising KeyError if absent.

        Parameters
        ----------
        key : Any
            Key to retrieve.

        Returns
        -------
        Any
            Associated value.

        Raises
        ------
        KeyError
            If *key* is not in the table.

        Examples
        --------
        >>> ht = HashTableChaining()
        >>> ht.put("k", 42)
        >>> ht["k"]
        42
        """
        idx = self._index(key)
        for pair in self._buckets[idx]:
            if pair[0] == key:
                return pair[1]
        raise KeyError(key)

    def __setitem__(self, key: Any, value: Any) -> None:
        """Syntactic sugar for put().

        Examples
        --------
        >>> ht = HashTableChaining()
        >>> ht["x"] = 99
        >>> ht["x"]
        99
        """
        self.put(key, value)

    def __repr__(self) -> str:
        """Return a detailed string representation.

        Returns
        -------
        str
            ``HashTableChaining(size=n, capacity=m, load_factor=x.xx)``.

        Examples
        --------
        >>> ht = HashTableChaining(capacity=8)
        >>> repr(ht)
        'HashTableChaining(size=0, capacity=8, load_factor=0.00)'
        """
        return (
            f"HashTableChaining(size={self._size}, "
            f"capacity={self._capacity}, "
            f"load_factor={self.load_factor:.2f})"
        )

    def __str__(self) -> str:
        """Return a concise string representation.

        Returns
        -------
        str
            Human-readable summary.

        Examples
        --------
        >>> ht = HashTableChaining()
        >>> str(ht)
        'HashTableChaining: 0 entries'
        """
        return f"HashTableChaining: {self._size} entries"


# ---------------------------------------------------------------------------
# HashTableOpenAddressing
# ---------------------------------------------------------------------------


class HashTableOpenAddressing(AbstractHashTable):
    """Hash table using open addressing with linear probing.

    All entries are stored directly in the primary array. On collision, the
    algorithm probes subsequent slots (``index + 1``, ``index + 2``, …) until
    an empty slot is found. Deleted slots are marked with a sentinel
    (``_DELETED``) so that probing chains are not broken.

    Automatic resizing doubles the capacity when the load factor (including
    tombstones) exceeds ``max_load_factor``.

    Parameters
    ----------
    capacity : int
        Initial number of slots. Must be ≥ 2. Default is 16.
    max_load_factor : float
        Resize threshold. Must be in (0.0, 1.0). Default is 0.6.

    Attributes
    ----------
    capacity : int
        Current number of slots (read-only).
    load_factor : float
        Ratio of active entries to slots (read-only). Excludes tombstones.

    Raises
    ------
    ValueError
        If ``capacity < 2`` or ``max_load_factor`` not in (0, 1).

    Examples
    --------
    >>> ht = HashTableOpenAddressing(capacity=8)
    >>> ht.put(1, "one")
    >>> ht.put(2, "two")
    >>> ht.get(1)
    'one'
    >>> 2 in ht
    True
    >>> ht.delete(1)
    True
    >>> len(ht)
    1

    Notes
    -----
    - Keys must be hashable and support ``==``.
    - Load factor must remain below 1.0 (enforced by max_load_factor < 1.0).
    - Tombstones (``_DELETED``) accumulate after deletions; a resize clears
      them by rehashing all live entries.
    - Linear probing suffers from *primary clustering*. For production use
      with adversarial input, consider quadratic probing or double hashing.
    """

    def __init__(
        self,
        capacity: int = 16,
        max_load_factor: float = 0.6,
    ) -> None:
        """Initialise an empty open-addressing hash table.

        Parameters
        ----------
        capacity : int
            Initial number of slots (default 16). Must be ≥ 2.
        max_load_factor : float
            Resize threshold (default 0.6). Must be in (0.0, 1.0).

        Raises
        ------
        ValueError
            If ``capacity < 2`` or ``max_load_factor`` not in (0, 1).

        Examples
        --------
        >>> ht = HashTableOpenAddressing()
        >>> len(ht)
        0

        Notes
        -----
        Time complexity: O(capacity).
        """
        if capacity < 2:
            raise ValueError(f"capacity must be at least 2, got {capacity}")
        if not (0.0 < max_load_factor < 1.0):
            raise ValueError(
                f"max_load_factor must be in (0.0, 1.0), got {max_load_factor}"
            )
        self._capacity = capacity
        self._max_load_factor = max_load_factor
        self._size = 0
        # None = empty, _DELETED = tombstone, otherwise (key, value)
        self._slots: list[Any] = [None] * capacity

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def capacity(self) -> int:
        """Current number of slots.

        Returns
        -------
        int
            Size of the internal array.
        """
        return self._capacity

    @property
    def load_factor(self) -> float:
        """Ratio of live entries to total slots.

        Returns
        -------
        float
            ``len(self) / capacity``. Tombstones are excluded.
        """
        return self._size / self._capacity

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _index(self, key: Any) -> int:
        """Compute the home slot index for *key*."""
        return hash(key) % self._capacity

    def _probe(self, key: Any) -> tuple[int, bool]:
        """Linear probe to find the slot for *key*.

        Returns
        -------
        tuple[int, bool]
            ``(slot_index, found)`` where *found* is True if *key* is
            already present, False if an empty slot was reached.
        """
        idx = self._index(key)
        first_deleted: Optional[int] = None

        for i in range(self._capacity):
            slot = self._slots[(idx + i) % self._capacity]
            pos = (idx + i) % self._capacity

            if slot is None:
                # Key not found; best insertion point is first tombstone
                return (first_deleted if first_deleted is not None else pos, False)
            elif slot is _DELETED:
                if first_deleted is None:
                    first_deleted = pos
            elif slot[0] == key:
                return (pos, True)

        # Table full of live entries or tombstones (should not happen after resize)
        return (first_deleted if first_deleted is not None else idx, False)

    def _resize(self) -> None:
        """Double capacity and rehash all live entries (clears tombstones)."""
        old_slots = self._slots
        self._capacity *= 2
        self._slots = [None] * self._capacity
        self._size = 0
        for slot in old_slots:
            if slot is not None and slot is not _DELETED:
                self.put(slot[0], slot[1])

    # ------------------------------------------------------------------
    # AbstractHashTable interface
    # ------------------------------------------------------------------

    def is_empty(self) -> bool:
        """Return True if the table contains no live entries.

        Returns
        -------
        bool
            True if size is 0.

        Notes
        -----
        Time complexity: O(1).
        """
        return self._size == 0

    def clear(self) -> None:
        """Remove all entries and tombstones from the table.

        Resets the slot array without changing capacity.

        Notes
        -----
        Time complexity: O(capacity).
        """
        self._slots = [None] * self._capacity
        self._size = 0

    def put(self, key: Any, value: Any) -> None:
        """Insert or update a key-value pair.

        Probes linearly from the home slot. If *key* already exists its
        value is updated; otherwise the entry is placed in the first
        available slot (empty or tombstone). Triggers a resize when the live
        load factor exceeds ``max_load_factor``.

        Parameters
        ----------
        key : Any
            Hashable key.
        value : Any
            Value to store.

        Examples
        --------
        >>> ht = HashTableOpenAddressing()
        >>> ht.put("a", 1)
        >>> ht.put("a", 2)   # update
        >>> ht.get("a")
        2
        >>> len(ht)
        1

        Notes
        -----
        Time complexity: O(1) average, O(n) on resize.
        """
        if self.load_factor >= self._max_load_factor:
            self._resize()

        pos, found = self._probe(key)
        self._slots[pos] = (key, value)
        if not found:
            self._size += 1

    def get(self, key: Any) -> Optional[Any]:
        """Return the value for *key*, or None if absent.

        Parameters
        ----------
        key : Any
            Key to look up.

        Returns
        -------
        Any or None
            Stored value, or None if the key is not present.

        Examples
        --------
        >>> ht = HashTableOpenAddressing()
        >>> ht.put(1, "one")
        >>> ht.get(1)
        'one'
        >>> ht.get(99) is None
        True

        Notes
        -----
        Time complexity: O(1) average.
        """
        _, found = self._probe(key)
        if found:
            idx = self._index(key)
            for i in range(self._capacity):
                slot = self._slots[(idx + i) % self._capacity]
                if slot is None:
                    return None
                if slot is not _DELETED and slot[0] == key:
                    return slot[1]
        return None

    def delete(self, key: Any) -> bool:
        """Remove the entry with the given key.

        Marks the slot with a tombstone (``_DELETED``) so that probing chains
        remain intact. Tombstones are cleared on the next resize.

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
        >>> ht = HashTableOpenAddressing()
        >>> ht.put(5, "five")
        >>> ht.delete(5)
        True
        >>> ht.delete(5)
        False

        Notes
        -----
        Time complexity: O(1) average.
        """
        idx = self._index(key)
        for i in range(self._capacity):
            pos = (idx + i) % self._capacity
            slot = self._slots[pos]
            if slot is None:
                return False
            if slot is _DELETED:
                continue
            if slot[0] == key:
                self._slots[pos] = _DELETED
                self._size -= 1
                return True
        return False

    def __contains__(self, key: Any) -> bool:
        """Test whether *key* is in the table.

        Parameters
        ----------
        key : Any
            Key to test.

        Returns
        -------
        bool
            True if present.

        Examples
        --------
        >>> ht = HashTableOpenAddressing()
        >>> ht.put("k", 1)
        >>> "k" in ht
        True
        >>> "z" in ht
        False

        Notes
        -----
        Time complexity: O(1) average.
        """
        _, found = self._probe(key)
        return found

    def __len__(self) -> int:
        """Return the number of stored key-value pairs.

        Returns
        -------
        int
            Number of live entries (tombstones excluded).

        Examples
        --------
        >>> ht = HashTableOpenAddressing()
        >>> ht.put(1, "a")
        >>> len(ht)
        1
        """
        return self._size

    def __iter__(self) -> Iterator[Any]:
        """Iterate over all keys in unspecified order.

        Yields
        ------
        Any
            One key per live entry.

        Examples
        --------
        >>> ht = HashTableOpenAddressing()
        >>> ht.put(1, "a")
        >>> ht.put(2, "b")
        >>> sorted(ht)
        [1, 2]

        Notes
        -----
        Time complexity: O(capacity).
        """
        for slot in self._slots:
            if slot is not None and slot is not _DELETED:
                yield slot[0]

    def items(self) -> Iterator[tuple[Any, Any]]:
        """Iterate over ``(key, value)`` pairs in unspecified order.

        Yields
        ------
        tuple[Any, Any]
            ``(key, value)`` pairs for all live entries.

        Examples
        --------
        >>> ht = HashTableOpenAddressing()
        >>> ht.put("x", 10)
        >>> list(ht.items())
        [('x', 10)]

        Notes
        -----
        Time complexity: O(capacity).
        """
        for slot in self._slots:
            if slot is not None and slot is not _DELETED:
                yield slot[0], slot[1]

    def __getitem__(self, key: Any) -> Any:
        """Return value for *key*, raising KeyError if absent.

        Parameters
        ----------
        key : Any
            Key to retrieve.

        Returns
        -------
        Any
            Associated value.

        Raises
        ------
        KeyError
            If *key* is not present.

        Examples
        --------
        >>> ht = HashTableOpenAddressing()
        >>> ht.put("k", 42)
        >>> ht["k"]
        42
        """
        idx = self._index(key)
        for i in range(self._capacity):
            slot = self._slots[(idx + i) % self._capacity]
            if slot is None:
                raise KeyError(key)
            if slot is not _DELETED and slot[0] == key:
                return slot[1]
        raise KeyError(key)

    def __setitem__(self, key: Any, value: Any) -> None:
        """Syntactic sugar for put().

        Examples
        --------
        >>> ht = HashTableOpenAddressing()
        >>> ht["x"] = 99
        >>> ht["x"]
        99
        """
        self.put(key, value)

    def __repr__(self) -> str:
        """Return a detailed string representation.

        Returns
        -------
        str
            ``HashTableOpenAddressing(size=n, capacity=m, load_factor=x.xx)``.

        Examples
        --------
        >>> ht = HashTableOpenAddressing(capacity=8)
        >>> repr(ht)
        'HashTableOpenAddressing(size=0, capacity=8, load_factor=0.00)'
        """
        return (
            f"HashTableOpenAddressing(size={self._size}, "
            f"capacity={self._capacity}, "
            f"load_factor={self.load_factor:.2f})"
        )

    def __str__(self) -> str:
        """Return a concise string representation.

        Returns
        -------
        str
            Human-readable summary.

        Examples
        --------
        >>> ht = HashTableOpenAddressing()
        >>> str(ht)
        'HashTableOpenAddressing: 0 entries'
        """
        return f"HashTableOpenAddressing: {self._size} entries"
