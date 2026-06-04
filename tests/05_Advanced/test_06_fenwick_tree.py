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

"""Tests for FenwickTree (Binary Indexed Tree).

Test Classes
------------
TestFenwickTreeCreation
    Instantiation, from_list, parameter validation.
TestUpdate
    update() — positive, negative, cumulative.
TestPrefixSum
    prefix_sum() — correctness, boundaries, after updates.
TestRangeSum
    range_sum() — correctness, single-element, full range.
TestPointQuery
    point_query() — individual element retrieval.
TestTotal
    total() — sum of all elements.
TestToList
    to_list() — full reconstruction.
TestIndexErrors
    IndexError for out-of-bounds accesses.
TestValueErrors
    ValueError for invalid arguments.
TestBruteForceCorrectness
    Exhaustive comparison against naive summation.
TestSpecialMethods
    __len__, __repr__, __str__.
TestApplicationScenarios
    Real-world usage patterns.
TestEdgeCases
    Boundary conditions: size=1, floats, negatives, large trees.
"""

import random

import pytest

from sds.advanced import AbstractFenwickTree, FenwickTree

# ---------------------------------------------------------------------------
# TestFenwickTreeCreation
# ---------------------------------------------------------------------------


class TestFenwickTreeCreation:
    """Instantiation and from_list construction."""

    def test_empty_tree_zeros(self) -> None:
        """A freshly created tree returns 0 for all prefix sums."""
        ft = FenwickTree(size=5)
        for i in range(1, 6):
            assert ft.prefix_sum(i) == 0.0

    def test_size_property(self) -> None:
        """size property equals the constructor argument."""
        ft = FenwickTree(size=10)
        assert ft.size == 10

    def test_len_equals_size(self) -> None:
        """len() equals the size."""
        ft = FenwickTree(size=7)
        assert len(ft) == 7

    def test_is_abstract_fenwick_tree(self) -> None:
        """FenwickTree satisfies AbstractFenwickTree."""
        assert isinstance(FenwickTree(size=1), AbstractFenwickTree)

    def test_from_list_basic(self) -> None:
        """from_list builds a tree with correct prefix sums."""
        ft = FenwickTree.from_list([1, 2, 3, 4, 5])
        assert ft.prefix_sum(5) == 15.0

    def test_from_list_size(self) -> None:
        """from_list sets size to len(values)."""
        ft = FenwickTree.from_list([10, 20, 30])
        assert ft.size == 3

    def test_from_list_single(self) -> None:
        """from_list with one element works correctly."""
        ft = FenwickTree.from_list([42])
        assert ft.prefix_sum(1) == 42.0

    def test_from_list_floats(self) -> None:
        """from_list accepts float values."""
        ft = FenwickTree.from_list([1.5, 2.5, 3.0])
        assert ft.prefix_sum(3) == pytest.approx(7.0)

    def test_invalid_size_zero(self) -> None:
        """size=0 raises ValueError."""
        with pytest.raises(ValueError, match="size"):
            FenwickTree(size=0)

    def test_invalid_size_negative(self) -> None:
        """Negative size raises ValueError."""
        with pytest.raises(ValueError, match="size"):
            FenwickTree(size=-1)

    def test_from_list_empty_raises(self) -> None:
        """from_list with empty list raises ValueError."""
        with pytest.raises(ValueError):
            FenwickTree.from_list([])


# ---------------------------------------------------------------------------
# TestUpdate
# ---------------------------------------------------------------------------


