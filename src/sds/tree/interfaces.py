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

from abc import abstractmethod
from typing import Any, Iterator, Optional

from ..core.interfaces import Collection
from .node import BinaryNode

__all__ = ["AbstractTree", "AbstractBinaryTree"]


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
    inorder_traversal()
        Return an iterator for inorder traversal (left-root-right).
    preorder_traversal()
        Return an iterator for preorder traversal (root-left-right).
    postorder_traversal()
        Return an iterator for postorder traversal (left-right-root).
    level_order_traversal()
        Return an iterator for level-order traversal (BFS).

    Examples
    --------
    >>> tree = BinarySearchTree()
    >>> tree.insert(10)
    >>> tree.insert(5)
    >>> tree.insert(15)
    >>> list(tree.inorder_traversal())
    [5, 10, 15]

    Notes
    -----
    Binary trees have specific traversal methods that are not
    applicable to general trees.

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

    @abstractmethod
    def inorder_traversal(self) -> Iterator[Any]:
        """Return an iterator for inorder traversal (left-root-right).

        In inorder traversal, we visit:
        1. Left subtree
        2. Root
        3. Right subtree

        For BST, this yields elements in sorted order.

        Yields
        ------
        Any
            Items from the tree in inorder.

        Examples
        --------
        >>> tree = BinarySearchTree()
        >>> tree.insert(10)
        >>> tree.insert(5)
        >>> tree.insert(15)
        >>> list(tree.inorder_traversal())
        [5, 10, 15]

        Notes
        -----
        Time complexity: O(n)
        Space complexity: O(h) where h is height (recursion stack)

        See Also
        --------
        preorder_traversal : Root-left-right traversal.
        postorder_traversal : Left-right-root traversal.
        """
        pass

    @abstractmethod
    def preorder_traversal(self) -> Iterator[Any]:
        """Return an iterator for preorder traversal (root-left-right).

        In preorder traversal, we visit:
        1. Root
        2. Left subtree
        3. Right subtree

        Useful for creating a copy of the tree.

        Yields
        ------
        Any
            Items from the tree in preorder.

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
        Space complexity: O(h) where h is height

        See Also
        --------
        inorder_traversal : Left-root-right traversal.
        """
        pass

    @abstractmethod
    def postorder_traversal(self) -> Iterator[Any]:
        """Return an iterator for postorder traversal (left-right-root).

        In postorder traversal, we visit:
        1. Left subtree
        2. Right subtree
        3. Root

        Useful for deleting the tree (delete children before parent).

        Yields
        ------
        Any
            Items from the tree in postorder.

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
        Space complexity: O(h) where h is height

        See Also
        --------
        inorder_traversal : Left-root-right traversal.
        """
        pass

    @abstractmethod
    def level_order_traversal(self) -> Iterator[Any]:
        """Return an iterator for level-order traversal (BFS).

        Level-order traversal visits nodes level by level, from left
        to right at each level. Also known as breadth-first search.

        Yields
        ------
        Any
            Items from the tree level by level.

        Examples
        --------
        >>> tree = BinaryTree()
        >>> tree.insert(10)
        >>> tree.insert(5)
        >>> tree.insert(15)
        >>> list(tree.level_order_traversal())
        [10, 5, 15]

        Notes
        -----
        Time complexity: O(n)
        Space complexity: O(w) where w is maximum width of tree

        See Also
        --------
        inorder_traversal : Depth-first inorder traversal.
        """
        pass
