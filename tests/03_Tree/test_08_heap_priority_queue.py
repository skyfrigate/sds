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
from sds.tree.heap import HeapPriorityQueue, MaxHeap, MinHeap

# =============================================================================
# HeapPriorityQueue Tests
# =============================================================================


class TestHeapPriorityQueueCreation:
    """Test HeapPriorityQueue creation."""

    def test_create_empty_priority_queue(self) -> None:
        """Test creating empty priority queue."""
        pq = HeapPriorityQueue()
        assert pq.is_empty()
        assert len(pq) == 0

    def test_priority_queue_bool(self) -> None:
        """Test boolean evaluation."""
        pq = HeapPriorityQueue()
        assert not pq
        pq.enqueue("task", 1)
        assert pq


class TestHeapPriorityQueueEnqueue:
    """Test HeapPriorityQueue enqueue operations."""

    def test_enqueue_single_item(self) -> None:
        """Test enqueuing single item."""
        pq = HeapPriorityQueue()
        pq.enqueue("task1", 5)
        assert len(pq) == 1

    def test_enqueue_multiple_items(self) -> None:
        """Test enqueuing multiple items."""
        pq = HeapPriorityQueue()
        pq.enqueue("low", 10)
        pq.enqueue("high", 1)
        pq.enqueue("medium", 5)
        assert len(pq) == 3

    def test_enqueue_maintains_priority_order(self) -> None:
        """Test that highest priority is always accessible."""
        pq = HeapPriorityQueue()
        pq.enqueue("low", 10)
        pq.enqueue("high", 1)
        pq.enqueue("medium", 5)
        item, priority = pq.peek()
        assert item == "high"
        assert priority == 1


class TestHeapPriorityQueueDequeue:
    """Test HeapPriorityQueue dequeue operations."""

    def test_dequeue_from_empty_queue(self) -> None:
        """Test dequeuing from empty queue."""
        pq = HeapPriorityQueue()
        with pytest.raises(EmptyStructureError):
            pq.dequeue()

    def test_dequeue_single_item(self) -> None:
        """Test dequeuing single item."""
        pq = HeapPriorityQueue()
        pq.enqueue("task", 5)
        item, priority = pq.dequeue()
        assert item == "task"
        assert priority == 5
        assert pq.is_empty()

    def test_dequeue_by_priority(self) -> None:
        """Test that items are dequeued in priority order."""
        pq = HeapPriorityQueue()
        pq.enqueue("task1", 5)
        pq.enqueue("task2", 1)
        pq.enqueue("task3", 10)
        pq.enqueue("task4", 3)

        items = []
        while not pq.is_empty():
            item, priority = pq.dequeue()
            items.append((item, priority))

        # Check priorities are in ascending order
        priorities = [p for _, p in items]
        assert priorities == [1, 3, 5, 10]

    def test_dequeue_same_priority(self) -> None:
        """Test dequeuing items with same priority."""
        pq = HeapPriorityQueue()
        pq.enqueue("task1", 5)
        pq.enqueue("task2", 5)
        pq.enqueue("task3", 5)

        for _ in range(3):
            item, priority = pq.dequeue()
            assert priority == 5


class TestHeapPriorityQueuePeek:
    """Test HeapPriorityQueue peek operations."""

    def test_peek_empty_queue(self) -> None:
        """Test peeking at empty queue."""
        pq = HeapPriorityQueue()
        with pytest.raises(EmptyStructureError):
            pq.peek()

    def test_peek_returns_highest_priority(self) -> None:
        """Test that peek returns highest priority item."""
        pq = HeapPriorityQueue()
        pq.enqueue("low", 10)
        pq.enqueue("high", 1)
        pq.enqueue("medium", 5)
        item, priority = pq.peek()
        assert item == "high"
        assert priority == 1

    def test_peek_does_not_remove(self) -> None:
        """Test that peek does not remove item."""
        pq = HeapPriorityQueue()
        pq.enqueue("task", 5)
        first = pq.peek()
        second = pq.peek()
        assert first == second
        assert len(pq) == 1


class TestHeapPriorityQueueClear:
    """Test HeapPriorityQueue clear operation."""

    def test_clear_empty_queue(self) -> None:
        """Test clearing empty queue."""
        pq = HeapPriorityQueue()
        pq.clear()
        assert pq.is_empty()

    def test_clear_non_empty_queue(self) -> None:
        """Test clearing non-empty queue."""
        pq = HeapPriorityQueue()
        pq.enqueue("task1", 5)
        pq.enqueue("task2", 3)
        pq.clear()
        assert pq.is_empty()
        assert len(pq) == 0

    def test_queue_usable_after_clear(self) -> None:
        """Test that queue is usable after clear."""
        pq = HeapPriorityQueue()
        pq.enqueue("task1", 5)
        pq.clear()
        pq.enqueue("task2", 3)
        assert len(pq) == 1


