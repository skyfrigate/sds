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
structures such as binary trees, binary search trees, AVL trees, and general
trees.

Classes
-------
BinaryNode
    Node for binary trees with left and right child references.
TreeNode
    Node for general trees with variable number of children.
BTreeNode
    Node for B-Trees with multiple keys and children (inherits from TreeNode).
TrieNode
    Node for Trie structures with character-indexed children.
AVLNode
    Node for AVL trees with height tracking.
RedBlackNode
    Node for Red-Black trees with color attribute.

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

Create a B-Tree node:

>>> from sds.tree.node import BTreeNode
>>> node = BTreeNode(t=3)
>>> node.keys = [10, 20, 30]
>>> node.is_leaf
True
>>> node.is_full()
False


See Also
--------
sds.core.node : Abstract base Node class.
sds.trees : Tree implementations using these nodes.
"""

from typing import Any, Dict, List, Optional

from ..core import Node

__all__ = [
    "AVLNode",
    "BinaryNode",
    "BTreeNode",
    "RedBlackNode",
    "TreeNode",
    "TrieNode",
]


class BinaryNode(Node):
    """A node for binary trees.

    Each node contains data and references to left child, right child, and
    optionally a parent node. This is the basic building block for binary
    trees, binary search trees, AVL trees, and other binary tree structures.

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
    ) -> None:
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
        if len(self._refs) > 0:
            # Type narrowing for mypy
            result: Optional[Node] = self._refs[0]
            return result  # type: ignore[return-value]
        return None

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
        if len(self._refs) > 1:
            # Type narrowing for mypy
            result: Optional[Node] = self._refs[1]
            return result  # type: ignore[return-value]
        return None

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

    Each node contains data, a list of children nodes, and optionally a
    parent node. This is the basic building block for general trees, file
    systems, organizational hierarchies, and other tree structures with
    arbitrary branching.

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
    managed internally (stored in _refs directly) and should only be
    modified through add_child() and remove_child() methods to maintain
    parent-child consistency.

    See Also
    --------
    BinaryNode : Node with exactly two children (left and right).
    BTreeNode : Specialization for B-Trees with multiple keys.
    sds.core.node.Node : Abstract base class.
    """

    __slots__ = ()  # No additional slots, inherits from Node

    def __init__(self, data: Any, parent: Optional["TreeNode"] = None) -> None:
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
        add_child() and remove_child() methods to modify children to
        maintain consistency.

        Time complexity: O(1)
        """
        # Cast needed for mypy - _refs is List[Optional[Node]] but we know
        # it contains List[TreeNode] for TreeNode instances
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
        to maintain bidirectional consistency. If the child is already in
        the children list, it is not added again.

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


