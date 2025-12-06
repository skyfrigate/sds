"""Tests for DoublyLinkedList from sds.linear.list module."""

import pytest

from sds.core.exceptions import (
    EmptyStructureError,
)
from sds.core.exceptions import IndexStructureError as SDSIndexError
from sds.linear.interfaces import AbstractLinkedList
from sds.linear.list import DoublyLinkedList


class TestDoublyLinkedListCreation:
    """Tests for DoublyLinkedList creation and initialization."""

    def test_doubly_linked_list_creation(self):
        """Test creating an empty DoublyLinkedList."""
        dll = DoublyLinkedList()

        assert isinstance(dll, DoublyLinkedList)
        assert isinstance(dll, AbstractLinkedList)

    def test_initial_state(self, empty_doubly_linked_list):
        """Test the initial state of an empty DoublyLinkedList using fixture."""
        assert empty_doubly_linked_list.is_empty() is True
        assert len(empty_doubly_linked_list) == 0
        assert empty_doubly_linked_list.size == 0
        assert empty_doubly_linked_list.head is None
        assert empty_doubly_linked_list.tail is None

    def test_head_property_is_read_only(self, empty_doubly_linked_list):
        """Test that head property cannot be set directly."""
        with pytest.raises(AttributeError):
            empty_doubly_linked_list.head = None

    def test_tail_property_is_read_only(self, empty_doubly_linked_list):
        """Test that tail property cannot be set directly."""
        with pytest.raises(AttributeError):
            empty_doubly_linked_list.tail = None


class TestDoublyLinkedListProperties:
    """Tests for DoublyLinkedList properties."""

    def test_head_property_with_elements(self, populated_doubly_linked_list):
        """Test that head property returns the first node."""
        assert populated_doubly_linked_list.head is not None
        assert populated_doubly_linked_list.head.data == 1

    def test_tail_property_with_elements(self, populated_doubly_linked_list):
        """Test that tail property returns the last node."""
        assert populated_doubly_linked_list.tail is not None
        assert populated_doubly_linked_list.tail.data == 5

    def test_head_and_tail_same_for_single_element(self, empty_doubly_linked_list):
        """Test that head and tail are the same for single element."""
        empty_doubly_linked_list.append(1)

        assert empty_doubly_linked_list.head is empty_doubly_linked_list.tail
        assert empty_doubly_linked_list.head.data == 1

    def test_size_property(self, populated_doubly_linked_list):
        """Test the size property."""
        assert populated_doubly_linked_list.size == 5

        populated_doubly_linked_list.append(6)
        assert populated_doubly_linked_list.size == 6

        populated_doubly_linked_list.remove_first()
        assert populated_doubly_linked_list.size == 5

    def test_size_is_read_only(self, empty_doubly_linked_list):
        """Test that size property cannot be set directly."""
        with pytest.raises(AttributeError):
            empty_doubly_linked_list.size = 10


class TestDoublyLinkedListAppend:
    """Tests for DoublyLinkedList append operation."""

    def test_append_to_empty_list(self, empty_doubly_linked_list):
        """Test appending to an empty list."""
        empty_doubly_linked_list.append(1)

        assert len(empty_doubly_linked_list) == 1
        assert empty_doubly_linked_list.head.data == 1
        assert empty_doubly_linked_list.tail.data == 1
        assert empty_doubly_linked_list.head.next is None
        assert empty_doubly_linked_list.head.prev is None

    def test_append_multiple_items(self, empty_doubly_linked_list):
        """Test appending multiple items."""
        for i in range(1, 6):
            empty_doubly_linked_list.append(i)

        assert len(empty_doubly_linked_list) == 5
        assert list(empty_doubly_linked_list) == [1, 2, 3, 4, 5]

    def test_append_updates_tail(self, populated_doubly_linked_list):
        """Test that append correctly updates the tail."""
        old_tail = populated_doubly_linked_list.tail

        populated_doubly_linked_list.append(6)

        assert populated_doubly_linked_list.tail.data == 6
        assert populated_doubly_linked_list.tail.prev is old_tail
        assert old_tail.next is populated_doubly_linked_list.tail

    def test_append_various_types(self, empty_doubly_linked_list, sample_values):
        """Test appending various data types using fixture."""
        for val in sample_values:
            empty_doubly_linked_list.append(val)

        assert len(empty_doubly_linked_list) == len(sample_values)
        assert list(empty_doubly_linked_list) == sample_values


