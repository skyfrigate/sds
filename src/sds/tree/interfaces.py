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

"""Abstract base classes for tree data structures.

This module provides the abstract base classes that define the interfaces
for all tree implementations in the sds library. These interfaces ensure
a consistent API across different tree types.

The hierarchy is:
- Collection: Base interface (from core)
- AbstractTree: Base interface for all trees
- AbstractBinaryTree: Interface for binary trees

Classes
-------
AbstractTree
    Abstract base class for all tree structures.
AbstractBinaryTree
    Abstract base class for binary tree structures.

Examples
--------
Implementing a custom tree:

>>> from sds.tree.interfaces import AbstractBinaryTree
>>> class MyBinaryTree(AbstractBinaryTree):
...     def __init__(self):
...         super().__init__()
...         self._root = None
...         self._size = 0
...     # Implement all abstract methods...

Notes
-----
All classes in this module are abstract base classes and cannot be
instantiated directly. They must be subclassed with concrete
implementations of all abstract methods.

See Also
--------
sds.core.interfaces : Core collection interfaces.
sds.tree.binary_tree : Concrete binary tree implementations.
"""

import warnings
from abc import abstractmethod
from typing import Any, Iterator, List, Optional, Tuple

from ..core.interfaces import Collection
from .node import BinaryNode


def _warn_traversal_deprecated(method: str, replacement: str) -> None:
    """Emit the DeprecationWarning shared by the four traversal methods.

    ``stacklevel=3`` makes the warning point at the caller of the
    deprecated method, not at this helper or at the method itself.
    """
    warnings.warn(
        f"{method}() is deprecated since 0.7.0 and will be removed in 1.0.0; "
        f"use sds.algorithms.tree_algorithms.{replacement}(tree) instead.",
        DeprecationWarning,
        stacklevel=3,
    )


__all__ = ["AbstractTree", "AbstractBinaryTree", "AbstractSegmentTree"]


