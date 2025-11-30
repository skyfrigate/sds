"""Tests for Queue from sds.linear.queue module."""

import re

import pytest

from sds.core.exceptions import EmptyStructureError
from sds.core.interfaces import LinearCollection
from sds.linear.queue import Queue


@pytest.fixture
def empty_queue():
    """Provide an empty Queue."""
    return Queue()


@pytest.fixture
def populated_queue():
    """Provide a Queue with elements [1, 2, 3] (1 at front)."""
    queue = Queue()
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)
    return queue


class TestQueueCreation:
    """Tests for Queue creation and initialization."""

    def test_queue_creation(self):
        """Test creating an empty Queue."""
        queue = Queue()

        assert isinstance(queue, Queue)
        assert isinstance(queue, LinearCollection)

    def test_initial_state(self, empty_queue):
        """Test the initial state of an empty Queue."""
        assert empty_queue.is_empty() is True
        assert len(empty_queue) == 0
        assert empty_queue.size == 0

    def test_add_element(self, empty_queue):
        """Test adding an element to the queue."""
        empty_queue.add(1)
        empty_queue.add(2)
        empty_queue.add(3)
        assert empty_queue.size == 3
        assert list(empty_queue) == [1, 2, 3]

    def test_remove_element(self, populated_queue):
        """Test removing an element from the queue."""
        populated_queue.remove(3)
        assert populated_queue.size == 2
        assert list(populated_queue) == [1, 2]
        populated_queue.remove(2)
        populated_queue.remove(1)
        assert populated_queue.size == 0
        assert list(populated_queue) == []

    @pytest.mark.parametrize(
        "q_name, index, exc, exc_msg",
        [
            ("empty_queue", 2, EmptyStructureError, "Cannot remove from empty list"),
            ("populated_queue", (1, 2), ValueError, "Item (1, 2) not found in list"),
        ],
    )
    def test_remove_failed(self, q_name, index, exc, exc_msg, request):
        queue = request.getfixturevalue(q_name)
        """Test removing all elements from the queue."""
        with pytest.raises(exc, match=re.escape(exc_msg)):
            queue.remove(index)


class TestQueueProperties:
    """Tests for Queue properties."""

    def test_size_property(self, populated_queue):
        """Test the size property."""
        assert populated_queue.size == 3

        populated_queue.enqueue(4)
        assert populated_queue.size == 4

        populated_queue.dequeue()
        assert populated_queue.size == 3

    def test_size_is_read_only(self, empty_queue):
        """Test that size property cannot be set directly."""
        with pytest.raises(AttributeError):
            empty_queue.size = 10


class TestQueueEnqueue:
    """Tests for Queue enqueue operation."""

    def test_enqueue_to_empty_queue(self, empty_queue):
        """Test enqueuing to an empty queue."""
        empty_queue.enqueue(1)

        assert len(empty_queue) == 1
        assert empty_queue.front() == 1

    def test_enqueue_multiple_items(self, empty_queue):
        """Test enqueuing multiple items."""
        empty_queue.enqueue(1)
        empty_queue.enqueue(2)
        empty_queue.enqueue(3)

        assert len(empty_queue) == 3
        assert empty_queue.front() == 1

    def test_enqueue_order_fifo(self, empty_queue):
        """Test that enqueue follows FIFO order."""
        empty_queue.enqueue(1)
        empty_queue.enqueue(2)
        empty_queue.enqueue(3)

        assert list(empty_queue) == [1, 2, 3]


class TestQueueDequeue:
    """Tests for Queue dequeue operation."""

    def test_dequeue_from_single_element(self, empty_queue):
        """Test dequeuing from a single-element queue."""
        empty_queue.enqueue(1)

        item = empty_queue.dequeue()

        assert item == 1
        assert empty_queue.is_empty()

    def test_dequeue_multiple_times(self, populated_queue):
        """Test dequeuing multiple times follows FIFO."""
        assert populated_queue.dequeue() == 1
        assert populated_queue.dequeue() == 2
        assert populated_queue.dequeue() == 3
        assert populated_queue.is_empty()

    def test_dequeue_from_empty_queue(self, empty_queue):
        """Test that dequeuing from empty queue raises error."""
        with pytest.raises(EmptyStructureError):
            empty_queue.dequeue()

    def test_enqueue_dequeue_alternating(self, empty_queue):
        """Test alternating enqueue and dequeue operations."""
        empty_queue.enqueue(1)
        assert empty_queue.dequeue() == 1

        empty_queue.enqueue(2)
        empty_queue.enqueue(3)
        assert empty_queue.dequeue() == 2
        assert empty_queue.dequeue() == 3


class TestQueueFront:
    """Tests for Queue front operation."""

    def test_front_at_first(self, populated_queue):
        """Test viewing the front element."""
        assert populated_queue.front() == 1
        assert len(populated_queue) == 3  # front doesn't remove

    def test_front_empty_queue(self, empty_queue):
        """Test that front on empty queue raises error."""
        with pytest.raises(EmptyStructureError):
            empty_queue.front()

    def test_front_after_operations(self, empty_queue):
        """Test front after various operations."""
        empty_queue.enqueue(1)
        assert empty_queue.front() == 1

        empty_queue.enqueue(2)
        assert empty_queue.front() == 1  # Still first

        empty_queue.dequeue()
        assert empty_queue.front() == 2