class TestDoublyLinkedListPrepend:
    """Tests for DoublyLinkedList prepend operation."""

    def test_prepend_to_empty_list(self, empty_doubly_linked_list):
        """Test prepending to an empty list."""
        empty_doubly_linked_list.prepend(1)

        assert len(empty_doubly_linked_list) == 1
        assert empty_doubly_linked_list.head.data == 1
        assert empty_doubly_linked_list.tail.data == 1

    def test_prepend_multiple_items(self, empty_doubly_linked_list):
        """Test prepending multiple items."""
        for i in range(1, 6):
            empty_doubly_linked_list.prepend(i)

        assert len(empty_doubly_linked_list) == 5
        assert list(empty_doubly_linked_list) == [5, 4, 3, 2, 1]

    def test_prepend_updates_head(self, populated_doubly_linked_list):
        """Test that prepend correctly updates the head."""
        old_head = populated_doubly_linked_list.head

        populated_doubly_linked_list.prepend(0)

        assert populated_doubly_linked_list.head.data == 0
        assert populated_doubly_linked_list.head.next is old_head
        assert old_head.prev is populated_doubly_linked_list.head


class TestDoublyLinkedListInsertAt:
    """Tests for DoublyLinkedList insert_at operation."""

    def test_insert_at_beginning(self, populated_doubly_linked_list):
        """Test inserting at the beginning (index 0)."""
        populated_doubly_linked_list.insert_at(0, 0)

        assert list(populated_doubly_linked_list) == [0, 1, 2, 3, 4, 5]
        assert populated_doubly_linked_list.head.data == 0

    def test_insert_at_end(self, populated_doubly_linked_list):
        """Test inserting at the end."""
        populated_doubly_linked_list.insert_at(5, 6)

        assert list(populated_doubly_linked_list) == [1, 2, 3, 4, 5, 6]
        assert populated_doubly_linked_list.tail.data == 6

    def test_insert_at_middle(self, populated_doubly_linked_list):
        """Test inserting in the middle."""
        populated_doubly_linked_list.insert_at(2, 2.5)

        assert list(populated_doubly_linked_list) == [1, 2, 2.5, 3, 4, 5]

    def test_insert_at_maintains_bidirectional_links(
        self, populated_doubly_linked_list
    ):
        """Test that insert_at maintains proper prev/next links."""
        populated_doubly_linked_list.insert_at(2, 2.5)

        # Verify forward links
        current = populated_doubly_linked_list.head
        values_forward = []
        while current is not None:
            values_forward.append(current.data)
            current = current.next

        # Verify backward links
        current = populated_doubly_linked_list.tail
        values_backward = []
        while current is not None:
            values_backward.append(current.data)
            current = current.prev

        assert values_forward == [1, 2, 2.5, 3, 4, 5]
        assert values_backward == [5, 4, 3, 2.5, 2, 1]

    def test_insert_at_negative_index(self, populated_doubly_linked_list):
        """Test inserting with negative index."""
        populated_doubly_linked_list.insert_at(-1, 4.5)

        # -1 should insert before the last element
        assert list(populated_doubly_linked_list) == [1, 2, 3, 4, 4.5, 5]

    def test_insert_at_invalid_index(self, populated_doubly_linked_list):
        """Test inserting at an invalid index."""
        with pytest.raises(SDSIndexError):
            populated_doubly_linked_list.insert_at(10, 999)

        with pytest.raises(SDSIndexError):
            populated_doubly_linked_list.insert_at(-10, 999)


class TestDoublyLinkedListRemoveFirst:
    """Tests for DoublyLinkedList remove_first operation."""

    def test_remove_first_from_single_element(self, empty_doubly_linked_list):
        """Test removing the first element from a single-element list."""
        empty_doubly_linked_list.append(1)

        item = empty_doubly_linked_list.remove_first()

        assert item == 1
        assert empty_doubly_linked_list.is_empty()
        assert empty_doubly_linked_list.head is None
        assert empty_doubly_linked_list.tail is None

    def test_remove_first_multiple_times(self, populated_doubly_linked_list):
        """Test removing first element multiple times."""
        assert populated_doubly_linked_list.remove_first() == 1
        assert populated_doubly_linked_list.remove_first() == 2
        assert populated_doubly_linked_list.remove_first() == 3

        assert list(populated_doubly_linked_list) == [4, 5]

    def test_remove_first_updates_prev_link(self, populated_doubly_linked_list):
        """Test that remove_first properly updates prev link of new head."""
        populated_doubly_linked_list.remove_first()

        assert populated_doubly_linked_list.head.prev is None

    def test_remove_first_from_empty_list(self, empty_doubly_linked_list):
        """Test removing from empty list raises error."""
        with pytest.raises(EmptyStructureError):
            empty_doubly_linked_list.remove_first()


