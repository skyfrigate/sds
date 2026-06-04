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

"""Tests for HashTableChaining and HashTableOpenAddressing.

Both classes share the same AbstractHashTable interface; most tests are
parameterised over both implementations. Strategy-specific tests cover
details unique to chaining (load factor > 1) or open addressing (tombstones,
max_load_factor < 1 constraint).

Test Classes
------------
TestHashTableChainingCreation
    Instantiation and parameter validation for chaining.
TestHashTableOpenAddressingCreation
    Instantiation and parameter validation for open addressing.
TestPut
    put() — insert, update, bulk.  [parameterised]
TestGet
    get() — found, missing, value=None.  [parameterised]
TestContains
    __contains__.  [parameterised]
TestDelete
    delete() — existing, missing, after resize.  [parameterised]
TestIteration
    __iter__ and items().  [parameterised]
TestGetSetItem
    __getitem__ and __setitem__.  [parameterised]
TestResize
    Automatic resize behaviour.  [parameterised]
TestSpecialMethods
    __len__, __repr__, __str__.  [parameterised]
TestChainingSpecific
    Chaining-only tests (load factor > 1).
TestOpenAddressingSpecific
    Open-addressing-only tests (tombstones, load factor < 1).
TestApplicationScenarios
    Real-world usage patterns.  [parameterised]
TestEdgeCases
    Boundary conditions.  [parameterised]
"""

import pytest

from sds.advanced import (
    AbstractHashTable,
    HashTableChaining,
    HashTableOpenAddressing,
)

# ---------------------------------------------------------------------------
# Parametrisation fixture
# ---------------------------------------------------------------------------

BOTH = [HashTableChaining, HashTableOpenAddressing]


# ---------------------------------------------------------------------------
# TestHashTableChainingCreation
# ---------------------------------------------------------------------------


class TestHashTableChainingCreation:
    """Instantiation and validation for HashTableChaining."""

    def test_default_creation(self) -> None:
        """Default constructor produces empty table with capacity 16."""
        ht = HashTableChaining()
        assert len(ht) == 0
        assert ht.capacity == 16

    def test_custom_capacity(self) -> None:
        """Custom capacity is respected."""
        ht = HashTableChaining(capacity=8)
        assert ht.capacity == 8

    def test_custom_load_factor(self) -> None:
        """Custom max_load_factor stored correctly."""
        ht = HashTableChaining(max_load_factor=1.5)
        assert ht.load_factor == 0.0

    def test_is_abstract_hash_table(self) -> None:
        """HashTableChaining satisfies AbstractHashTable."""
        assert isinstance(HashTableChaining(), AbstractHashTable)

    def test_invalid_capacity_zero(self) -> None:
        """capacity=0 raises ValueError."""
        with pytest.raises(ValueError, match="capacity"):
            HashTableChaining(capacity=0)

    def test_invalid_capacity_negative(self) -> None:
        """Negative capacity raises ValueError."""
        with pytest.raises(ValueError, match="capacity"):
            HashTableChaining(capacity=-1)

    def test_invalid_load_factor_zero(self) -> None:
        """max_load_factor=0 raises ValueError."""
        with pytest.raises(ValueError, match="max_load_factor"):
            HashTableChaining(max_load_factor=0)

    def test_invalid_load_factor_negative(self) -> None:
        """Negative max_load_factor raises ValueError."""
        with pytest.raises(ValueError, match="max_load_factor"):
            HashTableChaining(max_load_factor=-0.5)

    def test_load_factor_empty(self) -> None:
        """Load factor of empty table is 0.0."""
        assert HashTableChaining().load_factor == 0.0


# ---------------------------------------------------------------------------
# TestHashTableOpenAddressingCreation
# ---------------------------------------------------------------------------


