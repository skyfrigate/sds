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

"""Disjoint Set (Union-Find) data structure implementation.

This module provides an efficient implementation of the Disjoint Set data
structure with path compression and union by rank optimizations, achieving
nearly constant time complexity for all operations.

Classes
-------
DisjointSet
    Union-Find data structure with path compression and union by rank.

Examples
--------
Basic usage for connected components:

>>> ds = DisjointSet()
>>> for i in range(5):
...     ds.make_set(i)
>>> ds.union(0, 1)
True
>>> ds.union(2, 3)
True
>>> ds.union(1, 2)
True
>>> ds.connected(0, 3)
True
>>> ds.connected(0, 4)
False
>>> ds.count_sets()
2

Use with graphs for cycle detection:

>>> ds = DisjointSet()
>>> edges = [(0, 1), (1, 2), (0, 2)]  # Forms a cycle
>>> for node in [0, 1, 2]:
...     ds.make_set(node)
>>> has_cycle = False
>>> for u, v in edges:
...     if ds.connected(u, v):
...         has_cycle = True
...         break
...     ds.union(u, v)
>>> has_cycle
True

Notes
-----
Time Complexity (amortized with path compression and union by rank):
- make_set: O(1)
- find: O(α(n)) where α is inverse Ackermann function
- union: O(α(n))
- connected: O(α(n))
- count_sets: O(1)
- size: O(α(n))
- get_sets: O(n)

Space Complexity: O(n) where n is number of elements

The inverse Ackermann function α(n) grows so slowly that for all
practical values of n, α(n) ≤ 4. Thus operations are effectively O(1).

References
----------
.. [1] Tarjan, R. E. (1975). "Efficiency of a Good But Not Linear Set
       Union Algorithm". Journal of the ACM.
.. [2] Cormen, T. H., et al. (2009). "Introduction to Algorithms", 3rd ed.
       Chapter 21: Data Structures for Disjoint Sets.

See Also
--------
sds.algorithms.graph.spanning_tree.kruskal : Uses DisjointSet for MST.
sds.algorithms.graph.connectivity : Uses DisjointSet for components.
"""

from typing import Any, Dict, Iterator, List, Set

from .interfaces import AbstractDisjointSet

__all__ = ["DisjointSet"]