class TestDoublyLinkedListRemoveLast:
    """Tests for DoublyLinkedList remove_last operation."""

    def test_remove_last_from_single_element(self, empty_doubly_linked_list):
        """Test removing the last element from a single-element list."""
        empty_doubly_linked_list.append(1)

        item = empty_doubly_linked_list.remove_last()

        assert item == 1
        assert empty_doubly_linked_list.is_empty()
        assert empty_doubly_linked_list.head is None
        assert empty_doubly_linked_list.tail is None

    def test_remove_last_multiple_times(self, populated_doubly_linked_list):
        """Test removing last element multiple times."""
        assert populated_doubly_linked_list.remove_last() == 5
        assert populated_doubly_linked_list.remove_last() == 4
        assert populated_doubly_linked_list.remove_last() == 3

        assert list(populated_doubly_linked_list) == [1, 2]

    def test_remove_last_updates_next_link(self, populated_doubly_linked_list):
        """Test that remove_last properly updates next link of new tail."""
        populated_doubly_linked_list.remove_last()

        assert populated_doubly_linked_list.tail.next is None

    def test_remove_last_from_empty_list(self, empty_doubly_linked_list):
        """Test removing from empty list raises error."""
        with pytest.raises(EmptyStructureError):
            empty_doubly_linked_list.remove_last()


class TestDoublyLinkedListRemove:
    """Tests for DoublyLinkedList remove (by value) operation."""

    def test_remove_existing_item(self, populated_doubly_linked_list):
        """Test removing an existing item."""
        item = populated_doubly_linked_list.remove(3)

        assert item == 3
        assert list(populated_doubly_linked_list) == [1, 2, 4, 5]

    def test_remove_first_item(self, populated_doubly_linked_list):
        """Test removing the first item."""
        item = populated_doubly_linked_list.remove(1)

        assert item == 1
        assert list(populated_doubly_linked_list) == [2, 3, 4, 5]
        assert populated_doubly_linked_list.head.prev is None

    def test_remove_last_item(self, populated_doubly_linked_list):
        """Test removing the last item."""
        item = populated_doubly_linked_list.remove(5)

        assert item == 5
        assert list(populated_doubly_linked_list) == [1, 2, 3, 4]
        assert populated_doubly_linked_list.tail.next is None

    def test_remove_maintains_bidirectional_links(self, populated_doubly_linked_list):
        """Test that remove maintains proper prev/next links."""
        populated_doubly_linked_list.remove(3)

        # Verify forward and backward traversal
        assert list(populated_doubly_linked_list) == [1, 2, 4, 5]
        assert list(reversed(populated_doubly_linked_list)) == [5, 4, 2, 1]

    def test_remove_nonexistent_item(self, populated_doubly_linked_list):
        """Test removing a non-existent item raises error."""
        with pytest.raises(ValueError):
            populated_doubly_linked_list.remove(999)

    def test_remove_from_empty_list(self, empty_doubly_linked_list):
        """Test removing from empty list raises error."""
        with pytest.raises(EmptyStructureError):
            empty_doubly_linked_list.remove(1)


class TestDoublyLinkedListRemoveAt:
    """Tests for DoublyLinkedList remove_at operation."""

    def test_remove_at_beginning(self, populated_doubly_linked_list):
        """Test removing at the beginning."""
        item = populated_doubly_linked_list.remove_at(0)

        assert item == 1
        assert list(populated_doubly_linked_list) == [2, 3, 4, 5]
        assert populated_doubly_linked_list.head.prev is None

    def test_remove_at_end(self, populated_doubly_linked_list):
        """Test removing at the end."""
        item = populated_doubly_linked_list.remove_at(4)

        assert item == 5
        assert list(populated_doubly_linked_list) == [1, 2, 3, 4]
        assert populated_doubly_linked_list.tail.next is None

    def test_remove_at_middle(self, populated_doubly_linked_list):
        """Test removing in the middle."""
        item = populated_doubly_linked_list.remove_at(2)

        assert item == 3
        assert list(populated_doubly_linked_list) == [1, 2, 4, 5]

    def test_remove_at_negative_index(self, populated_doubly_linked_list):
        """Test removing with negative index."""
        item = populated_doubly_linked_list.remove_at(-1)

        assert item == 5
        assert list(populated_doubly_linked_list) == [1, 2, 3, 4]

    def test_remove_at_invalid_index(self, populated_doubly_linked_list):
        """Test removing at invalid index raises error."""
        with pytest.raises(SDSIndexError):
            populated_doubly_linked_list.remove_at(10)

        with pytest.raises(SDSIndexError):
            populated_doubly_linked_list.remove_at(-10)

    def test_remove_at_from_empty_list(self, empty_doubly_linked_list):
        """Test removing from empty list raises error."""
        with pytest.raises(EmptyStructureError):
            empty_doubly_linked_list.remove_at(0)


