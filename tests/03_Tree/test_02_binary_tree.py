"""Tests for BinaryTree class."""

import pytest

from sds.core.exceptions import EmptyStructureError
from sds.tree.binary import BinaryTree
from sds.tree.interfaces import AbstractBinaryTree


class TestBinaryTreeCreation:
    """Tests for BinaryTree creation and initialization."""

    def test_binary_tree_creation(self):
        """Test creating an empty binary tree."""
        tree = BinaryTree()
        assert tree.is_empty()
        assert len(tree) == 0
        assert tree.size == 0
        assert tree.root is None

    def test_binary_tree_inherits_from_abstract(self):
        """Test that BinaryTree inherits from AbstractBinaryTree."""
        tree = BinaryTree()
        assert isinstance(tree, AbstractBinaryTree)


class TestBinaryTreeInsertion:
    """Tests for insertion operations."""

    def test_insert_into_empty_tree(self):
        """Test inserting into an empty tree."""
        tree = BinaryTree()
        tree.insert(10)
        assert not tree.is_empty()
        assert len(tree) == 1
        assert tree.root.data == 10

    def test_insert_multiple_items(self):
        """Test inserting multiple items."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)
        assert len(tree) == 3
        assert tree.root.data == 10
        assert tree.root.left.data == 5
        assert tree.root.right.data == 15

    def test_insert_maintains_complete_tree(self):
        """Test that insertion maintains complete tree structure."""
        tree = BinaryTree()
        for i in range(7):
            tree.insert(i)

        # Level 0: 0
        assert tree.root.data == 0
        # Level 1: 1, 2
        assert tree.root.left.data == 1
        assert tree.root.right.data == 2
        # Level 2: 3, 4, 5, 6
        assert tree.root.left.left.data == 3
        assert tree.root.left.right.data == 4
        assert tree.root.right.left.data == 5
        assert tree.root.right.right.data == 6

    def test_insert_increments_size(self):
        """Test that insert increments size correctly."""
        tree = BinaryTree()
        for i in range(5):
            tree.insert(i)
            assert len(tree) == i + 1


class TestBinaryTreeSearch:
    """Tests for search operations."""

    def test_search_in_empty_tree(self):
        """Test searching in an empty tree."""
        tree = BinaryTree()
        assert tree.search(10) is False

    def test_search_existing_item(self):
        """Test searching for existing items."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)
        assert tree.search(10) is True
        assert tree.search(5) is True
        assert tree.search(15) is True

    def test_search_non_existing_item(self):
        """Test searching for non-existing item."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        assert tree.search(15) is False
        assert tree.search(100) is False

    def test_contains_operator(self):
        """Test __contains__ operator."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        assert 10 in tree
        assert 5 in tree
        assert 15 not in tree


class TestBinaryTreeRemoval:
    """Tests for removal operations."""

    def test_remove_from_empty_tree_raises_error(self):
        """Test that removing from empty tree raises error."""
        tree = BinaryTree()
        with pytest.raises(EmptyStructureError):
            tree.remove(10)

    def test_remove_non_existing_item_raises_error(self):
        """Test that removing non-existing item raises error."""
        tree = BinaryTree()
        tree.insert(10)
        with pytest.raises(ValueError):
            tree.remove(5)

    def test_remove_root_from_single_node_tree(self):
        """Test removing root from tree with only one node."""
        tree = BinaryTree()
        tree.insert(10)
        result = tree.remove(10)
        assert result == 10
        assert tree.is_empty()
        assert tree.root is None

    def test_remove_item_from_tree(self):
        """Test removing an item from tree."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)

        result = tree.remove(5)
        assert result == 5
        assert len(tree) == 2
        assert tree.search(5) is False

    def test_remove_decrements_size(self):
        """Test that remove decrements size."""
        tree = BinaryTree()
        for i in range(5):
            tree.insert(i)

        initial_size = len(tree)
        tree.remove(2)
        assert len(tree) == initial_size - 1


class TestBinaryTreeHeight:
    """Tests for height calculation."""

    def test_height_of_empty_tree(self):
        """Test height of empty tree is -1."""
        tree = BinaryTree()
        assert tree.height() == -1

    def test_height_of_single_node_tree(self):
        """Test height of tree with one node is 0."""
        tree = BinaryTree()
        tree.insert(10)
        assert tree.height() == 0

    def test_height_of_two_level_tree(self):
        """Test height of tree with two levels."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)
        assert tree.height() == 1

    def test_height_of_three_level_tree(self):
        """Test height of tree with three levels."""
        tree = BinaryTree()
        for i in range(7):
            tree.insert(i)
        assert tree.height() == 2


class TestBinaryTreeClear:
    """Tests for clear operation."""

    def test_clear_empty_tree(self):
        """Test clearing an empty tree."""
        tree = BinaryTree()
        tree.clear()
        assert tree.is_empty()
        assert tree.root is None

    def test_clear_non_empty_tree(self):
        """Test clearing a non-empty tree."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)

        tree.clear()
        assert tree.is_empty()
        assert len(tree) == 0
        assert tree.root is None


class TestBinaryTreeInorderTraversal:
    """Tests for inorder traversal."""

    def test_inorder_empty_tree(self):
        """Test inorder traversal of empty tree."""
        tree = BinaryTree()
        result = list(tree.inorder_traversal())
        assert result == []

    def test_inorder_single_node(self):
        """Test inorder traversal of single node."""
        tree = BinaryTree()
        tree.insert(10)
        result = list(tree.inorder_traversal())
        assert result == [10]

    def test_inorder_multiple_nodes(self):
        """Test inorder traversal of multiple nodes."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)
        result = list(tree.inorder_traversal())
        assert result == [5, 10, 15]

    def test_inorder_complete_tree(self):
        """Test inorder traversal of complete tree."""
        tree = BinaryTree()
        for i in range(7):
            tree.insert(i)
        result = list(tree.inorder_traversal())
        assert result == [3, 1, 4, 0, 5, 2, 6]


