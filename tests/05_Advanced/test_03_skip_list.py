# Copyright 2024-2025, skyfrigate, biface
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

"""Tests for SkipList probabilistic sorted data structure.

Test Classes
------------
TestSkipListCreation
    Instantiation and parameter validation.
TestInsert
    insert() — new keys, duplicate keys (update), ordering.
TestSearch
    search() — found, not found, value=None.
TestContains
    __contains__ — membership including value=None nodes.
TestDelete
    delete() — existing keys, missing keys, level shrinking.
TestIteration
    __iter__ and items() — sorted order.
TestMinMax
    min_key() and max_key() helpers.
TestSpecialMethods
    __len__, __repr__, __str__.
TestSortingProperties
    Invariant: elements always iterate in ascending order.
TestApplicationScenarios
    Real-world usage patterns.
TestEdgeCases
    Boundary conditions: single element, duplicates, large inputs.
"""

import random

import pytest

from sds.advanced import AbstractSkipList, SkipList

# ---------------------------------------------------------------------------
# TestSkipListCreation
# ---------------------------------------------------------------------------


class TestSkipListCreation:
    """Test SkipList instantiation and parameter validation."""

    def test_default_creation(self) -> None:
        """Default constructor produces an empty skip list."""
        sl = SkipList()
        assert len(sl) == 0
        assert sl.max_level == 16
        assert sl.probability == 0.5
        assert sl.level == 0

    def test_custom_max_level(self) -> None:
        """Custom max_level is stored correctly."""
        sl = SkipList(max_level=8)
        assert sl.max_level == 8

    def test_custom_probability(self) -> None:
        """Custom probability is stored correctly."""
        sl = SkipList(probability=0.25)
        assert sl.probability == 0.25

    def test_max_level_one(self) -> None:
        """max_level=1 is the smallest valid value."""
        sl = SkipList(max_level=1)
        sl.insert(1)
        assert 1 in sl

    def test_is_abstract_skip_list(self) -> None:
        """SkipList satisfies the AbstractSkipList interface."""
        assert isinstance(SkipList(), AbstractSkipList)

    def test_invalid_max_level_zero(self) -> None:
        """max_level=0 raises ValueError."""
        with pytest.raises(ValueError, match="max_level"):
            SkipList(max_level=0)

    def test_invalid_max_level_negative(self) -> None:
        """Negative max_level raises ValueError."""
        with pytest.raises(ValueError, match="max_level"):
            SkipList(max_level=-1)

    def test_invalid_probability_zero(self) -> None:
        """probability=0.0 raises ValueError."""
        with pytest.raises(ValueError, match="probability"):
            SkipList(probability=0.0)

    def test_invalid_probability_one(self) -> None:
        """probability=1.0 raises ValueError."""
        with pytest.raises(ValueError, match="probability"):
            SkipList(probability=1.0)

    def test_invalid_probability_above_one(self) -> None:
        """probability > 1.0 raises ValueError."""
        with pytest.raises(ValueError, match="probability"):
            SkipList(probability=2.0)

    def test_empty_iteration(self) -> None:
        """Iterating over an empty skip list yields nothing."""
        assert list(SkipList()) == []

    def test_empty_min_max(self) -> None:
        """min_key() and max_key() return None on empty list."""
        sl = SkipList()
        assert sl.min_key() is None
        assert sl.max_key() is None


# ---------------------------------------------------------------------------
# TestInsert
# ---------------------------------------------------------------------------