class TestHashTableOpenAddressingCreation:
    """Instantiation and validation for HashTableOpenAddressing."""

    def test_default_creation(self) -> None:
        """Default constructor produces empty table."""
        ht = HashTableOpenAddressing()
        assert len(ht) == 0
        assert ht.capacity == 16

    def test_custom_capacity(self) -> None:
        """Custom capacity is respected."""
        ht = HashTableOpenAddressing(capacity=8)
        assert ht.capacity == 8

    def test_is_abstract_hash_table(self) -> None:
        """HashTableOpenAddressing satisfies AbstractHashTable."""
        assert isinstance(HashTableOpenAddressing(), AbstractHashTable)

    def test_invalid_capacity_one(self) -> None:
        """capacity=1 raises ValueError (must be ≥ 2)."""
        with pytest.raises(ValueError, match="capacity"):
            HashTableOpenAddressing(capacity=1)

    def test_invalid_capacity_zero(self) -> None:
        """capacity=0 raises ValueError."""
        with pytest.raises(ValueError, match="capacity"):
            HashTableOpenAddressing(capacity=0)

    def test_invalid_load_factor_zero(self) -> None:
        """max_load_factor=0.0 raises ValueError."""
        with pytest.raises(ValueError, match="max_load_factor"):
            HashTableOpenAddressing(max_load_factor=0.0)

    def test_invalid_load_factor_one(self) -> None:
        """max_load_factor=1.0 raises ValueError."""
        with pytest.raises(ValueError, match="max_load_factor"):
            HashTableOpenAddressing(max_load_factor=1.0)

    def test_invalid_load_factor_above_one(self) -> None:
        """max_load_factor > 1.0 raises ValueError."""
        with pytest.raises(ValueError, match="max_load_factor"):
            HashTableOpenAddressing(max_load_factor=1.5)

    def test_load_factor_empty(self) -> None:
        """Load factor of empty table is 0.0."""
        assert HashTableOpenAddressing().load_factor == 0.0


# ---------------------------------------------------------------------------
# TestPut
# ---------------------------------------------------------------------------


class TestPut:
    """Test put() — parameterised over both implementations."""

    @pytest.mark.parametrize("cls", BOTH)
    def test_put_single(self, cls: type) -> None:
        """Inserting one entry sets len to 1."""
        ht = cls()
        ht.put("a", 1)
        assert len(ht) == 1

    @pytest.mark.parametrize("cls", BOTH)
    def test_put_multiple(self, cls: type) -> None:
        """Inserting n distinct keys sets len to n."""
        ht = cls()
        for i in range(10):
            ht.put(i, i * 2)
        assert len(ht) == 10

    @pytest.mark.parametrize("cls", BOTH)
    def test_put_update_does_not_grow(self, cls: type) -> None:
        """Re-inserting an existing key updates value, len unchanged."""
        ht = cls()
        ht.put("k", "old")
        ht.put("k", "new")
        assert ht.get("k") == "new"
        assert len(ht) == 1

    @pytest.mark.parametrize("cls", BOTH)
    def test_put_none_value(self, cls: type) -> None:
        """Storing None as value is valid."""
        ht = cls()
        ht.put("null", None)
        assert "null" in ht
        assert ht.get("null") is None

    @pytest.mark.parametrize("cls", BOTH)
    def test_put_integer_keys(self, cls: type) -> None:
        """Integer keys are stored and retrieved correctly."""
        ht = cls()
        for i in range(20):
            ht.put(i, str(i))
        for i in range(20):
            assert ht.get(i) == str(i)

    @pytest.mark.parametrize("cls", BOTH)
    def test_put_string_keys(self, cls: type) -> None:
        """String keys are stored and retrieved correctly."""
        ht = cls()
        ht.put("hello", 1)
        ht.put("world", 2)
        assert ht.get("hello") == 1
        assert ht.get("world") == 2

    @pytest.mark.parametrize("cls", BOTH)
    def test_put_tuple_keys(self, cls: type) -> None:
        """Tuple keys (hashable) are supported."""
        ht = cls()
        ht.put((1, 2), "pair")
        assert ht.get((1, 2)) == "pair"


# ---------------------------------------------------------------------------
# TestGet
# ---------------------------------------------------------------------------


