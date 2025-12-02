"""Tests for BinaryNode and TreeNode classes."""

import pytest

from sds.core.node import Node
from sds.tree.node import BinaryNode, TreeNode

# =============================================================================
# BinaryNode Tests
# =============================================================================


class TestBinaryNodeCreation:
    """Tests for BinaryNode creation and initialization."""

    def test_binary_node_creation_with_data_only(self):
        """Test creating a binary node with only data."""
        node = BinaryNode(42)
        assert node.data == 42
        assert node.left is None
        assert node.right is None
        assert node.parent is None

    def test_binary_node_creation_with_left_child(self):
        """Test creating a binary node with left child."""
        left = BinaryNode(10)
        node = BinaryNode(42, left=left)
        assert node.data == 42
        assert node.left is left
        assert node.left.data == 10
        assert node.right is None
        assert left.parent is node

    def test_binary_node_creation_with_right_child(self):
        """Test creating a binary node with right child."""
        right = BinaryNode(20)
        node = BinaryNode(42, right=right)
        assert node.data == 42
        assert node.left is None
        assert node.right is right
        assert node.right.data == 20
        assert right.parent is node

    def test_binary_node_creation_with_both_children(self):
        """Test creating a binary node with both children."""
        left = BinaryNode(10)
        right = BinaryNode(20)
        node = BinaryNode(42, left=left, right=right)
        assert node.data == 42
        assert node.left is left
        assert node.right is right
        assert left.parent is node
        assert right.parent is node

    def test_binary_node_creation_with_parent(self):
        """Test creating a binary node with parent."""
        parent = BinaryNode(100)
        node = BinaryNode(42, parent=parent)
        assert node.data == 42
        assert node.parent is parent

    def test_binary_node_inherits_from_node(self):
        """Test that BinaryNode inherits from Node."""
        assert issubclass(BinaryNode, Node)

    def test_binary_node_has_refs(self):
        """Test that BinaryNode has _refs list."""
        node = BinaryNode(42)
        assert hasattr(node, "_refs")
        assert isinstance(node._refs, list)
        assert len(node._refs) == 2


class TestBinaryNodeLeftProperty:
    """Tests for BinaryNode left property."""

    def test_binary_node_left_getter(self):
        """Test getting left child."""
        left = BinaryNode(10)
        node = BinaryNode(42, left=left)
        assert node.left is left

    def test_binary_node_left_setter(self):
        """Test setting left child."""
        node = BinaryNode(42)
        left = BinaryNode(10)
        node.left = left
        assert node.left is left
        assert left.parent is node

    def test_binary_node_left_setter_updates_parent(self):
        """Test that setting left child updates parent reference."""
        parent = BinaryNode(42)
        child = BinaryNode(10)
        parent.left = child
        assert child.parent is parent

    def test_binary_node_left_can_be_none(self):
        """Test that left child can be None."""
        node = BinaryNode(42)
        node.left = None
        assert node.left is None

    def test_binary_node_left_can_be_replaced(self):
        """Test that left child can be replaced."""
        node = BinaryNode(42)
        left1 = BinaryNode(10)
        left2 = BinaryNode(20)
        node.left = left1
        assert node.left is left1
        node.left = left2
        assert node.left is left2
        assert left2.parent is node


class TestBinaryNodeRightProperty:
    """Tests for BinaryNode right property."""

    def test_binary_node_right_getter(self):
        """Test getting right child."""
        right = BinaryNode(20)
        node = BinaryNode(42, right=right)
        assert node.right is right

    def test_binary_node_right_setter(self):
        """Test setting right child."""
        node = BinaryNode(42)
        right = BinaryNode(20)
        node.right = right
        assert node.right is right
        assert right.parent is node

    def test_binary_node_right_setter_updates_parent(self):
        """Test that setting right child updates parent reference."""
        parent = BinaryNode(42)
        child = BinaryNode(20)
        parent.right = child
        assert child.parent is parent

    def test_binary_node_right_can_be_none(self):
        """Test that right child can be None."""
        node = BinaryNode(42)
        node.right = None
        assert node.right is None