class TestInsert:
    """Test the insert() operation."""

    def test_insert_single(self) -> None:
        """Inserting one element gives length 1."""
        sl = SkipList()
        sl.insert(42)
        assert len(sl) == 1

    def test_insert_with_value(self) -> None:
        """Inserted value is retrievable via search()."""
        sl = SkipList()
        sl.insert(1, "hello")
        assert sl.search(1) == "hello"

    def test_insert_multiple_keys(self) -> None:
        """Multiple inserts produce correct length."""
        sl = SkipList()
        for i in range(10):
            sl.insert(i)
        assert len(sl) == 10

    def test_insert_maintains_sorted_order(self) -> None:
        """Keys inserted in random order iterate in sorted order."""
        keys = [5, 2, 8, 1, 9, 3]
        sl = SkipList()
        for k in keys:
            sl.insert(k)
        assert list(sl) == sorted(keys)

    def test_insert_duplicate_updates_value(self) -> None:
        """Re-inserting an existing key updates its value, not count."""
        sl = SkipList()
        sl.insert(1, "original")
        sl.insert(1, "updated")
        assert sl.search(1) == "updated"
        assert len(sl) == 1

    def test_insert_duplicate_no_length_change(self) -> None:
        """Updating via insert() does not increment length."""
        sl = SkipList()
        sl.insert(7)
        sl.insert(7)
        sl.insert(7)
        assert len(sl) == 1

    def test_insert_none_value_explicitly(self) -> None:
        """Inserting with value=None is valid."""
        sl = SkipList()
        sl.insert(5, None)
        assert 5 in sl
        assert sl.search(5) is None

    def test_insert_string_keys(self) -> None:
        """String keys are inserted and sorted lexicographically."""
        sl = SkipList()
        for word in ["banana", "apple", "cherry"]:
            sl.insert(word, len(word))
        assert list(sl) == ["apple", "banana", "cherry"]

    def test_insert_float_keys(self) -> None:
        """Float keys are supported."""
        sl = SkipList()
        sl.insert(1.5, "a")
        sl.insert(0.5, "b")
        sl.insert(2.5, "c")
        assert list(sl) == [0.5, 1.5, 2.5]

    def test_insert_updates_level(self) -> None:
        """level attribute is at least 0 after inserts."""
        sl = SkipList()
        for i in range(50):
            sl.insert(i)
        assert sl.level >= 0


# ---------------------------------------------------------------------------
# TestSearch
# ---------------------------------------------------------------------------


class TestSearch:
    """Test the search() operation."""

    def test_search_existing_key(self) -> None:
        """search() returns the correct value for a present key."""
        sl = SkipList()
        sl.insert(10, "ten")
        assert sl.search(10) == "ten"

    def test_search_missing_key(self) -> None:
        """search() returns None for an absent key."""
        sl = SkipList()
        sl.insert(1, "one")
        assert sl.search(99) is None

    def test_search_empty_list(self) -> None:
        """search() on empty list returns None."""
        assert SkipList().search(0) is None

    def test_search_after_delete(self) -> None:
        """search() returns None after the key has been deleted."""
        sl = SkipList()
        sl.insert(3, "three")
        sl.delete(3)
        assert sl.search(3) is None

    def test_search_value_none(self) -> None:
        """search() returns None when the stored value is None."""
        sl = SkipList()
        sl.insert(7, None)
        assert sl.search(7) is None
        assert 7 in sl  # key exists even though value is None

    def test_search_all_inserted_keys(self) -> None:
        """All inserted keys are found after bulk insert."""
        pairs = {i: f"val_{i}" for i in range(50)}
        sl = SkipList()
        for k, v in pairs.items():
            sl.insert(k, v)
        for k, v in pairs.items():
            assert sl.search(k) == v

    def test_search_after_update(self) -> None:
        """search() reflects the latest value after update."""
        sl = SkipList()
        sl.insert(1, "v1")
        sl.insert(1, "v2")
        assert sl.search(1) == "v2"


# ---------------------------------------------------------------------------
# TestContains
# ---------------------------------------------------------------------------


