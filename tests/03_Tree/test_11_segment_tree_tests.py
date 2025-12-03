# Copyright 2024-205, skyfrigate, biface
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

"""Tests for Segment Tree implementation."""

import math

import pytest

from sds.core.exceptions import InvalidOperationError
from sds.tree.segment_tree import SegmentTree


class TestSegmentTreeCreation:
    """Test segment tree creation."""

    def test_create_from_array(self) -> None:
        """Test creating segment tree from array."""
        arr = [1, 2, 3, 4, 5]
        tree = SegmentTree(arr)
        assert tree.size == 5
        assert len(tree) == 5

    def test_create_empty_array_raises_error(self) -> None:
        """Test creating from empty array raises error."""
        with pytest.raises(ValueError):
            SegmentTree([])

    def test_create_with_sum_operation(self) -> None:
        """Test creating with sum operation."""
        tree = SegmentTree([1, 2, 3], operation="sum")
        assert tree.query(0, 2) == 6

    def test_create_with_min_operation(self) -> None:
        """Test creating with min operation."""
        tree = SegmentTree([5, 2, 8, 1], operation="min")
        assert tree.query(0, 3) == 1

    def test_create_with_max_operation(self) -> None:
        """Test creating with max operation."""
        tree = SegmentTree([5, 2, 8, 1], operation="max")
        assert tree.query(0, 3) == 8

    def test_create_with_invalid_operation(self) -> None:
        """Test creating with invalid operation raises error."""
        with pytest.raises(ValueError):
            SegmentTree([1, 2, 3], operation="invalid")

    def test_create_with_custom_operation(self) -> None:
        """Test creating with custom operation."""

        def multiply(a, b):
            return a * b

        tree = SegmentTree([2, 3, 4], operation=multiply, identity=1)
        assert tree.query(0, 2) == 24

    def test_custom_operation_without_identity_raises_error(self) -> None:
        """Test custom operation without identity raises error."""
        with pytest.raises(ValueError):
            SegmentTree([1, 2, 3], operation=lambda a, b: a + b)


class TestSegmentTreeSumQueries:
    """Test range sum queries."""

    def test_sum_entire_array(self) -> None:
        """Test sum of entire array."""
        tree = SegmentTree([1, 2, 3, 4, 5], operation="sum")
        assert tree.query(0, 4) == 15

    def test_sum_partial_range(self) -> None:
        """Test sum of partial range."""
        tree = SegmentTree([1, 2, 3, 4, 5], operation="sum")
        assert tree.query(1, 3) == 9  # 2+3+4

    def test_sum_single_element(self) -> None:
        """Test sum of single element."""
        tree = SegmentTree([1, 2, 3, 4, 5], operation="sum")
        assert tree.query(2, 2) == 3

    def test_sum_first_elements(self) -> None:
        """Test sum from start."""
        tree = SegmentTree([1, 2, 3, 4, 5], operation="sum")
        assert tree.query(0, 2) == 6  # 1+2+3

    def test_sum_last_elements(self) -> None:
        """Test sum to end."""
        tree = SegmentTree([1, 2, 3, 4, 5], operation="sum")
        assert tree.query(3, 4) == 9  # 4+5


class TestSegmentTreeMinQueries:
    """Test range minimum queries."""

    def test_min_entire_array(self) -> None:
        """Test min of entire array."""
        tree = SegmentTree([5, 2, 8, 1, 9], operation="min")
        assert tree.query(0, 4) == 1

    def test_min_partial_range(self) -> None:
        """Test min of partial range."""
        tree = SegmentTree([5, 2, 8, 1, 9], operation="min")
        assert tree.query(0, 2) == 2

    def test_min_single_element(self) -> None:
        """Test min of single element."""
        tree = SegmentTree([5, 2, 8], operation="min")
        assert tree.query(1, 1) == 2

    def test_min_with_duplicates(self) -> None:
        """Test min with duplicate values."""
        tree = SegmentTree([3, 1, 4, 1, 5], operation="min")
        assert tree.query(0, 4) == 1


