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

"""Tests for BloomFilter probabilistic data structure.

This module contains comprehensive tests for the BloomFilter implementation,
verifying correctness, probabilistic guarantees, edge cases, and API contracts.

Test Classes
------------
TestBloomFilterCreation
    Instantiation and parameter validation.
TestOptimalParams
    Static method for optimal parameter calculation.
TestAdd
    The add() operation.
TestContains
    The __contains__ / membership test operation.
TestProbabilisticGuarantees
    No false negatives; controlled false positive rate.
TestFillRatio
    estimated_fill_ratio() and estimated_fp_rate().
TestUnion
    union() operation between compatible and incompatible filters.
TestIntersection
    intersection() operation.
TestSpecialMethods
    __len__, __repr__, __str__.
TestApplicationScenarios
    Real-world usage patterns.
TestEdgeCases
    Boundary conditions and unusual inputs.
"""

import random
import string

import pytest

from sds.advanced import BloomFilter
from sds.advanced.interfaces import AbstractProbabilisticSet

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _random_words(n: int, length: int = 8) -> list[str]:
    """Generate n distinct random lowercase words of given length."""
    words: set[str] = set()
    while len(words) < n:
        words.add("".join(random.choices(string.ascii_lowercase, k=length)))
    return list(words)


# ---------------------------------------------------------------------------
# TestBloomFilterCreation
# ---------------------------------------------------------------------------


class TestBloomFilterCreation:
    """Test BloomFilter instantiation and parameter validation."""

    def test_basic_creation(self) -> None:
        """A freshly created filter has count 0 and correct parameters."""
        bf = BloomFilter(size=1000, num_hashes=3)
        assert len(bf) == 0
        assert bf.size == 1000
        assert bf.num_hashes == 3
        assert bf.count == 0

    def test_minimal_valid_parameters(self) -> None:
        """size=1 and num_hashes=1 are the smallest valid parameters."""
        bf = BloomFilter(size=1, num_hashes=1)
        assert bf.size == 1
        assert bf.num_hashes == 1

    def test_large_filter(self) -> None:
        """Large filters are created without error."""
        bf = BloomFilter(size=10_000_000, num_hashes=10)
        assert bf.size == 10_000_000

    def test_is_abstract_probabilistic_set(self) -> None:
        """BloomFilter satisfies the AbstractProbabilisticSet interface."""
        bf = BloomFilter(size=1000, num_hashes=3)
        assert isinstance(bf, AbstractProbabilisticSet)

    def test_invalid_size_zero(self) -> None:
        """size=0 raises ValueError."""
        with pytest.raises(ValueError, match="size"):
            BloomFilter(size=0, num_hashes=3)

    def test_invalid_size_negative(self) -> None:
        """Negative size raises ValueError."""
        with pytest.raises(ValueError, match="size"):
            BloomFilter(size=-1, num_hashes=3)

    def test_invalid_num_hashes_zero(self) -> None:
        """num_hashes=0 raises ValueError."""
        with pytest.raises(ValueError, match="num_hashes"):
            BloomFilter(size=1000, num_hashes=0)

    def test_invalid_num_hashes_negative(self) -> None:
        """Negative num_hashes raises ValueError."""
        with pytest.raises(ValueError, match="num_hashes"):
            BloomFilter(size=1000, num_hashes=-1)

    def test_fill_ratio_empty(self) -> None:
        """An empty filter has a fill ratio of 0.0."""
        bf = BloomFilter(size=1000, num_hashes=3)
        assert bf.estimated_fill_ratio() == 0.0

    def test_fp_rate_empty(self) -> None:
        """An empty filter has an estimated FP rate of 0.0."""
        bf = BloomFilter(size=1000, num_hashes=3)
        assert bf.estimated_fp_rate() == 0.0


# ---------------------------------------------------------------------------
# TestOptimalParams
# ---------------------------------------------------------------------------


