# Copyright 2024-2025, skyfrigate, biface
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

"""B-Tree implementation.

This module provides a B-Tree data structure, which is a self-balancing
search tree optimized for systems that read and write large blocks of data.
B-Trees are commonly used in databases and file systems.

Classes
-------
BTree
    Self-balancing search tree with multiple keys per node.

Examples
--------
Creating and using a B-Tree:

>>> from sds.tree.btree import BTree
>>> tree = BTree(t=3)
>>> tree.insert(10)
>>> tree.insert(20)
>>> tree.insert(5)
>>> tree.search(10)
True
>>> list(tree)
[5, 10, 20]

B-Trees maintain balance automatically:

>>> tree = BTree(t=2)
>>> for i in range(1, 8):
...     tree.insert(i * 10)
>>> tree.height()  # Stays logarithmic
1

Notes
-----
B-Trees are particularly useful for:
- Database indexing
- File system implementations
- Large datasets that don't fit in memory
- Minimizing disk I/O operations

Time Complexity (all operations):
- Search: O(log n)
- Insert: O(log n)
- Delete: O(log n)
- All operations guaranteed logarithmic

See Also
--------
sds.tree.binary : Binary search tree implementations.
sds.tree.balanced : AVL and Red-Black trees.
"""

from collections import deque
from typing import Any, Iterator, List, Optional, Tuple, cast

from ..core.exceptions import EmptyStructureError
from ..core.node import Node
from .interfaces import AbstractTree
from .node import BTreeNode

__all__ = ["BTree"]


