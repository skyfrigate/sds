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

"""Tests for AVL Tree implementation."""

import pytest

from sds.core.exceptions import EmptyStructureError
from sds.tree import AVLNode
from sds.tree.balanced import AVLTree


class TestAVLNodeCreation:
    """Test AVL node creation."""

    def test_create_avl_node(self) -> None:
        """Test creating an AVL node."""
        node = AVLNode(10)
        assert node.data == 10
        assert node.height == 0
        assert node.left is None
        assert node.right is None

    def test_avl_node_with_children(self) -> None:
        """Test AVL node with children."""
        left = AVLNode(5)
        right = AVLNode(15)
        root = AVLNode(10, left=left, right=right)
        assert root.left is left
        assert root.right is right
        assert left.parent is root
        assert right.parent is root


class TestAVLTreeCreation:
    """Test AVL tree creation and basic properties."""

    def test_create_empty_avl(self) -> None:
        """Test creating an empty AVL tree."""
        avl = AVLTree()
        assert avl.is_empty()
        assert len(avl) == 0
        assert avl.root is None
        assert avl.height() == -1

    def test_avl_bool(self) -> None:
        """Test boolean evaluation."""
        avl = AVLTree()
        assert not avl
        avl.insert(10)
        assert avl


class TestAVLTreeInsertion:
    """Test AVL tree insertion with automatic balancing."""

    def test_insert_single_element(self) -> None:
        """Test inserting a single element."""
        avl = AVLTree()
        avl.insert(10)
        assert len(avl) == 1
        assert avl.root.data == 10
        assert avl.height() == 0

    def test_insert_no_rotation_needed(self) -> None:
        """Test insertion that doesn't require rotation."""
        avl = AVLTree()
        avl.insert(10)
        avl.insert(5)
        avl.insert(15)
        assert len(avl) == 3
        assert avl.root.data == 10
        assert avl.height() == 1

    def test_insert_left_left_case(self) -> None:
        """Test left-left case requiring right rotation."""
        avl = AVLTree()
        avl.insert(30)
        avl.insert(20)
        avl.insert(10)  # Triggers right rotation
        # Tree should be: 20 as root, 10 left, 30 right
        assert avl.root.data == 20
        assert avl.root.left.data == 10
        assert avl.root.right.data == 30
        assert avl.height() == 1

    def test_insert_right_right_case(self) -> None:
        """Test right-right case requiring left rotation."""
        avl = AVLTree()
        avl.insert(10)
        avl.insert(20)
        avl.insert(30)  # Triggers left rotation
        # Tree should be: 20 as root, 10 left, 30 right
        assert avl.root.data == 20
        assert avl.root.left.data == 10
        assert avl.root.right.data == 30
        assert avl.height() == 1

    def test_insert_left_right_case(self) -> None:
        """Test left-right case requiring left-right rotation."""
        avl = AVLTree()
        avl.insert(30)
        avl.insert(10)
        avl.insert(20)  # Triggers left-right rotation
        # Tree should be: 20 as root, 10 left, 30 right
        assert avl.root.data == 20
        assert avl.root.left.data == 10
        assert avl.root.right.data == 30

    def test_insert_right_left_case(self) -> None:
        """Test right-left case requiring right-left rotation."""
        avl = AVLTree()
        avl.insert(10)
        avl.insert(30)
        avl.insert(20)  # Triggers right-left rotation
        # Tree should be: 20 as root, 10 left, 30 right
        assert avl.root.data == 20
        assert avl.root.left.data == 10
        assert avl.root.right.data == 30

    def test_insert_multiple_elements_balanced(self) -> None:
        """Test that tree stays balanced with multiple insertions."""
        avl = AVLTree()
        # Insert 1-7 in order (worst case for BST)
        for i in range(1, 8):
            avl.insert(i)
        # AVL should keep height at O(log n)
        assert len(avl) == 7
        assert avl.height() <= 3  # log2(7) ≈ 2.8

    def test_insert_maintains_bst_property(self) -> None:
        """Test that AVL maintains BST property."""
        avl = AVLTree()
        values = [50, 25, 75, 10, 30, 60, 80, 5, 15, 27, 55]
        for val in values:
            avl.insert(val)
        # Inorder should give sorted values
        result = list(avl.inorder_traversal())
        assert result == sorted(values)

    def test_height_stays_logarithmic(self) -> None:
        """Test that height stays O(log n) even with sequential inserts."""
        avl = AVLTree()
        # Insert 100 elements in order
        for i in range(100):
            avl.insert(i)
        # Height should be around log2(100) ≈ 6.6
        assert avl.height() <= 8  # With some slack for AVL overhead