class TestQueueRear:
    """Tests for Queue rear operation."""

    def test_rear_at_last(self, populated_queue):
        """Test viewing the rear element."""
        assert populated_queue.rear() == 3
        assert len(populated_queue) == 3  # rear doesn't remove

    def test_rear_empty_queue(self, empty_queue):
        """Test that rear on empty queue raises error."""
        with pytest.raises(EmptyStructureError):
            empty_queue.rear()

    def test_rear_after_operations(self, empty_queue):
        """Test rear after various operations."""
        empty_queue.enqueue(1)
        assert empty_queue.rear() == 1

        empty_queue.enqueue(2)
        assert empty_queue.rear() == 2

        empty_queue.enqueue(3)
        assert empty_queue.rear() == 3

    def test_clear_populated_queue(self, populated_queue):
        """Test clearing a populated queue."""
        populated_queue.clear()

        assert populated_queue.is_empty()
        assert len(populated_queue) == 0

    def test_clear_empty_queue(self, empty_queue):
        """Test clearing an already empty queue."""
        empty_queue.clear()

        assert empty_queue.is_empty()


class TestQueueIteration:
    """Tests for Queue iteration."""

    def test_iterate_over_queue(self, populated_queue):
        """Test iterating over the queue (front to rear)."""
        result = []
        for item in populated_queue:
            result.append(item)

        assert result == [1, 2, 3]

    def test_list_conversion(self, populated_queue):
        """Test converting to Python list."""
        assert list(populated_queue) == [1, 2, 3]

    def test_iterate_empty_queue(self, empty_queue):
        """Test iterating over empty queue."""
        result = list(empty_queue)

        assert result == []

    def test_iteration_does_not_modify_queue(self, populated_queue):
        """Test that iteration doesn't modify the queue."""
        original_size = len(populated_queue)

        list(populated_queue)

        assert len(populated_queue) == original_size


class TestQueueContains:
    """Tests for Queue membership testing."""

    def test_contains_existing_item(self, populated_queue):
        """Test membership for existing items."""
        assert 1 in populated_queue
        assert 2 in populated_queue
        assert 3 in populated_queue

    def test_contains_nonexistent_item(self, populated_queue):
        """Test membership for non-existent items."""
        assert 999 not in populated_queue
        assert 0 not in populated_queue

    def test_contains_empty_queue(self, empty_queue):
        """Test membership in empty queue."""
        assert 1 not in empty_queue


class TestQueueStringRepresentation:
    """Tests for Queue string representations."""

    def test_repr(self, populated_queue):
        """Test __repr__ method."""
        result = repr(populated_queue)

        assert result == "Queue([1, 2, 3])"

    def test_str(self, populated_queue):
        """Test __str__ method."""
        result = str(populated_queue)

        assert result == "Queue (front to rear): [1 <- 2 <- 3]"

    def test_repr_empty_queue(self, empty_queue):
        """Test __repr__ for empty queue."""
        assert repr(empty_queue) == "Queue([])"

    def test_str_empty_queue(self, empty_queue):
        """Test __str__ for empty queue."""
        assert str(empty_queue) == "Queue: []"


class TestQueueFifoProperty:
    """Tests to verify FIFO property of Queue."""

    def test_fifo_order_maintained(self, empty_queue):
        """Test that FIFO order is maintained through operations."""
        # Enqueue items
        for i in range(10):
            empty_queue.enqueue(i)

        # Dequeue all and verify order
        dequeued = []
        while not empty_queue.is_empty():
            dequeued.append(empty_queue.dequeue())

        assert dequeued == list(range(10))

    def test_front_shows_first_enqueued(self, empty_queue):
        """Test that front always shows the first enqueued item."""
        empty_queue.enqueue(1)
        assert empty_queue.front() == 1

        empty_queue.enqueue(2)
        assert empty_queue.front() == 1  # Still first

        empty_queue.enqueue(3)
        assert empty_queue.front() == 1  # Still first


class TestQueueWithVariousDataTypes:
    """Tests for Queue with various data types."""

    def test_with_strings(self, empty_queue):
        """Test queue with strings."""
        empty_queue.enqueue("hello")
        empty_queue.enqueue("world")

        assert empty_queue.dequeue() == "hello"
        assert empty_queue.dequeue() == "world"

    def test_with_mixed_types(self, empty_queue):
        """Test queue with mixed data types."""
        empty_queue.enqueue(1)
        empty_queue.enqueue("hello")
        empty_queue.enqueue(3.14)
        empty_queue.enqueue([1, 2, 3])

        assert empty_queue.dequeue() == 1
        assert empty_queue.dequeue() == "hello"
        assert empty_queue.dequeue() == 3.14
        assert empty_queue.dequeue() == [1, 2, 3]


class TestQueueUseCases:
    """Tests demonstrating typical queue use cases."""

    def test_task_scheduling(self, empty_queue):
        """Test using queue for task scheduling."""
        tasks = ["task1", "task2", "task3"]

        # Add tasks to queue
        for task in tasks:
            empty_queue.enqueue(task)

        # Process tasks in order
        processed = []
        while not empty_queue.is_empty():
            processed.append(empty_queue.dequeue())

        assert processed == tasks

    def test_breadth_first_traversal(self, empty_queue):
        """Test using queue for BFS-like traversal."""
        # Simulate tree level-order traversal
        empty_queue.enqueue(1)

        visited = []
        while not empty_queue.is_empty():
            node = empty_queue.dequeue()
            visited.append(node)

            # Simulate adding children
            if node == 1:
                empty_queue.enqueue(2)
                empty_queue.enqueue(3)

        assert visited == [1, 2, 3]
