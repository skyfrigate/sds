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

"""Tests for Binary Search Tree implementation."""

import pytest

from sds.core.exceptions import EmptyStructureError
from sds.tree.binary import BinarySearchTree


class TestBinarySearchTreeCreation:
    """Test BST creation and basic properties."""

    def test_create_empty_bst(self) -> None:
        """Test creating an empty BST."""
        bst = BinarySearchTree()
        assert bst.is_empty()
        assert len(bst) == 0
        assert bst.root is None
        assert bst.size == 0

    def test_bst_bool(self) -> None:
        """Test boolean evaluation of BST."""
        bst = BinarySearchTree()
        assert not bst
        bst.insert(10)
        assert bst

    def test_empty_bst_height(self) -> None:
        """Test height of empty BST."""
        bst = BinarySearchTree()
        assert bst.height() == -1


class TestBinarySearchTreeInsertion:
    """Test BST insertion operations."""

    def test_insert_single_element(self) -> None:
        """Test inserting a single element."""
        bst = BinarySearchTree()
        bst.insert(10)
        assert not bst.is_empty()
        assert len(bst) == 1
        assert bst.root is not None
        assert bst.root.data == 10
        assert bst.height() == 0

    def test_insert_multiple_elements(self) -> None:
        """Test inserting multiple elements."""
        bst = BinarySearchTree()
        values = [10, 5, 15, 3, 7, 12, 20]
        for val in values:
            bst.insert(val)
        assert len(bst) == 7
        assert bst.root.data == 10

    def test_insert_maintains_bst_property(self) -> None:
        """Test that insertion maintains BST property."""
        bst = BinarySearchTree()
        bst.insert(10)
        bst.insert(5)
        bst.insert(15)
        bst.insert(3)
        bst.insert(7)

        # Check BST property
        assert bst.root.data == 10
        assert bst.root.left.data == 5
        assert bst.root.right.data == 15
        assert bst.root.left.left.data == 3
        assert bst.root.left.right.data == 7

    def test_insert_duplicates(self) -> None:
        """Test inserting duplicate values (go to right)."""
        bst = BinarySearchTree()
        bst.insert(10)
        bst.insert(10)
        bst.insert(10)
        assert len(bst) == 3
        # Duplicates should go to the right
        assert bst.root.right.data == 10

    def test_insert_sorted_ascending(self) -> None:
        """Test inserting sorted values (worst case - right skewed)."""
        bst = BinarySearchTree()
        for i in range(1, 6):
            bst.insert(i)
        assert len(bst) == 5
        assert bst.height() == 4  # Degenerate tree

    def test_insert_sorted_descending(self) -> None:
        """Test inserting reverse sorted values (left skewed)."""
        bst = BinarySearchTree()
        for i in range(5, 0, -1):
            bst.insert(i)
        assert len(bst) == 5
        assert bst.height() == 4  # Degenerate tree


class TestBinarySearchTreeSearch:
    """Test BST search operations."""

    def test_search_empty_tree(self) -> None:
        """Test searching in empty tree."""
        bst = BinarySearchTree()
        assert not bst.search(10)

    def test_search_existing_elements(self) -> None:
        """Test searching for existing elements."""
        bst = BinarySearchTree()
        values = [10, 5, 15, 3, 7, 12, 20]
        for val in values:
            bst.insert(val)

        for val in values:
            assert bst.search(val)

    def test_search_non_existing_elements(self) -> None:
        """Test searching for non-existing elements."""
        bst = BinarySearchTree()
        for val in [10, 5, 15]:
            bst.insert(val)

        assert not bst.search(3)
        assert not bst.search(7)
        assert not bst.search(100)

    def test_contains_operator(self) -> None:
        """Test __contains__ method (in operator)."""
        bst = BinarySearchTree()
        bst.insert(10)
        bst.insert(5)
        bst.insert(15)

        assert 10 in bst
        assert 5 in bst
        assert 15 in bst
        assert 3 not in bst


class TestBinarySearchTreeMinMax:
    """Test finding min and max values."""

    def test_find_min_empty_tree(self) -> None:
        """Test finding min in empty tree."""
        bst = BinarySearchTree()
        with pytest.raises(EmptyStructureError):
            bst.find_min()

    def test_find_max_empty_tree(self) -> None:
        """Test finding max in empty tree."""
        bst = BinarySearchTree()
        with pytest.raises(EmptyStructureError):
            bst.find_max()

    def test_find_min_single_element(self) -> None:
        """Test finding min with single element."""
        bst = BinarySearchTree()
        bst.insert(10)
        assert bst.find_min() == 10

    def test_find_max_single_element(self) -> None:
        """Test finding max with single element."""
        bst = BinarySearchTree()
        bst.insert(10)
        assert bst.find_max() == 10

    def test_find_min_multiple_elements(self) -> None:
        """Test finding min with multiple elements."""
        bst = BinarySearchTree()
        values = [10, 5, 15, 3, 7, 12, 20]
        for val in values:
            bst.insert(val)
        assert bst.find_min() == 3

    def test_find_max_multiple_elements(self) -> None:
        """Test finding max with multiple elements."""
        bst = BinarySearchTree()
        values = [10, 5, 15, 3, 7, 12, 20]
        for val in values:
            bst.insert(val)
        assert bst.find_max() == 20


