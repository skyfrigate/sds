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

"""Tests for CountMinSketch frequency estimation structure.

Test Classes
------------
TestCountMinSketchCreation
    Instantiation via epsilon/delta and from_dimensions.
TestAdd
    add() — single item, bulk count, total tracking.
TestFrequency
    frequency() — correctness, no false negatives, zero for unseen.
TestContains
    __contains__ — membership without underestimation.
TestProbabilisticGuarantees
    No false negatives; additive error within theoretical bounds.
TestMerge
    merge() — stream union, dimension mismatch.
TestCollectionInterface
    is_empty, clear, __iter__, __bool__, Collection compliance.
TestSpecialMethods
    __len__, __repr__, __str__.
TestApplicationScenarios
    Real-world usage patterns.
TestEdgeCases
    Boundary conditions: single item, high frequency, unicode.
"""

import random
import string

import pytest

from sds.advanced import CountMinSketch
from sds.core.interfaces import Collection

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _random_words(n: int, length: int = 6) -> list[str]:
    """Generate n distinct random lowercase words."""
    words: set[str] = set()
    while len(words) < n:
        words.add("".join(random.choices(string.ascii_lowercase, k=length)))
    return list(words)


# ---------------------------------------------------------------------------
# TestCountMinSketchCreation
# ---------------------------------------------------------------------------


class TestCountMinSketchCreation:
    """Instantiation and parameter validation."""

    def test_epsilon_delta_dimensions(self) -> None:
        """epsilon=0.01, delta=0.05 produce correct w and d."""
        cms = CountMinSketch(epsilon=0.01, delta=0.05)
        assert cms.width == 272  # ceil(e / 0.01)
        assert cms.depth == 3  # ceil(ln(20))

    def test_from_dimensions_basic(self) -> None:
        """from_dimensions stores width and depth correctly."""
        cms = CountMinSketch.from_dimensions(width=200, depth=5)
        assert cms.width == 200
        assert cms.depth == 5

    def test_from_dimensions_minimal(self) -> None:
        """from_dimensions(1, 1) is the smallest valid sketch."""
        cms = CountMinSketch.from_dimensions(width=1, depth=1)
        assert cms.width == 1 and cms.depth == 1

    def test_is_collection(self) -> None:
        """CountMinSketch satisfies the Collection interface."""
        assert isinstance(CountMinSketch(epsilon=0.1, delta=0.1), Collection)

    def test_initial_total_zero(self) -> None:
        """A freshly created sketch has total == 0."""
        assert CountMinSketch(epsilon=0.1, delta=0.1).total == 0

    def test_initial_len_zero(self) -> None:
        """len() is 0 on a fresh sketch."""
        assert len(CountMinSketch(epsilon=0.1, delta=0.1)) == 0

    def test_invalid_epsilon_zero(self) -> None:
        """epsilon=0.0 raises ValueError."""
        with pytest.raises(ValueError, match="epsilon"):
            CountMinSketch(epsilon=0.0, delta=0.1)

    def test_invalid_epsilon_one(self) -> None:
        """epsilon=1.0 raises ValueError."""
        with pytest.raises(ValueError, match="epsilon"):
            CountMinSketch(epsilon=1.0, delta=0.1)

    def test_invalid_delta_zero(self) -> None:
        """delta=0.0 raises ValueError."""
        with pytest.raises(ValueError, match="delta"):
            CountMinSketch(epsilon=0.1, delta=0.0)

    def test_invalid_delta_one(self) -> None:
        """delta=1.0 raises ValueError."""
        with pytest.raises(ValueError, match="delta"):
            CountMinSketch(epsilon=0.1, delta=1.0)

    def test_from_dimensions_invalid_width(self) -> None:
        """from_dimensions(width=0, ...) raises ValueError."""
        with pytest.raises(ValueError, match="width"):
            CountMinSketch.from_dimensions(width=0, depth=3)

    def test_from_dimensions_invalid_depth(self) -> None:
        """from_dimensions(..., depth=0) raises ValueError."""
        with pytest.raises(ValueError, match="depth"):
            CountMinSketch.from_dimensions(width=100, depth=0)


# ---------------------------------------------------------------------------
# TestAdd
# ---------------------------------------------------------------------------


