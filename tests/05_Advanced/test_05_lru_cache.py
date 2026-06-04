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

"""Tests for LRUCache — Least Recently Used cache.

Test Classes
------------
TestLRUCacheCreation
    Instantiation and parameter validation.
TestPut
    put() — insert, update, eviction on overflow.
TestGet
    get() — hit, miss, recency update.
TestEvictionPolicy
    Core LRU eviction ordering guarantees.
TestContains
    __contains__ — membership without recency update.
TestDelete
    delete() — manual removal.
TestClear
    clear() — full reset.
TestPeek
    peek() — value access without recency update.
TestKeys
    keys() — LRU-to-MRU ordering.
TestItems
    items() — ordered iteration.
TestEvictionsCount
    evictions_count tracking.
TestSpecialMethods
    __len__, __repr__, __str__.
TestApplicationScenarios
    Real-world usage patterns.
TestEdgeCases
    Boundary conditions.
"""

import pytest

from sds.advanced import AbstractLRUCache, LRUCache

# ---------------------------------------------------------------------------
# TestLRUCacheCreation
# ---------------------------------------------------------------------------


class TestLRUCacheCreation:
    """Instantiation and parameter validation."""

    def test_default_creation(self) -> None:
        """LRUCache is created empty with the given capacity."""
        cache = LRUCache(capacity=5)
        assert len(cache) == 0
        assert cache.capacity == 5

    def test_capacity_one(self) -> None:
        """capacity=1 is the smallest valid value."""
        cache = LRUCache(capacity=1)
        cache.put(1, "a")
        assert cache.get(1) == "a"

    def test_is_abstract_lru_cache(self) -> None:
        """LRUCache satisfies the AbstractLRUCache interface."""
        assert isinstance(LRUCache(capacity=1), AbstractLRUCache)

    def test_invalid_capacity_zero(self) -> None:
        """capacity=0 raises ValueError."""
        with pytest.raises(ValueError, match="capacity"):
            LRUCache(capacity=0)

    def test_invalid_capacity_negative(self) -> None:
        """Negative capacity raises ValueError."""
        with pytest.raises(ValueError, match="capacity"):
            LRUCache(capacity=-1)

    def test_initial_evictions_zero(self) -> None:
        """No evictions on a freshly created cache."""
        assert LRUCache(capacity=10).evictions_count == 0

    def test_initial_len_zero(self) -> None:
        """Empty cache has length 0."""
        assert len(LRUCache(capacity=10)) == 0

    def test_repr_empty(self) -> None:
        """repr() of empty cache has expected format."""
        assert repr(LRUCache(capacity=3)) == "LRUCache(capacity=3, size=0, evictions=0)"

    def test_str_empty(self) -> None:
        """str() of empty cache has expected format."""
        assert str(LRUCache(capacity=3)) == "LRUCache: 0/3 entries"


# ---------------------------------------------------------------------------
# TestPut
# ---------------------------------------------------------------------------


class TestPut:
    """Test put() — insert, update, capacity enforcement."""

    def test_put_single(self) -> None:
        """Inserting one entry sets len to 1."""
        cache = LRUCache(capacity=3)
        cache.put(1, "one")
        assert len(cache) == 1

    def test_put_up_to_capacity(self) -> None:
        """Inserting capacity entries fills the cache without eviction."""
        cache = LRUCache(capacity=3)
        cache.put(1, "a")
        cache.put(2, "b")
        cache.put(3, "c")
        assert len(cache) == 3
        assert cache.evictions_count == 0

    def test_put_beyond_capacity_evicts(self) -> None:
        """Inserting beyond capacity triggers exactly one eviction."""
        cache = LRUCache(capacity=2)
        cache.put(1, "a")
        cache.put(2, "b")
        cache.put(3, "c")
        assert len(cache) == 2
        assert cache.evictions_count == 1

    def test_put_update_no_eviction(self) -> None:
        """Updating an existing key does not trigger eviction."""
        cache = LRUCache(capacity=2)
        cache.put(1, "a")
        cache.put(1, "A")
        assert len(cache) == 1
        assert cache.evictions_count == 0

    def test_put_update_reflects_new_value(self) -> None:
        """get() returns the updated value after put()."""
        cache = LRUCache(capacity=3)
        cache.put("k", "old")
        cache.put("k", "new")
        assert cache.get("k") == "new"

    def test_put_none_value(self) -> None:
        """Storing None as a value is valid."""
        cache = LRUCache(capacity=2)
        cache.put("null", None)
        assert "null" in cache
        assert cache.get("null") is None

    def test_put_string_keys(self) -> None:
        """String keys are stored and retrieved correctly."""
        cache = LRUCache(capacity=5)
        cache.put("alpha", 1)
        cache.put("beta", 2)
        assert cache.get("alpha") == 1
        assert cache.get("beta") == 2