class TestAVLTreeSearch:
    """Test AVL tree search operations."""

    def test_search_empty_tree(self) -> None:
        """Test searching in empty tree."""
        avl = AVLTree()
        assert not avl.search(10)

    def test_search_existing_elements(self) -> None:
        """Test searching for existing elements."""
        avl = AVLTree()
        values = [50, 25, 75, 10, 30, 60, 80]
        for val in values:
            avl.insert(val)
        for val in values:
            assert avl.search(val)

    def test_search_non_existing(self) -> None:
        """Test searching for non-existing elements."""
        avl = AVLTree()
        for val in [10, 20, 30]:
            avl.insert(val)
        assert not avl.search(5)
        assert not avl.search(25)
        assert not avl.search(100)

    def test_contains_operator(self) -> None:
        """Test __contains__ method."""
        avl = AVLTree()
        for val in [10, 20, 30]:
            avl.insert(val)
        assert 10 in avl
        assert 20 in avl
        assert 5 not in avl


class TestAVLTreeRemoval:
    """Test AVL tree removal with rebalancing."""

    def test_remove_from_empty_tree(self) -> None:
        """Test removing from empty tree."""
        avl = AVLTree()
        with pytest.raises(EmptyStructureError):
            avl.remove(10)

    def test_remove_non_existing(self) -> None:
        """Test removing non-existing element."""
        avl = AVLTree()
        avl.insert(10)
        with pytest.raises(ValueError):
            avl.remove(5)

    def test_remove_leaf(self) -> None:
        """Test removing a leaf node."""
        avl = AVLTree()
        for val in [10, 5, 15, 3, 7]:
            avl.insert(val)
        avl.remove(3)
        assert len(avl) == 4
        assert not avl.search(3)
        # Tree should still be balanced
        assert abs(avl._get_balance_factor(avl.root)) <= 1

    def test_remove_with_rebalancing(self) -> None:
        """Test removal that triggers rebalancing."""
        avl = AVLTree()
        # Create a tree that will need rebalancing on removal
        for val in [10, 5, 15, 3, 7, 12, 20, 1]:
            avl.insert(val)
        avl.remove(20)
        avl.remove(15)
        # Tree should remain balanced
        result = list(avl.inorder_traversal())
        assert result == sorted(result)
        # Check balance at root
        assert abs(avl._get_balance_factor(avl.root)) <= 1

    def test_remove_root(self) -> None:
        """Test removing root node."""
        avl = AVLTree()
        for val in [10, 5, 15, 3, 7, 12, 20]:
            avl.insert(val)
        old_root = avl.root.data
        avl.remove(old_root)
        assert not avl.search(old_root)
        assert len(avl) == 6
        # Tree should still be valid and balanced
        result = list(avl.inorder_traversal())
        assert result == sorted(result)

    def test_remove_maintains_balance(self) -> None:
        """Test that removals maintain AVL balance property."""
        avl = AVLTree()
        values = list(range(1, 16))  # 1 to 15
        for val in values:
            avl.insert(val)

        # Remove half the elements
        for val in [1, 3, 5, 7, 9]:
            avl.remove(val)

        # Verify balance at every node
        def check_balance(node):
            if node is None:
                return True
            balance = avl._get_balance_factor(node)
            if abs(balance) > 1:
                return False
            return check_balance(node.left) and check_balance(node.right)

        assert check_balance(avl.root)