class TestHeapPriorityQueueIteration:
    """Test HeapPriorityQueue iteration."""

    def test_iter_empty_queue(self) -> None:
        """Test iterating over empty queue."""
        pq = HeapPriorityQueue()
        assert list(pq) == []

    def test_iter_non_empty_queue(self) -> None:
        """Test iterating over non-empty queue."""
        pq = HeapPriorityQueue()
        pq.enqueue("task1", 5)
        pq.enqueue("task2", 3)
        items = list(pq)
        assert len(items) == 2

    def test_contains(self) -> None:
        """Test __contains__ method."""
        pq = HeapPriorityQueue()
        pq.enqueue("task1", 5)
        pq.enqueue("task2", 3)
        assert "task1" in pq
        assert "task2" in pq
        assert "task3" not in pq


class TestHeapPriorityQueueStringRepresentation:
    """Test HeapPriorityQueue string representations."""

    def test_repr_empty_queue(self) -> None:
        """Test repr of empty queue."""
        pq = HeapPriorityQueue()
        assert repr(pq) == "HeapPriorityQueue(size=0)"

    def test_repr_non_empty_queue(self) -> None:
        """Test repr of non-empty queue."""
        pq = HeapPriorityQueue()
        pq.enqueue("task", 5)
        assert repr(pq) == "HeapPriorityQueue(size=1)"

    def test_str_empty_queue(self) -> None:
        """Test str of empty queue."""
        pq = HeapPriorityQueue()
        assert str(pq) == "HeapPriorityQueue: []"


class TestHeapPriorityQueueEdgeCases:
    """Test HeapPriorityQueue edge cases."""

    def test_negative_priorities(self) -> None:
        """Test with negative priorities."""
        pq = HeapPriorityQueue()
        pq.enqueue("task1", -5)
        pq.enqueue("task2", -10)
        pq.enqueue("task3", 0)
        item, priority = pq.dequeue()
        assert priority == -10

    def test_float_priorities(self) -> None:
        """Test with float priorities."""
        pq = HeapPriorityQueue()
        pq.enqueue("task1", 5.5)
        pq.enqueue("task2", 3.2)
        pq.enqueue("task3", 7.1)
        item, priority = pq.dequeue()
        assert priority == 3.2

    def test_string_priorities(self) -> None:
        """Test with string priorities (lexicographic order)."""
        pq = HeapPriorityQueue()
        pq.enqueue("task1", "high")
        pq.enqueue("task2", "low")
        pq.enqueue("task3", "medium")
        item, priority = pq.dequeue()
        assert priority == "high"

    def test_large_queue(self) -> None:
        """Test with large number of items."""
        pq = HeapPriorityQueue()
        n = 1000
        import random

        priorities = list(range(n))
        random.shuffle(priorities)
        for i, p in enumerate(priorities):
            pq.enqueue(f"task{i}", p)
        assert len(pq) == n

        # Verify items come out in priority order
        previous_priority = -1
        while not pq.is_empty():
            _, priority = pq.dequeue()
            assert priority >= previous_priority
            previous_priority = priority


class TestHeapPriorityQueueRealWorldScenarios:
    """Test HeapPriorityQueue with real-world scenarios."""

    def test_task_scheduling(self) -> None:
        """Test priority queue for task scheduling."""
        pq = HeapPriorityQueue()
        pq.enqueue("Send email", 3)
        pq.enqueue("Critical bug fix", 1)
        pq.enqueue("Documentation", 5)
        pq.enqueue("Code review", 2)

        # Process tasks in priority order
        tasks = []
        while not pq.is_empty():
            task, _ = pq.dequeue()
            tasks.append(task)

        assert tasks[0] == "Critical bug fix"
        assert tasks[1] == "Code review"
        assert tasks[2] == "Send email"
        assert tasks[3] == "Documentation"

    def test_emergency_room_triage(self) -> None:
        """Test priority queue for emergency room triage."""
        pq = HeapPriorityQueue()
        pq.enqueue("Patient A - Minor cut", 5)
        pq.enqueue("Patient B - Heart attack", 1)
        pq.enqueue("Patient C - Broken arm", 3)
        pq.enqueue("Patient D - Critical", 1)

        # First two should be critical patients
        patient1, priority1 = pq.dequeue()
        patient2, priority2 = pq.dequeue()
        assert priority1 == 1
        assert priority2 == 1


class TestHeapComparison:
    """Compare MinHeap and MaxHeap behaviors."""

    def test_min_max_opposite_order(self) -> None:
        """Test that min and max heaps give opposite orders."""
        values = [5, 3, 7, 1, 9, 4]
        min_heap = MinHeap(values.copy())
        max_heap = MaxHeap(values.copy())

        min_extracted = []
        max_extracted = []

        while not min_heap.is_empty():
            min_extracted.append(min_heap.extract())
        while not max_heap.is_empty():
            max_extracted.append(max_heap.extract())

        assert min_extracted == sorted(values)
        assert max_extracted == sorted(values, reverse=True)

    def test_same_elements_different_peek(self) -> None:
        """Test that min and max heaps have different peek values."""
        values = [5, 3, 7, 1, 9]
        min_heap = MinHeap(values)
        max_heap = MaxHeap(values)

        assert min_heap.peek() == 1
        assert max_heap.peek() == 9
