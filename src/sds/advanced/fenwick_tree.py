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

"""Fenwick Tree (Binary Indexed Tree) data structure.

A Fenwick Tree supports O(log n) point updates and O(log n) prefix sum
queries on a mutable sequence of numbers. It is space-efficient, requiring
only O(n) extra storage, and relies entirely on bitwise index arithmetic.

Classes
-------
FenwickTree
    Binary Indexed Tree for mutable prefix-sum queries.

Examples
--------
Build from a list:

>>> ft = FenwickTree.from_list([1, 2, 3, 4, 5])
>>> ft.prefix_sum(3)   # 1 + 2 + 3
6.0
>>> ft.range_sum(2, 4) # 2 + 3 + 4
9.0
>>> ft.update(3, 10)   # add 10 to index 3
>>> ft.prefix_sum(3)
16.0

Build empty and populate:

>>> ft = FenwickTree(size=5)
>>> for i, v in enumerate([1, 2, 3, 4, 5], start=1):
...     ft.update(i, v)
>>> ft.prefix_sum(5)
15.0

Notes
-----
Indexing is **1-based**: valid indices are ``1 .. size``.

Time Complexity:
- update: O(log n)
- prefix_sum: O(log n)
- range_sum: O(log n)
- point_query: O(log n)
- from_list (construction): O(n log n)

Space Complexity: O(n) — one internal array of size n+1.

The core idea: each cell ``_tree[i]`` stores the sum of elements in the
range ``[i - lowbit(i) + 1, i]`` where ``lowbit(i) = i & (-i)``.

- **Update** propagates upward: ``i += lowbit(i)``.
- **Prefix sum** accumulates downward: ``i -= lowbit(i)``.

References
----------
.. [1] Fenwick, P. M. (1994). "A new data structure for cumulative frequency
       tables". Software: Practice and Experience, 24(3), 327-336.
       DOI: 10.1002/spe.4380240306
.. [2] OpenDSA — Bit Manipulation chapter (Fenwick Trees).
       https://opendsa-server.cs.vt.edu/ODSA/Books/Everything/html/BinaryIndexedTree.html
.. [3] Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009).
       *Introduction to Algorithms* (3rd ed.), Problem 14-1.
       MIT Press.
"""

from typing import Iterator, Union

from ..core.exceptions import IndexStructureError
from .interfaces import AbstractFenwickTree

__all__ = ["FenwickTree"]

Number = Union[int, float]


