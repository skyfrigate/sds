"""Tests for BTree class.

This module contains comprehensive tests for the BTree class,
ensuring proper functionality of all methods and B-Tree properties.
"""

import pytest

from sds.core.exceptions import EmptyStructureError
from sds.tree.btree import BTree


class TestBTreeInit:
    """Tests for BTree initialization."""

    def test_init_default(self):
        """Test default initialization."""
        tree = BTree()
        assert tree.t == 3
        assert tree.is_empty()
        assert len(tree) == 0
        assert tree.root is None
        assert tree.height() == -1

    def test_init_custom_t(self):
        """Test initialization with custom t."""
        for t in [2, 3, 5, 10, 50]:
            tree = BTree(t=t)
            assert tree.t == t
            assert tree.is_empty()

    def test_init_invalid_t_zero(self):
        """Test that t=0 raises ValueError."""
        with pytest.raises(ValueError, match="at least 2"):
            BTree(t=0)

    def test_init_invalid_t_one(self):
        """Test that t=1 raises ValueError."""
        with pytest.raises(ValueError, match="at least 2"):
            BTree(t=1)

    def test_init_invalid_t_negative(self):
        """Test that negative t raises ValueError."""
        with pytest.raises(ValueError, match="at least 2"):
            BTree(t=-5)


class TestBTreeInsertSimple:
    """Tests for simple insertion operations."""

    def test_insert_single_key(self):
        """Test inserting a single key."""
        tree = BTree(t=3)
        tree.insert(10)
        assert len(tree) == 1
        assert tree.search(10)
        assert tree.root.keys == [10]
        assert tree.root.is_leaf

    def test_insert_multiple_keys_no_split(self):
        """Test inserting multiple keys without splitting."""
        tree = BTree(t=3)
        keys = [10, 20, 5, 15]
        for key in keys:
            tree.insert(key)

        assert len(tree) == 4
        for key in keys:
            assert tree.search(key)

    def test_insert_sorted_order(self):
        """Test that insertion maintains sorted order."""
        tree = BTree(t=3)
        tree.insert(10)
        tree.insert(20)
        tree.insert(5)
        tree.insert(15)

        assert list(tree) == [5, 10, 15, 20]

    def test_insert_duplicate_ignored(self):
        """Test that duplicate insertions are ignored."""
        tree = BTree(t=3)
        tree.insert(10)
        tree.insert(20)
        tree.insert(10)  # Duplicate

        assert len(tree) == 2
        assert list(tree) == [10, 20]

    def test_insert_ascending_order(self):
        """Test inserting keys in ascending order."""
        tree = BTree(t=2)
        for i in range(1, 8):
            tree.insert(i * 10)

        assert len(tree) == 7
        assert list(tree) == [10, 20, 30, 40, 50, 60, 70]

    def test_insert_descending_order(self):
        """Test inserting keys in descending order."""
        tree = BTree(t=2)
        for i in range(7, 0, -1):
            tree.insert(i * 10)

        assert len(tree) == 7
        assert list(tree) == [10, 20, 30, 40, 50, 60, 70]

    def test_insert_random_order(self):
        """Test inserting keys in random order."""
        tree = BTree(t=3)
        keys = [50, 20, 80, 10, 30, 70, 90, 5, 15, 25]
        for key in keys:
            tree.insert(key)

        assert len(tree) == len(keys)
        assert list(tree) == sorted(keys)