class TestContains:
    """Test the __contains__ operation."""

    def test_contains_present_key(self) -> None:
        """A recently inserted key is found."""
        sl = SkipList()
        sl.insert(42)
        assert 42 in sl

    def test_contains_absent_key(self) -> None:
        """A key never inserted is not found."""
        sl = SkipList()
        sl.insert(1)
        assert 99 not in sl

    def test_contains_after_delete(self) -> None:
        """A deleted key is no longer found."""
        sl = SkipList()
        sl.insert(5)
        sl.delete(5)
        assert 5 not in sl

    def test_contains_value_none(self) -> None:
        """A key stored with value=None is still found."""
        sl = SkipList()
        sl.insert(3, None)
        assert 3 in sl

    def test_contains_empty(self) -> None:
        """No key is found in an empty skip list."""
        assert 0 not in SkipList()

    def test_contains_multiple_keys(self) -> None:
        """All 20 inserted keys are found."""
        sl = SkipList()
        keys = list(range(20))
        for k in keys:
            sl.insert(k)
        for k in keys:
            assert k in sl


# ---------------------------------------------------------------------------
# TestDelete
# ---------------------------------------------------------------------------


class TestDelete:
    """Test the delete() operation."""

    def test_delete_existing_key(self) -> None:
        """delete() returns True for a present key."""
        sl = SkipList()
        sl.insert(1)
        assert sl.delete(1) is True

    def test_delete_missing_key(self) -> None:
        """delete() returns False for an absent key."""
        sl = SkipList()
        assert sl.delete(99) is False

    def test_delete_decrements_length(self) -> None:
        """Length decreases by 1 after a successful delete."""
        sl = SkipList()
        sl.insert(1)
        sl.insert(2)
        sl.delete(1)
        assert len(sl) == 1

    def test_delete_removes_from_iteration(self) -> None:
        """Deleted key no longer appears in iteration."""
        sl = SkipList()
        for k in [1, 2, 3]:
            sl.insert(k)
        sl.delete(2)
        assert list(sl) == [1, 3]

    def test_delete_first_element(self) -> None:
        """Deleting the minimum element maintains order."""
        sl = SkipList()
        for k in [1, 2, 3]:
            sl.insert(k)
        sl.delete(1)
        assert list(sl) == [2, 3]
        assert sl.min_key() == 2

    def test_delete_last_element(self) -> None:
        """Deleting the maximum element maintains order."""
        sl = SkipList()
        for k in [1, 2, 3]:
            sl.insert(k)
        sl.delete(3)
        assert list(sl) == [1, 2]
        assert sl.max_key() == 2

    def test_delete_only_element(self) -> None:
        """Deleting the only element leaves an empty list."""
        sl = SkipList()
        sl.insert(7)
        sl.delete(7)
        assert len(sl) == 0
        assert list(sl) == []

    def test_delete_idempotent(self) -> None:
        """Deleting the same key twice: first True, then False."""
        sl = SkipList()
        sl.insert(5)
        assert sl.delete(5) is True
        assert sl.delete(5) is False

    def test_delete_all_elements(self) -> None:
        """Deleting all elements one by one empties the list."""
        sl = SkipList()
        keys = list(range(10))
        for k in keys:
            sl.insert(k)
        for k in keys:
            sl.delete(k)
        assert len(sl) == 0
        assert list(sl) == []

    def test_delete_shrinks_level(self) -> None:
        """After deleting all nodes, level is still valid (>= 0)."""
        sl = SkipList()
        for k in range(20):
            sl.insert(k)
        for k in range(20):
            sl.delete(k)
        assert sl.level >= 0


# ---------------------------------------------------------------------------
# TestIteration
# ---------------------------------------------------------------------------