class TestAdd:
    """Test the add() operation."""

    def test_add_single(self) -> None:
        """Adding one item increments total to 1."""
        cms = CountMinSketch.from_dimensions(100, 4)
        cms.add("x")
        assert cms.total == 1
        assert len(cms) == 1

    def test_add_multiple_distinct(self) -> None:
        """Adding n distinct items sets total to n."""
        cms = CountMinSketch.from_dimensions(200, 5)
        for w in ["a", "b", "c", "d"]:
            cms.add(w)
        assert cms.total == 4

    def test_add_same_item_multiple_times(self) -> None:
        """Adding the same item k times sets total to k."""
        cms = CountMinSketch.from_dimensions(100, 4)
        for _ in range(10):
            cms.add("dup")
        assert cms.total == 10

    def test_add_with_count(self) -> None:
        """add(item, count=k) is equivalent to k individual adds."""
        cms1 = CountMinSketch.from_dimensions(100, 4)
        cms2 = CountMinSketch.from_dimensions(100, 4)
        for _ in range(7):
            cms1.add("x")
        cms2.add("x", count=7)
        assert cms1.frequency("x") == cms2.frequency("x")
        assert cms1.total == cms2.total

    def test_add_count_invalid(self) -> None:
        """add with count < 1 raises ValueError."""
        cms = CountMinSketch.from_dimensions(100, 3)
        with pytest.raises(ValueError, match="count"):
            cms.add("x", count=0)

    def test_add_integer(self) -> None:
        """Integer items are accepted."""
        cms = CountMinSketch.from_dimensions(100, 3)
        cms.add(42)
        assert cms.frequency(42) >= 1

    def test_add_float(self) -> None:
        """Float items are accepted."""
        cms = CountMinSketch.from_dimensions(100, 3)
        cms.add(3.14)
        assert cms.frequency(3.14) >= 1

    def test_add_tuple(self) -> None:
        """Tuple items are accepted."""
        cms = CountMinSketch.from_dimensions(100, 3)
        cms.add((1, 2, 3))
        assert cms.frequency((1, 2, 3)) >= 1


# ---------------------------------------------------------------------------
# TestFrequency
# ---------------------------------------------------------------------------


class TestFrequency:
    """Test frequency() — correctness and guarantees."""

    def test_frequency_unseen_item(self) -> None:
        """frequency() returns 0 for an item never added."""
        cms = CountMinSketch.from_dimensions(100, 4)
        assert cms.frequency("ghost") == 0

    def test_frequency_single_item(self) -> None:
        """frequency() returns ≥ 1 after adding an item once."""
        cms = CountMinSketch.from_dimensions(100, 4)
        cms.add("hello")
        assert cms.frequency("hello") >= 1

    def test_frequency_exact_for_large_sketch(self) -> None:
        """On a very large sketch, frequency() equals the true count."""
        cms = CountMinSketch.from_dimensions(10000, 10)
        for _ in range(42):
            cms.add("target")
        assert cms.frequency("target") == 42

    def test_frequency_no_underestimate(self) -> None:
        """frequency() is always ≥ true count (no false negatives)."""
        words = _random_words(100)
        counts = {w: random.randint(1, 20) for w in words}
        cms = CountMinSketch(epsilon=0.001, delta=0.001)
        for w, c in counts.items():
            cms.add(w, count=c)
        for w, c in counts.items():
            assert cms.frequency(w) >= c, f"Underestimate for {w}"

    def test_frequency_after_clear(self) -> None:
        """frequency() returns 0 for all items after clear()."""
        cms = CountMinSketch.from_dimensions(100, 4)
        cms.add("x", 5)
        cms.clear()
        assert cms.frequency("x") == 0

    def test_frequency_monotone_with_adds(self) -> None:
        """frequency() is non-decreasing as the same item is added."""
        cms = CountMinSketch.from_dimensions(200, 5)
        prev = 0
        for i in range(1, 11):
            cms.add("item")
            freq = cms.frequency("item")
            assert freq >= prev
            prev = freq


# ---------------------------------------------------------------------------
# TestContains
# ---------------------------------------------------------------------------


class TestContains:
    """Test __contains__ — membership without underestimation."""

    def test_contains_added_item(self) -> None:
        """An added item is always found."""
        cms = CountMinSketch.from_dimensions(100, 4)
        cms.add("present")
        assert "present" in cms

    def test_contains_unseen_item_empty(self) -> None:
        """An unseen item is not in a fresh sketch."""
        cms = CountMinSketch.from_dimensions(100, 4)
        assert "ghost" not in cms

    def test_contains_after_clear(self) -> None:
        """An added item is no longer found after clear()."""
        cms = CountMinSketch.from_dimensions(100, 4)
        cms.add("x")
        cms.clear()
        assert "x" not in cms

    def test_no_false_negatives_contains(self) -> None:
        """All 50 added items are found via __contains__."""
        words = _random_words(50)
        cms = CountMinSketch(epsilon=0.01, delta=0.01)
        for w in words:
            cms.add(w)
        fn = [w for w in words if w not in cms]
        assert fn == [], f"False negatives: {fn}"


