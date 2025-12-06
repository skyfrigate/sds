"""Tests for LinkedList from sds.linear.list module."""

import pytest

from sds.core.exceptions import (
    EmptyStructureError,
)
from sds.core.exceptions import IndexStructureError as SDSIndexError
from sds.linear.interfaces import AbstractLinkedList
from sds.linear.list import LinkedList


class TestLinkedListCreation:
    """Tests for LinkedList creation and initialization."""

    def test_linked_list_creation(self):
        """Test creating an empty LinkedList."""
        lst = LinkedList()

        assert isinstance(lst, LinkedList)
        assert isinstance(lst, AbstractLinkedList)

    def test_initial_state(self, empty_linked_list):
        """Test the initial state of an empty LinkedList using fixture."""
        assert empty_linked_list.is_empty() is True
        assert len(empty_linked_list) == 0
        assert empty_linked_list.size == 0
        assert empty_linked_list.head is None

    def test_head_property_is_read_only(self, empty_linked_list):
        """Test that head property cannot be set directly."""
        with pytest.raises(AttributeError):
            empty_linked_list.head = None


class TestLinkedListProperties:
    """Tests for LinkedList properties."""

    def test_head_property_with_elements(self, populated_linked_list):
        """Test that head property returns the first node."""
        assert populated_linked_list.head is not None
        assert populated_linked_list.head.data == 1

    def test_size_property(self, populated_linked_list):
        """Test the size property."""
        assert populated_linked_list.size == 5

        populated_linked_list.append(6)
        assert populated_linked_list.size == 6

        populated_linked_list.remove_first()
        assert populated_linked_list.size == 5

    def test_size_is_read_only(self, empty_linked_list):
        """Test that size property cannot be set directly."""
        with pytest.raises(AttributeError):
            empty_linked_list.size = 10


class TestLinkedListAppend:
    """Tests for LinkedList append operation."""

    def test_append_to_empty_list(self, empty_linked_list):
        """Test appending to an empty list."""
        empty_linked_list.append(1)

        assert len(empty_linked_list) == 1
        assert empty_linked_list.head.data == 1
        assert empty_linked_list.head.next is None

    def test_append_multiple_items(self, empty_linked_list):
        """Test appending multiple items."""
        for i in range(1, 6):
            empty_linked_list.append(i)

        assert len(empty_linked_list) == 5
        assert list(empty_linked_list) == [1, 2, 3, 4, 5]

    def test_append_various_types(self, empty_linked_list, sample_values):
        """Test appending various data types using fixture."""
        for val in sample_values:
            empty_linked_list.append(val)

        assert len(empty_linked_list) == len(sample_values)
        assert list(empty_linked_list) == sample_values


class TestLinkedListPrepend:
    """Tests for LinkedList prepend operation."""

    def test_prepend_to_empty_list(self, empty_linked_list):
        """Test prepending to an empty list."""
        empty_linked_list.prepend(1)

        assert len(empty_linked_list) == 1
        assert empty_linked_list.head.data == 1

    def test_prepend_multiple_items(self, empty_linked_list):
        """Test prepending multiple items."""
        for i in range(1, 6):
            empty_linked_list.prepend(i)

        assert len(empty_linked_list) == 5
        assert list(empty_linked_list) == [5, 4, 3, 2, 1]

    def test_prepend_updates_head(self, populated_linked_list):
        """Test that prepend correctly updates the head."""
        old_head = populated_linked_list.head

        populated_linked_list.prepend(0)

        assert populated_linked_list.head.data == 0
        assert populated_linked_list.head.next is old_head


class TestLinkedListInsertAt:
    """Tests for LinkedList insert_at operation."""

    def test_insert_at_beginning(self, populated_linked_list):
        """Test inserting at the beginning (index 0)."""
        populated_linked_list.insert_at(0, 0)

        assert list(populated_linked_list) == [0, 1, 2, 3, 4, 5]

    def test_insert_at_end(self, populated_linked_list):
        """Test inserting at the end."""
        populated_linked_list.insert_at(5, 6)

        assert list(populated_linked_list) == [1, 2, 3, 4, 5, 6]

    def test_insert_at_middle(self, populated_linked_list):
        """Test inserting in the middle."""
        populated_linked_list.insert_at(2, 2.5)

        assert list(populated_linked_list) == [1, 2, 2.5, 3, 4, 5]

    def test_insert_at_negative_index(self, populated_linked_list):
        """Test inserting with negative index."""
        populated_linked_list.insert_at(-1, 4.5)

        # -1 should insert before the last element
        assert list(populated_linked_list) == [1, 2, 3, 4, 4.5, 5]

    def test_insert_at_invalid_index(self, populated_linked_list):
        """Test inserting at an invalid index."""
        with pytest.raises(SDSIndexError):
            populated_linked_list.insert_at(10, 999)

        with pytest.raises(SDSIndexError):
            populated_linked_list.insert_at(-10, 999)


