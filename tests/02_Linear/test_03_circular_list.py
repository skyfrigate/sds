"""Tests for CircularLinkedList from sds.linear.list module."""

import re

import pytest

from sds.core.exceptions import (
    EmptyStructureError,
)
from sds.core.exceptions import IndexStructureError as SDSIndexError
from sds.linear.interfaces import AbstractLinkedList
from sds.linear.list import CircularLinkedList


@pytest.fixture
def empty_circular_list():
    """Provide an empty CircularLinkedList."""
    return CircularLinkedList()


@pytest.fixture
def populated_circular_list():
    """Provide a CircularLinkedList with elements [1, 2, 3, 4, 5]."""
    cll = CircularLinkedList()
    for i in range(1, 6):
        cll.append(i)
    return cll


class TestCircularLinkedListCreation:
    """Tests for CircularLinkedList creation and initialization."""

    def test_circular_linked_list_creation(self):
        """Test creating an empty CircularLinkedList."""
        cll = CircularLinkedList()

        assert isinstance(cll, CircularLinkedList)
        assert isinstance(cll, AbstractLinkedList)

    def test_initial_state(self, empty_circular_list):
        """Test the initial state of an empty CircularLinkedList."""
        assert empty_circular_list.is_empty() is True
        assert len(empty_circular_list) == 0
        assert empty_circular_list.size == 0
        assert empty_circular_list.head is None
        assert empty_circular_list.tail is None

    def test_head_property_is_read_only(self, empty_circular_list):
        """Test that head property cannot be set directly."""
        with pytest.raises(AttributeError):
            empty_circular_list.head = None

    def test_tail_property_is_read_only(self, empty_circular_list):
        """Test that tail property cannot be set directly."""
        with pytest.raises(AttributeError):
            empty_circular_list.tail = None

    @pytest.mark.parametrize(
        "list_name, index, exc, exc_msg",
        [
            ("empty_circular_list", 0, SDSIndexError, "List is empty"),
            (
                "populated_circular_list",
                6,
                SDSIndexError,
                "Index 6 out of range for list of size 5",
            ),
        ],
    )
    def test_get_item_failed(
        self, empty_circular_list, list_name, index, exc, exc_msg, request
    ):
        list_obj = request.getfixturevalue(list_name)
        with pytest.raises(exc, match=re.escape(exc_msg)):
            f"{list_obj[index]}"

    def test_set_item(self, populated_circular_list):
        item = populated_circular_list[3]
        assert item == 4
        populated_circular_list[3] = 100
        assert list(populated_circular_list) == [1, 2, 3, 100, 5]

    def test_contains(self, populated_circular_list):
        assert 4 in populated_circular_list
        assert 6 not in populated_circular_list


class TestCircularLinkedListProperties:
    """Tests for CircularLinkedList properties."""

    def test_head_property_with_elements(self, populated_circular_list):
        """Test that head property returns the first node."""
        assert populated_circular_list.head is not None
        assert populated_circular_list.head.data == 1

    def test_tail_property_with_elements(self, populated_circular_list):
        """Test that tail property returns the last node."""
        assert populated_circular_list.tail is not None
        assert populated_circular_list.tail.data == 5

    def test_circular_structure(self, populated_circular_list):
        """Test that tail.next points back to head."""
        assert populated_circular_list.tail.next is populated_circular_list.head

    def test_head_equals_tail_next(self, populated_circular_list):
        """Test that head is accessible via tail.next."""
        assert populated_circular_list.head is populated_circular_list.tail.next

    def test_single_element_circular_structure(self, empty_circular_list):
        """Test circular structure with single element."""
        empty_circular_list.append(1)

        assert empty_circular_list.head is empty_circular_list.tail
        assert empty_circular_list.head.next is empty_circular_list.head


class TestCircularLinkedListClear:
    """Tests for CircularLinkedList clear."""

    def test_clear_populated_circular_list(self, populated_circular_list):
        populated_circular_list.clear()

        assert populated_circular_list.is_empty()
        assert len(populated_circular_list) == 0
        assert populated_circular_list.head is None
        assert populated_circular_list.tail is None
        assert populated_circular_list.size == 0

    def test_clear_populated_circular_list_attribute(self, populated_circular_list):
        populated_circular_list.clear()

        assert populated_circular_list._size == 0
        assert populated_circular_list._tail is None