class TestOptimalParams:
    """Test BloomFilter.optimal_params static method."""

    def test_standard_case(self) -> None:
        """n=1000, fp_rate=0.01 returns mathematically sound values."""
        m, k = BloomFilter.optimal_params(n=1000, fp_rate=0.01)
        # m must be at least -n*ln(p)/ln(2)^2 ≈ 9585.06
        assert m >= 9585
        assert k == 7

    def test_low_fp_rate_gives_larger_size(self) -> None:
        """A tighter false positive rate requires a larger bit array."""
        m1, _ = BloomFilter.optimal_params(n=1000, fp_rate=0.01)
        m2, _ = BloomFilter.optimal_params(n=1000, fp_rate=0.001)
        assert m2 > m1

    def test_more_elements_gives_larger_size(self) -> None:
        """More expected elements require a larger bit array."""
        m1, _ = BloomFilter.optimal_params(n=1000, fp_rate=0.01)
        m2, _ = BloomFilter.optimal_params(n=10000, fp_rate=0.01)
        assert m2 > m1

    def test_returns_positive_values(self) -> None:
        """Returned size and num_hashes are always positive."""
        m, k = BloomFilter.optimal_params(n=1, fp_rate=0.5)
        assert m >= 1
        assert k >= 1

    def test_invalid_n_zero(self) -> None:
        """n=0 raises ValueError."""
        with pytest.raises(ValueError):
            BloomFilter.optimal_params(n=0, fp_rate=0.01)

    def test_invalid_n_negative(self) -> None:
        """Negative n raises ValueError."""
        with pytest.raises(ValueError):
            BloomFilter.optimal_params(n=-10, fp_rate=0.01)

    def test_invalid_fp_rate_zero(self) -> None:
        """fp_rate=0.0 raises ValueError."""
        with pytest.raises(ValueError):
            BloomFilter.optimal_params(n=1000, fp_rate=0.0)

    def test_invalid_fp_rate_one(self) -> None:
        """fp_rate=1.0 raises ValueError."""
        with pytest.raises(ValueError):
            BloomFilter.optimal_params(n=1000, fp_rate=1.0)

    def test_invalid_fp_rate_above_one(self) -> None:
        """fp_rate > 1.0 raises ValueError."""
        with pytest.raises(ValueError):
            BloomFilter.optimal_params(n=1000, fp_rate=2.0)

    def test_optimal_filter_achieves_target_fp(self) -> None:
        """A filter built with optimal_params stays near the target FP rate."""
        target_fp = 0.05
        words = _random_words(500)
        m, k = BloomFilter.optimal_params(n=len(words), fp_rate=target_fp)
        bf = BloomFilter(size=m, num_hashes=k)
        for w in words:
            bf.add(w)
        # Estimated FP rate should be in the right ballpark
        assert bf.estimated_fp_rate() < target_fp * 3


# ---------------------------------------------------------------------------
# TestAdd
# ---------------------------------------------------------------------------


class TestAdd:
    """Test the add() operation."""

    def test_add_single_string(self) -> None:
        """Adding one string increments count to 1."""
        bf = BloomFilter(size=1000, num_hashes=3)
        bf.add("hello")
        assert bf.count == 1

    def test_add_multiple_items(self) -> None:
        """Adding n items increments count to n (not deduplicated)."""
        bf = BloomFilter(size=1000, num_hashes=3)
        items = ["a", "b", "c", "d", "e"]
        for item in items:
            bf.add(item)
        assert bf.count == len(items)

    def test_add_same_item_twice_increments_count(self) -> None:
        """Adding the same item twice increments count twice."""
        bf = BloomFilter(size=1000, num_hashes=3)
        bf.add("dup")
        bf.add("dup")
        assert bf.count == 2

    def test_add_increases_fill_ratio(self) -> None:
        """Each add call increases or maintains the fill ratio."""
        bf = BloomFilter(size=1000, num_hashes=3)
        prev = bf.estimated_fill_ratio()
        for word in _random_words(20):
            bf.add(word)
            current = bf.estimated_fill_ratio()
            assert current >= prev
            prev = current

    def test_add_integer(self) -> None:
        """Integers can be added (converted via str())."""
        bf = BloomFilter(size=1000, num_hashes=3)
        bf.add(42)
        assert 42 in bf

    def test_add_float(self) -> None:
        """Floats can be added."""
        bf = BloomFilter(size=1000, num_hashes=3)
        bf.add(3.14)
        assert 3.14 in bf

    def test_add_tuple(self) -> None:
        """Tuples can be added."""
        bf = BloomFilter(size=1000, num_hashes=3)
        bf.add((1, 2, 3))
        assert (1, 2, 3) in bf

    def test_add_empty_string(self) -> None:
        """The empty string is a valid item."""
        bf = BloomFilter(size=1000, num_hashes=3)
        bf.add("")
        assert "" in bf


