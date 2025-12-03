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

"""B-Tree implementation for databases and file systems.

This module provides a B-Tree data structure, commonly used in databases
and file systems for efficient disk access. A B-Tree is a self-balancing
tree where nodes can have multiple keys and children.

Classes
-------
BTreeNode
    Node for B-Tree with multiple keys and children.
BTree
    B-Tree implementation with configurable order.

Examples
--------
Basic usage:

>>> from sds.tree.btree import BTree
>>> btree = BTree(order=3)  # Minimum degree = 3
>>> btree.insert(10)
>>> btree.insert(20)
>>> btree.insert(5)
>>> btree.search(10)
True

Bulk insertion:

>>> btree = BTree(order=4)
>>> for i in [10, 20, 30, 40, 50, 25, 35, 45]:
...     btree.insert(i)
>>> list(btree.inorder_traversal())
[10, 20, 25, 30, 35, 40, 45, 50]

Notes
-----
B-Trees are used in:
- Database indexes (MySQL, PostgreSQL)
- File systems (NTFS, HFS+, ext4)
- Key-value stores

Properties:
- All leaves are at the same level
- Nodes have between t-1 and 2t-1 keys (except root)
- Root has at least 1 key
- All nodes have at most 2t children

Time Complexity:
- Search: O(log n)
- Insert: O(log n)
- Delete: O(log n)

See Also
--------
sds.tree.binary : Binary search tree.
sds.tree.balanced : Balanced trees (AVL, Red-Black).
"""

from typing import Any, Iterator, Optional

from ..core.interfaces import Collection
from .node import BTreeNode

__all__ = ["BTree"]


