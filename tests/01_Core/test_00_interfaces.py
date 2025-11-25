from abc import ABC

import pytest

from sds.core.exceptions import EmptyStructureError
from sds.core.interfaces import Collection, LinearCollection


class TestCollection:
    """Tests for the Collection abstract base class."""

    def test_collection_is_abstract(self):
        """Test that Collection cannot be instantiated directly."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            Collection()

    def test_collection_is_abc(self):
        """Test that Collection is an ABC."""
        assert issubclass(Collection, ABC)

    def test_collection_has_required_abstract_methods(self):
        """Test that Collection defines the required abstract methods."""
        abstract_methods = Collection.__abstractmethods__

        required_methods = {
            "__len__",
            "is_empty",
            "clear",
            "__iter__",
            "__contains__",
        }

        assert abstract_methods == required_methods

    def test_collection_subclass_without_implementation_fails(self):
        """Test that a subclass without implementations cannot be instantiated."""

        class IncompleteCollection(Collection):
            pass

        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            IncompleteCollection()

    def test_collection_bool_is_concrete(self):
        """Test that __bool__ is implemented concretely in Collection."""
        # __bool__ should not be in abstract methods
        assert "__bool__" not in Collection.__abstractmethods__


class TestConcreteCollection:
    """Tests for concrete implementations of Collection."""

    @pytest.fixture
    def simple_collection_class(self):
        """Provide a simple concrete Collection implementation."""

        class SimpleCollection(Collection):
            def __init__(self):
                self._items = []

            def __len__(self):
                return len(self._items)

            def is_empty(self):
                return len(self._items) == 0

            def clear(self):
                self._items.clear()

            def __iter__(self):
                return iter(self._items)

            def __contains__(self, item):
                return item in self._items

            def add(self, item):
                """Helper method for testing."""
                self._items.append(item)

        return SimpleCollection

    def test_concrete_collection_can_be_instantiated(self, simple_collection_class):
        """Test that a complete concrete implementation can be instantiated."""
        collection = simple_collection_class()
        assert isinstance(collection, Collection)

    def test_len_works(self, simple_collection_class):
        """Test that __len__ works correctly."""
        collection = simple_collection_class()
        assert len(collection) == 0

        collection.add(1)
        assert len(collection) == 1

        collection.add(2)
        assert len(collection) == 2

    def test_is_empty_works(self, simple_collection_class):
        """Test that is_empty works correctly."""
        collection = simple_collection_class()
        assert collection.is_empty() is True

        collection.add(1)
        assert collection.is_empty() is False

        collection.clear()
        assert collection.is_empty() is True

    def test_clear_works(self, simple_collection_class):
        """Test that clear works correctly."""
        collection = simple_collection_class()
        collection.add(1)
        collection.add(2)
        collection.add(3)

        assert len(collection) == 3

        collection.clear()

        assert len(collection) == 0
        assert collection.is_empty() is True

    def test_iter_works(self, simple_collection_class):
        """Test that __iter__ works correctly."""
        collection = simple_collection_class()
        collection.add(1)
        collection.add(2)
        collection.add(3)

        items = list(collection)
        assert items == [1, 2, 3]

        # Test that we can iterate multiple times
        items2 = list(collection)
        assert items2 == [1, 2, 3]

    def test_contains_works(self, simple_collection_class):
        """Test that __contains__ works correctly."""
        collection = simple_collection_class()
        collection.add(1)
        collection.add(2)

        assert 1 in collection
        assert 2 in collection
        assert 3 not in collection

    def test_bool_works_when_empty(self, simple_collection_class):
        """Test that __bool__ returns False for empty collection."""
        collection = simple_collection_class()

        assert bool(collection) is False
        assert not collection

        # Test in conditional
        if collection:
            pytest.fail("Empty collection should be falsy")

    def test_bool_works_when_not_empty(self, simple_collection_class):
        """Test that __bool__ returns True for non-empty collection."""
        collection = simple_collection_class()
        collection.add(1)

        assert bool(collection) is True
        assert collection

        # Test in conditional
        if not collection:
            pytest.fail("Non-empty collection should be truthy")

    def test_bool_delegates_to_is_empty(self, simple_collection_class):
        """Test that __bool__ delegates to is_empty."""
        collection = simple_collection_class()

        # When empty
        assert collection.is_empty() is True
        assert bool(collection) is False

        # When not empty
        collection.add(1)
        assert collection.is_empty() is False
        assert bool(collection) is True


class TestLinearCollection:
    """Tests for the LinearCollection abstract base class."""

    def test_linear_collection_is_abstract(self):
        """Test that LinearCollection cannot be instantiated directly."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            LinearCollection()

    def test_linear_collection_is_abc(self):
        """Test that LinearCollection is an ABC."""
        assert issubclass(LinearCollection, ABC)

    def test_linear_collection_extends_collection(self):
        """Test that LinearCollection extends Collection."""
        assert issubclass(LinearCollection, Collection)

    def test_linear_collection_has_required_abstract_methods(self):
        """Test that LinearCollection defines all required abstract methods."""
        abstract_methods = LinearCollection.__abstractmethods__

        # Should include all Collection methods plus add and remove
        required_methods = {
            "__len__",
            "is_empty",
            "clear",
            "__iter__",
            "__contains__",
            "add",
            "remove",
        }

        assert abstract_methods == required_methods

    def test_linear_collection_subclass_without_implementation_fails(self):
        """Test that a subclass without implementations cannot be instantiated."""

        class IncompleteLinearCollection(LinearCollection):
            pass

        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            IncompleteLinearCollection()


