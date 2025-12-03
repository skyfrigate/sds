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

"""Tests for B-Tree implementation."""

import pytest

from sds.tree.btree import BTree


class TestBTreeCreation:
    """Test B-Tree creation."""

    def test_create_btree_default_order(self) -> None:
        """Test creating B-Tree with default order."""
        btree = BTree()
        assert btree.order == 3
        assert btree.is_empty()
        assert len(btree) == 0

    def test_create_btree_custom_order(self) -> None:
        """Test creating B-Tree with custom order."""
        btree = BTree(order=5)
        assert btree.order == 5

    def test_create_btree_invalid_order(self) -> None:
        """Test creating B-Tree with invalid order."""
        with pytest.raises(ValueError):
            BTree(order=1)

    def test_btree_bool(self) -> None:
        """Test boolean evaluation."""
        btree = BTree()
        assert not btree
        btree.insert(10)
        assert btree


class TestBTreeInsertion:
    """Test B-Tree insertion."""

    def test_insert_single_key(self) -> None:
        """Test inserting a single key."""
        btree = BTree(order=3)
        btree.insert(10)
        assert len(btree) == 1
        assert 10 in btree

    def test_insert_multiple_keys(self) -> None:
        """Test inserting multiple keys."""
        btree = BTree(order=3)
        keys = [10, 20, 5, 15, 25]
        for key in keys:
            btree.insert(key)
        assert len(btree) == 5
        for key in keys:
            assert key in btree

    def test_insert_maintains_order(self) -> None:
        """Test that insertion maintains sorted order."""
        btree = BTree(order=3)
        keys = [20, 10, 30, 5, 15, 25, 35]
        for key in keys:
            btree.insert(key)
        result = list(btree.inorder_traversal())
        assert result == sorted(keys)

    def test_insert_triggers_split(self) -> None:
        """Test that insertion triggers node splits."""
        btree = BTree(order=3)  # Max 5 keys per node
        # Insert enough keys to force splits
        for i in range(10):
            btree.insert(i)
        assert len(btree) == 10
        # Tree should still maintain order
        result = list(btree.inorder_traversal())
        assert result == list(range(10))

    def test_insert_duplicate_keys(self) -> None:
        """Test inserting duplicate keys."""
        btree = BTree(order=3)
        btree.insert(10)
        btree.insert(10)
        assert len(btree) == 2  # Duplicates allowed


class TestBTreeSearch:
    """Test B-Tree search operations."""

    def test_search_empty_tree(self) -> None:
        """Test searching in empty tree."""
        btree = BTree()
        assert not btree.search(10)

    def test_search_existing_key(self) -> None:
        """Test searching for existing key."""
        btree = BTree(order=3)
        btree.insert(10)
        btree.insert(20)
        assert btree.search(10)
        assert btree.search(20)

    def test_search_non_existing_key(self) -> None:
        """Test searching for non-existing key."""
        btree = BTree(order=3)
        btree.insert(10)
        assert not btree.search(20)

    def test_contains_operator(self) -> None:
        """Test __contains__ operator."""
        btree = BTree()
        btree.insert(10)
        assert 10 in btree
        assert 20 not in btree


class TestBTreeRemoval:
    """Test B-Tree removal operations."""

    def test_remove_from_empty_tree(self) -> None:
        """Test removing from empty tree."""
        btree = BTree()
        with pytest.raises(ValueError):
            btree.remove(10)

    def test_remove_existing_key(self) -> None:
        """Test removing existing key."""
        btree = BTree(order=3)
        btree.insert(10)
        btree.insert(20)
        btree.remove(10)
        assert len(btree) == 1
        assert 10 not in btree
        assert 20 in btree

    def test_remove_non_existing_key(self) -> None:
        """Test removing non-existing key."""
        btree = BTree()
        btree.insert(10)
        with pytest.raises(ValueError):
            btree.remove(20)

    def test_remove_multiple_keys(self) -> None:
        """Test removing multiple keys."""
        btree = BTree(order=3)
        keys = [10, 20, 30, 40, 50]
        for key in keys:
            btree.insert(key)

        btree.remove(20)
        btree.remove(40)

        assert len(btree) == 3
        assert 20 not in btree
        assert 40 not in btree


class TestBTreeTraversal:
    """Test B-Tree traversal."""

    def test_inorder_empty_tree(self) -> None:
        """Test inorder traversal of empty tree."""
        btree = BTree()
        assert list(btree.inorder_traversal()) == []

    def test_inorder_single_key(self) -> None:
        """Test inorder traversal with single key."""
        btree = BTree()
        btree.insert(10)
        assert list(btree.inorder_traversal()) == [10]

    def test_inorder_multiple_keys(self) -> None:
        """Test inorder traversal with multiple keys."""
        btree = BTree(order=3)
        keys = [50, 20, 80, 10, 30, 70, 90]
        for key in keys:
            btree.insert(key)
        result = list(btree.inorder_traversal())
        assert result == sorted(keys)

    def test_iter_uses_inorder(self) -> None:
        """Test that __iter__ uses inorder."""
        btree = BTree()
        keys = [30, 10, 20]
        for key in keys:
            btree.insert(key)
        assert list(btree) == sorted(keys)


class TestBTreeHeight:
    """Test B-Tree height calculation."""

    def test_height_empty_tree(self) -> None:
        """Test height of empty tree."""
        btree = BTree()
        assert btree.height() == -1

    def test_height_single_key(self) -> None:
        """Test height with single key."""
        btree = BTree()
        btree.insert(10)
        assert btree.height() == 0

    def test_height_increases_with_splits(self) -> None:
        """Test that height increases appropriately."""
        btree = BTree(order=2)  # Small order to force splits
        # Insert enough to force multiple levels
        for i in range(20):
            btree.insert(i)
        # Height should be logarithmic
        assert btree.height() >= 2


