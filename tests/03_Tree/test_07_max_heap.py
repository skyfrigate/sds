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
from sds.tree.heap import MaxHeap

# =============================================================================
# MaxHeap Tests
# =============================================================================


class TestMaxHeapCreation:
    """Test MaxHeap creation and initialization."""

    def test_create_empty_max_heap(self) -> None:
        """Test creating an empty max-heap."""
        heap = MaxHeap()
        assert heap.is_empty()
        assert len(heap) == 0

    def test_create_max_heap_from_list(self) -> None:
        """Test creating max-heap from list."""
        items = [5, 3, 7, 1, 9, 4]
        heap = MaxHeap(items)
        assert len(heap) == 6
        assert heap.peek() == 9

    def test_max_heap_bool(self) -> None:
        """Test boolean evaluation."""
        heap = MaxHeap()
        assert not heap
        heap.insert(5)
        assert heap


class TestMaxHeapInsertion:
    """Test MaxHeap insertion operations."""

    def test_insert_single_element(self) -> None:
        """Test inserting single element."""
        heap = MaxHeap()
        heap.insert(5)
        assert heap.peek() == 5

    def test_insert_multiple_elements(self) -> None:
        """Test inserting multiple elements."""
        heap = MaxHeap()
        heap.insert(5)
        heap.insert(3)
        heap.insert(7)
        assert heap.peek() == 7

    def test_insert_maintains_max_heap_property(self) -> None:
        """Test that insertion maintains max-heap property."""
        heap = MaxHeap()
        values = [10, 5, 15, 3, 7, 12, 20]
        for val in values:
            heap.insert(val)
        extracted = []
        while not heap.is_empty():
            extracted.append(heap.extract())
        assert extracted == sorted(values, reverse=True)


class TestMaxHeapExtraction:
    """Test MaxHeap extraction operations."""

    def test_extract_from_empty_heap(self) -> None:
        """Test extracting from empty heap."""
        heap = MaxHeap()
        with pytest.raises(EmptyStructureError):
            heap.extract()

    def test_extract_single_element(self) -> None:
        """Test extracting single element."""
        heap = MaxHeap()
        heap.insert(5)
        assert heap.extract() == 5
        assert heap.is_empty()

    def test_extract_multiple_elements(self) -> None:
        """Test extracting multiple elements in descending order."""
        heap = MaxHeap([5, 3, 7, 1, 9])
        extracted = []
        while not heap.is_empty():
            extracted.append(heap.extract())
        assert extracted == [9, 7, 5, 3, 1]


class TestMaxHeapPeek:
    """Test MaxHeap peek operations."""

    def test_peek_empty_heap(self) -> None:
        """Test peeking at empty heap."""
        heap = MaxHeap()
        with pytest.raises(EmptyStructureError):
            heap.peek()

    def test_peek_returns_maximum(self) -> None:
        """Test that peek returns maximum."""
        heap = MaxHeap([10, 5, 15, 3, 7])
        assert heap.peek() == 15

    def test_peek_does_not_remove(self) -> None:
        """Test that peek does not remove element."""
        heap = MaxHeap([5, 3, 7])
        assert heap.peek() == 7
        assert len(heap) == 3


class TestMaxHeapClear:
    """Test MaxHeap clear operation."""

    def test_clear_non_empty_heap(self) -> None:
        """Test clearing non-empty heap."""
        heap = MaxHeap([5, 3, 7])
        heap.clear()
        assert heap.is_empty()


class TestMaxHeapStringRepresentation:
    """Test MaxHeap string representations."""

    def test_repr_empty_heap(self) -> None:
        """Test repr of empty heap."""
        heap = MaxHeap()
        assert repr(heap) == "MaxHeap(size=0)"

    def test_str_empty_heap(self) -> None:
        """Test str of empty heap."""
        heap = MaxHeap()
        assert str(heap) == "MaxHeap: []"


class TestMaxHeapEdgeCases:
    """Test MaxHeap edge cases."""

    def test_negative_numbers(self) -> None:
        """Test heap with negative numbers."""
        heap = MaxHeap([0, -5, 5, -3, 3])
        assert heap.peek() == 5
        extracted = []
        while not heap.is_empty():
            extracted.append(heap.extract())
        assert extracted == [5, 3, 0, -3, -5]

    def test_string_values(self) -> None:
        """Test heap with string values."""
        heap = MaxHeap(["dog", "cat", "elephant", "ant"])
        assert heap.peek() == "elephant"