class TestSegmentTreeMaxQueries:
    """Test range maximum queries."""

    def test_max_entire_array(self) -> None:
        """Test max of entire array."""
        tree = SegmentTree([5, 2, 8, 1, 9], operation="max")
        assert tree.query(0, 4) == 9

    def test_max_partial_range(self) -> None:
        """Test max of partial range."""
        tree = SegmentTree([5, 2, 8, 1, 9], operation="max")
        assert tree.query(0, 2) == 8

    def test_max_single_element(self) -> None:
        """Test max of single element."""
        tree = SegmentTree([5, 2, 8], operation="max")
        assert tree.query(2, 2) == 8


class TestSegmentTreeUpdate:
    """Test update operations."""

    def test_update_and_query_sum(self) -> None:
        """Test update with sum operation."""
        tree = SegmentTree([1, 2, 3, 4, 5], operation="sum")
        assert tree.query(0, 4) == 15
        tree.update(2, 10)  # Change 3 to 10
        assert tree.query(0, 4) == 22  # 1+2+10+4+5

    def test_update_and_query_min(self) -> None:
        """Test update with min operation."""
        tree = SegmentTree([5, 2, 8, 1, 9], operation="min")
        assert tree.query(0, 4) == 1
        tree.update(3, 10)  # Change 1 to 10
        assert tree.query(0, 4) == 2  # New min

    def test_update_and_query_max(self) -> None:
        """Test update with max operation."""
        tree = SegmentTree([5, 2, 8, 1, 9], operation="max")
        assert tree.query(0, 4) == 9
        tree.update(4, 15)  # Change 9 to 15
        assert tree.query(0, 4) == 15

    def test_update_multiple_times(self) -> None:
        """Test multiple updates."""
        tree = SegmentTree([1, 2, 3], operation="sum")
        tree.update(0, 10)
        tree.update(1, 20)
        tree.update(2, 30)
        assert tree.query(0, 2) == 60

    def test_update_out_of_bounds_raises_error(self) -> None:
        """Test updating out of bounds raises error."""
        tree = SegmentTree([1, 2, 3])
        with pytest.raises(InvalidOperationError):
            tree.update(5, 10)

    def test_update_negative_index_raises_error(self) -> None:
        """Test updating negative index raises error."""
        tree = SegmentTree([1, 2, 3])
        with pytest.raises(InvalidOperationError):
            tree.update(-1, 10)


class TestSegmentTreeQueryValidation:
    """Test query validation."""

    def test_query_invalid_range_raises_error(self) -> None:
        """Test querying invalid range raises error."""
        tree = SegmentTree([1, 2, 3, 4, 5])
        with pytest.raises(InvalidOperationError):
            tree.query(3, 1)  # left > right

    def test_query_out_of_bounds_raises_error(self) -> None:
        """Test querying out of bounds raises error."""
        tree = SegmentTree([1, 2, 3])
        with pytest.raises(InvalidOperationError):
            tree.query(0, 5)

    def test_query_negative_index_raises_error(self) -> None:
        """Test querying negative index raises error."""
        tree = SegmentTree([1, 2, 3])
        with pytest.raises(InvalidOperationError):
            tree.query(-1, 2)


class TestSegmentTreeGetSet:
    """Test get and set operations."""

    def test_get_element(self) -> None:
        """Test getting element at index."""
        tree = SegmentTree([1, 2, 3, 4, 5])
        assert tree.get(0) == 1
        assert tree.get(2) == 3
        assert tree.get(4) == 5

    def test_get_out_of_bounds_raises_error(self) -> None:
        """Test getting out of bounds raises error."""
        tree = SegmentTree([1, 2, 3])
        with pytest.raises(InvalidOperationError):
            tree.get(5)

    def test_array_indexing(self) -> None:
        """Test array-style indexing."""
        tree = SegmentTree([1, 2, 3, 4, 5])
        assert tree[0] == 1
        assert tree[2] == 3
        tree[1] = 10
        assert tree[1] == 10

    def test_to_array(self) -> None:
        """Test converting to array."""
        tree = SegmentTree([1, 2, 3])
        tree.update(1, 10)
        arr = tree.to_array()
        assert arr == [1, 10, 3]