class TestGet:
    """Test get() — parameterised over both implementations."""

    @pytest.mark.parametrize("cls", BOTH)
    def test_get_existing(self, cls: type) -> None:
        """get() returns correct value for a present key."""
        ht = cls()
        ht.put("x", 42)
        assert ht.get("x") == 42

    @pytest.mark.parametrize("cls", BOTH)
    def test_get_missing(self, cls: type) -> None:
        """get() returns None for an absent key."""
        ht = cls()
        assert ht.get("ghost") is None

    @pytest.mark.parametrize("cls", BOTH)
    def test_get_after_update(self, cls: type) -> None:
        """get() reflects the latest value after put()."""
        ht = cls()
        ht.put("k", "v1")
        ht.put("k", "v2")
        assert ht.get("k") == "v2"

    @pytest.mark.parametrize("cls", BOTH)
    def test_get_after_delete(self, cls: type) -> None:
        """get() returns None after key is deleted."""
        ht = cls()
        ht.put("k", "v")
        ht.delete("k")
        assert ht.get("k") is None

    @pytest.mark.parametrize("cls", BOTH)
    def test_get_empty_table(self, cls: type) -> None:
        """get() on empty table returns None."""
        assert cls().get("anything") is None


# ---------------------------------------------------------------------------
# TestContains
# ---------------------------------------------------------------------------


class TestContains:
    """Test __contains__ — parameterised over both implementations."""

    @pytest.mark.parametrize("cls", BOTH)
    def test_contains_present(self, cls: type) -> None:
        """A recently inserted key is found."""
        ht = cls()
        ht.put(1, "one")
        assert 1 in ht

    @pytest.mark.parametrize("cls", BOTH)
    def test_contains_absent(self, cls: type) -> None:
        """A key never inserted is not found."""
        ht = cls()
        assert 99 not in ht

    @pytest.mark.parametrize("cls", BOTH)
    def test_contains_after_delete(self, cls: type) -> None:
        """A deleted key is no longer found."""
        ht = cls()
        ht.put(5, "five")
        ht.delete(5)
        assert 5 not in ht

    @pytest.mark.parametrize("cls", BOTH)
    def test_contains_none_value(self, cls: type) -> None:
        """A key stored with value=None is still found."""
        ht = cls()
        ht.put("null_val", None)
        assert "null_val" in ht

    @pytest.mark.parametrize("cls", BOTH)
    def test_contains_empty(self, cls: type) -> None:
        """No key is found in an empty table."""
        assert 0 not in cls()


# ---------------------------------------------------------------------------
# TestDelete
# ---------------------------------------------------------------------------


class TestDelete:
    """Test delete() — parameterised over both implementations."""

    @pytest.mark.parametrize("cls", BOTH)
    def test_delete_existing(self, cls: type) -> None:
        """delete() returns True for a present key."""
        ht = cls()
        ht.put(1, "one")
        assert ht.delete(1) is True

    @pytest.mark.parametrize("cls", BOTH)
    def test_delete_missing(self, cls: type) -> None:
        """delete() returns False for an absent key."""
        ht = cls()
        assert ht.delete(99) is False

    @pytest.mark.parametrize("cls", BOTH)
    def test_delete_decrements_len(self, cls: type) -> None:
        """Length decreases by 1 after a successful delete."""
        ht = cls()
        ht.put(1, "a")
        ht.put(2, "b")
        ht.delete(1)
        assert len(ht) == 1

    @pytest.mark.parametrize("cls", BOTH)
    def test_delete_idempotent(self, cls: type) -> None:
        """Deleting the same key twice: first True, then False."""
        ht = cls()
        ht.put(7, "seven")
        assert ht.delete(7) is True
        assert ht.delete(7) is False

    @pytest.mark.parametrize("cls", BOTH)
    def test_delete_all(self, cls: type) -> None:
        """Deleting all keys leaves an empty table."""
        ht = cls()
        for i in range(10):
            ht.put(i, str(i))
        for i in range(10):
            ht.delete(i)
        assert len(ht) == 0
        for i in range(10):
            assert i not in ht

    @pytest.mark.parametrize("cls", BOTH)
    def test_delete_then_reinsert(self, cls: type) -> None:
        """A deleted key can be re-inserted cleanly."""
        ht = cls()
        ht.put("k", "first")
        ht.delete("k")
        ht.put("k", "second")
        assert ht.get("k") == "second"
        assert len(ht) == 1