class TestBinaryNodeTreeStructure:
    """Tests for binary tree structure operations."""

    def test_build_simple_binary_tree(self):
        """Test building a simple binary tree."""
        root = BinaryNode(10)
        left = BinaryNode(5)
        right = BinaryNode(15)

        root.left = left
        root.right = right

        assert root.data == 10
        assert root.left.data == 5
        assert root.right.data == 15
        assert left.parent is root
        assert right.parent is root

    def test_build_three_level_tree(self):
        """Test building a three-level binary tree."""
        root = BinaryNode(10)
        root.left = BinaryNode(5)
        root.right = BinaryNode(15)
        root.left.left = BinaryNode(2)
        root.left.right = BinaryNode(7)

        assert root.left.left.data == 2
        assert root.left.right.data == 7
        assert root.left.left.parent is root.left
        assert root.left.right.parent is root.left


class TestBinaryNodeIsLeaf:
    """Tests for is_leaf() method."""

    def test_is_leaf_for_node_without_children(self):
        """Test is_leaf returns True for node without children."""
        node = BinaryNode(42)
        assert node.is_leaf() is True

    def test_is_leaf_for_node_with_left_child(self):
        """Test is_leaf returns False for node with left child."""
        node = BinaryNode(42)
        node.left = BinaryNode(10)
        assert node.is_leaf() is False

    def test_is_leaf_for_node_with_right_child(self):
        """Test is_leaf returns False for node with right child."""
        node = BinaryNode(42)
        node.right = BinaryNode(20)
        assert node.is_leaf() is False

    def test_is_leaf_for_node_with_both_children(self):
        """Test is_leaf returns False for node with both children."""
        node = BinaryNode(42)
        node.left = BinaryNode(10)
        node.right = BinaryNode(20)
        assert node.is_leaf() is False


class TestBinaryNodeStringRepresentations:
    """Tests for __repr__ and __str__ methods."""

    def test_binary_node_repr(self):
        """Test __repr__ method."""
        node = BinaryNode(42)
        assert repr(node) == "BinaryNode(42)"

    def test_binary_node_repr_with_string_data(self):
        """Test __repr__ with string data."""
        node = BinaryNode("hello")
        assert repr(node) == "BinaryNode('hello')"

    def test_binary_node_str(self):
        """Test __str__ method."""
        node = BinaryNode(42)
        assert str(node) == "42"


class TestBinaryNodeVariousDataTypes:
    """Tests for BinaryNode with various data types."""

    def test_binary_node_accepts_various_data_types(self, sample_values):
        """Test that binary node accepts various data types."""
        node = BinaryNode(sample_values)
        assert node.data == sample_values


# =============================================================================
# TreeNode Tests
# =============================================================================


class TestTreeNodeCreation:
    """Tests for TreeNode creation and initialization."""

    def test_tree_node_creation_with_data_only(self):
        """Test creating a tree node with only data."""
        node = TreeNode(42)
        assert node.data == 42
        assert node.children == []
        assert node.parent is None

    def test_tree_node_creation_with_parent(self):
        """Test creating a tree node with parent."""
        parent = TreeNode(100)
        node = TreeNode(42, parent=parent)
        assert node.data == 42
        assert node.parent is parent
        assert node.children == []

    def test_tree_node_inherits_from_node(self):
        """Test that TreeNode inherits from Node."""
        assert issubclass(TreeNode, Node)

    def test_tree_node_children_is_refs(self):
        """Test that children property returns _refs."""
        node = TreeNode(42)
        assert node.children is node._refs


class TestTreeNodeChildrenProperty:
    """Tests for TreeNode children property."""

    def test_tree_node_children_getter_empty(self):
        """Test getting children from node without children."""
        node = TreeNode(42)
        assert node.children == []
        assert isinstance(node.children, list)

    def test_tree_node_children_getter_with_children(self):
        """Test getting children from node with children."""
        parent = TreeNode(42)
        child1 = TreeNode(10)
        child2 = TreeNode(20)
        parent.add_child(child1)
        parent.add_child(child2)

        assert len(parent.children) == 2
        assert child1 in parent.children
        assert child2 in parent.children


class TestTreeNodeAddChild:
    """Tests for add_child() method."""

    def test_add_child_to_empty_node(self):
        """Test adding a child to node without children."""
        parent = TreeNode(42)
        child = TreeNode(10)
        parent.add_child(child)

        assert len(parent.children) == 1
        assert child in parent.children
        assert child.parent is parent

    def test_add_multiple_children(self):
        """Test adding multiple children."""
        parent = TreeNode(42)
        child1 = TreeNode(10)
        child2 = TreeNode(20)
        child3 = TreeNode(30)

        parent.add_child(child1)
        parent.add_child(child2)
        parent.add_child(child3)

        assert len(parent.children) == 3
        assert child1 in parent.children
        assert child2 in parent.children
        assert child3 in parent.children

    def test_add_child_updates_parent_reference(self):
        """Test that add_child updates child's parent reference."""
        parent = TreeNode(42)
        child = TreeNode(10)
        parent.add_child(child)
        assert child.parent is parent

    def test_add_same_child_twice(self):
        """Test adding the same child twice doesn't duplicate."""
        parent = TreeNode(42)
        child = TreeNode(10)
        parent.add_child(child)
        parent.add_child(child)
        assert len(parent.children) == 1


