"""Tests for Deque from sds.linear.queue module."""

import pytest

from sds.core.exceptions import EmptyStructureError
from sds.core.interfaces import LinearCollection
from sds.linear.queue import Deque


@pytest.fixture
def empty_deque():
    """Provide an empty Deque."""
    return Deque()


@pytest.fixture
def populated_deque():
    """Provide a Deque with elements [1, 2, 3]."""
    deque = Deque()
    deque.add_rear(1)
    deque.add_rear(2)
    deque.add_rear(3)
    return deque


class TestDequeCreation:
    """Tests for Deque creation and initialization."""

    def test_deque_creation(self):
        """Test creating an empty Deque."""
        deque = Deque()

        assert isinstance(deque, Deque)
        assert isinstance(deque, LinearCollection)

    def test_initial_state(self, empty_deque):
        """Test the initial state of an empty Deque."""
        assert empty_deque.is_empty() is True
        assert len(empty_deque) == 0
        assert empty_deque.size == 0

    def test_contains(self, populated_deque):
        """Test the contains() method of an empty Deque."""
        assert 2 in populated_deque


class TestDequeAddFront:
    """Tests for Deque add_front operation."""

    def test_add_front_to_empty(self, empty_deque):
        """Test adding to front of empty deque."""
        empty_deque.add_front(1)

        assert len(empty_deque) == 1
        assert empty_deque.peek_front() == 1
        assert empty_deque.peek_rear() == 1

    def test_add_front_multiple(self, empty_deque):
        """Test adding multiple items to front."""
        empty_deque.add_front(3)
        empty_deque.add_front(2)
        empty_deque.add_front(1)

        assert list(empty_deque) == [1, 2, 3]


class TestDequeAddRear:
    """Tests for Deque add_rear operation."""

    def test_add_rear_to_empty(self, empty_deque):
        """Test adding to rear of empty deque."""
        empty_deque.add_rear(1)

        assert len(empty_deque) == 1
        assert empty_deque.peek_front() == 1
        assert empty_deque.peek_rear() == 1

    def test_add_rear_multiple(self, empty_deque):
        """Test adding multiple items to rear."""
        empty_deque.add_rear(1)
        empty_deque.add_rear(2)
        empty_deque.add_rear(3)

        assert list(empty_deque) == [1, 2, 3]


class TestDequeRemoveFront:
    """Tests for Deque remove_front operation."""

    def test_remove_front_single_element(self, empty_deque):
        """Test removing front from single-element deque."""
        empty_deque.add_rear(1)

        item = empty_deque.remove_front()

        assert item == 1
        assert empty_deque.is_empty()

    def test_remove_front_multiple(self, populated_deque):
        """Test removing from front multiple times."""
        assert populated_deque.remove_front() == 1
        assert populated_deque.remove_front() == 2
        assert list(populated_deque) == [3]

    def test_remove_front_empty_raises(self, empty_deque):
        """Test removing from empty deque raises error."""
        with pytest.raises(EmptyStructureError):
            empty_deque.remove_front()


class TestDequeRemoveRear:
    """Tests for Deque remove_rear operation."""

    def test_remove_rear_single_element(self, empty_deque):
        """Test removing rear from single-element deque."""
        empty_deque.add_rear(1)

        item = empty_deque.remove_rear()

        assert item == 1
        assert empty_deque.is_empty()

    def test_remove_rear_multiple(self, populated_deque):
        """Test removing from rear multiple times."""
        assert populated_deque.remove_rear() == 3
        assert populated_deque.remove_rear() == 2
        assert list(populated_deque) == [1]

    def test_remove_rear_empty_raises(self, empty_deque):
        """Test removing from empty deque raises error."""
        with pytest.raises(EmptyStructureError):
            empty_deque.remove_rear()


class TestDequePeekFront:
    """Tests for Deque peek_front operation."""

    def test_peek_front(self, populated_deque):
        """Test peeking at front."""
        assert populated_deque.peek_front() == 1
        assert len(populated_deque) == 3

    def test_peek_front_empty_raises(self, empty_deque):
        """Test peeking at empty deque raises error."""
        with pytest.raises(EmptyStructureError):
            empty_deque.peek_front()