class TestUpdate:
    """Test update() — point mutations."""

    def test_update_single(self) -> None:
        """A single update is reflected in prefix_sum."""
        ft = FenwickTree(size=5)
        ft.update(3, 7)
        assert ft.prefix_sum(3) == 7.0

    def test_update_does_not_affect_lower_prefix(self) -> None:
        """Updating index i does not change prefix_sum(i-1)."""
        ft = FenwickTree(size=5)
        ft.update(3, 10)
        assert ft.prefix_sum(2) == 0.0

    def test_update_affects_higher_prefix(self) -> None:
        """Updating index i changes prefix_sum for all j >= i."""
        ft = FenwickTree(size=5)
        ft.update(3, 10)
        assert ft.prefix_sum(4) == 10.0
        assert ft.prefix_sum(5) == 10.0

    def test_update_cumulative(self) -> None:
        """Multiple updates to the same index accumulate."""
        ft = FenwickTree(size=3)
        ft.update(2, 5)
        ft.update(2, 3)
        assert ft.point_query(2) == 8.0

    def test_update_negative_delta(self) -> None:
        """Negative delta decreases the stored value."""
        ft = FenwickTree(size=3)
        ft.update(1, 10)
        ft.update(1, -4)
        assert ft.point_query(1) == 6.0

    def test_update_first_index(self) -> None:
        """Updating index 1 works correctly."""
        ft = FenwickTree(size=5)
        ft.update(1, 42)
        assert ft.prefix_sum(1) == 42.0

    def test_update_last_index(self) -> None:
        """Updating the last index works correctly."""
        ft = FenwickTree(size=5)
        ft.update(5, 99)
        assert ft.prefix_sum(5) == 99.0
        assert ft.prefix_sum(4) == 0.0

    def test_update_integer_stored_as_float(self) -> None:
        """Integer delta is stored and returned as float."""
        ft = FenwickTree(size=3)
        ft.update(1, 7)
        assert isinstance(ft.prefix_sum(1), float)

    def test_update_float_delta(self) -> None:
        """Float delta is accepted."""
        ft = FenwickTree(size=3)
        ft.update(2, 1.5)
        assert ft.point_query(2) == pytest.approx(1.5)


# ---------------------------------------------------------------------------
# TestPrefixSum
# ---------------------------------------------------------------------------


class TestPrefixSum:
    """Test prefix_sum() — cumulative sums."""

    def test_prefix_sum_one(self) -> None:
        """prefix_sum(1) equals the first element."""
        ft = FenwickTree.from_list([5, 10, 15])
        assert ft.prefix_sum(1) == 5.0

    def test_prefix_sum_all(self) -> None:
        """prefix_sum(size) equals the total sum."""
        ft = FenwickTree.from_list([1, 2, 3, 4, 5])
        assert ft.prefix_sum(5) == 15.0

    def test_prefix_sum_monotone(self) -> None:
        """prefix_sum is non-decreasing for non-negative values."""
        ft = FenwickTree.from_list([1, 2, 3, 4, 5])
        sums = [ft.prefix_sum(i) for i in range(1, 6)]
        for a, b in zip(sums, sums[1:]):
            assert b >= a

    def test_prefix_sum_after_update(self) -> None:
        """prefix_sum reflects updates correctly."""
        ft = FenwickTree.from_list([1, 2, 3])
        ft.update(2, 10)
        assert ft.prefix_sum(2) == 13.0  # 1 + (2+10)
        assert ft.prefix_sum(3) == 16.0

    def test_prefix_sum_zero_tree(self) -> None:
        """prefix_sum on a zero-initialised tree is always 0."""
        ft = FenwickTree(size=10)
        for i in range(1, 11):
            assert ft.prefix_sum(i) == 0.0

    def test_prefix_sum_matches_naive(self) -> None:
        """prefix_sum matches naive list summation for all indices."""
        vals = [3, 1, 4, 1, 5, 9, 2, 6]
        ft = FenwickTree.from_list(vals)
        for i in range(1, len(vals) + 1):
            assert ft.prefix_sum(i) == pytest.approx(float(sum(vals[:i])))


# ---------------------------------------------------------------------------
# TestRangeSum
# ---------------------------------------------------------------------------


class TestRangeSum:
    """Test range_sum() — sub-range sums."""

    def test_range_sum_full(self) -> None:
        """range_sum(1, size) equals total()."""
        ft = FenwickTree.from_list([1, 2, 3, 4, 5])
        assert ft.range_sum(1, 5) == 15.0

    def test_range_sum_single_element(self) -> None:
        """range_sum(i, i) equals point_query(i)."""
        ft = FenwickTree.from_list([10, 20, 30, 40])
        for i in range(1, 5):
            assert ft.range_sum(i, i) == ft.point_query(i)

    def test_range_sum_middle(self) -> None:
        """range_sum(2, 4) equals sum of elements 2..4."""
        ft = FenwickTree.from_list([1, 2, 3, 4, 5])
        assert ft.range_sum(2, 4) == 9.0

    def test_range_sum_after_update(self) -> None:
        """range_sum reflects updates."""
        ft = FenwickTree.from_list([1, 2, 3, 4, 5])
        ft.update(3, 10)
        assert ft.range_sum(2, 4) == 19.0  # 2 + (3+10) + 4

    def test_range_sum_matches_naive(self) -> None:
        """range_sum matches naive slice summation for all pairs."""
        vals = [2, 5, 1, 8, 3, 7]
        ft = FenwickTree.from_list(vals)
        for left in range(1, len(vals) + 1):
            for r in range(left, len(vals) + 1):
                expected = float(sum(vals[left - 1 : r]))
                assert ft.range_sum(left, r) == pytest.approx(expected)

    def test_range_sum_start_equals_end(self) -> None:
        """range_sum with left == right is a point query."""
        ft = FenwickTree.from_list([7, 3, 9])
        assert ft.range_sum(2, 2) == 3.0