class AbstractTree(Collection):
    """Abstract base class for all tree structures.

    Defines the common interface that all tree types must implement.
    This includes operations for tree manipulation, traversal, and queries.

    All concrete tree implementations should inherit from this class
    or one of its subclasses.

    Attributes
    ----------
    size : int
        The number of nodes in the tree (read-only property).

    Methods
    -------
    height()
        Return the height of the tree.
    insert(item)
        Insert an item into the tree.
    remove(item)
        Remove an item from the tree.
    search(item)
        Search for an item in the tree.
    clear()
        Remove all nodes from the tree.

    Examples
    --------
    Any concrete tree can be used polymorphically:

    >>> def process_tree(tree: AbstractTree):
    ...     tree.insert(10)
    ...     return tree.height()

    Notes
    -----
    This class is abstract and cannot be instantiated directly.
    Concrete subclasses must implement all abstract methods.

    See Also
    --------
    AbstractBinaryTree : Interface for binary trees.
    Collection : Base interface for all collections.
    """

    def __init__(self) -> None:
        """Initialize the abstract tree.

        Subclasses should call this via super().__init__() and then
        initialize their own internal attributes.
        """
        self._size = 0

    @property
    def size(self) -> int:
        """Get the number of nodes in the tree.

        Returns
        -------
        int
            The number of nodes currently in the tree.

        Examples
        --------
        >>> tree = BinaryTree()
        >>> tree.size
        0
        >>> tree.insert(10)
        >>> tree.size
        1

        Notes
        -----
        Time complexity: O(1)

        See Also
        --------
        __len__ : Returns the same value.
        """
        return self._size

    @abstractmethod
    def height(self) -> int:
        """Return the height of the tree.

        The height is the length of the longest path from root to a leaf.
        An empty tree has height -1, a tree with only root has height 0.

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
        Time complexity typically O(n) for unbalanced trees,
        O(log n) for balanced trees if height is cached.

        See Also
        --------
        size : Get the number of nodes.
        """
        pass

    @abstractmethod
    def insert(self, item: Any) -> None:
        """Insert an item into the tree.

        The specific behavior depends on the concrete tree implementation.
        For example, BST maintains order, while simple binary tree may not.

        Parameters
        ----------
        item : Any
            The item to insert.

        Examples
        --------
        >>> tree = BinaryTree()
        >>> tree.insert(10)
        >>> tree.insert(5)
        >>> len(tree)
        2

        Notes
        -----
        Time complexity varies by implementation:
        - Simple binary tree: O(1) to O(n)
        - BST: O(log n) average, O(n) worst
        - Balanced trees: O(log n) guaranteed

        See Also
        --------
        remove : Remove an item from the tree.
        search : Search for an item.
        """
        pass

    @abstractmethod
    def remove(self, item: Any) -> Any:
        """Remove and return an item from the tree.

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
        >>> tree.remove(5)
        5

        Notes
        -----
        Time complexity varies by implementation.

        See Also
        --------
        insert : Insert an item into the tree.
        """
        pass

    @abstractmethod
    def search(self, item: Any) -> bool:
        """Search for an item in the tree.

        Parameters
        ----------
        item : Any
            The item to search for.

        Returns
        -------
        bool
            True if the item is found, False otherwise.

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
        Time complexity varies by implementation:
        - Simple binary tree: O(n)
        - BST: O(log n) average, O(n) worst
        - Balanced trees: O(log n) guaranteed

        See Also
        --------
        __contains__ : Alternative way to check membership.
        """
        pass

    def __len__(self) -> int:
        """Return the number of nodes in the tree.

        Returns
        -------
        int
            The number of nodes.

        Examples
        --------
        >>> tree = BinaryTree()
        >>> len(tree)
        0
        >>> tree.insert(10)
        >>> len(tree)
        1

        Notes
        -----
        Time complexity: O(1)
        """
        return self._size

    def is_empty(self) -> bool:
        """Return True if the tree is empty.

        Returns
        -------
        bool
            True if the tree contains no nodes, False otherwise.

        Examples
        --------
        >>> tree = BinaryTree()
        >>> tree.is_empty()
        True
        >>> tree.insert(10)
        >>> tree.is_empty()
        False

        Notes
        -----
        Time complexity: O(1)
        """
        return self._size == 0


