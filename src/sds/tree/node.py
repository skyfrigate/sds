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

"""Node classes for tree data structures.

This module provides node implementations specifically designed for tree
structures such as binary trees, binary search trees, AVL trees, and general trees.

Classes
-------
BinaryNode
    Node for binary trees with left and right child references.
TreeNode
    Node for general trees with variable number of children.

Examples
--------
Using BinaryNode:

>>> from sds.tree.node import BinaryNode
>>> root = BinaryNode(10)
>>> root.left = BinaryNode(5)
>>> root.right = BinaryNode(15)
>>> root.left.data
5

Using TreeNode:

>>> from sds.tree.node import TreeNode
>>> root = TreeNode("A")
>>> root.add_child(TreeNode("B"))
>>> root.add_child(TreeNode("C"))
>>> len(root.children)
2

Notes
-----
These nodes inherit from the abstract Node class in core.node and use
the _refs list internally to store references, exposing them through
specific properties (left, right, children).

See Also
--------
sds.core.node : Abstract base Node class.
sds.trees : Tree implementations using these nodes.
"""

from typing import Any, List, Optional

from ..core.node import Node

__all__ = ["AVLNode", "BinaryNode", "RedBlackNode", "TreeNode"]


class BinaryNode(Node):
    """A node for binary trees.

    Each node contains data and references to left child, right child, and
    optionally a parent node. This is the basic building block for binary trees,
    binary search trees, AVL trees, and other binary tree structures.

    Internally uses _refs[0] for left and _refs[1] for right.

    Parameters
    ----------
    data : Any
        The data to store in the node.
    left : BinaryNode or None, optional
        Reference to the left child node. Default is None.
    right : BinaryNode or None, optional
        Reference to the right child node. Default is None.
    parent : BinaryNode or None, optional
        Reference to the parent node. Default is None.

    Attributes
    ----------
    data : Any
        The data stored in the node (inherited from Node).
    left : BinaryNode or None
        Reference to the left child (property accessing _refs[0]).
    right : BinaryNode or None
        Reference to the right child (property accessing _refs[1]).
    parent : Node or None
        Reference to parent node (inherited from Node).

    Examples
    --------
    Create a simple binary node:

    >>> node = BinaryNode(42)
    >>> node.data
    42
    >>> node.left is None
    True
    >>> node.right is None
    True

    Create a binary tree structure:

    >>> root = BinaryNode(10)
    >>> root.left = BinaryNode(5)
    >>> root.right = BinaryNode(15)
    >>> root.left.data
    5
    >>> root.right.data
    15

    With automatic parent maintenance:

    >>> root = BinaryNode(10)
    >>> left_child = BinaryNode(5)
    >>> root.left = left_child
    >>> left_child.parent is root
    True

    Check if node is a leaf:

    >>> node = BinaryNode(42)
    >>> node.is_leaf()
    True
    >>> node.left = BinaryNode(10)
    >>> node.is_leaf()
    False

    Notes
    -----
    This class uses __slots__ for memory efficiency. When setting left or
    right children, the parent reference of the child is automatically
    updated to maintain consistency.

    See Also
    --------
    TreeNode : Node with multiple children for general trees.
    sds.core.node.Node : Abstract base class.
    """

    __slots__ = ()  # No additional slots, inherits from Node

    def __init__(
        self,
        data: Any,
        left: Optional["BinaryNode"] = None,
        right: Optional["BinaryNode"] = None,
        parent: Optional["BinaryNode"] = None,
    ):
        """Initialize a new binary node.

        Parameters
        ----------
        data : Any
            The data to store in the node.
        left : BinaryNode or None, optional
            The left child node. Default is None.
        right : BinaryNode or None, optional
            The right child node. Default is None.
        parent : BinaryNode or None, optional
            The parent node. Default is None.
        """
        super().__init__(data)
        self._parent = parent

        # Initialize _refs with two slots: [left, right]
        self._refs.append(None)
        self._refs.append(None)

        # Use setters to maintain parent consistency
        if left is not None:
            self.left = left
        if right is not None:
            self.right = right

    @property
    def left(self) -> Optional["BinaryNode"]:
        """Get or set the left child node.

        Returns
        -------
        BinaryNode or None
            The left child node, or None if no left child.

        Examples
        --------
        >>> root = BinaryNode(10)
        >>> left = BinaryNode(5)
        >>> root.left = left
        >>> root.left.data
        5
        >>> left.parent is root
        True

        Notes
        -----
        This property accesses _refs[0]. Setting this property automatically
        updates the child's parent reference.
        """
        return self._refs[0] if len(self._refs) > 0 else None  # type: ignore[return-value]

    @left.setter
    def left(self, node: Optional["BinaryNode"]) -> None:
        """Set the left child node.

        Parameters
        ----------
        node : BinaryNode or None
            The node to set as left child, or None to remove left child.

        Notes
        -----
        This setter automatically updates the parent reference of the child
        node to maintain bidirectional consistency.
        """

        self._refs[0] = node

        if node is not None:
            node._parent = self

    @property
    def right(self) -> Optional["BinaryNode"]:
        """Get or set the right child node.

        Returns
        -------
        BinaryNode or None
            The right child node, or None if no right child.

        Examples
        --------
        >>> root = BinaryNode(10)
        >>> right = BinaryNode(15)
        >>> root.right = right
        >>> root.right.data
        15
        >>> right.parent is root
        True

        Notes
        -----
        This property accesses _refs[1]. Setting this property automatically
        updates the child's parent reference.
        """
        return self._refs[1] if len(self._refs) > 1 else None  # type: ignore[return-value]

    @right.setter
    def right(self, node: Optional["BinaryNode"]) -> None:
        """Set the right child node.

        Parameters
        ----------
        node : BinaryNode or None
            The node to set as right child, or None to remove right child.

        Notes
        -----
        This setter automatically updates the parent reference of the child
        node to maintain bidirectional consistency.
        """

        self._refs[1] = node

        if node is not None:
            node._parent = self

    def is_leaf(self) -> bool:
        """Check if this node is a leaf (has no children).

        Returns
        -------
        bool
            True if the node has no left or right children, False otherwise.

        Examples
        --------
        >>> node = BinaryNode(42)
        >>> node.is_leaf()
        True
        >>> node.left = BinaryNode(10)
        >>> node.is_leaf()
        False

        Notes
        -----
        Time complexity: O(1)
        """
        return self.left is None and self.right is None

    def __repr__(self) -> str:
        """Return a detailed string representation of the node.

        Returns
        -------
        str
            String representation in the form "BinaryNode(data)".

        Examples
        --------
        >>> node = BinaryNode(42)
        >>> repr(node)
        'BinaryNode(42)'
        >>> node = BinaryNode("hello")
        >>> repr(node)
        "BinaryNode('hello')"
        """
        return f"BinaryNode({self._data!r})"

    def __str__(self) -> str:
        """Return a simple string representation of the node's data.

        Returns
        -------
        str
            String representation of the data.

        Examples
        --------
        >>> node = BinaryNode(42)
        >>> str(node)
        '42'
        >>> print(node)
        42
        """
        return str(self._data)


