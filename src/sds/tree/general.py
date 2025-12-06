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

"""General tree (n-ary tree) implementation.

This module provides a general tree implementation where each node can have
an arbitrary number of children. This is in contrast to binary trees where
each node has at most two children.

Classes
-------
Tree
    General tree where nodes can have any number of children.

Examples
--------
Creating and using a general tree:

>>> from sds.tree.general import Tree
>>> tree = Tree("Root")
>>> child1 = tree.add_child("Child 1")
>>> child2 = tree.add_child("Child 2")
>>> grandchild = tree.add_child_to("Child 1", "Grandchild")
>>> tree.height()
2

Tree structure visualization:

>>> tree = Tree("A")
>>> tree.add_child("B")
>>> tree.add_child("C")
>>> tree.add_child_to("B", "D")
>>> tree.add_child_to("B", "E")
>>> # Structure:
>>> #       A
>>> #      / \\
>>> #     B   C
>>> #    / \\
>>> #   D   E

Notes
-----
General trees are useful for:
- File systems and directory structures
- Organization hierarchies
- XML/HTML DOM trees
- Game trees (decision trees)
- Abstract syntax trees (AST)

See Also
--------
sds.tree.binary : Binary tree implementations.
sds.tree.node.TreeNode : Node class used internally.
"""

from collections import deque
from typing import Any, Iterator, List, Optional, cast

from ..core.exceptions import EmptyStructureError, InvalidOperationError
from .interfaces import AbstractTree
from .node import TreeNode

__all__ = ["Tree"]


