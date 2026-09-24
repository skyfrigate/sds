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

"""Deprecation of AbstractBinaryTree traversal methods (#89, #90)."""

import warnings
from typing import Any, List, Type

import pytest

from sds.algorithms import tree_algorithms
from sds.tree import AVLTree, BinarySearchTree, BinaryTree, RedBlackTree
from sds.tree.interfaces import AbstractBinaryTree

TREES: List[Any] = [
    pytest.param(BinaryTree, id="BinaryTree"),
    pytest.param(BinarySearchTree, id="BinarySearchTree"),
    pytest.param(AVLTree, id="AVLTree"),
    pytest.param(RedBlackTree, id="RedBlackTree"),
]
METHODS: List[Any] = [
    pytest.param("inorder_traversal", "inorder", id="inorder"),
    pytest.param("preorder_traversal", "preorder", id="preorder"),
    pytest.param("postorder_traversal", "postorder", id="postorder"),
    pytest.param("level_order_traversal", "level_order", id="level_order"),
]


def _tree(cls: Type[AbstractBinaryTree]) -> AbstractBinaryTree:
    tree = cls()
    for value in (8, 4, 12, 2, 6, 10, 14):
        tree.insert(value)
    return tree


@pytest.mark.parametrize(("method", "replacement"), METHODS)
@pytest.mark.parametrize("tree_cls", TREES)
class TestDeprecatedTraversals:
    """Each deprecated method warns and still returns the right items."""

    def test_warns_and_names_replacement(
        self, tree_cls: Type[AbstractBinaryTree], method: str, replacement: str
    ) -> None:
        """The warning names the tree_algorithms replacement."""
        tree = _tree(tree_cls)
        expected = rf"sds\.algorithms\.tree_algorithms\.{replacement}\(tree\)"
        with pytest.warns(DeprecationWarning, match=expected):
            getattr(tree, method)()

    def test_warns_at_call_not_at_iteration(
        self, tree_cls: Type[AbstractBinaryTree], method: str, replacement: str
    ) -> None:
        """The warning fires when the method is called, before iterating."""
        tree = _tree(tree_cls)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            getattr(tree, method)()  # iterator deliberately not consumed
        assert any(issubclass(w.category, DeprecationWarning) for w in caught)

    def test_points_at_caller(
        self, tree_cls: Type[AbstractBinaryTree], method: str, replacement: str
    ) -> None:
        """The warning is attributed to the calling code (stacklevel)."""
        tree = _tree(tree_cls)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            getattr(tree, method)()
        assert caught[0].filename == __file__

    def test_same_items_as_replacement(
        self, tree_cls: Type[AbstractBinaryTree], method: str, replacement: str
    ) -> None:
        """The deprecated method delegates to the algorithm."""
        tree = _tree(tree_cls)
        with pytest.warns(DeprecationWarning):
            old = list(getattr(tree, method)())
        assert old == list(getattr(tree_algorithms, replacement)(tree))


@pytest.mark.parametrize("tree_cls", TREES)
class TestNoWarningOnProtocols:
    """Iteration and string conversion do not go through deprecated API."""

    def test_iter(self, tree_cls: Type[AbstractBinaryTree]) -> None:
        """Iterating a tree emits no warning."""
        tree = _tree(tree_cls)
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            list(tree)

    def test_str_and_repr(self, tree_cls: Type[AbstractBinaryTree]) -> None:
        """str() and repr() emit no warning."""
        tree = _tree(tree_cls)
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            str(tree)
            repr(tree)

    def test_iter_is_inorder(self, tree_cls: Type[AbstractBinaryTree]) -> None:
        """Iteration order is still inorder."""
        tree = _tree(tree_cls)
        assert list(tree) == list(tree_algorithms.inorder(tree))