class TrieNode(Node):
    """Node for Trie (prefix tree) structure.

    A Trie node maps characters to child nodes and tracks whether it marks
    the end of a valid word. Each node can have multiple children, indexed
    by character.

    The children are stored in a dictionary mapping characters to TrieNode
    objects, allowing O(1) access to any child by character.

    This is fundamentally different from TreeNode's list-based children,
    so TrieNode inherits directly from Node rather than from TreeNode.

    Parameters
    ----------
    None

    Attributes
    ----------
    children : Dict[str, TrieNode]
        Dictionary mapping characters to child nodes (accessed via property).
    is_end_of_word : bool
        True if this node marks the end of a valid word.

    Examples
    --------
    >>> node = TrieNode()
    >>> node.is_end_of_word = False
    >>> node.children['a'] = TrieNode()
    >>> 'a' in node.children
    True

    >>> root = TrieNode()
    >>> root.children['c'] = TrieNode()
    >>> root.children['c'].children['a'] = TrieNode()
    >>> root.children['c'].children['a'].children['t'] = TrieNode()
    >>> root.children['c'].children['a'].children['t'].is_end_of_word = True

    Notes
    -----
    This class uses __slots__ for memory efficiency.
    Unlike other Node types, Trie nodes use a dictionary for children
    rather than a list, as they need character-based indexing.

    The inherited _refs list is not used in TrieNode.

    See Also
    --------
    Trie : Trie implementation using this node type.
    Node : Abstract base class.
    TreeNode : List-based children for general trees.
    """

    __slots__ = ("is_end_of_word", "_children_dict")

    def __init__(self) -> None:
        """Initialize a Trie node.

        Creates an empty node with no children and not marking end of word.
        """
        # Trie nodes don't have single data value
        super().__init__(data=None)
        self.is_end_of_word: bool = False
        self._children_dict: Dict[str, "TrieNode"] = {}
        # Note: _refs from Node is not used in TrieNode

    @property
    def children(self) -> Dict[str, "TrieNode"]:
        """Get the dictionary of child nodes.

        Returns
        -------
        Dict[str, TrieNode]
            Dictionary mapping characters to child nodes.

        Examples
        --------
        >>> node = TrieNode()
        >>> node.children['a'] = TrieNode()
        >>> len(node.children)
        1
        >>> 'a' in node.children
        True

        Notes
        -----
        This property provides direct access to the children dictionary.
        Modifications to the returned dictionary affect the node.

        Time complexity: O(1)
        """
        return self._children_dict

    def __repr__(self) -> str:
        """Return detailed string representation.

        Returns
        -------
        str
            String representation showing children count and end status.

        Examples
        --------
        >>> node = TrieNode()
        >>> node.children['a'] = TrieNode()
        >>> node.is_end_of_word = True
        >>> repr(node)
        'TrieNode(children=1, is_end=True)'
        """
        return (
            f"TrieNode(children={len(self.children)}, " f"is_end={self.is_end_of_word})"
        )

    def __str__(self) -> str:
        """Return simple string representation.

        Returns
        -------
        str
            String showing number of children.

        Examples
        --------
        >>> node = TrieNode()
        >>> node.children['a'] = TrieNode()
        >>> node.children['b'] = TrieNode()
        >>> str(node)
        'TrieNode(2 children)'
        """
        return f"TrieNode({len(self.children)} children)"


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

    Notes
    -----
    Time complexity: O(1) for height access
    """

    __slots__ = ("height",)

    def __init__(
        self,
        data: Any,
        left: Optional["AVLNode"] = None,
        right: Optional["AVLNode"] = None,
        parent: Optional["AVLNode"] = None,
    ) -> None:
        """Initialize an AVL node with height tracking.

        Parameters
        ----------
        data : Any
            The data to store in the node.
        left : AVLNode or None, optional
            The left child. Default is None.
        right : AVLNode or None, optional
            The right child. Default is None.
        parent : AVLNode or None, optional
            The parent node. Default is None.
        """
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

    Notes
    -----
    Time complexity: O(1) for color access
    """

    __slots__ = ("color",)

    def __init__(
        self,
        data: Any,
        color: str = "RED",
        left: Optional["RedBlackNode"] = None,
        right: Optional["RedBlackNode"] = None,
        parent: Optional["RedBlackNode"] = None,
    ) -> None:
        """Initialize a Red-Black node.

        Parameters
        ----------
        data : Any
            The data to store in the node.
        color : str, optional
            The color ("RED" or "BLACK"). Default is "RED".
        left : RedBlackNode or None, optional
            The left child. Default is None.
        right : RedBlackNode or None, optional
            The right child. Default is None.
        parent : RedBlackNode or None, optional
            The parent node. Default is None.
        """
        super().__init__(data, left, right, parent)
        self.color: str = color