class Tree(AbstractTree):
    """General tree (n-ary tree) implementation.

    A general tree is a tree structure where each node can have any number
    of children (0 to n). This is the most flexible tree structure and is
    used for hierarchical data like file systems, organizational charts,
    and XML/HTML documents.

    The tree is implemented using TreeNode objects that maintain a list
    of children for each node.

    Attributes
    ----------
    root : TreeNode or None
        The root node of the tree (read-only property).
    size : int
        The number of nodes in the tree (read-only property).

    Examples
    --------
    Create a simple tree:

    >>> tree = Tree("Root")
    >>> tree.add_child("Child 1")
    TreeNode('Child 1')
    >>> tree.add_child("Child 2")
    TreeNode('Child 2')
    >>> len(tree)
    3

    Build a hierarchical structure:

    >>> tree = Tree("CEO")
    >>> tree.add_child("CTO")
    TreeNode('CTO')
    >>> tree.add_child("CFO")
    TreeNode('CFO')
    >>> tree.add_child_to("CTO", "Dev Team Lead")
    TreeNode('Dev Team Lead')
    >>> tree.height()
    2

    Traverse the tree:

    >>> tree = Tree("A")
    >>> tree.add_child("B")
    TreeNode('B')
    >>> tree.add_child("C")
    TreeNode('C')
    >>> list(tree.preorder_traversal())
    ['A', 'B', 'C']

    Notes
    -----
    Time Complexity:
    - Insert child: O(1) at root, O(n) for search + O(1) for add
    - Remove: O(n) to find node
    - Search: O(n)
    - Height: O(n)
    - Traversals: O(n)

    Space Complexity: O(n)

    See Also
    --------
    BinaryTree : Tree with at most 2 children per node.
    TreeNode : Node class with variable children.
    """

    def __init__(self, root_data: Optional[Any] = None):
        """Initialize a general tree.

        Parameters
        ----------
        root_data : Any, optional
            Data for the root node. If None, creates an empty tree.

        Examples
        --------
        >>> tree = Tree("Root")
        >>> tree.root.data
        'Root'

        >>> empty_tree = Tree()
        >>> empty_tree.is_empty()
        True
        """
        super().__init__()
        self._root: Optional[TreeNode] = None
        if root_data is not None:
            self._root = TreeNode(root_data)
            self._size = 1
        else:
            self._size = 0

    @property
    def root(self) -> Optional[TreeNode]:
        """Get the root node of the tree.

        Returns
        -------
        TreeNode or None
            The root node, or None if tree is empty.

        Examples
        --------
        >>> tree = Tree("Root")
        >>> tree.root.data
        'Root'
        """
        return self._root

    def height(self) -> int:
        """Return the height of the tree.

        The height is the length of the longest path from root to a leaf.
        An empty tree has height -1, a tree with only root has height 0.

        Returns
        -------
        int
            The height of the tree.

        Examples
        --------
        >>> tree = Tree()
        >>> tree.height()
        -1

        >>> tree = Tree("Root")
        >>> tree.height()
        0

        >>> tree.add_child("Child")
        TreeNode('Child')
        >>> tree.height()
        1

        Notes
        -----
        Time complexity: O(n)
        """
        if self._root is None:
            return -1
        return self._height_recursive(self._root)

    def _height_recursive(self, node: TreeNode) -> int:
        """Calculate height recursively.

        Parameters
        ----------
        node : TreeNode
            Current node.

        Returns
        -------
        int
            Height of subtree rooted at node.
        """
        if node.is_leaf():
            return 0

        max_child_height = -1
        for child in node.children:
            child_height = self._height_recursive(child)
            max_child_height = max(max_child_height, child_height)

        return 1 + max_child_height

    def add_child(self, data: Any, parent: Optional[TreeNode] = None) -> TreeNode:
        """Add a child node.

        Parameters
        ----------
        data : Any
            Data for the new child node.
        parent : TreeNode, optional
            Parent node. If None, adds to root. If root doesn't exist,
            creates root with this data.

        Returns
        -------
        TreeNode
            The newly created child node.

        Raises
        ------
        InvalidOperationError
            If parent is None and tree already has a root.

        Examples
        --------
        >>> tree = Tree("Root")
        >>> child = tree.add_child("Child")
        >>> child.data
        'Child'
        >>> child.parent.data
        'Root'

        Notes
        -----
        Time complexity: O(1) when adding to a known parent.
        """
        new_node = TreeNode(data)

        if parent is None:
            if self._root is None:
                # No root yet, make this the root
                self._root = new_node
                self._size = 1
                return new_node
            else:
                # Add to root
                parent = self._root

        parent.add_child(new_node)
        self._size += 1
        return new_node

    def add_child_to(self, parent_data: Any, child_data: Any) -> TreeNode:
        """Add a child to a node with specific data.

        Searches for a node with parent_data and adds a child with child_data.

        Parameters
        ----------
        parent_data : Any
            Data of the parent node to search for.
        child_data : Any
            Data for the new child node.

        Returns
        -------
        TreeNode
            The newly created child node.

        Raises
        ------
        ValueError
            If parent node is not found.

        Examples
        --------
        >>> tree = Tree("Root")
        >>> tree.add_child("Child1")
        TreeNode('Child1')
        >>> tree.add_child_to("Child1", "Grandchild")
        TreeNode('Grandchild')

        Notes
        -----
        Time complexity: O(n) - must search for parent.
        """
        parent = self.find_node(parent_data)
        if parent is None:
            raise ValueError(f"Parent node with data {parent_data} not found")

        return self.add_child(child_data, parent)

    def find_node(self, data: Any) -> Optional[TreeNode]:
        """Find a node by its data.

        Uses breadth-first search to find the first node with matching data.

        Parameters
        ----------
        data : Any
            Data to search for.

        Returns
        -------
        TreeNode or None
            The found node, or None if not found.

        Examples
        --------
        >>> tree = Tree("Root")
        >>> tree.add_child("Child")
        TreeNode('Child')
        >>> node = tree.find_node("Child")
        >>> node.data
        'Child'

        Notes
        -----
        Time complexity: O(n)
        """
        if self._root is None:
            return None

        # BFS to find node
        queue: deque[TreeNode] = deque([self._root])
        while queue:
            current = queue.popleft()
            if current.data == data:
                return current

            queue.extend(current.children)

        return None

    def remove_node(self, data: Any) -> Any:
        """Remove a node and all its descendants.

        Parameters
        ----------
        data : Any
            Data of the node to remove.

        Returns
        -------
        Any
            The data of the removed node.

        Raises
        ------
        EmptyStructureError
            If tree is empty.
        ValueError
            If node is not found.
        InvalidOperationError
            If attempting to remove root without replacement.

        Examples
        --------
        >>> tree = Tree("Root")
        >>> tree.add_child("Child")
        TreeNode('Child')
        >>> tree.remove_node("Child")
        'Child'

        Notes
        -----
        Time complexity: O(n)
        Removing a node removes all its descendants.
        """
        if self._root is None:
            raise EmptyStructureError("Cannot remove from empty tree")

        # Special case: removing root
        if self._root.data == data:
            removed_data = self._root.data
            # Count all nodes in tree
            count = self._count_nodes(self._root)
            self._root = None
            self._size -= count
            return removed_data

        # Find parent of node to remove
        node_to_remove = self.find_node(data)
        if node_to_remove is None:
            raise ValueError(f"Node with data {data} not found")

        if node_to_remove.parent is None:
            raise InvalidOperationError("Cannot remove root this way")

        # Count nodes in subtree
        count = self._count_nodes(node_to_remove)

        # Remove from parent
        parent = cast(TreeNode, node_to_remove.parent)
        parent.remove_child(node_to_remove)
        self._size -= count

        return data

    def _count_nodes(self, node: TreeNode) -> int:
        """Count nodes in subtree.

        Parameters
        ----------
        node : TreeNode
            Root of subtree.

        Returns
        -------
        int
            Number of nodes in subtree.
        """
        count = 1  # Count this node
        for child in node.children:
            count += self._count_nodes(child)
        return count

    def insert(self, item: Any) -> None:
        """Insert an item into the tree.

        If tree is empty, creates root. Otherwise adds as child of root.

        Parameters
        ----------
        item : Any
            The item to insert.

        Examples
        --------
        >>> tree = Tree()
        >>> tree.insert("Root")
        >>> tree.insert("Child")
        >>> len(tree)
        2

        Notes
        -----
        Time complexity: O(1)
        """
        if self._root is None:
            self._root = TreeNode(item)
            self._size = 1
        else:
            self.add_child(item, self._root)

    def remove(self, item: Any) -> Any:
        """Remove an item from the tree.

        Parameters
        ----------
        item : Any
            The item to remove.

        Returns
        -------
        Any
            The removed item.

        Notes
        -----
        Time complexity: O(n)
        """
        return self.remove_node(item)

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
        >>> tree = Tree("Root")
        >>> tree.add_child("Child")
        TreeNode('Child')
        >>> tree.search("Child")
        True
        >>> tree.search("NotFound")
        False

        Notes
        -----
        Time complexity: O(n)
        """
        return self.find_node(item) is not None

    def clear(self) -> None:
        """Remove all nodes from the tree.

        Examples
        --------
        >>> tree = Tree("Root")
        >>> tree.add_child("Child")
        TreeNode('Child')
        >>> tree.clear()
        >>> tree.is_empty()
        True

        Notes
        -----
        Time complexity: O(1)
        """
        self._root = None
        self._size = 0

    def preorder_traversal(self) -> Iterator[Any]:
        """Return preorder traversal iterator.

        Preorder: parent -> children (left to right).

        Yields
        ------
        Any
            Items in preorder.

        Examples
        --------
        >>> tree = Tree("A")
        >>> tree.add_child("B")
        TreeNode('B')
        >>> tree.add_child("C")
        TreeNode('C')
        >>> list(tree.preorder_traversal())
        ['A', 'B', 'C']

        Notes
        -----
        Time complexity: O(n)
        """
        if self._root is not None:
            yield from self._preorder_recursive(self._root)

    def _preorder_recursive(self, node: TreeNode) -> Iterator[Any]:
        """Preorder traversal helper.

        Parameters
        ----------
        node : TreeNode
            Current node.

        Yields
        ------
        Any
            Node data in preorder.
        """
        yield node.data
        for child in node.children:
            yield from self._preorder_recursive(child)

    def postorder_traversal(self) -> Iterator[Any]:
        """Return postorder traversal iterator.

        Postorder: children (left to right) -> parent.

        Yields
        ------
        Any
            Items in postorder.

        Examples
        --------
        >>> tree = Tree("A")
        >>> tree.add_child("B")
        TreeNode('B')
        >>> tree.add_child("C")
        TreeNode('C')
        >>> list(tree.postorder_traversal())
        ['B', 'C', 'A']

        Notes
        -----
        Time complexity: O(n)
        """
        if self._root is not None:
            yield from self._postorder_recursive(self._root)

    def _postorder_recursive(self, node: TreeNode) -> Iterator[Any]:
        """Postorder traversal helper.

        Parameters
        ----------
        node : TreeNode
            Current node.

        Yields
        ------
        Any
            Node data in postorder.
        """
        for child in node.children:
            yield from self._postorder_recursive(child)
        yield node.data

    def level_order_traversal(self) -> Iterator[Any]:
        """Return level-order traversal iterator (BFS).

        Visits nodes level by level, left to right.

        Yields
        ------
        Any
            Items level by level.

        Examples
        --------
        >>> tree = Tree("A")
        >>> b = tree.add_child("B")
        >>> c = tree.add_child("C")
        >>> tree.add_child("D", b)
        TreeNode('D')
        >>> list(tree.level_order_traversal())
        ['A', 'B', 'C', 'D']

        Notes
        -----
        Time complexity: O(n)
        """
        if self._root is None:
            return

        queue: deque[TreeNode] = deque([self._root])
        while queue:
            current = queue.popleft()
            yield current.data
            queue.extend(current.children)

    def __iter__(self) -> Iterator[Any]:
        """Iterate over tree elements (preorder by default).

        Yields
        ------
        Any
            Elements in preorder.

        Examples
        --------
        >>> tree = Tree("A")
        >>> tree.add_child("B")
        TreeNode('B')
        >>> list(tree)
        ['A', 'B']
        """
        return self.preorder_traversal()

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
        >>> tree = Tree("Root")
        >>> tree.add_child("Child")
        TreeNode('Child')
        >>> "Child" in tree
        True
        """
        return self.search(item)

    def get_children(self, data: Any) -> List[TreeNode]:
        """Get all children of a node.

        Parameters
        ----------
        data : Any
            Data of the parent node.

        Returns
        -------
        List[TreeNode]
            List of child nodes.

        Raises
        ------
        ValueError
            If node is not found.

        Examples
        --------
        >>> tree = Tree("Root")
        >>> tree.add_child("Child1")
        TreeNode('Child1')
        >>> tree.add_child("Child2")
        TreeNode('Child2')
        >>> children = tree.get_children("Root")
        >>> len(children)
        2

        Notes
        -----
        Time complexity: O(n) for search.
        """
        node = self.find_node(data)
        if node is None:
            raise ValueError(f"Node with data {data} not found")
        return node.children.copy()

    def get_parent(self, data: Any) -> Optional[TreeNode]:
        """Get the parent of a node.

        Parameters
        ----------
        data : Any
            Data of the child node.

        Returns
        -------
        TreeNode or None
            The parent node, or None if node is root or not found.

        Examples
        --------
        >>> tree = Tree("Root")
        >>> tree.add_child("Child")
        TreeNode('Child')
        >>> parent = tree.get_parent("Child")
        >>> parent.data
        'Root'

        Notes
        -----
        Time complexity: O(n) for search.
        """
        node = self.find_node(data)
        if node is None:
            return None
        return cast(Optional[TreeNode], node.parent)

    def degree(self, data: Any) -> int:
        """Get the degree (number of children) of a node.

        Parameters
        ----------
        data : Any
            Data of the node.

        Returns
        -------
        int
            Number of children.

        Raises
        ------
        ValueError
            If node is not found.

        Examples
        --------
        >>> tree = Tree("Root")
        >>> tree.add_child("Child1")
        TreeNode('Child1')
        >>> tree.add_child("Child2")
        TreeNode('Child2')
        >>> tree.degree("Root")
        2

        Notes
        -----
        Time complexity: O(n) for search + O(1) for count.
        """
        node = self.find_node(data)
        if node is None:
            raise ValueError(f"Node with data {data} not found")
        return len(node.children)

    def is_leaf(self, data: Any) -> bool:
        """Check if a node is a leaf.

        Parameters
        ----------
        data : Any
            Data of the node.

        Returns
        -------
        bool
            True if node is a leaf (has no children).

        Raises
        ------
        ValueError
            If node is not found.

        Examples
        --------
        >>> tree = Tree("Root")
        >>> tree.add_child("Leaf")
        TreeNode('Leaf')
        >>> tree.is_leaf("Leaf")
        True
        >>> tree.is_leaf("Root")
        False

        Notes
        -----
        Time complexity: O(n) for search.
        """
        node = self.find_node(data)
        if node is None:
            raise ValueError(f"Node with data {data} not found")
        return node.is_leaf()

    def leaves(self) -> List[Any]:
        """Get all leaf nodes' data.

        Returns
        -------
        List[Any]
            List of data from all leaf nodes.

        Examples
        --------
        >>> tree = Tree("Root")
        >>> tree.add_child("Leaf1")
        TreeNode('Leaf1')
        >>> tree.add_child("Leaf2")
        TreeNode('Leaf2')
        >>> tree.leaves()
        ['Leaf1', 'Leaf2']

        Notes
        -----
        Time complexity: O(n)
        """
        if self._root is None:
            return []

        leaves = []
        for node_data in self.preorder_traversal():
            node = self.find_node(node_data)
            if node and node.is_leaf():
                leaves.append(node_data)
        return leaves

    def __repr__(self) -> str:
        """Return string representation.

        Returns
        -------
        str
            String representation.

        Examples
        --------
        >>> tree = Tree("Root")
        >>> repr(tree)
        'Tree(size=1)'
        """
        return f"Tree(size={self._size})"

    def __str__(self) -> str:
        """Return string showing tree structure.

        Returns
        -------
        str
            String representation.

        Examples
        --------
        >>> tree = Tree("Root")
        >>> tree.add_child("Child")
        TreeNode('Child')
        >>> print(tree)
        Tree: Root
          └─ Child
        """
        if self.is_empty():
            return "Tree: []"

        root = self._root
        # Avoid using `assert` for runtime checks (Bandit B101)
        if root is None:
            return "Tree: []"
        lines = [f"Tree: {root.data}"]
        self._build_tree_string(root, "", True, lines)
        return "\n".join(lines)

    def _build_tree_string(
        self, node: TreeNode, prefix: str, is_last: bool, lines: List[str]
    ) -> None:
        """Build string representation recursively.

        Parameters
        ----------
        node : TreeNode
            Current node.
        prefix : str
            Prefix for indentation.
        is_last : bool
            Whether this is the last child.
        lines : List[str]
            Accumulated lines.
        """
        if not node.children:
            return

        for i, child in enumerate(node.children):
            is_last_child = i == len(node.children) - 1
            connector = "└─" if is_last_child else "├─"
            lines.append(f"{prefix}{connector} {child.data}")

            extension = "  " if is_last_child else "│ "
            self._build_tree_string(child, prefix + extension, is_last_child, lines)
