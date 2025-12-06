# Copyright 2024-205, skyfrigate, biface
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

"""Tests for Heap implementations."""

import pytest

from sds.core.exceptions import EmptyStructureError
from sds.tree.heap import MinHeap

# =============================================================================
# MinHeap Tests
# =============================================================================


class TestMinHeapCreation:
    """Test MinHeap creation and initialization."""

    def test_create_empty_min_heap(self) -> None:
        """Test creating an empty min-heap."""
        heap = MinHeap()
        assert heap.is_empty()
        assert len(heap) == 0
        assert heap.size == 0

    def test_create_min_heap_from_list(self) -> None:
        """Test creating min-heap from list."""
        items = [5, 3, 7, 1, 9, 4]
        heap = MinHeap(items)
        assert len(heap) == 6
        assert heap.peek() == 1

    def test_min_heap_bool(self) -> None:
        """Test boolean evaluation of min-heap."""
        heap = MinHeap()
        assert not heap
        heap.insert(5)
        assert heap


class TestMinHeapInsertion:
    """Test MinHeap insertion operations."""

    def test_insert_single_element(self) -> None:
        """Test inserting a single element."""
        heap = MinHeap()
        heap.insert(5)
        assert len(heap) == 1
        assert heap.peek() == 5

    def test_insert_multiple_elements(self) -> None:
        """Test inserting multiple elements."""
        heap = MinHeap()
        heap.insert(5)
        heap.insert(3)
        heap.insert(7)
        assert len(heap) == 3
        assert heap.peek() == 3

    def test_insert_maintains_min_heap_property(self) -> None:
        """Test that insertion maintains min-heap property."""
        heap = MinHeap()
        values = [10, 5, 15, 3, 7, 12, 20]
        for val in values:
            heap.insert(val)
        # Extract all and verify order
        extracted = []
        while not heap.is_empty():
            extracted.append(heap.extract())
        assert extracted == sorted(values)

    def test_insert_duplicates(self) -> None:
        """Test inserting duplicate values."""
        heap = MinHeap()
        heap.insert(5)
        heap.insert(5)
        heap.insert(5)
        assert len(heap) == 3
        assert heap.peek() == 5

    def test_insert_ascending_order(self) -> None:
        """Test inserting in ascending order."""
        heap = MinHeap()
        for i in range(1, 6):
            heap.insert(i)
        assert heap.peek() == 1

    def test_insert_descending_order(self) -> None:
        """Test inserting in descending order."""
        heap = MinHeap()
        for i in range(5, 0, -1):
            heap.insert(i)
        assert heap.peek() == 1


class TestMinHeapExtraction:
    """Test MinHeap extraction operations."""

    def test_extract_from_empty_heap(self) -> None:
        """Test extracting from empty heap raises error."""
        heap = MinHeap()
        with pytest.raises(EmptyStructureError):
            heap.extract()

    def test_extract_single_element(self) -> None:
        """Test extracting single element."""
        heap = MinHeap()
        heap.insert(5)
        assert heap.extract() == 5
        assert heap.is_empty()

    def test_extract_multiple_elements(self) -> None:
        """Test extracting multiple elements."""
        heap = MinHeap([5, 3, 7, 1, 9])
        extracted = []
        while not heap.is_empty():
            extracted.append(heap.extract())
        assert extracted == [1, 3, 5, 7, 9]

    def test_extract_maintains_heap_property(self) -> None:
        """Test that extraction maintains min-heap property."""
        heap = MinHeap([10, 5, 15, 3, 7, 12, 20, 1])
        first = heap.extract()
        assert first == 1
        second = heap.extract()
        assert second == 3
        # Rest should still be a valid heap
        assert heap.peek() == 5


