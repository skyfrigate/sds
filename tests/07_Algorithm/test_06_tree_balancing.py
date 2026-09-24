# Copyright 2024-2026, skyfrigate, biface
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

"""Tests for sds.algorithms.tree_algorithms balancing (#61, #89)."""

import math
import random
from typing import Any, List

import pytest

from sds.algorithms.tree_algorithms import (
    inorder,
    is_balanced,
    level_order,
    rebalance,
)
from sds.tree import AVLTree, BinaryNode, BinarySearchTree, BinaryTree, RedBlackTree


def _bst(values: List[int]) -> BinarySearchTree:
    tree = BinarySearchTree()
    for value in values:
        tree.insert(value)
    return tree


def _min_height(n: int) -> int:
    return -1 if n == 0 else math.floor(math.log2(n))


class TestIsBalanced:
    """The AVL balance criterion on any binary tree."""

    def test_empty(self) -> None:
        """An empty tree is balanced."""
        assert is_balanced(BinarySearchTree())

    def test_single(self) -> None:
        """A single node is balanced."""
        assert is_balanced(_bst([1]))

    def test_chain_of_three(self) -> None:
        """A three-node chain is not balanced (heights 1 vs -1 at root)."""
        assert not is_balanced(_bst([1, 2, 3]))

    def test_two_nodes(self) -> None:
        """Two nodes are balanced (heights 0 vs -1)."""
        assert is_balanced(_bst([1, 2]))

    def test_imbalance_below_root(self) -> None:
        """Imbalance deep in the tree is detected, not only at the root."""
        #        8
        #      /   \
        #     4     12
        #    /     /  \
        #   2     10   14
        #  /
        # 1
        tree = _bst([8, 4, 12, 2, 10, 14, 1])
        assert not is_balanced(tree)

    def test_perfect_tree(self) -> None:
        """A perfect tree is balanced."""
        assert is_balanced(_bst([4, 2, 6, 1, 3, 5, 7]))

    @pytest.mark.parametrize("seed", range(10))
    def test_avl_always_balanced(self, seed: int) -> None:
        """Every AVL tree satisfies the criterion."""
        tree = AVLTree()
        for value in random.Random(seed).sample(range(1000), 200):
            tree.insert(value)
        assert is_balanced(tree)

    def test_red_black_sentinels_ignored(self) -> None:
        """NIL sentinels do not count as nodes."""
        tree = RedBlackTree()
        for value in (2, 1, 3):
            tree.insert(value)
        assert is_balanced(tree)

    def test_complete_binary_tree(self) -> None:
        """A level-order BinaryTree is complete, hence balanced."""
        tree = BinaryTree()
        for value in range(20):
            tree.insert(value)
        assert is_balanced(tree)

    def test_deep_chain(self) -> None:
        """A chain deeper than the recursion limit is handled iteratively."""
        tree = BinarySearchTree()
        head = node = BinaryNode(0)
        for value in range(1, 5000):
            child = BinaryNode(value)
            node.right = child
            node = child
        tree._root = head  # past the recursive insert, test only
        assert not is_balanced(tree)


class TestRebalance:
    """In-place rebuild of a binary search tree."""

    def test_sorted_input_chain(self) -> None:
        """A chain from sorted input becomes a perfect tree."""
        tree = _bst(list(range(1, 8)))
        assert tree.height() == 6
        rebalance(tree)
        assert tree.height() == 2
        assert list(level_order(tree)) == [4, 2, 6, 1, 3, 5, 7]

    @pytest.mark.parametrize("n", [0, 1, 2, 3, 4, 7, 8, 15, 16, 100, 511, 512])
    def test_minimum_height(self, n: int) -> None:
        """After rebalancing, height is floor(log2 n) for distinct keys."""
        tree = _bst(list(range(n)))
        rebalance(tree)
        assert tree.height() == _min_height(n)
        assert is_balanced(tree)

    @pytest.mark.parametrize("seed", range(10))
    def test_items_preserved(self, seed: int) -> None:
        """Same items, same order, same size."""
        values = random.Random(seed).sample(range(10_000), 300)
        tree = _bst(values)
        rebalance(tree)
        assert list(inorder(tree)) == sorted(values)
        assert len(tree) == len(values)

    def test_same_object(self) -> None:
        """The tree is rebuilt in place; the object is unchanged."""
        tree = _bst([3, 2, 1])
        alias = tree
        assert rebalance(tree) is None
        assert alias is tree
        assert alias.search(2)

    def test_still_a_working_bst(self) -> None:
        """Insert, search and remove keep working afterwards."""
        tree = _bst(list(range(10)))
        rebalance(tree)
        tree.insert(42)
        tree.remove(0)
        assert tree.search(42)
        assert not tree.search(0)
        assert list(inorder(tree)) == list(range(1, 10)) + [42]

    def test_idempotent(self) -> None:
        """Rebalancing a balanced tree keeps it balanced and unchanged."""
        tree = _bst(list(range(15)))
        rebalance(tree)
        shape = list(level_order(tree))
        rebalance(tree)
        assert list(level_order(tree)) == shape

    def test_duplicates_kept(self) -> None:
        """Duplicate keys are all kept, in order."""
        tree = _bst([2, 1, 2, 3, 2])
        rebalance(tree)
        assert list(inorder(tree)) == [1, 2, 2, 2, 3]

    def test_empty(self) -> None:
        """An empty tree stays empty."""
        tree = BinarySearchTree()
        rebalance(tree)
        assert tree.is_empty()

    @pytest.mark.parametrize(
        "bad",
        [AVLTree(), RedBlackTree(), BinaryTree(), [1, 2, 3], None],
        ids=["AVLTree", "RedBlackTree", "BinaryTree", "list", "None"],
    )
    def test_rejects_other_types(self, bad: Any) -> None:
        """Only plain BinarySearchTree is accepted (#86)."""
        with pytest.raises(TypeError, match="BinarySearchTree"):
            rebalance(bad)