class TestAVLTreeTraversal:
    """Test AVL tree traversals."""

    def test_inorder_traversal_empty(self) -> None:
        """Test inorder traversal of empty tree."""
        avl = AVLTree()
        assert list(avl.inorder_traversal()) == []

    def test_inorder_gives_sorted(self) -> None:
        """Test that inorder traversal gives sorted values."""
        avl = AVLTree()
        import random

        values = list(range(1, 20))
        random.shuffle(values)
        for val in values:
            avl.insert(val)
        result = list(avl.inorder_traversal())
        assert result == sorted(values)

    def test_preorder_traversal(self) -> None:
        """Test preorder traversal."""
        avl = AVLTree()
        for val in [10, 5, 15]:
            avl.insert(val)
        # After balancing, tree is 10-5-15
        result = list(avl.preorder_traversal())
        assert result[0] == 10  # Root first

    def test_postorder_traversal(self) -> None:
        """Test postorder traversal."""
        avl = AVLTree()
        for val in [10, 5, 15]:
            avl.insert(val)
        result = list(avl.postorder_traversal())
        assert result[-1] == 10  # Root last

    def test_level_order_traversal(self) -> None:
        """Test level-order traversal."""
        avl = AVLTree()
        for val in [10, 5, 15, 3, 7, 12, 20]:
            avl.insert(val)
        result = list(avl.level_order_traversal())
        # Check that it's level by level
        assert len(result) == 7

    def test_iter_uses_inorder(self) -> None:
        """Test that __iter__ uses inorder."""
        avl = AVLTree()
        values = [50, 25, 75, 10, 30]
        for val in values:
            avl.insert(val)
        assert list(avl) == sorted(values)


class TestAVLTreeClear:
    """Test AVL tree clear operation."""

    def test_clear_empty_tree(self) -> None:
        """Test clearing empty tree."""
        avl = AVLTree()
        avl.clear()
        assert avl.is_empty()

    def test_clear_non_empty(self) -> None:
        """Test clearing non-empty tree."""
        avl = AVLTree()
        for val in [10, 5, 15, 3, 7]:
            avl.insert(val)
        avl.clear()
        assert avl.is_empty()
        assert len(avl) == 0
        assert avl.root is None

    def test_reuse_after_clear(self) -> None:
        """Test that tree is usable after clear."""
        avl = AVLTree()
        for val in [10, 5, 15]:
            avl.insert(val)
        avl.clear()
        avl.insert(20)
        assert len(avl) == 1
        assert avl.search(20)


class TestAVLTreeStringRepresentation:
    """Test string representations."""

    def test_repr_empty(self) -> None:
        """Test repr of empty tree."""
        avl = AVLTree()
        assert repr(avl) == "AVLTree(size=0)"

    def test_repr_non_empty(self) -> None:
        """Test repr of non-empty tree."""
        avl = AVLTree()
        avl.insert(10)
        avl.insert(5)
        assert repr(avl) == "AVLTree(size=2)"

    def test_str_empty(self) -> None:
        """Test str of empty tree."""
        avl = AVLTree()
        assert str(avl) == "AVLTree: []"

    def test_str_non_empty(self) -> None:
        """Test str of non-empty tree shows sorted values."""
        avl = AVLTree()
        for val in [30, 10, 20]:
            avl.insert(val)
        assert str(avl) == "AVLTree: [10, 20, 30]"


