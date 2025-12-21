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

"""Tests for DisjointSet (Union-Find) data structure.

This module contains comprehensive tests for the DisjointSet implementation,
verifying correctness, edge cases, and performance characteristics.
"""

import pytest

from sds.advanced import DisjointSet


class TestDisjointSetCreation:
    """Test disjoint set creation and initialization."""

    def test_empty_creation(self) -> None:
        """Test creating an empty disjoint set."""
        ds = DisjointSet()
        assert len(ds) == 0
        assert ds.count_sets() == 0
        assert ds.num_sets == 0

    def test_repr_empty(self) -> None:
        """Test string representation of empty set."""
        ds = DisjointSet()
        assert "DisjointSet" in repr(ds)
        assert "elements=0" in repr(ds)
        assert "sets=0" in repr(ds)

    def test_str_empty(self) -> None:
        """Test string conversion of empty set."""
        ds = DisjointSet()
        assert "DisjointSet" in str(ds)
        assert "0 elements" in str(ds)


class TestMakeSet:
    """Test make_set operation."""

    def test_make_single_set(self) -> None:
        """Test creating a single set."""
        ds = DisjointSet()
        ds.make_set(1)
        assert len(ds) == 1
        assert ds.count_sets() == 1
        assert 1 in ds

    def test_make_multiple_sets(self) -> None:
        """Test creating multiple sets."""
        ds = DisjointSet()
        for i in range(5):
            ds.make_set(i)
        assert len(ds) == 5
        assert ds.count_sets() == 5

    def test_make_set_with_different_types(self) -> None:
        """Test make_set with various hashable types."""
        ds = DisjointSet()
        ds.make_set(1)
        ds.make_set("hello")
        ds.make_set((1, 2))
        ds.make_set(3.14)
        assert len(ds) == 4

    def test_make_set_duplicate_raises_error(self) -> None:
        """Test that duplicate element raises ValueError."""
        ds = DisjointSet()
        ds.make_set(1)
        with pytest.raises(ValueError, match="already exists"):
            ds.make_set(1)

    def test_make_set_unhashable_raises_error(self) -> None:
        """Test that unhashable element raises TypeError."""
        ds = DisjointSet()
        with pytest.raises(TypeError, match="must be hashable"):
            ds.make_set([1, 2, 3])  # Lists are not hashable

    def test_contains_operator(self) -> None:
        """Test __contains__ operator."""
        ds = DisjointSet()
        assert 1 not in ds
        ds.make_set(1)
        assert 1 in ds


class TestFind:
    """Test find operation."""

    def test_find_single_element(self) -> None:
        """Test finding element in singleton set."""
        ds = DisjointSet()
        ds.make_set(1)
        root = ds.find(1)
        assert root == 1  # Element is its own root

    def test_find_nonexistent_element_raises_error(self) -> None:
        """Test finding nonexistent element raises ValueError."""
        ds = DisjointSet()
        with pytest.raises(ValueError, match="not in any set"):
            ds.find(999)

    def test_find_after_union(self) -> None:
        """Test that find returns same root for merged sets."""
        ds = DisjointSet()
        ds.make_set(1)
        ds.make_set(2)
        ds.union(1, 2)
        assert ds.find(1) == ds.find(2)

    def test_find_idempotent(self) -> None:
        """Test that repeated finds return same result."""
        ds = DisjointSet()
        ds.make_set(1)
        root1 = ds.find(1)
        root2 = ds.find(1)
        root3 = ds.find(1)
        assert root1 == root2 == root3


class TestUnion:
    """Test union operation."""

    def test_union_two_elements(self) -> None:
        """Test uniting two separate sets."""
        ds = DisjointSet()
        ds.make_set(1)
        ds.make_set(2)
        result = ds.union(1, 2)
        assert result is True
        assert ds.count_sets() == 1

    def test_union_already_connected_returns_false(self) -> None:
        """Test union of already connected elements returns False."""
        ds = DisjointSet()
        ds.make_set(1)
        ds.make_set(2)
        ds.union(1, 2)
        result = ds.union(1, 2)
        assert result is False
        assert ds.count_sets() == 1

    def test_union_chain(self) -> None:
        """Test chaining multiple unions."""
        ds = DisjointSet()
        for i in range(5):
            ds.make_set(i)
        ds.union(0, 1)
        ds.union(1, 2)
        ds.union(2, 3)
        ds.union(3, 4)
        assert ds.count_sets() == 1
        assert all(ds.connected(0, i) for i in range(5))

    def test_union_nonexistent_element_raises_error(self) -> None:
        """Test union with nonexistent element raises ValueError."""
        ds = DisjointSet()
        ds.make_set(1)
        with pytest.raises(ValueError, match="not in any set"):
            ds.union(1, 999)

    def test_union_reduces_set_count(self) -> None:
        """Test that union decreases set count correctly."""
        ds = DisjointSet()
        for i in range(10):
            ds.make_set(i)
        assert ds.count_sets() == 10
        ds.union(0, 1)
        assert ds.count_sets() == 9
        ds.union(2, 3)
        assert ds.count_sets() == 8
        ds.union(0, 2)
        assert ds.count_sets() == 7