# ---------------------------------------------------------------------------
# TestContains
# ---------------------------------------------------------------------------


class TestContains:
    """Test the __contains__ / membership test operation."""

    def test_added_item_is_found(self) -> None:
        """An added item is always found (no false negatives)."""
        bf = BloomFilter(size=1000, num_hashes=3)
        bf.add("present")
        assert "present" in bf

    def test_unadded_item_may_be_absent(self) -> None:
        """An item not added is not found in an empty filter."""
        bf = BloomFilter(size=10000, num_hashes=7)
        assert "ghost" not in bf

    def test_contains_before_any_add(self) -> None:
        """An empty filter returns False for any query."""
        bf = BloomFilter(size=1000, num_hashes=3)
        assert "anything" not in bf

    def test_multiple_added_items_all_found(self) -> None:
        """All 50 added items are found."""
        bf = BloomFilter(size=5000, num_hashes=5)
        words = _random_words(50)
        for w in words:
            bf.add(w)
        for w in words:
            assert w in bf, f"False negative for: {w}"

    def test_in_operator_alias(self) -> None:
        """The 'in' operator delegates to __contains__."""
        bf = BloomFilter(size=1000, num_hashes=3)
        bf.add("test")
        assert ("test" in bf) is True
        assert bf.__contains__("test") is True


# ---------------------------------------------------------------------------
# TestProbabilisticGuarantees
# ---------------------------------------------------------------------------


class TestProbabilisticGuarantees:
    """Test the core probabilistic properties of BloomFilter."""

    def test_no_false_negatives_small(self) -> None:
        """No false negatives on 100 items with well-sized filter."""
        words = _random_words(100)
        m, k = BloomFilter.optimal_params(n=len(words), fp_rate=0.01)
        bf = BloomFilter(size=m, num_hashes=k)
        for w in words:
            bf.add(w)
        fn = [w for w in words if w not in bf]
        assert fn == [], f"False negatives found: {fn}"

    def test_no_false_negatives_large(self) -> None:
        """No false negatives on 500 items with well-sized filter."""
        words = _random_words(500)
        m, k = BloomFilter.optimal_params(n=len(words), fp_rate=0.01)
        bf = BloomFilter(size=m, num_hashes=k)
        for w in words:
            bf.add(w)
        fn = [w for w in words if w not in bf]
        assert fn == [], f"False negatives found: {fn}"

    def test_false_positive_rate_within_bounds(self) -> None:
        """FP rate on 1000 non-members stays below 3× the target rate."""
        inserted = _random_words(200, length=10)
        # Generate disjoint test words
        test_words: set[str] = set()
        inserted_set = set(inserted)
        while len(test_words) < 1000:
            w = "".join(random.choices(string.ascii_uppercase, k=10))
            if w not in inserted_set:
                test_words.add(w)

        m, k = BloomFilter.optimal_params(n=len(inserted), fp_rate=0.01)
        bf = BloomFilter(size=m, num_hashes=k)
        for w in inserted:
            bf.add(w)

        fp_count = sum(1 for w in test_words if w in bf)
        fp_rate = fp_count / len(test_words)
        # Allow 3× margin for statistical variance
        assert fp_rate < 0.03, f"FP rate {fp_rate:.3f} exceeded 3%"

    def test_oversized_filter_has_low_fp(self) -> None:
        """A generously-sized filter has a very low false positive rate."""
        words = _random_words(10)
        bf = BloomFilter(size=100_000, num_hashes=7)
        for w in words:
            bf.add(w)
        assert bf.estimated_fp_rate() < 0.001

    def test_full_filter_has_high_fp(self) -> None:
        """A heavily over-filled filter approaches FP rate of 1."""
        bf = BloomFilter(size=100, num_hashes=5)
        for w in _random_words(1000, length=12):
            bf.add(w)
        # Fill ratio should be near 1
        assert bf.estimated_fill_ratio() > 0.9


# ---------------------------------------------------------------------------
# TestFillRatio
# ---------------------------------------------------------------------------