class TestAVLTreeBalanceProperty:
    """Test that AVL balance property is maintained."""

    def verify_avl_property(self, avl: AVLTree) -> bool:
        """Helper to verify AVL property recursively."""

        def check_node(node):
            if node is None:
                return True, -1

            left_valid, left_height = check_node(node.left)
            if not left_valid:
                return False, 0

            right_valid, right_height = check_node(node.right)
            if not right_valid:
                return False, 0

            balance = left_height - right_height
            if abs(balance) > 1:
                return False, 0

            height = 1 + max(left_height, right_height)
            if node.height != height:
                return False, 0

            return True, height

        valid, _ = check_node(avl.root)
        return valid

    def test_balance_after_insertions(self) -> None:
        """Test balance property after many insertions."""
        avl = AVLTree()
        for i in range(50):
            avl.insert(i)
        assert self.verify_avl_property(avl)

    def test_balance_after_mixed_operations(self) -> None:
        """Test balance after mixed insert/remove operations."""
        avl = AVLTree()
        values = list(range(1, 21))
        for val in values:
            avl.insert(val)

        # Remove some elements
        for val in [5, 10, 15]:
            avl.remove(val)

        assert self.verify_avl_property(avl)

    def test_balance_worst_case_insertions(self) -> None:
        """Test balance with worst-case sequential insertions."""
        avl = AVLTree()
        # Sequential insertions (worst case for unbalanced BST)
        for i in range(1, 32):
            avl.insert(i)
        # Should maintain O(log n) height
        assert avl.height() <= 5  # log2(31) ≈ 4.95
        assert self.verify_avl_property(avl)


class TestAVLTreeEdgeCases:
    """Test edge cases and special scenarios."""

    def test_duplicate_insertions(self) -> None:
        """Test inserting duplicate values."""
        avl = AVLTree()
        avl.insert(10)
        avl.insert(10)
        avl.insert(10)
        assert len(avl) == 3
        # Duplicates should maintain BST property (go right)
        result = list(avl.inorder_traversal())
        assert result == [10, 10, 10]

    def test_single_node_operations(self) -> None:
        """Test operations on single-node tree."""
        avl = AVLTree()
        avl.insert(42)
        assert avl.height() == 0
        assert list(avl) == [42]
        avl.remove(42)
        assert avl.is_empty()

    def test_string_values(self) -> None:
        """Test AVL with string values."""
        avl = AVLTree()
        words = ["dog", "cat", "elephant", "ant", "zebra"]
        for word in words:
            avl.insert(word)
        result = list(avl)
        assert result == sorted(words)

    def test_negative_numbers(self) -> None:
        """Test AVL with negative numbers."""
        avl = AVLTree()
        values = [0, -5, 5, -3, 3, -10, 10]
        for val in values:
            avl.insert(val)
        result = list(avl)
        assert result == sorted(values)


class TestAVLTreePerformance:
    """Test performance characteristics of AVL tree."""

    def test_height_logarithmic_large_dataset(self) -> None:
        """Test that height stays logarithmic with large dataset."""
        avl = AVLTree()
        n = 1000
        for i in range(n):
            avl.insert(i)
        # Height should be roughly log2(n) with AVL constant
        import math

        max_expected_height = int(1.44 * math.log2(n + 2) - 1)
        assert avl.height() <= max_expected_height

    def test_operations_after_many_insertions(self) -> None:
        """Test that operations remain fast after many insertions."""
        avl = AVLTree()
        # Insert many elements
        for i in range(500):
            avl.insert(i)
        # Search should still be fast (O(log n))
        assert avl.search(250)
        assert not avl.search(1000)
        # Height should be reasonable
        assert avl.height() <= 10


class TestAVLTreeComparison:
    """Compare AVL with unbalanced BST."""

    def test_avl_better_height_than_bst(self) -> None:
        """Test that AVL maintains better height than BST."""
        from sds.tree.binary import BinarySearchTree

        avl = AVLTree()
        bst = BinarySearchTree()

        # Insert sequential values (worst case for BST)
        for i in range(1, 16):
            avl.insert(i)
            bst.insert(i)

        # AVL should have much better height
        assert avl.height() < bst.height()
        assert avl.height() <= 4  # O(log n)
        assert bst.height() == 14  # O(n) - degenerate