class TestCircularLinkedListAppend:
    """Tests for CircularLinkedList append operation."""

    def test_append_to_empty_list(self, empty_circular_list):
        """Test appending to an empty list."""
        empty_circular_list.append(1)

        assert len(empty_circular_list) == 1
        assert empty_circular_list.head.data == 1
        assert empty_circular_list.tail.data == 1
        assert empty_circular_list.head.next is empty_circular_list.head

    def test_append_multiple_items(self, empty_circular_list):
        """Test appending multiple items."""
        for i in range(1, 6):
            empty_circular_list.append(i)

        assert len(empty_circular_list) == 5
        assert list(empty_circular_list) == [1, 2, 3, 4, 5]

    def test_append_maintains_circular_structure(self, populated_circular_list):
        """Test that append maintains circular structure."""
        populated_circular_list.append(6)

        assert populated_circular_list.tail.data == 6
        assert populated_circular_list.tail.next is populated_circular_list.head


class TestCircularLinkedListPrepend:
    """Tests for CircularLinkedList prepend operation."""

    def test_prepend_to_empty_list(self, empty_circular_list):
        """Test prepending to an empty list."""
        empty_circular_list.prepend(1)

        assert len(empty_circular_list) == 1
        assert empty_circular_list.head.data == 1
        assert empty_circular_list.head.next is empty_circular_list.head

    def test_prepend_multiple_items(self, empty_circular_list):
        """Test prepending multiple items."""
        for i in range(1, 6):
            empty_circular_list.prepend(i)

        assert len(empty_circular_list) == 5
        assert list(empty_circular_list) == [5, 4, 3, 2, 1]

    def test_prepend_maintains_circular_structure(self, populated_circular_list):
        """Test that prepend maintains circular structure."""
        populated_circular_list.prepend(0)

        assert populated_circular_list.head.data == 0
        assert populated_circular_list.tail.next is populated_circular_list.head


class TestCircularLinkedListInsert:
    """Tests for CircularLinkedList insert operation."""

    @pytest.mark.parametrize(
        "index, value, expected",
        [
            (0, 0, [0, 1, 2, 3, 4, 5]),
            (3, 3.5, [1, 2, 3, 3.5, 4, 5]),
            (-1, 4.5, [1, 2, 3, 4, 4.5, 5]),
            (-2, 3.5, [1, 2, 3, 3.5, 4, 5]),
            (5, 6, [1, 2, 3, 4, 5, 6]),
        ],
    )
    def test_insert_to_list(self, populated_circular_list, index, value, expected):
        """Test inserting an empty list."""
        populated_circular_list.insert_at(index, value)
        assert list(populated_circular_list) == expected

    @pytest.mark.parametrize(
        "list_name, index, exc, exc_msg",
        [
            (
                "empty_circular_list",
                1,
                SDSIndexError,
                "Index 1 out of range for insertion",
            ),
            (
                "populated_circular_list",
                -10,
                SDSIndexError,
                "Index -5 out of range for insertion",
            ),
        ],
    )
    def test_insert_list_failed(self, list_name, index, exc, exc_msg, request):
        """Test inserting an empty list."""
        list_obj = request.getfixturevalue(list_name)
        with pytest.raises(exc, match=re.escape(exc_msg)):
            list_obj.insert_at(index, exc)


