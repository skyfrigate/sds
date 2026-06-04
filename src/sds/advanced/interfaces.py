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

"""Abstract interfaces for advanced data structures.

This module provides abstract base classes that define contracts for
advanced data structures like disjoint sets, probabilistic structures,
and specialized trees.

Classes
-------
AbstractDisjointSet
    Interface for Union-Find / Disjoint Set data structure.
AbstractProbabilisticSet
    Interface for probabilistic membership structures.

Notes
-----
These interfaces ensure consistency across different implementations
and enable polymorphic usage of advanced structures.

See Also
--------
sds.core.interfaces : Core collection interfaces.
sds.advanced.disjoint_set : Concrete disjoint set implementation.
"""

from abc import abstractmethod
from typing import Any, Iterator, List, Optional, Set

from ..core.interfaces import Collection

__all__ = [
    "AbstractDisjointSet",
    "AbstractProbabilisticSet",
    "AbstractSkipList",
    "AbstractHashTable",
    "AbstractLRUCache",
    "AbstractFenwickTree",
]


class AbstractDisjointSet(Collection):
    """Abstract base class for Disjoint Set (Union-Find) data structure.

    A disjoint-set data structure maintains a collection of disjoint sets
    and supports efficient union and find operations. This is fundamental
    for algorithms like Kruskal's MST and cycle detection.

    Notes
    -----
    Implementations should use:
    - Path compression in find() for O(α(n)) amortized complexity
    - Union by rank or size for balanced trees
    - α(n) is the inverse Ackermann function, effectively constant

    See Also
    --------
    DisjointSet : Concrete implementation with optimizations.
    """

    @abstractmethod
    def make_set(self, element: Any) -> None:
        """Create a new set containing only the given element.

        Parameters
        ----------
        element : Any
            Element to create a set for (must be hashable).

        Raises
        ------
        ValueError
            If element already exists in a set.

        Notes
        -----
        Time complexity: O(1)
        """
        pass

    @abstractmethod
    def find(self, element: Any) -> Any:
        """Find the representative of the set containing element.

        Parameters
        ----------
        element : Any
            Element to find the representative for.

        Returns
        -------
        Any
            Representative (root) of the set containing element.

        Raises
        ------
        ValueError
            If element is not in any set.

        Notes
        -----
        Time complexity: O(α(n)) amortized with path compression.
        """
        pass

    @abstractmethod
    def union(self, x: Any, y: Any) -> bool:
        """Unite the sets containing x and y.

        Parameters
        ----------
        x : Any
            Element in first set.
        y : Any
            Element in second set.

        Returns
        -------
        bool
            True if sets were merged (were different), False otherwise.

        Raises
        ------
        ValueError
            If x or y is not in any set.

        Notes
        -----
        Time complexity: O(α(n)) amortized with union by rank.
        """
        pass

    @abstractmethod
    def connected(self, x: Any, y: Any) -> bool:
        """Check if x and y are in the same set.

        Parameters
        ----------
        x : Any
            First element.
        y : Any
            Second element.

        Returns
        -------
        bool
            True if x and y are in the same set.

        Raises
        ------
        ValueError
            If x or y is not in any set.

        Notes
        -----
        Time complexity: O(α(n)) amortized.
        """
        pass

    @abstractmethod
    def get_sets(self) -> List[Set[Any]]:
        """Get all disjoint sets.

        Returns
        -------
        List[Set[Any]]
            List of all disjoint sets.

        Notes
        -----
        Time complexity: O(n)
        """
        pass

    @abstractmethod
    def count_sets(self) -> int:
        """Get the number of disjoint sets.

        Returns
        -------
        int
            Number of disjoint sets.

        Notes
        -----
        Time complexity: O(1)
        """
        pass

    @abstractmethod
    def size(self, element: Any) -> int:
        """Get the size of the set containing element.

        Parameters
        ----------
        element : Any
            Element in the set.

        Returns
        -------
        int
            Number of elements in the set.

        Raises
        ------
        ValueError
            If element is not in any set.

        Notes
        -----
        Time complexity: O(α(n)) amortized.
        """
        pass


