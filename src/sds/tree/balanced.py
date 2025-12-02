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

"""Balanced tree implementations.

This module provides self-balancing binary search tree implementations
that guarantee O(log n) operations by maintaining balance invariants.

Classes
-------
AVLNode
    Node for AVL tree with height attribute.
AVLTree
    Self-balancing BST using AVL rotations.
RedBlackNode
    Node for Red-Black tree with color attribute.
RedBlackTree
    Self-balancing BST using Red-Black properties.

Examples
--------
Using an AVL Tree:

>>> from sds.tree.balanced import AVLTree
>>> avl = AVLTree()
>>> for val in [10, 20, 30, 40, 50, 25]:
...     avl.insert(val)
>>> avl.height()
2
>>> list(avl)
[10, 20, 25, 30, 40, 50]

Notes
-----
Both AVL and Red-Black trees maintain balance automatically during
insertions and deletions, ensuring O(log n) worst-case performance.

See Also
--------
sds.tree.binary : Basic binary search tree.
"""

from collections import deque
from typing import Any, Iterator, Optional, cast

from ..core.exceptions import EmptyStructureError
from .interfaces import AbstractBinaryTree
from .node import AVLNode, RedBlackNode

__all__ = ["AVLTree", "RedBlackTree"]


class AVLTree(AbstractBinaryTree):
    """AVL Tree - Self-balancing binary search tree.

    An AVL tree is a BST where the heights of the two child subtrees
    of any node differ by at most one. If at any time they differ by
    more than one, rebalancing is done through rotations to restore
    this property.

    Balance factor = height(left subtree) - height(right subtree)
    Valid balance factors: -1, 0, 1

    Attributes
    ----------
    root : sds.tree.AVLNode or None
        The root node of the tree (read-only property).
    size : int
        The number of nodes in the tree (read-only property).

    Examples
    --------
    Create and populate an AVL tree:

    >>> avl = AVLTree()
    >>> for val in [10, 20, 30, 40, 50, 25]:
    ...     avl.insert(val)
    >>> avl.height()
    2
    >>> list(avl)
    [10, 20, 25, 30, 40, 50]

    Tree remains balanced after insertions:

    >>> avl = AVLTree()
    >>> for i in range(1, 8):
    ...     avl.insert(i)
    >>> avl.height()  # Much better than BST height of 6
    2

    Notes
    -----
    Time Complexity (guaranteed):
    - Insert: O(log n)
    - Search: O(log n)
    - Remove: O(log n)
    - All operations: O(log n) worst case

    AVL trees are more rigidly balanced than Red-Black trees,
    leading to faster lookups but slightly slower insertions/deletions.

    See Also
    --------
    BinarySearchTree : Unbalanced BST.
    RedBlackTree : Alternative self-balancing tree.
    """

    def __init__(self) -> None:
        """Initialize an empty AVL tree."""
        super().__init__()
        self._root: Optional[AVLNode] = None

    def height(self) -> int:
        """Return the height of the tree.

        Returns
        -------
        int
            The height of the tree, or -1 if empty.

        Examples
        --------
        >>> avl = AVLTree()
        >>> avl.height()
        -1
        >>> avl.insert(10)
        >>> avl.height()
        0

        Notes
        -----
        Time complexity: O(1) - height is stored in root node.
        """
        return self._root.height if self._root else -1

    def _get_height(self, node: Optional[AVLNode]) -> int:
        """Get height of a node.

        Parameters
        ----------
        node : AVLNode or None
            The node to get height from.

        Returns
        -------
        int
            Height of the node, or -1 if None.
        """
        return node.height if node else -1

    def _update_height(self, node: AVLNode) -> None:
        """Update the height of a node based on its children.

        Parameters
        ----------
        node : AVLNode
            The node to update.
        """
        left_height = self._get_height(cast(Optional[AVLNode], node.left))
        right_height = self._get_height(cast(Optional[AVLNode], node.right))
        node.height = 1 + max(left_height, right_height)

    def _get_balance_factor(self, node: Optional[AVLNode]) -> int:
        """Calculate the balance factor of a node.

        Balance factor = height(left) - height(right)

        Parameters
        ----------
        node : AVLNode or None
            The node to calculate balance for.

        Returns
        -------
        int
            Balance factor. Valid range: [-1, 0, 1] for balanced tree.
        """
        if node is None:
            return 0
        left_height = self._get_height(cast(Optional[AVLNode], node.left))
        right_height = self._get_height(cast(Optional[AVLNode], node.right))
        return left_height - right_height

    def _rotate_right(self, z: AVLNode) -> AVLNode:
        """Perform a right rotation.

        Parameters
        ----------
        z : AVLNode
            The node to rotate around.

        Returns
        -------
        AVLNode
            The new root of the subtree after rotation.

        Notes
        -----
        Right rotation:
            z                y
           / \\              / \\
          y   C    -->     x   z
         / \\                 / \\
        x   B               B   C
        """
        y = cast(AVLNode, z.left)
        # In AVL rotation, left child must exist; use explicit check (no assert for Bandit B101)
        if y is None:
            raise RuntimeError(
                "AVL rotate_right precondition failed: left child is None"
            )
        B = cast(Optional[AVLNode], y.right)

        # Perform rotation
        y.right = z
        z.left = B

        # Update heights
        self._update_height(z)
        self._update_height(y)

        return y

    def _rotate_left(self, z: AVLNode) -> AVLNode:
        """Perform a left rotation.

        Parameters
        ----------
        z : AVLNode
            The node to rotate around.

        Returns
        -------
        AVLNode
            The new root of the subtree after rotation.

        Notes
        -----
        Left rotation:
          z                  y
         / \\                / \\
        A   y      -->     z   C
           / \\            / \\
          B   C          A   B
        """
        y = cast(AVLNode, z.right)
        if y is None:
            raise RuntimeError(
                "AVL rotate_left precondition failed: right child is None"
            )
        B = cast(Optional[AVLNode], y.left)

        # Perform rotation
        y.left = z
        z.right = B

        # Update heights
        self._update_height(z)
        self._update_height(y)

        return y

    def insert(self, item: Any) -> None:
        """Insert an item into the AVL tree with automatic balancing.

        Parameters
        ----------
        item : Any
            The item to insert. Must be comparable.

        Examples
        --------
        >>> avl = AVLTree()
        >>> avl.insert(10)
        >>> avl.insert(20)
        >>> avl.insert(30)  # Triggers left rotation
        >>> list(avl)
        [10, 20, 30]

        Notes
        -----
        Time complexity: O(log n) guaranteed.
        """
        self._root = self._insert_recursive(self._root, item)
        self._size += 1

    def _insert_recursive(self, node: Optional[AVLNode], item: Any) -> AVLNode:
        """Insert recursively with balancing.

        Parameters
        ----------
        node : AVLNode or None
            Current node in recursion.
        item : Any
            Item to insert.

        Returns
        -------
        AVLNode
            The balanced node after insertion.
        """
        # Standard BST insertion
        if node is None:
            return AVLNode(item)

        if item < node.data:
            node.left = self._insert_recursive(cast(Optional[AVLNode], node.left), item)
        else:
            node.right = self._insert_recursive(
                cast(Optional[AVLNode], node.right), item
            )

        # Update height
        self._update_height(node)

        # Get balance factor
        balance = self._get_balance_factor(node)

        # Left-Left Case
        if balance > 1:
            left_child = cast(AVLNode, node.left)
            if left_child is None:
                raise RuntimeError(
                    "AVL insert rebalance precondition failed: left child is None"
                )
            if item < left_child.data:
                return self._rotate_right(node)

        # Right-Right Case
        if balance < -1:
            right_child = cast(AVLNode, node.right)
            if right_child is None:
                raise RuntimeError(
                    "AVL insert rebalance precondition failed: right child is None"
                )
            if item >= right_child.data:
                return self._rotate_left(node)

        # Left-Right Case
        if balance > 1:
            left_child = cast(AVLNode, node.left)
            if left_child is None:
                raise RuntimeError(
                    "AVL insert LR case precondition failed: left child is None"
                )
            if item >= left_child.data:
                node.left = self._rotate_left(left_child)
                return self._rotate_right(node)

        # Right-Left Case
        if balance < -1:
            right_child = cast(AVLNode, node.right)
            if right_child is None:
                raise RuntimeError(
                    "AVL insert RL case precondition failed: right child is None"
                )
            if item < right_child.data:
                node.right = self._rotate_right(right_child)
                return self._rotate_left(node)

        return node

    def remove(self, item: Any) -> Any:
        """Remove an item from the AVL tree with automatic balancing.

        Parameters
        ----------
        item : Any
            The item to remove.

        Returns
        -------
        Any
            The removed item.

        Raises
        ------
        EmptyStructureError
            If the tree is empty.
        ValueError
            If the item is not found.

        Examples
        --------
        >>> avl = AVLTree()
        >>> for val in [10, 20, 30]:
        ...     avl.insert(val)
        >>> avl.remove(10)
        10

        Notes
        -----
        Time complexity: O(log n) guaranteed.
        """
        if self._root is None:
            raise EmptyStructureError("Cannot remove from empty tree")

        if not self.search(item):
            raise ValueError(f"Item {item} not found in tree")

        self._root = self._remove_recursive(self._root, item)
        self._size -= 1
        return item

    def _remove_recursive(
        self, node: Optional[AVLNode], item: Any
    ) -> Optional[AVLNode]:
        """Remove recursively with balancing.

        Parameters
        ----------
        node : AVLNode or None
            Current node in recursion.
        item : Any
            Item to remove.

        Returns
        -------
        AVLNode or None
            The balanced node after removal.
        """
        if node is None:
            return None

        # Standard BST deletion
        if item < node.data:
            node.left = self._remove_recursive(cast(Optional[AVLNode], node.left), item)
        elif item > node.data:
            node.right = self._remove_recursive(
                cast(Optional[AVLNode], node.right), item
            )
        else:
            # Node with only one child or no child
            if node.left is None:
                return cast(Optional[AVLNode], node.right)
            elif node.right is None:
                return cast(Optional[AVLNode], node.left)

            # Node with two children: get inorder successor
            successor = self._find_min_node(cast(AVLNode, node.right))
            node.data = successor.data
            node.right = self._remove_recursive(
                cast(Optional[AVLNode], node.right), successor.data
            )

        # Update height
        self._update_height(node)

        # Get balance factor
        balance = self._get_balance_factor(node)

        # Left-Left Case
        if (
            balance > 1
            and self._get_balance_factor(cast(Optional[AVLNode], node.left)) >= 0
        ):
            return self._rotate_right(node)

        # Left-Right Case
        if (
            balance > 1
            and self._get_balance_factor(cast(Optional[AVLNode], node.left)) < 0
        ):
            node.left = self._rotate_left(cast(AVLNode, node.left))
            return self._rotate_right(node)

        # Right-Right Case
        if (
            balance < -1
            and self._get_balance_factor(cast(Optional[AVLNode], node.right)) <= 0
        ):
            return self._rotate_left(node)

        # Right-Left Case
        if (
            balance < -1
            and self._get_balance_factor(cast(Optional[AVLNode], node.right)) > 0
        ):
            node.right = self._rotate_right(cast(AVLNode, node.right))
            return self._rotate_left(node)

        return node

    def search(self, item: Any) -> bool:
        """Search for an item in the tree.

        Parameters
        ----------
        item : Any
            The item to search for.

        Returns
        -------
        bool
            True if found, False otherwise.

        Examples
        --------
        >>> avl = AVLTree()
        >>> avl.insert(10)
        >>> avl.search(10)
        True

        Notes
        -----
        Time complexity: O(log n) guaranteed.
        """
        return self._search_recursive(self._root, item)

    def _search_recursive(self, node: Optional[AVLNode], item: Any) -> bool:
        """Search recursively using BST property."""
        if node is None:
            return False
        if item == node.data:
            return True
        elif item < node.data:
            return self._search_recursive(cast(Optional[AVLNode], node.left), item)
        else:
            return self._search_recursive(cast(Optional[AVLNode], node.right), item)

    def _find_min_node(self, node: AVLNode) -> AVLNode:
        """Find the node with minimum value in subtree."""
        current = node
        while current.left is not None:
            current = cast(AVLNode, current.left)
        return current

    def clear(self) -> None:
        """Remove all nodes from the tree."""
        self._root = None
        self._size = 0

    def __iter__(self) -> Iterator[Any]:
        """Iterate over tree elements (inorder)."""
        return self.inorder_traversal()

    def __contains__(self, item: Any) -> bool:
        """Check if item is in the tree."""
        return self.search(item)

    def inorder_traversal(self) -> Iterator[Any]:
        """Return inorder traversal iterator."""
        yield from self._inorder_recursive(self._root)

    def _inorder_recursive(self, node: Optional[AVLNode]) -> Iterator[Any]:
        """Inorder traversal helper."""
        if node is not None:
            yield from self._inorder_recursive(node.left)  # type: ignore
            yield node.data
            yield from self._inorder_recursive(node.right)  # type: ignore

    def preorder_traversal(self) -> Iterator[Any]:
        """Return preorder traversal iterator."""
        yield from self._preorder_recursive(self._root)

    def _preorder_recursive(self, node: Optional[AVLNode]) -> Iterator[Any]:
        """Preorder traversal helper."""
        if node is not None:
            yield node.data
            yield from self._preorder_recursive(node.left)  # type: ignore
            yield from self._preorder_recursive(node.right)  # type: ignore

    def postorder_traversal(self) -> Iterator[Any]:
        """Return postorder traversal iterator."""
        yield from self._postorder_recursive(self._root)

    def _postorder_recursive(self, node: Optional[AVLNode]) -> Iterator[Any]:
        """Postorder traversal helper."""
        if node is not None:
            yield from self._postorder_recursive(node.left)  # type: ignore
            yield from self._postorder_recursive(node.right)  # type: ignore
            yield node.data

    def level_order_traversal(self) -> Iterator[Any]:
        """Return level-order traversal iterator."""
        if self._root is None:
            return

        queue: deque[AVLNode] = deque([self._root])
        while queue:
            current = queue.popleft()
            yield current.data
            if current.left:
                queue.append(current.left)  # type: ignore
            if current.right:
                queue.append(current.right)  # type: ignore

    def __repr__(self) -> str:
        """Return string representation."""
        return f"AVLTree(size={self._size})"

    def __str__(self) -> str:
        """Return string showing inorder traversal."""
        if self.is_empty():
            return "AVLTree: []"
        elements = ", ".join(str(item) for item in self.inorder_traversal())
        return f"AVLTree: [{elements}]"