class TestCircularLinkedListRotate:
    """Tests for CircularLinkedList rotate operation."""

    def test_rotate_forward_single_step(self, populated_circular_list):
        """Test rotating forward by one step."""
        populated_circular_list.rotate(1)

        assert list(populated_circular_list) == [2, 3, 4, 5, 1]

    def test_rotate_forward_multiple_steps(self, populated_circular_list):
        """Test rotating forward by multiple steps."""
        populated_circular_list.rotate(3)

        assert list(populated_circular_list) == [4, 5, 1, 2, 3]

    def test_rotate_backward_single_step(self, populated_circular_list):
        """Test rotating backward by one step."""
        populated_circular_list.rotate(-1)

        assert list(populated_circular_list) == [5, 1, 2, 3, 4]

    def test_rotate_backward_multiple_steps(self, populated_circular_list):
        """Test rotating backward by multiple steps."""
        populated_circular_list.rotate(-2)

        assert list(populated_circular_list) == [4, 5, 1, 2, 3]

    def test_rotate_by_size(self, populated_circular_list):
        """Test that rotating by size returns to same state."""
        original = list(populated_circular_list)

        populated_circular_list.rotate(5)

        assert list(populated_circular_list) == original

    def test_rotate_by_multiple_of_size(self, populated_circular_list):
        """Test rotating by multiples of size."""
        original = list(populated_circular_list)

        populated_circular_list.rotate(15)  # 3 * size

        assert list(populated_circular_list) == original

    def test_rotate_forward_then_backward(self, populated_circular_list):
        """Test that rotating forward then backward returns to original."""
        original = list(populated_circular_list)

        populated_circular_list.rotate(3)
        populated_circular_list.rotate(-3)

        assert list(populated_circular_list) == original

    def test_rotate_empty_list(self, empty_circular_list):
        """Test rotating an empty list does nothing."""
        empty_circular_list.rotate(5)

        assert empty_circular_list.is_empty()

    def test_rotate_single_element(self, empty_circular_list):
        """Test rotating a single-element list."""
        empty_circular_list.append(1)

        empty_circular_list.rotate(3)

        assert list(empty_circular_list) == [1]


class TestCircularLinkedListReverse:
    """Tests for CircularLinkedList rotation."""

    def test_reverse(self, populated_circular_list):
        assert list(populated_circular_list) == [1, 2, 3, 4, 5]
        populated_circular_list.reverse()
        assert list(populated_circular_list) == [5, 4, 3, 2, 1]

    def test_reverse_empty(self, empty_circular_list):
        assert empty_circular_list.reverse() is None


class TestCircularLinkedListRemoveOperations:
    """Tests for CircularLinkedList remove operations."""

    def test_remove_first(self, populated_circular_list):
        """Test removing first element."""
        item = populated_circular_list.remove_first()

        assert item == 1
        assert list(populated_circular_list) == [2, 3, 4, 5]
        assert populated_circular_list.tail.next is populated_circular_list.head

    def test_remove_first_failed(self, empty_circular_list):
        """Test removing first element."""
        with pytest.raises(EmptyStructureError, match="Cannot remove from empty list"):
            empty_circular_list.remove_first()

    def test_remove_last(self, populated_circular_list):
        """Test removing last element."""
        item = populated_circular_list.remove_last()

        assert item == 5
        assert list(populated_circular_list) == [1, 2, 3, 4]
        assert populated_circular_list.tail.next is populated_circular_list.head

        for i in range(1, 4):
            populated_circular_list.remove_last()

        assert list(populated_circular_list) == [1]

        populated_circular_list.remove_last()

        assert populated_circular_list.size == 0

    def test_remove_last_failed(self, empty_circular_list):
        """Test removing last element."""
        with pytest.raises(EmptyStructureError, match="Cannot remove from empty list"):
            empty_circular_list.remove_last()

    @pytest.mark.parametrize(
        "index, item, value_list",
        [
            (0, 1, [2, 3, 4, 5]),
            (1, 0, [1, 3, 4, 5]),
            (-1, 5, [1, 2, 3, 4]),
            (-2, 4, [1, 2, 3, 5]),
        ],
    )
    def test_remove_at(self, populated_circular_list, index, item, value_list):
        item = populated_circular_list.remove_at(index)

        assert item == item
        assert list(populated_circular_list) == value_list
        assert populated_circular_list.tail.next is populated_circular_list.head

    @pytest.mark.parametrize(
        "name_list, index, exc, exc_msg",
        [
            (
                "empty_circular_list",
                0,
                EmptyStructureError,
                "Cannot remove from empty list",
            ),
            ("populated_circular_list", 10, SDSIndexError, "Index 10 out of range"),
        ],
    )
    def test_remove_at_failed(self, name_list, index, exc, exc_msg, request):
        class_list = request.getfixturevalue(name_list)
        with pytest.raises(exc, match=exc_msg):
            class_list.remove_at(index)

    def test_remove_until_empty(self, populated_circular_list):
        """Test removing all elements."""
        while not populated_circular_list.is_empty():
            populated_circular_list.remove_first()

        assert populated_circular_list.is_empty()
        assert populated_circular_list.head is None
        assert populated_circular_list.tail is None

    @pytest.mark.parametrize(
        "item, value_list",
        [
            (1, [2, 3, 4, 5]),
            (2, [1, 3, 4, 5]),
            (3, [1, 2, 4, 5]),
            (4, [1, 2, 3, 5]),
            (5, [1, 2, 3, 4]),
        ],
    )
    def test_remove(self, populated_circular_list, item, value_list):
        populated_circular_list.remove(item)
        assert list(populated_circular_list) == value_list

    @pytest.mark.parametrize(
        "list_name, item, exc, exc_msg",
        [
            (
                "empty_circular_list",
                1,
                EmptyStructureError,
                "Cannot remove from empty list",
            ),
            (
                "populated_circular_list",
                (1, 2),
                ValueError,
                "Item (1, 2) not found in list",
            ),
        ],
    )
    def test_remove_failed(
        self, populated_circular_list, list_name, item, exc, exc_msg, request
    ):
        list_obj = request.getfixturevalue(list_name)
        with pytest.raises(exc, match=re.escape(exc_msg)):
            list_obj.remove(item)