# ---------------------------------------------------------------------------
# TestProbabilisticGuarantees
# ---------------------------------------------------------------------------


class TestProbabilisticGuarantees:
    """Core probabilistic properties of CountMinSketch."""

    def test_no_false_negatives_small(self) -> None:
        """No false negatives on 100 items with well-sized sketch."""
        words = _random_words(100)
        cms = CountMinSketch(epsilon=0.01, delta=0.01)
        for w in words:
            cms.add(w)
        fn = [w for w in words if cms.frequency(w) < 1]
        assert fn == []

    def test_no_false_negatives_with_counts(self) -> None:
        """frequency() ≥ true count for all items."""
        items = {"a": 10, "b": 5, "c": 20, "d": 1}
        cms = CountMinSketch(epsilon=0.001, delta=0.001)
        for item, count in items.items():
            cms.add(item, count=count)
        for item, count in items.items():
            assert cms.frequency(item) >= count

    def test_additive_error_bound(self) -> None:
        """Overestimate is bounded by ε × N for large sketches."""
        n = 500
        words = _random_words(n)
        epsilon = 0.05
        cms = CountMinSketch(epsilon=epsilon, delta=0.001)
        for w in words:
            cms.add(w)
        N = cms.total
        overestimates = [
            cms.frequency(w) - 1 for w in words  # true count = 1 for each distinct word
        ]
        # Most overestimates should be < epsilon * N
        within_bound = sum(1 for e in overestimates if e <= epsilon * N)
        # At least 90% should satisfy the bound (conservative threshold)
        assert within_bound / n >= 0.9

    def test_frequent_item_dominates(self) -> None:
        """A highly frequent item is estimated at least as its true count."""
        cms = CountMinSketch.from_dimensions(1000, 7)
        cms.add("hot", count=1000)
        for _ in range(500):
            cms.add("cold")
        assert cms.frequency("hot") >= 1000


# ---------------------------------------------------------------------------
# TestMerge
# ---------------------------------------------------------------------------


class TestMerge:
    """Test merge() — stream union."""

    def test_merge_sums_frequencies(self) -> None:
        """Merged sketch reports at least the sum of individual counts."""
        cms1 = CountMinSketch.from_dimensions(200, 5)
        cms2 = CountMinSketch.from_dimensions(200, 5)
        cms1.add("x", 3)
        cms2.add("x", 2)
        merged = cms1.merge(cms2)
        assert merged.frequency("x") >= 5

    def test_merge_total_is_sum(self) -> None:
        """Merged total equals the sum of both totals."""
        cms1 = CountMinSketch.from_dimensions(200, 5)
        cms2 = CountMinSketch.from_dimensions(200, 5)
        cms1.add("a", 4)
        cms2.add("b", 6)
        merged = cms1.merge(cms2)
        assert merged.total == 10
        assert len(merged) == 10

    def test_merge_does_not_mutate_sources(self) -> None:
        """merge() returns a new sketch without modifying the originals."""
        cms1 = CountMinSketch.from_dimensions(100, 4)
        cms2 = CountMinSketch.from_dimensions(100, 4)
        cms1.add("x", 5)
        cms2.add("y", 3)
        t1, t2 = cms1.total, cms2.total
        cms1.merge(cms2)
        assert cms1.total == t1
        assert cms2.total == t2

    def test_merge_with_empty(self) -> None:
        """Merging with an empty sketch preserves all frequencies."""
        cms = CountMinSketch.from_dimensions(100, 4)
        cms.add("z", 7)
        empty = CountMinSketch.from_dimensions(100, 4)
        merged = cms.merge(empty)
        assert merged.frequency("z") >= 7

    def test_merge_mismatched_width_raises(self) -> None:
        """merge() raises ValueError when widths differ."""
        cms1 = CountMinSketch.from_dimensions(100, 4)
        cms2 = CountMinSketch.from_dimensions(200, 4)
        with pytest.raises(ValueError):
            cms1.merge(cms2)

    def test_merge_mismatched_depth_raises(self) -> None:
        """merge() raises ValueError when depths differ."""
        cms1 = CountMinSketch.from_dimensions(100, 4)
        cms2 = CountMinSketch.from_dimensions(100, 5)
        with pytest.raises(ValueError):
            cms1.merge(cms2)

    def test_merge_no_false_negatives(self) -> None:
        """All items from both sources are found in the merged sketch."""
        words_a = _random_words(30, length=8)
        words_b = _random_words(30, length=9)
        cms1 = CountMinSketch.from_dimensions(1000, 5)
        cms2 = CountMinSketch.from_dimensions(1000, 5)
        for w in words_a:
            cms1.add(w)
        for w in words_b:
            cms2.add(w)
        merged = cms1.merge(cms2)
        for w in words_a + words_b:
            assert merged.frequency(w) >= 1