class TestBTreeInsertWithSplit:
    """Tests for insertion with node splitting."""

    def test_insert_causes_root_split(self):
        """Test insertion that causes root to split."""
        tree = BTree(t=2)  # Max 3 keys per node

        # Insert 4 keys to force split
        for i in [10, 20, 30, 40]:
            tree.insert(i)

        assert len(tree) == 4
        assert tree.height() == 1
        # Root should have moved up
        assert len(tree.root.keys) >= 1
        assert not tree.root.is_leaf

    def test_insert_multiple_splits(self):
        """Test insertion causing multiple splits."""
        tree = BTree(t=2)

        # Insert many keys to cause multiple splits
        for i in range(1, 16):
            tree.insert(i * 10)

        assert len(tree) == 15
        assert list(tree) == [i * 10 for i in range(1, 16)]
        # Height should stay logarithmic
        assert tree.height() <= 3

    def test_split_maintains_sorted_order(self):
        """Test that splits maintain sorted order."""
        tree = BTree(t=2)
        keys = list(range(1, 11))

        for key in keys:
            tree.insert(key)
            # Check sorted order after each insertion
            assert list(tree) == sorted([k for k in keys if k <= key])

    def test_split_updates_parent_correctly(self):
        """Test that split correctly updates parent references."""
        tree = BTree(t=2)

        for i in range(1, 8):
            tree.insert(i)

        # Verify all nodes have correct parent references
        def check_parents(node):
            if not node.is_leaf:
                for child in node.children:
                    assert child.parent is node or child.parent._parent is None
                    check_parents(child)

        if tree.root:
            check_parents(tree.root)

    def test_split_child_keys_distribution(self):
        """Test that split distributes keys correctly."""
        tree = BTree(t=3)  # Max 5 keys
        # Fill root to trigger split
        for i in range(1, 7):
            tree.insert(i * 10)

        # After split, verify tree structure
        assert tree.height() >= 1
        # All keys should still be present
        assert sorted(list(tree)) == [10, 20, 30, 40, 50, 60]


class TestBTreeSearch:
    """Tests for search operations."""

    def test_search_empty_tree(self):
        """Test searching in empty tree."""
        tree = BTree()
        assert tree.search(10) is False

    def test_search_single_key(self):
        """Test searching with single key."""
        tree = BTree()
        tree.insert(10)
        assert tree.search(10) is True
        assert tree.search(20) is False

    def test_search_multiple_keys(self):
        """Test searching with multiple keys."""
        tree = BTree(t=3)
        keys = [10, 20, 5, 15, 30, 25]
        for key in keys:
            tree.insert(key)

        for key in keys:
            assert tree.search(key) is True

        assert tree.search(7) is False
        assert tree.search(100) is False

    def test_search_after_splits(self):
        """Test searching after node splits."""
        tree = BTree(t=2)
        keys = list(range(1, 16))
        for key in keys:
            tree.insert(key)

        for key in keys:
            assert tree.search(key) is True

    def test_contains_operator(self):
        """Test 'in' operator."""
        tree = BTree()
        tree.insert(10)
        tree.insert(20)

        assert 10 in tree
        assert 20 in tree
        assert 30 not in tree


class TestBTreeRemoveLeaf:
    """Tests for removal from leaf nodes."""

    def test_remove_single_key(self):
        """Test removing single key."""
        tree = BTree()
        tree.insert(10)
        removed = tree.remove(10)

        assert removed == 10
        assert len(tree) == 0
        assert tree.is_empty()

    def test_remove_from_leaf_multiple_keys(self):
        """Test removing from leaf with multiple keys."""
        tree = BTree(t=3)
        keys = [10, 20, 5, 15]
        for key in keys:
            tree.insert(key)

        tree.remove(15)
        assert len(tree) == 3
        assert tree.search(15) is False
        assert list(tree) == [5, 10, 20]

    def test_remove_maintains_order(self):
        """Test that removal maintains sorted order."""
        tree = BTree(t=3)
        keys = [10, 20, 30, 40, 50]
        for key in keys:
            tree.insert(key)

        tree.remove(30)
        assert list(tree) == [10, 20, 40, 50]

    def test_remove_empty_tree(self):
        """Test removing from empty tree raises error."""
        tree = BTree()
        with pytest.raises(EmptyStructureError):
            tree.remove(10)

    def test_remove_nonexistent_key(self):
        """Test removing nonexistent key raises error."""
        tree = BTree()
        tree.insert(10)
        tree.insert(20)

        with pytest.raises(ValueError, match="not found"):
            tree.remove(30)