class TestCircularLinkedListIteration:
    """Tests for CircularLinkedList iteration."""

    def test_iteration_stops_after_one_cycle(self, populated_circular_list):
        """Test that iteration stops after visiting all nodes once."""
        count = 0
        for _ in populated_circular_list:
            count += 1

        assert count == 5

    def test_multiple_iterations(self, populated_circular_list):
        """Test that multiple iterations work correctly."""
        first_pass = list(populated_circular_list)
        second_pass = list(populated_circular_list)

        assert first_pass == second_pass == [1, 2, 3, 4, 5]


class TestCircularLinkedListStringRepresentation:
    """Tests for CircularLinkedList string representations."""

    def test_str_representation(self, populated_circular_list):
        """Test __str__ method."""
        result = str(populated_circular_list)

        assert result == "[1 -> 2 -> 3 -> 4 -> 5 -> (circular)]"

    def test_repr_representation(self, populated_circular_list):
        """Test __repr__ method."""
        result = repr(populated_circular_list)

        assert result == "CircularLinkedList([1, 2, 3, 4, 5])"

    def test_str_empty_list(self, empty_circular_list):
        """Test __str__ for empty list."""
        assert str(empty_circular_list) == "[]"

    def test_repr_empty_list(self, empty_circular_list):
        """Test __repr__ for empty list."""
        assert repr(empty_circular_list) == "CircularLinkedList([])"


class TestCircularLinkedListAllOperations:
    """Integration tests for CircularLinkedList with all operations."""

    def test_comprehensive_operations(self, empty_circular_list):
        """Test a comprehensive sequence of operations."""
        # Build list
        for i in range(1, 6):
            empty_circular_list.append(i)

        # Verify circular structure
        assert empty_circular_list.tail.next is empty_circular_list.head

        # Rotate
        empty_circular_list.rotate(2)
        assert list(empty_circular_list) == [3, 4, 5, 1, 2]

        # Insert
        empty_circular_list.insert_at(2, 99)
        assert list(empty_circular_list) == [3, 4, 99, 5, 1, 2]

        # Remove
        empty_circular_list.remove(99)
        assert list(empty_circular_list) == [3, 4, 5, 1, 2]

        # Verify still circular
        assert empty_circular_list.tail.next is empty_circular_list.head

    @pytest.mark.parametrize(
        "list_name, item, expected",
        [
            ("empty_circular_list", 0, -1),
            ("populated_circular_list", 1, 0),
            ("populated_circular_list", 2, 1),
            ("populated_circular_list", 3, 2),
            ("populated_circular_list", 4, 3),
            ("populated_circular_list", 5, 4),
            ("populated_circular_list", 6, -1),
        ],
    )
    def test_comprehensive_find_operations(
        self, populated_circular_list, list_name, item, expected, request
    ):
        list_obj = request.getfixturevalue(list_name)
        assert list_obj.find(item) == expected