# ---------------------------------------------------------------------------
# TestCollectionInterface
# ---------------------------------------------------------------------------


class TestCollectionInterface:
    """Test Collection interface compliance for CountMinSketch."""

    def test_is_collection(self) -> None:
        """CountMinSketch is a Collection."""
        assert isinstance(CountMinSketch(epsilon=0.1, delta=0.1), Collection)

    def test_is_empty_on_new(self) -> None:
        """is_empty() returns True on a fresh sketch."""
        assert CountMinSketch(epsilon=0.1, delta=0.1).is_empty() is True

    def test_is_empty_after_add(self) -> None:
        """is_empty() returns False after adding an item."""
        cms = CountMinSketch(epsilon=0.1, delta=0.1)
        cms.add("x")
        assert cms.is_empty() is False

    def test_bool_empty(self) -> None:
        """bool(cms) is False when empty."""
        assert not CountMinSketch(epsilon=0.1, delta=0.1)

    def test_bool_non_empty(self) -> None:
        """bool(cms) is True after adding an item."""
        cms = CountMinSketch(epsilon=0.1, delta=0.1)
        cms.add("x")
        assert cms

    def test_clear_resets_total(self) -> None:
        """clear() resets total to 0."""
        cms = CountMinSketch(epsilon=0.1, delta=0.1)
        cms.add("a", count=5)
        cms.clear()
        assert cms.total == 0
        assert cms.is_empty() is True

    def test_clear_resets_counters(self) -> None:
        """clear() resets all counters so frequency returns 0."""
        cms = CountMinSketch.from_dimensions(100, 4)
        cms.add("x", 10)
        cms.clear()
        assert cms.frequency("x") == 0

    def test_clear_allows_reuse(self) -> None:
        """Sketch is fully usable after clear()."""
        cms = CountMinSketch.from_dimensions(100, 4)
        cms.add("old", 5)
        cms.clear()
        cms.add("new", 3)
        assert cms.frequency("new") >= 3
        assert cms.total == 3

    def test_iter_raises_type_error(self) -> None:
        """__iter__ raises TypeError."""
        cms = CountMinSketch.from_dimensions(100, 4)
        cms.add("x")
        with pytest.raises(TypeError):
            list(cms)


# ---------------------------------------------------------------------------
# TestSpecialMethods
# ---------------------------------------------------------------------------


class TestSpecialMethods:
    """Test __len__, __repr__, __str__."""

    def test_len_empty(self) -> None:
        """len() is 0 on a fresh sketch."""
        assert len(CountMinSketch(epsilon=0.1, delta=0.1)) == 0

    def test_len_after_adds(self) -> None:
        """len() equals total items added."""
        cms = CountMinSketch.from_dimensions(100, 4)
        cms.add("a", 3)
        cms.add("b", 2)
        assert len(cms) == 5

    def test_repr_format(self) -> None:
        """repr() matches expected format."""
        cms = CountMinSketch.from_dimensions(100, 5)
        assert repr(cms) == "CountMinSketch(width=100, depth=5, total=0)"

    def test_repr_after_add(self) -> None:
        """repr() reflects updated total."""
        cms = CountMinSketch.from_dimensions(100, 5)
        cms.add("x", 3)
        assert "total=3" in repr(cms)

    def test_str_format(self) -> None:
        """str() mentions items and matrix dimensions."""
        cms = CountMinSketch.from_dimensions(100, 5)
        cms.add("x", 2)
        s = str(cms)
        assert "2" in s
        assert "5" in s
        assert "100" in s


# ---------------------------------------------------------------------------
# TestApplicationScenarios
# ---------------------------------------------------------------------------


