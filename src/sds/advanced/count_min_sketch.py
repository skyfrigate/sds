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

"""Count-Min Sketch — frequency estimation over data streams.

A Count-Min Sketch estimates the frequency of elements in a data stream
using a compact matrix of counters. It never underestimates frequencies,
but may overestimate by a controllable additive error.

Classes
-------
CountMinSketch
    Probabilistic frequency estimator backed by a d × w counter matrix.

Examples
--------
Basic usage:

>>> cms = CountMinSketch(epsilon=0.01, delta=0.01)
>>> cms.add("apple")
>>> cms.add("apple")
>>> cms.add("banana")
>>> cms.frequency("apple")
2
>>> cms.frequency("cherry")
0

Custom matrix dimensions:

>>> cms = CountMinSketch.from_dimensions(width=100, depth=5)
>>> for word in ["a", "b", "a", "c", "a"]:
...     cms.add(word)
>>> cms.frequency("a")
3

Notes
-----
Time Complexity:
- add: O(d)
- frequency: O(d)
- merge: O(d × w)
- clear: O(d × w)

Space Complexity: O(d × w) counters, where:
  - w = ⌈e / ε⌉  (width — controls additive error)
  - d = ⌈ln(1/δ)⌉  (depth — controls failure probability)

The additive error guarantee is:

    P(frequency(x) ≤ true_count(x) + ε × N) ≥ 1 − δ

where N is the total number of items added.

No false negatives: ``frequency(x)`` is always ≥ the true count.

References
----------
.. [1] Cormode, G., & Muthukrishnan, S. (2005). "An improved data stream
       summary: The count-min sketch and its applications". Journal of
       Algorithms, 55(1), 58-75.
       DOI: 10.1016/j.jalgor.2003.12.001
.. [2] Cormode, G. (2009). "Count-Min Sketch". Encyclopedia of Database
       Systems. Springer.
       https://dimacs.rutgers.edu/~graham/pubs/papers/cmencyc.pdf
"""

import hashlib
import math
from typing import Any, Iterator

from ..core.interfaces import Collection

__all__ = ["CountMinSketch"]