class TestBinarySearchTreeRemoval:
    """Test BST removal operations."""

    def test_remove_from_empty_tree(self) -> None:
        """Test removing from empty tree."""
        bst = BinarySearchTree()
        with pytest.raises(EmptyStructureError):
            bst.remove(10)

    def test_remove_non_existing_element(self) -> None:
        """Test removing non-existing element."""
        bst = BinarySearchTree()
        bst.insert(10)
        with pytest.raises(ValueError):
            bst.remove(5)

    def test_remove_leaf_node(self) -> None:
        """Test removing a leaf node."""
        bst = BinarySearchTree()
        for val in [10, 5, 15, 3, 7]:
            bst.insert(val)

        assert bst.remove(3) == 3
        assert len(bst) == 4
        assert not bst.search(3)
        assert bst.search(5)

    def test_remove_node_with_one_child_left(self) -> None:
        """Test removing node with only left child."""
        bst = BinarySearchTree()
        for val in [10, 5, 3]:
            bst.insert(val)

        assert bst.remove(5) == 5
        assert len(bst) == 2
        assert not bst.search(5)
        assert bst.search(3)
        assert bst.search(10)

    def test_remove_node_with_one_child_right(self) -> None:
        """Test removing node with only right child."""
        bst = BinarySearchTree()
        for val in [10, 5, 7]:
            bst.insert(val)

        assert bst.remove(5) == 5
        assert len(bst) == 2
        assert not bst.search(5)
        assert bst.search(7)

    def test_remove_node_with_two_children(self) -> None:
        """Test removing node with two children."""
        bst = BinarySearchTree()
        for val in [10, 5, 15, 3, 7, 12, 20]:
            bst.insert(val)

        assert bst.remove(5) == 5
        assert len(bst) == 6
        assert not bst.search(5)
        # Check BST property is maintained
        inorder = list(bst.inorder_traversal())
        assert inorder == sorted(inorder)

    def test_remove_root_node(self) -> None:
        """Test removing root node."""
        bst = BinarySearchTree()
        for val in [10, 5, 15, 3, 7, 12, 20]:
            bst.insert(val)

        assert bst.remove(10) == 10
        assert len(bst) == 6
        assert not bst.search(10)
        # Tree should still be valid BST
        inorder = list(bst.inorder_traversal())
        assert inorder == sorted(inorder)

    def test_remove_all_elements(self) -> None:
        """Test removing all elements."""
        bst = BinarySearchTree()
        values = [10, 5, 15]
        for val in values:
            bst.insert(val)

        for val in values:
            bst.remove(val)

        assert bst.is_empty()
        assert len(bst) == 0


class TestBinarySearchTreeTraversal:
    """Test BST traversal operations."""

    def test_inorder_traversal_empty(self) -> None:
        """Test inorder traversal of empty tree."""
        bst = BinarySearchTree()
        result = list(bst.inorder_traversal())
        assert result == []

    def test_inorder_traversal_sorted(self) -> None:
        """Test inorder traversal returns sorted values."""
        bst = BinarySearchTree()
        values = [10, 5, 15, 3, 7, 12, 20]
        for val in values:
            bst.insert(val)

        result = list(bst.inorder_traversal())
        assert result == sorted(values)

    def test_preorder_traversal(self) -> None:
        """Test preorder traversal."""
        bst = BinarySearchTree()
        for val in [10, 5, 15, 3, 7]:
            bst.insert(val)

        result = list(bst.preorder_traversal())
        assert result == [10, 5, 3, 7, 15]

    def test_postorder_traversal(self) -> None:
        """Test postorder traversal."""
        bst = BinarySearchTree()
        for val in [10, 5, 15, 3, 7]:
            bst.insert(val)

        result = list(bst.postorder_traversal())
        assert result == [3, 7, 5, 15, 10]

    def test_level_order_traversal(self) -> None:
        """Test level-order traversal."""
        bst = BinarySearchTree()
        for val in [10, 5, 15, 3, 7, 12, 20]:
            bst.insert(val)

        result = list(bst.level_order_traversal())
        assert result == [10, 5, 15, 3, 7, 12, 20]

    def test_iter_uses_inorder(self) -> None:
        """Test that __iter__ uses inorder traversal."""
        bst = BinarySearchTree()
        values = [10, 5, 15, 3, 7]
        for val in values:
            bst.insert(val)

        result = list(bst)
        assert result == sorted(values)