class TestBTreeRemoveInternal:
    """Tests for removal from internal nodes."""

    def test_remove_from_internal_with_predecessor(self):
        """Test removing from internal node using predecessor."""
        tree = BTree(t=2)
        # Insert keys to create multi-level structure
        for i in range(1, 11):
            tree.insert(i * 10)

        # Remove key that should be in internal position
        initial_size = len(tree)
        tree.remove(50)
        assert tree.search(50) is False
        assert len(tree) == initial_size - 1
        # Verify sorted order maintained
        result = list(tree)
        expected = [10, 20, 30, 40, 60, 70, 80, 90, 100]
        assert result == expected

    def test_remove_from_internal_with_successor(self):
        """Test removing from internal node using successor."""
        tree = BTree(t=2)
        for i in range(1, 11):
            tree.insert(i * 10)

        # Remove from middle - test successor path
        initial_size = len(tree)
        tree.remove(40)
        assert tree.search(40) is False
        assert len(tree) == initial_size - 1
        result = list(tree)
        expected = [10, 20, 30, 50, 60, 70, 80, 90, 100]
        assert result == expected


class TestBTreeRemoveWithMerge:
    """Tests for removal with node merging."""

    def test_remove_causes_merge(self):
        """Test removal that causes node merge."""
        tree = BTree(t=2)
        keys = [10, 20, 30, 40, 50]
        for key in keys:
            tree.insert(key)

        initial_height = tree.height()
        tree.remove(50)

        assert tree.height() == initial_height
        assert tree.search(50) is False
        assert len(tree) == 4

    def test_remove_multiple_merges(self):
        """Test removal causing multiple merges."""
        tree = BTree(t=2)
        keys = list(range(10, 110, 10))
        for key in keys:
            tree.insert(key)

        # Remove keys that might cause merges
        for key in [100, 90, 80]:
            tree.remove(key)

        assert len(tree) == 7
        for key in [100, 90, 80]:
            assert tree.search(key) is False


class TestBTreeRemoveWithBorrow:
    """Tests for removal with borrowing from siblings."""

    def test_remove_borrow_from_left(self):
        """Test removal with borrowing from left sibling."""
        tree = BTree(t=2)
        keys = [10, 20, 30, 40, 50, 60, 70]
        for key in keys:
            tree.insert(key)

        # Remove to trigger borrow
        tree.remove(70)
        assert tree.search(70) is False

    def test_remove_borrow_from_right(self):
        """Test removal with borrowing from right sibling."""
        tree = BTree(t=2)
        keys = [10, 20, 30, 40, 50, 60, 70]
        for key in keys:
            tree.insert(key)

        # Remove to trigger borrow
        tree.remove(10)
        assert tree.search(10) is False


class TestBTreeRemoveComplex:
    """Tests for complex removal scenarios."""

    def test_remove_all_keys_sequential(self):
        """Test removing all keys sequentially."""
        tree = BTree(t=2)
        keys = [10, 20, 30, 40, 50]
        for key in keys:
            tree.insert(key)

        for key in keys:
            tree.remove(key)
            assert tree.search(key) is False

        assert tree.is_empty()
        assert tree.root is None

    def test_remove_all_keys_reverse(self):
        """Test removing all keys in reverse order."""
        tree = BTree(t=2)
        keys = [10, 20, 30, 40, 50]
        for key in keys:
            tree.insert(key)

        for key in reversed(keys):
            tree.remove(key)

        assert tree.is_empty()

    def test_remove_and_reinsert(self):
        """Test removing and reinserting keys."""
        tree = BTree(t=2)
        keys = [10, 20, 30, 40, 50]

        for key in keys:
            tree.insert(key)

        tree.remove(30)
        assert tree.search(30) is False

        tree.insert(30)
        assert tree.search(30) is True
        assert list(tree) == keys


