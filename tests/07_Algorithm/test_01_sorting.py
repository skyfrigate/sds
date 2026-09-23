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

"""Tests for sds.algorithms.sorting (quick_sort, merge_sort), per #93."""

import random
import sys
from typing import Any, Callable, List, Tuple

import pytest

from sds.algorithms.sorting import merge_sort, quick_sort
from sds.linear import LinkedList

# Inputs shared by both algorithms: (id, data)
CASES: List[Tuple[str, List[int]]] = [
    ("empty", []),
    ("single", [7]),
    ("two_sorted", [1, 2]),
    ("two_reversed", [2, 1]),
    ("sorted", list(range(20))),
    ("reversed", list(range(20, 0, -1))),
    ("duplicates", [3, 1, 3, 2, 1, 3, 2]),
    ("all_equal", [5] * 15),
    ("negatives", [0, -3, 7, -1, -3, 2]),
    ("organ_pipe", [1, 3, 5, 7, 9, 8, 6, 4, 2, 0]),
]


def _quick(data: List[Any], **kw: Any) -> List[Any]:
    """Run quick_sort on a copy and return the sorted copy."""
    copy = list(data)
    quick_sort(copy, **kw)
    return copy


SORTERS: List[Any] = [
    pytest.param(merge_sort, id="merge_sort"),
    pytest.param(_quick, id="quick_sort"),
]


@pytest.mark.parametrize("sorter", SORTERS)
class TestSortingContract:
    """Behaviour both algorithms share: same results as sorted()."""

    @pytest.mark.parametrize(("name", "data"), CASES, ids=[c[0] for c in CASES])
    def test_matches_sorted(
        self, sorter: Callable[..., List[Any]], name: str, data: List[int]
    ) -> None:
        """Result equals sorted() on edge-case inputs."""
        assert sorter(data) == sorted(data)

    @pytest.mark.parametrize(("name", "data"), CASES, ids=[c[0] for c in CASES])
    def test_reverse(
        self, sorter: Callable[..., List[Any]], name: str, data: List[int]
    ) -> None:
        """reverse=True equals sorted(reverse=True)."""
        assert sorter(data, reverse=True) == sorted(data, reverse=True)

    def test_key(self, sorter: Callable[..., List[Any]]) -> None:
        """key= orders by the extracted key."""
        words = ["pear", "fig", "banana", "kiwi", "apple"]
        result = sorter(words, key=len)
        assert [len(w) for w in result] == sorted(len(w) for w in words)
        assert sorted(result) == sorted(words)

    def test_key_called_once_per_item(self, sorter: Callable[..., List[Any]]) -> None:
        """The key function is evaluated exactly n times."""
        calls: List[int] = []

        def key(x: int) -> int:
            calls.append(x)
            return -x

        data = list(range(50))
        random.Random(0).shuffle(data)
        sorter(data, key=key)
        assert len(calls) == len(data)

    @pytest.mark.parametrize("seed", range(20))
    def test_random_against_sorted(
        self, sorter: Callable[..., List[Any]], seed: int
    ) -> None:
        """Random inputs with many duplicates agree with sorted()."""
        rng = random.Random(seed)
        data = [rng.randint(-20, 20) for _ in range(rng.randint(0, 200))]
        assert sorter(data) == sorted(data)
        assert sorter(data, reverse=True) == sorted(data, reverse=True)

    def test_strings(self, sorter: Callable[..., List[Any]]) -> None:
        """Any mutually comparable items are accepted."""
        data = ["delta", "alpha", "charlie", "bravo"]
        assert sorter(data) == sorted(data)

    def test_large_sorted_input_is_fast_and_shallow(
        self, sorter: Callable[..., List[Any]]
    ) -> None:
        """Sorted input of size well above the recursion limit is handled."""
        n = sys.getrecursionlimit() * 4
        data = list(range(n))
        assert sorter(data) == data
        assert sorter(data[::-1]) == data

    def test_incomparable_keys_raise(self, sorter: Callable[..., List[Any]]) -> None:
        """Mixing incomparable types raises TypeError, like sorted()."""
        with pytest.raises(TypeError):
            sorter([1, "a", 2])

    @pytest.mark.parametrize(
        "bad", [(3, 1, 2), "cab", {3, 1, 2}, None], ids=["tuple", "str", "set", "none"]
    )
    def test_rejects_non_list(self, sorter: Callable[..., List[Any]], bad: Any) -> None:
        """Only Python lists are accepted (#93)."""
        with pytest.raises(TypeError, match="expects a list"):
            if sorter is merge_sort:
                merge_sort(bad)
            else:
                quick_sort(bad)

    def test_rejects_linear_structure(self, sorter: Callable[..., List[Any]]) -> None:
        """A linear structure must go through to_list() first (#94)."""
        lst = LinkedList()
        lst.append(2)
        lst.append(1)
        with pytest.raises(TypeError, match="expects a list"):
            if sorter is merge_sort:
                merge_sort(lst)  # type: ignore[arg-type]
            else:
                quick_sort(lst)  # type: ignore[arg-type]