class AbstractProbabilisticSet(Collection):
    """Abstract base class for probabilistic set membership structures.

    Probabilistic structures like Bloom Filters trade perfect accuracy
    for space efficiency, allowing false positives but no false negatives.

    Notes
    -----
    These structures are useful when:
    - Space is limited
    - Approximate answers are acceptable
    - False positives can be handled
    - False negatives are unacceptable

    See Also
    --------
    BloomFilter : Space-efficient probabilistic set.
    """

    @abstractmethod
    def add(self, item: Any) -> None:
        """Add an item to the set.

        Parameters
        ----------
        item : Any
            Item to add (must be hashable).

        Notes
        -----
        After adding, contains(item) will always return True.
        """
        pass

    @abstractmethod
    def __contains__(self, item: Any) -> bool:
        """Test if item might be in the set.

        Parameters
        ----------
        item : Any
            Item to test.

        Returns
        -------
        bool
            True if item might be in set (possible false positive).
            False if item is definitely not in set (no false negatives).

        Notes
        -----
        False positives are possible, false negatives are not.
        """
        pass

    @abstractmethod
    def estimated_fill_ratio(self) -> float:
        """Get the estimated fill ratio of the structure.

        Returns
        -------
        float
            Ratio of filled slots (0.0 to 1.0).

        Notes
        -----
        Higher fill ratios increase false positive probability.
        """
        pass


class AbstractSkipList(Collection):
    """Abstract base class for the Skip List probabilistic data structure.

    A skip list is a probabilistic sorted data structure that allows
    O(log n) average-case search, insertion, and deletion by maintaining
    multiple levels of linked lists, each a subset of the level below.

    Notes
    -----
    Implementations should:
    - Use a geometric distribution (probability p) to select node height.
    - Maintain a sentinel head node of maximum height.
    - Support forward iteration in sorted order.

    Time complexity (average, with p=0.5):
    - search: O(log n)
    - insert: O(log n)
    - delete: O(log n)
    - __contains__: O(log n)

    Space complexity: O(n log n) expected.

    See Also
    --------
    SkipList : Concrete implementation.
    """

    @abstractmethod
    def insert(self, key: Any, value: Any = None) -> None:
        """Insert a key-value pair into the skip list.

        Parameters
        ----------
        key : Any
            Comparable key to insert. Must support ``<`` and ``==``.
        value : Any, optional
            Associated value. Defaults to None.

        Notes
        -----
        Time complexity: O(log n) average.
        """
        pass

    @abstractmethod
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

        Notes
        -----
        Time complexity: O(log n) average.
        """
        pass

    @abstractmethod
    def search(self, key: Any) -> Optional[Any]:
        """Return the value associated with the given key.

        Parameters
        ----------
        key : Any
            Key to search for.

        Returns
        -------
        Any or None
            The associated value if found, None otherwise.

        Notes
        -----
        Time complexity: O(log n) average.
        """
        pass

    @abstractmethod
    def __contains__(self, key: Any) -> bool:
        """Test whether the given key exists in the skip list.

        Parameters
        ----------
        key : Any
            Key to test.

        Returns
        -------
        bool
            True if the key is present.

        Notes
        -----
        Time complexity: O(log n) average.
        """
        pass

    @abstractmethod
    def __len__(self) -> int:
        """Return the number of key-value pairs in the skip list.

        Returns
        -------
        int
            Number of elements.
        """
        pass

    @abstractmethod
    def __iter__(self) -> Iterator[Any]:
        """Iterate over keys in sorted ascending order.

        Yields
        ------
        Any
            Keys in sorted order.
        """
        pass


class AbstractHashTable(Collection):
    """Abstract base class for hash table data structures.

    A hash table maps keys to values using a hash function to compute an
    index into an array of buckets or slots. Concrete subclasses implement
    different collision-resolution strategies.

    Notes
    -----
    Two classical collision-resolution strategies are supported:

    - **Separate chaining**: each slot holds a list of (key, value) pairs.
      Worst-case O(n) per operation, O(1) average with a good hash function
      and load factor ≤ 1.
    - **Open addressing** (linear probing): all entries live in the array;
      collisions are resolved by probing subsequent slots.
      Worst-case O(n), O(1) average for load factor < 0.7.

    Both implementations resize automatically when the load factor exceeds
    a configurable threshold.

    See Also
    --------
    HashTableChaining : Separate-chaining implementation.
    HashTableOpenAddressing : Open-addressing (linear probing) implementation.
    """

    @abstractmethod
    def put(self, key: Any, value: Any) -> None:
        """Insert or update a key-value pair.

        Parameters
        ----------
        key : Any
            Hashable key.
        value : Any
            Value to associate with *key*.

        Notes
        -----
        Time complexity: O(1) average, O(n) worst case.
        """
        pass

    @abstractmethod
    def get(self, key: Any) -> Optional[Any]:
        """Return the value associated with *key*, or None if absent.

        Parameters
        ----------
        key : Any
            Key to look up.

        Returns
        -------
        Any or None
            Associated value, or None if the key is not present.

        Notes
        -----
        Time complexity: O(1) average, O(n) worst case.
        """
        pass

    @abstractmethod
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

        Notes
        -----
        Time complexity: O(1) average, O(n) worst case.
        """
        pass

    @abstractmethod
    def __contains__(self, key: Any) -> bool:
        """Test whether *key* exists in the table.

        Parameters
        ----------
        key : Any
            Key to test.

        Returns
        -------
        bool
            True if present.
        """
        pass

    @abstractmethod
    def __len__(self) -> int:
        """Return the number of key-value pairs stored.

        Returns
        -------
        int
            Number of entries.
        """
        pass

    @abstractmethod
    def __iter__(self) -> Iterator[Any]:
        """Iterate over all keys.

        Yields
        ------
        Any
            Keys in unspecified order.
        """
        pass