class BTree(AbstractTree):
    """B-Tree implementation.

    A B-Tree is a self-balancing search tree where each node can contain
    multiple keys and have multiple children. It maintains the following
    properties:

    1. Every node has at most 2t-1 keys
    2. Every non-leaf node has at least t-1 keys (except root)
    3. Root has at least 1 key (if tree is non-empty)
    4. All leaves are at the same depth
    5. A non-leaf node with k keys has k+1 children
    6. Keys in each node are in ascending order

    Parameters
    ----------
    t : int, optional
        Minimum degree (minimum number of keys is t-1, maximum is 2t-1).
        Must be >= 2. Default is 3.

    Attributes
    ----------
    root : BTreeNode or None
        The root node of the tree (read-only property).
    size : int
        The number of keys in the tree (read-only property).
    t : int
        The minimum degree of the tree (read-only property).

    Examples
    --------
    Create and populate a B-Tree:

    >>> tree = BTree(t=3)
    >>> tree.insert(10)
    >>> tree.insert(20)
    >>> tree.insert(5)
    >>> tree.insert(6)
    >>> len(tree)
    4

    Search for keys:

    >>> tree.search(10)
    True
    >>> tree.search(15)
    False
    >>> 20 in tree
    True

    Iterate in sorted order:

    >>> list(tree)
    [5, 6, 10, 20]

    Find minimum and maximum:

    >>> tree.find_min()
    5
    >>> tree.find_max()
    20

    Remove keys:

    >>> tree.remove(10)
    10
    >>> tree.search(10)
    False
    >>> list(tree)
    [5, 6, 20]

    Notes
    -----
    Time Complexity (guaranteed):
    - insert: O(log n)
    - search: O(log n)
    - remove: O(log n)
    - find_min/max: O(log n)
    - height: O(1)

    B-Trees are optimized for systems that read/write large blocks of data.
    The parameter t should be chosen based on block size for optimal I/O.

    Duplicate keys are not allowed. Attempting to insert an existing key
    has no effect.

    See Also
    --------
    BTreeNode : Node class used internally.
    BinarySearchTree : Simpler binary search tree.
    AVLTree : Height-balanced binary search tree.
    """

    def __init__(self, t: int = 3) -> None:
        """Initialize an empty B-Tree.

        Parameters
        ----------
        t : int, optional
            Minimum degree. Must be >= 2. Default is 3.

        Raises
        ------
        ValueError
            If t < 2.

        Examples
        --------
        >>> tree = BTree()
        >>> tree.t
        3
        >>> tree.is_empty()
        True

        >>> tree = BTree(t=5)
        >>> tree.t
        5
        """
        if t < 2:
            raise ValueError("Minimum degree t must be at least 2")

        super().__init__()
        self._t: int = t
        self._root: Optional[BTreeNode] = None
        self._size: int = 0

    @property
    def root(self) -> Optional[BTreeNode]:
        """Get the root node of the tree.

        Returns
        -------
        BTreeNode or None
            The root node, or None if tree is empty.

        Examples
        --------
        >>> tree = BTree()
        >>> tree.root is None
        True
        >>> tree.insert(10)
        >>> tree.root.keys
        [10]
        """
        return self._root

    @property
    def t(self) -> int:
        """Get the minimum degree of the tree.

        Returns
        -------
        int
            The minimum degree.

        Examples
        --------
        >>> tree = BTree(t=3)
        >>> tree.t
        3
        """
        return self._t

    def height(self) -> int:
        """Return the height of the tree.

        Returns
        -------
        int
            Height of the tree, or -1 if empty.

        Examples
        --------
        >>> tree = BTree()
        >>> tree.height()
        -1
        >>> tree.insert(10)
        >>> tree.height()
        0

        Notes
        -----
        Time complexity: O(1) - height is tracked during operations.
        """
        if self._root is None:
            return -1
        return self._get_height(self._root)

    def _get_height(self, node: BTreeNode) -> int:
        """Get height of subtree rooted at node.

        Parameters
        ----------
        node : BTreeNode
            Root of subtree.

        Returns
        -------
        int
            Height of subtree.
        """
        if node.is_leaf:
            return 0
        return 1 + self._get_height(node.children[0])

    def search(self, key: Any) -> bool:
        """Search for a key in the tree.

        Parameters
        ----------
        key : Any
            Key to search for.

        Returns
        -------
        bool
            True if key is found, False otherwise.

        Examples
        --------
        >>> tree = BTree()
        >>> tree.insert(10)
        >>> tree.search(10)
        True
        >>> tree.search(20)
        False

        Notes
        -----
        Time complexity: O(log n)
        """
        if self._root is None:
            return False
        result = self._search_recursive(self._root, key)
        return result[0] is not None

    def _search_recursive(
        self, node: BTreeNode, key: Any
    ) -> Tuple[Optional[BTreeNode], int]:
        """Search for key starting from node.

        Parameters
        ----------
        node : BTreeNode
            Current node.
        key : Any
            Key to search for.

        Returns
        -------
        Tuple[BTreeNode or None, int]
            (node, index) if found, (None, -1) if not found.
        """
        i = 0
        # Find the first key greater than or equal to key
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        # Check if key is found
        if i < len(node.keys) and key == node.keys[i]:
            return (node, i)

        # If leaf, key not found
        if node.is_leaf:
            return (None, -1)

        # Recurse to appropriate child
        return self._search_recursive(node.children[i], key)

    def insert(self, key: Any) -> None:
        """Insert a key into the tree.

        If the key already exists, the insertion is ignored (no duplicates).

        Parameters
        ----------
        key : Any
            Key to insert. Must be comparable.

        Examples
        --------
        >>> tree = BTree(t=2)
        >>> tree.insert(10)
        >>> tree.insert(20)
        >>> tree.insert(5)
        >>> list(tree)
        [5, 10, 20]

        Duplicate keys are ignored:

        >>> tree.insert(10)
        >>> len(tree)
        3

        Notes
        -----
        Time complexity: O(log n)
        """
        # Check if key already exists
        if self.search(key):
            return

        # If tree is empty
        if self._root is None:
            self._root = BTreeNode(self._t)
            self._root.keys = [key]
            self._size = 1
            return

        # If root is full, split it
        if self._root.is_full():
            old_root = self._root
            self._root = BTreeNode(self._t, is_leaf=False)
            self._root.add_child(old_root)
            self._split_child(self._root, 0)

        # Insert in non-full tree
        self._insert_non_full(self._root, key)
        self._size += 1

    def _insert_non_full(self, node: BTreeNode, key: Any) -> None:
        """Insert key in non-full node.

        Parameters
        ----------
        node : BTreeNode
            Node to insert into (must not be full).
        key : Any
            Key to insert.
        """
        i = len(node.keys) - 1

        if node.is_leaf:
            # Insert key in sorted position
            node.keys.append(None)
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = key
        else:
            # Find child to insert into
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1

            # Split child if full
            if node.children[i].is_full():
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1

            self._insert_non_full(node.children[i], key)

    def _split_child(self, parent: BTreeNode, index: int) -> None:
        """Split full child at index.

        Parameters
        ----------
        parent : BTreeNode
            Parent node.
        index : int
            Index of child to split.
        """
        t = self._t
        full_child = parent.children[index]
        new_child = BTreeNode(t, is_leaf=full_child.is_leaf)

        # Calculate middle index and save middle key BEFORE modifying lists
        mid_idx = t - 1
        middle_key = full_child.keys[mid_idx]

        # Move half of keys to new child
        new_child.keys = full_child.keys[mid_idx + 1 :]
        full_child.keys = full_child.keys[:mid_idx]

        # Move half of children if not leaf
        if not full_child.is_leaf:
            # Cast needed: _refs is typed as List[Optional[Node]] in base class,
            # while slices below are List[BTreeNode]. Runtime types are correct.
            new_child._refs = cast(
                List[Optional[Node]], full_child.children[mid_idx + 1 :]
            )
            full_child._refs = cast(
                List[Optional[Node]], full_child.children[: mid_idx + 1]
            )
            # Update parent references
            for child in new_child.children:
                child._parent = new_child

        # Move middle key up to parent
        parent.insert_key(middle_key, index)

        # Add new child to parent
        parent.add_child(new_child, index + 1)

    def remove(self, key: Any) -> Any:
        """Remove and return a key from the tree.

        Parameters
        ----------
        key : Any
            Key to remove.

        Returns
        -------
        Any
            The removed key.

        Raises
        ------
        EmptyStructureError
            If tree is empty.
        ValueError
            If key is not found.

        Examples
        --------
        >>> tree = BTree()
        >>> tree.insert(10)
        >>> tree.insert(20)
        >>> tree.remove(10)
        10
        >>> tree.search(10)
        False

        Notes
        -----
        Time complexity: O(log n)
        """
        if self._root is None:
            raise EmptyStructureError("Cannot remove from empty tree")

        if not self.search(key):
            raise ValueError(f"Key {key} not found in tree")

        self._remove_from_node(self._root, key)
        self._size -= 1

        # If root is empty after deletion, make first child new root
        if len(self._root.keys) == 0:
            if not self._root.is_leaf and len(self._root.children) > 0:
                self._root = self._root.children[0]
            else:
                self._root = None

        return key

    def _remove_from_node(self, node: BTreeNode, key: Any) -> None:
        """Remove key from subtree rooted at node.

        Parameters
        ----------
        node : BTreeNode
            Root of subtree.
        key : Any
            Key to remove.
        """
        i = node.find_key_index(key)

        if i < len(node.keys) and node.keys[i] == key:
            # Key found in this node
            if node.is_leaf:
                node.remove_key(i)
            else:
                self._remove_from_internal(node, i)
        elif not node.is_leaf:
            # Key is in subtree
            is_in_last_child = i == len(node.keys)

            # Fill child if it has minimum keys
            if node.children[i].is_minimal():
                self._fill(node, i)

            # After filling, check if key moved up
            if is_in_last_child and i > len(node.keys):
                self._remove_from_node(node.children[i - 1], key)
            else:
                # Recompute index as it may have changed
                i = node.find_key_index(key)
                if i < len(node.keys) and node.keys[i] == key:
                    # Key moved up during fill
                    self._remove_from_internal(node, i)
                else:
                    self._remove_from_node(node.children[i], key)

    def _remove_from_internal(self, node: BTreeNode, idx: int) -> None:
        """Remove key at index from internal node.

        Parameters
        ----------
        node : BTreeNode
            Internal node.
        idx : int
            Index of key to remove.
        """
        key = node.keys[idx]

        if not node.children[idx].is_minimal():
            # Get predecessor from left child
            pred = self._get_predecessor(node, idx)
            node.keys[idx] = pred
            self._remove_from_node(node.children[idx], pred)
        elif not node.children[idx + 1].is_minimal():
            # Get successor from right child
            succ = self._get_successor(node, idx)
            node.keys[idx] = succ
            self._remove_from_node(node.children[idx + 1], succ)
        else:
            # Merge with sibling
            self._merge(node, idx)
            self._remove_from_node(node.children[idx], key)

    def _get_predecessor(self, node: BTreeNode, idx: int) -> Any:
        """Get predecessor key (rightmost in left subtree).

        Parameters
        ----------
        node : BTreeNode
            Parent node.
        idx : int
            Index of key.

        Returns
        -------
        Any
            Predecessor key.
        """
        current = node.children[idx]
        while not current.is_leaf:
            current = current.children[-1]
        return current.keys[-1]

    def _get_successor(self, node: BTreeNode, idx: int) -> Any:
        """Get successor key (leftmost in right subtree).

        Parameters
        ----------
        node : BTreeNode
            Parent node.
        idx : int
            Index of key.

        Returns
        -------
        Any
            Successor key.
        """
        current = node.children[idx + 1]
        while not current.is_leaf:
            current = current.children[0]
        return current.keys[0]

    def _fill(self, node: BTreeNode, idx: int) -> None:
        """Fill child at idx if it has minimum keys.

        Parameters
        ----------
        node : BTreeNode
            Parent node.
        idx : int
            Index of child to fill.
        """
        # If previous sibling has extra keys, borrow from it
        if idx != 0 and not node.children[idx - 1].is_minimal():
            self._borrow_from_prev(node, idx)
        # If next sibling has extra keys, borrow from it
        elif idx != len(node.children) - 1 and not node.children[idx + 1].is_minimal():
            self._borrow_from_next(node, idx)
        # Merge with sibling
        else:
            if idx != len(node.children) - 1:
                self._merge(node, idx)
            else:
                self._merge(node, idx - 1)

    def _borrow_from_prev(self, node: BTreeNode, child_idx: int) -> None:
        """Borrow key from previous sibling.

        Parameters
        ----------
        node : BTreeNode
            Parent node.
        child_idx : int
            Index of child that needs key.
        """
        child = node.children[child_idx]
        sibling = node.children[child_idx - 1]

        # Move parent key down to child
        child.insert_key(node.keys[child_idx - 1], 0)

        # Move sibling's last key up to parent
        node.keys[child_idx - 1] = sibling.keys[-1]
        sibling.remove_key(len(sibling.keys) - 1)

        # Move child pointer if not leaf
        if not child.is_leaf:
            child.add_child(sibling.children[-1], 0)
            sibling.remove_child(len(sibling.children) - 1)

    def _borrow_from_next(self, node: BTreeNode, child_idx: int) -> None:
        """Borrow key from next sibling.

        Parameters
        ----------
        node : BTreeNode
            Parent node.
        child_idx : int
            Index of child that needs key.
        """
        child = node.children[child_idx]
        sibling = node.children[child_idx + 1]

        # Move parent key down to child
        child.insert_key(node.keys[child_idx])

        # Move sibling's first key up to parent
        node.keys[child_idx] = sibling.keys[0]
        sibling.remove_key(0)

        # Move child pointer if not leaf
        if not child.is_leaf:
            child.add_child(sibling.children[0])
            sibling.remove_child(0)

    def _merge(self, node: BTreeNode, idx: int) -> None:
        """Merge child with its sibling.

        Parameters
        ----------
        node : BTreeNode
            Parent node.
        idx : int
            Index of key to pull down.
        """
        child = node.children[idx]
        sibling = node.children[idx + 1]

        # Pull key from parent and merge with right sibling
        child.insert_key(node.keys[idx])
        child.keys.extend(sibling.keys)

        # Copy child pointers
        if not child.is_leaf:
            for grandchild in sibling.children:
                child.add_child(grandchild)

        # Remove key from parent
        node.remove_key(idx)
        node.remove_child(idx + 1)

    def find_min(self) -> Any:
        """Find and return the minimum key.

        Returns
        -------
        Any
            The minimum key.

        Raises
        ------
        EmptyStructureError
            If tree is empty.

        Examples
        --------
        >>> tree = BTree()
        >>> tree.insert(10)
        >>> tree.insert(5)
        >>> tree.insert(20)
        >>> tree.find_min()
        5

        Notes
        -----
        Time complexity: O(log n)
        """
        if self._root is None:
            raise EmptyStructureError("Cannot find min in empty tree")

        current = self._root
        while not current.is_leaf:
            current = current.children[0]
        return current.keys[0]

    def find_max(self) -> Any:
        """Find and return the maximum key.

        Returns
        -------
        Any
            The maximum key.

        Raises
        ------
        EmptyStructureError
            If tree is empty.

        Examples
        --------
        >>> tree = BTree()
        >>> tree.insert(10)
        >>> tree.insert(5)
        >>> tree.insert(20)
        >>> tree.find_max()
        20

        Notes
        -----
        Time complexity: O(log n)
        """
        if self._root is None:
            raise EmptyStructureError("Cannot find max in empty tree")

        current = self._root
        while not current.is_leaf:
            current = current.children[-1]
        return current.keys[-1]

    def clear(self) -> None:
        """Remove all keys from the tree.

        Examples
        --------
        >>> tree = BTree()
        >>> tree.insert(10)
        >>> tree.insert(20)
        >>> tree.clear()
        >>> tree.is_empty()
        True

        Notes
        -----
        Time complexity: O(1)
        """
        self._root = None
        self._size = 0

    def inorder_traversal(self) -> Iterator[Any]:
        """Yield keys in sorted order (inorder traversal).

        Yields
        ------
        Any
            Keys in ascending order.

        Examples
        --------
        >>> tree = BTree()
        >>> for val in [10, 5, 20, 15, 25]:
        ...     tree.insert(val)
        >>> list(tree.inorder_traversal())
        [5, 10, 15, 20, 25]

        Notes
        -----
        Time complexity: O(n)
        """
        if self._root is not None:
            yield from self._inorder_recursive(self._root)

    def _inorder_recursive(self, node: BTreeNode) -> Iterator[Any]:
        """Inorder traversal helper.

        Parameters
        ----------
        node : BTreeNode
            Current node.

        Yields
        ------
        Any
            Keys in inorder.
        """
        n_keys = len(node.keys)

        for i in range(n_keys):
            # Visit left child
            if not node.is_leaf:
                yield from self._inorder_recursive(node.children[i])
            # Visit key
            yield node.keys[i]

        # Visit rightmost child (index = number of keys)
        if not node.is_leaf:
            yield from self._inorder_recursive(node.children[n_keys])

    def level_order_traversal(self) -> Iterator[Any]:
        """Yield keys level by level (breadth-first).

        Yields
        ------
        Any
            Keys in level order.

        Examples
        --------
        >>> tree = BTree(t=2)
        >>> for val in [10, 20, 5, 15]:
        ...     tree.insert(val)
        >>> list(tree.level_order_traversal())
        [10, 5, 15, 20]

        Notes
        -----
        Time complexity: O(n)
        """
        if self._root is None:
            return

        queue: deque[BTreeNode] = deque([self._root])
        while queue:
            current = queue.popleft()
            # Yield all keys in current node
            for key in current.keys:
                yield key
            # Add children to queue
            if not current.is_leaf:
                queue.extend(current.children)

    def __iter__(self) -> Iterator[Any]:
        """Iterate over keys in sorted order.

        Yields
        ------
        Any
            Keys in ascending order.

        Examples
        --------
        >>> tree = BTree()
        >>> for val in [10, 5, 20]:
        ...     tree.insert(val)
        >>> list(tree)
        [5, 10, 20]
        """
        return self.inorder_traversal()

    def __contains__(self, key: Any) -> bool:
        """Check if key is in tree.

        Parameters
        ----------
        key : Any
            Key to check.

        Returns
        -------
        bool
            True if key exists.

        Examples
        --------
        >>> tree = BTree()
        >>> tree.insert(10)
        >>> 10 in tree
        True
        >>> 20 in tree
        False
        """
        return self.search(key)

    def __repr__(self) -> str:
        """Return string representation.

        Returns
        -------
        str
            String representation.

        Examples
        --------
        >>> tree = BTree(t=3)
        >>> tree.insert(10)
        >>> repr(tree)
        'BTree(t=3, size=1)'
        """
        return f"BTree(t={self._t}, size={self._size})"

    def __str__(self) -> str:
        """Return string showing keys in sorted order.

        Returns
        -------
        str
            String representation.

        Examples
        --------
        >>> tree = BTree()
        >>> tree.insert(10)
        >>> tree.insert(5)
        >>> str(tree)
        'BTree: [5, 10]'
        """
        if self.is_empty():
            return "BTree: []"
        keys = ", ".join(str(key) for key in self.inorder_traversal())
        return f"BTree: [{keys}]"