class TestFillRatio:
    """Test estimated_fill_ratio() and estimated_fp_rate()."""

    def test_fill_ratio_zero_on_empty(self) -> None:
        """Empty filter has fill ratio 0.0."""
        assert BloomFilter(size=1000, num_hashes=3).estimated_fill_ratio() == 0.0

    def test_fill_ratio_increases_with_inserts(self) -> None:
        """Fill ratio is non-decreasing as items are added."""
        bf = BloomFilter(size=1000, num_hashes=3)
        ratios = [bf.estimated_fill_ratio()]
        for w in _random_words(30):
            bf.add(w)
            ratios.append(bf.estimated_fill_ratio())
        for a, b in zip(ratios, ratios[1:]):
            assert b >= a

    def test_fill_ratio_bounded(self) -> None:
        """Fill ratio is always in [0.0, 1.0]."""
        bf = BloomFilter(size=200, num_hashes=5)
        for w in _random_words(500):
            bf.add(w)
        r = bf.estimated_fill_ratio()
        assert 0.0 <= r <= 1.0

    def test_fp_rate_zero_on_empty(self) -> None:
        """Empty filter has FP rate 0.0."""
        assert BloomFilter(size=1000, num_hashes=3).estimated_fp_rate() == 0.0

    def test_fp_rate_bounded(self) -> None:
        """Estimated FP rate is always in [0.0, 1.0]."""
        bf = BloomFilter(size=100, num_hashes=3)
        for w in _random_words(500):
            bf.add(w)
        r = bf.estimated_fp_rate()
        assert 0.0 <= r <= 1.0

    def test_fp_rate_increases_with_fill(self) -> None:
        """FP rate increases as filter fills up."""
        bf = BloomFilter(size=500, num_hashes=3)
        fp0 = bf.estimated_fp_rate()
        for w in _random_words(100):
            bf.add(w)
        fp1 = bf.estimated_fp_rate()
        assert fp1 >= fp0


# ---------------------------------------------------------------------------
# TestUnion
# ---------------------------------------------------------------------------


class TestUnion:
    """Test the union() operation."""

    def test_union_contains_items_from_both(self) -> None:
        """Union contains all items from both source filters."""
        bf1 = BloomFilter(size=1000, num_hashes=3)
        bf2 = BloomFilter(size=1000, num_hashes=3)
        bf1.add("alpha")
        bf2.add("beta")
        merged = bf1.union(bf2)
        assert "alpha" in merged
        assert "beta" in merged

    def test_union_count_is_sum(self) -> None:
        """Union count equals the sum of both filters' counts."""
        bf1 = BloomFilter(size=1000, num_hashes=3)
        bf2 = BloomFilter(size=1000, num_hashes=3)
        for w in ["a", "b", "c"]:
            bf1.add(w)
        for w in ["d", "e"]:
            bf2.add(w)
        merged = bf1.union(bf2)
        assert len(merged) == len(bf1) + len(bf2)

    def test_union_does_not_mutate_sources(self) -> None:
        """union() returns a new filter without modifying the originals."""
        bf1 = BloomFilter(size=1000, num_hashes=3)
        bf2 = BloomFilter(size=1000, num_hashes=3)
        bf1.add("x")
        bf2.add("y")
        count1_before = bf1.count
        count2_before = bf2.count
        bf1.union(bf2)
        assert bf1.count == count1_before
        assert bf2.count == count2_before

    def test_union_is_commutative(self) -> None:
        """bf1.union(bf2) and bf2.union(bf1) contain the same items."""
        bf1 = BloomFilter(size=1000, num_hashes=3)
        bf2 = BloomFilter(size=1000, num_hashes=3)
        bf1.add("hello")
        bf2.add("world")
        m1 = bf1.union(bf2)
        m2 = bf2.union(bf1)
        assert ("hello" in m1) == ("hello" in m2)
        assert ("world" in m1) == ("world" in m2)

    def test_union_with_empty_filter(self) -> None:
        """Union with an empty filter returns a filter equivalent to the original."""
        bf = BloomFilter(size=1000, num_hashes=3)
        bf.add("only")
        empty = BloomFilter(size=1000, num_hashes=3)
        merged = bf.union(empty)
        assert "only" in merged

    def test_union_mismatched_size_raises(self) -> None:
        """union() raises ValueError when sizes differ."""
        bf1 = BloomFilter(size=1000, num_hashes=3)
        bf2 = BloomFilter(size=500, num_hashes=3)
        with pytest.raises(ValueError):
            bf1.union(bf2)

    def test_union_mismatched_hashes_raises(self) -> None:
        """union() raises ValueError when num_hashes differ."""
        bf1 = BloomFilter(size=1000, num_hashes=3)
        bf2 = BloomFilter(size=1000, num_hashes=5)
        with pytest.raises(ValueError):
            bf1.union(bf2)

    def test_union_preserves_no_false_negatives(self) -> None:
        """Items added to either source are always found in the union."""
        words_a = _random_words(50)
        words_b = _random_words(50)
        bf1 = BloomFilter(size=5000, num_hashes=5)
        bf2 = BloomFilter(size=5000, num_hashes=5)
        for w in words_a:
            bf1.add(w)
        for w in words_b:
            bf2.add(w)
        merged = bf1.union(bf2)
        for w in words_a + words_b:
            assert w in merged, f"False negative in union: {w}"