class AbstractBinaryTree(AbstractTree):
    """Abstract base class for binary tree structures.

    Extends AbstractTree with operations specific to binary trees,
    where each node has at most two children (left and right).

    Attributes
    ----------
    root : BinaryNode or None
        The root node of the tree (read-only property).

    Methods
    -------
    children(node)
        Return the real ``(left, right)`` children of a node.
    inorder_traversal()
        Deprecated since 0.7.0: use ``sds.algorithms.tree_algorithms.inorder``.
    preorder_traversal()
        Deprecated since 0.7.0: use ``sds.algorithms.tree_algorithms.preorder``.
    postorder_traversal()
        Deprecated since 0.7.0: use ``sds.algorithms.tree_algorithms.postorder``.
    level_order_traversal()
        Deprecated since 0.7.0: use ``sds.algorithms.tree_algorithms.level_order``.

    Examples
    --------
    >>> tree = BinarySearchTree()
    >>> tree.insert(10)
    >>> tree.insert(5)
    >>> tree.insert(15)
    >>> list(tree)
    [5, 10, 15]

    Notes
    -----
    Traversal orders (inorder, preorder, postorder, level order) are
    algorithms and live in :mod:`sds.algorithms.tree_algorithms`, which
    walks any binary tree through :meth:`root` and :meth:`children`.

    See Also
    --------
    AbstractTree : Base interface for all trees.
    BinaryTree : Simple binary tree implementation.
    """

    def __init__(self) -> None:
        """Initialize the abstract binary tree."""
        super().__init__()
        self._root: Optional[BinaryNode] = None

    @property
    def root(self) -> Optional[BinaryNode]:
        """Get the root node of the tree.

        Returns
        -------
        BinaryNode or None
            The root node, or None if the tree is empty.

        Examples
        --------
        >>> tree = BinaryTree()
        >>> tree.root is None
        True
        >>> tree.insert(10)
        >>> tree.root.data
        10

        Notes
        -----
        This property is read-only. To modify the tree, use
        insert() and remove() methods.
        """
        return self._root

    def children(
        self, node: BinaryNode
    ) -> Tuple[Optional[BinaryNode], Optional[BinaryNode]]:
        """Return the real ``(left, right)`` children of a node.

        This is the navigation primitive algorithms use to walk a binary
        tree without knowing how a given implementation stores absent
        children. A missing child is always reported as ``None``, even when
        the implementation represents it with a sentinel node internally
        (as :class:`~sds.tree.RedBlackTree` does).

        Parameters
        ----------
        node : BinaryNode
            A node of this tree.

        Returns
        -------
        tuple of (BinaryNode or None, BinaryNode or None)
            The left and right children, ``None`` where absent.

        Examples
        --------
        >>> from sds.tree import BinarySearchTree
        >>> bst = BinarySearchTree()
        >>> for value in (10, 5):
        ...     bst.insert(value)
        >>> left, right = bst.children(bst.root)
        >>> left.data, right
        (5, None)

        Notes
        -----
        Time complexity: O(1)

        Subclasses that use sentinel nodes must override this method so
        that sentinels never leak out of the structure (#89).
        """
        return node.left, node.right

    def inorder_traversal(self) -> Iterator[Any]:
        """Return an iterator over the items in inorder (left, root, right).

        .. deprecated:: 0.7.0
            Traversals are algorithms and moved to
            :func:`sds.algorithms.tree_algorithms.inorder`, which takes the
            tree as argument: ``inorder(tree)``. This method will be removed
            in 1.0.0 (#89).

        For a binary search tree, this yields the items in ascending order.

        Yields
        ------
        Any
            The items of the tree, in inorder.

        Warns
        -----
        DeprecationWarning
            On every call, when the method is called, not when the iterator
            is first advanced.

        Notes
        -----
        Time complexity: O(n)
        """
        _warn_traversal_deprecated("inorder_traversal", "inorder")
        from ..algorithms.tree_algorithms import inorder

        return inorder(self)

    def preorder_traversal(self) -> Iterator[Any]:
        """Return an iterator over the items in preorder (root, left, right).

        .. deprecated:: 0.7.0
            Traversals are algorithms and moved to
            :func:`sds.algorithms.tree_algorithms.preorder`, which takes the
            tree as argument: ``preorder(tree)``. This method will be removed
            in 1.0.0 (#89).

        Yields
        ------
        Any
            The items of the tree, in preorder.

        Warns
        -----
        DeprecationWarning
            On every call, when the method is called, not when the iterator
            is first advanced.

        Notes
        -----
        Time complexity: O(n)
        """
        _warn_traversal_deprecated("preorder_traversal", "preorder")
        from ..algorithms.tree_algorithms import preorder

        return preorder(self)

    def postorder_traversal(self) -> Iterator[Any]:
        """Return an iterator over the items in postorder (left, right, root).

        .. deprecated:: 0.7.0
            Traversals are algorithms and moved to
            :func:`sds.algorithms.tree_algorithms.postorder`, which takes the
            tree as argument: ``postorder(tree)``. This method will be removed
            in 1.0.0 (#89).

        Yields
        ------
        Any
            The items of the tree, in postorder.

        Warns
        -----
        DeprecationWarning
            On every call, when the method is called, not when the iterator
            is first advanced.

        Notes
        -----
        Time complexity: O(n)
        """
        _warn_traversal_deprecated("postorder_traversal", "postorder")
        from ..algorithms.tree_algorithms import postorder

        return postorder(self)

    def level_order_traversal(self) -> Iterator[Any]:
        """Return an iterator over the items in level order (breadth-first).

        .. deprecated:: 0.7.0
            Traversals are algorithms and moved to
            :func:`sds.algorithms.tree_algorithms.level_order`, which takes the
            tree as argument: ``level_order(tree)``. This method will be removed
            in 1.0.0 (#89).

        Yields
        ------
        Any
            The items of the tree, in level order.

        Warns
        -----
        DeprecationWarning
            On every call, when the method is called, not when the iterator
            is first advanced.

        Notes
        -----
        Time complexity: O(n)
        """
        _warn_traversal_deprecated("level_order_traversal", "level_order")
        from ..algorithms.tree_algorithms import level_order

        return level_order(self)