class BTree(Collection):
    """B-Tree implementation for efficient disk-based storage.

    A B-Tree of order t (minimum degree) has the following properties:
    - Every node has at most 2t-1 keys
    - Every non-leaf node has at least t-1 keys (except root)
    - Root has at least 1 key (if tree is non-empty)
    - All leaves are at the same depth
    - A node with k keys has k+1 children

    The order t determines the branching factor. Higher t means:
    - Fewer levels (better for disk I/O)
    - More keys per node
    - Larger nodes

    Attributes
    ----------
    order : int
        The minimum degree (t) of the B-Tree.
    size : int
        Number of keys in the tree.

    Examples
    --------
    Create a B-Tree:

    >>> btree = BTree(order=3)
    >>> btree.insert(10)
    >>> btree.insert(20)
    >>> btree.insert(5)
    >>> len(btree)
    3

    Search for keys:

    >>> 10 in btree
    True
    >>> 15 in btree
    False

    Traverse in order:

    >>> btree = BTree(order=3)
    >>> for i in [20, 10, 30, 5, 15]:
    ...     btree.insert(i)
    >>> list(btree.inorder_traversal())
    [5, 10, 15, 20, 30]

    Notes
    -----
    Time Complexity (n = number of keys):
    - Search: O(log n)
    - Insert: O(log n)
    - Delete: O(log n)
    - Height: O(log n)

    B-Trees are optimized for systems that read/write large blocks
    of data (like databases and file systems).

    See Also
    --------
    BTreeNode : Node class used internally.
    """

    def __init__(self, order: int = 3):
        """Initialize an empty B-Tree.

        Parameters
        ----------
        order : int, optional
            The minimum degree (t) of the tree. Must be >= 2.
            Default is 3.

        Raises
        ------
        ValueError
            If order < 2.

        Examples
        --------
        >>> btree = BTree(order=3)
        >>> btree.order
        3
        """
        if order < 2:
            raise ValueError("B-Tree order must be at least 2")

        self._order = order  # Minimum degree (t)
        self._root: Optional[BTreeNode] = None
        self._size = 0

    @property
    def order(self) -> int:
        """Get the order (minimum degree) of the B-Tree.

        Returns
        -------
        int
            The order of the tree.
        """
        return self._order

    @property
    def size(self) -> int:
        """Get the number of keys in the tree.

        Returns
        -------
        int
            Number of keys.
        """
        return self._size

    def search(self, key: Any) -> bool:
        """Search for a key in the B-Tree.

        Parameters
        ----------
        key : Any
            The key to search for.

        Returns
        -------
        bool
            True if key exists, False otherwise.

        Examples
        --------
        >>> btree = BTree()
        >>> btree.insert(10)
        >>> btree.search(10)
        True
        >>> btree.search(20)
        False

        Notes
        -----
        Time complexity: O(log n)
        """
        if self._root is None:
            return False
        return self._search_recursive(self._root, key)

    def _search_recursive(self, node: BTreeNode, key: Any) -> bool:
        """Recursively search for a key.

        Parameters
        ----------
        node : BTreeNode
            Current node.
        key : Any
            Key to search for.

        Returns
        -------
        bool
            True if found.
        """
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and key == node.keys[i]:
            return True

        if node.is_leaf:
            return False

        return self._search_recursive(node.children[i], key)

    def insert(self, key: Any) -> None:
        """Insert a key into the B-Tree.

        Parameters
        ----------
        key : Any
            The key to insert. Must be comparable.

        Examples
        --------
        >>> btree = BTree(order=3)
        >>> btree.insert(10)
        >>> btree.insert(20)
        >>> len(btree)
        2

        Notes
        -----
        Time complexity: O(log n)
        If the key already exists, it's inserted again (duplicates allowed).
        """
        if self._root is None:
            self._root = BTreeNode(is_leaf=True)
            self._root.keys.append(key)
            self._size += 1
            return

        # If root is full, split it
        if len(self._root.keys) == 2 * self._order - 1:
            new_root = BTreeNode(is_leaf=False)
            new_root.children.append(self._root)
            self._split_child(new_root, 0)
            self._root = new_root

        self._insert_non_full(self._root, key)
        self._size += 1

    def _insert_non_full(self, node: BTreeNode, key: Any) -> None:
        """Insert key into non-full node.

        Parameters
        ----------
        node : BTreeNode
            Node to insert into (guaranteed not full).
        key : Any
            Key to insert.
        """
        i = len(node.keys) - 1

        if node.is_leaf:
            # Insert key in sorted position
            node.keys.append(None)  # Make space
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = key
        else:
            # Find child to insert into
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1

            # If child is full, split it
            if len(node.children[i].keys) == 2 * self._order - 1:
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1

            self._insert_non_full(node.children[i], key)

    def _split_child(self, parent: BTreeNode, index: int) -> None:
        """Split a full child node.

        Parameters
        ----------
        parent : BTreeNode
            Parent node.
        index : int
            Index of the child to split.
        """
        t = self._order
        full_child = parent.children[index]
        new_child = BTreeNode(is_leaf=full_child.is_leaf)

        # Save middle key BEFORE modifying arrays
        mid_index = t - 1
        middle_key = full_child.keys[mid_index]  # ✅ Save first

        # Move second half of keys to new node
        new_child.keys = full_child.keys[mid_index + 1 :]
        full_child.keys = full_child.keys[:mid_index]  # Remove middle key

        # Move second half of children if not leaf
        if not full_child.is_leaf:
            new_child.children = full_child.children[mid_index + 1 :]
            full_child.children = full_child.children[: mid_index + 1]

        # Move middle key up to parent
        parent.keys.insert(index, middle_key)  # ✅ Reuse the temporary save

        # Add new child to parent
        parent.children.insert(index + 1, new_child)

    def remove(self, key: Any) -> Any:
        """Remove a key from the B-Tree.

        Parameters
        ----------
        key : Any
            The key to remove.

        Returns
        -------
        Any
            The removed key.

        Raises
        ------
        ValueError
            If key not found.

        Examples
        --------
        >>> btree = BTree()
        >>> btree.insert(10)
        >>> btree.remove(10)
        10
        >>> 10 in btree
        False

        Notes
        -----
        Time complexity: O(log n)
        This is a simplified implementation.
        """
        if self._root is None or not self.search(key):
            raise ValueError(f"Key {key} not found in tree")

        self._remove_from_node(self._root, key)
        self._size -= 1

        # If root is empty after deletion, make its only child the new root
        if len(self._root.keys) == 0:
            if not self._root.is_leaf and len(self._root.children) > 0:
                self._root = self._root.children[0]
            else:
                self._root = None

        return key

    def _remove_from_node(self, node: BTreeNode, key: Any) -> None:
        """Remove key from node (simplified version).

        Parameters
        ----------
        node : BTreeNode
            Node to remove from.
        key : Any
            Key to remove.
        """
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and key == node.keys[i]:
            # Key found in this node
            if node.is_leaf:
                node.keys.pop(i)
            else:
                # Replace with predecessor or successor
                # Simplified: just remove from leaf
                predecessor = self._get_predecessor(node, i)
                node.keys[i] = predecessor
                self._remove_from_node(node.children[i], predecessor)
        elif not node.is_leaf:
            # Key might be in subtree
            self._remove_from_node(node.children[i], key)

    def _get_predecessor(self, node: BTreeNode, index: int) -> Any:
        """Get predecessor key (rightmost key in left subtree).

        Parameters
        ----------
        node : BTreeNode
            Parent node.
        index : int
            Index of the key.

        Returns
        -------
        Any
            Predecessor key.
        """
        current = node.children[index]
        while not current.is_leaf:
            current = current.children[-1]
        return current.keys[-1]

    def clear(self) -> None:
        """Remove all keys from the tree."""
        self._root = None
        self._size = 0

    def __len__(self) -> int:
        """Return number of keys in tree."""
        return self._size

    def is_empty(self) -> bool:
        """Check if tree is empty."""
        return self._size == 0

    def __contains__(self, key: Any) -> bool:
        """Check if key is in tree."""
        return self.search(key)

    def __iter__(self) -> Iterator[Any]:
        """Iterate over keys in sorted order."""
        return self.inorder_traversal()

    def inorder_traversal(self) -> Iterator[Any]:
        """Traverse keys in sorted order.

        Yields
        ------
        Any
            Keys in sorted order.

        Examples
        --------
        >>> btree = BTree()
        >>> for i in [20, 10, 30]:
        ...     btree.insert(i)
        >>> list(btree.inorder_traversal())
        [10, 20, 30]

        Notes
        -----
        Time complexity: O(n)
        """
        if self._root:
            yield from self._inorder_recursive(self._root)

    def _inorder_recursive(self, node: BTreeNode) -> Iterator[Any]:
        """Recursively traverse in order.

        Parameters
        ----------
        node : BTreeNode
            Current node.

        Yields
        ------
        Any
            Keys in order.
        """
        if node.is_leaf:
            yield from node.keys
        else:
            for i in range(len(node.keys)):
                yield from self._inorder_recursive(node.children[i])
                yield node.keys[i]
            yield from self._inorder_recursive(node.children[-1])

    def height(self) -> int:
        """Calculate the height of the tree.

        Returns
        -------
        int
            Height of the tree (-1 if empty).

        Examples
        --------
        >>> btree = BTree(order=3)
        >>> btree.height()
        -1
        >>> btree.insert(10)
        >>> btree.height()
        0

        Notes
        -----
        Time complexity: O(log n)
        """
        if self._root is None:
            return -1
        return self._height_recursive(self._root)

    def _height_recursive(self, node: BTreeNode) -> int:
        """Recursively calculate height.

        Parameters
        ----------
        node : BTreeNode
            Current node.

        Returns
        -------
        int
            Height from this node.
        """
        if node.is_leaf:
            return 0
        return 1 + self._height_recursive(node.children[0])

    def __repr__(self) -> str:
        """Return string representation."""
        return f"BTree(order={self._order}, size={self._size})"

    def __str__(self) -> str:
        """Return string showing keys."""
        if self.is_empty():
            return "BTree: []"
        keys = list(self.inorder_traversal())
        if len(keys) <= 20:
            return f"BTree: {keys}"
        return f"BTree: [{', '.join(map(str, keys[:20]))}, ... ({len(keys)} keys)]"