class TestBTreeTraversal:
    """Tests for tree traversal methods."""

    def test_inorder_traversal_empty(self):
        """Test inorder traversal of empty tree."""
        tree = BTree()
        assert list(tree.inorder_traversal()) == []

    def test_inorder_traversal_sorted(self):
        """Test that inorder traversal returns sorted keys."""
        tree = BTree(t=3)
        keys = [50, 20, 80, 10, 30, 70, 90]
        for key in keys:
            tree.insert(key)

        result = list(tree.inorder_traversal())
        assert result == sorted(keys)

    def test_inorder_after_operations(self):
        """Test inorder traversal after mixed operations."""
        tree = BTree(t=2)
        tree.insert(10)
        tree.insert(20)
        tree.insert(30)
        tree.remove(20)
        tree.insert(25)

        assert list(tree.inorder_traversal()) == [10, 25, 30]

    def test_level_order_traversal(self):
        """Test level order traversal."""
        tree = BTree(t=2)
        keys = [10, 20, 30, 40, 50]
        for key in keys:
            tree.insert(key)

        result = list(tree.level_order_traversal())
        assert len(result) == 5
        assert set(result) == set(keys)

    def test_iterator(self):
        """Test using tree as iterator."""
        tree = BTree(t=3)
        keys = [30, 10, 50, 20, 40]
        for key in keys:
            tree.insert(key)

        result = [key for key in tree]
        assert result == sorted(keys)


class TestBTreeMinMax:
    """Tests for find_min and find_max methods."""

    def test_find_min_empty(self):
        """Test find_min on empty tree."""
        tree = BTree()
        with pytest.raises(EmptyStructureError):
            tree.find_min()

    def test_find_max_empty(self):
        """Test find_max on empty tree."""
        tree = BTree()
        with pytest.raises(EmptyStructureError):
            tree.find_max()

    def test_find_min_single_key(self):
        """Test find_min with single key."""
        tree = BTree()
        tree.insert(42)
        assert tree.find_min() == 42

    def test_find_max_single_key(self):
        """Test find_max with single key."""
        tree = BTree()
        tree.insert(42)
        assert tree.find_max() == 42

    def test_find_min_multiple_keys(self):
        """Test find_min with multiple keys."""
        tree = BTree(t=3)
        keys = [50, 20, 80, 10, 30, 70, 90]
        for key in keys:
            tree.insert(key)

        assert tree.find_min() == 10

    def test_find_max_multiple_keys(self):
        """Test find_max with multiple keys."""
        tree = BTree(t=3)
        keys = [50, 20, 80, 10, 30, 70, 90]
        for key in keys:
            tree.insert(key)

        assert tree.find_max() == 90

    def test_min_max_after_removal(self):
        """Test min/max after removals."""
        tree = BTree(t=2)
        keys = [10, 20, 30, 40, 50]
        for key in keys:
            tree.insert(key)

        tree.remove(10)
        assert tree.find_min() == 20

        tree.remove(50)
        assert tree.find_max() == 40


class TestBTreeHeight:
    """Tests for height method."""

    def test_height_empty(self):
        """Test height of empty tree."""
        tree = BTree()
        assert tree.height() == -1

    def test_height_single_node(self):
        """Test height with single node."""
        tree = BTree()
        tree.insert(10)
        assert tree.height() == 0

    def test_height_after_split(self):
        """Test height increases after split."""
        tree = BTree(t=2)

        # Before split
        tree.insert(10)
        tree.insert(20)
        tree.insert(30)
        height_before = tree.height()

        # After split
        tree.insert(40)
        height_after = tree.height()

        assert height_after >= height_before

    def test_height_logarithmic(self):
        """Test that height stays logarithmic."""
        tree = BTree(t=3)

        # Insert many keys
        for i in range(1, 51):
            tree.insert(i)

        # Height should be much less than n
        assert tree.height() <= 5


class TestBTreeClear:
    """Tests for clear method."""

    def test_clear_empty_tree(self):
        """Test clearing empty tree."""
        tree = BTree()
        tree.clear()
        assert tree.is_empty()

    def test_clear_with_keys(self):
        """Test clearing tree with keys."""
        tree = BTree(t=3)
        keys = [10, 20, 30, 40, 50]
        for key in keys:
            tree.insert(key)

        tree.clear()
        assert tree.is_empty()
        assert len(tree) == 0
        assert tree.root is None

    def test_clear_and_reuse(self):
        """Test clearing and reusing tree."""
        tree = BTree(t=2)

        # First use
        tree.insert(10)
        tree.insert(20)
        tree.clear()

        # Second use
        tree.insert(30)
        tree.insert(40)

        assert len(tree) == 2
        assert list(tree) == [30, 40]