class TestDoublyLinkedListFind:
    """Tests for DoublyLinkedList find operation."""

    def test_find_existing_item(self, populated_doubly_linked_list):
        """Test finding an existing item."""
        assert populated_doubly_linked_list.find(1) == 0
        assert populated_doubly_linked_list.find(3) == 2
        assert populated_doubly_linked_list.find(5) == 4

    def test_find_nonexistent_item(self, populated_doubly_linked_list):
        """Test finding a non-existent item returns -1."""
        assert populated_doubly_linked_list.find(999) == -1

    def test_find_in_empty_list(self, empty_doubly_linked_list):
        """Test finding in empty list returns -1."""
        assert empty_doubly_linked_list.find(1) == -1


class TestDoublyLinkedListIndexing:
    """Tests for DoublyLinkedList indexing operations."""

    def test_getitem_positive_index(self, populated_doubly_linked_list):
        """Test getting items with positive indices."""
        assert populated_doubly_linked_list[0] == 1
        assert populated_doubly_linked_list[2] == 3
        assert populated_doubly_linked_list[4] == 5

    def test_getitem_negative_index(self, populated_doubly_linked_list):
        """Test getting items with negative indices."""
        assert populated_doubly_linked_list[-1] == 5
        assert populated_doubly_linked_list[-3] == 3
        assert populated_doubly_linked_list[-5] == 1

    def test_getitem_optimization(self, populated_doubly_linked_list):
        """Test that getitem optimizes by starting from nearest end.

        This is a behavioral test - we verify it works correctly,
        though the optimization itself is internal.
        """
        # Access near beginning (should start from head)
        assert populated_doubly_linked_list[1] == 2

        # Access near end (should start from tail)
        assert populated_doubly_linked_list[3] == 4
        assert populated_doubly_linked_list[-2] == 4

    def test_getitem_invalid_index(self, populated_doubly_linked_list):
        """Test getting item at invalid index raises error."""
        with pytest.raises(SDSIndexError):
            _ = populated_doubly_linked_list[10]

        with pytest.raises(SDSIndexError):
            _ = populated_doubly_linked_list[-10]

    def test_getitem_from_empty_list(self, empty_doubly_linked_list):
        """Test getting from empty list raises error."""
        with pytest.raises(SDSIndexError):
            _ = empty_doubly_linked_list[0]

    def test_setitem_positive_index(self, populated_doubly_linked_list):
        """Test setting items with positive indices."""
        populated_doubly_linked_list[0] = 100
        populated_doubly_linked_list[2] = 300

        assert list(populated_doubly_linked_list) == [100, 2, 300, 4, 5]

    def test_setitem_negative_index(self, populated_doubly_linked_list):
        """Test setting items with negative indices."""
        populated_doubly_linked_list[-1] = 500
        populated_doubly_linked_list[-3] = 300

        assert list(populated_doubly_linked_list) == [1, 2, 300, 4, 500]

    def test_setitem_invalid_index(self, populated_doubly_linked_list):
        """Test setting item at invalid index raises error."""
        with pytest.raises(SDSIndexError):
            populated_doubly_linked_list[10] = 999

        with pytest.raises(SDSIndexError):
            populated_doubly_linked_list[-10] = 999


