# Copyright 2024-2026, skyfrigate, biface
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

"""Quicksort: in place, not stable, O(n log n) on average.

Quicksort picks a pivot, partitions the list so that every element before
the split point is not after the pivot and every element after it is not
before the pivot, then sorts both parts. This implementation uses:

- **Hoare partitioning**, which scans from both ends and swaps
  out-of-place pairs. It handles runs of equal keys well: equal elements
  are spread over both sides instead of piling up on one.
- **Median-of-three pivot selection** (first, middle, last), which makes
  already sorted and reverse-sorted inputs, the classic worst cases of a
  naive first-element pivot, run in O(n log n).
- **Recursion on the smaller part only**, looping on the larger one, which
  bounds the call stack to O(log n) even when partitions are unbalanced.

.. code-block:: text

    quick_sort(A, lo, hi):
        while lo < hi:
            p <- partition(A, lo, hi)          # A[lo..p] <= pivot <= A[p+1..hi]
            recurse on the smaller of A[lo..p] and A[p+1..hi]
            continue the loop on the larger one

Swapping elements across the pivot breaks the original order of equal
keys, so quicksort is not stable: use
:func:`~sds.algorithms.sorting.merge_sort` when that matters.
"""

from typing import Any, Callable, List, Optional, TypeVar

T = TypeVar("T")


def quick_sort(
    items: List[T],
    *,
    key: Optional[Callable[[T], Any]] = None,
    reverse: bool = False,
) -> None:
    """Sort ``items`` in place.

    Like :meth:`list.sort`, the function returns ``None`` to make it clear
    that the argument itself was modified.

    Parameters
    ----------
    items : list
        The list to sort, modified in place.
    key : callable, optional
        Function of one argument extracting the comparison key from each
        item, as for :meth:`list.sort`. It is called exactly once per item.
    reverse : bool, optional
        If True, sort in descending order.

    Raises
    ------
    TypeError
        If ``items`` is not a ``list``, or if two keys cannot be compared.

    Examples
    --------
    >>> data = [5, 2, 4, 1]
    >>> quick_sort(data)
    >>> data
    [1, 2, 4, 5]
    >>> words = ["ccc", "a", "bb"]
    >>> quick_sort(words, key=len, reverse=True)
    >>> words
    ['ccc', 'bb', 'a']

    Notes
    -----
    Time complexity: O(n log n) on average, O(n²) in the worst case (made
    unlikely, not impossible, by the median-of-three pivot).
    Space complexity: O(log n) recursion depth; O(n) additional when
    ``key`` is given, for the precomputed keys.

    The sort is not stable: items with equal keys may end up in any
    relative order. Three records sharing one key are enough to show it:

    >>> records = [(0, "a"), (0, "b"), (0, "c")]
    >>> quick_sort(records, key=lambda r: r[0])
    >>> records
    [(0, 'a'), (0, 'c'), (0, 'b')]

    When the order of ties matters, use :func:`merge_sort`, which is
    stable and O(n log n) in every case. To sort a list in place *and*
    stably, assign the result back into the same list object::

        items[:] = merge_sort(items, key=key)

    A stable quicksort would need O(n) extra memory to break ties by
    original position, losing its only advantage over merge sort while
    keeping its O(n²) worst case, so none is provided.
    """
    if not isinstance(items, list):
        raise TypeError(f"quick_sort expects a list, got {type(items).__name__}")
    keys: List[Any] = items if key is None else [key(item) for item in items]
    _Sorter(items, keys, reverse).sort(0, len(items) - 1)


class _Sorter:
    """Carry the lists being sorted so the helpers need no long signatures.

    ``keys`` is either ``items`` itself (no key function) or a parallel list
    of precomputed keys that is permuted in lockstep with ``items``.
    """

    __slots__ = ("_items", "_keys", "_reverse")

    def __init__(self, items: List[Any], keys: List[Any], reverse: bool) -> None:
        self._items = items
        self._keys = keys
        self._reverse = reverse

    def _before(self, a: Any, b: Any) -> bool:
        """Return True if key ``a`` must come strictly before key ``b``."""
        return bool(a > b) if self._reverse else bool(a < b)

    def _swap(self, i: int, j: int) -> None:
        """Swap positions ``i`` and ``j`` in both lists."""
        items, keys = self._items, self._keys
        items[i], items[j] = items[j], items[i]
        if keys is not items:
            keys[i], keys[j] = keys[j], keys[i]

    def sort(self, lo: int, hi: int) -> None:
        """Sort the slice ``[lo, hi]`` (inclusive bounds)."""
        while lo < hi:
            split = self._partition(lo, hi)
            if split - lo < hi - split:
                self.sort(lo, split)
                lo = split + 1
            else:
                self.sort(split + 1, hi)
                hi = split

    def _partition(self, lo: int, hi: int) -> int:
        """Hoare partition of ``[lo, hi]``; return the split index.

        On return, no key in ``[lo, split]`` comes after the pivot and no
        key in ``[split + 1, hi]`` comes before it. ``split < hi`` always
        holds, so both parts are strictly smaller than the input.
        """
        self._median_of_three_to_front(lo, hi)
        keys = self._keys
        pivot = keys[lo]
        i, j = lo - 1, hi + 1
        while True:
            i += 1
            while self._before(keys[i], pivot):
                i += 1
            j -= 1
            while self._before(pivot, keys[j]):
                j -= 1
            if i >= j:
                return j
            self._swap(i, j)

    def _median_of_three_to_front(self, lo: int, hi: int) -> None:
        """Move the median of ``keys[lo]``, ``keys[mid]``, ``keys[hi]`` to ``lo``."""
        keys = self._keys
        mid = (lo + hi) // 2
        # Order the three candidates so that keys[lo] <= keys[mid] <= keys[hi]
        # (in the requested direction), then bring the median to the front.
        if self._before(keys[mid], keys[lo]):
            self._swap(mid, lo)
        if self._before(keys[hi], keys[lo]):
            self._swap(hi, lo)
        if self._before(keys[hi], keys[mid]):
            self._swap(hi, mid)
        self._swap(lo, mid)