class TestBTreeStringRepresentation:
    """Tests for string representations."""

    def test_repr_empty(self):
        """Test repr of empty tree."""
        tree = BTree(t=3)
        rep = repr(tree)
        assert "t=3" in rep
        assert "size=0" in rep

    def test_repr_with_keys(self):
        """Test repr with keys."""
        tree = BTree(t=2)
        tree.insert(10)
        tree.insert(20)
        rep = repr(tree)
        assert "t=2" in rep
        assert "size=2" in rep

    def test_str_empty(self):
        """Test str of empty tree."""
        tree = BTree()
        assert str(tree) == "BTree: []"

    def test_str_with_keys(self):
        """Test str with keys."""
        tree = BTree()
        tree.insert(10)
        tree.insert(20)
        tree.insert(5)
        s = str(tree)
        assert "5" in s
        assert "10" in s
        assert "20" in s


class TestBTreeProperties:
    """Tests for B-Tree property maintenance."""

    def test_all_leaves_same_depth(self):
        """Test that all leaves are at same depth."""
        tree = BTree(t=2)
        for i in range(1, 16):
            tree.insert(i * 10)

        def get_leaf_depths(node, depth=0):
            if node.is_leaf:
                return [depth]
            depths = []
            for child in node.children:
                depths.extend(get_leaf_depths(child, depth + 1))
            return depths

        if tree.root:
            depths = get_leaf_depths(tree.root)
            assert len(set(depths)) == 1

    def test_keys_in_range(self):
        """Test that nodes have valid number of keys."""
        tree = BTree(t=3)
        for i in range(1, 26):
            tree.insert(i * 10)

        def check_keys(node, is_root=False):
            n_keys = len(node.keys)
            if is_root and n_keys > 0:
                assert n_keys >= 1
            elif not is_root:
                assert n_keys >= tree.t - 1
            assert n_keys <= 2 * tree.t - 1

            if not node.is_leaf:
                for child in node.children:
                    check_keys(child, False)

        if tree.root:
            check_keys(tree.root, True)

    def test_keys_sorted_in_nodes(self):
        """Test that keys are sorted within each node."""
        tree = BTree(t=2)
        keys = [50, 20, 80, 10, 30, 70, 90, 5, 15]
        for key in keys:
            tree.insert(key)

        def check_sorted(node):
            # Check keys are sorted
            for i in range(len(node.keys) - 1):
                assert node.keys[i] < node.keys[i + 1]

            # Check children
            if not node.is_leaf:
                for child in node.children:
                    check_sorted(child)

        if tree.root:
            check_sorted(tree.root)


class TestBTreeEdgeCases:
    """Tests for edge cases and stress scenarios."""

    def test_large_number_of_keys(self):
        """Test with large number of keys."""
        tree = BTree(t=5)
        n = 1000

        for i in range(n):
            tree.insert(i)

        assert len(tree) == n
        assert tree.find_min() == 0
        assert tree.find_max() == n - 1

    def test_different_t_values(self):
        """Test tree works with different t values."""
        for t in [2, 3, 5, 10]:
            tree = BTree(t=t)
            keys = list(range(1, 51))

            for key in keys:
                tree.insert(key)

            assert len(tree) == 50
            assert list(tree) == keys

    def test_string_keys(self):
        """Test tree with string keys."""
        tree = BTree(t=3)
        words = ["apple", "banana", "cherry", "date", "elderberry"]

        for word in words:
            tree.insert(word)

        assert len(tree) == 5
        assert list(tree) == sorted(words)

    def test_mixed_insert_remove(self):
        """Test mixed insert and remove operations."""
        tree = BTree(t=2)

        for i in range(1, 11):
            tree.insert(i * 10)

        tree.remove(50)
        tree.remove(30)
        tree.insert(35)
        tree.insert(45)
        tree.remove(70)

        result = list(tree)
        expected = [10, 20, 35, 40, 45, 60, 80, 90, 100]
        assert result == expected


# Run tests with coverage
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=sds.tree.btree", "--cov-report=term-missing"])