class TreeNode(Node):
    """A node for general trees.

    Each node contains data, a list of children nodes, and optionally a parent
    node. This is the basic building block for general trees, file systems,
    organizational hierarchies, and other tree structures with arbitrary branching.

    The _refs list directly stores the children list.

    Parameters
    ----------
    data : Any
        The data to store in the node.
    parent : TreeNode or None, optional
        Reference to the parent node. Default is None.

    Attributes
    ----------
    data : Any
        The data stored in the node (inherited from Node).
    children : List[TreeNode]
        List of child nodes (property accessing _refs directly).
    parent : Node or None
        Reference to parent node (inherited from Node).

    Examples
    --------
    Create a simple tree node:

    >>> node = TreeNode("root")
    >>> node.data
    'root'
    >>> node.children
    []
    >>> node.parent is None
    True

    Build a tree structure:

    >>> root = TreeNode("A")
    >>> child1 = TreeNode("B")
    >>> child2 = TreeNode("C")
    >>> root.add_child(child1)
    >>> root.add_child(child2)
    >>> len(root.children)
    2
    >>> child1.parent is root
    True

    Remove a child:

    >>> root.remove_child(child1)
    >>> len(root.children)
    1
    >>> child1.parent is None
    True

    Check if node is a leaf:

    >>> child2.is_leaf()
    True
    >>> root.is_leaf()
    False

    Notes
    -----
    This class uses __slots__ for memory efficiency. The children list is
    managed internally (stored in _refs directly) and should only be modified
    through add_child() and remove_child() methods to maintain parent-child
    consistency.

    See Also
    --------
    BinaryNode : Node with exactly two children (left and right).
    sds.core.node.Node : Abstract base class.
    """

    __slots__ = ()  # No additional slots, inherits from Node

    def __init__(self, data: Any, parent: Optional["TreeNode"] = None):
        """Initialize a new tree node.

        Parameters
        ----------
        data : Any
            The data to store in the node.
        parent : TreeNode or None, optional
            The parent node. Default is None.
        """
        super().__init__(data)
        self._parent = parent
        # _refs IS the children list for TreeNode

    @property
    def children(self) -> List["TreeNode"]:
        """Get the list of child nodes.

        Returns
        -------
        List[TreeNode]
            The list of child nodes. Returns empty list if no children.

        Examples
        --------
        >>> root = TreeNode("A")
        >>> root.children
        []
        >>> root.add_child(TreeNode("B"))
        >>> len(root.children)
        1

        Notes
        -----
        This property returns the internal _refs list directly. Use
        add_child() and remove_child() methods to modify children to maintain
        consistency.

        Time complexity: O(1)
        """
        # Cast needed for mypy - _refs is List[Node] but we know it's
        # List[TreeNode] for TreeNode instances
        return self._refs  # type: ignore[return-value]

    def add_child(self, child: "TreeNode") -> None:
        """Add a child node to this node.

        Parameters
        ----------
        child : TreeNode
            The node to add as a child.

        Examples
        --------
        >>> root = TreeNode("A")
        >>> child = TreeNode("B")
        >>> root.add_child(child)
        >>> child in root.children
        True
        >>> child.parent is root
        True

        Notes
        -----
        This method automatically updates the parent reference of the child
        to maintain bidirectional consistency. If the child is already in the
        children list, it is not added again.

        Time complexity: O(n) for checking if child exists, O(1) for adding
        """
        if child not in self._refs:
            self._refs.append(child)
            child._parent = self

    def remove_child(self, child: "TreeNode") -> None:
        """Remove a child node from this node.

        Parameters
        ----------
        child : TreeNode
            The node to remove from children.

        Raises
        ------
        ValueError
            If the child is not in the children list.

        Examples
        --------
        >>> root = TreeNode("A")
        >>> child = TreeNode("B")
        >>> root.add_child(child)
        >>> root.remove_child(child)
        >>> child not in root.children
        True
        >>> child.parent is None
        True

        Notes
        -----
        This method automatically clears the parent reference of the removed
        child to maintain consistency.

        Time complexity: O(n) for finding and removing
        """
        self._refs.remove(child)
        child._parent = None

    def is_leaf(self) -> bool:
        """Check if this node is a leaf (has no children).

        Returns
        -------
        bool
            True if the node has no children, False otherwise.

        Examples
        --------
        >>> node = TreeNode(42)
        >>> node.is_leaf()
        True
        >>> node.add_child(TreeNode(10))
        >>> node.is_leaf()
        False

        Notes
        -----
        Time complexity: O(1)
        """
        return len(self._refs) == 0

    def __repr__(self) -> str:
        """Return a detailed string representation of the node.

        Returns
        -------
        str
            String representation in the form "TreeNode(data)".

        Examples
        --------
        >>> node = TreeNode(42)
        >>> repr(node)
        'TreeNode(42)'
        >>> node = TreeNode("hello")
        >>> repr(node)
        "TreeNode('hello')"
        """
        return f"TreeNode({self._data!r})"

    def __str__(self) -> str:
        """Return a simple string representation of the node's data.

        Returns
        -------
        str
            String representation of the data.

        Examples
        --------
        >>> node = TreeNode(42)
        >>> str(node)
        '42'
        >>> print(node)
        42
        """
        return str(self._data)