class TestSegmentTreeStringRepresentation:
    """Test string representations."""

    def test_repr(self) -> None:
        """Test repr."""
        tree = SegmentTree([1, 2, 3])
        assert repr(tree) == "SegmentTree(size=3)"

    def test_str(self) -> None:
        """Test str."""
        tree = SegmentTree([1, 2, 3])
        assert str(tree) == "SegmentTree: [1, 2, 3]"

    def test_str_after_update(self) -> None:
        """Test str after update."""
        tree = SegmentTree([1, 2, 3])
        tree.update(1, 10)
        assert str(tree) == "SegmentTree: [1, 10, 3]"


class TestSegmentTreeCustomOperations:
    """Test custom operations."""

    def test_gcd_operation(self) -> None:
        """Test GCD operation."""

        def gcd_op(a, b):
            return math.gcd(a, b)

        tree = SegmentTree([12, 18, 24, 30], operation=gcd_op, identity=0)
        assert tree.query(0, 3) == 6

    def test_multiply_operation(self) -> None:
        """Test multiplication operation."""

        def mult(a, b):
            return a * b

        tree = SegmentTree([2, 3, 4], operation=mult, identity=1)
        assert tree.query(0, 2) == 24
        assert tree.query(0, 1) == 6

    def test_lcm_operation(self) -> None:
        """Test LCM operation."""

        def lcm_op(a, b):
            return abs(a * b) // math.gcd(a, b)

        tree = SegmentTree([4, 6, 8], operation=lcm_op, identity=1)
        result = tree.query(0, 2)
        assert result == 24


class TestSegmentTreeEdgeCases:
    """Test edge cases."""

    def test_single_element_array(self) -> None:
        """Test with single element."""
        tree = SegmentTree([42], operation="sum")
        assert tree.query(0, 0) == 42
        tree.update(0, 100)
        assert tree.query(0, 0) == 100

    def test_two_element_array(self) -> None:
        """Test with two elements."""
        tree = SegmentTree([1, 2], operation="sum")
        assert tree.query(0, 1) == 3
        assert tree.query(0, 0) == 1
        assert tree.query(1, 1) == 2

    def test_all_same_values(self) -> None:
        """Test with all same values."""
        tree = SegmentTree([5, 5, 5, 5], operation="sum")
        assert tree.query(0, 3) == 20
        assert tree.query(1, 2) == 10

    def test_negative_numbers(self) -> None:
        """Test with negative numbers."""
        tree = SegmentTree([-5, -2, -8, -1], operation="sum")
        assert tree.query(0, 3) == -16
        tree.update(0, 10)
        assert tree.query(0, 3) == -1

    def test_floating_point_numbers(self) -> None:
        """Test with floating point numbers."""
        tree = SegmentTree([1.5, 2.5, 3.5], operation="sum")
        assert tree.query(0, 2) == 7.5

    def test_zero_values(self) -> None:
        """Test with zeros."""
        tree = SegmentTree([0, 0, 0], operation="sum")
        assert tree.query(0, 2) == 0
        tree.update(1, 5)
        assert tree.query(0, 2) == 5