# ---------------------------------------------------------------------------
# TestPointQuery
# ---------------------------------------------------------------------------


class TestPointQuery:
    """Test point_query() — individual element access."""

    def test_point_query_all_elements(self) -> None:
        """point_query recovers each element from from_list."""
        vals = [5, 2, 8, 1, 9]
        ft = FenwickTree.from_list(vals)
        for i, v in enumerate(vals, start=1):
            assert ft.point_query(i) == pytest.approx(float(v))

    def test_point_query_after_update(self) -> None:
        """point_query reflects updates."""
        ft = FenwickTree(size=4)
        ft.update(2, 7)
        ft.update(2, 3)
        assert ft.point_query(2) == 10.0

    def test_point_query_first(self) -> None:
        """point_query(1) works correctly."""
        ft = FenwickTree.from_list([42, 0, 0])
        assert ft.point_query(1) == 42.0

    def test_point_query_zero_tree(self) -> None:
        """point_query on zero-initialised tree returns 0."""
        ft = FenwickTree(size=5)
        for i in range(1, 6):
            assert ft.point_query(i) == 0.0


# ---------------------------------------------------------------------------
# TestTotal
# ---------------------------------------------------------------------------


class TestTotal:
    """Test total() — sum of all elements."""

    def test_total_zero_tree(self) -> None:
        """Total of a zero-initialised tree is 0."""
        assert FenwickTree(size=10).total() == 0.0

    def test_total_from_list(self) -> None:
        """total() equals sum of the original list."""
        vals = [1, 2, 3, 4, 5]
        ft = FenwickTree.from_list(vals)
        assert ft.total() == float(sum(vals))

    def test_total_after_updates(self) -> None:
        """total() reflects all updates."""
        ft = FenwickTree(size=3)
        ft.update(1, 10)
        ft.update(2, 20)
        ft.update(3, 30)
        assert ft.total() == 60.0

    def test_total_after_negative_update(self) -> None:
        """total() decreases after a negative update."""
        ft = FenwickTree.from_list([10, 10, 10])
        ft.update(2, -5)
        assert ft.total() == 25.0


# ---------------------------------------------------------------------------
# TestToList
# ---------------------------------------------------------------------------


class TestToList:
    """Test to_list() — full reconstruction."""

    def test_to_list_round_trip(self) -> None:
        """to_list() reconstructs the original values exactly."""
        vals = [3, 1, 4, 1, 5, 9, 2, 6]
        ft = FenwickTree.from_list(vals)
        assert ft.to_list() == pytest.approx([float(v) for v in vals])

    def test_to_list_after_update(self) -> None:
        """to_list() reflects updates."""
        ft = FenwickTree.from_list([1, 2, 3])
        ft.update(2, 10)
        result = ft.to_list()
        assert result == pytest.approx([1.0, 12.0, 3.0])

    def test_to_list_zero_tree(self) -> None:
        """to_list() of zero-initialised tree is all zeros."""
        ft = FenwickTree(size=4)
        assert ft.to_list() == [0.0, 0.0, 0.0, 0.0]

    def test_to_list_length(self) -> None:
        """to_list() returns a list of length size."""
        ft = FenwickTree.from_list([1, 2, 3, 4, 5])
        assert len(ft.to_list()) == 5


# ---------------------------------------------------------------------------
# TestIndexErrors
# ---------------------------------------------------------------------------