class TestMinHeapPeek:
    """Test MinHeap peek operations."""

    def test_peek_empty_heap(self) -> None:
        """Test peeking at empty heap raises error."""
        heap = MinHeap()
        with pytest.raises(EmptyStructureError):
            heap.peek()

    def test_peek_single_element(self) -> None:
        """Test peeking at single element."""
        heap = MinHeap()
        heap.insert(5)
        assert heap.peek() == 5
        assert len(heap) == 1

    def test_peek_does_not_remove(self) -> None:
        """Test that peek does not remove element."""
        heap = MinHeap([5, 3, 7])
        first_peek = heap.peek()
        second_peek = heap.peek()
        assert first_peek == second_peek == 3
        assert len(heap) == 3

    def test_peek_returns_minimum(self) -> None:
        """Test that peek always returns minimum."""
        heap = MinHeap([10, 5, 15, 3, 7])
        assert heap.peek() == 3


class TestMinHeapClear:
    """Test MinHeap clear operation."""

    def test_clear_empty_heap(self) -> None:
        """Test clearing empty heap."""
        heap = MinHeap()
        heap.clear()
        assert heap.is_empty()

    def test_clear_non_empty_heap(self) -> None:
        """Test clearing non-empty heap."""
        heap = MinHeap([5, 3, 7, 1])
        heap.clear()
        assert heap.is_empty()
        assert len(heap) == 0

    def test_heap_usable_after_clear(self) -> None:
        """Test that heap is usable after clear."""
        heap = MinHeap([5, 3, 7])
        heap.clear()
        heap.insert(10)
        assert len(heap) == 1
        assert heap.peek() == 10


class TestMinHeapIteration:
    """Test MinHeap iteration."""

    def test_iter_empty_heap(self) -> None:
        """Test iterating over empty heap."""
        heap = MinHeap()
        assert list(heap) == []

    def test_iter_non_empty_heap(self) -> None:
        """Test iterating over non-empty heap."""
        heap = MinHeap([5, 3, 7])
        items = list(heap)
        assert len(items) == 3
        assert 3 in items
        assert 5 in items
        assert 7 in items

    def test_contains(self) -> None:
        """Test __contains__ method."""
        heap = MinHeap([5, 3, 7, 1])
        assert 3 in heap
        assert 7 in heap
        assert 10 not in heap


class TestMinHeapStringRepresentation:
    """Test MinHeap string representations."""

    def test_repr_empty_heap(self) -> None:
        """Test repr of empty heap."""
        heap = MinHeap()
        assert repr(heap) == "MinHeap(size=0)"

    def test_repr_non_empty_heap(self) -> None:
        """Test repr of non-empty heap."""
        heap = MinHeap([5, 3])
        assert repr(heap) == "MinHeap(size=2)"

    def test_str_empty_heap(self) -> None:
        """Test str of empty heap."""
        heap = MinHeap()
        assert str(heap) == "MinHeap: []"

    def test_str_non_empty_heap(self) -> None:
        """Test str of non-empty heap."""
        heap = MinHeap([5, 3, 7])
        result = str(heap)
        assert result.startswith("MinHeap: ")


class TestMinHeapEdgeCases:
    """Test MinHeap edge cases."""

    def test_negative_numbers(self) -> None:
        """Test heap with negative numbers."""
        heap = MinHeap([0, -5, 5, -3, 3])
        assert heap.peek() == -5
        extracted = []
        while not heap.is_empty():
            extracted.append(heap.extract())
        assert extracted == [-5, -3, 0, 3, 5]

    def test_float_values(self) -> None:
        """Test heap with float values."""
        heap = MinHeap([3.5, 1.2, 5.7, 2.1])
        assert heap.peek() == 1.2

    def test_string_values(self) -> None:
        """Test heap with string values."""
        heap = MinHeap(["dog", "cat", "elephant", "ant"])
        assert heap.peek() == "ant"
        extracted = []
        while not heap.is_empty():
            extracted.append(heap.extract())
        assert extracted == ["ant", "cat", "dog", "elephant"]

    def test_large_heap(self) -> None:
        """Test with large number of elements."""
        n = 1000
        import random

        values = list(range(n))
        random.shuffle(values)
        heap = MinHeap(values)
        assert heap.peek() == 0
        assert len(heap) == n
