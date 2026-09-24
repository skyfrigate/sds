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

"""Tests for sds.algorithms.tree_algorithms traversals (#61, #89)."""

import random
import sys
from typing import Any, Callable, Iterator, List, Type

import pytest

from sds.algorithms.tree_algorithms import inorder, level_order, postorder, preorder
from sds.tree import AVLTree, BinaryNode, BinarySearchTree, BinaryTree, RedBlackTree
from sds.tree.interfaces import AbstractBinaryTree

TREES: List[Any] = [
    pytest.param(BinaryTree, id="BinaryTree"),
    pytest.param(BinarySearchTree, id="BinarySearchTree"),
    pytest.param(AVLTree, id="AVLTree"),
    pytest.param(RedBlackTree, id="RedBlackTree"),
]
SEARCH_TREES: List[Any] = TREES[1:]
TRAVERSALS: List[Any] = [
    pytest.param(inorder, id="inorder"),
    pytest.param(preorder, id="preorder"),
    pytest.param(postorder, id="postorder"),
    pytest.param(level_order, id="level_order"),
]

Traversal = Callable[[AbstractBinaryTree], Iterator[Any]]


def _build(cls: Type[AbstractBinaryTree], values: List[int]) -> AbstractBinaryTree:
    tree = cls()
    for value in values:
        tree.insert(value)
    return tree


def _bst_example() -> BinarySearchTree:
    r"""Build the reference BST used by the expected sequences below.

    .. code-block:: text

                10
              /    \
             5      15
            / \    /  \
           3   7  12   20
    """
    tree = BinarySearchTree()
    for value in (10, 5, 15, 3, 7, 12, 20):
        tree.insert(value)
    return tree


def _chain(n: int) -> BinarySearchTree:
    """Return a degenerate BST of height ``n`` (a right-leaning chain).

    Built by hand because ``BinarySearchTree.insert`` is itself recursive
    and cannot build a chain deeper than the recursion limit.
    """
    tree = BinarySearchTree()
    head = BinaryNode(0)
    node = head
    for value in range(1, n):
        child = BinaryNode(value)
        node.right = child
        node = child
    tree._root = head  # test-only shortcut past the recursive insert
    return tree


class TestReferenceSequences:
    """Exact sequences on a known BST shape."""

    def test_inorder(self) -> None:
        """Left, node, right: ascending for a BST."""
        assert list(inorder(_bst_example())) == [3, 5, 7, 10, 12, 15, 20]

    def test_preorder(self) -> None:
        """Node, left, right."""
        assert list(preorder(_bst_example())) == [10, 5, 3, 7, 15, 12, 20]

    def test_postorder(self) -> None:
        """Left, right, node."""
        assert list(postorder(_bst_example())) == [3, 7, 5, 12, 20, 15, 10]

    def test_level_order(self) -> None:
        """Level by level, left to right."""
        assert list(level_order(_bst_example())) == [10, 5, 15, 3, 7, 12, 20]


@pytest.mark.parametrize("traversal", TRAVERSALS)
@pytest.mark.parametrize("tree_cls", TREES)
class TestAllTrees:
    """Invariants holding for every traversal on every binary tree."""

    def test_empty(
        self, tree_cls: Type[AbstractBinaryTree], traversal: Traversal
    ) -> None:
        """An empty tree yields nothing."""
        assert list(traversal(tree_cls())) == []

    def test_single(
        self, tree_cls: Type[AbstractBinaryTree], traversal: Traversal
    ) -> None:
        """A one-node tree yields that node."""
        assert list(traversal(_build(tree_cls, [42]))) == [42]

    @pytest.mark.parametrize("seed", range(10))
    def test_visits_every_item_once(
        self, tree_cls: Type[AbstractBinaryTree], traversal: Traversal, seed: int
    ) -> None:
        """Every stored item appears exactly once, sentinels never."""
        values = random.Random(seed).sample(range(500), 40)
        result = list(traversal(_build(tree_cls, values)))
        assert sorted(result) == sorted(values)
        assert None not in result

    def test_is_lazy(
        self, tree_cls: Type[AbstractBinaryTree], traversal: Traversal
    ) -> None:
        """Traversals are generators: items come one at a time."""
        it = traversal(_build(tree_cls, [2, 1, 3]))
        assert iter(it) is it
        next(it)


@pytest.mark.parametrize("tree_cls", TREES)
class TestRootPosition:
    """Where the root lands in each order."""

    def test_preorder_starts_with_root(
        self, tree_cls: Type[AbstractBinaryTree]
    ) -> None:
        """Preorder emits the root first."""
        tree = _build(tree_cls, [8, 4, 12, 2, 6, 10, 14, 1])
        assert list(preorder(tree))[0] == tree.root.data  # type: ignore[union-attr]

    def test_postorder_ends_with_root(self, tree_cls: Type[AbstractBinaryTree]) -> None:
        """Postorder emits the root last."""
        tree = _build(tree_cls, [8, 4, 12, 2, 6, 10, 14, 1])
        assert list(postorder(tree))[-1] == tree.root.data  # type: ignore[union-attr]

    def test_level_order_starts_with_root(
        self, tree_cls: Type[AbstractBinaryTree]
    ) -> None:
        """Level order emits the root first."""
        tree = _build(tree_cls, [8, 4, 12, 2, 6, 10, 14, 1])
        assert list(level_order(tree))[0] == tree.root.data  # type: ignore[union-attr]


@pytest.mark.parametrize("tree_cls", SEARCH_TREES)
class TestSearchTrees:
    """Inorder on search trees (BST, AVL, Red-Black) is sorted."""

    @pytest.mark.parametrize("seed", range(10))
    def test_inorder_sorted(
        self, tree_cls: Type[AbstractBinaryTree], seed: int
    ) -> None:
        """Inorder yields the items in ascending order."""
        values = random.Random(seed).sample(range(1000), 60)
        assert list(inorder(_build(tree_cls, values))) == sorted(values)

    def test_inorder_after_removals(self, tree_cls: Type[AbstractBinaryTree]) -> None:
        """Traversals follow the tree after removals and rebalancing."""
        values = list(range(30))
        tree = _build(tree_cls, values)
        for value in values[::3]:
            tree.remove(value)
        remaining = [v for v in values if v % 3]
        assert list(inorder(tree)) == remaining
        assert sorted(level_order(tree)) == remaining


class TestRedBlackSentinel:
    """RedBlackTree leaves point to a NIL sentinel that must stay hidden."""

    def test_small_tree_exact(self) -> None:
        """A three-node RB tree yields exactly its three items."""
        tree = _build(RedBlackTree, [5, 3, 8])
        assert list(inorder(tree)) == [3, 5, 8]
        assert list(preorder(tree)) == [5, 3, 8]
        assert list(postorder(tree)) == [3, 8, 5]
        assert list(level_order(tree)) == [5, 3, 8]

    def test_emptied_tree(self) -> None:
        """Removing every item leaves nothing to traverse."""
        tree = _build(RedBlackTree, [5, 3, 8])
        for value in (5, 3, 8):
            tree.remove(value)
        assert list(inorder(tree)) == []
        assert list(level_order(tree)) == []


@pytest.mark.parametrize("traversal", TRAVERSALS)
class TestDepth:
    """Iterative implementations are not bound by the recursion limit."""

    def test_degenerate_chain(self, traversal: Traversal) -> None:
        """A chain three times deeper than the recursion limit is traversed."""
        n = sys.getrecursionlimit() * 3
        result = list(traversal(_chain(n)))
        expected = list(range(n))
        assert result == (expected[::-1] if traversal is postorder else expected)