class AbstractSegmentTree(Collection):
    """Abstract base class for segment tree structures.

    Segment trees are data structures for efficient range queries on arrays.
    This abstract class defines the interface that all segment tree
    implementations must provide.

    A segment tree supports:
    - Range queries (sum, min, max, etc.) in O(log n)
    - Point updates in O(log n)
    - Array-like access to underlying data

    Attributes
    ----------
    size : int
        The size of the underlying array (read-only property).

    Methods
    -------
    query(left, right)
        Query the result for a range.
    update(index, value)
        Update a single element.
    get(index)
        Get value at index.
    to_array()
        Get the current array representation.

    Examples
    --------
    Concrete implementations must provide all abstract methods:

    >>> class MySegmentTree(AbstractSegmentTree):
    ...     def __init__(self, arr):
    ...         self._arr = arr
    ...         self._size = len(arr)
    ...     def query(self, left, right):
    ...         return sum(self._arr[left:right+1])
    ...     # ... other methods

    Notes
    -----
    All segment tree implementations should maintain:
    - O(log n) query time
    - O(log n) update time
    - O(n) space complexity

    See Also
    --------
    SegmentTree : Concrete segment tree implementation.
    Collection : Base interface for all collections.
    """

    def __init__(self) -> None:
        """Initialize abstract segment tree."""
        self._size = 0

    @property
    @abstractmethod
    def size(self) -> int:
        """Get the size of the underlying array.

        Returns
        -------
        int
            Size of the array.
        """
        pass

    @abstractmethod
    def query(self, left: int, right: int) -> Any:
        """Query the result for a range [left, right].

        Parameters
        ----------
        left : int
            Start index of the range (inclusive).
        right : int
            End index of the range (inclusive).

        Returns
        -------
        Any
            Result of the operation on the range.

        Raises
        ------
        InvalidOperationError
            If range is invalid.

        Notes
        -----
        Time complexity: O(log n)
        """
        pass

    @abstractmethod
    def update(self, index: int, value: Any) -> None:
        """Update a single element in the array.

        Parameters
        ----------
        index : int
            Index of the element to update.
        value : Any
            New value.

        Raises
        ------
        InvalidOperationError
            If index is out of bounds.

        Notes
        -----
        Time complexity: O(log n)
        """
        pass

    @abstractmethod
    def get(self, index: int) -> Any:
        """Get the value at a specific index.

        Parameters
        ----------
        index : int
            Index to query.

        Returns
        -------
        Any
            Value at the index.

        Raises
        ------
        InvalidOperationError
            If index is out of bounds.

        Notes
        -----
        Time complexity: O(1)
        """
        pass

    @abstractmethod
    def to_array(self) -> List[Any]:
        """Get the current array representation.

        Returns
        -------
        List[Any]
            Copy of the underlying array.

        Notes
        -----
        Time complexity: O(n)
        """
        pass

    # Override __getitem__ and __setitem__ with concrete implementations
    def __getitem__(self, index: int) -> Any:
        """Get value at index using array notation.

        Parameters
        ----------
        index : int
            Index to access.

        Returns
        -------
        Any
            Value at the index.
        """
        return self.get(index)

    def __setitem__(self, index: int, value: Any) -> None:
        """Update value at index using array notation.

        Parameters
        ----------
        index : int
            Index to update.
        value : Any
            New value.
        """
        self.update(index, value)