# ---------------------------------------------------------------------------
# TestIteration
# ---------------------------------------------------------------------------


class TestIteration:
    """Test __iter__ and items() — parameterised."""

    @pytest.mark.parametrize("cls", BOTH)
    def test_iter_empty(self, cls: type) -> None:
        """Iterating an empty table yields nothing."""
        assert list(cls()) == []

    @pytest.mark.parametrize("cls", BOTH)
    def test_iter_all_keys(self, cls: type) -> None:
        """All inserted keys appear in iteration."""
        ht = cls()
        keys = list(range(15))
        for k in keys:
            ht.put(k, k)
        assert sorted(ht) == keys

    @pytest.mark.parametrize("cls", BOTH)
    def test_iter_after_delete(self, cls: type) -> None:
        """Deleted keys do not appear in iteration."""
        ht = cls()
        for k in range(5):
            ht.put(k, k)
        ht.delete(2)
        assert 2 not in list(ht)
        assert sorted(ht) == [0, 1, 3, 4]

    @pytest.mark.parametrize("cls", BOTH)
    def test_items_all_pairs(self, cls: type) -> None:
        """items() yields all (key, value) pairs."""
        ht = cls()
        data = {i: i * 10 for i in range(10)}
        for k, v in data.items():
            ht.put(k, v)
        assert dict(ht.items()) == data

    @pytest.mark.parametrize("cls", BOTH)
    def test_items_after_update(self, cls: type) -> None:
        """items() reflects updated values."""
        ht = cls()
        ht.put("k", "old")
        ht.put("k", "new")
        items = dict(ht.items())
        assert items["k"] == "new"
        assert len(items) == 1


# ---------------------------------------------------------------------------
# TestGetSetItem
# ---------------------------------------------------------------------------


class TestGetSetItem:
    """Test __getitem__ and __setitem__ — parameterised."""

    @pytest.mark.parametrize("cls", BOTH)
    def test_getitem_present(self, cls: type) -> None:
        """ht[key] returns the stored value."""
        ht = cls()
        ht.put("a", 42)
        assert ht["a"] == 42

    @pytest.mark.parametrize("cls", BOTH)
    def test_getitem_missing_raises(self, cls: type) -> None:
        """ht[key] raises KeyError for absent key."""
        ht = cls()
        with pytest.raises(KeyError):
            _ = ht["ghost"]

    @pytest.mark.parametrize("cls", BOTH)
    def test_setitem(self, cls: type) -> None:
        """ht[key] = value is equivalent to put()."""
        ht = cls()
        ht["x"] = 99
        assert ht.get("x") == 99
        assert len(ht) == 1

    @pytest.mark.parametrize("cls", BOTH)
    def test_setitem_update(self, cls: type) -> None:
        """ht[key] = value updates an existing key."""
        ht = cls()
        ht["k"] = "v1"
        ht["k"] = "v2"
        assert ht["k"] == "v2"
        assert len(ht) == 1


# ---------------------------------------------------------------------------
# TestResize
# ---------------------------------------------------------------------------


class TestResize:
    """Test automatic resize behaviour — parameterised."""

    @pytest.mark.parametrize("cls", BOTH)
    def test_resize_preserves_all_entries(self, cls: type) -> None:
        """All entries survive a resize triggered by bulk inserts."""
        ht = cls(capacity=4)
        for i in range(50):
            ht.put(i, str(i))
        assert len(ht) == 50
        for i in range(50):
            assert ht.get(i) == str(i), f"Missing {i} after resize in {cls.__name__}"

    @pytest.mark.parametrize("cls", BOTH)
    def test_capacity_grows(self, cls: type) -> None:
        """Capacity increases after resize."""
        ht = cls(capacity=4)
        initial = ht.capacity
        for i in range(20):
            ht.put(i, i)
        assert ht.capacity > initial

    @pytest.mark.parametrize("cls", BOTH)
    def test_resize_keeps_correct_values(self, cls: type) -> None:
        """Values are correctly rehashed after resize."""
        ht = cls(capacity=2)
        pairs = {f"key_{i}": i * 3 for i in range(30)}
        for k, v in pairs.items():
            ht.put(k, v)
        for k, v in pairs.items():
            assert ht.get(k) == v