class TestMergeSort:
    """Properties specific to merge_sort: stable, non-mutating."""

    def test_returns_new_list(self) -> None:
        """The result is a distinct list object."""
        data = [2, 1]
        result = merge_sort(data)
        assert result is not data

    def test_does_not_mutate_input(self) -> None:
        """The argument is left untouched."""
        data = [3, 1, 2]
        merge_sort(data)
        assert data == [3, 1, 2]

    def test_stable(self) -> None:
        """Equal keys keep their original relative order."""
        records = [("b", 2), ("a", 1), ("c", 2), ("d", 1), ("e", 2)]
        result = merge_sort(records, key=lambda r: r[1])
        assert result == [("a", 1), ("d", 1), ("b", 2), ("c", 2), ("e", 2)]

    def test_stable_in_reverse(self) -> None:
        """reverse=True keeps equal keys in original order, like sorted()."""
        records = [("b", 2), ("a", 1), ("c", 2), ("d", 1), ("e", 2)]
        result = merge_sort(records, key=lambda r: r[1], reverse=True)
        assert result == sorted(records, key=lambda r: r[1], reverse=True)
        assert result == [("b", 2), ("c", 2), ("e", 2), ("a", 1), ("d", 1)]

    @pytest.mark.parametrize("seed", range(10))
    def test_stable_random(self, seed: int) -> None:
        """Stability holds on random records with many ties."""
        rng = random.Random(seed)
        records = [(rng.randint(0, 5), i) for i in range(100)]
        key: Callable[[Tuple[int, int]], int] = lambda r: r[0]  # noqa: E731
        assert merge_sort(records, key=key) == sorted(records, key=key)
        assert merge_sort(records, key=key, reverse=True) == sorted(
            records, key=key, reverse=True
        )

    def test_items_never_compared(self) -> None:
        """Only keys are compared, so unorderable items are fine with key=."""

        class Opaque:
            def __init__(self, rank: int) -> None:
                self.rank = rank

        data = [Opaque(3), Opaque(1), Opaque(2)]
        assert [o.rank for o in merge_sort(data, key=lambda o: o.rank)] == [1, 2, 3]


class TestQuickSort:
    """Properties specific to quick_sort: in place, returns None."""

    def test_returns_none(self) -> None:
        """Like list.sort(), the function returns None."""
        assert quick_sort([2, 1]) is None

    def test_sorts_in_place(self) -> None:
        """The argument object itself is sorted."""
        data = [3, 1, 2]
        alias = data
        quick_sort(data)
        assert alias == [1, 2, 3]

    def test_items_follow_keys(self) -> None:
        """With key=, items are permuted together with their keys."""
        data = [("x", 3), ("y", 1), ("z", 2)]
        quick_sort(data, key=lambda r: r[1])
        assert data == [("y", 1), ("z", 2), ("x", 3)]

    def test_items_never_compared(self) -> None:
        """Only keys are compared, so unorderable items are fine with key=."""

        class Opaque:
            def __init__(self, rank: int) -> None:
                self.rank = rank

        data = [Opaque(3), Opaque(1), Opaque(2)]
        quick_sort(data, key=lambda o: o.rank)
        assert [o.rank for o in data] == [1, 2, 3]

    def test_many_duplicates_large(self) -> None:
        """Heavy duplication (Hoare's strong case) stays correct."""
        rng = random.Random(42)
        data = [rng.randint(0, 3) for _ in range(5000)]
        expected = sorted(data)
        quick_sort(data)
        assert data == expected

    def test_not_guaranteed_stable(self) -> None:
        """Documented contract: stability is not promised.

        Only the key order is asserted; the order of ties is free.
        """
        records = [(1, "a"), (0, "b"), (1, "c"), (0, "d")] * 5
        quick_sort(records, key=lambda r: r[0])
        assert [r[0] for r in records] == sorted(r[0] for r in records)
