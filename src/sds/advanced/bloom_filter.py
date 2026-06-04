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

"""Bloom Filter probabilistic data structure implementation.

This module provides a space-efficient probabilistic set membership structure.
A Bloom filter can test whether an element is a member of a set, with a
controlled false positive rate and no false negatives.

Classes
-------
BloomFilter
    Space-efficient probabilistic membership structure using k hash functions
    and a bit array of size m.

Examples
--------
Basic membership testing:

>>> bf = BloomFilter(size=1000, num_hashes=3)
>>> bf.add("apple")
>>> bf.add("banana")
>>> "apple" in bf
True
>>> "cherry" in bf
False

Optimal parameter calculation:

>>> size, k = BloomFilter.optimal_params(n=1000, fp_rate=0.01)
>>> bf = BloomFilter(size=size, num_hashes=k)
>>> bf.add("hello")
>>> "hello" in bf
True

Notes
-----
Time Complexity:
- add: O(k) where k is the number of hash functions
- __contains__: O(k)
- estimated_fill_ratio: O(1)

Space Complexity: O(m) bits where m is the bit array size.

A Bloom filter with k hash functions and m bits for n elements has a
false positive probability of approximately:

    P(fp) ≈ (1 - e^(-kn/m))^k

The optimal number of hash functions is:

    k_opt = (m/n) * ln(2)

And the optimal bit array size for a target false positive rate p is:

    m_opt = -n * ln(p) / (ln(2))^2

References
----------
.. [1] Bloom, B. H. (1970). "Space/time trade-offs in hash coding with
       allowable errors". Communications of the ACM, 13(7), 422-426.
       DOI: 10.1145/362686.362692
.. [2] Broder, A., & Mitzenmacher, M. (2004). "Network Applications of
       Bloom Filters: A Survey". Internet Mathematics, 1(4), 485-509.
       https://www.eecs.harvard.edu/~michaelm/postscripts/im2005b.pdf
"""

import hashlib
import math
from typing import Any, Iterator

from .interfaces import AbstractProbabilisticSet

__all__ = ["BloomFilter"]