# ---------------------------------------------------------------------------
# TestSpecialMethods
# ---------------------------------------------------------------------------


class TestSpecialMethods:
    """Test __len__, __repr__, __str__ — parameterised."""

    @pytest.mark.parametrize("cls", BOTH)
    def test_len_empty(self, cls: type) -> None:
        """len() of empty table is 0."""
        assert len(cls()) == 0

    @pytest.mark.parametrize("cls", BOTH)
    def test_len_after_puts(self, cls: type) -> None:
        """len() equals number of distinct keys."""
        ht = cls()
        for i in range(7):
            ht.put(i, i)
        assert len(ht) == 7

    @pytest.mark.parametrize("cls", BOTH)
    def test_repr_contains_class_name(self, cls: type) -> None:
        """repr() contains the class name."""
        ht = cls()
        assert cls.__name__ in repr(ht)

    @pytest.mark.parametrize("cls", BOTH)
    def test_repr_contains_size(self, cls: type) -> None:
        """repr() mentions size=0 when empty."""
        ht = cls()
        assert "size=0" in repr(ht)

    @pytest.mark.parametrize("cls", BOTH)
    def test_str_contains_entries(self, cls: type) -> None:
        """str() mentions the number of entries."""
        ht = cls()
        assert "0" in str(ht)

    @pytest.mark.parametrize("cls", BOTH)
    def test_str_after_insert(self, cls: type) -> None:
        """str() mentions updated count."""
        ht = cls()
        ht.put(1, "a")
        assert "1" in str(ht)


# ---------------------------------------------------------------------------
# TestChainingSpecific
# ---------------------------------------------------------------------------


class TestChainingSpecific:
    """Tests specific to HashTableChaining."""

    def test_load_factor_above_one(self) -> None:
        """Chaining tolerates load factor > 1 before resizing."""
        ht = HashTableChaining(capacity=4, max_load_factor=2.0)
        for i in range(8):
            ht.put(i, i)
        assert len(ht) == 8
        assert ht.capacity == 4  # no resize yet

    def test_many_collisions_all_retrievable(self) -> None:
        """All entries are retrievable even under heavy collision."""
        # Force all keys to the same bucket by using a tiny table
        ht = HashTableChaining(capacity=1, max_load_factor=100.0)
        for i in range(30):
            ht.put(i, str(i))
        for i in range(30):
            assert ht.get(i) == str(i)

    def test_load_factor_increases_with_inserts(self) -> None:
        """load_factor grows as entries are added."""
        ht = HashTableChaining(capacity=16, max_load_factor=10.0)
        prev = ht.load_factor
        for i in range(10):
            ht.put(i, i)
            assert ht.load_factor >= prev
            prev = ht.load_factor

    def test_items_consistent_with_iter(self) -> None:
        """Keys from __iter__ and items() are identical."""
        ht = HashTableChaining()
        for i in range(20):
            ht.put(i, i * 2)
        iter_keys = sorted(ht)
        items_keys = sorted(k for k, _ in ht.items())
        assert iter_keys == items_keys


# ---------------------------------------------------------------------------
# TestOpenAddressingSpecific
# ---------------------------------------------------------------------------