class TestIndexErrors:
    """Out-of-bounds access raises IndexError."""

    def test_update_index_zero(self) -> None:
        """update(0, ...) raises IndexError."""
        ft = FenwickTree(size=5)
        with pytest.raises(IndexError):
            ft.update(0, 1)

    def test_update_index_beyond_size(self) -> None:
        """update(size+1, ...) raises IndexError."""
        ft = FenwickTree(size=5)
        with pytest.raises(IndexError):
            ft.update(6, 1)

    def test_prefix_sum_index_zero(self) -> None:
        """prefix_sum(0) raises IndexError."""
        ft = FenwickTree(size=5)
        with pytest.raises(IndexError):
            ft.prefix_sum(0)

    def test_prefix_sum_index_beyond_size(self) -> None:
        """prefix_sum(size+1) raises IndexError."""
        ft = FenwickTree(size=5)
        with pytest.raises(IndexError):
            ft.prefix_sum(6)

    def test_range_sum_left_zero(self) -> None:
        """range_sum(0, ...) raises IndexError."""
        ft = FenwickTree(size=5)
        with pytest.raises(IndexError):
            ft.range_sum(0, 3)

    def test_range_sum_right_beyond_size(self) -> None:
        """range_sum(..., size+1) raises IndexError."""
        ft = FenwickTree(size=5)
        with pytest.raises(IndexError):
            ft.range_sum(1, 6)

    def test_point_query_index_zero(self) -> None:
        """point_query(0) raises IndexError."""
        ft = FenwickTree(size=5)
        with pytest.raises(IndexError):
            ft.point_query(0)

    def test_point_query_index_beyond_size(self) -> None:
        """point_query(size+1) raises IndexError."""
        ft = FenwickTree(size=5)
        with pytest.raises(IndexError):
            ft.point_query(6)


# ---------------------------------------------------------------------------
# TestValueErrors
# ---------------------------------------------------------------------------


class TestValueErrors:
    """Invalid argument combinations raise ValueError."""

    def test_range_sum_left_greater_than_right(self) -> None:
        """range_sum(left, right) with left > right raises ValueError."""
        ft = FenwickTree(size=5)
        with pytest.raises(ValueError):
            ft.range_sum(4, 2)

    def test_from_list_empty(self) -> None:
        """from_list([]) raises ValueError."""
        with pytest.raises(ValueError):
            FenwickTree.from_list([])


# ---------------------------------------------------------------------------
# TestBruteForceCorrectness
# ---------------------------------------------------------------------------


class TestBruteForceCorrectness:
    """Exhaustive comparison against naive list summation."""

    def test_prefix_sum_exhaustive(self) -> None:
        """prefix_sum matches naive for 50 random elements."""
        vals = [random.randint(1, 100) for _ in range(50)]
        ft = FenwickTree.from_list(vals)
        for i in range(1, 51):
            assert ft.prefix_sum(i) == pytest.approx(float(sum(vals[:i])))

    def test_range_sum_exhaustive(self) -> None:
        """range_sum matches naive slice sum for all pairs (size=20)."""
        vals = [random.randint(-50, 50) for _ in range(20)]
        ft = FenwickTree.from_list(vals)
        for left in range(1, 21):
            for r in range(left, 21):
                expected = float(sum(vals[left - 1 : r]))
                assert ft.range_sum(left, r) == pytest.approx(expected)

    def test_point_query_after_random_updates(self) -> None:
        """point_query is correct after 100 random updates."""
        n = 15
        reference = [0.0] * (n + 1)  # 1-indexed
        ft = FenwickTree(size=n)
        for _ in range(100):
            i = random.randint(1, n)
            delta = float(random.randint(-10, 10))
            ft.update(i, delta)
            reference[i] += delta
        for i in range(1, n + 1):
            assert ft.point_query(i) == pytest.approx(reference[i])

    def test_to_list_matches_reference(self) -> None:
        """to_list() matches reference array after mixed updates."""
        n = 10
        ref = [0.0] * n
        ft = FenwickTree(size=n)
        for _ in range(50):
            i = random.randint(1, n)
            delta = float(random.randint(1, 20))
            ft.update(i, delta)
            ref[i - 1] += delta
        assert ft.to_list() == pytest.approx(ref)


# ---------------------------------------------------------------------------
# TestSpecialMethods
# ---------------------------------------------------------------------------


