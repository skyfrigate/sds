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

"""Binary tree implementation.

This module provides a simple binary tree implementation where nodes can
have at most two children. Unlike BST, this tree does not maintain any
ordering property.

Classes
-------
BinaryTree
    Simple binary tree without ordering constraints.

Examples
--------
Creating and using a binary tree:

>>> from sds.tree.binary import BinaryTree
>>> tree = BinaryTree()
>>> tree.insert(10)
>>> tree.insert(5)
>>> tree.insert(15)
>>> len(tree)
3
>>> tree.height()
1

Traversals:

>>> list(tree.inorder_traversal())
[5, 10, 15]
>>> list(tree.preorder_traversal())
[10, 5, 15]

Notes
-----
This is a basic binary tree without ordering. For ordered insertion,
use BinarySearchTree instead.

See Also
--------
sds.tree.bst : Binary search tree with ordering.
sds.tree.interfaces : Abstract tree interfaces.
"""

from collections import deque
from typing import Any, Iterator, Optional

from ..core.exceptions import EmptyStructureError
from .interfaces import AbstractBinaryTree
from .node import BinaryNode

__all__ = ["BinaryTree", "BinarySearchTree"]


class BinaryTree(AbstractBinaryTree):
    """A simple binary tree implementation.

    A binary tree where each node has at most two children. This
    implementation inserts nodes level by level (breadth-first),
    maintaining a complete tree structure.

    Attributes
    ----------
    root : BinaryNode or None
        The root node of the tree (read-only property).
    size : int
        The number of nodes in the tree (read-only property).

    Examples
    --------
    Create and populate a binary tree:

    >>> tree = BinaryTree()
    >>> tree.insert(10)
    >>> tree.insert(5)
    >>> tree.insert(15)
    >>> tree.insert(3)
    >>> len(tree)
    4

    Check height:

    >>> tree.height()
    2

    Search for items:

    >>> tree.search(5)
    True
    >>> tree.search(100)
    False

    Traverse the tree:

    >>> list(tree.level_order_traversal())
    [10, 5, 15, 3]

    Notes
    -----
    This implementation inserts nodes in level-order to maintain
    a complete binary tree. For ordered insertion, use BST.

    Time Complexity
    ---------------
    - Insert: O(n) - must find insertion point
    - Search: O(n) - linear search
    - Remove: O(n) - must find and reorganize
    - Traversals: O(n)
    - Height: O(n)

    See Also
    --------
    BinarySearchTree : Ordered binary tree.
    """

    def __init__(self) -> None:
        """Initialize an empty binary tree."""
        super().__init__()

    def height(self) -> int:
        """Return the height of the tree.

        Returns
        -------
        int
            The height of the tree, or -1 if empty.

        Examples
        --------
        >>> tree = BinaryTree()
        >>> tree.height()
        -1
        >>> tree.insert(10)
        >>> tree.height()
        0
        >>> tree.insert(5)
        >>> tree.insert(15)
        >>> tree.height()
        1

        Notes
        -----
        Time complexity: O(n)
        """
        return self._height_recursive(self._root)

    def _height_recursive(self, node: Optional[BinaryNode]) -> int:
        """Calculate height recursively.

        Parameters
        ----------
        node : BinaryNode or None
            The current node.

        Returns
        -------
        int
            Height of subtree rooted at node.
        """
        if node is None:
            return -1

        left_height = self._height_recursive(node.left)
        right_height = self._height_recursive(node.right)

        return 1 + max(left_height, right_height)

    def insert(self, item: Any) -> None:
        """Insert an item into the tree.

        Inserts in level-order to maintain a complete binary tree.

        Parameters
        ----------
        item : Any
            The item to insert.

        Examples
        --------
        >>> tree = BinaryTree()
        >>> tree.insert(10)
        >>> tree.insert(5)
        >>> tree.insert(15)
        >>> len(tree)
        3

        Notes
        -----
        Time complexity: O(n) - must traverse to find insertion point
        """
        new_node = BinaryNode(item)

        if self._root is None:
            self._root = new_node
            self._size += 1
            return

        # Level-order traversal to find first available position
        queue: deque[BinaryNode] = deque([self._root])

        while queue:
            current = queue.popleft()

            if current.left is None:
                current.left = new_node
                self._size += 1
                return
            else:
                queue.append(current.left)

            if current.right is None:
                current.right = new_node
                self._size += 1
                return
            else:
                queue.append(current.right)

    def remove(self, item: Any) -> Any:
        """Remove and return an item from the tree.

        Removes the node containing item and replaces it with the
        deepest rightmost node to maintain tree structure.

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
        >>> tree = BinaryTree()
        >>> tree.insert(10)
        >>> tree.insert(5)
        >>> tree.insert(15)
        >>> tree.remove(5)
        5
        >>> len(tree)
        2

        Notes
        -----
        Time complexity: O(n)
        """
        if self._root is None:
            raise EmptyStructureError("Cannot remove from empty tree")

        # Find the node to delete and the deepest rightmost node
        target_node: Optional[BinaryNode] = None
        last_node: Optional[BinaryNode] = None
        parent_of_last: Optional[BinaryNode] = None

        queue: deque[tuple[BinaryNode, Optional[BinaryNode]]] = deque(
            [(self._root, None)]
        )

        while queue:
            current, parent = queue.popleft()
            last_node = current
            parent_of_last = parent

            if current.data == item:
                target_node = current

            if current.left:
                queue.append((current.left, current))
            if current.right:
                queue.append((current.right, current))

        if target_node is None:
            raise ValueError(f"Item {item} not found in tree")

        # Store the value to return
        removed_data = target_node.data

        # If tree has only one node
        if self._root.left is None and self._root.right is None:
            self._root = None
            self._size -= 1
            return removed_data

        # Replace target with last node's data
        if last_node is not None:
            target_node.data = last_node.data

            # Remove the last node
            if parent_of_last:
                if parent_of_last.right == last_node:
                    parent_of_last.right = None
                else:
                    parent_of_last.left = None

        self._size -= 1
        return removed_data

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
        >>> tree = BinaryTree()
        >>> tree.insert(10)
        >>> tree.search(10)
        True
        >>> tree.search(5)
        False

        Notes
        -----
        Time complexity: O(n) - linear search
        """
        return self._search_recursive(self._root, item)

    def _search_recursive(self, node: Optional[BinaryNode], item: Any) -> bool:
        """Search recursively.

        Parameters
        ----------
        node : BinaryNode or None
            Current node.
        item : Any
            Item to search for.

        Returns
        -------
        bool
            True if found.
        """
        if node is None:
            return False

        if node.data == item:
            return True

        return self._search_recursive(node.left, item) or self._search_recursive(
            node.right, item
        )

    def clear(self) -> None:
        """Remove all nodes from the tree.

        Examples
        --------
        >>> tree = BinaryTree()
        >>> tree.insert(10)
        >>> tree.insert(5)
        >>> tree.clear()
        >>> tree.is_empty()
        True

        Notes
        -----
        Time complexity: O(1)
        """
        self._root = None
        self._size = 0

    def __iter__(self) -> Iterator[Any]:
        """Iterate over tree elements (inorder by default).

        Yields
        ------
        Any
            Elements in inorder.

        Examples
        --------
        >>> tree = BinaryTree()
        >>> tree.insert(10)
        >>> tree.insert(5)
        >>> tree.insert(15)
        >>> list(tree)
        [5, 10, 15]
        """
        return self.inorder_traversal()

    def __contains__(self, item: Any) -> bool:
        """Check if item is in the tree.

        Parameters
        ----------
        item : Any
            Item to check.

        Returns
        -------
        bool
            True if item is in tree.

        Examples
        --------
        >>> tree = BinaryTree()
        >>> tree.insert(10)
        >>> 10 in tree
        True
        >>> 5 in tree
        False
        """
        return self.search(item)

    def inorder_traversal(self) -> Iterator[Any]:
        """Return inorder traversal iterator (left-root-right).

        Yields
        ------
        Any
            Items in inorder.

        Examples
        --------
        >>> tree = BinaryTree()
        >>> tree.insert(10)
        >>> tree.insert(5)
        >>> tree.insert(15)
        >>> list(tree.inorder_traversal())
        [5, 10, 15]

        Notes
        -----
        Time complexity: O(n)
        """
        yield from self._inorder_recursive(self._root)

    def _inorder_recursive(self, node: Optional[BinaryNode]) -> Iterator[Any]:
        """Inorder traversal helper.

        Parameters
        ----------
        node : BinaryNode or None
            Current node.

        Yields
        ------
        Any
            Items in inorder.
        """
        if node is not None:
            yield from self._inorder_recursive(node.left)
            yield node.data
            yield from self._inorder_recursive(node.right)

    def preorder_traversal(self) -> Iterator[Any]:
        """Return preorder traversal iterator (root-left-right).

        Yields
        ------
        Any
            Items in preorder.

        Examples
        --------
        >>> tree = BinaryTree()
        >>> tree.insert(10)
        >>> tree.insert(5)
        >>> tree.insert(15)
        >>> list(tree.preorder_traversal())
        [10, 5, 15]

        Notes
        -----
        Time complexity: O(n)
        """
        yield from self._preorder_recursive(self._root)

    def _preorder_recursive(self, node: Optional[BinaryNode]) -> Iterator[Any]:
        """Preorder traversal helper.

        Parameters
        ----------
        node : BinaryNode or None
            Current node.

        Yields
        ------
        Any
            Items in preorder.
        """
        if node is not None:
            yield node.data
            yield from self._preorder_recursive(node.left)
            yield from self._preorder_recursive(node.right)

    def postorder_traversal(self) -> Iterator[Any]:
        """Return postorder traversal iterator (left-right-root).

        Yields
        ------
        Any
            Items in postorder.

        Examples
        --------
        >>> tree = BinaryTree()
        >>> tree.insert(10)
        >>> tree.insert(5)
        >>> tree.insert(15)
        >>> list(tree.postorder_traversal())
        [5, 15, 10]

        Notes
        -----
        Time complexity: O(n)
        """
        yield from self._postorder_recursive(self._root)

    def _postorder_recursive(self, node: Optional[BinaryNode]) -> Iterator[Any]:
        """Postorder traversal helper.

        Parameters
        ----------
        node : BinaryNode or None
            Current node.

        Yields
        ------
        Any
            Items in postorder.
        """
        if node is not None:
            yield from self._postorder_recursive(node.left)
            yield from self._postorder_recursive(node.right)
            yield node.data

    def level_order_traversal(self) -> Iterator[Any]:
        """Return level-order traversal iterator (BFS).

        Yields
        ------
        Any
            Items level by level.

        Examples
        --------
        >>> tree = BinaryTree()
        >>> tree.insert(10)
        >>> tree.insert(5)
        >>> tree.insert(15)
        >>> tree.insert(3)
        >>> list(tree.level_order_traversal())
        [10, 5, 15, 3]

        Notes
        -----
        Time complexity: O(n)
        """
        if self._root is None:
            return

        queue: deque[BinaryNode] = deque([self._root])

        while queue:
            current = queue.popleft()
            yield current.data

            if current.left:
                queue.append(current.left)
            if current.right:
                queue.append(current.right)

    def __repr__(self) -> str:
        """Return string representation.

        Returns
        -------
        str
            String representation.

        Examples
        --------
        >>> tree = BinaryTree()
        >>> tree.insert(10)
        >>> repr(tree)
        'BinaryTree(size=1)'
        """
        return f"BinaryTree(size={self._size})"

    def __str__(self) -> str:
        """Return string showing level-order traversal.

        Returns
        -------
        str
            String representation.

        Examples
        --------
        >>> tree = BinaryTree()
        >>> tree.insert(10)
        >>> tree.insert(5)
        >>> str(tree)
        'BinaryTree: [10, 5]'
        """
        if self.is_empty():
            return "BinaryTree: []"
        elements = ", ".join(
            str(item) for item in self.level_order_traversal()
        )  # noqa: E501
        return f"BinaryTree: [{elements}]"


class BinarySearchTree(AbstractBinaryTree):
    """Binary Search Tree implementation.

    A binary search tree where for each node:
    - All values in left subtree are less than the node's value
    - All values in right subtree are greater than the node's value
    - Both left and right subtrees are also BSTs

    This property enables efficient O(log n) average case operations
    for search, insert, and delete in balanced trees.

    Attributes
    ----------
    root : BinaryNode or None
        The root node of the tree (read-only property).
    size : int
        The number of nodes in the tree (read-only property).

    Examples
    --------
    Create and populate a BST:

    >>> bst = BinarySearchTree()
    >>> for value in [10, 5, 15, 3, 7, 12, 20]:
    ...     bst.insert(value)
    >>> len(bst)
    7

    Inorder traversal yields sorted values:

    >>> list(bst.inorder_traversal())
    [3, 5, 7, 10, 12, 15, 20]

    Search operations:

    >>> bst.search(7)
    True
    >>> 12 in bst
    True
    >>> bst.search(100)
    False

    Find minimum and maximum:

    >>> bst.find_min()
    3
    >>> bst.find_max()
    20

    Remove elements:

    >>> bst.remove(10)
    10
    >>> list(bst.inorder_traversal())
    [3, 5, 7, 12, 15, 20]

    Notes
    -----
    Time Complexity (average case for balanced tree):
    - Insert: O(log n)
    - Search: O(log n)
    - Remove: O(log n)
    - Find min/max: O(log n)
    - Traversals: O(n)

    Worst case (degenerate tree): O(n) for all operations.

    See Also
    --------
    BinaryTree : Unordered binary tree.
    """

    def __init__(self) -> None:
        """Initialize an empty binary search tree."""
        super().__init__()

    def height(self) -> int:
        """Return the height of the tree.

        Returns
        -------
        int
            The height of the tree, or -1 if empty.

        Examples
        --------
        >>> bst = BinarySearchTree()
        >>> bst.height()
        -1
        >>> bst.insert(10)
        >>> bst.height()
        0
        >>> bst.insert(5)
        >>> bst.insert(15)
        >>> bst.height()
        1

        Notes
        -----
        Time complexity: O(n)
        """
        return self._height_recursive(self._root)

    def _height_recursive(self, node: Optional[BinaryNode]) -> int:
        """Calculate height recursively.

        Parameters
        ----------
        node : BinaryNode or None
            The current node.

        Returns
        -------
        int
            Height of subtree rooted at node.
        """
        if node is None:
            return -1

        left_height = self._height_recursive(node.left)
        right_height = self._height_recursive(node.right)

        return 1 + max(left_height, right_height)

    def insert(self, item: Any) -> None:
        """Insert an item into the BST maintaining BST property.

        Parameters
        ----------
        item : Any
            The item to insert. Must be comparable.

        Examples
        --------
        >>> bst = BinarySearchTree()
        >>> bst.insert(10)
        >>> bst.insert(5)
        >>> bst.insert(15)
        >>> list(bst.inorder_traversal())
        [5, 10, 15]

        Notes
        -----
        Duplicate values are allowed and placed in the right subtree.
        Time complexity: O(log n) average, O(n) worst case.

        Raises
        ------
        TypeError
            If item is not comparable with existing items.
        """
        self._root = self._insert_recursive(self._root, item)
        self._size += 1

    def _insert_recursive(self, node: Optional[BinaryNode], item: Any) -> BinaryNode:
        """Insert recursively maintaining BST property.

        Parameters
        ----------
        node : BinaryNode or None
            Current node in recursion.
        item : Any
            Item to insert.

        Returns
        -------
        BinaryNode
            The node after insertion.
        """
        if node is None:
            return BinaryNode(item)

        if item < node.data:
            node.left = self._insert_recursive(node.left, item)
        else:  # item >= node.data (duplicates go right)
            node.right = self._insert_recursive(node.right, item)

        return node

    def remove(self, item: Any) -> Any:
        """Remove and return an item from the BST.

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
        >>> bst = BinarySearchTree()
        >>> bst.insert(10)
        >>> bst.insert(5)
        >>> bst.insert(15)
        >>> bst.remove(5)
        5
        >>> list(bst.inorder_traversal())
        [10, 15]

        Notes
        -----
        Time complexity: O(log n) average, O(n) worst case.
        """
        if self._root is None:
            raise EmptyStructureError("Cannot remove from empty tree")

        if not self.search(item):
            raise ValueError(f"Item {item} not found in tree")

        self._root = self._remove_recursive(self._root, item)
        self._size -= 1
        return item

    def _remove_recursive(
        self, node: Optional[BinaryNode], item: Any
    ) -> Optional[BinaryNode]:
        """Remove recursively maintaining BST property.

        Parameters
        ----------
        node : BinaryNode or None
            Current node in recursion.
        item : Any
            Item to remove.

        Returns
        -------
        BinaryNode or None
            The node after removal.
        """
        if node is None:
            return None

        if item < node.data:
            node.left = self._remove_recursive(node.left, item)
        elif item > node.data:
            node.right = self._remove_recursive(node.right, item)
        else:
            # Node to be deleted found
            # Case 1: Node with only right child or no child
            if node.left is None:
                return node.right
            # Case 2: Node with only left child
            elif node.right is None:
                return node.left
            # Case 3: Node with two children
            else:
                # Find inorder successor (min in right subtree)
                successor = self._find_min_node(node.right)
                node.data = successor.data
                # Remove the successor
                node.right = self._remove_recursive(node.right, successor.data)

        return node

    def search(self, item: Any) -> bool:
        """Search for an item in the BST.

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
        >>> bst = BinarySearchTree()
        >>> bst.insert(10)
        >>> bst.search(10)
        True
        >>> bst.search(5)
        False

        Notes
        -----
        Time complexity: O(log n) average, O(n) worst case.
        """
        return self._search_recursive(self._root, item)

    def _search_recursive(self, node: Optional[BinaryNode], item: Any) -> bool:
        """Search recursively using BST property.

        Parameters
        ----------
        node : BinaryNode or None
            Current node.
        item : Any
            Item to search for.

        Returns
        -------
        bool
            True if found.
        """
        if node is None:
            return False

        if item == node.data:
            return True
        elif item < node.data:
            return self._search_recursive(node.left, item)
        else:
            return self._search_recursive(node.right, item)

    def find_min(self) -> Any:
        """Find and return the minimum value in the BST.

        Returns
        -------
        Any
            The minimum value.

        Raises
        ------
        EmptyStructureError
            If the tree is empty.

        Examples
        --------
        >>> bst = BinarySearchTree()
        >>> bst.insert(10)
        >>> bst.insert(5)
        >>> bst.insert(15)
        >>> bst.find_min()
        5

        Notes
        -----
        Time complexity: O(log n) average, O(n) worst case.
        """
        if self._root is None:
            raise EmptyStructureError("Cannot find min in empty tree")

        return self._find_min_node(self._root).data

    def _find_min_node(self, node: BinaryNode) -> BinaryNode:
        """Find the node with minimum value in subtree.

        Parameters
        ----------
        node : BinaryNode
            Root of subtree.

        Returns
        -------
        BinaryNode
            Node with minimum value.
        """
        current = node
        while current.left is not None:
            current = current.left
        return current

    def find_max(self) -> Any:
        """Find and return the maximum value in the BST.

        Returns
        -------
        Any
            The maximum value.

        Raises
        ------
        EmptyStructureError
            If the tree is empty.

        Examples
        --------
        >>> bst = BinarySearchTree()
        >>> bst.insert(10)
        >>> bst.insert(5)
        >>> bst.insert(15)
        >>> bst.find_max()
        15

        Notes
        -----
        Time complexity: O(log n) average, O(n) worst case.
        """
        if self._root is None:
            raise EmptyStructureError("Cannot find max in empty tree")

        return self._find_max_node(self._root).data

    def _find_max_node(self, node: BinaryNode) -> BinaryNode:
        """Find the node with maximum value in subtree.

        Parameters
        ----------
        node : BinaryNode
            Root of subtree.

        Returns
        -------
        BinaryNode
            Node with maximum value.
        """
        current = node
        while current.right is not None:
            current = current.right
        return current

    def clear(self) -> None:
        """Remove all nodes from the tree.

        Examples
        --------
        >>> bst = BinarySearchTree()
        >>> bst.insert(10)
        >>> bst.insert(5)
        >>> bst.clear()
        >>> bst.is_empty()
        True

        Notes
        -----
        Time complexity: O(1)
        """
        self._root = None
        self._size = 0

    def __iter__(self) -> Iterator[Any]:
        """Iterate over tree elements (inorder - sorted order).

        Yields
        ------
        Any
            Elements in sorted order.

        Examples
        --------
        >>> bst = BinarySearchTree()
        >>> for val in [10, 5, 15, 3, 7]:
        ...     bst.insert(val)
        >>> list(bst)
        [3, 5, 7, 10, 15]
        """
        return self.inorder_traversal()

    def __contains__(self, item: Any) -> bool:
        """Check if item is in the tree.

        Parameters
        ----------
        item : Any
            Item to check.

        Returns
        -------
        bool
            True if item is in tree.

        Examples
        --------
        >>> bst = BinarySearchTree()
        >>> bst.insert(10)
        >>> 10 in bst
        True
        >>> 5 in bst
        False
        """
        return self.search(item)

    def inorder_traversal(self) -> Iterator[Any]:
        """Return inorder traversal iterator (sorted order for BST).

        Yields
        ------
        Any
            Items in sorted order.

        Examples
        --------
        >>> bst = BinarySearchTree()
        >>> for val in [10, 5, 15, 3, 7]:
        ...     bst.insert(val)
        >>> list(bst.inorder_traversal())
        [3, 5, 7, 10, 15]

        Notes
        -----
        Time complexity: O(n)
        Space complexity: O(h) for recursion stack
        """
        yield from self._inorder_recursive(self._root)

    def _inorder_recursive(self, node: Optional[BinaryNode]) -> Iterator[Any]:
        """Inorder traversal helper.

        Parameters
        ----------
        node : BinaryNode or None
            Current node.

        Yields
        ------
        Any
            Items in inorder.
        """
        if node is not None:
            yield from self._inorder_recursive(node.left)
            yield node.data
            yield from self._inorder_recursive(node.right)

    def preorder_traversal(self) -> Iterator[Any]:
        """Return preorder traversal iterator (root-left-right).

        Yields
        ------
        Any
            Items in preorder.

        Examples
        --------
        >>> bst = BinarySearchTree()
        >>> for val in [10, 5, 15]:
        ...     bst.insert(val)
        >>> list(bst.preorder_traversal())
        [10, 5, 15]

        Notes
        -----
        Time complexity: O(n)
        """
        yield from self._preorder_recursive(self._root)

    def _preorder_recursive(self, node: Optional[BinaryNode]) -> Iterator[Any]:
        """Preorder traversal helper.

        Parameters
        ----------
        node : BinaryNode or None
            Current node.

        Yields
        ------
        Any
            Items in preorder.
        """
        if node is not None:
            yield node.data
            yield from self._preorder_recursive(node.left)
            yield from self._preorder_recursive(node.right)

    def postorder_traversal(self) -> Iterator[Any]:
        """Return postorder traversal iterator (left-right-root).

        Yields
        ------
        Any
            Items in postorder.

        Examples
        --------
        >>> bst = BinarySearchTree()
        >>> for val in [10, 5, 15]:
        ...     bst.insert(val)
        >>> list(bst.postorder_traversal())
        [5, 15, 10]

        Notes
        -----
        Time complexity: O(n)
        """
        yield from self._postorder_recursive(self._root)

    def _postorder_recursive(self, node: Optional[BinaryNode]) -> Iterator[Any]:
        """Postorder traversal helper.

        Parameters
        ----------
        node : BinaryNode or None
            Current node.

        Yields
        ------
        Any
            Items in postorder.
        """
        if node is not None:
            yield from self._postorder_recursive(node.left)
            yield from self._postorder_recursive(node.right)
            yield node.data

    def level_order_traversal(self) -> Iterator[Any]:
        """Return level-order traversal iterator (BFS).

        Yields
        ------
        Any
            Items level by level.

        Examples
        --------
        >>> bst = BinarySearchTree()
        >>> for val in [10, 5, 15, 3, 7]:
        ...     bst.insert(val)
        >>> list(bst.level_order_traversal())
        [10, 5, 15, 3, 7]

        Notes
        -----
        Time complexity: O(n)
        """
        if self._root is None:
            return

        queue: deque[BinaryNode] = deque([self._root])

        while queue:
            current = queue.popleft()
            yield current.data

            if current.left:
                queue.append(current.left)
            if current.right:
                queue.append(current.right)

    def __repr__(self) -> str:
        """Return string representation.

        Returns
        -------
        str
            String representation.

        Examples
        --------
        >>> bst = BinarySearchTree()
        >>> bst.insert(10)
        >>> repr(bst)
        'BinarySearchTree(size=1)'
        """
        return f"BinarySearchTree(size={self._size})"

    def __str__(self) -> str:
        """Return string showing inorder traversal (sorted).

        Returns
        -------
        str
            String representation.

        Examples
        --------
        >>> bst = BinarySearchTree()
        >>> bst.insert(10)
        >>> bst.insert(5)
        >>> str(bst)
        'BinarySearchTree: [5, 10]'
        """
        if self.is_empty():
            return "BinarySearchTree: []"
        elements = ", ".join(str(item) for item in self.inorder_traversal())
        return f"BinarySearchTree: [{elements}]"