class TestOpenAddressingSpecific:
    """Tests specific to HashTableOpenAddressing."""

    def test_tombstones_do_not_break_lookup(self) -> None:
        """Deleted entries (tombstones) do not break subsequent lookups."""
        ht = HashTableOpenAddressing(capacity=16)
        # Insert keys that hash to the same slot sequence
        ht.put(0, "zero")
        ht.put(16, "sixteen")  # likely same home slot as 0
        ht.put(32, "thirty-two")
        ht.delete(16)  # create tombstone in the chain
        # 0 and 32 must still be found through the tombstone
        assert ht.get(0) == "zero"
        assert ht.get(32) == "thirty-two"

    def test_reinsert_after_delete_through_tombstone(self) -> None:
        """Reinserting a deleted key reuses the tombstone slot."""
        ht = HashTableOpenAddressing(capacity=8)
        ht.put("k", "v1")
        ht.delete("k")
        ht.put("k", "v2")
        assert ht.get("k") == "v2"
        assert len(ht) == 1

    def test_load_factor_excludes_tombstones(self) -> None:
        """load_factor counts only live entries, not tombstones."""
        ht = HashTableOpenAddressing(capacity=16)
        for i in range(8):
            ht.put(i, i)
        for i in range(4):
            ht.delete(i)
        assert len(ht) == 4
        assert ht.load_factor == pytest.approx(4 / ht.capacity)

    def test_max_load_factor_respected(self) -> None:
        """Table resizes before load factor reaches max_load_factor."""
        ht = HashTableOpenAddressing(capacity=8, max_load_factor=0.5)
        for i in range(20):
            ht.put(i, i)
        # load_factor should never have exceeded max
        assert ht.load_factor <= 0.5

    def test_iter_skips_tombstones(self) -> None:
        """__iter__ yields only live keys."""
        ht = HashTableOpenAddressing(capacity=16)
        for i in range(10):
            ht.put(i, i)
        for i in range(5):
            ht.delete(i)
        result = sorted(ht)
        assert result == list(range(5, 10))


# ---------------------------------------------------------------------------
# TestApplicationScenarios
# ---------------------------------------------------------------------------


class TestApplicationScenarios:
    """Real-world usage patterns — parameterised."""

    @pytest.mark.parametrize("cls", BOTH)
    def test_word_frequency_counter(self, cls: type) -> None:
        """Hash table counts word frequencies correctly."""
        ht = cls()
        words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
        for w in words:
            count = ht.get(w)
            ht.put(w, (count or 0) + 1)
        assert ht.get("apple") == 3
        assert ht.get("banana") == 2
        assert ht.get("cherry") == 1

    @pytest.mark.parametrize("cls", BOTH)
    def test_cache_layer(self, cls: type) -> None:
        """Hash table as a simple key-value cache."""
        cache = cls()
        cache.put("user:1", {"name": "Alice", "age": 30})
        cache.put("user:2", {"name": "Bob", "age": 25})
        assert cache.get("user:1")["name"] == "Alice"  # type: ignore[index]
        assert "user:2" in cache
        assert cache.get("user:99") is None

    @pytest.mark.parametrize("cls", BOTH)
    def test_index_mapping(self, cls: type) -> None:
        """Hash table maps string IDs to integer indices."""
        ht = cls()
        tokens = ["the", "quick", "brown", "fox"]
        for i, t in enumerate(tokens):
            ht.put(t, i)
        assert ht.get("quick") == 1
        assert ht.get("fox") == 3
        assert ht.get("dog") is None

    @pytest.mark.parametrize("cls", BOTH)
    def test_deduplication(self, cls: type) -> None:
        """Hash table deduplicates a list of IDs."""
        ht = cls()
        ids = [1, 2, 3, 2, 1, 4, 3, 5]
        for i in ids:
            ht.put(i, True)
        assert len(ht) == 5
        assert sorted(ht) == [1, 2, 3, 4, 5]