# ---------------------------------------------------------------------------
# TestIntersection
# ---------------------------------------------------------------------------


class TestIntersection:
    """Test the intersection() operation."""

    def test_intersection_common_item_found(self) -> None:
        """An item added to both filters is found in the intersection."""
        bf1 = BloomFilter(size=2000, num_hashes=4)
        bf2 = BloomFilter(size=2000, num_hashes=4)
        bf1.add("common")
        bf2.add("common")
        inter = bf1.intersection(bf2)
        assert "common" in inter

    def test_intersection_does_not_mutate_sources(self) -> None:
        """intersection() returns a new filter without modifying sources."""
        bf1 = BloomFilter(size=1000, num_hashes=3)
        bf2 = BloomFilter(size=1000, num_hashes=3)
        bf1.add("x")
        bf2.add("x")
        c1 = bf1.count
        c2 = bf2.count
        bf1.intersection(bf2)
        assert bf1.count == c1
        assert bf2.count == c2

    def test_intersection_mismatched_size_raises(self) -> None:
        """intersection() raises ValueError when sizes differ."""
        bf1 = BloomFilter(size=1000, num_hashes=3)
        bf2 = BloomFilter(size=500, num_hashes=3)
        with pytest.raises(ValueError):
            bf1.intersection(bf2)

    def test_intersection_mismatched_hashes_raises(self) -> None:
        """intersection() raises ValueError when num_hashes differ."""
        bf1 = BloomFilter(size=1000, num_hashes=3)
        bf2 = BloomFilter(size=1000, num_hashes=5)
        with pytest.raises(ValueError):
            bf1.intersection(bf2)

    def test_intersection_empty_gives_empty_result(self) -> None:
        """Intersection of two empty filters returns a filter with ratio 0."""
        bf1 = BloomFilter(size=1000, num_hashes=3)
        bf2 = BloomFilter(size=1000, num_hashes=3)
        inter = bf1.intersection(bf2)
        assert inter.estimated_fill_ratio() == 0.0

    def test_intersection_with_empty_filter(self) -> None:
        """Intersection with an empty filter clears all bits."""
        bf1 = BloomFilter(size=1000, num_hashes=3)
        for w in _random_words(20):
            bf1.add(w)
        empty = BloomFilter(size=1000, num_hashes=3)
        inter = bf1.intersection(empty)
        assert inter.estimated_fill_ratio() == 0.0


# ---------------------------------------------------------------------------
# TestSpecialMethods
# ---------------------------------------------------------------------------