# ---------------------------------------------------------------------------
# TestGet
# ---------------------------------------------------------------------------


class TestGet:
    """Test get() — hit, miss, recency update."""

    def test_get_existing(self) -> None:
        """get() returns the correct value."""
        cache = LRUCache(capacity=3)
        cache.put(1, "one")
        assert cache.get(1) == "one"

    def test_get_missing(self) -> None:
        """get() returns None for an absent key."""
        cache = LRUCache(capacity=3)
        assert cache.get(99) is None

    def test_get_empty_cache(self) -> None:
        """get() on empty cache returns None."""
        assert LRUCache(capacity=5).get(0) is None

    def test_get_promotes_to_mru(self) -> None:
        """get() moves the accessed entry to MRU position."""
        cache = LRUCache(capacity=2)
        cache.put(1, "a")
        cache.put(2, "b")
        cache.get(1)  # 1 → MRU, 2 → LRU
        cache.put(3, "c")  # evicts 2 (LRU)
        assert cache.get(1) == "a"
        assert cache.get(2) is None

    def test_get_after_delete(self) -> None:
        """get() returns None after the key has been deleted."""
        cache = LRUCache(capacity=3)
        cache.put(1, "a")
        cache.delete(1)
        assert cache.get(1) is None

    def test_get_value_none(self) -> None:
        """get() returns None both for missing keys and None values."""
        cache = LRUCache(capacity=2)
        cache.put("real_none", None)
        # Both cases return None; use __contains__ to distinguish
        assert cache.get("real_none") is None
        assert cache.get("not_there") is None
        assert "real_none" in cache
        assert "not_there" not in cache


# ---------------------------------------------------------------------------
# TestEvictionPolicy
# ---------------------------------------------------------------------------


