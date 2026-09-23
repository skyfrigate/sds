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

"""Merge sort: stable, non-mutating, O(n log n) in every case.

Merge sort splits the input in two halves, sorts each half recursively and
merges the two sorted halves into one. Merging takes the element of the
left half whenever the two candidates compare equal, which is what makes
the algorithm stable: equal elements keep their original relative order.

.. code-block:: text

    merge_sort(A):
        if |A| <= 1: return A
        L <- merge_sort(A[0 .. n/2 - 1])
        R <- merge_sort(A[n/2 .. n - 1])
        return merge(L, R)

The recursion tree has ``log2 n`` levels and each level merges ``n``
elements in total, hence ``O(n log n)`` comparisons whatever the input.
"""

from typing import Any, Callable, List, Optional, Tuple, TypeVar

T = TypeVar("T")

_Pair = Tuple[Any, T]


def merge_sort(
    items: List[T],
    *,
    key: Optional[Callable[[T], Any]] = None,
    reverse: bool = False,
) -> List[T]:
    """Return a new list with the items of ``items`` in sorted order.

    Parameters
    ----------
    items : list
        The list to sort. It is not modified.
    key : callable, optional
        Function of one argument extracting the comparison key from each
        item, as for :func:`sorted`. It is called exactly once per item.
    reverse : bool, optional
        If True, sort in descending order. Stability is preserved: equal
        items still keep their original relative order.

    Returns
    -------
    list
        A new sorted list.

    Raises
    ------
    TypeError
        If ``items`` is not a ``list``, or if two keys cannot be compared.

    Examples
    --------
    >>> merge_sort([5, 2, 4, 1])
    [1, 2, 4, 5]
    >>> merge_sort(["bb", "a", "cc", "d"], key=len)
    ['a', 'd', 'bb', 'cc']
    >>> merge_sort([1, 3, 2], reverse=True)
    [3, 2, 1]

    Notes
    -----
    Time complexity: O(n log n) in the best, average and worst case.
    Space complexity: O(n) for the merged lists, plus O(log n) recursion
    depth.

    Keys are computed once up front and carried alongside each item, so
    items themselves are never compared and ``key`` is never called twice
    for the same element.
    """
    if not isinstance(items, list):
        raise TypeError(f"merge_sort expects a list, got {type(items).__name__}")
    pairs: List[_Pair[T]] = [
        (item if key is None else key(item), item) for item in items
    ]
    return [item for _, item in _sort(pairs, reverse)]


def _sort(pairs: List[_Pair[T]], reverse: bool) -> List[_Pair[T]]:
    """Recursively sort ``(key, item)`` pairs by key."""
    if len(pairs) <= 1:
        return list(pairs)
    middle = len(pairs) // 2
    return _merge(
        _sort(pairs[:middle], reverse), _sort(pairs[middle:], reverse), reverse
    )


def _merge(
    left: List[_Pair[T]], right: List[_Pair[T]], reverse: bool
) -> List[_Pair[T]]:
    """Merge two sorted runs, taking from ``left`` on ties (stability)."""
    merged: List[_Pair[T]] = []
    i = j = 0
    while i < len(left) and j < len(right):
        # Take from the right run only when it is strictly first in the
        # requested order; equal keys fall through to the left run.
        right_first = right[j][0] > left[i][0] if reverse else right[j][0] < left[i][0]
        if right_first:
            merged.append(right[j])
            j += 1
        else:
            merged.append(left[i])
            i += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged
