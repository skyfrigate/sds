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

"""Balance check and external rebalancing of binary search trees.

A binary tree is **height-balanced** (the AVL criterion) when, at every
node, the heights of the left and right subtrees differ by at most one.
Such a tree of ``n`` nodes has height ``O(log n)``, which keeps search,
insertion and removal logarithmic.

A plain :class:`~sds.tree.BinarySearchTree` does not maintain that
property: inserting already sorted values produces a chain of height
``n - 1``. Self-balancing trees (``AVLTree``, ``RedBlackTree``) repair their
shape on every update with rotations, which is an invariant of the
structure and stays inside those classes. Rebalancing an arbitrary BST
after the fact is an operation performed *on* the tree from outside, and
therefore an algorithm (#89).

Rebalancing strategy
--------------------
:func:`rebalance` rebuilds the tree from its sorted content: the median
becomes the root, the medians of each half become its children, and so on.

.. code-block:: text

    items <- inorder(T)                     # sorted
    clear T
    queue <- [(0, n - 1)]
    while queue not empty:                  # breadth-first over ranges
        (lo, hi) <- dequeue
        if lo > hi: continue
        mid <- (lo + hi) // 2
        insert items[mid] into T
        enqueue (lo, mid - 1), (mid + 1, hi)

Inserting the medians range by range, in breadth-first order, lays each
level down before the next, so every insertion follows an already short
path and the result has the minimum possible height,
``floor(log2 n)``, for distinct keys.
"""

from __future__ import annotations

from collections import deque
from typing import TYPE_CHECKING, Any, Deque, Dict, List, Tuple

from ...tree.binary import BinarySearchTree
from .traversals import inorder

if TYPE_CHECKING:  # pragma: no cover
    from ...tree.interfaces import AbstractBinaryTree
    from ...tree.node import BinaryNode

__all__ = ["is_balanced", "rebalance"]


def is_balanced(tree: AbstractBinaryTree) -> bool:
    """Return True if the tree is height-balanced (AVL criterion).

    Parameters
    ----------
    tree : AbstractBinaryTree
        Any binary tree.

    Returns
    -------
    bool
        True if, at every node, the heights of the two subtrees differ by
        at most one. An empty tree is balanced.

    Examples
    --------
    >>> from sds.tree import BinarySearchTree
    >>> bst = BinarySearchTree()
    >>> for value in (1, 2, 3):
    ...     bst.insert(value)
    >>> is_balanced(bst)
    False
    >>> rebalance(bst)
    >>> is_balanced(bst)
    True

    Notes
    -----
    Time complexity: O(n). Space complexity: O(h).

    Heights are computed bottom-up in a single iterative postorder pass,
    so a degenerate tree of any depth is handled. An ``AVLTree`` always
    passes this check; a ``RedBlackTree`` need not, since its own balance
    rule is looser (the longest path is at most twice the shortest).
    """
    heights: Dict[int, int] = {}  # id(node) -> height; -1 for an absent child

    def height_of(node: BinaryNode | None) -> int:
        return -1 if node is None else heights[id(node)]

    stack: List[Tuple[BinaryNode, bool]] = []
    if tree.root is not None:
        stack.append((tree.root, False))
    while stack:
        node, children_done = stack.pop()
        left, right = tree.children(node)
        if not children_done:
            stack.append((node, True))
            for child in (left, right):
                if child is not None:
                    stack.append((child, False))
            continue
        left_h, right_h = height_of(left), height_of(right)
        if abs(left_h - right_h) > 1:
            return False
        heights[id(node)] = 1 + max(left_h, right_h)
    return True


def rebalance(tree: BinarySearchTree) -> None:
    """Rebuild a binary search tree into a height-balanced shape, in place.

    The tree keeps the same items and the same identity: only its shape
    changes. Afterwards its height is ``floor(log2 n)`` when the keys are
    distinct.

    Parameters
    ----------
    tree : BinarySearchTree
        The tree to rebalance. It is modified in place.

    Raises
    ------
    TypeError
        If ``tree`` is not a ``BinarySearchTree``. ``AVLTree`` and
        ``RedBlackTree`` are rejected too: they keep themselves balanced.

    Examples
    --------
    >>> from sds.tree import BinarySearchTree
    >>> bst = BinarySearchTree()
    >>> for value in range(1, 8):          # sorted input: a chain
    ...     bst.insert(value)
    >>> bst.height()
    6
    >>> rebalance(bst)
    >>> bst.height()
    2
    >>> list(bst)
    [1, 2, 3, 4, 5, 6, 7]

    Notes
    -----
    Time complexity: O(n log n): one inorder pass, then ``n`` insertions
    into a tree whose height never exceeds ``log2 n``.
    Space complexity: O(n) for the sorted copy of the items.

    The parameter is narrowed to the concrete ``BinarySearchTree`` (#86):
    rebalancing needs the search-tree ordering of ``insert()``, which the
    ``AbstractBinaryTree`` interface does not promise (``BinaryTree``
    inserts level by level).

    The rebuild only uses the tree's public interface (``clear()`` and
    ``insert()``). An O(n), O(1)-space alternative exists, the
    Day-Stout-Warren algorithm, but it rewires node links directly, which
    would mean reaching into the structure's internals.

    ``BinarySearchTree`` sends duplicates to the right subtree, so a tree
    with many equal keys cannot reach minimum height whatever its shape;
    the items are still all kept, in order.
    """
    if not isinstance(tree, BinarySearchTree):
        raise TypeError(
            f"rebalance expects a BinarySearchTree, got {type(tree).__name__}"
        )
    items: List[Any] = list(inorder(tree))
    tree.clear()
    ranges: Deque[Tuple[int, int]] = deque([(0, len(items) - 1)])
    while ranges:
        lo, hi = ranges.popleft()
        if lo > hi:
            continue
        mid = (lo + hi) // 2
        tree.insert(items[mid])
        ranges.append((lo, mid - 1))
        ranges.append((mid + 1, hi))