class TestBinarySearchTreeClear:
    """Test BST clear operation."""

    def test_clear_empty_tree(self) -> None:
        """Test clearing empty tree."""
        bst = BinarySearchTree()
        bst.clear()
        assert bst.is_empty()
        assert len(bst) == 0

    def test_clear_non_empty_tree(self) -> None:
        """Test clearing non-empty tree."""
        bst = BinarySearchTree()
        for val in [10, 5, 15, 3, 7]:
            bst.insert(val)

        bst.clear()
        assert bst.is_empty()
        assert len(bst) == 0
        assert bst.root is None

    def test_tree_usable_after_clear(self) -> None:
        """Test that tree is usable after clear."""
        bst = BinarySearchTree()
        for val in [10, 5, 15]:
            bst.insert(val)

        bst.clear()
        bst.insert(20)
        assert len(bst) == 1
        assert bst.search(20)


class TestBinarySearchTreeStringRepresentation:
    """Test string representations."""

    def test_repr_empty_tree(self) -> None:
        """Test repr of empty tree."""
        bst = BinarySearchTree()
        assert repr(bst) == "BinarySearchTree(size=0)"

    def test_repr_non_empty_tree(self) -> None:
        """Test repr of non-empty tree."""
        bst = BinarySearchTree()
        bst.insert(10)
        bst.insert(5)
        assert repr(bst) == "BinarySearchTree(size=2)"

    def test_str_empty_tree(self) -> None:
        """Test str of empty tree."""
        bst = BinarySearchTree()
        assert str(bst) == "BinarySearchTree: []"

    def test_str_non_empty_tree(self) -> None:
        """Test str of non-empty tree shows sorted values."""
        bst = BinarySearchTree()
        for val in [10, 5, 15]:
            bst.insert(val)
        assert str(bst) == "BinarySearchTree: [5, 10, 15]"


class TestBinarySearchTreeHeight:
    """Test height calculation."""

    def test_height_single_node(self) -> None:
        """Test height with single node."""
        bst = BinarySearchTree()
        bst.insert(10)
        assert bst.height() == 0

    def test_height_balanced_tree(self) -> None:
        """Test height of balanced tree."""
        bst = BinarySearchTree()
        for val in [10, 5, 15, 3, 7, 12, 20]:
            bst.insert(val)
        assert bst.height() == 2

    def test_height_left_skewed(self) -> None:
        """Test height of left-skewed tree."""
        bst = BinarySearchTree()
        for val in [5, 4, 3, 2, 1]:
            bst.insert(val)
        assert bst.height() == 4

    def test_height_right_skewed(self) -> None:
        """Test height of right-skewed tree."""
        bst = BinarySearchTree()
        for val in [1, 2, 3, 4, 5]:
            bst.insert(val)
        assert bst.height() == 4


class TestBinarySearchTreeEdgeCases:
    """Test edge cases and special scenarios."""

    def test_insert_string_values(self) -> None:
        """Test BST with string values."""
        bst = BinarySearchTree()
        words = ["dog", "cat", "elephant", "ant", "zebra"]
        for word in words:
            bst.insert(word)

        result = list(bst.inorder_traversal())
        assert result == sorted(words)

    def test_insert_negative_numbers(self) -> None:
        """Test BST with negative numbers."""
        bst = BinarySearchTree()
        values = [0, -5, 5, -3, 3, -10, 10]
        for val in values:
            bst.insert(val)

        result = list(bst.inorder_traversal())
        assert result == sorted(values)

    def test_single_node_operations(self) -> None:
        """Test operations on single-node tree."""
        bst = BinarySearchTree()
        bst.insert(42)

        assert bst.find_min() == 42
        assert bst.find_max() == 42
        assert bst.height() == 0
        assert list(bst.inorder_traversal()) == [42]
        assert list(bst.preorder_traversal()) == [42]
        assert list(bst.postorder_traversal()) == [42]
        assert list(bst.level_order_traversal()) == [42]

        bst.remove(42)
        assert bst.is_empty()

    def test_complex_removal_sequence(self) -> None:
        """Test complex sequence of removals."""
        bst = BinarySearchTree()
        values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 65]
        for val in values:
            bst.insert(val)

        # Remove nodes in various orders
        bst.remove(20)  # Node with two children
        bst.remove(30)  # Node with two children
        bst.remove(50)  # Root with two children

        remaining = list(bst.inorder_traversal())
        # Check that BST property is maintained
        assert remaining == sorted(remaining)
        assert len(bst) == len(values) - 3


class TestBinarySearchTreePropertyInvariance:
    """Test that BST property is maintained."""

    def test_bst_property_after_insertions(self) -> None:
        """Test BST property is maintained after insertions."""
        bst = BinarySearchTree()
        import random

        values = list(range(1, 20))
        random.shuffle(values)

        for val in values:
            bst.insert(val)

        # Inorder traversal should give sorted sequence
        result = list(bst.inorder_traversal())
        assert result == sorted(values)

    def test_bst_property_after_removals(self) -> None:
        """Test BST property is maintained after removals."""
        bst = BinarySearchTree()
        values = [10, 5, 15, 3, 7, 12, 20, 1, 4, 6, 8]
        for val in values:
            bst.insert(val)

        # Remove several nodes
        for val in [3, 7, 15]:
            bst.remove(val)

        # Check BST property
        result = list(bst.inorder_traversal())
        assert result == sorted(result)