class TestSpecialMethods:
    """Test __len__, __repr__, __str__."""

    def test_len_empty(self) -> None:
        """len() of empty filter is 0."""
        assert len(BloomFilter(size=1000, num_hashes=3)) == 0

    def test_len_after_adds(self) -> None:
        """len() equals number of add() calls (not deduplicated)."""
        bf = BloomFilter(size=1000, num_hashes=3)
        bf.add("x")
        bf.add("x")
        bf.add("y")
        assert len(bf) == 3

    def test_repr_format(self) -> None:
        """repr() matches the expected format."""
        bf = BloomFilter(size=1000, num_hashes=3)
        assert repr(bf) == "BloomFilter(size=1000, num_hashes=3, count=0)"

    def test_repr_after_add(self) -> None:
        """repr() reflects updated count."""
        bf = BloomFilter(size=500, num_hashes=5)
        bf.add("item")
        assert "count=1" in repr(bf)

    def test_str_contains_count(self) -> None:
        """str() mentions the number of items added."""
        bf = BloomFilter(size=1000, num_hashes=3)
        bf.add("hello")
        assert "1" in str(bf)

    def test_str_contains_fill(self) -> None:
        """str() mentions fill ratio."""
        bf = BloomFilter(size=1000, num_hashes=3)
        bf.add("test")
        s = str(bf)
        assert "fill" in s.lower() or "%" in s

    def test_str_empty_filter(self) -> None:
        """str() of empty filter mentions 0 items."""
        bf = BloomFilter(size=1000, num_hashes=3)
        assert "0" in str(bf)


# ---------------------------------------------------------------------------
# TestApplicationScenarios
# ---------------------------------------------------------------------------


class TestApplicationScenarios:
    """Test real-world usage patterns for BloomFilter."""

    def test_url_deduplication(self) -> None:
        """Bloom filter can deduplicate a URL stream without false negatives."""
        seen_urls = [
            "https://example.com/page/1",
            "https://example.com/page/2",
            "https://example.com/page/3",
        ]
        new_url = "https://example.com/page/99"

        m, k = BloomFilter.optimal_params(n=1000, fp_rate=0.01)
        bf = BloomFilter(size=m, num_hashes=k)

        for url in seen_urls:
            bf.add(url)

        for url in seen_urls:
            assert url in bf  # no false negatives

        assert new_url not in bf  # new URL is correctly absent

    def test_cache_filter_no_false_negatives(self) -> None:
        """Cache filter never misses a cached key."""
        cached_keys = [f"user:{i}" for i in range(100)]
        m, k = BloomFilter.optimal_params(n=len(cached_keys), fp_rate=0.01)
        bf = BloomFilter(size=m, num_hashes=k)

        for key in cached_keys:
            bf.add(key)

        # Every cached key must be found
        for key in cached_keys:
            assert key in bf

    def test_kruskal_cycle_detection_with_disjoint_set(self) -> None:
        """BloomFilter used as quick pre-filter alongside DisjointSet."""
        # BloomFilter to quickly reject edges whose endpoints were never seen
        bf = BloomFilter(size=500, num_hashes=3)
        edges = [(0, 1), (1, 2), (2, 3), (4, 5)]
        nodes = {0, 1, 2, 3, 4, 5}

        for n in nodes:
            bf.add(n)

        for u, v in edges:
            # If either endpoint not in filter, skip (no false negatives)
            assert u in bf
            assert v in bf

    def test_optimal_params_then_build(self) -> None:
        """Using optimal_params to build a filter with target FP rate."""
        n = 300
        target = 0.02
        words = _random_words(n)
        m, k = BloomFilter.optimal_params(n=n, fp_rate=target)
        bf = BloomFilter(size=m, num_hashes=k)

        for w in words:
            bf.add(w)

        # All inserted words found
        for w in words:
            assert w in bf

        # Estimated FP rate reasonable
        assert bf.estimated_fp_rate() < target * 4

    def test_union_merges_two_seen_sets(self) -> None:
        """Two filters covering different crawled domains can be merged."""
        domain_a = [f"a.com/{i}" for i in range(50)]
        domain_b = [f"b.com/{i}" for i in range(50)]

        bf_a = BloomFilter(size=5000, num_hashes=5)
        bf_b = BloomFilter(size=5000, num_hashes=5)

        for url in domain_a:
            bf_a.add(url)
        for url in domain_b:
            bf_b.add(url)

        merged = bf_a.union(bf_b)

        for url in domain_a + domain_b:
            assert url in merged