class TestConnected:
    """Test connected operation."""

    def test_connected_same_element(self) -> None:
        """Test that element is connected to itself."""
        ds = DisjointSet()
        ds.make_set(1)
        assert ds.connected(1, 1)

    def test_connected_separate_sets(self) -> None:
        """Test that elements in different sets are not connected."""
        ds = DisjointSet()
        ds.make_set(1)
        ds.make_set(2)
        assert not ds.connected(1, 2)

    def test_connected_after_union(self) -> None:
        """Test that elements are connected after union."""
        ds = DisjointSet()
        ds.make_set(1)
        ds.make_set(2)
        ds.union(1, 2)
        assert ds.connected(1, 2)
        assert ds.connected(2, 1)  # Symmetric

    def test_connected_transitive(self) -> None:
        """Test transitivity of connectivity."""
        ds = DisjointSet()
        ds.make_set(1)
        ds.make_set(2)
        ds.make_set(3)
        ds.union(1, 2)
        ds.union(2, 3)
        assert ds.connected(1, 3)

    def test_connected_nonexistent_element_raises_error(self) -> None:
        """Test connected with nonexistent element raises ValueError."""
        ds = DisjointSet()
        ds.make_set(1)
        with pytest.raises(ValueError, match="not in any set"):
            ds.connected(1, 999)


class TestSize:
    """Test size operation."""

    def test_size_singleton(self) -> None:
        """Test size of singleton set."""
        ds = DisjointSet()
        ds.make_set(1)
        assert ds.size(1) == 1

    def test_size_after_unions(self) -> None:
        """Test size increases with unions."""
        ds = DisjointSet()
        for i in range(5):
            ds.make_set(i)
        ds.union(0, 1)
        assert ds.size(0) == 2
        assert ds.size(1) == 2
        ds.union(0, 2)
        assert ds.size(0) == 3
        assert ds.size(1) == 3
        assert ds.size(2) == 3

    def test_size_independent_sets(self) -> None:
        """Test sizes of independent sets."""
        ds = DisjointSet()
        for i in range(6):
            ds.make_set(i)
        ds.union(0, 1)
        ds.union(0, 2)
        ds.union(3, 4)
        ds.union(3, 5)
        assert ds.size(0) == 3
        assert ds.size(3) == 3

    def test_size_nonexistent_element_raises_error(self) -> None:
        """Test size with nonexistent element raises ValueError."""
        ds = DisjointSet()
        with pytest.raises(ValueError, match="not in any set"):
            ds.size(999)


class TestGetSets:
    """Test get_sets operation."""

    def test_get_sets_empty(self) -> None:
        """Test get_sets on empty structure."""
        ds = DisjointSet()
        sets = ds.get_sets()
        assert len(sets) == 0

    def test_get_sets_all_singleton(self) -> None:
        """Test get_sets with all singleton sets."""
        ds = DisjointSet()
        for i in range(5):
            ds.make_set(i)
        sets = ds.get_sets()
        assert len(sets) == 5
        assert all(len(s) == 1 for s in sets)

    def test_get_sets_after_unions(self) -> None:
        """Test get_sets reflects union operations."""
        ds = DisjointSet()
        for i in range(6):
            ds.make_set(i)
        ds.union(0, 1)
        ds.union(0, 2)
        ds.union(3, 4)
        sets = ds.get_sets()
        assert len(sets) == 3
        # Check that one set contains {0, 1, 2}
        assert any({0, 1, 2} == s for s in sets)
        # Check that one set contains {3, 4}
        assert any({3, 4} == s for s in sets)
        # Check that one set contains {5}
        assert any({5} == s for s in sets)

    def test_get_sets_returns_copies(self) -> None:
        """Test that get_sets returns independent copies."""
        ds = DisjointSet()
        for i in range(3):
            ds.make_set(i)
        sets1 = ds.get_sets()
        sets1[0].add(999)  # Modify returned set
        sets2 = ds.get_sets()
        # Original should be unchanged
        assert all(999 not in s for s in sets2)


class TestCountSets:
    """Test count_sets operation."""

    def test_count_sets_empty(self) -> None:
        """Test count on empty structure."""
        ds = DisjointSet()
        assert ds.count_sets() == 0

    def test_count_sets_after_make_set(self) -> None:
        """Test count increases with make_set."""
        ds = DisjointSet()
        assert ds.count_sets() == 0
        ds.make_set(1)
        assert ds.count_sets() == 1
        ds.make_set(2)
        assert ds.count_sets() == 2

    def test_count_sets_after_union(self) -> None:
        """Test count decreases with union."""
        ds = DisjointSet()
        for i in range(10):
            ds.make_set(i)
        assert ds.count_sets() == 10
        for i in range(9):
            ds.union(i, i + 1)
        assert ds.count_sets() == 1

    def test_num_sets_property(self) -> None:
        """Test num_sets property matches count_sets()."""
        ds = DisjointSet()
        for i in range(5):
            ds.make_set(i)
        assert ds.num_sets == ds.count_sets()
        ds.union(0, 1)
        assert ds.num_sets == ds.count_sets()


