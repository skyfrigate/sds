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

"""Tests for AbstractBinaryTree.children() (#89)."""

from typing import Any, List, Type

import pytest

from sds.tree import AVLTree, BinarySearchTree, BinaryTree, RedBlackTree
from sds.tree.interfaces import AbstractBinaryTree

TREES: List[Any] = [
    pytest.param(BinaryTree, id="BinaryTree"),
    pytest.param(BinarySearchTree, id="BinarySearchTree"),
    pytest.param(AVLTree, id="AVLTree"),
    pytest.param(RedBlackTree, id="RedBlackTree"),
]


@pytest.mark.parametrize("tree_cls", TREES)
class TestChildren:
    """children() reports real children, None where absent."""

    def test_single_node_has_none(self, tree_cls: Type[AbstractBinaryTree]) -> None:
        """A lone root has no children."""
        tree = tree_cls()
        tree.insert(1)
        assert tree.children(tree.root) == (None, None)  # type: ignore[arg-type]

    def test_matches_node_links_without_sentinel(
        self, tree_cls: Type[AbstractBinaryTree]
    ) -> None:
        """Walking with children() reaches every item, never a placeholder."""
        tree = tree_cls()
        values = [8, 4, 12, 2, 6, 10, 14]
        for value in values:
            tree.insert(value)
        seen = []
        stack = [tree.root]
        while stack:
            node = stack.pop()
            assert node is not None
            seen.append(node.data)
            stack.extend(c for c in tree.children(node) if c is not None)
        assert sorted(seen) == sorted(values)

    def test_returns_tuple_of_two(self, tree_cls: Type[AbstractBinaryTree]) -> None:
        """The result always has exactly two entries."""
        tree = tree_cls()
        tree.insert(1)
        tree.insert(2)
        result = tree.children(tree.root)  # type: ignore[arg-type]
        assert isinstance(result, tuple)
        assert len(result) == 2


class TestRedBlackChildren:
    """The Red-Black override hides the NIL sentinel."""

    def test_leaf_children_are_none(self) -> None:
        """A leaf's NIL links are reported as None."""
        tree = RedBlackTree()
        for value in (5, 3, 8):
            tree.insert(value)
        left, right = tree.children(tree.root)  # type: ignore[arg-type]
        assert left is not None and right is not None
        assert tree.children(left) == (None, None)
        assert tree.children(right) == (None, None)

    def test_raw_links_are_sentinels(self) -> None:
        """Sanity check: the raw node links really are sentinels."""
        tree = RedBlackTree()
        tree.insert(5)
        root = tree.root
        assert root is not None
        assert root.left is not None and root.left.data is None