class AVLNode(BinaryNode):
    """A node for AVL trees with height tracking.

    Extends BinaryNode to include a height attribute for efficient
    balance factor calculation.

    Parameters
    ----------
    data : Any
        The data to store in the node.
    left : AVLNode or None, optional
        Reference to the left child node. Default is None.
    right : AVLNode or None, optional
        Reference to the right child node. Default is None.
    parent : AVLNode or None, optional
        Reference to the parent node. Default is None.

    Attributes
    ----------
    height : int
        The height of the subtree rooted at this node.

    Examples
    --------
    >>> node = AVLNode(10)
    >>> node.height
    0
    >>> node.left = AVLNode(5)
    >>> node.height = 1
    """

    __slots__ = ("height",)

    def __init__(
        self,
        data: Any,
        left: Optional["AVLNode"] = None,
        right: Optional["AVLNode"] = None,
        parent: Optional["AVLNode"] = None,
    ):
        """Initialize an AVL node with height tracking."""
        super().__init__(data, left, right, parent)
        self.height: int = 0


class RedBlackNode(BinaryNode):
    """A node for Red-Black trees with color attribute.

    Red-Black trees use node coloring to maintain balance. Each node
    is either RED or BLACK, and the tree maintains specific color
    properties to ensure logarithmic height.

    Parameters
    ----------
    data : Any
        The data to store in the node.
    color : str, optional
        The color of the node ("RED" or "BLACK"). Default is "RED".
    left : RedBlackNode or None, optional
        Reference to the left child. Default is None.
    right : RedBlackNode or None, optional
        Reference to the right child. Default is None.
    parent : RedBlackNode or None, optional
        Reference to the parent. Default is None.

    Attributes
    ----------
    color : str
        The color of the node ("RED" or "BLACK").

    Examples
    --------
    >>> node = RedBlackNode(10)
    >>> node.color
    'RED'
    >>> node.color = 'BLACK'
    """

    __slots__ = ("color",)

    def __init__(
        self,
        data: Any,
        color: str = "RED",
        left: Optional["RedBlackNode"] = None,
        right: Optional["RedBlackNode"] = None,
        parent: Optional["RedBlackNode"] = None,
    ):
        """Initialize a Red-Black node."""
        super().__init__(data, left, right, parent)
        self.color: str = color