class TestDoublyLinkedListReverse:
    """Tests for DoublyLinkedList reverse operation."""

    def test_reverse_populated_list(self, populated_doubly_linked_list):
        """Test reversing a populated list."""
        populated_doubly_linked_list.reverse()

        assert list(populated_doubly_linked_list) == [5, 4, 3, 2, 1]

    def test_reverse_maintains_bidirectional_links(self, populated_doubly_linked_list):
        """Test that reverse maintains proper prev/next links."""
        populated_doubly_linked_list.reverse()

        # Verify forward traversal
        assert list(populated_doubly_linked_list) == [5, 4, 3, 2, 1]

        # Verify backward traversal
        assert list(reversed(populated_doubly_linked_list)) == [1, 2, 3, 4, 5]

    def test_reverse_updates_head_and_tail(self, populated_doubly_linked_list):
        """Test that reverse correctly swaps head and tail."""
        old_head = populated_doubly_linked_list.head
        old_tail = populated_doubly_linked_list.tail

        populated_doubly_linked_list.reverse()

        assert populated_doubly_linked_list.head is old_tail
        assert populated_doubly_linked_list.tail is old_head

    def test_reverse_single_element(self, empty_doubly_linked_list):
        """Test reversing a single-element list."""
        empty_doubly_linked_list.append(1)
        empty_doubly_linked_list.reverse()

        assert list(empty_doubly_linked_list) == [1]

    def test_reverse_empty_list(self, empty_doubly_linked_list):
        """Test reversing an empty list."""

        assert empty_doubly_linked_list.reverse() is None
        assert empty_doubly_linked_list.is_empty()

    def test_reverse_twice(self, populated_doubly_linked_list):
        """Test that reversing twice returns to original order."""
        original = list(populated_doubly_linked_list)

        populated_doubly_linked_list.reverse()
        populated_doubly_linked_list.reverse()

        assert list(populated_doubly_linked_list) == original


class TestDoublyLinkedListIteration:
    """Tests for DoublyLinkedList iteration."""

    def test_forward_iteration(self, populated_doubly_linked_list):
        """Test forward iteration over the list."""
        result = []
        for item in populated_doubly_linked_list:
            result.append(item)

        assert result == [1, 2, 3, 4, 5]

    def test_backward_iteration(self, populated_doubly_linked_list):
        """Test backward iteration using reversed()."""
        result = []
        for item in reversed(populated_doubly_linked_list):
            result.append(item)

        assert result == [5, 4, 3, 2, 1]

    def test_list_conversion(self, populated_doubly_linked_list):
        """Test converting to Python list."""
        assert list(populated_doubly_linked_list) == [1, 2, 3, 4, 5]

    def test_reversed_list_conversion(self, populated_doubly_linked_list):
        """Test converting reversed iterator to Python list."""
        assert list(reversed(populated_doubly_linked_list)) == [5, 4, 3, 2, 1]

    def test_iterate_empty_list(self, empty_doubly_linked_list):
        """Test iterating over empty list."""
        assert list(empty_doubly_linked_list) == []
        assert list(reversed(empty_doubly_linked_list)) == []


class TestDoublyLinkedListContains:
    """Tests for DoublyLinkedList membership testing."""

    def test_contains_existing_item(self, populated_doubly_linked_list):
        """Test membership for existing items."""
        assert 1 in populated_doubly_linked_list
        assert 3 in populated_doubly_linked_list
        assert 5 in populated_doubly_linked_list

    def test_contains_nonexistent_item(self, populated_doubly_linked_list):
        """Test membership for non-existent items."""
        assert 999 not in populated_doubly_linked_list
        assert 0 not in populated_doubly_linked_list

    def test_contains_empty_list(self, empty_doubly_linked_list):
        """Test membership in empty list."""
        assert 1 not in empty_doubly_linked_list


class TestDoublyLinkedListClear:
    """Tests for DoublyLinkedList clear operation."""

    def test_clear_populated_list(self, populated_doubly_linked_list):
        """Test clearing a populated list."""
        populated_doubly_linked_list.clear()

        assert populated_doubly_linked_list.is_empty()
        assert len(populated_doubly_linked_list) == 0
        assert populated_doubly_linked_list.head is None
        assert populated_doubly_linked_list.tail is None

    def test_clear_doubly_linked_list_attribute(self, populated_doubly_linked_list):
        populated_doubly_linked_list.clear()

        assert populated_doubly_linked_list.size == 0
        assert populated_doubly_linked_list._size == 0
        assert populated_doubly_linked_list._tail is None

    def test_clear_empty_list(self, empty_doubly_linked_list):
        """Test clearing an already empty list."""
        empty_doubly_linked_list.clear()

        assert empty_doubly_linked_list.is_empty()