class TestIteration:
    """Test __iter__ and items() iteration."""

    def test_iter_empty(self) -> None:
        """Iterating empty list yields nothing."""
        assert list(SkipList()) == []

    def test_iter_sorted(self) -> None:
        """Keys yield in ascending order regardless of insert order."""
        sl = SkipList()
        for k in [5, 1, 3, 2, 4]:
            sl.insert(k)
        assert list(sl) == [1, 2, 3, 4, 5]

    def test_iter_after_delete(self) -> None:
        """Iteration reflects deletions."""
        sl = SkipList()
        for k in [1, 2, 3, 4, 5]:
            sl.insert(k)
        sl.delete(2)
        sl.delete(4)
        assert list(sl) == [1, 3, 5]

    def test_items_sorted(self) -> None:
        """items() yields (key, value) pairs in ascending key order."""
        sl = SkipList()
        sl.insert(3, "c")
        sl.insert(1, "a")
        sl.insert(2, "b")
        assert list(sl.items()) == [(1, "a"), (2, "b"), (3, "c")]

    def test_items_value_none(self) -> None:
        """items() yields None for nodes without a value."""
        sl = SkipList()
        sl.insert(1)
        sl.insert(2, "two")
        items = dict(sl.items())
        assert items[1] is None
        assert items[2] == "two"

    def test_iter_large(self) -> None:
        """200 randomly inserted elements iterate in sorted order."""
        keys = random.sample(range(10000), 200)
        sl = SkipList()
        for k in keys:
            sl.insert(k)
        assert list(sl) == sorted(keys)


# ---------------------------------------------------------------------------
# TestMinMax
# ---------------------------------------------------------------------------


class TestMinMax:
    """Test min_key() and max_key() helpers."""

    def test_min_empty(self) -> None:
        """min_key() returns None on empty list."""
        assert SkipList().min_key() is None

    def test_max_empty(self) -> None:
        """max_key() returns None on empty list."""
        assert SkipList().max_key() is None

    def test_min_single(self) -> None:
        """min_key() returns the only element."""
        sl = SkipList()
        sl.insert(7)
        assert sl.min_key() == 7

    def test_max_single(self) -> None:
        """max_key() returns the only element."""
        sl = SkipList()
        sl.insert(7)
        assert sl.max_key() == 7

    def test_min_multiple(self) -> None:
        """min_key() returns the smallest key."""
        sl = SkipList()
        for k in [5, 2, 8, 1, 9]:
            sl.insert(k)
        assert sl.min_key() == 1

    def test_max_multiple(self) -> None:
        """max_key() returns the largest key."""
        sl = SkipList()
        for k in [5, 2, 8, 1, 9]:
            sl.insert(k)
        assert sl.max_key() == 9

    def test_min_after_delete_min(self) -> None:
        """min_key() updates after the minimum is deleted."""
        sl = SkipList()
        for k in [1, 2, 3]:
            sl.insert(k)
        sl.delete(1)
        assert sl.min_key() == 2

    def test_max_after_delete_max(self) -> None:
        """max_key() updates after the maximum is deleted."""
        sl = SkipList()
        for k in [1, 2, 3]:
            sl.insert(k)
        sl.delete(3)
        assert sl.max_key() == 2


# ---------------------------------------------------------------------------
# TestSpecialMethods
# ---------------------------------------------------------------------------


class TestSpecialMethods:
    """Test __len__, __repr__, __str__."""

    def test_len_empty(self) -> None:
        """len() of empty list is 0."""
        assert len(SkipList()) == 0

    def test_len_after_inserts(self) -> None:
        """len() reflects unique keys inserted."""
        sl = SkipList()
        for i in range(5):
            sl.insert(i)
        assert len(sl) == 5

    def test_len_after_duplicate(self) -> None:
        """Duplicate insert does not change len()."""
        sl = SkipList()
        sl.insert(1)
        sl.insert(1)
        assert len(sl) == 1

    def test_repr_format(self) -> None:
        """repr() matches the expected pattern."""
        sl = SkipList(max_level=8, probability=0.5)
        r = repr(sl)
        assert "SkipList" in r
        assert "length=0" in r
        assert "max_level=8" in r
        assert "probability=0.5" in r

    def test_repr_after_insert(self) -> None:
        """repr() reflects updated length."""
        sl = SkipList()
        sl.insert(1)
        assert "length=1" in repr(sl)

    def test_str_contains_elements(self) -> None:
        """str() mentions the number of elements."""
        sl = SkipList()
        sl.insert(1)
        assert "1" in str(sl)

    def test_str_contains_levels(self) -> None:
        """str() mentions the level range."""
        sl = SkipList(max_level=8)
        s = str(sl)
        assert "8" in s