class TestApplicationScenarios:
    """Real-world usage patterns."""

    def test_word_frequency_stream(self) -> None:
        """Estimate word frequencies in a text stream."""
        stream = ["the", "cat", "sat", "on", "the", "mat", "the", "cat"]
        cms = CountMinSketch(epsilon=0.01, delta=0.01)
        for word in stream:
            cms.add(word)
        assert cms.frequency("the") >= 3
        assert cms.frequency("cat") >= 2
        assert cms.frequency("dog") == 0
        assert len(cms) == len(stream)

    def test_top_item_detection(self) -> None:
        """Detect the most frequent item in a stream."""
        cms = CountMinSketch(epsilon=0.001, delta=0.001)
        items = ["a"] * 100 + ["b"] * 50 + ["c"] * 10
        random.shuffle(items)
        for item in items:
            cms.add(item)
        # "a" must have the highest estimate
        assert cms.frequency("a") >= cms.frequency("b")
        assert cms.frequency("a") >= cms.frequency("c")

    def test_network_traffic_monitoring(self) -> None:
        """Track packet source frequencies in a network stream."""
        cms = CountMinSketch(epsilon=0.01, delta=0.01)
        ips = [f"192.168.1.{i}" for i in range(10)]
        # One IP sends many more packets
        heavy_hitter = "192.168.1.0"
        for ip in ips:
            count = 100 if ip == heavy_hitter else 5
            cms.add(ip, count=count)
        assert cms.frequency(heavy_hitter) >= 100
        for ip in ips:
            assert cms.frequency(ip) >= 5

    def test_merge_distributed_streams(self) -> None:
        """Merge frequency sketches from two distributed nodes."""
        node1 = CountMinSketch.from_dimensions(500, 5)
        node2 = CountMinSketch.from_dimensions(500, 5)
        shared_items = _random_words(20, length=5)
        for w in shared_items:
            node1.add(w, 3)
            node2.add(w, 2)
        combined = node1.merge(node2)
        for w in shared_items:
            assert combined.frequency(w) >= 5

    def test_cache_miss_detection(self) -> None:
        """Use sketch to detect items not yet cached."""
        cache_hits = _random_words(50)
        cms = CountMinSketch(epsilon=0.01, delta=0.01)
        for item in cache_hits:
            cms.add(item)
        # All cached items are detected
        for item in cache_hits:
            assert item in cms
        # A fresh item has 0 frequency
        fresh = "zzzzzzz_definitely_not_cached"
        assert cms.frequency(fresh) == 0


# ---------------------------------------------------------------------------
# TestEdgeCases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    """Boundary conditions."""

    def test_single_item_sketch(self) -> None:
        """from_dimensions(1, 1) estimates all items as the same counter."""
        cms = CountMinSketch.from_dimensions(width=1, depth=1)
        cms.add("a", 5)
        cms.add("b", 3)
        # With width=1 everything maps to column 0, so frequency >= true count
        assert cms.frequency("a") >= 5
        assert cms.frequency("b") >= 3

    def test_high_frequency_single_item(self) -> None:
        """add(item, count=10000) is handled correctly."""
        cms = CountMinSketch.from_dimensions(1000, 5)
        cms.add("massive", count=10_000)
        assert cms.frequency("massive") >= 10_000
        assert cms.total == 10_000

    def test_unicode_items(self) -> None:
        """Unicode items are handled correctly."""
        cms = CountMinSketch.from_dimensions(200, 5)
        items = ["café", "日本語", "العربية", "emoji🌍"]
        for item in items:
            cms.add(item, 2)
        for item in items:
            assert cms.frequency(item) >= 2

    def test_many_items_no_false_negatives(self) -> None:
        """500 distinct items added once each — no false negatives."""
        words = _random_words(500, length=10)
        cms = CountMinSketch(epsilon=0.01, delta=0.01)
        for w in words:
            cms.add(w)
        fn = [w for w in words if w not in cms]
        assert fn == []

    def test_add_count_one_vs_explicit(self) -> None:
        """add(x) and add(x, count=1) are equivalent."""
        cms1 = CountMinSketch.from_dimensions(100, 4)
        cms2 = CountMinSketch.from_dimensions(100, 4)
        cms1.add("x")
        cms2.add("x", count=1)
        assert cms1.frequency("x") == cms2.frequency("x")
        assert cms1.total == cms2.total

    def test_merge_with_self(self) -> None:
        """Merging a sketch with itself doubles all frequencies."""
        cms = CountMinSketch.from_dimensions(200, 5)
        cms.add("x", 4)
        merged = cms.merge(cms)
        assert merged.frequency("x") >= 8
        assert merged.total == 2 * cms.total