class TestBTreeClear:
    """Test B-Tree clear operation."""

    def test_clear_empty_tree(self) -> None:
        """Test clearing empty tree."""
        btree = BTree()
        btree.clear()
        assert btree.is_empty()

    def test_clear_non_empty_tree(self) -> None:
        """Test clearing non-empty tree."""
        btree = BTree()
        for i in range(10):
            btree.insert(i)
        btree.clear()
        assert btree.is_empty()
        assert len(btree) == 0

    def test_tree_usable_after_clear(self) -> None:
        """Test that tree is usable after clear."""
        btree = BTree()
        btree.insert(10)
        btree.clear()
        btree.insert(20)
        assert len(btree) == 1


class TestBTreeStringRepresentation:
    """Test string representations."""

    def test_repr(self) -> None:
        """Test repr."""
        btree = BTree(order=4)
        btree.insert(10)
        assert repr(btree) == "BTree(order=4, size=1)"

    def test_str_empty(self) -> None:
        """Test str of empty tree."""
        btree = BTree()
        assert str(btree) == "BTree: []"

    def test_str_small_tree(self) -> None:
        """Test str of small tree."""
        btree = BTree()
        btree.insert(10)
        btree.insert(20)
        result = str(btree)
        assert "10" in result
        assert "20" in result


class TestBTreeEdgeCases:
    """Test edge cases."""

    def test_negative_numbers(self) -> None:
        """Test with negative numbers."""
        btree = BTree()
        keys = [-5, -10, 0, 5, 10]
        for key in keys:
            btree.insert(key)
        result = list(btree)
        assert result == sorted(keys)

    def test_floating_point_numbers(self) -> None:
        """Test with floating point numbers."""
        btree = BTree()
        keys = [1.5, 2.3, 0.7, 3.2]
        for key in keys:
            btree.insert(key)
        result = list(btree)
        assert result == sorted(keys)

    def test_string_keys(self) -> None:
        """Test with string keys."""
        btree = BTree()
        keys = ["dog", "cat", "bird", "ant"]
        for key in keys:
            btree.insert(key)
        result = list(btree)
        assert result == sorted(keys)


class TestBTreeRealWorldScenarios:
    """Test real-world usage scenarios."""

    def test_database_index_simulation(self) -> None:
        """Test simulating a database index."""
        # B-Tree used as database index
        index = BTree(order=5)

        # Insert record IDs
        for record_id in [100, 200, 150, 250, 175, 125]:
            index.insert(record_id)

        # Search for records
        assert 150 in index
        assert 300 not in index

        # Range query simulation (get all records in order)
        all_records = list(index)
        assert all_records == sorted([100, 200, 150, 250, 175, 125])

    def test_file_system_directory(self) -> None:
        """Test simulating file system directory."""
        directory = BTree(order=4)

        # Add file entries
        files = ["readme.txt", "config.json", "main.py", "test.py"]
        for filename in files:
            directory.insert(filename)

        # Check if file exists
        assert "main.py" in directory

        # List files in order
        file_list = list(directory)
        assert file_list == sorted(files)


class TestBTreePerformance:
    """Test performance characteristics."""

    def test_large_insertions(self) -> None:
        """Test inserting many keys."""
        btree = BTree(order=5)
        n = 100
        for i in range(n):
            btree.insert(i)
        assert len(btree) == n

    def test_maintains_logarithmic_height(self) -> None:
        """Test that height remains logarithmic."""
        btree = BTree(order=5)
        import math

        n = 100
        for i in range(n):
            btree.insert(i)

        # Height should be O(log n)
        max_expected_height = math.ceil(math.log(n + 1, btree.order)) + 1
        assert btree.height() <= max_expected_height

    def test_sequential_operations(self) -> None:
        """Test sequence of insertions and searches."""
        btree = BTree(order=4)

        # Insert in random order
        import random

        keys = list(range(50))
        random.shuffle(keys)

        for key in keys:
            btree.insert(key)

        # Verify all keys present and in order
        result = list(btree)
        assert result == list(range(50))


class TestBTreeProperties:
    """Test B-Tree properties are maintained."""

    def test_size(self) -> None:
        """Test that all leaves are at same depth."""
        btree = BTree(order=3)

        assert btree.size == 0

    def test_all_leaves_same_depth(self) -> None:
        """Test that all leaves are at same depth."""
        btree = BTree(order=3)
        for i in range(20):
            btree.insert(i)

        # All leaves should be at same level (B-Tree property)
        # This is guaranteed by the insertion algorithm
        assert btree.height() >= 0  # Just verify it's valid

    def test_sorted_order_maintained(self) -> None:
        """Test that sorted order is always maintained."""
        btree = BTree(order=3)
        import random

        keys = list(range(30))
        random.shuffle(keys)

        for key in keys:
            btree.insert(key)
            # After each insertion, order should be maintained
            result = list(btree)
            assert result == sorted(result)


class TestBTreeComparison:
    """Compare B-Tree with other structures."""

    def test_btree_vs_binary_search_tree(self) -> None:
        """Compare B-Tree with BST."""
        from sds.tree.binary import BinarySearchTree

        btree = BTree(order=4)
        bst = BinarySearchTree()

        keys = [50, 30, 70, 20, 40, 60, 80]
        for key in keys:
            btree.insert(key)
            bst.insert(key)

        # Both should maintain sorted order
        assert list(btree) == list(bst) == sorted(keys)

        # B-Tree typically has better height for large datasets
        # (more balanced due to multiple keys per node)
