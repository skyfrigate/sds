"""Tests for PriorityQueue from sds.linear.queue module."""

import re

import pytest

from sds.core.exceptions import EmptyStructureError
from sds.core.interfaces import LinearCollection
from sds.linear.queue import PriorityItem, PriorityQueue


@pytest.fixture
def empty_priority_queue():
    """Provide an empty PriorityQueue."""
    return PriorityQueue()


@pytest.fixture
def populated_priority_queue():
    """Provide a PriorityQueue with elements [5, 1, 3]."""
    pq = PriorityQueue()
    pq.enqueue(5)
    pq.enqueue(1)
    pq.enqueue(3)
    return pq


class TestPriorityQueueCreation:
    """Tests for PriorityQueue creation and initialization."""

    def test_priority_queue_creation(self):
        """Test creating an empty PriorityQueue."""
        pq = PriorityQueue()

        assert isinstance(pq, PriorityQueue)
        assert isinstance(pq, LinearCollection)

    def test_initial_state(self, empty_priority_queue):
        """Test the initial state of an empty PriorityQueue."""
        assert empty_priority_queue.is_empty() is True
        assert len(empty_priority_queue) == 0
        assert empty_priority_queue.size == 0

    def test_creation_with_reverse(self):
        """Test creating with reverse=True (max-heap behavior)."""
        pq = PriorityQueue(reverse=True)
        pq.enqueue(1)
        pq.enqueue(5)
        pq.enqueue(3)

        assert pq.dequeue() == 5  # Highest value first

    def test_creation_with_key_function(self):
        """Test creating with custom key function."""
        pq = PriorityQueue(key=lambda x: -x)  # Negate for reverse order
        pq.enqueue(1)
        pq.enqueue(5)
        pq.enqueue(3)

        assert pq.dequeue() == 5

    def test_contains(self, populated_priority_queue):
        """Test the contains() method of an empty PriorityQueue."""
        assert 5 in populated_priority_queue
        assert 3 in populated_priority_queue
        assert 0 not in populated_priority_queue


class TestPriorityQueueEnqueue:
    """Tests for PriorityQueue enqueue operation."""

    def test_enqueue_to_empty(self, empty_priority_queue):
        """Test enqueuing to empty priority queue."""
        empty_priority_queue.enqueue(5)

        assert len(empty_priority_queue) == 1
        assert empty_priority_queue.peek() == 5

    def test_enqueue_maintains_priority_order(self, empty_priority_queue):
        """Test that enqueue maintains priority order."""
        empty_priority_queue.enqueue(5)
        empty_priority_queue.enqueue(1)
        empty_priority_queue.enqueue(3)
        empty_priority_queue.enqueue(2)

        assert list(empty_priority_queue) == [1, 2, 3, 5]

    def test_enqueue_same_priority(self, empty_priority_queue):
        """Test enqueuing items with same priority."""
        empty_priority_queue.enqueue(2)
        empty_priority_queue.enqueue(2)
        empty_priority_queue.enqueue(2)

        assert len(empty_priority_queue) == 3


class TestPriorityQueueDequeue:
    """Tests for PriorityQueue dequeue operation."""

    def test_dequeue_highest_priority(self, populated_priority_queue):
        """Test that dequeue returns highest priority (lowest value)."""
        assert populated_priority_queue.dequeue() == 1
        assert populated_priority_queue.dequeue() == 3
        assert populated_priority_queue.dequeue() == 5

    def test_dequeue_from_empty_raises(self, empty_priority_queue):
        """Test that dequeue from empty raises error."""
        with pytest.raises(EmptyStructureError):
            empty_priority_queue.dequeue()

    def test_dequeue_order(self, empty_priority_queue):
        """Test that items are dequeued in priority order."""
        values = [10, 3, 7, 1, 5, 9, 2]
        for val in values:
            empty_priority_queue.enqueue(val)

        dequeued = []
        while not empty_priority_queue.is_empty():
            dequeued.append(empty_priority_queue.dequeue())

        assert dequeued == sorted(values)


class TestPriorityQueuePeek:
    """Tests for PriorityQueue peek operation."""

    def test_peek_highest_priority(self, populated_priority_queue):
        """Test that peek returns highest priority without removing."""
        assert populated_priority_queue.peek() == 1
        assert len(populated_priority_queue) == 3

    def test_peek_empty_raises(self, empty_priority_queue):
        """Test that peek on empty queue raises error."""
        with pytest.raises(EmptyStructureError):
            empty_priority_queue.peek()


class TestPriorityQueueClear:
    """Tests for PriorityQueue clear operation."""

    def test_clear_(self, populated_priority_queue):
        populated_priority_queue.clear()
        assert len(populated_priority_queue) == 0
        assert list(populated_priority_queue) == []