class DisjointSet(AbstractDisjointSet):
    """Disjoint Set (Union-Find) with path compression and union by rank.

    This implementation maintains a forest of trees where each tree represents
    a disjoint set. Path compression flattens trees during find operations,
    and union by rank keeps trees balanced.

    Attributes
    ----------
    num_sets : int
        Current number of disjoint sets (read-only property).

    Examples
    --------
    Create and merge sets:

    >>> ds = DisjointSet()
    >>> for i in range(4):
    ...     ds.make_set(i)
    >>> ds.union(0, 1)
    True
    >>> ds.union(2, 3)
    True
    >>> ds.count_sets()
    2
    >>> ds.size(0)
    2

    Check connectivity:

    >>> ds.connected(0, 1)
    True
    >>> ds.connected(0, 2)
    False
    >>> ds.union(1, 2)
    True
    >>> ds.connected(0, 3)
    True

    Get all sets:

    >>> ds = DisjointSet()
    >>> for i in range(6):
    ...     ds.make_set(i)
    >>> ds.union(0, 1)
    True
    >>> ds.union(2, 3)
    True
    >>> ds.union(4, 5)
    True
    >>> sets = ds.get_sets()
    >>> len(sets)
    3

    Notes
    -----
    - Elements must be hashable
    - Once created, elements cannot be removed
    - Each element can only be in one set at a time
    - Union operations are irreversible

    Implementation Details:
    - parent[x] = parent of x in tree (x if root)
    - rank[x] = upper bound on height of subtree rooted at x
    - set_size[x] = size of set for root nodes

    See Also
    --------
    AbstractDisjointSet : Abstract interface for disjoint sets.
    """

    def __init__(self) -> None:
        """Initialize an empty disjoint set structure.

        Examples
        --------
        >>> ds = DisjointSet()
        >>> ds.count_sets()
        0
        """
        self._parent: Dict[Any, Any] = {}
        self._rank: Dict[Any, int] = {}
        self._set_size: Dict[Any, int] = {}
        self._num_sets = 0

    @property
    def num_sets(self) -> int:
        """Get the number of disjoint sets.

        Returns
        -------
        int
            Current number of disjoint sets.

        Examples
        --------
        >>> ds = DisjointSet()
        >>> ds.num_sets
        0
        >>> ds.make_set(1)
        >>> ds.num_sets
        1
        """
        return self._num_sets

    def is_empty(self) -> bool:
        """Return True if no elements have been added.

        Returns
        -------
        bool
            True if len(self) == 0.

        Notes
        -----
        Time complexity: O(1).
        """
        return len(self._parent) == 0

    def clear(self) -> None:
        """Remove all elements and sets.

        Notes
        -----
        Time complexity: O(1).
        """
        self._parent.clear()
        self._rank.clear()
        self._set_size.clear()
        self._num_sets = 0

    def __iter__(self) -> "Iterator[Any]":
        """Iterate over all elements in the structure.

        Yields
        ------
        Any
            Elements in unspecified order.

        Notes
        -----
        Time complexity: O(n).
        """
        return iter(self._parent)

    def make_set(self, element: Any) -> None:
        """Create a new set containing only the given element.

        Parameters
        ----------
        element : Any
            Element to create a set for (must be hashable).

        Raises
        ------
        TypeError
            If element is not hashable.
        ValueError
            If element already exists in a set.

        Examples
        --------
        >>> ds = DisjointSet()
        >>> ds.make_set(1)
        >>> ds.make_set(2)
        >>> ds.count_sets()
        2

        Duplicate elements raise error:

        >>> ds.make_set(1)
        Traceback (most recent call last):
            ...
        ValueError: Element 1 already exists in a set

        Notes
        -----
        Time complexity: O(1)
        Space complexity: O(1)
        """
        # Check if element is hashable by attempting to use it as dict key
        try:
            _ = hash(element)
        except TypeError:
            raise TypeError(f"Element must be hashable, got {type(element).__name__}")

        if element in self._parent:
            raise ValueError(f"Element {element} already exists in a set")

        self._parent[element] = element
        self._rank[element] = 0
        self._set_size[element] = 1
        self._num_sets += 1

    def find(self, element: Any) -> Any:
        """Find the representative of the set containing element.

        Uses path compression: makes all nodes on path point directly to root.

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

        Examples
        --------
        >>> ds = DisjointSet()
        >>> ds.make_set(1)
        >>> ds.make_set(2)
        >>> ds.union(1, 2)
        True
        >>> root = ds.find(1)
        >>> ds.find(2) == root
        True

        Notes
        -----
        Time complexity: O(α(n)) amortized with path compression.
        Path compression flattens the tree structure on each find operation.
        """
        if element not in self._parent:
            raise ValueError(f"Element {element} is not in any set")

        # Path compression: make all nodes point to root
        if self._parent[element] != element:
            self._parent[element] = self.find(self._parent[element])

        return self._parent[element]

    def union(self, x: Any, y: Any) -> bool:
        """Unite the sets containing x and y.

        Uses union by rank: attach smaller rank tree under root of higher rank.

        Parameters
        ----------
        x : Any
            Element in first set.
        y : Any
            Element in second set.

        Returns
        -------
        bool
            True if sets were merged (were different), False if already same set.

        Raises
        ------
        ValueError
            If x or y is not in any set.

        Examples
        --------
        >>> ds = DisjointSet()
        >>> for i in range(4):
        ...     ds.make_set(i)
        >>> ds.union(0, 1)
        True
        >>> ds.union(0, 1)  # Already in same set
        False
        >>> ds.union(2, 3)
        True
        >>> ds.count_sets()
        2

        Notes
        -----
        Time complexity: O(α(n)) amortized.
        Union by rank keeps trees balanced for optimal performance.
        """
        root_x = self.find(x)
        root_y = self.find(y)

        # Already in same set
        if root_x == root_y:
            return False

        # Union by rank: attach smaller tree under root of larger tree
        if self._rank[root_x] < self._rank[root_y]:
            self._parent[root_x] = root_y
            self._set_size[root_y] += self._set_size[root_x]
            del self._set_size[root_x]
        elif self._rank[root_x] > self._rank[root_y]:
            self._parent[root_y] = root_x
            self._set_size[root_x] += self._set_size[root_y]
            del self._set_size[root_y]
        else:
            # Equal rank: make one root and increment its rank
            self._parent[root_y] = root_x
            self._rank[root_x] += 1
            self._set_size[root_x] += self._set_size[root_y]
            del self._set_size[root_y]

        self._num_sets -= 1
        return True

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

        Examples
        --------
        >>> ds = DisjointSet()
        >>> ds.make_set(1)
        >>> ds.make_set(2)
        >>> ds.make_set(3)
        >>> ds.connected(1, 2)
        False
        >>> ds.union(1, 2)
        True
        >>> ds.connected(1, 2)
        True
        >>> ds.connected(1, 3)
        False

        Notes
        -----
        Time complexity: O(α(n)) amortized.
        """
        return bool(self.find(x) == self.find(y))

    def get_sets(self) -> List[Set[Any]]:
        """Get all disjoint sets.

        Returns
        -------
        List[Set[Any]]
            List of all disjoint sets.

        Examples
        --------
        >>> ds = DisjointSet()
        >>> for i in range(6):
        ...     ds.make_set(i)
        >>> ds.union(0, 1)
        True
        >>> ds.union(2, 3)
        True
        >>> ds.union(4, 5)
        True
        >>> sets = ds.get_sets()
        >>> len(sets)
        3
        >>> any({0, 1} == s for s in sets)
        True

        Notes
        -----
        Time complexity: O(n) where n is number of elements.
        Creates new set objects, so modifications don't affect structure.
        """
        sets_dict: Dict[Any, Set[Any]] = {}

        for element in self._parent:
            root = self.find(element)
            if root not in sets_dict:
                sets_dict[root] = set()
            sets_dict[root].add(element)

        return list(sets_dict.values())

    def count_sets(self) -> int:
        """Get the number of disjoint sets.

        Returns
        -------
        int
            Number of disjoint sets.

        Examples
        --------
        >>> ds = DisjointSet()
        >>> ds.count_sets()
        0
        >>> for i in range(5):
        ...     ds.make_set(i)
        >>> ds.count_sets()
        5
        >>> ds.union(0, 1)
        True
        >>> ds.count_sets()
        4

        Notes
        -----
        Time complexity: O(1)
        """
        return self._num_sets

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

        Examples
        --------
        >>> ds = DisjointSet()
        >>> for i in range(5):
        ...     ds.make_set(i)
        >>> ds.size(0)
        1
        >>> ds.union(0, 1)
        True
        >>> ds.union(0, 2)
        True
        >>> ds.size(0)
        3
        >>> ds.size(1)
        3

        Notes
        -----
        Time complexity: O(α(n)) amortized.
        """
        root = self.find(element)
        return self._set_size[root]

    def __len__(self) -> int:
        """Return the total number of elements across all sets.

        Returns
        -------
        int
            Total number of elements.

        Examples
        --------
        >>> ds = DisjointSet()
        >>> len(ds)
        0
        >>> for i in range(5):
        ...     ds.make_set(i)
        >>> len(ds)
        5
        """
        return len(self._parent)

    def __contains__(self, element: Any) -> bool:
        """Check if element exists in any set.

        Parameters
        ----------
        element : Any
            Element to check.

        Returns
        -------
        bool
            True if element is in any set.

        Examples
        --------
        >>> ds = DisjointSet()
        >>> 1 in ds
        False
        >>> ds.make_set(1)
        >>> 1 in ds
        True
        """
        return element in self._parent

    def __repr__(self) -> str:
        """Return detailed string representation.

        Returns
        -------
        str
            String representation.

        Examples
        --------
        >>> ds = DisjointSet()
        >>> for i in range(3):
        ...     ds.make_set(i)
        >>> ds.union(0, 1)
        True
        >>> repr(ds)
        'DisjointSet(elements=3, sets=2)'
        """
        return f"DisjointSet(elements={len(self)}, sets={self._num_sets})"

    def __str__(self) -> str:
        """Return simple string representation.

        Returns
        -------
        str
            String representation.

        Examples
        --------
        >>> ds = DisjointSet()
        >>> for i in range(3):
        ...     ds.make_set(i)
        >>> str(ds)
        'DisjointSet: 3 elements in 3 sets'
        """
        return f"DisjointSet: {len(self)} elements in {self._num_sets} sets"