class TestConcreteLinearCollection:
    """Tests for concrete implementations of LinearCollection."""

    @pytest.fixture
    def simple_linear_collection_class(self):
        """Provide a simple concrete LinearCollection implementation (Stack-like)."""

        class SimpleLinearCollection(LinearCollection):
            def __init__(self):
                self._items = []

            def __len__(self):
                return len(self._items)

            def is_empty(self):
                return len(self._items) == 0

            def clear(self):
                self._items.clear()

            def __iter__(self):
                return iter(self._items)

            def __contains__(self, item):
                return item in self._items

            def add(self, item):
                """Add to end (like append)."""
                self._items.append(item)

            def remove(self, item):
                """Remove from end (like pop)."""
                if self.is_empty():
                    raise EmptyStructureError("Cannot remove from empty collection")
                return self._items.pop()

        return SimpleLinearCollection

    def test_concrete_linear_collection_can_be_instantiated(
        self, simple_linear_collection_class
    ):
        """Test that a complete concrete implementation can be instantiated."""
        collection = simple_linear_collection_class()
        assert isinstance(collection, LinearCollection)
        assert isinstance(collection, Collection)

    def test_add_works(self, simple_linear_collection_class):
        """Test that add works correctly."""
        collection = simple_linear_collection_class()

        collection.add(1)
        assert len(collection) == 1
        assert 1 in collection

        collection.add(2)
        assert len(collection) == 2
        assert 2 in collection

    def test_remove_works(self, simple_linear_collection_class):
        """Test that remove works correctly."""
        collection = simple_linear_collection_class()
        collection.add(1)
        collection.add(2)

        item = collection.remove(None)  # Argument ignored in this implementation
        assert item == 2  # LIFO behavior
        assert len(collection) == 1

        item = collection.remove(None)
        assert item == 1
        assert len(collection) == 0

    def test_remove_from_empty_raises_error(self, simple_linear_collection_class):
        """Test that remove from empty collection raises EmptyStructureError."""
        collection = simple_linear_collection_class()

        with pytest.raises(EmptyStructureError):
            collection.remove(None)

    def test_linear_collection_inherits_collection_behavior(
        self, simple_linear_collection_class
    ):
        """Test that LinearCollection inherits all Collection behavior."""
        collection = simple_linear_collection_class()

        # Test inherited methods
        assert collection.is_empty() is True
        assert len(collection) == 0
        assert bool(collection) is False

        collection.add(1)
        collection.add(2)

        assert collection.is_empty() is False
        assert len(collection) == 2
        assert bool(collection) is True
        assert list(collection) == [1, 2]

        collection.clear()
        assert collection.is_empty() is True