class TestPriorityQueueAlaises:
    """Tests for PriorityQueue alaises operation."""

    def test_add(self, empty_priority_queue):
        """Test that adding items to empty priority queue."""
        empty_priority_queue.add(PriorityItem("Fix critical bug", 1))
        assert len(empty_priority_queue) == 1

    def test_remove(self, populated_priority_queue):
        """Test that removing items from empty priority queue."""
        populated_priority_queue.remove(1)
        assert len(populated_priority_queue) == 2
        populated_priority_queue.remove(5)
        assert len(populated_priority_queue) == 1

    @pytest.mark.parametrize(
        "list_name, index, exc, exc_msg",
        [
            (
                "empty_priority_queue",
                1,
                EmptyStructureError,
                "Cannot remove from empty priority queue",
            ),
            ("populated_priority_queue", 6, ValueError, "Item 6 not found in queue"),
        ],
    )
    def test_remove_failed(self, list_name, index, exc, exc_msg, request):
        """Test that removing failed items from empty priority queue."""
        list_obj = request.getfixturevalue(list_name)
        with pytest.raises(exc, match=re.escape(exc_msg)):
            list_obj.remove(index)


class TestPriorityQueueStringRepresentation:
    """Tests for PriorityQueue string representations."""

    def test_repr(self, populated_priority_queue):
        """Test __repr__ method."""
        assert repr(populated_priority_queue) == "PriorityQueue([1, 3, 5])"

    def test_str(self, populated_priority_queue):
        """Test __str__ method."""
        expected = "PriorityQueue (highest to lowest priority): [1 -> 3 -> 5]"
        assert str(populated_priority_queue) == expected

    def test_repr_empty(self, empty_priority_queue):
        """Test __repr__ for empty queue."""
        assert repr(empty_priority_queue) == "PriorityQueue([])"

    def test_str_empty(self, empty_priority_queue):
        """Test __str__ for empty queue."""
        assert str(empty_priority_queue) == "PriorityQueue: []"


class TestPriorityQueueWithPriorityItem:
    """Tests for PriorityQueue with PriorityItem helper class."""

    def test_priority_item_creation(self):
        """Test creating PriorityItem."""
        item = PriorityItem("Task 1", 5)

        assert item.data == "Task 1"
        assert item.priority == 5

    def test_enqueue_priority_items(self, empty_priority_queue):
        """Test enqueuing PriorityItems."""
        empty_priority_queue.enqueue(PriorityItem("Low", 10))
        empty_priority_queue.enqueue(PriorityItem("High", 1))
        empty_priority_queue.enqueue(PriorityItem("Medium", 5))

        first = empty_priority_queue.dequeue()
        assert first.data == "High"
        assert first.priority == 1


class TestPriorityQueueWithCustomKey:
    """Tests for PriorityQueue with custom key function."""

    def test_with_tuple_key(self):
        """Test with tuples and custom key."""
        pq = PriorityQueue(key=lambda x: x[1])

        pq.enqueue(("task1", 5))
        pq.enqueue(("task2", 1))
        pq.enqueue(("task3", 3))

        assert pq.dequeue() == ("task2", 1)
        assert pq.dequeue() == ("task3", 3)
        assert pq.dequeue() == ("task1", 5)

    def test_with_dict_key(self):
        """Test with dictionaries and custom key."""
        pq = PriorityQueue(key=lambda x: x["priority"])

        pq.enqueue({"name": "task1", "priority": 5})
        pq.enqueue({"name": "task2", "priority": 1})
        pq.enqueue({"name": "task3", "priority": 3})

        first = pq.dequeue()
        assert first["name"] == "task2"


class TestPriorityQueueMinHeapMaxHeap:
    """Tests to verify min-heap and max-heap behavior."""

    def test_min_heap_default(self):
        """Test that default behavior is min-heap (lower values = higher priority)."""
        pq = PriorityQueue()

        for val in [5, 2, 8, 1, 9]:
            pq.enqueue(val)

        assert pq.dequeue() == 1
        assert pq.dequeue() == 2

    def test_max_heap_with_reverse(self):
        """Test max-heap behavior with reverse=True."""
        pq = PriorityQueue(reverse=True)

        for val in [5, 2, 8, 1, 9]:
            pq.enqueue(val)

        assert pq.dequeue() == 9
        assert pq.dequeue() == 8


class TestPriorityQueueUseCases:
    """Tests demonstrating typical priority queue use cases."""

    def test_task_scheduling_by_priority(self, empty_priority_queue):
        """Test using priority queue for task scheduling."""
        tasks = [
            ("Check email", 3),
            ("Fix critical bug", 1),
            ("Write documentation", 5),
            ("Code review", 2),
        ]

        for name, priority in tasks:
            empty_priority_queue.enqueue(PriorityItem(name, priority))

        # Process tasks in priority order
        executed = []
        while not empty_priority_queue.is_empty():
            task = empty_priority_queue.dequeue()
            executed.append(task.data)

        assert executed == [
            "Fix critical bug",
            "Code review",
            "Check email",
            "Write documentation",
        ]

    def test_dijkstra_like_usage(self, empty_priority_queue):
        """Test using priority queue for Dijkstra-like algorithm."""
        # Simulate storing (distance, node) pairs
        pq = PriorityQueue(key=lambda x: x[0])

        pq.enqueue((0, "A"))
        pq.enqueue((10, "B"))
        pq.enqueue((5, "C"))
        pq.enqueue((3, "D"))

        visited = []
        while not pq.is_empty():
            distance, node = pq.dequeue()
            visited.append(node)

        assert visited == ["A", "D", "C", "B"]
