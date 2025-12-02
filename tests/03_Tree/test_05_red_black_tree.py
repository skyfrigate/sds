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

"""Tests for Red-Black Tree implementation."""

import pytest

from sds.core.exceptions import EmptyStructureError
from sds.tree import RedBlackNode
from sds.tree.balanced import RedBlackTree


class TestRedBlackNodeCreation:
    """Test Red-Black node creation."""

    def test_create_rb_node(self) -> None:
        """Test creating a Red-Black node."""
        node = RedBlackNode(10)
        assert node.data == 10
        assert node.color == "RED"
        assert node.left is None
        assert node.right is None

    def test_create_black_node(self) -> None:
        """Test creating a BLACK node."""
        node = RedBlackNode(10, color="BLACK")
        assert node.color == "BLACK"


class TestRedBlackTreeCreation:
    """Test Red-Black tree creation."""

    def test_create_empty_rbt(self) -> None:
        """Test creating an empty RBT."""
        rbt = RedBlackTree()
        assert rbt.is_empty()
        assert len(rbt) == 0
        assert rbt.root is None
        assert rbt.height() == -1

    def test_rbt_bool(self) -> None:
        """Test boolean evaluation."""
        rbt = RedBlackTree()
        assert not rbt
        rbt.insert(10)
        assert rbt


class TestRedBlackTreeInsertion:
    """Test Red-Black tree insertion."""

    def test_insert_single_element(self) -> None:
        """Test inserting single element."""
        rbt = RedBlackTree()
        rbt.insert(10)
        assert len(rbt) == 1
        assert rbt.root.data == 10
        assert rbt.root.color == "BLACK"  # Root must be BLACK

    def test_insert_multiple_elements(self) -> None:
        """Test inserting multiple elements."""
        rbt = RedBlackTree()
        for val in [10, 20, 30, 40, 50]:
            rbt.insert(val)
        assert len(rbt) == 5
        # Root must be BLACK
        assert rbt.root.color == "BLACK"

    def test_root_always_black(self) -> None:
        """Test that root is always BLACK."""
        rbt = RedBlackTree()
        for i in range(1, 11):
            rbt.insert(i)
            assert rbt.root.color == "BLACK"

    def test_insert_maintains_bst_property(self) -> None:
        """Test that BST property is maintained."""
        rbt = RedBlackTree()
        values = [50, 25, 75, 10, 30, 60, 80]
        for val in values:
            rbt.insert(val)
        result = list(rbt.inorder_traversal())
        assert result == sorted(values)

    def test_height_stays_logarithmic(self) -> None:
        """Test that height stays O(log n)."""
        rbt = RedBlackTree()
        # Insert sequential values
        for i in range(100):
            rbt.insert(i)
        # RB tree height is at most 2*log2(n+1)
        assert rbt.height() <= 14  # 2*log2(101) ≈ 13.3


class TestRedBlackTreeSearch:
    """Test Red-Black tree search."""

    def test_search_empty_tree(self) -> None:
        """Test searching in empty tree."""
        rbt = RedBlackTree()
        assert not rbt.search(10)

    def test_search_existing_elements(self) -> None:
        """Test searching for existing elements."""
        rbt = RedBlackTree()
        values = [50, 25, 75, 10, 30]
        for val in values:
            rbt.insert(val)
        for val in values:
            assert rbt.search(val)

    def test_search_non_existing(self) -> None:
        """Test searching for non-existing elements."""
        rbt = RedBlackTree()
        for val in [10, 20, 30]:
            rbt.insert(val)
        assert not rbt.search(5)
        assert not rbt.search(100)

    def test_contains_operator(self) -> None:
        """Test __contains__ method."""
        rbt = RedBlackTree()
        for val in [10, 20, 30]:
            rbt.insert(val)
        assert 10 in rbt
        assert 5 not in rbt