# ---------------------------------------------------------------------------
# TestSortingProperties
# ---------------------------------------------------------------------------


class TestSortingProperties:
    """Invariant: elements always iterate in ascending sorted order."""

    def test_sorted_after_random_inserts(self) -> None:
        """100 random insertions yield sorted iteration."""
        keys = random.sample(range(1000), 100)
        sl = SkipList()
        for k in keys:
            sl.insert(k)
        assert list(sl) == sorted(keys)

    def test_sorted_after_mixed_operations(self) -> None:
        """Insert/delete mix preserves sorted order."""
        sl = SkipList()
        inserted: set[int] = set()
        ops = random.choices(range(50), k=200)
        for k in ops:
            if k in inserted:
                sl.delete(k)
                inserted.discard(k)
            else:
                sl.insert(k)
                inserted.add(k)
        assert list(sl) == sorted(inserted)

    def test_sorted_string_keys(self) -> None:
        """String keys iterate in lexicographic order."""
        words = ["zebra", "ant", "monkey", "bear", "lion"]
        sl = SkipList()
        for w in words:
            sl.insert(w)
        assert list(sl) == sorted(words)

    def test_sorted_float_keys(self) -> None:
        """Float keys iterate in numeric order."""
        keys = [1.5, 0.1, 3.14, 2.71, 0.5]
        sl = SkipList()
        for k in keys:
            sl.insert(k)
        assert list(sl) == sorted(keys)


# ---------------------------------------------------------------------------
# TestApplicationScenarios
# ---------------------------------------------------------------------------


class TestApplicationScenarios:
    """Test real-world usage patterns for SkipList."""

    def test_leaderboard(self) -> None:
        """SkipList maintains sorted scores for a leaderboard."""
        sl = SkipList()
        scores = {"alice": 150, "bob": 200, "carol": 175, "dave": 90}
        for score, name in scores.items():
            sl.insert(score, name)
        # Scores iterate in ascending order
        assert list(sl) == sorted(scores.keys())

    def test_range_query(self) -> None:
        """Manual range query via sorted iteration."""
        sl = SkipList()
        for k in range(20):
            sl.insert(k, k * 2)
        # Keys in [5, 10]
        result = [(k, v) for k, v in sl.items() if 5 <= k <= 10]
        assert result == [(k, k * 2) for k in range(5, 11)]

    def test_order_book(self) -> None:
        """Price levels in an order book are sorted correctly."""
        sl = SkipList()
        prices = [101.5, 100.0, 102.0, 99.5, 103.0]
        for p in prices:
            sl.insert(p, f"qty@{p}")
        assert list(sl) == sorted(prices)
        # Best bid = min price
        assert sl.min_key() == 99.5
        # Best ask = max price
        assert sl.max_key() == 103.0

    def test_insert_delete_reinsert(self) -> None:
        """A deleted key can be re-inserted cleanly."""
        sl = SkipList()
        sl.insert(10, "first")
        sl.delete(10)
        sl.insert(10, "second")
        assert sl.search(10) == "second"
        assert len(sl) == 1

    def test_bulk_insert_and_search(self) -> None:
        """500 keys inserted and searched with no misses."""
        keys = random.sample(range(10000), 500)
        sl = SkipList()
        for k in keys:
            sl.insert(k, str(k))
        for k in keys:
            assert sl.search(k) == str(k)


