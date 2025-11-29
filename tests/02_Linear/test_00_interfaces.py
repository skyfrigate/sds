from abc import ABC

import pytest

from sds.core.exceptions import EmptyStructureError
from sds.core.interfaces import LinearCollection
from sds.linear.interfaces import AbstractLinkedList


class TestAbstractLinkedList:
    """Tests for the AbstractLinkedList abstract base class."""

    def test_abstract_linked_list_is_abstract(self):
        """Test that AbstractLinkedList cannot be instantiated directly."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            AbstractLinkedList()

    def test_abstract_linked_list_is_abc(self):
        """Test that AbstractLinkedList is an ABC."""
        assert issubclass(AbstractLinkedList, ABC)

    def test_abstract_linked_list_extends_linear_collection(self):
        """Test that AbstractLinkedList extends LinearCollection."""
        assert issubclass(AbstractLinkedList, LinearCollection)

    def test_abstract_linked_list_has_required_abstract_methods(self):
        """Test that AbstractLinkedList defines all required abstract methods."""
        abstract_methods = AbstractLinkedList.__abstractmethods__

        # Should include all LinearCollection methods plus list-specific ones
        expected_methods = {
            # From Collection
            "__iter__",
            "__contains__",
            "clear",
            # From LinearCollection
            "remove",
            # From AbstractLinkedList
            "prepend",
            "append",
            "insert_at",
            "remove_first",
            "remove_last",
            "remove_at",
            "find",
            "reverse",
            "__getitem__",
            "__setitem__",
        }

        assert expected_methods.issubset(abstract_methods)

    def test_abstract_linked_list_size_property_exists(self):
        """Test that size property is defined."""
        assert hasattr(AbstractLinkedList, "size")
        assert isinstance(AbstractLinkedList.size, property)

    def test_abstract_linked_list_has_concrete_methods(self):
        """Test that AbstractLinkedList provides concrete implementations."""
        # These methods should be concrete (not abstract)
        concrete_methods = ["__len__", "is_empty", "add"]

        for method_name in concrete_methods:
            assert method_name not in AbstractLinkedList.__abstractmethods__
            assert hasattr(AbstractLinkedList, method_name)


class TestAbstractLinkedListInterface:
    """Tests for the interface contract of AbstractLinkedList."""

    @pytest.fixture
    def minimal_linked_list_class(self):
        """Provide a minimal concrete implementation of AbstractLinkedList."""

        class MinimalLinkedList(AbstractLinkedList):
            def __init__(self):
                super().__init__()
                self._items = []

            def clear(self):
                self._items.clear()
                self._size = 0

            def __iter__(self):
                return iter(self._items)

            def __contains__(self, item):
                return item in self._items

            def prepend(self, item):
                self._items.insert(0, item)
                self._size += 1

            def append(self, item):
                self._items.append(item)
                self._size += 1

            def insert_at(self, index, item):
                if index < 0:
                    index += self._size + 1
                if index < 0 or index > self._size:
                    raise IndexError("Index out of range")
                self._items.insert(index, item)
                self._size += 1

            def remove_first(self):
                if self.is_empty():
                    raise EmptyStructureError()
                self._size -= 1
                return self._items.pop(0)

            def remove_last(self):
                if self.is_empty():
                    raise EmptyStructureError()
                self._size -= 1
                return self._items.pop()

            def remove(self, item):
                if self.is_empty():
                    raise EmptyStructureError()
                self._items.remove(item)
                self._size -= 1
                return item

            def remove_at(self, index):
                if self.is_empty():
                    raise EmptyStructureError()
                if index < 0:
                    index += self._size
                if index < 0 or index >= self._size:
                    raise IndexError("Index out of range")
                self._size -= 1
                return self._items.pop(index)

            def find(self, item):
                try:
                    return self._items.index(item)
                except ValueError:
                    return -1

            def reverse(self):
                self._items.reverse()

            def __getitem__(self, index):
                return self._items[index]

            def __setitem__(self, index, value):
                self._items[index] = value

        return MinimalLinkedList

    def test_can_instantiate_concrete_implementation(self, minimal_linked_list_class):
        """Test that a complete concrete implementation can be instantiated."""
        lst = minimal_linked_list_class()
        assert isinstance(lst, AbstractLinkedList)
        assert isinstance(lst, LinearCollection)

    def test_size_property_works(self, minimal_linked_list_class):
        """Test that the size property works correctly."""
        lst = minimal_linked_list_class()

        assert lst.size == 0

        lst.append(1)
        assert lst.size == 1

        lst.append(2)
        assert lst.size == 2

        lst.remove_first()
        assert lst.size == 1

    def test_len_works(self, minimal_linked_list_class):
        """Test that __len__ works correctly."""
        lst = minimal_linked_list_class()

        assert len(lst) == 0

        lst.append(1)
        assert len(lst) == 1

        lst.append(2)
        assert len(lst) == 2

    def test_is_empty_works(self, minimal_linked_list_class):
        """Test that is_empty works correctly."""
        lst = minimal_linked_list_class()

        assert lst.is_empty() is True

        lst.append(1)
        assert lst.is_empty() is False

        lst.clear()
        assert lst.is_empty() is True

    def test_add_delegates_to_append(self, minimal_linked_list_class):
        """Test that add() delegates to append()."""
        lst = minimal_linked_list_class()

        lst.add(1)
        lst.add(2)

        assert list(lst) == [1, 2]

    def test_prepend_adds_to_beginning(self, minimal_linked_list_class):
        """Test that prepend adds items to the beginning."""
        lst = minimal_linked_list_class()

        lst.prepend(3)
        lst.prepend(2)
        lst.prepend(1)

        assert list(lst) == [1, 2, 3]

    def test_append_adds_to_end(self, minimal_linked_list_class):
        """Test that append adds items to the end."""
        lst = minimal_linked_list_class()

        lst.append(1)
        lst.append(2)
        lst.append(3)

        assert list(lst) == [1, 2, 3]

    def test_insert_at_works(self, minimal_linked_list_class):
        """Test that insert_at works correctly."""
        lst = minimal_linked_list_class()

        lst.append(1)
        lst.append(3)
        lst.insert_at(1, 2)

        assert list(lst) == [1, 2, 3]

    def test_remove_first_works(self, minimal_linked_list_class):
        """Test that remove_first works correctly."""
        lst = minimal_linked_list_class()

        lst.append(1)
        lst.append(2)
        lst.append(3)

        item = lst.remove_first()

        assert item == 1
        assert list(lst) == [2, 3]

    def test_remove_last_works(self, minimal_linked_list_class):
        """Test that remove_last works correctly."""
        lst = minimal_linked_list_class()

        lst.append(1)
        lst.append(2)
        lst.append(3)

        item = lst.remove_last()

        assert item == 3
        assert list(lst) == [1, 2]

    def test_remove_at_works(self, minimal_linked_list_class):
        """Test that remove_at works correctly."""
        lst = minimal_linked_list_class()

        lst.append(1)
        lst.append(2)
        lst.append(3)

        item = lst.remove_at(1)

        assert item == 2
        assert list(lst) == [1, 3]

    def test_find_works(self, minimal_linked_list_class):
        """Test that find works correctly."""
        lst = minimal_linked_list_class()

        lst.append(10)
        lst.append(20)
        lst.append(30)

        assert lst.find(20) == 1
        assert lst.find(99) == -1

    def test_reverse_works(self, minimal_linked_list_class):
        """Test that reverse works correctly."""
        lst = minimal_linked_list_class()

        lst.append(1)
        lst.append(2)
        lst.append(3)

        lst.reverse()

        assert list(lst) == [3, 2, 1]

    def test_getitem_works(self, minimal_linked_list_class):
        """Test that __getitem__ works correctly."""
        lst = minimal_linked_list_class()

        lst.append(10)
        lst.append(20)
        lst.append(30)

        assert lst[0] == 10
        assert lst[1] == 20
        assert lst[-1] == 30

    def test_setitem_works(self, minimal_linked_list_class):
        """Test that __setitem__ works correctly."""
        lst = minimal_linked_list_class()

        lst.append(10)
        lst.append(20)

        lst[0] = 100
        lst[1] = 200

        assert list(lst) == [100, 200]


class TestAbstractLinkedListContract:
    """Tests to verify the contract defined by AbstractLinkedList."""

    @pytest.fixture
    def list_class(self):
        """Provide a minimal implementation for contract testing."""

        class ContractTestList(AbstractLinkedList):
            def __init__(self):
                super().__init__()
                self._data = []

            def clear(self):
                self._data.clear()
                self._size = 0

            def __iter__(self):
                return iter(self._data)

            def __contains__(self, item):
                return item in self._data

            def prepend(self, item):
                self._data.insert(0, item)
                self._size += 1

            def append(self, item):
                self._data.append(item)
                self._size += 1

            def insert_at(self, index, item):
                self._data.insert(index, item)
                self._size += 1

            def remove_first(self):
                if self.is_empty():
                    raise EmptyStructureError()
                self._size -= 1
                return self._data.pop(0)

            def remove_last(self):
                if self.is_empty():
                    raise EmptyStructureError()
                self._size -= 1
                return self._data.pop()

            def remove(self, item):
                self._data.remove(item)
                self._size -= 1
                return item

            def remove_at(self, index):
                self._size -= 1
                return self._data.pop(index)

            def find(self, item):
                try:
                    return self._data.index(item)
                except ValueError:
                    return -1

            def reverse(self):
                self._data.reverse()

            def __getitem__(self, index):
                return self._data[index]

            def __setitem__(self, index, value):
                self._data[index] = value

        return ContractTestList

    def test_size_and_len_are_consistent(self, list_class):
        """Test that size property and __len__ are consistent."""
        lst = list_class()

        assert lst.size == len(lst)

        lst.append(1)
        assert lst.size == len(lst)

        lst.prepend(0)
        assert lst.size == len(lst)

        lst.remove_first()
        assert lst.size == len(lst)

    def test_operations_update_size_correctly(self, list_class):
        """Test that all operations update size correctly."""
        lst = list_class()
        initial_size = lst.size

        # append increases size
        lst.append(1)
        assert lst.size == initial_size + 1

        # prepend increases size
        lst.prepend(0)
        assert lst.size == initial_size + 2

        # insert_at increases size
        lst.insert_at(1, 0.5)
        assert lst.size == initial_size + 3

        # remove_first decreases size
        lst.remove_first()
        assert lst.size == initial_size + 2

        # remove_last decreases size
        lst.remove_last()
        assert lst.size == initial_size + 1

        # remove_at decreases size
        lst.remove_at(0)
        assert lst.size == initial_size

    def test_clear_resets_size_to_zero(self, list_class):
        """Test that clear() resets size to 0."""
        lst = list_class()

        lst.append(1)
        lst.append(2)
        lst.append(3)

        assert lst.size > 0

        lst.clear()

        assert lst.size == 0
        assert lst.is_empty() is True

    def test_indexing_is_consistent_with_iteration(self, list_class):
        """Test that indexing produces same order as iteration."""
        lst = list_class()

        values = [1, 2, 3, 4, 5]
        for val in values:
            lst.append(val)

        # Check forward indexing
        for i, expected in enumerate(values):
            assert lst[i] == expected

        # Check that list() produces same order
        assert list(lst) == values