class FenwickTree(AbstractFenwickTree):
    """Binary Indexed Tree for O(log n) point updates and prefix sums.

    Stores a sequence of *n* numeric values (initially zero) and supports
    efficient cumulative sum queries and element updates.

    Parameters
    ----------
    size : int
        Number of elements. Must be ≥ 1. Valid indices are ``1 .. size``.

    Attributes
    ----------
    size : int
        Length of the underlying sequence (read-only).

    Raises
    ------
    ValueError
        If ``size < 1``.

    Examples
    --------
    Manual construction:

    >>> ft = FenwickTree(size=5)
    >>> ft.update(1, 3)
    >>> ft.update(2, 2)
    >>> ft.update(3, 7)
    >>> ft.update(4, 1)
    >>> ft.update(5, 5)
    >>> ft.prefix_sum(4)
    13.0
    >>> ft.range_sum(2, 4)
    10.0
    >>> ft.point_query(3)
    7.0

    From a list:

    >>> ft = FenwickTree.from_list([3, 2, 7, 1, 5])
    >>> ft.prefix_sum(5)
    18.0

    Notes
    -----
    - All values are stored as ``float`` internally for consistency.
    - Negative deltas are supported by ``update()``.
    - ``point_query(i)`` returns the current value at position *i* using
      ``prefix_sum(i) - prefix_sum(i-1)``.
    """

    def __init__(self, size: int) -> None:
        """Initialise a Fenwick Tree of *size* elements, all zero.

        Parameters
        ----------
        size : int
            Number of elements (1-based). Must be ≥ 1.

        Raises
        ------
        ValueError
            If ``size < 1``.

        Examples
        --------
        >>> ft = FenwickTree(size=10)
        >>> ft.prefix_sum(10)
        0.0

        Notes
        -----
        Time complexity: O(n) — zeroes the internal array.
        """
        if size < 1:
            raise ValueError(f"size must be at least 1, got {size}")
        self._size = size
        # 1-indexed; _tree[0] is unused
        self._tree: list[float] = [0.0] * (size + 1)

    # ------------------------------------------------------------------
    # Class method constructors
    # ------------------------------------------------------------------

    @classmethod
    def from_list(cls, values: list[Number]) -> "FenwickTree":
        """Build a FenwickTree from an existing list of values.

        Parameters
        ----------
        values : list[int | float]
            Initial values. ``values[0]`` maps to index 1, etc.
            Must be non-empty.

        Returns
        -------
        FenwickTree
            A tree initialised with the given values.

        Raises
        ------
        ValueError
            If *values* is empty.

        Examples
        --------
        >>> ft = FenwickTree.from_list([1, 2, 3, 4, 5])
        >>> ft.prefix_sum(5)
        15.0
        >>> ft.range_sum(2, 4)
        9.0

        Notes
        -----
        Time complexity: O(n log n).
        """
        if not values:
            raise ValueError("values must not be empty")
        tree = cls(size=len(values))
        for i, v in enumerate(values, start=1):
            tree.update(i, v)
        return tree

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def size(self) -> int:
        """Number of elements in the tree (1-based range 1..size).

        Returns
        -------
        int
            The *size* passed at construction.
        """
        return self._size

    # ------------------------------------------------------------------
    # Internal helper
    # ------------------------------------------------------------------

    @staticmethod
    def _lowbit(i: int) -> int:
        """Return the lowest set bit of *i*: ``i & (-i)``."""
        return i & (-i)

    # ------------------------------------------------------------------
    # AbstractFenwickTree interface
    # ------------------------------------------------------------------

    def update(self, i: int, delta: Number) -> None:
        """Add *delta* to the element at 1-based index *i*.

        Propagates the change upward through all ancestor cells using
        the relation ``i += lowbit(i)``.

        Parameters
        ----------
        i : int
            1-based index (1 ≤ i ≤ size).
        delta : int or float
            Value to add. May be negative to decrease.

        Raises
        ------
        IndexError
            If *i* < 1 or *i* > size.

        Examples
        --------
        >>> ft = FenwickTree(size=5)
        >>> ft.update(3, 7)
        >>> ft.prefix_sum(3)
        7.0
        >>> ft.update(3, -2)
        >>> ft.prefix_sum(3)
        5.0

        Notes
        -----
        Time complexity: O(log n).
        """
        if i < 1 or i > self._size:
            raise IndexStructureError(
                f"index {i} out of range for FenwickTree of size {self._size}"
            )
        while i <= self._size:
            self._tree[i] += float(delta)
            i += self._lowbit(i)

    def prefix_sum(self, i: int) -> float:
        """Return the cumulative sum of elements at positions 1..i.

        Accumulates partial sums downward using ``i -= lowbit(i)``.

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
            If *i* < 1 or *i* > size.

        Examples
        --------
        >>> ft = FenwickTree.from_list([1, 2, 3, 4, 5])
        >>> ft.prefix_sum(1)
        1.0
        >>> ft.prefix_sum(3)
        6.0
        >>> ft.prefix_sum(5)
        15.0

        Notes
        -----
        Time complexity: O(log n).
        """
        if i < 1 or i > self._size:
            raise IndexStructureError(
                f"index {i} out of range for FenwickTree of size {self._size}"
            )
        total = 0.0
        while i > 0:
            total += self._tree[i]
            i -= self._lowbit(i)
        return total

    def range_sum(self, left: int, right: int) -> float:
        """Return the sum of elements at positions left..right (inclusive).

        Computed as ``prefix_sum(right) - prefix_sum(left - 1)``.

        Parameters
        ----------
        left : int
            1-based lower bound (1 ≤ left ≤ size).
        right : int
            1-based upper bound (left ≤ right ≤ size).

        Returns
        -------
        float
            Sum of elements at positions left, left+1, …, right.

        Raises
        ------
        IndexError
            If *left* or *right* is out of ``[1, size]``.
        ValueError
            If *left* > *right*.

        Examples
        --------
        >>> ft = FenwickTree.from_list([1, 2, 3, 4, 5])
        >>> ft.range_sum(2, 4)   # 2 + 3 + 4
        9.0
        >>> ft.range_sum(1, 5)   # full sum
        15.0
        >>> ft.range_sum(3, 3)   # single element
        3.0

        Notes
        -----
        Time complexity: O(log n).
        """
        if left < 1 or left > self._size:
            raise IndexStructureError(
                f"left index {left} out of range for FenwickTree of size {self._size}"
            )
        if right < 1 or right > self._size:
            raise IndexStructureError(
                f"right index {right} out of range for FenwickTree of size {self._size}"
            )
        if left > right:
            raise ValueError(f"left ({left}) must be ≤ right ({right})")
        if left == 1:
            return self.prefix_sum(right)
        return self.prefix_sum(right) - self.prefix_sum(left - 1)

    def is_empty(self) -> bool:
        """Return True if all elements are zero.

        Returns
        -------
        bool
            True if total() == 0.

        Notes
        -----
        Time complexity: O(log n).
        A FenwickTree is considered empty when all stored values are zero
        (equivalent to the initial state after construction or clear()).
        """
        return self.total() == 0.0

    def clear(self) -> None:
        """Reset all elements to zero.

        Notes
        -----
        Time complexity: O(n).
        """
        self._tree = [0.0] * (self._size + 1)

    def __iter__(self) -> "Iterator[float]":
        """Iterate over element values at positions 1..size.

        Yields
        ------
        float
            Current value at each position in order.

        Notes
        -----
        Time complexity: O(n log n).
        """
        for i in range(1, self._size + 1):
            yield self.point_query(i)

    def __contains__(self, value: object) -> bool:
        """Return True if *value* equals any element in the tree.

        Parameters
        ----------
        value : object
            Value to search for.

        Returns
        -------
        bool
            True if any position holds *value*.

        Notes
        -----
        Time complexity: O(n log n) — scans all positions.
        For index-based lookup, use point_query() instead.
        """
        try:
            v = float(value)  # type: ignore[arg-type]
        except (TypeError, ValueError):
            return False
        return any(self.point_query(i) == v for i in range(1, self._size + 1))

    def __len__(self) -> int:
        """Return the size of the underlying sequence.

        Returns
        -------
        int
            Equivalent to ``self.size``.

        Examples
        --------
        >>> ft = FenwickTree(size=10)
        >>> len(ft)
        10
        """
        return self._size

    # ------------------------------------------------------------------
    # Additional helpers
    # ------------------------------------------------------------------

    def point_query(self, i: int) -> float:
        """Return the current value at 1-based index *i*.

        Computed as ``prefix_sum(i) - prefix_sum(i-1)``.

        Parameters
        ----------
        i : int
            1-based index (1 ≤ i ≤ size).

        Returns
        -------
        float
            Current value stored at position *i*.

        Raises
        ------
        IndexError
            If *i* is out of range.

        Examples
        --------
        >>> ft = FenwickTree.from_list([10, 20, 30])
        >>> ft.point_query(2)
        20.0
        >>> ft.update(2, 5)
        >>> ft.point_query(2)
        25.0

        Notes
        -----
        Time complexity: O(log n).
        """
        if i < 1 or i > self._size:
            raise IndexStructureError(
                f"index {i} out of range for FenwickTree of size {self._size}"
            )
        if i == 1:
            return self.prefix_sum(1)
        return self.prefix_sum(i) - self.prefix_sum(i - 1)

    def total(self) -> float:
        """Return the sum of all elements.

        Equivalent to ``prefix_sum(size)``.

        Returns
        -------
        float
            Sum of all elements.

        Examples
        --------
        >>> ft = FenwickTree.from_list([1, 2, 3, 4, 5])
        >>> ft.total()
        15.0

        Notes
        -----
        Time complexity: O(log n).
        """
        return self.prefix_sum(self._size)

    def to_list(self) -> list[float]:
        """Return the current values as a plain list (1-indexed → 0-indexed).

        Returns
        -------
        list[float]
            Values at positions 1..size, with ``result[0]`` = value at index 1.

        Examples
        --------
        >>> ft = FenwickTree.from_list([3, 1, 4, 1, 5])
        >>> ft.to_list()
        [3.0, 1.0, 4.0, 1.0, 5.0]

        Notes
        -----
        Time complexity: O(n log n).
        """
        return [self.point_query(i) for i in range(1, self._size + 1)]

    # ------------------------------------------------------------------
    # Dunder methods
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        """Return a detailed string representation.

        Returns
        -------
        str
            ``FenwickTree(size=n, total=x)``.

        Examples
        --------
        >>> ft = FenwickTree(size=5)
        >>> repr(ft)
        'FenwickTree(size=5, total=0.0)'
        """
        return f"FenwickTree(size={self._size}, total={self.total()})"

    def __str__(self) -> str:
        """Return a concise human-readable representation.

        Returns
        -------
        str
            Summary including size and total.

        Examples
        --------
        >>> ft = FenwickTree.from_list([1, 2, 3])
        >>> str(ft)
        'FenwickTree: 3 elements, total=6.0'
        """
        return f"FenwickTree: {self._size} elements, total={self.total()}"