class TestLinkedListRemoveFirst:
    """Tests for LinkedList remove_first operation."""

    def test_remove_first_from_single_element(self, empty_linked_list):
        """Test removing the first element from a single-element list."""
        empty_linked_list.append(1)

        item = empty_linked_list.remove_first()

        assert item == 1
        assert empty_linked_list.is_empty()

    def test_remove_first_multiple_times(self, populated_linked_list):
        """Test removing first element multiple times."""
        assert populated_linked_list.remove_first() == 1
        assert populated_linked_list.remove_first() == 2
        assert populated_linked_list.remove_first() == 3

        assert list(populated_linked_list) == [4, 5]

    def test_remove_first_from_empty_list(self, empty_linked_list):
        """Test removing from empty list raises error."""
        with pytest.raises(EmptyStructureError):
            empty_linked_list.remove_first()


class TestLinkedListRemoveLast:
    """Tests for LinkedList remove_last operation."""

    def test_remove_last_from_single_element(self, empty_linked_list):
        """Test removing the last element from a single-element list."""
        empty_linked_list.append(1)

        item = empty_linked_list.remove_last()

        assert item == 1
        assert empty_linked_list.is_empty()

    def test_remove_last_multiple_times(self, populated_linked_list):
        """Test removing last element multiple times."""
        assert populated_linked_list.remove_last() == 5
        assert populated_linked_list.remove_last() == 4
        assert populated_linked_list.remove_last() == 3

        assert list(populated_linked_list) == [1, 2]

    def test_remove_last_from_empty_list(self, empty_linked_list):
        """Test removing from empty list raises error."""
        with pytest.raises(EmptyStructureError):
            empty_linked_list.remove_last()


class TestLinkedListRemove:
    """Tests for LinkedList remove (by value) operation."""

    def test_remove_existing_item(self, populated_linked_list):
        """Test removing an existing item."""
        item = populated_linked_list.remove(3)

        assert item == 3
        assert list(populated_linked_list) == [1, 2, 4, 5]

    def test_remove_first_item(self, populated_linked_list):
        """Test removing the first item."""
        item = populated_linked_list.remove(1)

        assert item == 1
        assert list(populated_linked_list) == [2, 3, 4, 5]

    def test_remove_last_item(self, populated_linked_list):
        """Test removing the last item."""
        item = populated_linked_list.remove(5)

        assert item == 5
        assert list(populated_linked_list) == [1, 2, 3, 4]

    def test_remove_nonexistent_item(self, populated_linked_list):
        """Test removing a non-existent item raises error."""
        with pytest.raises(ValueError):
            populated_linked_list.remove(999)

    def test_remove_from_empty_list(self, empty_linked_list):
        """Test removing from empty list raises error."""
        with pytest.raises(EmptyStructureError):
            empty_linked_list.remove(1)


class TestLinkedListRemoveAt:
    """Tests for LinkedList remove_at operation."""

    def test_remove_at_beginning(self, populated_linked_list):
        """Test removing at the beginning."""
        item = populated_linked_list.remove_at(0)

        assert item == 1
        assert list(populated_linked_list) == [2, 3, 4, 5]

    def test_remove_at_end(self, populated_linked_list):
        """Test removing at the end."""
        item = populated_linked_list.remove_at(4)

        assert item == 5
        assert list(populated_linked_list) == [1, 2, 3, 4]

    def test_remove_at_middle(self, populated_linked_list):
        """Test removing in the middle."""
        item = populated_linked_list.remove_at(2)

        assert item == 3
        assert list(populated_linked_list) == [1, 2, 4, 5]

    def test_remove_at_negative_index(self, populated_linked_list):
        """Test removing with negative index."""
        item = populated_linked_list.remove_at(-1)

        assert item == 5
        assert list(populated_linked_list) == [1, 2, 3, 4]

    def test_remove_at_invalid_index(self, populated_linked_list):
        """Test removing at invalid index raises error."""
        with pytest.raises(SDSIndexError):
            populated_linked_list.remove_at(10)

        with pytest.raises(SDSIndexError):
            populated_linked_list.remove_at(-10)

    def test_remove_at_from_empty_list(self, empty_linked_list):
        """Test removing from empty list raises error."""
        with pytest.raises(EmptyStructureError):
            empty_linked_list.remove_at(0)


class TestLinkedListFind:
    """Tests for LinkedList find operation."""

    def test_find_existing_item(self, populated_linked_list):
        """Test finding an existing item."""
        assert populated_linked_list.find(1) == 0
        assert populated_linked_list.find(3) == 2
        assert populated_linked_list.find(5) == 4

    def test_find_nonexistent_item(self, populated_linked_list):
        """Test finding a non-existent item returns -1."""
        assert populated_linked_list.find(999) == -1

    def test_find_in_empty_list(self, empty_linked_list):
        """Test finding in empty list returns -1."""
        assert empty_linked_list.find(1) == -1