class TestSegmentTreeRealWorldScenarios:
    """Test real-world usage scenarios."""

    def test_range_sum_after_updates(self) -> None:
        """Test range sum with multiple updates."""
        # Like tracking account balances
        balances = [100, 200, 150, 300, 250]
        tree = SegmentTree(balances, operation="sum")

        # Initial total
        assert tree.query(0, 4) == 1000

        # Update balances
        tree.update(0, 150)  # Account 0: +50
        tree.update(2, 100)  # Account 2: -50
        assert tree.query(0, 4) == 1000  # Total unchanged

    def test_range_minimum_temperature(self) -> None:
        """Test finding minimum temperature in range."""
        temperatures = [20, 18, 22, 17, 19, 21]
        tree = SegmentTree(temperatures, operation="min")

        # Coldest temperature in first half
        assert tree.query(0, 2) == 18

        # Coldest overall
        assert tree.query(0, 5) == 17

    def test_range_maximum_price(self) -> None:
        """Test finding maximum price in range."""
        prices = [100, 105, 98, 110, 95, 108]
        tree = SegmentTree(prices, operation="max")

        # Highest price in range
        assert tree.query(0, 3) == 110

        # Update price
        tree.update(4, 115)
        assert tree.query(0, 5) == 115

    def test_stock_price_analysis(self) -> None:
        """Test stock price analysis."""
        # Daily stock prices
        prices = [100, 102, 98, 105, 103, 107, 110]
        tree = SegmentTree(prices, operation="max")

        # Max price in week
        assert tree.query(0, 6) == 110

        # Max price in first 3 days
        assert tree.query(0, 2) == 102

        # Price changes
        tree.update(3, 115)  # Price spike
        assert tree.query(0, 6) == 115


class TestSegmentTreePerformance:
    """Test performance characteristics."""

    def test_large_array_creation(self) -> None:
        """Test creating tree with large array."""
        arr = list(range(1000))
        tree = SegmentTree(arr, operation="sum")
        assert tree.size == 1000

    def test_multiple_queries_on_large_tree(self) -> None:
        """Test multiple queries on large tree."""
        arr = list(range(1000))
        tree = SegmentTree(arr, operation="sum")

        # Multiple range queries
        assert tree.query(0, 99) == sum(range(100))
        assert tree.query(500, 599) == sum(range(500, 600))
        assert tree.query(0, 999) == sum(range(1000))

    def test_multiple_updates_on_large_tree(self) -> None:
        """Test multiple updates on large tree."""
        arr = [1] * 1000
        tree = SegmentTree(arr, operation="sum")

        # Initial sum
        assert tree.query(0, 999) == 1000

        # Multiple updates
        for i in range(0, 100):
            tree.update(i, 10)

        assert tree.query(0, 99) == 1000  # 100 * 10
        assert tree.query(0, 999) == 1900  # 100*10 + 900*1


class TestSegmentTreeComplexScenarios:
    """Test complex usage scenarios."""

    def test_alternating_queries_and_updates(self) -> None:
        """Test alternating queries and updates."""
        tree = SegmentTree([1, 2, 3, 4, 5], operation="sum")

        assert tree.query(0, 4) == 15
        tree.update(2, 10)
        assert tree.query(0, 4) == 22
        tree.update(0, 5)
        assert tree.query(0, 4) == 26
        tree.update(4, 1)
        assert tree.query(0, 4) == 22

    def test_overlapping_range_queries(self) -> None:
        """Test overlapping range queries."""
        tree = SegmentTree([1, 2, 3, 4, 5], operation="sum")

        assert tree.query(0, 2) == 6
        assert tree.query(1, 3) == 9
        assert tree.query(2, 4) == 12
        # Sum of all three should equal sum of unique elements
        # But they overlap, so we can't add them directly

    def test_segment_tree_maintains_correctness(self) -> None:
        """Test that segment tree maintains correctness."""
        import random

        arr = [random.randint(1, 100) for _ in range(50)]
        tree = SegmentTree(arr, operation="sum")

        # Verify random ranges match brute force
        for _ in range(20):
            left = random.randint(0, 40)
            right = random.randint(left, 49)
            expected = sum(arr[left : right + 1])
            actual = tree.query(left, right)
            assert actual == expected

    def test_min_max_consistency(self) -> None:
        """Test min and max operations are consistent."""
        arr = [5, 2, 8, 1, 9, 3]

        min_tree = SegmentTree(arr, operation="min")
        max_tree = SegmentTree(arr, operation="max")

        # Min and max of same range
        assert min_tree.query(0, 5) == 1
        assert max_tree.query(0, 5) == 9

        # After updates
        min_tree.update(3, 10)
        max_tree.update(3, 10)

        assert min_tree.query(0, 5) == 2
        assert max_tree.query(0, 5) == 10