class BloomFilter(AbstractProbabilisticSet):
    """Space-efficient probabilistic set membership structure.

    A Bloom filter uses k independent hash functions and a bit array of m bits
    to represent a set. Adding an element sets k bits; querying checks if all
    k bits are set.

    - **No false negatives**: if ``item in bf`` returns False, the item is
      definitely not in the set.
    - **Possible false positives**: if ``item in bf`` returns True, the item
      is *probably* (but not certainly) in the set.

    Parameters
    ----------
    size : int
        Size of the bit array (m). Larger values reduce false positive rate.
    num_hashes : int
        Number of hash functions (k). Optimal value is ``(m/n) * ln(2)``.

    Attributes
    ----------
    size : int
        Size of the bit array in bits (read-only).
    num_hashes : int
        Number of hash functions used (read-only).
    count : int
        Number of items added (read-only). Not deduplicated.

    Raises
    ------
    ValueError
        If ``size`` or ``num_hashes`` is not a positive integer.

    Examples
    --------
    Create with explicit parameters:

    >>> bf = BloomFilter(size=9585, num_hashes=7)
    >>> bf.add("url:https://example.com")
    >>> "url:https://example.com" in bf
    True
    >>> "url:https://other.com" in bf
    False

    Create with optimal parameters for a target false positive rate:

    >>> size, k = BloomFilter.optimal_params(n=1000, fp_rate=0.01)
    >>> bf = BloomFilter(size=size, num_hashes=k)
    >>> for word in ["alpha", "beta", "gamma"]:
    ...     bf.add(word)
    >>> "alpha" in bf
    True

    Notes
    -----
    - Elements must be serialisable to bytes (strings, numbers, bytes).
    - Deletion is **not supported** — use a Counting Bloom Filter variant
      if removal is required.
    - Once the fill ratio approaches 1.0, the false positive rate rises
      sharply. Use :meth:`optimal_params` to size the filter correctly.

    See Also
    --------
    AbstractProbabilisticSet : Abstract interface for probabilistic sets.
    BloomFilter.optimal_params : Calculate optimal size and hash count.
    """

    def __init__(self, size: int, num_hashes: int) -> None:
        """Initialise a Bloom filter with a given bit array size and hash count.

        Parameters
        ----------
        size : int
            Number of bits in the filter (m). Must be a positive integer.
        num_hashes : int
            Number of independent hash functions (k). Must be a positive integer.

        Raises
        ------
        ValueError
            If ``size`` or ``num_hashes`` is less than 1.

        Examples
        --------
        >>> bf = BloomFilter(size=1000, num_hashes=3)
        >>> len(bf)
        0

        Notes
        -----
        Time complexity: O(m) for bit array initialisation.
        """
        if size < 1:
            raise ValueError(f"size must be a positive integer, got {size}")
        if num_hashes < 1:
            raise ValueError(f"num_hashes must be a positive integer, got {num_hashes}")

        self._size = size
        self._num_hashes = num_hashes
        self._bit_array: bytearray = bytearray(math.ceil(size / 8))
        self._count = 0

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def size(self) -> int:
        """Size of the bit array in bits.

        Returns
        -------
        int
            Number of bits (m).

        Examples
        --------
        >>> bf = BloomFilter(size=1000, num_hashes=3)
        >>> bf.size
        1000
        """
        return self._size

    @property
    def num_hashes(self) -> int:
        """Number of hash functions.

        Returns
        -------
        int
            Number of hash functions (k).

        Examples
        --------
        >>> bf = BloomFilter(size=1000, num_hashes=3)
        >>> bf.num_hashes
        3
        """
        return self._num_hashes

    @property
    def count(self) -> int:
        """Number of items added to the filter.

        Returns
        -------
        int
            Total number of ``add()`` calls (not deduplicated).

        Examples
        --------
        >>> bf = BloomFilter(size=1000, num_hashes=3)
        >>> bf.add("x")
        >>> bf.add("x")
        >>> bf.count
        2
        """
        return self._count

    # ------------------------------------------------------------------
    # Static helpers
    # ------------------------------------------------------------------

    @staticmethod
    def optimal_params(n: int, fp_rate: float) -> tuple[int, int]:
        """Calculate optimal bit array size and hash count for given constraints.

        Given the expected number of elements ``n`` and a target false positive
        rate ``fp_rate``, returns the minimal bit array size ``m`` and the
        optimal number of hash functions ``k``.

        Parameters
        ----------
        n : int
            Expected number of elements to insert. Must be positive.
        fp_rate : float
            Target false positive probability. Must be in (0.0, 1.0).

        Returns
        -------
        tuple[int, int]
            A ``(size, num_hashes)`` pair where ``size`` is the bit array
            length and ``num_hashes`` is the number of hash functions.

        Raises
        ------
        ValueError
            If ``n`` is not positive or ``fp_rate`` is not in (0, 1).

        Examples
        --------
        >>> size, k = BloomFilter.optimal_params(n=1000, fp_rate=0.01)
        >>> size  # approximately 9585
        9585
        >>> k    # approximately 7
        7

        Notes
        -----
        Formulae used:

        .. math::

            m = \\lceil -n \\cdot \\ln(p) / (\\ln 2)^2 \\rceil

            k = \\lfloor (m / n) \\cdot \\ln(2) \\rfloor

        where :math:`p` is ``fp_rate`` and :math:`m` is rounded up.
        """
        if n < 1:
            raise ValueError(f"n must be a positive integer, got {n}")
        if not (0.0 < fp_rate < 1.0):
            raise ValueError(f"fp_rate must be in (0.0, 1.0), got {fp_rate}")

        ln2_sq = math.log(2) ** 2
        m = math.ceil(-n * math.log(fp_rate) / ln2_sq)
        k = max(1, round((m / n) * math.log(2)))
        return m, k

    # ------------------------------------------------------------------
    # Internal hashing
    # ------------------------------------------------------------------

    def _hash_positions(self, item: Any) -> list[int]:
        """Compute k bit positions for a given item.

        Uses double hashing derived from SHA-256 and MD5 digests to generate
        k independent positions in the bit array:

            pos_i = (h1 + i * h2) mod m

        This avoids computing k truly independent hash functions while
        maintaining low correlation between positions.

        Parameters
        ----------
        item : Any
            The item to hash. Converted to bytes via UTF-8 string encoding.

        Returns
        -------
        list[int]
            List of k bit positions in ``[0, size)``.
        """
        data = str(item).encode("utf-8")

        h1 = int(hashlib.sha256(data).hexdigest(), 16)
        h2 = int(hashlib.md5(data, usedforsecurity=False).hexdigest(), 16)

        return [(h1 + i * h2) % self._size for i in range(self._num_hashes)]

    # ------------------------------------------------------------------
    # Bit array accessors
    # ------------------------------------------------------------------

    def _set_bit(self, pos: int) -> None:
        """Set the bit at position ``pos`` to 1."""
        self._bit_array[pos // 8] |= 1 << (pos % 8)

    def _get_bit(self, pos: int) -> bool:
        """Return True if the bit at position ``pos`` is set."""
        return bool(self._bit_array[pos // 8] & (1 << (pos % 8)))

    # ------------------------------------------------------------------
    # AbstractProbabilisticSet interface
    # ------------------------------------------------------------------

    def add(self, item: Any) -> None:
        """Add an item to the Bloom filter.

        Sets the k bits corresponding to the item's hash positions.
        After calling ``add(item)``, ``item in self`` will always return True.

        Parameters
        ----------
        item : Any
            Item to add. Must be convertible to a string.

        Examples
        --------
        >>> bf = BloomFilter(size=1000, num_hashes=3)
        >>> bf.add("hello")
        >>> "hello" in bf
        True

        Notes
        -----
        Time complexity: O(k) where k is ``num_hashes``.
        """
        for pos in self._hash_positions(item):
            self._set_bit(pos)
        self._count += 1

    def __contains__(self, item: Any) -> bool:
        """Test if an item might be in the set.

        Returns False if the item is **definitely** not in the set (no false
        negatives). Returns True if the item is **probably** in the set
        (false positives are possible).

        Parameters
        ----------
        item : Any
            Item to test. Must be convertible to a string.

        Returns
        -------
        bool
            True if all k bit positions are set (probable member).
            False if any bit position is unset (definite non-member).

        Examples
        --------
        >>> bf = BloomFilter(size=1000, num_hashes=3)
        >>> bf.add("hello")
        >>> "hello" in bf
        True
        >>> "world" in bf
        False

        Notes
        -----
        Time complexity: O(k).
        """
        return all(self._get_bit(pos) for pos in self._hash_positions(item))

    def estimated_fill_ratio(self) -> float:
        """Return the proportion of bits set to 1 in the bit array.

        A fill ratio near 0.5 corresponds to the optimal false positive rate
        for a well-configured filter. As the ratio approaches 1.0, the false
        positive rate rises sharply.

        Returns
        -------
        float
            Fraction of bits set (0.0 to 1.0).

        Examples
        --------
        >>> bf = BloomFilter(size=1000, num_hashes=3)
        >>> bf.estimated_fill_ratio()
        0.0
        >>> bf.add("x")
        >>> bf.estimated_fill_ratio() > 0.0
        True

        Notes
        -----
        Time complexity: O(m/8) — iterates over the byte array.
        """
        set_bits = sum(bin(byte).count("1") for byte in self._bit_array)
        return set_bits / self._size

    # ------------------------------------------------------------------
    # Additional helpers
    # ------------------------------------------------------------------

    def estimated_fp_rate(self) -> float:
        """Estimate the current false positive probability.

        Uses the fill ratio to approximate the false positive rate:

        .. math::

            P(fp) \\approx \\text{fill\\_ratio}^k

        Returns
        -------
        float
            Estimated false positive probability (0.0 to 1.0).

        Examples
        --------
        >>> bf = BloomFilter(size=10000, num_hashes=7)
        >>> bf.estimated_fp_rate()  # 0.0 when empty
        0.0

        Notes
        -----
        Time complexity: O(m/8).
        """
        return self.estimated_fill_ratio() ** self._num_hashes

    def union(self, other: "BloomFilter") -> "BloomFilter":
        """Return a new Bloom filter representing the union of two filters.

        The union filter will return True for any item that either source
        filter would return True for. Both filters must have identical
        ``size`` and ``num_hashes``.

        Parameters
        ----------
        other : BloomFilter
            Another Bloom filter with the same ``size`` and ``num_hashes``.

        Returns
        -------
        BloomFilter
            A new filter whose bit array is the bitwise OR of both arrays.

        Raises
        ------
        ValueError
            If the two filters have different ``size`` or ``num_hashes``.

        Examples
        --------
        >>> bf1 = BloomFilter(size=1000, num_hashes=3)
        >>> bf2 = BloomFilter(size=1000, num_hashes=3)
        >>> bf1.add("apple")
        >>> bf2.add("banana")
        >>> merged = bf1.union(bf2)
        >>> "apple" in merged
        True
        >>> "banana" in merged
        True

        Notes
        -----
        Time complexity: O(m/8).
        """
        if self._size != other._size or self._num_hashes != other._num_hashes:
            raise ValueError(
                "Cannot union filters with different size or num_hashes. "
                f"Got ({self._size}, {self._num_hashes}) and "
                f"({other._size}, {other._num_hashes})."
            )
        result = BloomFilter(self._size, self._num_hashes)
        for i, (a, b) in enumerate(zip(self._bit_array, other._bit_array)):
            result._bit_array[i] = a | b
        result._count = self._count + other._count
        return result

    def intersection(self, other: "BloomFilter") -> "BloomFilter":
        """Return a new filter representing an approximate intersection.

        The result is an *over-approximation*: it may include false positives
        for items in neither filter, because the bit arrays are ORed over time.
        Both filters must have identical ``size`` and ``num_hashes``.

        Parameters
        ----------
        other : BloomFilter
            Another Bloom filter with the same ``size`` and ``num_hashes``.

        Returns
        -------
        BloomFilter
            A new filter whose bit array is the bitwise AND of both arrays.

        Raises
        ------
        ValueError
            If the two filters have different ``size`` or ``num_hashes``.

        Examples
        --------
        >>> bf1 = BloomFilter(size=1000, num_hashes=3)
        >>> bf2 = BloomFilter(size=1000, num_hashes=3)
        >>> bf1.add("apple")
        >>> bf1.add("common")
        >>> bf2.add("banana")
        >>> bf2.add("common")
        >>> inter = bf1.intersection(bf2)
        >>> "common" in inter
        True

        Notes
        -----
        Time complexity: O(m/8).
        The intersection filter has a higher false positive rate than the
        individual filters. Use with caution.
        """
        if self._size != other._size or self._num_hashes != other._num_hashes:
            raise ValueError(
                "Cannot intersect filters with different size or num_hashes. "
                f"Got ({self._size}, {self._num_hashes}) and "
                f"({other._size}, {other._num_hashes})."
            )
        result = BloomFilter(self._size, self._num_hashes)
        for i, (a, b) in enumerate(zip(self._bit_array, other._bit_array)):
            result._bit_array[i] = a & b
        return result

    # ------------------------------------------------------------------
    # Dunder methods
    # ------------------------------------------------------------------

    def is_empty(self) -> bool:
        """Return True if no items have been added.

        Returns
        -------
        bool
            True if count is 0.

        Notes
        -----
        Time complexity: O(1).
        """
        return self._count == 0

    def clear(self) -> None:
        """Reset the filter to its initial empty state.

        Clears the bit array and resets the item count.

        Notes
        -----
        Time complexity: O(m/8) — resets the byte array.
        """
        self._bit_array = bytearray(len(self._bit_array))
        self._count = 0

    def __iter__(self) -> "Iterator[Any]":
        """Not supported — Bloom filters do not store elements.

        Raises
        ------
        TypeError
            Always, because elements cannot be recovered from a Bloom filter.
        """
        raise TypeError(
            "BloomFilter does not support iteration: "
            "elements cannot be recovered from a probabilistic set."
        )

    def __len__(self) -> int:
        """Return the number of items added.

        Returns
        -------
        int
            Value of :attr:`count`.

        Examples
        --------
        >>> bf = BloomFilter(size=1000, num_hashes=3)
        >>> bf.add("x")
        >>> len(bf)
        1
        """
        return self._count

    def __repr__(self) -> str:
        """Return a detailed string representation.

        Returns
        -------
        str
            String of the form ``BloomFilter(size=m, num_hashes=k, count=n)``.

        Examples
        --------
        >>> bf = BloomFilter(size=1000, num_hashes=3)
        >>> repr(bf)
        'BloomFilter(size=1000, num_hashes=3, count=0)'
        """
        return (
            f"BloomFilter(size={self._size}, "
            f"num_hashes={self._num_hashes}, "
            f"count={self._count})"
        )

    def __str__(self) -> str:
        """Return a concise string representation.

        Returns
        -------
        str
            Human-readable summary of the filter state.

        Examples
        --------
        >>> bf = BloomFilter(size=1000, num_hashes=3)
        >>> bf.add("x")
        >>> str(bf)
        'BloomFilter: 1 items, fill=0.30%'
        """
        fill_pct = self.estimated_fill_ratio() * 100
        return f"BloomFilter: {self._count} items, fill={fill_pct:.2f}%"