class TestBinaryTreePreorderTraversal:
    """Tests for preorder traversal."""

    def test_preorder_empty_tree(self):
        """Test preorder traversal of empty tree."""
        tree = BinaryTree()
        result = list(tree.preorder_traversal())
        assert result == []

    def test_preorder_single_node(self):
        """Test preorder traversal of single node."""
        tree = BinaryTree()
        tree.insert(10)
        result = list(tree.preorder_traversal())
        assert result == [10]

    def test_preorder_multiple_nodes(self):
        """Test preorder traversal of multiple nodes."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)
        result = list(tree.preorder_traversal())
        assert result == [10, 5, 15]

    def test_preorder_complete_tree(self):
        """Test preorder traversal of complete tree."""
        tree = BinaryTree()
        for i in range(7):
            tree.insert(i)
        result = list(tree.preorder_traversal())
        assert result == [0, 1, 3, 4, 2, 5, 6]


class TestBinaryTreePostorderTraversal:
    """Tests for postorder traversal."""

    def test_postorder_empty_tree(self):
        """Test postorder traversal of empty tree."""
        tree = BinaryTree()
        result = list(tree.postorder_traversal())
        assert result == []

    def test_postorder_single_node(self):
        """Test postorder traversal of single node."""
        tree = BinaryTree()
        tree.insert(10)
        result = list(tree.postorder_traversal())
        assert result == [10]

    def test_postorder_multiple_nodes(self):
        """Test postorder traversal of multiple nodes."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)
        result = list(tree.postorder_traversal())
        assert result == [5, 15, 10]

    def test_postorder_complete_tree(self):
        """Test postorder traversal of complete tree."""
        tree = BinaryTree()
        for i in range(7):
            tree.insert(i)
        result = list(tree.postorder_traversal())
        assert result == [3, 4, 1, 5, 6, 2, 0]


class TestBinaryTreeLevelOrderTraversal:
    """Tests for level-order traversal."""

    def test_level_order_empty_tree(self):
        """Test level-order traversal of empty tree."""
        tree = BinaryTree()
        result = list(tree.level_order_traversal())
        assert result == []

    def test_level_order_single_node(self):
        """Test level-order traversal of single node."""
        tree = BinaryTree()
        tree.insert(10)
        result = list(tree.level_order_traversal())
        assert result == [10]

    def test_level_order_multiple_nodes(self):
        """Test level-order traversal of multiple nodes."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)
        result = list(tree.level_order_traversal())
        assert result == [10, 5, 15]

    def test_level_order_complete_tree(self):
        """Test level-order traversal of complete tree."""
        tree = BinaryTree()
        for i in range(7):
            tree.insert(i)
        result = list(tree.level_order_traversal())
        assert result == [0, 1, 2, 3, 4, 5, 6]


class TestBinaryTreeIteration:
    """Tests for iteration (default inorder)."""

    def test_iter_uses_inorder(self):
        """Test that __iter__ uses inorder traversal."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)

        iter_result = list(tree)
        inorder_result = list(tree.inorder_traversal())
        assert iter_result == inorder_result


class TestBinaryTreeStringRepresentations:
    """Tests for __repr__ and __str__."""

    def test_repr_empty_tree(self):
        """Test __repr__ of empty tree."""
        tree = BinaryTree()
        assert repr(tree) == "BinaryTree(size=0)"

    def test_repr_non_empty_tree(self):
        """Test __repr__ of non-empty tree."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        assert repr(tree) == "BinaryTree(size=2)"

    def test_str_empty_tree(self):
        """Test __str__ of empty tree."""
        tree = BinaryTree()
        assert str(tree) == "BinaryTree: []"

    def test_str_non_empty_tree(self):
        """Test __str__ of non-empty tree."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)
        assert str(tree) == "BinaryTree: [10, 5, 15]"


class TestBinaryTreeEdgeCases:
    """Tests for edge cases."""

    def test_insert_none_value(self):
        """Test inserting None as a value."""
        tree = BinaryTree()
        tree.insert(None)
        assert len(tree) == 1
        assert tree.root.data is None

    def test_search_none_value(self):
        """Test searching for None."""
        tree = BinaryTree()
        tree.insert(None)
        assert tree.search(None) is True

    def test_insert_duplicate_values(self):
        """Test inserting duplicate values."""
        tree = BinaryTree()
        tree.insert(10)
        tree.insert(10)
        assert len(tree) == 2

    def test_large_tree(self):
        """Test with a large number of nodes."""
        tree = BinaryTree()
        n = 100
        for i in range(n):
            tree.insert(i)
        assert len(tree) == n
        assert tree.height() == 6  # log2(100) ≈ 6.64