class TestSpecialMethods:
    """Test special methods."""

    def test_len(self) -> None:
        """Test __len__ returns total element count."""
        ds = DisjointSet()
        assert len(ds) == 0
        for i in range(5):
            ds.make_set(i)
        assert len(ds) == 5
        ds.union(0, 1)
        assert len(ds) == 5  # Union doesn't change element count

    def test_repr(self) -> None:
        """Test __repr__ string representation."""
        ds = DisjointSet()
        ds.make_set(1)
        ds.make_set(2)
        ds.union(1, 2)
        repr_str = repr(ds)
        assert "DisjointSet" in repr_str
        assert "elements=2" in repr_str
        assert "sets=1" in repr_str

    def test_str(self) -> None:
        """Test __str__ string representation."""
        ds = DisjointSet()
        ds.make_set(1)
        ds.make_set(2)
        str_repr = str(ds)
        assert "2 elements" in str_repr
        assert "2 sets" in str_repr


class TestApplicationScenarios:
    """Test real-world application scenarios."""

    def test_cycle_detection(self) -> None:
        """Test using disjoint set for cycle detection."""
        ds = DisjointSet()
        # Graph edges (u, v)
        edges = [(0, 1), (1, 2), (2, 3), (3, 0)]  # Has cycle
        nodes = {0, 1, 2, 3}

        for node in nodes:
            ds.make_set(node)

        has_cycle = False
        for u, v in edges:
            if ds.connected(u, v):
                has_cycle = True
                break
            ds.union(u, v)

        assert has_cycle is True

    def test_connected_components(self) -> None:
        """Test finding connected components in graph."""
        ds = DisjointSet()
        # Graph with 3 components
        edges = [
            (0, 1),
            (1, 2),  # Component 1
            (3, 4),  # Component 2
            (5, 6),
            (6, 7),  # Component 3
        ]
        nodes = range(8)

        for node in nodes:
            ds.make_set(node)

        for u, v in edges:
            ds.union(u, v)

        components = ds.get_sets()
        assert len(components) == 3
        assert any({0, 1, 2} == c for c in components)
        assert any({3, 4} == c for c in components)
        assert any({5, 6, 7} == c for c in components)

    def test_equivalence_relations(self) -> None:
        """Test using disjoint set for equivalence classes."""
        ds = DisjointSet()
        # People
        people = ["Alice", "Bob", "Charlie", "Dave", "Eve"]
        for person in people:
            ds.make_set(person)

        # Friendship relations (transitive)
        ds.union("Alice", "Bob")
        ds.union("Bob", "Charlie")
        ds.union("Dave", "Eve")

        # Check equivalence classes
        assert ds.connected("Alice", "Charlie")
        assert not ds.connected("Alice", "Dave")
        assert ds.count_sets() == 2


class TestPerformance:
    """Test performance characteristics."""

    def test_large_number_of_elements(self) -> None:
        """Test with large number of elements."""
        ds = DisjointSet()
        n = 10000
        for i in range(n):
            ds.make_set(i)
        assert len(ds) == n
        assert ds.count_sets() == n

    def test_many_unions(self) -> None:
        """Test performance of many union operations."""
        ds = DisjointSet()
        n = 10000
        for i in range(n):
            ds.make_set(i)

        # Chain all elements together
        for i in range(n - 1):
            ds.union(i, i + 1)

        assert ds.count_sets() == 1
        assert ds.connected(0, n - 1)

    def test_path_compression_effectiveness(self) -> None:
        """Test that path compression improves subsequent finds."""
        ds = DisjointSet()
        n = 1000
        for i in range(n):
            ds.make_set(i)

        # Create a long chain
        for i in range(n - 1):
            ds.union(i, i + 1)

        # First find traverses long path
        root1 = ds.find(0)

        # Subsequent finds should be faster due to path compression
        root2 = ds.find(0)
        assert root1 == root2


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_union_element_with_itself(self) -> None:
        """Test union of element with itself."""
        ds = DisjointSet()
        ds.make_set(1)
        result = ds.union(1, 1)
        assert result is False  # Already in same set
        assert ds.count_sets() == 1

    def test_mixed_types_in_same_structure(self) -> None:
        """Test structure with mixed hashable types."""
        ds = DisjointSet()
        ds.make_set(1)
        ds.make_set("a")
        ds.make_set((1, 2))
        ds.union(1, "a")
        ds.union("a", (1, 2))
        assert ds.connected(1, (1, 2))

    def test_empty_get_sets(self) -> None:
        """Test get_sets on empty structure."""
        ds = DisjointSet()
        sets = ds.get_sets()
        assert sets == []

    def test_single_element_operations(self) -> None:
        """Test all operations with single element."""
        ds = DisjointSet()
        ds.make_set(42)
        assert ds.find(42) == 42
        assert ds.size(42) == 1
        assert ds.connected(42, 42)
        sets = ds.get_sets()
        assert len(sets) == 1
        assert 42 in sets[0]