class TestDequePeekRear:
    """Tests for Deque peek_rear operation."""

    def test_peek_rear(self, populated_deque):
        """Test peeking at rear."""
        assert populated_deque.peek_rear() == 3
        assert len(populated_deque) == 3

    def test_peek_rear_empty_raises(self, empty_deque):
        """Test peeking at empty deque raises error."""
        with pytest.raises(EmptyStructureError):
            empty_deque.peek_rear()


class TestDequeReversedIteration:
    """Tests for Deque reversed iteration."""

    def test_reversed_iteration(self, populated_deque):
        """Test iterating in reverse."""
        assert list(reversed(populated_deque)) == [3, 2, 1]

    def test_forward_and_backward_consistent(self, populated_deque):
        """Test that forward and backward are consistent."""
        forward = list(populated_deque)
        backward = list(reversed(populated_deque))

        assert forward == list(reversed(backward))


class TestDequeClear:
    """Tests for Deque clear operation."""

    def test_clear(self, populated_deque):
        """Test clearing from deque."""
        populated_deque.clear()
        assert populated_deque.size == 0


class TestDequeAliases:
    """Tests for Deque method aliases."""

    def test_append_alias(self, empty_deque):
        """Test append as alias for add_rear."""
        empty_deque.append(1)
        assert empty_deque.peek_rear() == 1

    def test_appendleft_alias(self, empty_deque):
        """Test appendleft as alias for add_front."""
        empty_deque.appendleft(1)
        assert empty_deque.peek_front() == 1

    def test_pop_alias(self, populated_deque):
        """Test pop as alias for remove_rear."""
        item = populated_deque.pop()
        assert item == 3

    def test_popleft_alias(self, populated_deque):
        """Test popleft as alias for remove_front."""
        item = populated_deque.popleft()
        assert item == 1

    def test_add(self, empty_deque):
        """Test adding from deque."""
        empty_deque.add(1)
        empty_deque.add((1, 2))
        assert empty_deque.peek_front() == 1
        assert empty_deque.peek_rear() == (1, 2)

    def test_remove(self, populated_deque):
        """Test removing from deque."""
        populated_deque.remove(3)
        assert populated_deque.peek_front() == 1
        assert populated_deque.peek_rear() == 2


class TestDequeStringRepresentation:
    """Tests for Deque string representations."""

    def test_repr(self, populated_deque):
        """Test __repr__ method."""
        assert repr(populated_deque) == "Deque([1, 2, 3])"

    def test_str(self, populated_deque):
        """Test __str__ method."""
        assert str(populated_deque) == "Deque (front to rear): [1 <-> 2 <-> 3]"

    def test_repr_empty(self, empty_deque):
        """Test __repr__ for empty deque."""
        assert repr(empty_deque) == "Deque([])"

    def test_str_empty(self, empty_deque):
        """Test __str__ for empty deque."""
        assert str(empty_deque) == "Deque: []"


class TestDequeDoubleEndedProperty:
    """Tests to verify double-ended property of Deque."""

    def test_operations_at_both_ends(self, empty_deque):
        """Test that operations work correctly at both ends."""
        empty_deque.add_front(2)
        empty_deque.add_rear(3)
        empty_deque.add_front(1)
        empty_deque.add_rear(4)

        assert list(empty_deque) == [1, 2, 3, 4]

        assert empty_deque.remove_front() == 1
        assert empty_deque.remove_rear() == 4

        assert list(empty_deque) == [2, 3]


class TestDequeUseCases:
    """Tests demonstrating typical deque use cases."""

    def test_palindrome_checker(self, empty_deque):
        """Test using deque for palindrome checking."""
        word = "racecar"

        for char in word:
            empty_deque.add_rear(char)

        is_palindrome = True
        while len(empty_deque) > 1:
            if empty_deque.remove_front() != empty_deque.remove_rear():
                is_palindrome = False
                break

        assert is_palindrome is True

    def test_sliding_window(self, empty_deque):
        """Test using deque for sliding window."""
        data = [1, 2, 3, 4, 5]
        window_size = 3

        # Build initial window
        for i in range(window_size):
            empty_deque.add_rear(data[i])

        windows = [list(empty_deque)]

        # Slide window
        for i in range(window_size, len(data)):
            empty_deque.remove_front()
            empty_deque.add_rear(data[i])
            windows.append(list(empty_deque))

        assert windows == [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
