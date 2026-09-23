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

"""Tests for to_list() / from_list() conversion utilities (#95)."""

from typing import Any, Iterator, List, Type

import pytest

from sds.core.interfaces import LinearCollection
from sds.linear import (
    CircularLinkedList,
    Deque,
    DoublyLinkedList,
    LinkedList,
    PriorityQueue,
    Queue,
    Stack,
    from_list,
    to_list,
)

ITEMS = [3, 1, 4, 1, 5, 9, 2, 6]

ORDER_PRESERVING = [LinkedList, DoublyLinkedList, CircularLinkedList, Queue, Deque]
ALL_CLASSES = ORDER_PRESERVING + [Stack, PriorityQueue]


def _cls_id(cls: type) -> str:
    return cls.__name__


class TestToList:
    """Tests for to_list()."""

    @pytest.mark.parametrize("cls", ALL_CLASSES, ids=_cls_id)
    def test_matches_iteration_order(self, cls: Type[LinearCollection]) -> None:
        """to_list() returns exactly what iterating the structure yields."""
        structure = from_list(cls, ITEMS)
        assert to_list(structure) == list(iter(structure))

    @pytest.mark.parametrize("cls", ALL_CLASSES, ids=_cls_id)
    def test_empty_structure(self, cls: Type[LinearCollection]) -> None:
        """An empty structure gives an empty list."""
        assert to_list(cls()) == []

    def test_returns_independent_copy(self) -> None:
        """Mutating the returned list leaves the structure untouched."""
        structure = from_list(LinkedList, [1, 2, 3])
        result = to_list(structure)
        result.append(4)
        assert to_list(structure) == [1, 2, 3]

    def test_does_not_consume_structure(self) -> None:
        """to_list() leaves the structure's size unchanged."""
        queue = from_list(Queue, [1, 2, 3])
        to_list(queue)
        assert len(queue) == 3

    @pytest.mark.parametrize("bad", [[1, 2], (1, 2), "ab", None, 42])
    def test_rejects_non_linear_collection(self, bad: Any) -> None:
        """Anything that is not a LinearCollection raises TypeError."""
        with pytest.raises(TypeError, match="LinearCollection"):
            to_list(bad)


class TestFromList:
    """Tests for from_list()."""

    @pytest.mark.parametrize("cls", ALL_CLASSES, ids=_cls_id)
    def test_returns_instance_of_cls(self, cls: Type[LinearCollection]) -> None:
        """The result is a new instance of the requested class."""
        structure = from_list(cls, ITEMS)
        assert type(structure) is cls
        assert len(structure) == len(ITEMS)

    @pytest.mark.parametrize("cls", ALL_CLASSES, ids=_cls_id)
    def test_empty_items(self, cls: Type[LinearCollection]) -> None:
        """No items gives an empty structure."""
        assert from_list(cls, []).is_empty()

    def test_accepts_any_iterable(self) -> None:
        """Generators, tuples and other structures are valid inputs."""

        def gen() -> Iterator[int]:
            yield from (1, 2, 3)

        assert to_list(from_list(Deque, gen())) == [1, 2, 3]
        assert to_list(from_list(Deque, (1, 2, 3))) == [1, 2, 3]
        source = from_list(DoublyLinkedList, [1, 2, 3])
        assert to_list(from_list(Queue, source)) == [1, 2, 3]

    def test_does_not_mutate_input(self) -> None:
        """The input list is left unchanged."""
        items = [3, 1, 2]
        from_list(PriorityQueue, items)
        assert items == [3, 1, 2]

    def test_uses_add_semantics(self) -> None:
        """Each class applies its own add(): push for Stack, dequeue order."""
        stack = from_list(Stack, [1, 2, 3])
        assert stack.pop() == 3
        queue = from_list(Queue, [1, 2, 3])
        assert queue.dequeue() == 1

    @pytest.mark.parametrize("bad", [list, dict, int, "Stack", None])
    def test_rejects_non_linear_class(self, bad: Any) -> None:
        """A class outside LinearCollection (or a non-class) raises TypeError."""
        with pytest.raises(TypeError, match="LinearCollection"):
            from_list(bad, [1, 2])

    def test_rejects_instance_instead_of_class(self) -> None:
        """Passing an instance rather than the class raises TypeError."""
        with pytest.raises(TypeError, match="LinearCollection"):
            from_list(LinkedList(), [1])  # type: ignore[arg-type]

    def test_unexpected_kwarg_raises(self) -> None:
        """kwargs not accepted by the constructor raise TypeError."""
        with pytest.raises(TypeError):
            from_list(Queue, [1], key=len)


class TestFromListKwargs:
    """Constructor keyword forwarding, exercised on PriorityQueue."""

    def test_default_is_ascending(self) -> None:
        """Without kwargs, lower values come first."""
        assert to_list(from_list(PriorityQueue, ITEMS)) == sorted(ITEMS)

    def test_reverse(self) -> None:
        """reverse=True puts higher values first."""
        result = to_list(from_list(PriorityQueue, ITEMS, reverse=True))
        assert result == sorted(ITEMS, reverse=True)

    def test_key(self) -> None:
        """key= is forwarded and drives the ordering."""
        words = ["pear", "fig", "banana", "kiwi"]
        result = to_list(from_list(PriorityQueue, words, key=len))
        assert [len(w) for w in result] == [3, 4, 4, 6]

    def test_key_and_reverse(self) -> None:
        """key= and reverse= combine."""
        words = ["pear", "fig", "banana"]
        result = to_list(from_list(PriorityQueue, words, key=len, reverse=True))
        assert result == ["banana", "pear", "fig"]


class TestRoundTrip:
    """to_list(from_list(cls, items)) for every linear class."""

    @pytest.mark.parametrize("cls", ORDER_PRESERVING, ids=_cls_id)
    def test_identity_for_order_preserving(self, cls: Type[LinearCollection]) -> None:
        """Insertion-ordered structures round-trip unchanged."""
        assert to_list(from_list(cls, ITEMS)) == ITEMS

    def test_stack_reverses(self) -> None:
        """Stack iterates top to bottom: the round trip is reversed."""
        assert to_list(from_list(Stack, ITEMS)) == ITEMS[::-1]

    def test_stack_double_round_trip_restores(self) -> None:
        """Two Stack round trips cancel the reversal."""
        once = to_list(from_list(Stack, ITEMS))
        assert to_list(from_list(Stack, once)) == ITEMS

    def test_priority_queue_sorts(self) -> None:
        """PriorityQueue reorders by priority, duplicates kept."""
        result: List[int] = to_list(from_list(PriorityQueue, ITEMS))
        assert result == sorted(ITEMS)
        assert result != ITEMS

    @pytest.mark.parametrize("cls", ALL_CLASSES, ids=_cls_id)
    def test_same_multiset(self, cls: Type[LinearCollection]) -> None:
        """Whatever the order, no item is lost or duplicated."""
        assert sorted(to_list(from_list(cls, ITEMS))) == sorted(ITEMS)

    @pytest.mark.parametrize("cls", ORDER_PRESERVING, ids=_cls_id)
    def test_sort_then_rebuild(self, cls: Type[LinearCollection]) -> None:
        """The intended workflow: structure -> list -> sorted -> structure."""
        structure = from_list(cls, ITEMS)
        rebuilt = from_list(cls, sorted(to_list(structure)))
        assert type(rebuilt) is cls
        assert to_list(rebuilt) == sorted(ITEMS)