class TestTreeNodeRemoveChild:
    """Tests for remove_child() method."""

    def test_remove_child_from_parent(self):
        """Test removing a child from parent."""
        parent = TreeNode(42)
        child = TreeNode(10)
        parent.add_child(child)
        parent.remove_child(child)

        assert len(parent.children) == 0
        assert child not in parent.children
        assert child.parent is None

    def test_remove_child_updates_parent_reference(self):
        """Test that remove_child clears child's parent reference."""
        parent = TreeNode(42)
        child = TreeNode(10)
        parent.add_child(child)
        parent.remove_child(child)
        assert child.parent is None

    def test_remove_child_with_multiple_children(self):
        """Test removing one child when multiple exist."""
        parent = TreeNode(42)
        child1 = TreeNode(10)
        child2 = TreeNode(20)
        child3 = TreeNode(30)

        parent.add_child(child1)
        parent.add_child(child2)
        parent.add_child(child3)

        parent.remove_child(child2)

        assert len(parent.children) == 2
        assert child1 in parent.children
        assert child2 not in parent.children
        assert child3 in parent.children

    def test_remove_nonexistent_child_raises_error(self):
        """Test removing a child that doesn't exist raises ValueError."""
        parent = TreeNode(42)
        child = TreeNode(10)

        with pytest.raises(ValueError):
            parent.remove_child(child)


class TestTreeNodeIsLeaf:
    """Tests for is_leaf() method."""

    def test_is_leaf_for_node_without_children(self):
        """Test is_leaf returns True for node without children."""
        node = TreeNode(42)
        assert node.is_leaf() is True

    def test_is_leaf_for_node_with_one_child(self):
        """Test is_leaf returns False for node with one child."""
        parent = TreeNode(42)
        parent.add_child(TreeNode(10))
        assert parent.is_leaf() is False

    def test_is_leaf_for_node_with_multiple_children(self):
        """Test is_leaf returns False for node with multiple children."""
        parent = TreeNode(42)
        parent.add_child(TreeNode(10))
        parent.add_child(TreeNode(20))
        parent.add_child(TreeNode(30))
        assert parent.is_leaf() is False


class TestTreeNodeTreeStructure:
    """Tests for tree structure operations."""

    def test_build_simple_tree(self):
        """Test building a simple tree structure."""
        root = TreeNode("A")
        child1 = TreeNode("B")
        child2 = TreeNode("C")

        root.add_child(child1)
        root.add_child(child2)

        assert root.data == "A"
        assert len(root.children) == 2
        assert child1.parent is root
        assert child2.parent is root

    def test_build_multi_level_tree(self):
        """Test building a multi-level tree."""
        root = TreeNode("A")
        b = TreeNode("B")
        c = TreeNode("C")
        d = TreeNode("D")
        e = TreeNode("E")

        root.add_child(b)
        root.add_child(c)
        b.add_child(d)
        b.add_child(e)

        assert len(root.children) == 2
        assert len(b.children) == 2
        assert d.parent is b
        assert e.parent is b


class TestTreeNodeStringRepresentations:
    """Tests for __repr__ and __str__ methods."""

    def test_tree_node_repr(self):
        """Test __repr__ method."""
        node = TreeNode(42)
        assert repr(node) == "TreeNode(42)"

    def test_tree_node_repr_with_string_data(self):
        """Test __repr__ with string data."""
        node = TreeNode("hello")
        assert repr(node) == "TreeNode('hello')"

    def test_tree_node_str(self):
        """Test __str__ method."""
        node = TreeNode(42)
        assert str(node) == "42"


class TestTreeNodeVariousDataTypes:
    """Tests for TreeNode with various data types."""

    def test_tree_node_accepts_various_data_types(self, sample_values):
        """Test that tree node accepts various data types."""
        node = TreeNode(sample_values)
        assert node.data == sample_values