class AbstractLRUCache(Collection):
    """Abstract base class for a Least Recently Used (LRU) cache.

    An LRU cache stores a bounded number of key-value pairs. When the cache
    is full and a new key must be inserted, the least recently used entry
    (the one not accessed for the longest time) is evicted.

    Every ``get`` and ``put`` operation counts as a "use" and moves the
    accessed entry to the most-recently-used position.

    Notes
    -----
    The canonical implementation combines a doubly-linked list (for O(1)
    eviction) with a hash map (for O(1) lookup), giving O(1) amortised
    time for both ``get`` and ``put``.

    See Also
    --------
    LRUCache : Concrete implementation.
    """

    @abstractmethod
    def get(self, key: Any) -> Optional[Any]:
        """Return the value for *key* and mark it as most recently used.

        Parameters
        ----------
        key : Any
            Key to look up.

        Returns
        -------
        Any or None
            Stored value, or None if the key is not in the cache.

        Notes
        -----
        Time complexity: O(1).
        """
        pass

    @abstractmethod
    def put(self, key: Any, value: Any) -> None:
        """Insert or update a key-value pair.

        If *key* already exists its value is updated and it is marked as
        most recently used. If the cache is at capacity, the least recently
        used entry is evicted before insertion.

        Parameters
        ----------
        key : Any
            Hashable key.
        value : Any
            Value to store.

        Notes
        -----
        Time complexity: O(1).
        """
        pass

    @abstractmethod
    def __contains__(self, key: Any) -> bool:
        """Test whether *key* is currently in the cache.

        Parameters
        ----------
        key : Any
            Key to test.

        Returns
        -------
        bool
            True if present (does **not** update recency).
        """
        pass

    @abstractmethod
    def __len__(self) -> int:
        """Return the number of entries currently in the cache.

        Returns
        -------
        int
            Number of live entries (≤ capacity).
        """
        pass


class AbstractFenwickTree(Collection):
    """Abstract base class for the Fenwick Tree (Binary Indexed Tree).

    A Fenwick Tree supports two operations on a mutable sequence of numbers:

    - **Point update**: add a delta to a single element.
    - **Prefix sum query**: compute the sum of elements from index 1 to i.

    Both operations run in O(log n) time using bitwise manipulation of indices.

    Notes
    -----
    Indexing is **1-based** by convention: valid indices are ``1 .. size``.

    See Also
    --------
    FenwickTree : Concrete implementation.
    """

    @abstractmethod
    def update(self, i: int, delta: float) -> None:
        """Add *delta* to the element at index *i*.

        Parameters
        ----------
        i : int
            1-based index (1 ≤ i ≤ size).
        delta : float
            Value to add (may be negative).

        Raises
        ------
        IndexError
            If *i* is out of range.

        Notes
        -----
        Time complexity: O(log n).
        """
        pass

    @abstractmethod
    def prefix_sum(self, i: int) -> float:
        """Return the sum of elements from index 1 to *i* (inclusive).

        Parameters
        ----------
        i : int
            1-based upper bound (1 ≤ i ≤ size).

        Returns
        -------
        float
            Sum of elements at positions 1, 2, …, i.

        Raises
        ------
        IndexError
            If *i* is out of range.

        Notes
        -----
        Time complexity: O(log n).
        """
        pass

    @abstractmethod
    def range_sum(self, left: int, right: int) -> float:
        """Return the sum of elements from index *left* to *right* (inclusive).

        Parameters
        ----------
        left : int
            1-based lower bound.
        right : int
            1-based upper bound.

        Returns
        -------
        float
            Sum of elements at positions left, left+1, …, right.

        Raises
        ------
        IndexError
            If either index is out of range.
        ValueError
            If left > right.

        Notes
        -----
        Time complexity: O(log n).
        """
        pass

    @abstractmethod
    def __len__(self) -> int:
        """Return the size of the underlying sequence.

        Returns
        -------
        int
            Number of elements (1-based indexing: valid range is 1..n).
        """
        pass