class TestEvictionPolicy:
    """Core LRU eviction ordering guarantees."""

    def test_lru_evicted_first(self) -> None:
        """The least recently used key is evicted when capacity is reached."""
        cache = LRUCache(capacity=3)
        cache.put(1, "a")
        cache.put(2, "b")
        cache.put(3, "c")
        # Access 1 and 2 → 3 becomes LRU
        cache.get(1)
        cache.get(2)
        cache.put(4, "d")  # evicts 3
        assert cache.get(3) is None
        assert cache.get(1) == "a"
        assert cache.get(2) == "b"
        assert cache.get(4) == "d"

    def test_put_refreshes_recency(self) -> None:
        """put() on an existing key refreshes its recency."""
        cache = LRUCache(capacity=2)
        cache.put(1, "a")
        cache.put(2, "b")
        cache.put(1, "A")  # 1 → MRU
        cache.put(3, "c")  # evicts 2 (LRU)
        assert cache.get(1) == "A"
        assert cache.get(2) is None

    def test_eviction_order_strict(self) -> None:
        """Eviction always follows strict LRU order over many operations."""
        cache = LRUCache(capacity=3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        cache.get("a")  # order: b(LRU), c, a(MRU)
        cache.get("b")  # order: c(LRU), a, b(MRU)
        cache.put("d", 4)  # evicts c
        assert "c" not in cache
        cache.put("e", 5)  # evicts a
        assert "a" not in cache
        cache.put("f", 6)  # evicts b
        assert "b" not in cache

    def test_single_capacity_always_evicts_previous(self) -> None:
        """With capacity=1 every new put evicts the previous entry."""
        cache = LRUCache(capacity=1)
        for i in range(5):
            cache.put(i, str(i))
            assert len(cache) == 1
            assert i in cache
        assert cache.evictions_count == 4

    def test_no_eviction_when_updating(self) -> None:
        """Updating existing keys never triggers eviction."""
        cache = LRUCache(capacity=2)
        cache.put(1, "a")
        cache.put(2, "b")
        for _ in range(10):
            cache.put(1, "x")
            cache.put(2, "y")
        assert cache.evictions_count == 0
        assert len(cache) == 2

    def test_keys_order_reflects_lru_to_mru(self) -> None:
        """keys() lists entries from LRU (index 0) to MRU (last)."""
        cache = LRUCache(capacity=4)
        for k in [1, 2, 3, 4]:
            cache.put(k, k)
        cache.get(2)  # 2 → MRU; order: 1, 3, 4, 2
        cache.get(4)  # 4 → MRU; order: 1, 3, 2, 4
        assert cache.keys() == [1, 3, 2, 4]


# ---------------------------------------------------------------------------
# TestContains
# ---------------------------------------------------------------------------


class TestContains:
    """Test __contains__ — membership without recency side effect."""

    def test_contains_present(self) -> None:
        """A present key is found."""
        cache = LRUCache(capacity=3)
        cache.put(1, "a")
        assert 1 in cache

    def test_contains_absent(self) -> None:
        """An absent key is not found."""
        cache = LRUCache(capacity=3)
        assert 99 not in cache

    def test_contains_does_not_update_recency(self) -> None:
        """__contains__ does not promote the checked key."""
        cache = LRUCache(capacity=2)
        cache.put(1, "a")
        cache.put(2, "b")
        _ = 1 in cache  # 1 is NOT promoted — still LRU
        cache.put(3, "c")  # must evict 1
        assert 1 not in cache

    def test_contains_after_eviction(self) -> None:
        """An evicted key is no longer found."""
        cache = LRUCache(capacity=1)
        cache.put(1, "a")
        cache.put(2, "b")  # evicts 1
        assert 1 not in cache
        assert 2 in cache

    def test_contains_after_delete(self) -> None:
        """A manually deleted key is no longer found."""
        cache = LRUCache(capacity=3)
        cache.put(5, "five")
        cache.delete(5)
        assert 5 not in cache


# ---------------------------------------------------------------------------
# TestDelete
# ---------------------------------------------------------------------------


class TestDelete:
    """Test delete() — manual removal."""

    def test_delete_existing(self) -> None:
        """delete() returns True for a present key."""
        cache = LRUCache(capacity=3)
        cache.put(1, "a")
        assert cache.delete(1) is True

    def test_delete_absent(self) -> None:
        """delete() returns False for an absent key."""
        assert LRUCache(capacity=3).delete(99) is False

    def test_delete_decrements_len(self) -> None:
        """Length decreases after a successful delete."""
        cache = LRUCache(capacity=3)
        cache.put(1, "a")
        cache.put(2, "b")
        cache.delete(1)
        assert len(cache) == 1

    def test_delete_does_not_count_as_eviction(self) -> None:
        """Manual delete does not increment evictions_count."""
        cache = LRUCache(capacity=3)
        cache.put(1, "a")
        cache.delete(1)
        assert cache.evictions_count == 0

    def test_delete_allows_reinsert(self) -> None:
        """A deleted key can be re-inserted."""
        cache = LRUCache(capacity=2)
        cache.put(1, "first")
        cache.delete(1)
        cache.put(1, "second")
        assert cache.get(1) == "second"

    def test_delete_idempotent(self) -> None:
        """Deleting the same key twice: first True, then False."""
        cache = LRUCache(capacity=2)
        cache.put(7, "seven")
        assert cache.delete(7) is True
        assert cache.delete(7) is False

    def test_delete_lru_node(self) -> None:
        """Deleting the LRU node and inserting doesn't corrupt order."""
        cache = LRUCache(capacity=3)
        cache.put(1, "a")
        cache.put(2, "b")
        cache.put(3, "c")
        cache.delete(1)  # remove current LRU
        cache.put(4, "d")  # should NOT evict anything (slot freed)
        assert len(cache) == 3
        assert cache.evictions_count == 0


# ---------------------------------------------------------------------------
# TestClear
# ---------------------------------------------------------------------------


class TestClear:
    """Test clear() — full reset."""

    def test_clear_empties_cache(self) -> None:
        """clear() removes all entries."""
        cache = LRUCache(capacity=5)
        for i in range(5):
            cache.put(i, str(i))
        cache.clear()
        assert len(cache) == 0

    def test_clear_no_eviction_count(self) -> None:
        """clear() does not increment evictions_count."""
        cache = LRUCache(capacity=3)
        cache.put(1, "a")
        cache.put(2, "b")
        cache.clear()
        assert cache.evictions_count == 0

    def test_clear_allows_reuse(self) -> None:
        """Cache is fully usable after clear()."""
        cache = LRUCache(capacity=2)
        cache.put(1, "a")
        cache.clear()
        cache.put(2, "b")
        cache.put(3, "c")
        assert len(cache) == 2
        assert cache.get(2) == "b"

    def test_clear_on_empty(self) -> None:
        """clear() on an already empty cache is a no-op."""
        cache = LRUCache(capacity=3)
        cache.clear()
        assert len(cache) == 0


# ---------------------------------------------------------------------------
# TestPeek
# ---------------------------------------------------------------------------


class TestPeek:
    """Test peek() — value access without recency update."""

    def test_peek_existing(self) -> None:
        """peek() returns the value without error."""
        cache = LRUCache(capacity=2)
        cache.put(1, "a")
        assert cache.peek(1) == "a"

    def test_peek_absent(self) -> None:
        """peek() returns None for absent key."""
        cache = LRUCache(capacity=2)
        assert cache.peek(99) is None

    def test_peek_does_not_promote(self) -> None:
        """peek() leaves the LRU order unchanged."""
        cache = LRUCache(capacity=2)
        cache.put(1, "a")
        cache.put(2, "b")
        cache.peek(1)  # 1 should stay LRU
        cache.put(3, "c")  # evicts 1
        assert 1 not in cache


# ---------------------------------------------------------------------------
# TestKeys
# ---------------------------------------------------------------------------


class TestKeys:
    """Test keys() — LRU-to-MRU ordering."""

    def test_keys_empty(self) -> None:
        """keys() returns empty list for empty cache."""
        assert LRUCache(capacity=3).keys() == []

    def test_keys_insertion_order(self) -> None:
        """Without gets, keys are in insertion order (oldest first)."""
        cache = LRUCache(capacity=3)
        cache.put(1, "a")
        cache.put(2, "b")
        cache.put(3, "c")
        assert cache.keys() == [1, 2, 3]

    def test_keys_after_get(self) -> None:
        """get() moves the accessed key to MRU (last in keys())."""
        cache = LRUCache(capacity=3)
        cache.put(1, "a")
        cache.put(2, "b")
        cache.put(3, "c")
        cache.get(1)
        assert cache.keys() == [2, 3, 1]

    def test_keys_length_matches_len(self) -> None:
        """len(cache.keys()) equals len(cache)."""
        cache = LRUCache(capacity=4)
        for i in range(4):
            cache.put(i, i)
        assert len(cache.keys()) == len(cache)


# ---------------------------------------------------------------------------
# TestItems
# ---------------------------------------------------------------------------


class TestItems:
    """Test items() — ordered (key, value) pairs."""

    def test_items_empty(self) -> None:
        """items() yields nothing on empty cache."""
        assert list(LRUCache(capacity=3).items()) == []

    def test_items_order(self) -> None:
        """items() yields pairs in LRU → MRU order."""
        cache = LRUCache(capacity=3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        cache.get("a")  # a → MRU
        assert list(cache.items()) == [("b", 2), ("c", 3), ("a", 1)]

    def test_items_values_correct(self) -> None:
        """items() returns correct values for all entries."""
        cache = LRUCache(capacity=3)
        cache.put(1, "one")
        cache.put(2, "two")
        d = dict(cache.items())
        assert d[1] == "one"
        assert d[2] == "two"


# ---------------------------------------------------------------------------
# TestEvictionsCount
# ---------------------------------------------------------------------------


class TestEvictionsCount:
    """Test evictions_count tracking."""

    def test_no_eviction_under_capacity(self) -> None:
        """No evictions when insertions stay within capacity."""
        cache = LRUCache(capacity=5)
        for i in range(5):
            cache.put(i, i)
        assert cache.evictions_count == 0

    def test_one_eviction_at_overflow(self) -> None:
        """One eviction occurs when capacity + 1 items are inserted."""
        cache = LRUCache(capacity=3)
        for i in range(4):
            cache.put(i, i)
        assert cache.evictions_count == 1

    def test_evictions_accumulate(self) -> None:
        """Evictions count accumulates over multiple overflows."""
        cache = LRUCache(capacity=2)
        for i in range(10):
            cache.put(i, i)
        assert cache.evictions_count == 8

    def test_update_no_eviction(self) -> None:
        """Repeated updates to existing keys never increment evictions."""
        cache = LRUCache(capacity=2)
        cache.put(1, "a")
        cache.put(2, "b")
        for _ in range(20):
            cache.put(1, "x")
        assert cache.evictions_count == 0

    def test_evictions_not_reset_by_clear(self) -> None:
        """evictions_count is not reset by clear()."""
        cache = LRUCache(capacity=1)
        cache.put(1, "a")
        cache.put(2, "b")  # evicts 1
        cache.clear()
        assert cache.evictions_count == 1


# ---------------------------------------------------------------------------
# TestSpecialMethods
# ---------------------------------------------------------------------------


class TestSpecialMethods:
    """Test __len__, __repr__, __str__."""

    def test_len_empty(self) -> None:
        """len() is 0 on empty cache."""
        assert len(LRUCache(capacity=5)) == 0

    def test_len_after_inserts(self) -> None:
        """len() equals the number of distinct keys stored."""
        cache = LRUCache(capacity=5)
        for i in range(4):
            cache.put(i, i)
        assert len(cache) == 4

    def test_len_capped_at_capacity(self) -> None:
        """len() never exceeds capacity."""
        cache = LRUCache(capacity=3)
        for i in range(10):
            cache.put(i, i)
        assert len(cache) == 3

    def test_repr_format(self) -> None:
        """repr() matches expected format."""
        cache = LRUCache(capacity=4)
        cache.put(1, "a")
        assert repr(cache) == "LRUCache(capacity=4, size=1, evictions=0)"

    def test_repr_evictions(self) -> None:
        """repr() reflects eviction count."""
        cache = LRUCache(capacity=1)
        cache.put(1, "a")
        cache.put(2, "b")
        assert "evictions=1" in repr(cache)

    def test_str_format(self) -> None:
        """str() shows size/capacity."""
        cache = LRUCache(capacity=3)
        cache.put(1, "a")
        cache.put(2, "b")
        assert str(cache) == "LRUCache: 2/3 entries"


# ---------------------------------------------------------------------------
# TestApplicationScenarios
# ---------------------------------------------------------------------------


class TestApplicationScenarios:
    """Real-world usage patterns."""

    def test_database_query_cache(self) -> None:
        """LRU cache for database query results."""
        cache = LRUCache(capacity=3)
        # Simulate caching query results
        cache.put("SELECT * FROM users WHERE id=1", {"id": 1, "name": "Alice"})
        cache.put("SELECT * FROM users WHERE id=2", {"id": 2, "name": "Bob"})
        cache.put("SELECT * FROM users WHERE id=3", {"id": 3, "name": "Carol"})

        result = cache.get("SELECT * FROM users WHERE id=1")
        assert result is not None
        assert result["name"] == "Alice"  # type: ignore[index]

    def test_web_page_cache(self) -> None:
        """Browser-style page cache with limited slots."""
        cache = LRUCache(capacity=3)
        pages = {
            "/home": "<html>home</html>",
            "/about": "<html>about</html>",
            "/contact": "<html>contact</html>",
        }
        for url, content in pages.items():
            cache.put(url, content)

        cache.get("/home")  # /home → MRU
        cache.put("/blog", "<html>blog</html>")  # evicts /about
        assert "/about" not in cache
        assert "/home" in cache

    def test_memoisation(self) -> None:
        """LRU cache as a memoisation layer for an expensive function."""
        cache = LRUCache(capacity=5)
        call_count = [0]

        def expensive(n: int) -> int:
            cached = cache.get(n)
            if cached is not None:
                return cached  # type: ignore[return-value]
            call_count[0] += 1
            result = n * n
            cache.put(n, result)
            return result

        for _ in range(3):
            assert expensive(4) == 16
        # Only computed once
        assert call_count[0] == 1

    def test_access_pattern_working_set(self) -> None:
        """Working-set access pattern keeps hot keys in cache.

        Uses capacity = len(hot_keys) + 1 so that one cold slot is always
        available. Hot keys are promoted to MRU before each cold insert,
        ensuring the single cold slot is the one evicted next round.
        """
        hot_keys = list(range(4))
        cache = LRUCache(capacity=len(hot_keys) + 1)  # capacity=5, 1 cold slot

        for k in hot_keys:
            cache.put(k, k)

        cold_keys = list(range(100, 115))
        for cold in cold_keys:
            # Promote all hot keys so the cold slot (if occupied) is LRU
            for h in hot_keys:
                cache.get(h)
            cache.put(cold, cold)  # occupies the 5th slot; evicted next round

        for h in hot_keys:
            assert h in cache, f"Hot key {h} evicted unexpectedly"


# ---------------------------------------------------------------------------
# TestEdgeCases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    """Boundary conditions."""

    def test_capacity_one_lifecycle(self) -> None:
        """Full lifecycle with capacity=1."""
        cache = LRUCache(capacity=1)
        cache.put(1, "a")
        assert cache.get(1) == "a"
        cache.put(2, "b")
        assert cache.get(1) is None
        assert cache.get(2) == "b"

    def test_put_get_interleaved(self) -> None:
        """Interleaved puts and gets maintain correct order."""
        cache = LRUCache(capacity=3)
        cache.put(1, "a")
        cache.put(2, "b")
        cache.get(1)  # 1 → MRU
        cache.put(3, "c")
        cache.get(2)  # 2 → MRU
        cache.put(4, "d")  # evicts 1 (LRU after 3 was inserted)
        assert cache.get(1) is None
        assert cache.get(2) == "b"
        assert cache.get(3) == "c"
        assert cache.get(4) == "d"

    def test_large_capacity(self) -> None:
        """1000 inserts on a large cache are all retrievable."""
        cache = LRUCache(capacity=1000)
        for i in range(1000):
            cache.put(i, i * 2)
        assert len(cache) == 1000
        for i in range(1000):
            assert cache.get(i) == i * 2

    def test_tuple_keys(self) -> None:
        """Tuple keys are hashable and work correctly."""
        cache = LRUCache(capacity=3)
        cache.put((1, 2), "pair")
        assert cache.get((1, 2)) == "pair"

    def test_none_value_distinct_from_miss(self) -> None:
        """peek() + __contains__ distinguish None value from cache miss."""
        cache = LRUCache(capacity=2)
        cache.put("k", None)
        assert "k" in cache
        assert cache.peek("k") is None
        assert "missing" not in cache
        assert cache.peek("missing") is None

    def test_many_evictions_correct_content(self) -> None:
        """After 100 evictions on a size-3 cache, content is always correct."""
        cache = LRUCache(capacity=3)
        for i in range(103):
            cache.put(i, str(i))
        # Last 3 insertions should be present
        for i in range(100, 103):
            assert cache.get(i) == str(i)
        assert cache.evictions_count == 100


# ---------------------------------------------------------------------------
# TestCollectionInterface
# ---------------------------------------------------------------------------


class TestCollectionInterface:
    """Test Collection interface compliance for LRUCache."""

    def test_is_collection(self) -> None:
        """LRUCache satisfies the Collection interface."""
        from sds.core.interfaces import Collection

        assert isinstance(LRUCache(capacity=1), Collection)

    def test_is_empty_on_new(self) -> None:
        """is_empty() returns True on a freshly created cache."""
        assert LRUCache(capacity=5).is_empty() is True

    def test_is_empty_after_put(self) -> None:
        """is_empty() returns False after inserting an entry."""
        cache = LRUCache(capacity=5)
        cache.put(1, "a")
        assert cache.is_empty() is False

    def test_is_empty_after_delete_all(self) -> None:
        """is_empty() returns True after all entries are deleted."""
        cache = LRUCache(capacity=5)
        cache.put(1, "a")
        cache.delete(1)
        assert cache.is_empty() is True

    def test_bool_empty(self) -> None:
        """bool(cache) is False when empty."""
        assert not LRUCache(capacity=3)

    def test_bool_non_empty(self) -> None:
        """bool(cache) is True when non-empty."""
        cache = LRUCache(capacity=3)
        cache.put(1, "a")
        assert cache

    def test_iter_lru_to_mru(self) -> None:
        """__iter__ yields keys from LRU to MRU."""
        cache = LRUCache(capacity=3)
        cache.put(1, "a")
        cache.put(2, "b")
        cache.put(3, "c")
        cache.get(1)  # 1 → MRU
        assert list(cache) == [2, 3, 1]

    def test_iter_empty(self) -> None:
        """Iterating an empty cache yields nothing."""
        assert list(LRUCache(capacity=3)) == []

    def test_iter_consistent_with_keys(self) -> None:
        """__iter__ and keys() return the same sequence."""
        cache = LRUCache(capacity=4)
        for i in [1, 2, 3, 4]:
            cache.put(i, i)
        cache.get(2)
        assert list(cache) == cache.keys()