class TestRedBlackTreeRemoval:
    """Test Red-Black tree removal."""

    def test_remove_from_empty_tree(self) -> None:
        """Test removing from empty tree."""
        rbt = RedBlackTree()
        with pytest.raises(EmptyStructureError):
            rbt.remove(10)

    def test_remove_non_existing(self) -> None:
        """Test removing non-existing element."""
        rbt = RedBlackTree()
        rbt.insert(10)
        with pytest.raises(ValueError):
            rbt.remove(5)

    def test_remove_single_element(self) -> None:
        """Test removing single element."""
        rbt = RedBlackTree()
        rbt.insert(10)
        rbt.remove(10)
        assert rbt.is_empty()

    def test_remove_maintains_bst_property(self) -> None:
        """Test that BST property is maintained after removal."""
        rbt = RedBlackTree()
        values = [50, 25, 75, 10, 30, 60, 80, 5, 15]
        for val in values:
            rbt.insert(val)

        rbt.remove(25)
        rbt.remove(75)

        result = list(rbt.inorder_traversal())
        assert result == sorted(result)

    def test_remove_root(self) -> None:
        """Test removing root."""
        rbt = RedBlackTree()
        for val in [10, 5, 15, 3, 7]:
            rbt.insert(val)
        rbt.remove(10)
        assert not rbt.search(10)
        assert len(rbt) == 4

    def test_remove_multiple(self) -> None:
        """Test removing multiple elements."""
        rbt = RedBlackTree()
        values = list(range(1, 21))
        for val in values:
            rbt.insert(val)

        for val in [5, 10, 15]:
            rbt.remove(val)

        assert len(rbt) == 17
        result = list(rbt.inorder_traversal())
        assert result == sorted(result)


class TestRedBlackTreeTraversal:
    """Test Red-Black tree traversals."""

    def test_inorder_traversal_empty(self) -> None:
        """Test inorder traversal of empty tree."""
        rbt = RedBlackTree()
        assert list(rbt.inorder_traversal()) == []

    def test_inorder_gives_sorted(self) -> None:
        """Test that inorder gives sorted values."""
        rbt = RedBlackTree()
        import random

        values = list(range(1, 20))
        random.shuffle(values)
        for val in values:
            rbt.insert(val)
        result = list(rbt.inorder_traversal())
        assert result == sorted(values)

    def test_preorder_traversal(self) -> None:
        """Test preorder traversal."""
        rbt = RedBlackTree()
        for val in [10, 5, 15]:
            rbt.insert(val)
        result = list(rbt.preorder_traversal())
        assert len(result) == 3

    def test_postorder_traversal(self) -> None:
        """Test postorder traversal."""
        rbt = RedBlackTree()
        for val in [10, 5, 15]:
            rbt.insert(val)
        result = list(rbt.postorder_traversal())
        assert len(result) == 3

    def test_level_order_traversal(self) -> None:
        """Test level-order traversal."""
        rbt = RedBlackTree()
        for val in [10, 5, 15, 3, 7]:
            rbt.insert(val)
        result = list(rbt.level_order_traversal())
        assert len(result) == 5

    def test_iter_uses_inorder(self) -> None:
        """Test that __iter__ uses inorder."""
        rbt = RedBlackTree()
        values = [50, 25, 75, 10, 30]
        for val in values:
            rbt.insert(val)
        assert list(rbt) == sorted(values)


class TestRedBlackTreeClear:
    """Test Red-Black tree clear."""

    def test_clear_empty_tree(self) -> None:
        """Test clearing empty tree."""
        rbt = RedBlackTree()
        rbt.clear()
        assert rbt.is_empty()

    def test_clear_non_empty(self) -> None:
        """Test clearing non-empty tree."""
        rbt = RedBlackTree()
        for val in [10, 5, 15]:
            rbt.insert(val)
        rbt.clear()
        assert rbt.is_empty()
        assert len(rbt) == 0

    def test_reuse_after_clear(self) -> None:
        """Test tree is usable after clear."""
        rbt = RedBlackTree()
        for val in [10, 5, 15]:
            rbt.insert(val)
        rbt.clear()
        rbt.insert(20)
        assert len(rbt) == 1


class TestRedBlackTreeStringRepresentation:
    """Test string representations."""

    def test_repr_empty(self) -> None:
        """Test repr of empty tree."""
        rbt = RedBlackTree()
        assert repr(rbt) == "RedBlackTree(size=0)"

    def test_repr_non_empty(self) -> None:
        """Test repr of non-empty tree."""
        rbt = RedBlackTree()
        rbt.insert(10)
        rbt.insert(5)
        assert repr(rbt) == "RedBlackTree(size=2)"

    def test_str_empty(self) -> None:
        """Test str of empty tree."""
        rbt = RedBlackTree()
        assert str(rbt) == "RedBlackTree: []"

    def test_str_non_empty(self) -> None:
        """Test str of non-empty tree."""
        rbt = RedBlackTree()
        for val in [30, 10, 20]:
            rbt.insert(val)
        assert str(rbt) == "RedBlackTree: [10, 20, 30]"