class TestLinkedListIndexing:
    """Tests for LinkedList indexing operations."""

    def test_getitem_positive_index(self, populated_linked_list):
        """Test getting items with positive indices."""
        assert populated_linked_list[0] == 1
        assert populated_linked_list[2] == 3
        assert populated_linked_list[4] == 5

    def test_getitem_negative_index(self, populated_linked_list):
        """Test getting items with negative indices."""
        assert populated_linked_list[-1] == 5
        assert populated_linked_list[-3] == 3
        assert populated_linked_list[-5] == 1

    def test_getitem_invalid_index(self, populated_linked_list):
        """Test getting item at invalid index raises error."""
        with pytest.raises(SDSIndexError):
            _ = populated_linked_list[10]

        with pytest.raises(SDSIndexError):
            _ = populated_linked_list[-10]

    def test_getitem_from_empty_list(self, empty_linked_list):
        """Test getting from empty list raises error."""
        with pytest.raises(SDSIndexError):
            _ = empty_linked_list[0]

    def test_setitem_positive_index(self, populated_linked_list):
        """Test setting items with positive indices."""
        populated_linked_list[0] = 100
        populated_linked_list[2] = 300

        assert list(populated_linked_list) == [100, 2, 300, 4, 5]

    def test_setitem_negative_index(self, populated_linked_list):
        """Test setting items with negative indices."""
        populated_linked_list[-1] = 500
        populated_linked_list[-3] = 300

        assert list(populated_linked_list) == [1, 2, 300, 4, 500]

    def test_setitem_invalid_index(self, populated_linked_list):
        """Test setting item at invalid index raises error."""
        with pytest.raises(SDSIndexError):
            populated_linked_list[10] = 999

        with pytest.raises(SDSIndexError):
            populated_linked_list[-10] = 999


class TestLinkedListReverse:
    """Tests for LinkedList reverse operation."""

    def test_reverse_populated_list(self, populated_linked_list):
        """Test reversing a populated list."""
        populated_linked_list.reverse()

        assert list(populated_linked_list) == [5, 4, 3, 2, 1]

    def test_reverse_single_element(self, empty_linked_list):
        """Test reversing a single-element list."""
        empty_linked_list.append(1)
        empty_linked_list.reverse()

        assert list(empty_linked_list) == [1]

    def test_reverse_empty_list(self, empty_linked_list):
        """Test reversing an empty list."""
        empty_linked_list.reverse()

        assert empty_linked_list.is_empty()

    def test_reverse_twice(self, populated_linked_list):
        """Test that reversing twice returns to original order."""
        original = list(populated_linked_list)

        populated_linked_list.reverse()
        populated_linked_list.reverse()

        assert list(populated_linked_list) == original


class TestLinkedListIteration:
    """Tests for LinkedList iteration."""

    def test_iterate_over_list(self, populated_linked_list):
        """Test iterating over the list."""
        result = []
        for item in populated_linked_list:
            result.append(item)

        assert result == [1, 2, 3, 4, 5]

    def test_list_conversion(self, populated_linked_list):
        """Test converting to Python list."""
        assert list(populated_linked_list) == [1, 2, 3, 4, 5]

    def test_iterate_empty_list(self, empty_linked_list):
        """Test iterating over empty list."""
        result = list(empty_linked_list)

        assert result == []


class TestLinkedListContains:
    """Tests for LinkedList membership testing."""

    def test_contains_existing_item(self, populated_linked_list):
        """Test membership for existing items."""
        assert 1 in populated_linked_list
        assert 3 in populated_linked_list
        assert 5 in populated_linked_list

    def test_contains_nonexistent_item(self, populated_linked_list):
        """Test membership for non-existent items."""
        assert 999 not in populated_linked_list
        assert 0 not in populated_linked_list

    def test_contains_empty_list(self, empty_linked_list):
        """Test membership in empty list."""
        assert 1 not in empty_linked_list


class TestLinkedListClear:
    """Tests for LinkedList clear operation."""

    def test_clear_populated_list(self, populated_linked_list):
        """Test clearing a populated list."""
        populated_linked_list.clear()

        assert populated_linked_list.is_empty()
        assert len(populated_linked_list) == 0
        assert populated_linked_list.head is None

    def test_clear_empty_list(self, empty_linked_list):
        """Test clearing an already empty list."""
        empty_linked_list.clear()

        assert empty_linked_list.is_empty()


class TestLinkedListStringRepresentation:
    """Tests for LinkedList string representations."""

    def test_repr(self, populated_linked_list):
        """Test __repr__ method."""
        result = repr(populated_linked_list)

        assert result == "LinkedList([1, 2, 3, 4, 5])"

    def test_str(self, populated_linked_list):
        """Test __str__ method."""
        result = str(populated_linked_list)

        assert result == "[1 -> 2 -> 3 -> 4 -> 5]"

    def test_repr_empty_list(self, empty_linked_list):
        """Test __repr__ for empty list."""
        assert repr(empty_linked_list) == "LinkedList([])"

    def test_str_empty_list(self, empty_linked_list):
        """Test __str__ for empty list."""
        assert str(empty_linked_list) == "[]"


class TestLinkedListWithVariousData:
    """Tests for LinkedList with various data types."""

    def test_with_different_data_types(self, empty_linked_list, list_data):
        """Test LinkedList with various data using parametrized fixture."""
        for item in list_data:
            empty_linked_list.append(item)

        assert len(empty_linked_list) == len(list_data)
        assert list(empty_linked_list) == list_data
