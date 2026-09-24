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

"""Algorithms on binary trees.

Traversals visit every node of an :class:`~sds.tree.interfaces.AbstractBinaryTree`
in one of the four classic orders. They walk the tree only through
``tree.root`` and ``tree.children(node)``, so they work unchanged on every
binary tree of :mod:`sds.tree`, including those that represent absent
children with a sentinel node (#89).

:func:`is_balanced` checks the AVL balance criterion on any binary tree;
:func:`rebalance` rebuilds a plain binary search tree into a balanced
shape, in place.

Examples
--------
>>> from sds.tree import BinarySearchTree
>>> from sds.algorithms.tree_algorithms import inorder, level_order
>>> bst = BinarySearchTree()
>>> for value in (10, 5, 15, 3):
...     bst.insert(value)
>>> list(inorder(bst))
[3, 5, 10, 15]
>>> list(level_order(bst))
[10, 5, 15, 3]
"""

from .balancing import is_balanced, rebalance
from .traversals import inorder, level_order, postorder, preorder

__all__ = [
    "inorder",
    "preorder",
    "postorder",
    "level_order",
    "is_balanced",
    "rebalance",
]