# ---------------------------------------------------------------------------
# TestEdgeCases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    """Test boundary conditions."""

    def test_single_element_insert_search_delete(self) -> None:
        """Full lifecycle with a single element."""
        sl = SkipList()
        sl.insert(1, "one")
        assert sl.search(1) == "one"
        assert 1 in sl
        assert sl.delete(1) is True
        assert 1 not in sl
        assert len(sl) == 0

    def test_insert_zero_key(self) -> None:
        """0 is a valid key."""
        sl = SkipList()
        sl.insert(0, "zero")
        assert sl.search(0) == "zero"
        assert 0 in sl

    def test_insert_negative_keys(self) -> None:
        """Negative keys are sorted correctly."""
        sl = SkipList()
        for k in [-3, -1, -5, -2, -4]:
            sl.insert(k)
        assert list(sl) == [-5, -4, -3, -2, -1]

    def test_mixed_positive_negative_keys(self) -> None:
        """Mixed positive/negative keys iterate in correct order."""
        sl = SkipList()
        for k in [-2, 0, 3, -1, 2]:
            sl.insert(k)
        assert list(sl) == [-2, -1, 0, 2, 3]

    def test_max_level_one_many_inserts(self) -> None:
        """max_level=1 still produces correct sorted output."""
        sl = SkipList(max_level=1)
        for k in [5, 3, 1, 4, 2]:
            sl.insert(k)
        assert list(sl) == [1, 2, 3, 4, 5]

    def test_high_probability_many_inserts(self) -> None:
        """probability=0.9 (tall nodes) still gives correct output."""
        sl = SkipList(probability=0.9)
        keys = list(range(30))
        for k in keys:
            sl.insert(k)
        assert list(sl) == keys

    def test_low_probability_many_inserts(self) -> None:
        """probability=0.1 (short nodes) still gives correct output."""
        sl = SkipList(probability=0.1)
        keys = list(range(30))
        for k in keys:
            sl.insert(k)
        assert list(sl) == keys

    def test_large_insert(self) -> None:
        """1000 inserts complete without error."""
        sl = SkipList(max_level=20)
        keys = random.sample(range(100000), 1000)
        for k in keys:
            sl.insert(k)
        assert len(sl) == 1000
        assert list(sl) == sorted(keys)


# ---------------------------------------------------------------------------
# TestCollectionInterface
# ---------------------------------------------------------------------------


class TestCollectionInterface:
    """Test Collection interface compliance for SkipList."""

    def test_is_collection(self) -> None:
        """SkipList satisfies the Collection interface."""
        from sds.core.interfaces import Collection

        assert isinstance(SkipList(), Collection)

    def test_is_empty_on_new(self) -> None:
        """is_empty() returns True on a freshly created list."""
        assert SkipList().is_empty() is True

    def test_is_empty_after_insert(self) -> None:
        """is_empty() returns False after inserting an element."""
        sl = SkipList()
        sl.insert(1)
        assert sl.is_empty() is False

    def test_is_empty_after_delete_all(self) -> None:
        """is_empty() returns True after all elements are deleted."""
        sl = SkipList()
        sl.insert(1)
        sl.delete(1)
        assert sl.is_empty() is True

    def test_bool_empty(self) -> None:
        """bool(sl) is False when empty."""
        assert not SkipList()

    def test_bool_non_empty(self) -> None:
        """bool(sl) is True when non-empty."""
        sl = SkipList()
        sl.insert(1)
        assert sl

    def test_clear_empties(self) -> None:
        """clear() removes all elements."""
        sl = SkipList()
        for k in [1, 2, 3]:
            sl.insert(k)
        sl.clear()
        assert len(sl) == 0
        assert sl.is_empty() is True

    def test_clear_removes_from_iteration(self) -> None:
        """clear() leaves nothing to iterate."""
        sl = SkipList()
        for k in range(5):
            sl.insert(k)
        sl.clear()
        assert list(sl) == []

    def test_clear_allows_reuse(self) -> None:
        """SkipList is fully usable after clear()."""
        sl = SkipList()
        sl.insert(1)
        sl.clear()
        sl.insert(2)
        assert list(sl) == [2]
        assert len(sl) == 1