# ---------------------------------------------------------------------------
# TestEdgeCases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    """Boundary conditions — parameterised."""

    @pytest.mark.parametrize("cls", BOTH)
    def test_single_entry_lifecycle(self, cls: type) -> None:
        """Full lifecycle with a single entry."""
        ht = cls()
        ht.put("only", 1)
        assert ht.get("only") == 1
        assert "only" in ht
        assert ht.delete("only") is True
        assert "only" not in ht
        assert len(ht) == 0

    @pytest.mark.parametrize("cls", BOTH)
    def test_zero_key(self, cls: type) -> None:
        """0 is a valid key."""
        ht = cls()
        ht.put(0, "zero")
        assert ht.get(0) == "zero"
        assert 0 in ht

    @pytest.mark.parametrize("cls", BOTH)
    def test_none_value_retrieved(self, cls: type) -> None:
        """Stored None value is retrievable."""
        ht = cls()
        ht.put("k", None)
        assert "k" in ht
        assert ht.get("k") is None

    @pytest.mark.parametrize("cls", BOTH)
    def test_large_bulk(self, cls: type) -> None:
        """1000 inserts complete without error and all are retrievable."""
        ht = cls()
        for i in range(1000):
            ht.put(i, i * 2)
        assert len(ht) == 1000
        for i in range(1000):
            assert ht.get(i) == i * 2

    @pytest.mark.parametrize("cls", BOTH)
    def test_float_value(self, cls: type) -> None:
        """Float values are stored and retrieved correctly."""
        ht = cls()
        ht.put("pi", 3.14159)
        assert ht.get("pi") == pytest.approx(3.14159)

    @pytest.mark.parametrize("cls", BOTH)
    def test_list_value(self, cls: type) -> None:
        """List values are stored and retrieved by reference."""
        ht = cls()
        lst = [1, 2, 3]
        ht.put("lst", lst)
        assert ht.get("lst") is lst


# ---------------------------------------------------------------------------
# TestCollectionInterface
# ---------------------------------------------------------------------------


class TestCollectionInterface:
    """Test Collection interface compliance for both HashTable implementations."""

    @pytest.mark.parametrize("cls", BOTH)
    def test_is_collection(self, cls: type) -> None:
        """HashTable satisfies the Collection interface."""
        from sds.core.interfaces import Collection

        assert isinstance(cls(), Collection)

    @pytest.mark.parametrize("cls", BOTH)
    def test_is_empty_on_new(self, cls: type) -> None:
        """is_empty() returns True on a freshly created table."""
        assert cls().is_empty() is True

    @pytest.mark.parametrize("cls", BOTH)
    def test_is_empty_after_put(self, cls: type) -> None:
        """is_empty() returns False after inserting an entry."""
        ht = cls()
        ht.put("k", "v")
        assert ht.is_empty() is False

    @pytest.mark.parametrize("cls", BOTH)
    def test_is_empty_after_delete_all(self, cls: type) -> None:
        """is_empty() returns True after all entries are deleted."""
        ht = cls()
        ht.put(1, "a")
        ht.delete(1)
        assert ht.is_empty() is True

    @pytest.mark.parametrize("cls", BOTH)
    def test_bool_empty(self, cls: type) -> None:
        """bool(ht) is False when empty."""
        assert not cls()

    @pytest.mark.parametrize("cls", BOTH)
    def test_bool_non_empty(self, cls: type) -> None:
        """bool(ht) is True when non-empty."""
        ht = cls()
        ht.put(1, "a")
        assert ht

    @pytest.mark.parametrize("cls", BOTH)
    def test_clear_empties(self, cls: type) -> None:
        """clear() removes all entries."""
        ht = cls()
        for i in range(5):
            ht.put(i, str(i))
        ht.clear()
        assert len(ht) == 0
        assert ht.is_empty() is True

    @pytest.mark.parametrize("cls", BOTH)
    def test_clear_removes_from_iteration(self, cls: type) -> None:
        """clear() leaves nothing to iterate."""
        ht = cls()
        for i in range(5):
            ht.put(i, i)
        ht.clear()
        assert list(ht) == []

    @pytest.mark.parametrize("cls", BOTH)
    def test_clear_allows_reuse(self, cls: type) -> None:
        """HashTable is fully usable after clear()."""
        ht = cls()
        ht.put(1, "old")
        ht.clear()
        ht.put(2, "new")
        assert ht.get(2) == "new"
        assert ht.get(1) is None
        assert len(ht) == 1