class TestSpecialMethods:
    """Test __len__, __repr__, __str__."""

    def test_len(self) -> None:
        """len() equals the size."""
        assert len(FenwickTree(size=8)) == 8

    def test_repr_empty(self) -> None:
        """repr() of zero tree has expected format."""
        ft = FenwickTree(size=5)
        assert repr(ft) == "FenwickTree(size=5, total=0.0)"

    def test_repr_after_updates(self) -> None:
        """repr() reflects the current total."""
        ft = FenwickTree.from_list([1, 2, 3])
        assert "total=6.0" in repr(ft)

    def test_str_format(self) -> None:
        """str() mentions size and total."""
        ft = FenwickTree.from_list([1, 2, 3])
        s = str(ft)
        assert "3" in s
        assert "6.0" in s


# ---------------------------------------------------------------------------
# TestApplicationScenarios
# ---------------------------------------------------------------------------


class TestApplicationScenarios:
    """Real-world usage patterns."""

    def test_running_total_stream(self) -> None:
        """FenwickTree as a running-total accumulator for a stream."""
        ft = FenwickTree(size=10)
        events = [(1, 5), (3, 2), (5, 8), (7, 1), (10, 4)]
        for idx, val in events:
            ft.update(idx, val)
        # Total events in positions 1..5
        assert ft.range_sum(1, 5) == 15.0  # 5+2+8

    def test_frequency_table(self) -> None:
        """Count occurrences and query frequency prefix sums."""
        n = 10
        ft = FenwickTree(size=n)
        data = [1, 3, 3, 5, 7, 7, 7, 9]
        for x in data:
            ft.update(x, 1)
        # Frequency of values ≤ 5
        assert ft.prefix_sum(5) == 4.0  # 1,3,3,5
        # Frequency of values in [3, 7]
        assert ft.range_sum(3, 7) == 6.0  # 3,3,5,7,7,7

    def test_order_statistics(self) -> None:
        """Use prefix sums to find rank of elements."""
        ft = FenwickTree.from_list([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        values = [3, 1, 4, 1, 5, 9, 2, 6]
        for v in values:
            ft.update(v, 1)
        # Rank of 5: how many elements ≤ 5 ?
        rank_5 = int(ft.prefix_sum(5))
        assert rank_5 == 6  # 1,1,2,3,4,5 → 6 elements ≤ 5

    def test_range_update_via_difference_array(self) -> None:
        """Simulate range update [l,r] += delta using difference Fenwick Tree.

        Standard trick: maintain a difference array D where D[i] = A[i]-A[i-1].
        A range update [l,r] += delta becomes D[l]+=delta, D[r+1]-=delta.
        prefix_sum(i) then gives A[i].
        """
        n = 8
        ft = FenwickTree(size=n + 1)  # extra slot for D[n+1]
        # Range update [2, 5] += 3
        ft.update(2, 3)
        ft.update(6, -3)
        # Query A[i] = prefix_sum(i) for each position
        expected = [0, 3, 3, 3, 3, 0, 0, 0]  # indices 1..8
        for i in range(1, n + 1):
            assert ft.prefix_sum(i) == pytest.approx(expected[i - 1])

    def test_inversion_count_contribution(self) -> None:
        """Count elements already inserted that are greater than current."""
        n = 5
        ft = FenwickTree(size=n)
        sequence = [3, 1, 4, 1, 5]
        inversions = 0
        for x in sequence:
            # Elements already inserted that are > x
            inversions += int(ft.range_sum(x + 1, n)) if x < n else 0
            ft.update(x, 1)
        # Inversions in [3,1,4,1,5]: (3,1),(3,1),(4,1) → 3
        assert inversions == 3


# ---------------------------------------------------------------------------
# TestEdgeCases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    """Boundary conditions."""

    def test_size_one(self) -> None:
        """A tree of size 1 supports all operations."""
        ft = FenwickTree(size=1)
        ft.update(1, 42)
        assert ft.prefix_sum(1) == 42.0
        assert ft.point_query(1) == 42.0
        assert ft.range_sum(1, 1) == 42.0
        assert ft.total() == 42.0

    def test_all_zeros(self) -> None:
        """A zero-valued tree has total 0 and all prefix sums 0."""
        ft = FenwickTree(size=10)
        assert ft.total() == 0.0
        assert ft.prefix_sum(5) == 0.0

    def test_large_tree(self) -> None:
        """A tree of size 1000 computes prefix sums correctly."""
        vals = list(range(1, 1001))  # 1..1000
        ft = FenwickTree.from_list(vals)
        assert ft.total() == pytest.approx(float(sum(vals)))
        assert ft.prefix_sum(100) == pytest.approx(float(sum(vals[:100])))

    def test_float_precision(self) -> None:
        """Float values accumulate with standard floating-point precision."""
        ft = FenwickTree(size=4)
        ft.update(1, 0.1)
        ft.update(2, 0.2)
        ft.update(3, 0.3)
        ft.update(4, 0.4)
        assert ft.total() == pytest.approx(1.0)

    def test_negative_values(self) -> None:
        """Negative values are handled correctly in sums."""
        ft = FenwickTree.from_list([-1, -2, -3, 4, 5])
        assert ft.prefix_sum(3) == pytest.approx(-6.0)
        assert ft.total() == pytest.approx(3.0)

    def test_mixed_positive_negative(self) -> None:
        """Mixed positive and negative updates give correct range sums."""
        ft = FenwickTree(size=5)
        ft.update(1, 10)
        ft.update(2, -3)
        ft.update(3, 5)
        assert ft.range_sum(1, 3) == pytest.approx(12.0)

    def test_update_to_zero(self) -> None:
        """Setting a value to zero via negative update works correctly."""
        ft = FenwickTree(size=3)
        ft.update(2, 7)
        ft.update(2, -7)
        assert ft.point_query(2) == pytest.approx(0.0)
        assert ft.total() == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# TestCollectionInterface
# ---------------------------------------------------------------------------


class TestCollectionInterface:
    """Test Collection interface compliance for FenwickTree."""

    def test_is_collection(self) -> None:
        """FenwickTree satisfies the Collection interface."""
        from sds.core.interfaces import Collection

        assert isinstance(FenwickTree(size=5), Collection)

    def test_is_empty_zero_tree(self) -> None:
        """is_empty() returns True on a zero-initialised tree."""
        assert FenwickTree(size=5).is_empty() is True

    def test_is_empty_after_update(self) -> None:
        """is_empty() returns False after a non-zero update."""
        ft = FenwickTree(size=5)
        ft.update(1, 1)
        assert ft.is_empty() is False

    def test_is_empty_after_clear(self) -> None:
        """is_empty() returns True after clear()."""
        ft = FenwickTree.from_list([1, 2, 3])
        ft.clear()
        assert ft.is_empty() is True

    def test_bool_empty(self) -> None:
        """bool(ft) is False on a zero tree."""
        assert not FenwickTree(size=5)

    def test_bool_non_empty(self) -> None:
        """bool(ft) is True after a non-zero update."""
        ft = FenwickTree(size=5)
        ft.update(1, 1)
        assert ft

    def test_clear_resets_all(self) -> None:
        """clear() sets all values back to zero."""
        ft = FenwickTree.from_list([1, 2, 3, 4, 5])
        ft.clear()
        assert ft.total() == 0.0
        assert ft.to_list() == [0.0] * 5

    def test_clear_allows_reuse(self) -> None:
        """FenwickTree is fully usable after clear()."""
        ft = FenwickTree(size=3)
        ft.update(1, 10)
        ft.clear()
        ft.update(2, 5)
        assert ft.point_query(1) == 0.0
        assert ft.point_query(2) == 5.0

    def test_iter_yields_values(self) -> None:
        """__iter__ yields values at positions 1..size in order."""
        vals = [3.0, 1.0, 4.0, 1.0, 5.0]
        ft = FenwickTree.from_list(vals)
        assert list(ft) == pytest.approx(vals)

    def test_contains_existing_value(self) -> None:
        """__contains__ returns True for a value present in the tree."""
        ft = FenwickTree.from_list([10, 20, 30])
        assert 20.0 in ft

    def test_contains_missing_value(self) -> None:
        """__contains__ returns False for a value not in the tree."""
        ft = FenwickTree.from_list([1, 2, 3])
        assert 99 not in ft

    def test_index_structure_error_is_index_error(self) -> None:
        """IndexStructureError is a subclass of IndexError."""
        from sds.core.exceptions import IndexStructureError

        assert issubclass(IndexStructureError, IndexError)