class TestDoublyLinkedListStringRepresentation:
    """Tests for DoublyLinkedList string representations."""

    def test_repr(self, populated_doubly_linked_list):
        """Test __repr__ method."""
        result = repr(populated_doubly_linked_list)

        assert result == "DoublyLinkedList([1, 2, 3, 4, 5])"

    def test_str(self, populated_doubly_linked_list):
        """Test __str__ method."""
        result = str(populated_doubly_linked_list)

        assert result == "[1 <-> 2 <-> 3 <-> 4 <-> 5]"

    def test_repr_empty_list(self, empty_doubly_linked_list):
        """Test __repr__ for empty list."""
        assert repr(empty_doubly_linked_list) == "DoublyLinkedList([])"

    def test_str_empty_list(self, empty_doubly_linked_list):
        """Test __str__ for empty list."""
        assert str(empty_doubly_linked_list) == "[]"


class TestDoublyLinkedListWithVariousData:
    """Tests for DoublyLinkedList with various data types."""

    def test_with_different_data_types(self, empty_doubly_linked_list, list_data):
        """Test DoublyLinkedList with various data using parametrized fixture."""
        for item in list_data:
            empty_doubly_linked_list.append(item)

        assert len(empty_doubly_linked_list) == len(list_data)
        assert list(empty_doubly_linked_list) == list_data
        assert list(reversed(empty_doubly_linked_list)) == list(reversed(list_data))


class TestDoublyLinkedListBidirectionalIntegrity:
    """Tests to verify bidirectional link integrity."""

    def test_forward_backward_consistency(self, populated_doubly_linked_list):
        """Test that forward and backward traversals are consistent."""
        forward = list(populated_doubly_linked_list)
        backward = list(reversed(populated_doubly_linked_list))

        assert forward == list(reversed(backward))

    def test_all_nodes_have_proper_links(self, populated_doubly_linked_list):
        """Test that all nodes have proper prev/next links."""
        current = populated_doubly_linked_list.head

        # Check that first node has no prev
        assert current.prev is None

        # Check all middle nodes
        while current.next is not None:
            assert current.next.prev is current
            current = current.next

        # Check that last node has no next and is tail
        assert current.next is None
        assert current is populated_doubly_linked_list.tail

    def test_operations_maintain_link_integrity(self, empty_doubly_linked_list):
        """Test that various operations maintain link integrity."""
        # Build list
        for i in range(1, 6):
            empty_doubly_linked_list.append(i)

        # Perform various operations
        empty_doubly_linked_list.prepend(0)
        empty_doubly_linked_list.insert_at(3, 2.5)
        empty_doubly_linked_list.remove(2.5)
        empty_doubly_linked_list.remove_at(0)

        # Verify integrity
        forward = list(empty_doubly_linked_list)
        backward = list(reversed(empty_doubly_linked_list))

        assert forward == list(reversed(backward))


class TestLinkedListVsDoublyLinkedList:
    """Comparison tests between LinkedList and DoublyLinkedList."""

    def test_both_implement_same_interface(self, list_class):
        """Test that both list types implement AbstractLinkedList using fixture."""
        lst = list_class()
        assert isinstance(lst, AbstractLinkedList)

    def test_both_produce_same_results(self, list_class):
        """Test that both produce same results for common operations."""
        lst = list_class()

        # Build list
        for i in range(1, 6):
            lst.append(i)

        # Test common operations
        assert len(lst) == 5
        assert list(lst) == [1, 2, 3, 4, 5]
        assert lst[0] == 1
        assert lst[-1] == 5
        assert 3 in lst
        assert lst.find(3) == 2

        # Modify
        lst.prepend(0)
        lst.insert_at(3, 2.5)

        assert list(lst) == [0, 1, 2, 2.5, 3, 4, 5]

        # Remove
        lst.remove_first()
        lst.remove_last()
        lst.remove(2.5)

        assert list(lst) == [1, 2, 3, 4]

    def test_append_performance_difference(self):
        """Test that DoublyLinkedList append is O(1) vs LinkedList O(n).

        Note: This is a conceptual test - we just verify both work correctly.
        Actual performance testing would require timing measurements.
        """
        from sds.linear.list import DoublyLinkedList, LinkedList

        ll = LinkedList()
        dll = DoublyLinkedList()

        # Both should produce same results
        for i in range(100):
            ll.append(i)
            dll.append(i)

        assert list(ll) == list(dll)
        assert len(ll) == len(dll) == 100