# ---------------------------------------------------------------------------
# TestEdgeCases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    """Test boundary conditions and unusual inputs."""

    def test_size_one_bit(self) -> None:
        """A filter with size=1 always has fill ratio 0 or 1."""
        bf = BloomFilter(size=1, num_hashes=1)
        bf.add("anything")
        assert bf.estimated_fill_ratio() in (0.0, 1.0)

    def test_num_hashes_one(self) -> None:
        """A filter with a single hash function still works correctly."""
        bf = BloomFilter(size=1000, num_hashes=1)
        bf.add("solo")
        assert "solo" in bf

    def test_high_num_hashes(self) -> None:
        """A filter with many hash functions has no false negatives."""
        bf = BloomFilter(size=10000, num_hashes=20)
        words = _random_words(30)
        for w in words:
            bf.add(w)
        for w in words:
            assert w in bf

    def test_unicode_items(self) -> None:
        """Unicode strings are handled correctly."""
        bf = BloomFilter(size=1000, num_hashes=3)
        items = ["café", "日本語", "العربية", "emoji: 🌍"]
        for item in items:
            bf.add(item)
        for item in items:
            assert item in bf

    def test_numeric_strings_vs_numbers(self) -> None:
        """The string '42' and the integer 42 produce the same hash."""
        bf = BloomFilter(size=1000, num_hashes=3)
        bf.add(42)
        # str(42) == "42", so both map to the same positions
        assert "42" in bf

    def test_large_number_of_inserts(self) -> None:
        """1000 inserts complete without error."""
        bf = BloomFilter(size=100_000, num_hashes=7)
        for i in range(1000):
            bf.add(f"item_{i}")
        assert bf.count == 1000

    def test_count_property_matches_len(self) -> None:
        """count property and len() always agree."""
        bf = BloomFilter(size=1000, num_hashes=3)
        for i in range(10):
            bf.add(f"item_{i}")
            assert bf.count == len(bf)

    def test_union_with_self(self) -> None:
        """Union of a filter with itself is idempotent."""
        bf = BloomFilter(size=1000, num_hashes=3)
        bf.add("hello")
        merged = bf.union(bf)
        assert "hello" in merged

    def test_intersection_with_self(self) -> None:
        """Intersection of a filter with itself preserves all items."""
        bf = BloomFilter(size=2000, num_hashes=4)
        words = _random_words(30)
        for w in words:
            bf.add(w)
        inter = bf.intersection(bf)
        for w in words:
            assert w in inter


# ---------------------------------------------------------------------------
# TestCollectionInterface
# ---------------------------------------------------------------------------


class TestCollectionInterface:
    """Test Collection interface compliance for BloomFilter."""

    def test_is_collection(self) -> None:
        """BloomFilter satisfies the Collection interface."""
        from sds.core.interfaces import Collection

        assert isinstance(BloomFilter(size=1000, num_hashes=3), Collection)

    def test_is_empty_on_new(self) -> None:
        """is_empty() returns True on a freshly created filter."""
        bf = BloomFilter(size=1000, num_hashes=3)
        assert bf.is_empty() is True

    def test_is_empty_after_add(self) -> None:
        """is_empty() returns False after adding an item."""
        bf = BloomFilter(size=1000, num_hashes=3)
        bf.add("x")
        assert bf.is_empty() is False

    def test_bool_empty(self) -> None:
        """bool(bf) is False when empty."""
        bf = BloomFilter(size=1000, num_hashes=3)
        assert not bf

    def test_bool_non_empty(self) -> None:
        """bool(bf) is True after an item is added."""
        bf = BloomFilter(size=1000, num_hashes=3)
        bf.add("x")
        assert bf

    def test_clear_resets_count(self) -> None:
        """clear() resets the item count to 0."""
        bf = BloomFilter(size=1000, num_hashes=3)
        bf.add("a")
        bf.add("b")
        bf.clear()
        assert len(bf) == 0
        assert bf.is_empty() is True

    def test_clear_resets_bit_array(self) -> None:
        """clear() resets the bit array so previously added items are gone."""
        bf = BloomFilter(size=10000, num_hashes=7)
        bf.add("hello")
        bf.clear()
        assert bf.estimated_fill_ratio() == 0.0

    def test_clear_allows_reuse(self) -> None:
        """BloomFilter is fully usable after clear()."""
        bf = BloomFilter(size=1000, num_hashes=3)
        bf.add("old")
        bf.clear()
        bf.add("new")
        assert "new" in bf
        assert len(bf) == 1

    def test_iter_raises_type_error(self) -> None:
        """__iter__ raises TypeError — elements cannot be recovered."""
        import pytest

        bf = BloomFilter(size=1000, num_hashes=3)
        bf.add("x")
        with pytest.raises(TypeError):
            list(bf)