class TestCollectionInterfaceContract:
    """Tests to verify the contract defined by Collection interface."""

    @pytest.fixture
    def collection_class(self):
        """Provide a minimal Collection implementation for contract testing."""

        class MinimalCollection(Collection):
            def __init__(self):
                self._data = []

            def __len__(self):
                return len(self._data)

            def is_empty(self):
                return len(self._data) == 0

            def clear(self):
                self._data.clear()

            def __iter__(self):
                return iter(self._data)

            def __contains__(self, item):
                return item in self._data

            def add(self, item):
                self._data.append(item)

        return MinimalCollection

    def test_len_and_is_empty_are_consistent(self, collection_class):
        """Test that len() == 0 implies is_empty() returns True."""
        collection = collection_class()

        # Empty collection
        assert len(collection) == 0
        assert collection.is_empty() is True

        # Non-empty collection
        collection.add(1)
        assert len(collection) > 0
        assert collection.is_empty() is False

    def test_bool_and_is_empty_are_consistent(self, collection_class):
        """Test that bool(collection) is the opposite of is_empty()."""
        collection = collection_class()

        assert collection.is_empty() is True
        assert bool(collection) is False

        collection.add(1)

        assert collection.is_empty() is False
        assert bool(collection) is True

    def test_clear_makes_collection_empty(self, collection_class):
        """Test that clear() makes the collection empty."""
        collection = collection_class()
        collection.add(1)
        collection.add(2)

        collection.clear()

        assert len(collection) == 0
        assert collection.is_empty() is True
        assert list(collection) == []

    def test_iter_returns_iterator(self, collection_class):
        """Test that __iter__ returns an iterator."""
        collection = collection_class()
        collection.add(1)

        iterator = iter(collection)
        assert hasattr(iterator, "__iter__")
        assert hasattr(iterator, "__next__")

    def test_contains_is_consistent_with_iter(self, collection_class):
        """Test that 'in' operator is consistent with iteration."""
        collection = collection_class()
        collection.add(1)
        collection.add(2)
        collection.add(3)

        # All iterated items should be contained
        for item in collection:
            assert item in collection

        # Items not added should not be contained
        assert 4 not in collection
        assert 5 not in collection


class TestLinearCollectionInterfaceContract:
    """Tests to verify the contract defined by LinearCollection interface."""

    @pytest.fixture
    def linear_collection_class(self):
        """Provide a minimal LinearCollection implementation for contract testing."""

        class MinimalLinearCollection(LinearCollection):
            def __init__(self):
                self._data = []

            def __len__(self):
                return len(self._data)

            def is_empty(self):
                return len(self._data) == 0

            def clear(self):
                self._data.clear()

            def __iter__(self):
                return iter(self._data)

            def __contains__(self, item):
                return item in self._data

            def add(self, item):
                self._data.append(item)

            def remove(self, item):
                if self.is_empty():
                    raise EmptyStructureError()
                return self._data.pop()

        return MinimalLinearCollection

    def test_add_increases_length(self, linear_collection_class):
        """Test that add() increases the length of the collection."""
        collection = linear_collection_class()
        initial_len = len(collection)

        collection.add(1)

        assert len(collection) == initial_len + 1

    def test_remove_decreases_length(self, linear_collection_class):
        """Test that remove() decreases the length of the collection."""
        collection = linear_collection_class()
        collection.add(1)
        collection.add(2)
        initial_len = len(collection)

        collection.remove(None)

        assert len(collection) == initial_len - 1

    def test_add_and_remove_are_inverse_operations(self, linear_collection_class):
        """Test that add followed by remove returns to initial state."""
        collection = linear_collection_class()
        collection.add(1)
        initial_len = len(collection)

        collection.add(2)
        assert len(collection) == initial_len + 1

        collection.remove(None)
        assert len(collection) == initial_len

    def test_remove_on_empty_raises_exception(self, linear_collection_class):
        """Test that remove on empty collection raises an exception."""
        collection = linear_collection_class()

        with pytest.raises(EmptyStructureError):
            collection.remove(None)