class BTreeNode(Node):
    """Node for B-Tree structures.

    A B-Tree node contains multiple keys and children. For a node with k keys,
    there are k+1 children. Keys and children maintain the B-Tree ordering:

        child[0] < key[0] < child[1] < key[1] < ... < key[k-1] < child[k]

    In a B-Tree of minimum degree t:
    - Every node (except root) has at least t-1 keys
    - Every node has at most 2t-1 keys
    - A node with k keys has k+1 children (if not a leaf)
    - All leaves are at the same depth

    Parameters
    ----------
    t : int
        Minimum degree (minimum number of keys is t-1, maximum is 2t-1).
        Must be >= 2.
    is_leaf : bool, optional
        Whether this node is a leaf. Default is True.

    Attributes
    ----------
    keys : List[Any]
        Sorted list of keys stored in this node (property).
    children : List[BTreeNode]
        List of child node references (property accessing _refs).
    is_leaf : bool
        True if this is a leaf node (has no children).
    t : int
        Minimum degree of the B-Tree.
    parent : BTreeNode or None
        Reference to parent node (inherited from Node).

    Examples
    --------
    Create a leaf node:

    >>> node = BTreeNode(t=3)
    >>> node.keys = [10, 20, 30]
    >>> node.is_leaf
    True
    >>> len(node.keys)
    3
    >>> node.is_full()
    False
    >>> node.is_minimal()
    True

    Create an internal node with children:

    >>> root = BTreeNode(t=3, is_leaf=False)
    >>> root.keys = [50]
    >>> left_child = BTreeNode(t=3)
    >>> left_child.keys = [10, 20, 30]
    >>> right_child = BTreeNode(t=3)
    >>> right_child.keys = [60, 70, 80]
    >>> root.add_child(left_child)
    >>> root.add_child(right_child)
    >>> len(root.children)
    2
    >>> left_child.parent is root
    True

    Check node state:

    >>> node = BTreeNode(t=2)
    >>> node.keys = [10]
    >>> node.is_minimal()
    True
    >>> node.keys.append(20)
    >>> node.keys.append(30)
    >>> node.is_full()
    True

    Find key position:

    >>> node = BTreeNode(t=3)
    >>> node.keys = [10, 30, 50]
    >>> node.find_key_index(20)
    1
    >>> node.find_key_index(40)
    2
    >>> node.find_key_index(5)
    0

    Notes
    -----
    This class uses __slots__ for memory efficiency. The _refs list
    (inherited from Node) stores the children.

    B-Tree nodes maintain the invariant that keys are always sorted.
    Methods like insert_key should maintain this invariant, but the
    class itself doesn't enforce it automatically.

    The minimum degree t must be at least 2. This ensures:
    - Each internal node has at least 2 children
    - Each node (except root) has at least 1 key

    See Also
    --------
    Node : Abstract base class.
    TreeNode : Node for general trees with list-based children.
    BinaryNode : Node for binary trees.
    """

    __slots__ = ("_keys", "is_leaf", "t")

    def __init__(self, t: int, is_leaf: bool = True) -> None:
        """Initialize a B-Tree node.

        Parameters
        ----------
        t : int
            Minimum degree (defines min/max keys: t-1 to 2t-1).
            Must be >= 2.
        is_leaf : bool, optional
            Whether this is a leaf node. Default is True.

        Raises
        ------
        ValueError
            If t < 2.

        Examples
        --------
        >>> node = BTreeNode(t=3)
        >>> node.t
        3
        >>> node.is_leaf
        True

        >>> internal = BTreeNode(t=2, is_leaf=False)
        >>> internal.is_leaf
        False
        """
        if t < 2:
            raise ValueError("Minimum degree t must be at least 2")

        # B-Tree nodes don't have a single data value
        super().__init__(data=None)
        self.t: int = t
        self.is_leaf: bool = is_leaf
        self._keys: List[Any] = []
        # _refs will store children (inherited from Node)

    @property
    def keys(self) -> List[Any]:
        """Get the list of keys in this node.

        Returns
        -------
        List[Any]
            Sorted list of keys.

        Examples
        --------
        >>> node = BTreeNode(t=3)
        >>> node.keys
        []
        >>> node.keys = [10, 20]
        >>> node.keys
        [10, 20]

        Notes
        -----
        This property returns a direct reference to the internal keys list.
        Modifications affect the node. For safe access, consider copying:
        `keys_copy = list(node.keys)`

        Time complexity: O(1)
        """
        return self._keys

    @keys.setter
    def keys(self, keys: List[Any]) -> None:
        """Set the keys for this node.

        Parameters
        ----------
        keys : List[Any]
            List of keys. Should be sorted for correct B-Tree behavior.

        Examples
        --------
        >>> node = BTreeNode(t=3)
        >>> node.keys = [10, 20, 30]
        >>> node.keys
        [10, 20, 30]

        Notes
        -----
        This setter does NOT verify that keys are sorted or that their
        count is within valid bounds (t-1 to 2t-1). The B-Tree
        implementation is responsible for maintaining these invariants.
        """
        self._keys = keys

    @property
    def children(self) -> List["BTreeNode"]:
        """Get the list of child nodes.

        Returns
        -------
        List[BTreeNode]
            List of children. For k keys, should have k+1 children
            (if not a leaf).

        Examples
        --------
        >>> node = BTreeNode(t=3, is_leaf=False)
        >>> node.keys = [50]
        >>> child1 = BTreeNode(t=3)
        >>> node.add_child(child1)
        >>> len(node.children)
        1

        Notes
        -----
        This property returns the internal _refs list directly.
        For leaf nodes, this list should always be empty.

        Time complexity: O(1)
        """
        return self._refs  # type: ignore[return-value]

    def add_child(self, child: "BTreeNode", index: Optional[int] = None) -> None:
        """Add a child node at the specified index.

        Parameters
        ----------
        child : BTreeNode
            Child node to add.
        index : int, optional
            Position to insert child. If None, appends to end.

        Examples
        --------
        >>> parent = BTreeNode(t=3, is_leaf=False)
        >>> child1 = BTreeNode(t=3)
        >>> child2 = BTreeNode(t=3)
        >>> parent.add_child(child1)
        >>> parent.add_child(child2)
        >>> len(parent.children)
        2
        >>> child1.parent is parent
        True

        Insert at specific position:

        >>> parent = BTreeNode(t=3, is_leaf=False)
        >>> child1 = BTreeNode(t=3)
        >>> child2 = BTreeNode(t=3)
        >>> child3 = BTreeNode(t=3)
        >>> parent.add_child(child1)
        >>> parent.add_child(child3)
        >>> parent.add_child(child2, index=1)
        >>> parent.children[1] is child2
        True

        Notes
        -----
        This method automatically updates the parent reference of the child.
        Time complexity: O(1) for append, O(n) for insert at index.
        """
        if index is None:
            self._refs.append(child)
        else:
            self._refs.insert(index, child)
        child._parent = self

    def remove_child(self, index: int) -> "BTreeNode":
        """Remove and return child at the specified index.

        Parameters
        ----------
        index : int
            Index of child to remove.

        Returns
        -------
        BTreeNode
            The removed child node.

        Raises
        ------
        IndexError
            If index is out of range.

        Examples
        --------
        >>> parent = BTreeNode(t=3, is_leaf=False)
        >>> child1 = BTreeNode(t=3)
        >>> child2 = BTreeNode(t=3)
        >>> parent.add_child(child1)
        >>> parent.add_child(child2)
        >>> removed = parent.remove_child(0)
        >>> removed is child1
        True
        >>> removed.parent is None
        True
        >>> len(parent.children)
        1

        Notes
        -----
        This method automatically clears the parent reference of the
        removed child.
        Time complexity: O(n) where n is the number of children.
        """
        child = self._refs.pop(index)
        if child:
            child._parent = None  # type: ignore
        return child  # type: ignore[return-value]

    def is_full(self) -> bool:
        """Check if node has maximum number of keys.

        Returns
        -------
        bool
            True if node has 2t-1 keys (maximum capacity).

        Examples
        --------
        >>> node = BTreeNode(t=3)
        >>> node.keys = [10, 20]
        >>> node.is_full()
        False
        >>> node.keys = [10, 20, 30, 40, 50]  # 2*3-1 = 5 keys
        >>> node.is_full()
        True

        >>> node = BTreeNode(t=2)
        >>> node.keys = [10, 20, 30]  # 2*2-1 = 3 keys
        >>> node.is_full()
        True

        Notes
        -----
        A full node must be split before inserting more keys.
        Time complexity: O(1)
        """
        return len(self._keys) == 2 * self.t - 1

    def is_minimal(self) -> bool:
        """Check if node has minimum number of keys.

        Returns
        -------
        bool
            True if node has exactly t-1 keys (minimum for non-root).

        Examples
        --------
        >>> node = BTreeNode(t=3)
        >>> node.keys = [10, 20]  # t-1 = 2 keys
        >>> node.is_minimal()
        True
        >>> node.keys.append(30)
        >>> node.is_minimal()
        False

        >>> node = BTreeNode(t=2)
        >>> node.keys = [10]  # t-1 = 1 key
        >>> node.is_minimal()
        True

        Notes
        -----
        Nodes with fewer than t-1 keys violate B-Tree properties
        (except for the root, which can have as few as 1 key).
        Time complexity: O(1)
        """
        return len(self._keys) == self.t - 1

    def insert_key(self, key: Any, index: Optional[int] = None) -> None:
        """Insert a key at the specified index.

        Parameters
        ----------
        key : Any
            Key to insert.
        index : int, optional
            Position to insert. If None, appends to end.

        Examples
        --------
        >>> node = BTreeNode(t=3)
        >>> node.insert_key(10)
        >>> node.insert_key(30)
        >>> node.insert_key(20, index=1)
        >>> node.keys
        [10, 20, 30]

        Notes
        -----
        This method does NOT maintain sorted order automatically.
        The caller (typically the B-Tree implementation) is responsible
        for determining the correct insertion index.

        Time complexity: O(1) for append, O(k) for insert where k is
        the number of keys.
        """
        if index is None:
            self._keys.append(key)
        else:
            self._keys.insert(index, key)

    def remove_key(self, index: int) -> Any:
        """Remove and return key at the specified index.

        Parameters
        ----------
        index : int
            Index of key to remove.

        Returns
        -------
        Any
            The removed key.

        Raises
        ------
        IndexError
            If index is out of range.

        Examples
        --------
        >>> node = BTreeNode(t=3)
        >>> node.keys = [10, 20, 30]
        >>> removed = node.remove_key(1)
        >>> removed
        20
        >>> node.keys
        [10, 30]

        Notes
        -----
        Time complexity: O(k) where k is the number of keys.
        """
        return self._keys.pop(index)

    def find_key_index(self, key: Any) -> int:
        """Find the index where key should be (or is located).

        This performs a linear search to find the first index i where
        key <= keys[i], or returns len(keys) if key is larger than all keys.

        Parameters
        ----------
        key : Any
            Key to find. Must be comparable with existing keys.

        Returns
        -------
        int
            Index i where keys[i-1] < key <= keys[i], or len(keys)
            if key is greater than all keys.

        Examples
        --------
        >>> node = BTreeNode(t=3)
        >>> node.keys = [10, 30, 50]
        >>> node.find_key_index(5)
        0
        >>> node.find_key_index(20)
        1
        >>> node.find_key_index(30)
        1
        >>> node.find_key_index(40)
        2
        >>> node.find_key_index(60)
        3

        Empty node:

        >>> node = BTreeNode(t=3)
        >>> node.find_key_index(10)
        0

        Notes
        -----
        This method uses linear search which is O(k) where k is the
        number of keys. For large nodes, binary search could be used
        instead, but since k <= 2t-1 and t is typically small (often < 100),
        the performance difference is negligible.

        The returned index can be used to:
        - Determine which child to follow in search (if not leaf)
        - Determine where to insert a new key
        - Check if the key exists (keys[i] == key if i < len(keys))

        Time complexity: O(k) where k is the number of keys in the node.
        """
        i = 0
        while i < len(self._keys) and key > self._keys[i]:
            i += 1
        return i

    def __repr__(self) -> str:
        """Return detailed string representation.

        Returns
        -------
        str
            String showing node state including t, keys, leaf status,
            and number of children.

        Examples
        --------
        >>> node = BTreeNode(t=3)
        >>> node.keys = [10, 20]
        >>> repr(node)
        'BTreeNode(t=3, keys=[10, 20], is_leaf=True, n_children=0)'

        >>> root = BTreeNode(t=2, is_leaf=False)
        >>> root.keys = [50]
        >>> root.add_child(BTreeNode(t=2))
        >>> root.add_child(BTreeNode(t=2))
        >>> repr(root)
        'BTreeNode(t=2, keys=[50], is_leaf=False, n_children=2)'
        """
        return (
            f"BTreeNode(t={self.t}, keys={self._keys}, "
            f"is_leaf={self.is_leaf}, n_children={len(self._refs)})"
        )

    def __str__(self) -> str:
        """Return simple string representation showing keys.

        Returns
        -------
        str
            String showing just the keys.

        Examples
        --------
        >>> node = BTreeNode(t=3)
        >>> node.keys = [10, 20, 30]
        >>> str(node)
        'BTreeNode([10, 20, 30])'

        >>> node = BTreeNode(t=3)
        >>> str(node)
        'BTreeNode([])'
        """
        return f"BTreeNode({self._keys})"