class CountMinSketch(Collection):
    """Probabilistic frequency estimator over data streams.

    Maintains a ``depth × width`` matrix of integer counters. Each item
    is hashed by *depth* independent hash functions; ``add(item)`` increments
    one counter per row, and ``frequency(item)`` returns the minimum across
    all *depth* counters — an upper bound on the true count.

    Parameters
    ----------
    epsilon : float
        Maximum additive error as a fraction of the total stream size.
        Must be in (0.0, 1.0). Smaller values require a wider matrix.
    delta : float
        Failure probability — the probability that the error bound is
        exceeded. Must be in (0.0, 1.0). Smaller values require more rows.

    Attributes
    ----------
    width : int
        Number of columns (read-only). Derived from *epsilon*.
    depth : int
        Number of rows / hash functions (read-only). Derived from *delta*.
    total : int
        Total number of items added (read-only). Not deduplicated.

    Raises
    ------
    ValueError
        If *epsilon* or *delta* is not in (0.0, 1.0).

    Examples
    --------
    >>> cms = CountMinSketch(epsilon=0.01, delta=0.01)
    >>> cms.add("hello")
    >>> cms.add("hello")
    >>> cms.add("world")
    >>> cms.frequency("hello")
    2
    >>> cms.frequency("world")
    1
    >>> cms.frequency("missing")
    0
    >>> len(cms)
    3

    Notes
    -----
    - ``frequency(x)`` ≥ true count of *x* (no underestimates).
    - ``frequency(x)`` ≤ true count of *x* + ε × N with probability ≥ 1 − δ.
    - Elements must be convertible to a string for hashing.
    - Counts are non-negative integers; ``add`` with ``count > 1``
      is equivalent to calling ``add`` *count* times.
    """

    def __init__(self, epsilon: float, delta: float) -> None:
        """Initialise a Count-Min Sketch from error parameters.

        Parameters
        ----------
        epsilon : float
            Additive error fraction. Must be in (0.0, 1.0).
        delta : float
            Failure probability. Must be in (0.0, 1.0).

        Raises
        ------
        ValueError
            If *epsilon* or *delta* is not in (0.0, 1.0).

        Examples
        --------
        >>> cms = CountMinSketch(epsilon=0.01, delta=0.05)
        >>> cms.width, cms.depth
        (272, 3)

        Notes
        -----
        Derived dimensions:

        .. math::

            w = \\lceil e / \\varepsilon \\rceil, \\quad
            d = \\lceil \\ln(1/\\delta) \\rceil

        Time complexity: O(d × w).
        """
        if not (0.0 < epsilon < 1.0):
            raise ValueError(f"epsilon must be in (0.0, 1.0), got {epsilon}")
        if not (0.0 < delta < 1.0):
            raise ValueError(f"delta must be in (0.0, 1.0), got {delta}")
        self._epsilon = epsilon
        self._delta = delta
        self._width = math.ceil(math.e / epsilon)
        self._depth = math.ceil(math.log(1.0 / delta))
        self._total = 0
        self._table: list[list[int]] = [[0] * self._width for _ in range(self._depth)]

    # ------------------------------------------------------------------
    # Class-method constructor
    # ------------------------------------------------------------------

    @classmethod
    def from_dimensions(cls, width: int, depth: int) -> "CountMinSketch":
        """Build a Count-Min Sketch with explicit matrix dimensions.

        Use this when you prefer to specify the matrix size directly
        rather than derive it from error parameters.

        Parameters
        ----------
        width : int
            Number of columns. Must be ≥ 1.
        depth : int
            Number of rows / hash functions. Must be ≥ 1.

        Returns
        -------
        CountMinSketch
            A sketch with the given dimensions.

        Raises
        ------
        ValueError
            If *width* or *depth* is less than 1.

        Examples
        --------
        >>> cms = CountMinSketch.from_dimensions(width=200, depth=5)
        >>> cms.width, cms.depth
        (200, 5)

        Notes
        -----
        Time complexity: O(d × w).
        """
        if width < 1:
            raise ValueError(f"width must be at least 1, got {width}")
        if depth < 1:
            raise ValueError(f"depth must be at least 1, got {depth}")
        # Use a tiny epsilon/delta that yield at least width × depth
        # via the standard formula — then override.
        instance = object.__new__(cls)
        instance._epsilon = math.e / width
        instance._delta = math.exp(-depth)
        instance._width = width
        instance._depth = depth
        instance._total = 0
        instance._table = [[0] * width for _ in range(depth)]
        return instance

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def width(self) -> int:
        """Number of columns in the counter matrix.

        Returns
        -------
        int
            Derived from *epsilon* at construction.
        """
        return self._width

    @property
    def depth(self) -> int:
        """Number of rows (hash functions) in the counter matrix.

        Returns
        -------
        int
            Derived from *delta* at construction.
        """
        return self._depth

    @property
    def total(self) -> int:
        """Total number of items added (stream size N).

        Returns
        -------
        int
            Monotonically increasing; not deduplicated.
        """
        return self._total

    # ------------------------------------------------------------------
    # Internal hashing
    # ------------------------------------------------------------------

    def _hash(self, item: Any, row: int) -> int:
        """Compute the column index for *item* in *row*.

        Uses double hashing: two independent digests combined as
        ``(h1 + row * h2) mod width`` to produce row-specific positions
        without computing *depth* fully independent hash functions.

        Parameters
        ----------
        item : Any
            Item to hash. Converted to bytes via UTF-8 string encoding.
        row : int
            Row index (0 .. depth-1).

        Returns
        -------
        int
            Column index in ``[0, width)``.
        """
        data = str(item).encode("utf-8")
        h1 = int(hashlib.sha256(data).hexdigest(), 16)
        h2 = int(hashlib.md5(data, usedforsecurity=False).hexdigest(), 16)
        return (h1 + row * h2) % self._width

    # ------------------------------------------------------------------
    # Core operations
    # ------------------------------------------------------------------

    def add(self, item: Any, count: int = 1) -> None:
        """Record one or more occurrences of *item* in the stream.

        Increments the counter at position ``_hash(item, row)`` in each
        row by *count*.

        Parameters
        ----------
        item : Any
            Item to record. Must be convertible to a string.
        count : int
            Number of occurrences to add. Must be ≥ 1.

        Raises
        ------
        ValueError
            If *count* < 1.

        Examples
        --------
        >>> cms = CountMinSketch(epsilon=0.01, delta=0.01)
        >>> cms.add("apple", count=5)
        >>> cms.frequency("apple")
        5

        Notes
        -----
        Time complexity: O(d).
        """
        if count < 1:
            raise ValueError(f"count must be at least 1, got {count}")
        for row in range(self._depth):
            self._table[row][self._hash(item, row)] += count
        self._total += count

    def frequency(self, item: Any) -> int:
        """Return the estimated frequency of *item*.

        Takes the minimum counter value across all *depth* rows — an upper
        bound on the true count with the probabilistic guarantee described
        in the class docstring.

        Parameters
        ----------
        item : Any
            Item to query. Must be convertible to a string.

        Returns
        -------
        int
            Estimated frequency (≥ true count, ≤ true + ε × N w.h.p.).
            Returns 0 for items never added.

        Examples
        --------
        >>> cms = CountMinSketch(epsilon=0.01, delta=0.01)
        >>> cms.add("a")
        >>> cms.add("a")
        >>> cms.frequency("a")
        2
        >>> cms.frequency("b")
        0

        Notes
        -----
        Time complexity: O(d).
        """
        return min(
            self._table[row][self._hash(item, row)] for row in range(self._depth)
        )

    def merge(self, other: "CountMinSketch") -> "CountMinSketch":
        """Return a new sketch representing the union of two streams.

        The result estimates frequencies as if both sketches had seen
        the combined stream. Both sketches must have identical dimensions.

        Parameters
        ----------
        other : CountMinSketch
            Another sketch with the same *width* and *depth*.

        Returns
        -------
        CountMinSketch
            A new sketch whose counters are the element-wise sums.

        Raises
        ------
        ValueError
            If the two sketches have different *width* or *depth*.

        Examples
        --------
        >>> cms1 = CountMinSketch.from_dimensions(width=100, depth=4)
        >>> cms2 = CountMinSketch.from_dimensions(width=100, depth=4)
        >>> cms1.add("a", 3)
        >>> cms2.add("a", 2)
        >>> merged = cms1.merge(cms2)
        >>> merged.frequency("a")
        5

        Notes
        -----
        Time complexity: O(d × w).
        """
        if self._width != other._width or self._depth != other._depth:
            raise ValueError(
                "Cannot merge sketches with different dimensions. "
                f"Got ({self._width}×{self._depth}) and "
                f"({other._width}×{other._depth})."
            )
        result = CountMinSketch.from_dimensions(self._width, self._depth)
        for row in range(self._depth):
            for col in range(self._width):
                result._table[row][col] = self._table[row][col] + other._table[row][col]
        result._total = self._total + other._total
        return result

    # ------------------------------------------------------------------
    # Collection interface
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        """Return the total number of items added (stream size).

        Returns
        -------
        int
            Equivalent to :attr:`total`.

        Examples
        --------
        >>> cms = CountMinSketch(epsilon=0.01, delta=0.01)
        >>> cms.add("x")
        >>> cms.add("x")
        >>> len(cms)
        2
        """
        return self._total

    def is_empty(self) -> bool:
        """Return True if no items have been added.

        Returns
        -------
        bool
            True if total == 0.

        Examples
        --------
        >>> cms = CountMinSketch(epsilon=0.01, delta=0.01)
        >>> cms.is_empty()
        True
        >>> cms.add("x")
        >>> cms.is_empty()
        False
        """
        return self._total == 0

    def clear(self) -> None:
        """Reset all counters and the total to zero.

        Examples
        --------
        >>> cms = CountMinSketch(epsilon=0.01, delta=0.01)
        >>> cms.add("x")
        >>> cms.clear()
        >>> len(cms)
        0
        >>> cms.is_empty()
        True

        Notes
        -----
        Time complexity: O(d × w).
        """
        self._table = [[0] * self._width for _ in range(self._depth)]
        self._total = 0

    def __iter__(self) -> Iterator[Any]:
        """Not supported — CountMinSketch does not store individual items.

        Raises
        ------
        TypeError
            Always, because individual items cannot be recovered from a
            Count-Min Sketch.
        """
        raise TypeError(
            "CountMinSketch does not support iteration: "
            "individual items cannot be recovered from the counter matrix."
        )

    def __contains__(self, item: Any) -> bool:
        """Return True if *item* has a non-zero estimated frequency.

        Parameters
        ----------
        item : Any
            Item to check.

        Returns
        -------
        bool
            True if ``frequency(item) > 0``.

        Examples
        --------
        >>> cms = CountMinSketch(epsilon=0.01, delta=0.01)
        >>> cms.add("hello")
        >>> "hello" in cms
        True
        >>> "world" in cms
        False

        Notes
        -----
        Time complexity: O(d).
        False positives are possible (consistent with the sketch guarantee).
        False negatives are not possible.
        """
        return self.frequency(item) > 0

    # ------------------------------------------------------------------
    # Dunder methods
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        """Return a detailed string representation.

        Returns
        -------
        str
            ``CountMinSketch(width=w, depth=d, total=n)``.

        Examples
        --------
        >>> cms = CountMinSketch.from_dimensions(width=100, depth=5)
        >>> repr(cms)
        'CountMinSketch(width=100, depth=5, total=0)'
        """
        return (
            f"CountMinSketch(width={self._width}, "
            f"depth={self._depth}, "
            f"total={self._total})"
        )

    def __str__(self) -> str:
        """Return a concise human-readable representation.

        Returns
        -------
        str
            Summary including dimensions and total count.

        Examples
        --------
        >>> cms = CountMinSketch.from_dimensions(width=100, depth=5)
        >>> cms.add("x")
        >>> str(cms)
        'CountMinSketch: 1 items, matrix=5×100'
        """
        return (
            f"CountMinSketch: {self._total} items, "
            f"matrix={self._depth}×{self._width}"
        )