class RedBlackTree(AbstractBinaryTree):
    """Red-Black Tree - Self-balancing binary search tree.

    A Red-Black tree is a BST with one extra bit per node: color (RED or BLACK).
    The tree maintains balance using the following properties:

    1. Every node is either RED or BLACK
    2. The root is always BLACK
    3. All leaves (NIL) are BLACK
    4. RED nodes cannot have RED children (no two RED nodes in a row)
    5. Every path from root to leaf has the same number of BLACK nodes

    These properties ensure the tree remains approximately balanced,
    guaranteeing O(log n) operations.

    Attributes
    ----------
    root : RedBlackNode or None
        The root node of the tree.
    size : int
        The number of nodes in the tree.

    Examples
    --------
    >>> rbt = RedBlackTree()
    >>> for val in [10, 20, 30, 40, 50]:
    ...     rbt.insert(val)
    >>> list(rbt)
    [10, 20, 30, 40, 50]
    >>> rbt.height() <= 10  # O(log n)
    True

    Notes
    -----
    Time Complexity (guaranteed):
    - Insert: O(log n)
    - Search: O(log n)
    - Remove: O(log n)

    Red-Black trees have less strict balancing than AVL trees,
    leading to faster insertions/deletions but slightly slower lookups.

    See Also
    --------
    AVLTree : More strictly balanced alternative.
    BinarySearchTree : Unbalanced BST.
    """

    def __init__(self) -> None:
        """Initialize an empty Red-Black tree."""
        super().__init__()
        # Use NIL sentinel for all leaves
        self._NIL = RedBlackNode(data=None, color="BLACK")
        self._root: Optional[RedBlackNode] = self._NIL

    @property
    def root(self) -> Optional[RedBlackNode]:
        """Get the root node."""
        return self._root if self._root != self._NIL else None

    def height(self) -> int:
        """Return the height of the tree.

        Returns
        -------
        int
            The height of the tree, or -1 if empty.

        Notes
        -----
        Time complexity: O(n)
        """
        return self._height_recursive(self._root)

    def _height_recursive(self, node: Optional[RedBlackNode]) -> int:
        """Calculate height recursively."""
        if node is None or node == self._NIL:
            return -1
        left_h = self._height_recursive(cast(Optional[RedBlackNode], node.left))
        right_h = self._height_recursive(cast(Optional[RedBlackNode], node.right))
        return 1 + max(left_h, right_h)

    def _rotate_left(self, x: RedBlackNode) -> None:
        """Perform a left rotation."""
        y = cast(RedBlackNode, x.right)
        if y == self._NIL:
            return

        x.right = y.left
        if y.left != self._NIL:
            cast(RedBlackNode, y.left)._parent = x

        y._parent = cast(Optional[RedBlackNode], x._parent)
        if x._parent is None:
            self._root = y
        elif x == cast(RedBlackNode, x._parent).left:
            cast(RedBlackNode, x._parent).left = y
        else:
            cast(RedBlackNode, x._parent).right = y

        y.left = x
        x._parent = y

    def _rotate_right(self, y: RedBlackNode) -> None:
        """Perform a right rotation."""
        x = cast(RedBlackNode, y.left)
        if x == self._NIL:
            return

        y.left = x.right
        if x.right != self._NIL:
            cast(RedBlackNode, x.right)._parent = y

        x._parent = cast(Optional[RedBlackNode], y._parent)
        if y._parent is None:
            self._root = x
        elif y == cast(RedBlackNode, y._parent).right:
            cast(RedBlackNode, y._parent).right = x
        else:
            cast(RedBlackNode, y._parent).left = x

        x.right = y
        y._parent = x

    def insert(self, item: Any) -> None:
        """Insert an item maintaining Red-Black properties.

        Parameters
        ----------
        item : Any
            The item to insert.

        Examples
        --------
        >>> rbt = RedBlackTree()
        >>> rbt.insert(10)
        >>> rbt.insert(20)
        >>> len(rbt)
        2

        Notes
        -----
        Time complexity: O(log n) guaranteed.
        """
        node = RedBlackNode(item, color="RED")
        node.left = self._NIL
        node.right = self._NIL

        parent: Optional[RedBlackNode] = None
        current: RedBlackNode = cast(RedBlackNode, self._root)

        # BST insertion
        while current != self._NIL:
            parent = current
            if node.data < current.data:
                current = cast(RedBlackNode, current.left)
            else:
                current = cast(RedBlackNode, current.right)

        node._parent = parent

        if parent is None:
            self._root = node
        elif node.data < parent.data:
            parent.left = node
        else:
            parent.right = node

        self._size += 1
        self._insert_fixup(node)

    def _insert_fixup(self, node: RedBlackNode) -> None:
        """Fix Red-Black properties after insertion."""
        while True:
            parent = cast(Optional[RedBlackNode], node._parent)
            if parent is None or parent.color != "RED":
                break

            grand = cast(RedBlackNode, parent._parent)
            if parent == grand.left:
                uncle = cast(RedBlackNode, grand.right)
                if uncle != self._NIL and uncle.color == "RED":
                    parent.color = "BLACK"
                    uncle.color = "BLACK"
                    grand.color = "RED"
                    node = grand
                else:
                    if node == parent.right:
                        node = parent
                        self._rotate_left(node)
                        parent = cast(Optional[RedBlackNode], node._parent)
                        grand = cast(RedBlackNode, cast(RedBlackNode, parent)._parent)
                    cast(RedBlackNode, parent).color = "BLACK"
                    grand.color = "RED"
                    self._rotate_right(grand)
            else:
                uncle = cast(RedBlackNode, grand.left)
                if uncle != self._NIL and uncle.color == "RED":
                    parent.color = "BLACK"
                    uncle.color = "BLACK"
                    grand.color = "RED"
                    node = grand
                else:
                    if node == parent.left:
                        node = parent
                        self._rotate_right(node)
                        parent = cast(Optional[RedBlackNode], node._parent)
                        grand = cast(RedBlackNode, cast(RedBlackNode, parent)._parent)
                    cast(RedBlackNode, parent).color = "BLACK"
                    grand.color = "RED"
                    self._rotate_left(grand)

        if self._root != self._NIL:
            cast(RedBlackNode, self._root).color = "BLACK"

    def search(self, item: Any) -> bool:
        """Search for an item.

        Parameters
        ----------
        item : Any
            The item to search for.

        Returns
        -------
        bool
            True if found.

        Notes
        -----
        Time complexity: O(log n) guaranteed.
        """
        current: RedBlackNode = cast(RedBlackNode, self._root)
        while current != self._NIL:
            if item == current.data:
                return True
            elif item < current.data:
                current = cast(RedBlackNode, current.left)
            else:
                current = cast(RedBlackNode, current.right)
        return False

    def remove(self, item: Any) -> Any:
        """Remove an item maintaining Red-Black properties.

        Parameters
        ----------
        item : Any
            The item to remove.

        Returns
        -------
        Any
            The removed item.

        Raises
        ------
        EmptyStructureError
            If tree is empty.
        ValueError
            If item not found.

        Notes
        -----
        Time complexity: O(log n) guaranteed.
        Red-Black tree deletion is complex and maintained for completeness.
        """
        if self._root == self._NIL:
            raise EmptyStructureError("Cannot remove from empty tree")

        if not self.search(item):
            raise ValueError(f"Item {item} not found in tree")

        # Find node to delete
        z: RedBlackNode = cast(RedBlackNode, self._root)
        while z != self._NIL:
            if item == z.data:
                break
            elif item < z.data:
                z = cast(RedBlackNode, z.left)
            else:
                z = cast(RedBlackNode, z.right)

        self._size -= 1
        self._delete_node(z)
        return item

    def _delete_node(self, z: RedBlackNode) -> None:
        """Delete node maintaining RB properties."""
        y = z
        y_original_color = y.color

        if z.left == self._NIL:
            x = cast(RedBlackNode, z.right)
            self._transplant(z, cast(RedBlackNode, z.right))
        elif z.right == self._NIL:
            x = cast(RedBlackNode, z.left)
            self._transplant(z, cast(RedBlackNode, z.left))
        else:
            y = self._minimum(cast(RedBlackNode, z.right))
            y_original_color = y.color
            x = cast(RedBlackNode, y.right)

            if y._parent == z:
                x._parent = y
            else:
                self._transplant(y, cast(RedBlackNode, y.right))
                y.right = z.right
                cast(RedBlackNode, y.right)._parent = y

            self._transplant(z, y)
            y.left = z.left
            cast(RedBlackNode, y.left)._parent = y
            y.color = z.color

        if y_original_color == "BLACK":
            self._delete_fixup(x)

    def _delete_fixup(self, x: RedBlackNode) -> None:
        """Fix RB properties after deletion."""
        while x != self._root and x.color == "BLACK":
            parent = cast(Optional[RedBlackNode], x._parent)
            if parent is None:
                break

            if x == parent.left:
                w = cast(RedBlackNode, parent.right)
                if w == self._NIL:
                    break

                if w.color == "RED":
                    w.color = "BLACK"
                    parent.color = "RED"
                    self._rotate_left(parent)
                    w = cast(RedBlackNode, parent.right)
                    if w == self._NIL:
                        break

                # Check if both children are BLACK
                left_black = (
                    w.left == self._NIL or cast(RedBlackNode, w.left).color == "BLACK"
                )
                right_black = (
                    w.right == self._NIL or cast(RedBlackNode, w.right).color == "BLACK"
                )

                if left_black and right_black:
                    w.color = "RED"
                    x = parent
                else:
                    if right_black:
                        if w.left != self._NIL:
                            cast(RedBlackNode, w.left).color = "BLACK"
                        w.color = "RED"
                        self._rotate_right(w)
                        w = cast(RedBlackNode, parent.right)
                        if w == self._NIL:
                            break

                    w.color = parent.color
                    parent.color = "BLACK"
                    if w.right != self._NIL:
                        cast(RedBlackNode, w.right).color = "BLACK"
                    self._rotate_left(parent)
                    x = cast(RedBlackNode, self._root)
            else:
                w = cast(RedBlackNode, parent.left)
                if w == self._NIL:
                    break

                if w.color == "RED":
                    w.color = "BLACK"
                    parent.color = "RED"
                    self._rotate_right(parent)
                    w = cast(RedBlackNode, parent.left)
                    if w == self._NIL:
                        break

                # Check if both children are BLACK
                left_black = (
                    w.left == self._NIL or cast(RedBlackNode, w.left).color == "BLACK"
                )
                right_black = (
                    w.right == self._NIL or cast(RedBlackNode, w.right).color == "BLACK"
                )

                if left_black and right_black:
                    w.color = "RED"
                    x = parent
                else:
                    if left_black:
                        if w.right != self._NIL:
                            cast(RedBlackNode, w.right).color = "BLACK"
                        w.color = "RED"
                        self._rotate_left(w)
                        w = cast(RedBlackNode, parent.left)
                        if w == self._NIL:
                            break

                    w.color = parent.color
                    parent.color = "BLACK"
                    if w.left != self._NIL:
                        cast(RedBlackNode, w.left).color = "BLACK"
                    self._rotate_right(parent)
                    x = cast(RedBlackNode, self._root)

        if x != self._NIL:
            x.color = "BLACK"

    def _transplant(self, u: RedBlackNode, v: RedBlackNode) -> None:
        """Replace subtree rooted at u with subtree rooted at v."""
        if u._parent is None:
            self._root = v
        elif u == cast(RedBlackNode, u._parent).left:
            cast(RedBlackNode, u._parent).left = v
        else:
            cast(RedBlackNode, u._parent).right = v
        v._parent = cast(Optional[RedBlackNode], u._parent)

    def _minimum(self, node: RedBlackNode) -> RedBlackNode:
        """Find minimum node in subtree."""
        while node.left != self._NIL:
            node = cast(RedBlackNode, node.left)
        return node

    def clear(self) -> None:
        """Remove all nodes from the tree."""
        self._root = self._NIL
        self._size = 0

    def __iter__(self) -> Iterator[Any]:
        """Iterate inorder."""
        return self.inorder_traversal()

    def __contains__(self, item: Any) -> bool:
        """Check membership."""
        return self.search(item)

    def inorder_traversal(self) -> Iterator[Any]:
        """Inorder traversal."""
        yield from self._inorder_recursive(self._root)

    def _inorder_recursive(self, node: Optional[RedBlackNode]) -> Iterator[Any]:
        """Inorder helper."""
        if node and node != self._NIL:
            yield from self._inorder_recursive(cast(Optional[RedBlackNode], node.left))
            yield node.data
            yield from self._inorder_recursive(cast(Optional[RedBlackNode], node.right))

    def preorder_traversal(self) -> Iterator[Any]:
        """Preorder traversal."""
        yield from self._preorder_recursive(self._root)

    def _preorder_recursive(self, node: Optional[RedBlackNode]) -> Iterator[Any]:
        """Preorder helper."""
        if node and node != self._NIL:
            yield node.data
            yield from self._preorder_recursive(cast(Optional[RedBlackNode], node.left))
            yield from self._preorder_recursive(
                cast(Optional[RedBlackNode], node.right)
            )

    def postorder_traversal(self) -> Iterator[Any]:
        """Postorder traversal."""
        yield from self._postorder_recursive(self._root)

    def _postorder_recursive(self, node: Optional[RedBlackNode]) -> Iterator[Any]:
        """Postorder helper."""
        if node and node != self._NIL:
            yield from self._postorder_recursive(
                cast(Optional[RedBlackNode], node.left)
            )
            yield from self._postorder_recursive(
                cast(Optional[RedBlackNode], node.right)
            )
            yield node.data

    def level_order_traversal(self) -> Iterator[Any]:
        """Level order traversal."""
        if self._root == self._NIL:
            return
        queue: deque[RedBlackNode] = deque([cast(RedBlackNode, self._root)])
        while queue:
            current = queue.popleft()
            if current != self._NIL:
                yield current.data
                if current.left != self._NIL:
                    queue.append(cast(RedBlackNode, current.left))
                if current.right != self._NIL:
                    queue.append(cast(RedBlackNode, current.right))

    def __repr__(self) -> str:
        """Return string representation."""
        return f"RedBlackTree(size={self._size})"

    def __str__(self) -> str:
        """Return string showing inorder traversal."""
        if self.is_empty():
            return "RedBlackTree: []"
        elements = ", ".join(str(item) for item in self.inorder_traversal())
        return f"RedBlackTree: [{elements}]"
