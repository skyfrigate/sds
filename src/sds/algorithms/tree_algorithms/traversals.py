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

"""Depth-first and breadth-first traversals of binary trees.

A traversal lists every node of a tree exactly once. The three depth-first
orders differ only in *when* a node is emitted relative to its subtrees:

==============  ======================  ====================================
Order           Sequence                Typical use
==============  ======================  ====================================
``preorder``    node, left, right       copying a tree, prefix expressions
``inorder``     left, node, right       sorted output of a search tree
``postorder``   left, right, node       freeing a tree, postfix expressions
``level_order`` level by level (BFS)    printing by depth, shortest root path
==============  ======================  ====================================

All four are generators: nodes are produced lazily, one at a time. The
depth-first traversals use an explicit stack instead of recursion, so a
degenerate tree (a BST fed with sorted input, of height ``n``) never hits
Python's recursion limit.

Every function yields the ``data`` stored in each node, in the order of the
traversal. The tree must not be modified while a traversal is in progress.
"""

from __future__ import annotations

from collections import deque
from typing import TYPE_CHECKING, Any, Deque, Iterator, List, Optional

if TYPE_CHECKING:  # pragma: no cover
    from ...tree.interfaces import AbstractBinaryTree
    from ...tree.node import BinaryNode

__all__ = ["inorder", "preorder", "postorder", "level_order"]


def inorder(tree: AbstractBinaryTree) -> Iterator[Any]:
    """Yield the items of a binary tree in inorder (left, node, right).

    On a binary search tree, inorder visits the items in ascending order.

    Parameters
    ----------
    tree : AbstractBinaryTree
        The tree to traverse.

    Yields
    ------
    Any
        The data of each node, in inorder.

    Examples
    --------
    >>> from sds.tree import BinarySearchTree
    >>> bst = BinarySearchTree()
    >>> for value in (10, 5, 15, 3, 7):
    ...     bst.insert(value)
    >>> list(inorder(bst))
    [3, 5, 7, 10, 15]

    Notes
    -----
    Time complexity: O(n). Space complexity: O(h), with h the height of
    the tree (the stack holds the path from the root to the current node).

    The stack stores the ancestors whose left subtree is being visited:

    .. code-block:: text

        node <- root
        while stack or node:
            while node: push node; node <- left(node)
            node <- pop(); emit node; node <- right(node)
    """
    stack: List[BinaryNode] = []
    node: Optional[BinaryNode] = tree.root
    while stack or node is not None:
        while node is not None:
            stack.append(node)
            node = tree.children(node)[0]
        node = stack.pop()
        yield node.data
        node = tree.children(node)[1]


def preorder(tree: AbstractBinaryTree) -> Iterator[Any]:
    """Yield the items of a binary tree in preorder (node, left, right).

    Parameters
    ----------
    tree : AbstractBinaryTree
        The tree to traverse.

    Yields
    ------
    Any
        The data of each node, in preorder.

    Examples
    --------
    >>> from sds.tree import BinarySearchTree
    >>> bst = BinarySearchTree()
    >>> for value in (10, 5, 15, 3, 7):
    ...     bst.insert(value)
    >>> list(preorder(bst))
    [10, 5, 3, 7, 15]

    Notes
    -----
    Time complexity: O(n). Space complexity: O(h).

    The right child is pushed before the left one so that the left
    subtree, popped first, is visited first.
    """
    root = tree.root
    if root is None:
        return
    stack: List[BinaryNode] = [root]
    while stack:
        node = stack.pop()
        yield node.data
        left, right = tree.children(node)
        if right is not None:
            stack.append(right)
        if left is not None:
            stack.append(left)


def postorder(tree: AbstractBinaryTree) -> Iterator[Any]:
    """Yield the items of a binary tree in postorder (left, right, node).

    Parameters
    ----------
    tree : AbstractBinaryTree
        The tree to traverse.

    Yields
    ------
    Any
        The data of each node, in postorder.

    Examples
    --------
    >>> from sds.tree import BinarySearchTree
    >>> bst = BinarySearchTree()
    >>> for value in (10, 5, 15, 3, 7):
    ...     bst.insert(value)
    >>> list(postorder(bst))
    [3, 7, 5, 15, 10]

    Notes
    -----
    Time complexity: O(n). Space complexity: O(h).

    A node is emitted only once its right subtree is done, which the loop
    detects by remembering the last node emitted: if it is the right child
    of the node on top of the stack (or there is no right child), that
    node's turn has come.
    """
    stack: List[BinaryNode] = []
    node: Optional[BinaryNode] = tree.root
    last: Optional[BinaryNode] = None
    while stack or node is not None:
        if node is not None:
            stack.append(node)
            node = tree.children(node)[0]
            continue
        top = stack[-1]
        right = tree.children(top)[1]
        if right is not None and right is not last:
            node = right
        else:
            yield top.data
            last = stack.pop()


def level_order(tree: AbstractBinaryTree) -> Iterator[Any]:
    """Yield the items of a binary tree level by level (breadth-first).

    Nodes of depth ``d`` all come before nodes of depth ``d + 1``; within a
    level, nodes appear from left to right.

    Parameters
    ----------
    tree : AbstractBinaryTree
        The tree to traverse.

    Yields
    ------
    Any
        The data of each node, level by level.

    Examples
    --------
    >>> from sds.tree import BinarySearchTree
    >>> bst = BinarySearchTree()
    >>> for value in (10, 5, 15, 3, 7):
    ...     bst.insert(value)
    >>> list(level_order(bst))
    [10, 5, 15, 3, 7]

    Notes
    -----
    Time complexity: O(n). Space complexity: O(w), with w the largest
    number of nodes on one level (up to about n/2 for a complete tree).
    """
    root = tree.root
    if root is None:
        return
    queue: Deque[BinaryNode] = deque([root])
    while queue:
        node = queue.popleft()
        yield node.data
        for child in tree.children(node):
            if child is not None:
                queue.append(child)