class TestRedBlackTreeProperties:
    """Test Red-Black tree properties."""

    def verify_rb_properties(self, rbt: RedBlackTree) -> bool:
        """Verify all RB properties.

        1. Every node is RED or BLACK
        2. Root is BLACK
        3. All leaves (NIL) are BLACK
        4. RED nodes have BLACK children
        5. All paths have same number of BLACK nodes
        """

        def check_node(node, black_count, path_black_counts):
            if node == rbt._NIL:
                path_black_counts.append(black_count)
                return True

            # Property 4: RED nodes have BLACK children
            if node.color == "RED":
                if node.left.color != "BLACK" or node.right.color != "BLACK":
                    return False

            # Increment black count if node is BLACK
            if node.color == "BLACK":
                black_count += 1

            return check_node(node.left, black_count, path_black_counts) and check_node(
                node.right, black_count, path_black_counts
            )

        if rbt.is_empty():
            return True

        # Property 2: Root is BLACK
        if rbt._root.color != "BLACK":
            return False

        # Property 5: Check all paths have same BLACK count
        path_black_counts = []
        if not check_node(rbt._root, 0, path_black_counts):
            return False

        # All paths should have same black count
        return len(set(path_black_counts)) == 1

    def test_properties_after_insertions(self) -> None:
        """Test RB properties after insertions."""
        rbt = RedBlackTree()
        for i in range(1, 21):
            rbt.insert(i)
        assert self.verify_rb_properties(rbt)

    def test_properties_after_removals(self) -> None:
        """Test RB properties after removals."""
        rbt = RedBlackTree()
        for i in range(1, 21):
            rbt.insert(i)

        for i in [5, 10, 15]:
            rbt.remove(i)

        assert self.verify_rb_properties(rbt)

    def test_properties_with_random_operations(self) -> None:
        """Test RB properties with random operations."""
        rbt = RedBlackTree()
        import random

        values = list(range(1, 51))
        random.shuffle(values)

        for val in values[:30]:
            rbt.insert(val)

        for val in values[:10]:
            rbt.remove(val)

        assert self.verify_rb_properties(rbt)


class TestRedBlackTreeEdgeCases:
    """Test edge cases."""

    def test_duplicate_insertions(self) -> None:
        """Test inserting duplicates."""
        rbt = RedBlackTree()
        rbt.insert(10)
        rbt.insert(10)
        rbt.insert(10)
        assert len(rbt) == 3

    def test_single_node_operations(self) -> None:
        """Test operations on single node."""
        rbt = RedBlackTree()
        rbt.insert(42)
        assert rbt.height() == 0
        assert list(rbt) == [42]
        rbt.remove(42)
        assert rbt.is_empty()

    def test_string_values(self) -> None:
        """Test RBT with strings."""
        rbt = RedBlackTree()
        words = ["dog", "cat", "elephant", "ant"]
        for word in words:
            rbt.insert(word)
        result = list(rbt)
        assert result == sorted(words)

    def test_negative_numbers(self) -> None:
        """Test RBT with negative numbers."""
        rbt = RedBlackTree()
        values = [0, -5, 5, -3, 3]
        for val in values:
            rbt.insert(val)
        result = list(rbt)
        assert result == sorted(values)


class TestRedBlackTreePerformance:
    """Test performance characteristics."""

    def test_height_logarithmic(self) -> None:
        """Test that height is O(log n)."""
        rbt = RedBlackTree()
        n = 1000
        for i in range(n):
            rbt.insert(i)
        # RB height <= 2*log2(n+1)
        import math

        max_height = int(2 * math.log2(n + 1))
        assert rbt.height() <= max_height

    def test_sequential_insertions(self) -> None:
        """Test performance with sequential insertions."""
        rbt = RedBlackTree()
        for i in range(500):
            rbt.insert(i)
        # Should maintain balance
        assert rbt.search(250)
        assert rbt.height() <= 20


class TestRedBlackVsAVLComparison:
    """Compare Red-Black with AVL characteristics."""

    def test_both_maintain_balance(self) -> None:
        """Test that both maintain balance."""
        from sds.tree.balanced import AVLTree

        rbt = RedBlackTree()
        avl = AVLTree()

        for i in range(1, 51):
            rbt.insert(i)
            avl.insert(i)

        # Both should have logarithmic height
        assert rbt.height() <= 12
        assert avl.height() <= 6  # AVL is more strictly balanced

    def test_both_give_sorted_inorder(self) -> None:
        """Test both give sorted inorder."""
        from sds.tree.balanced import AVLTree

        rbt = RedBlackTree()
        avl = AVLTree()

        import random

        values = list(range(1, 21))
        random.shuffle(values)

        for val in values:
            rbt.insert(val)
            avl.insert(val)

        assert list(rbt) == list(avl) == sorted(values)
