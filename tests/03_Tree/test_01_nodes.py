"""Tests for BinaryNode and TreeNode classes."""

import pytest

from sds.core.node import Node
from sds.tree.node import BinaryNode, BTreeNode, TreeNode, TrieNode

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


# =============================================================================
# TrieNode Tests
# =============================================================================


class TestTrieNodeCreation:
    """Test TrieNode creation."""

    def test_create_trie_node(self) -> None:
        """Test creating a trie node."""
        node = TrieNode()
        assert node.children == {}
        assert node.is_end_of_word is False

    def test_trie_node_add_child(self) -> None:
        """Test adding child to trie node."""
        node = TrieNode()
        child = TrieNode()
        node.children["a"] = child
        assert "a" in node.children
        assert node.children["a"] is child


# =============================================================================
# BTreeNode Tests
# =============================================================================


class TestBTreeNodeInit:
    """Tests for BTreeNode initialization."""

    def test_init_default_leaf(self):
        """Test default initialization creates a leaf node."""
        node = BTreeNode(t=3)
        assert node.t == 3
        assert node.is_leaf is True
        assert node.keys == []
        assert node.children == []
        assert node.parent is None

    def test_init_internal_node(self):
        """Test initialization of internal node."""
        node = BTreeNode(t=2, is_leaf=False)
        assert node.t == 2
        assert node.is_leaf is False
        assert node.keys == []
        assert node.children == []

    def test_init_various_t_values(self):
        """Test initialization with various t values."""
        for t in [2, 3, 5, 10, 100]:
            node = BTreeNode(t=t)
            assert node.t == t

    def test_init_invalid_t_zero(self):
        """Test that t=0 raises ValueError."""
        with pytest.raises(ValueError, match="at least 2"):
            BTreeNode(t=0)

    def test_init_invalid_t_one(self):
        """Test that t=1 raises ValueError."""
        with pytest.raises(ValueError, match="at least 2"):
            BTreeNode(t=1)

    def test_init_invalid_t_negative(self):
        """Test that negative t raises ValueError."""
        with pytest.raises(ValueError, match="at least 2"):
            BTreeNode(t=-5)

    def test_init_data_is_none(self):
        """Test that data attribute is None for BTreeNode."""
        node = BTreeNode(t=3)
        assert node.data is None


class TestBTreeNodeKeys:
    """Tests for key management."""

    def test_keys_getter_empty(self):
        """Test getting keys from empty node."""
        node = BTreeNode(t=3)
        assert node.keys == []
        assert isinstance(node.keys, list)

    def test_keys_setter(self):
        """Test setting keys."""
        node = BTreeNode(t=3)
        node.keys = [10, 20, 30]
        assert node.keys == [10, 20, 30]

    def test_keys_setter_empty_list(self):
        """Test setting empty list of keys."""
        node = BTreeNode(t=3)
        node.keys = [10, 20]
        node.keys = []
        assert node.keys == []

    def test_keys_direct_modification(self):
        """Test that keys can be modified directly."""
        node = BTreeNode(t=3)
        node.keys = [10, 20]
        node.keys.append(30)
        assert node.keys == [10, 20, 30]

    def test_keys_multiple_types(self):
        """Test keys with different comparable types."""
        node = BTreeNode(t=3)
        node.keys = [1, 2, 3]
        assert node.keys == [1, 2, 3]

        node.keys = ["a", "b", "c"]
        assert node.keys == ["a", "b", "c"]

        node.keys = [1.5, 2.7, 3.9]
        assert node.keys == [1.5, 2.7, 3.9]


class TestBTreeNodeChildren:
    """Tests for child management."""

    def test_children_empty_initially(self):
        """Test that children list is empty initially."""
        node = BTreeNode(t=3, is_leaf=False)
        assert node.children == []
        assert isinstance(node.children, list)

    def test_add_child_single(self):
        """Test adding a single child."""
        parent = BTreeNode(t=3, is_leaf=False)
        child = BTreeNode(t=3)
        parent.add_child(child)

        assert len(parent.children) == 1
        assert parent.children[0] is child
        assert child.parent is parent

    def test_add_child_multiple(self):
        """Test adding multiple children."""
        parent = BTreeNode(t=3, is_leaf=False)
        children = [BTreeNode(t=3) for _ in range(4)]

        for child in children:
            parent.add_child(child)

        assert len(parent.children) == 4
        for i, child in enumerate(children):
            assert parent.children[i] is child
            assert child.parent is parent

    def test_add_child_at_index(self):
        """Test adding child at specific index."""
        parent = BTreeNode(t=3, is_leaf=False)
        child1 = BTreeNode(t=3)
        child2 = BTreeNode(t=3)
        child3 = BTreeNode(t=3)

        parent.add_child(child1)
        parent.add_child(child3)
        parent.add_child(child2, index=1)

        assert parent.children == [child1, child2, child3]
        assert child2.parent is parent

    def test_add_child_at_beginning(self):
        """Test adding child at index 0."""
        parent = BTreeNode(t=3, is_leaf=False)
        child1 = BTreeNode(t=3)
        child2 = BTreeNode(t=3)

        parent.add_child(child1)
        parent.add_child(child2, index=0)

        assert parent.children[0] is child2
        assert parent.children[1] is child1

    def test_remove_child_single(self):
        """Test removing a single child."""
        parent = BTreeNode(t=3, is_leaf=False)
        child = BTreeNode(t=3)
        parent.add_child(child)

        removed = parent.remove_child(0)

        assert removed is child
        assert child.parent is None
        assert len(parent.children) == 0

    def test_remove_child_multiple(self):
        """Test removing children from multiple."""
        parent = BTreeNode(t=3, is_leaf=False)
        children = [BTreeNode(t=3) for _ in range(3)]
        for child in children:
            parent.add_child(child)

        removed = parent.remove_child(1)

        assert removed is children[1]
        assert children[1].parent is None
        assert len(parent.children) == 2
        assert parent.children == [children[0], children[2]]

    def test_remove_child_invalid_index(self):
        """Test removing child with invalid index."""
        parent = BTreeNode(t=3, is_leaf=False)
        parent.add_child(BTreeNode(t=3))

        with pytest.raises(IndexError):
            parent.remove_child(5)

    def test_remove_child_negative_index(self):
        """Test removing child with negative index."""
        parent = BTreeNode(t=3, is_leaf=False)
        child1 = BTreeNode(t=3)
        child2 = BTreeNode(t=3)
        parent.add_child(child1)
        parent.add_child(child2)

        removed = parent.remove_child(-1)
        assert removed is child2
        assert len(parent.children) == 1


class TestBTreeNodeStateMethods:
    """Tests for state checking methods."""

    def test_is_full_t2(self):
        """Test is_full for t=2 (max 3 keys)."""
        node = BTreeNode(t=2)
        assert node.is_full() is False

        node.keys = [10]
        assert node.is_full() is False

        node.keys = [10, 20]
        assert node.is_full() is False

        node.keys = [10, 20, 30]  # 2*2-1 = 3
        assert node.is_full() is True

    def test_is_full_t3(self):
        """Test is_full for t=3 (max 5 keys)."""
        node = BTreeNode(t=3)
        assert node.is_full() is False

        node.keys = [10, 20, 30, 40]
        assert node.is_full() is False

        node.keys = [10, 20, 30, 40, 50]  # 2*3-1 = 5
        assert node.is_full() is True

    def test_is_full_t5(self):
        """Test is_full for t=5 (max 9 keys)."""
        node = BTreeNode(t=5)
        node.keys = list(range(8))
        assert node.is_full() is False

        node.keys = list(range(9))  # 2*5-1 = 9
        assert node.is_full() is True

    def test_is_minimal_t2(self):
        """Test is_minimal for t=2 (min 1 key)."""
        node = BTreeNode(t=2)
        assert node.is_minimal() is False

        node.keys = [10]  # t-1 = 1
        assert node.is_minimal() is True

        node.keys = [10, 20]
        assert node.is_minimal() is False

    def test_is_minimal_t3(self):
        """Test is_minimal for t=3 (min 2 keys)."""
        node = BTreeNode(t=3)
        assert node.is_minimal() is False

        node.keys = [10]
        assert node.is_minimal() is False

        node.keys = [10, 20]  # t-1 = 2
        assert node.is_minimal() is True

        node.keys = [10, 20, 30]
        assert node.is_minimal() is False

    def test_is_minimal_t5(self):
        """Test is_minimal for t=5 (min 4 keys)."""
        node = BTreeNode(t=5)
        node.keys = [10, 20, 30]
        assert node.is_minimal() is False

        node.keys = [10, 20, 30, 40]  # t-1 = 4
        assert node.is_minimal() is True

        node.keys = [10, 20, 30, 40, 50]
        assert node.is_minimal() is False


class TestBTreeNodeKeyOperations:
    """Tests for key insertion and removal."""

    def test_insert_key_append(self):
        """Test inserting key at end (append)."""
        node = BTreeNode(t=3)
        node.insert_key(10)
        assert node.keys == [10]

        node.insert_key(20)
        assert node.keys == [10, 20]

        node.insert_key(30)
        assert node.keys == [10, 20, 30]

    def test_insert_key_at_index(self):
        """Test inserting key at specific index."""
        node = BTreeNode(t=3)
        node.insert_key(10)
        node.insert_key(30)
        node.insert_key(20, index=1)

        assert node.keys == [10, 20, 30]

    def test_insert_key_at_beginning(self):
        """Test inserting key at index 0."""
        node = BTreeNode(t=3)
        node.insert_key(20)
        node.insert_key(30)
        node.insert_key(10, index=0)

        assert node.keys == [10, 20, 30]

    def test_remove_key_single(self):
        """Test removing single key."""
        node = BTreeNode(t=3)
        node.keys = [10]
        removed = node.remove_key(0)

        assert removed == 10
        assert node.keys == []

    def test_remove_key_middle(self):
        """Test removing key from middle."""
        node = BTreeNode(t=3)
        node.keys = [10, 20, 30]
        removed = node.remove_key(1)

        assert removed == 20
        assert node.keys == [10, 30]

    def test_remove_key_first(self):
        """Test removing first key."""
        node = BTreeNode(t=3)
        node.keys = [10, 20, 30]
        removed = node.remove_key(0)

        assert removed == 10
        assert node.keys == [20, 30]

    def test_remove_key_last(self):
        """Test removing last key."""
        node = BTreeNode(t=3)
        node.keys = [10, 20, 30]
        removed = node.remove_key(2)

        assert removed == 30
        assert node.keys == [10, 20]

    def test_remove_key_invalid_index(self):
        """Test removing key with invalid index."""
        node = BTreeNode(t=3)
        node.keys = [10]

        with pytest.raises(IndexError):
            node.remove_key(5)

    def test_remove_key_negative_index(self):
        """Test removing key with negative index."""
        node = BTreeNode(t=3)
        node.keys = [10, 20, 30]
        removed = node.remove_key(-1)

        assert removed == 30
        assert node.keys == [10, 20]


class TestBTreeNodeFindKeyIndex:
    """Tests for find_key_index method."""

    def test_find_key_index_empty_node(self):
        """Test finding index in empty node."""
        node = BTreeNode(t=3)
        assert node.find_key_index(10) == 0
        assert node.find_key_index(0) == 0
        assert node.find_key_index(100) == 0

    def test_find_key_index_single_key(self):
        """Test finding index with single key."""
        node = BTreeNode(t=3)
        node.keys = [20]

        assert node.find_key_index(10) == 0
        assert node.find_key_index(20) == 0
        assert node.find_key_index(30) == 1

    def test_find_key_index_multiple_keys(self):
        """Test finding index with multiple keys."""
        node = BTreeNode(t=3)
        node.keys = [10, 30, 50]

        assert node.find_key_index(5) == 0
        assert node.find_key_index(10) == 0
        assert node.find_key_index(15) == 1
        assert node.find_key_index(30) == 1
        assert node.find_key_index(40) == 2
        assert node.find_key_index(50) == 2
        assert node.find_key_index(60) == 3

    def test_find_key_index_all_smaller(self):
        """Test when search key is smaller than all keys."""
        node = BTreeNode(t=3)
        node.keys = [20, 40, 60]
        assert node.find_key_index(10) == 0

    def test_find_key_index_all_larger(self):
        """Test when search key is larger than all keys."""
        node = BTreeNode(t=3)
        node.keys = [20, 40, 60]
        assert node.find_key_index(70) == 3

    def test_find_key_index_exact_match_first(self):
        """Test exact match at first position."""
        node = BTreeNode(t=3)
        node.keys = [10, 20, 30]
        idx = node.find_key_index(10)
        assert idx == 0
        assert node.keys[idx] == 10

    def test_find_key_index_exact_match_middle(self):
        """Test exact match in middle."""
        node = BTreeNode(t=3)
        node.keys = [10, 20, 30]
        idx = node.find_key_index(20)
        assert idx == 1
        assert node.keys[idx] == 20

    def test_find_key_index_exact_match_last(self):
        """Test exact match at last position."""
        node = BTreeNode(t=3)
        node.keys = [10, 20, 30]
        idx = node.find_key_index(30)
        assert idx == 2
        assert node.keys[idx] == 30

    def test_find_key_index_between_keys(self):
        """Test finding index between keys."""
        node = BTreeNode(t=3)
        node.keys = [10, 20, 30, 40, 50]

        assert node.find_key_index(15) == 1
        assert node.find_key_index(25) == 2
        assert node.find_key_index(35) == 3
        assert node.find_key_index(45) == 4

    def test_find_key_index_string_keys(self):
        """Test finding index with string keys."""
        node = BTreeNode(t=3)
        node.keys = ["apple", "cherry", "mango"]

        assert node.find_key_index("aardvark") == 0
        assert node.find_key_index("banana") == 1
        assert node.find_key_index("cherry") == 1
        assert node.find_key_index("grape") == 2
        assert node.find_key_index("zebra") == 3


class TestBTreeNodeStringRepresentation:
    """Tests for string representations."""

    def test_repr_empty_leaf(self):
        """Test repr of empty leaf node."""
        node = BTreeNode(t=3)
        rep = repr(node)
        assert "t=3" in rep
        assert "keys=[]" in rep
        assert "is_leaf=True" in rep
        assert "n_children=0" in rep

    def test_repr_leaf_with_keys(self):
        """Test repr of leaf with keys."""
        node = BTreeNode(t=3)
        node.keys = [10, 20, 30]
        rep = repr(node)
        assert "keys=[10, 20, 30]" in rep
        assert "is_leaf=True" in rep

    def test_repr_internal_node(self):
        """Test repr of internal node."""
        node = BTreeNode(t=2, is_leaf=False)
        node.keys = [50]
        node.add_child(BTreeNode(t=2))
        node.add_child(BTreeNode(t=2))
        rep = repr(node)

        assert "t=2" in rep
        assert "keys=[50]" in rep
        assert "is_leaf=False" in rep
        assert "n_children=2" in rep

    def test_str_empty(self):
        """Test str of empty node."""
        node = BTreeNode(t=3)
        assert str(node) == "BTreeNode([])"

    def test_str_with_keys(self):
        """Test str with keys."""
        node = BTreeNode(t=3)
        node.keys = [10, 20, 30]
        assert str(node) == "BTreeNode([10, 20, 30])"

    def test_str_single_key(self):
        """Test str with single key."""
        node = BTreeNode(t=3)
        node.keys = [42]
        assert str(node) == "BTreeNode([42])"


class TestBTreeNodeComplexScenarios:
    """Tests for complex scenarios and edge cases."""

    def test_build_small_tree(self):
        """Test building a small B-Tree structure."""
        # Root with one key and two children
        root = BTreeNode(t=3, is_leaf=False)
        root.keys = [50]

        left = BTreeNode(t=3)
        left.keys = [10, 20, 30]

        right = BTreeNode(t=3)
        right.keys = [60, 70, 80]

        root.add_child(left)
        root.add_child(right)

        assert len(root.children) == 2
        assert root.children[0] is left
        assert root.children[1] is right
        assert left.parent is root
        assert right.parent is root
        assert root.is_leaf is False
        assert left.is_leaf is True
        assert right.is_leaf is True

    def test_build_three_level_tree(self):
        """Test building a three-level tree structure."""
        # Root
        root = BTreeNode(t=2, is_leaf=False)
        root.keys = [50, 100]

        # Second level
        left = BTreeNode(t=2, is_leaf=False)
        left.keys = [25]

        middle = BTreeNode(t=2, is_leaf=False)
        middle.keys = [75]

        right = BTreeNode(t=2, is_leaf=False)
        right.keys = [125]

        root.add_child(left)
        root.add_child(middle)
        root.add_child(right)

        # Third level (leaves)
        left.add_child(BTreeNode(t=2))
        left.children[0].keys = [10, 20]

        left.add_child(BTreeNode(t=2))
        left.children[1].keys = [30, 40]

        # Verify structure
        assert len(root.children) == 3
        assert len(left.children) == 2
        assert left.children[0].parent is left
        assert left.parent is root

    def test_modify_keys_after_creation(self):
        """Test modifying keys after node creation."""
        node = BTreeNode(t=3)
        node.keys = [10, 20]

        # Direct list modification
        node.keys.append(30)
        assert node.keys == [10, 20, 30]

        # Using insert_key
        node.insert_key(15, index=1)
        assert node.keys == [10, 15, 20, 30]

        # Using remove_key
        node.remove_key(2)
        assert node.keys == [10, 15, 30]

    def test_parent_child_consistency(self):
        """Test parent-child relationship consistency."""
        parent = BTreeNode(t=3, is_leaf=False)
        child1 = BTreeNode(t=3)
        child2 = BTreeNode(t=3)

        # Add children
        parent.add_child(child1)
        parent.add_child(child2)

        assert child1.parent is parent
        assert child2.parent is parent

        # Remove child
        removed = parent.remove_child(0)
        assert removed is child1
        assert child1.parent is None
        assert child2.parent is parent

    def test_maximum_keys_boundary(self):
        """Test at maximum key capacity boundary."""
        node = BTreeNode(t=2)  # Max 3 keys

        for i in range(3):
            node.insert_key(i * 10)
            if i < 2:
                assert node.is_full() is False
            else:
                assert node.is_full() is True

    def test_minimum_keys_boundary(self):
        """Test at minimum key capacity boundary."""
        node = BTreeNode(t=3)  # Min 2 keys

        node.keys = [10]
        assert node.is_minimal() is False

        node.keys = [10, 20]
        assert node.is_minimal() is True

        node.keys = [10, 20, 30]
        assert node.is_minimal() is False

    def test_keys_are_reference(self):
        """Test that keys property returns reference, not copy."""
        node = BTreeNode(t=3)
        node.keys = [10, 20]

        keys_ref = node.keys
        keys_ref.append(30)

        assert node.keys == [10, 20, 30]

    def test_children_are_reference(self):
        """Test that children property returns reference, not copy."""
        node = BTreeNode(t=3, is_leaf=False)
        child = BTreeNode(t=3)
        node.add_child(child)

        children_ref = node.children
        assert len(children_ref) == 1
        assert children_ref[0] is child


class TestBTreeNodeTypeConsistency:
    """Tests for type consistency and edge cases."""

    def test_different_key_types(self):
        """Test with different key types."""
        # Integer keys
        node = BTreeNode(t=3)
        node.keys = [1, 2, 3]
        assert node.find_key_index(2) == 1

        # String keys
        node.keys = ["a", "b", "c"]
        assert node.find_key_index("b") == 1

        # Float keys
        node.keys = [1.5, 2.5, 3.5]
        assert node.find_key_index(2.0) == 1

    def test_large_number_of_keys(self):
        """Test with large number of keys."""
        node = BTreeNode(t=50)  # Max 99 keys
        keys = list(range(0, 990, 10))
        node.keys = keys

        assert node.is_full() is True
        assert len(node.keys) == 99
        assert node.find_key_index(455) == 46

    def test_large_number_of_children(self):
        """Test with large number of children."""
        parent = BTreeNode(t=50, is_leaf=False)
        parent.keys = list(range(0, 990, 10))  # 99 keys

        # Should have 100 children (k+1)
        for _ in range(100):
            parent.add_child(BTreeNode(t=50))

        assert len(parent.children) == 100
        assert parent.is_full() is True


class TestBTreeNodeInheritance:
    """Tests for inherited Node functionality."""

    def test_inherits_from_node(self):
        """Test that BTreeNode inherits from Node."""
        from sds.core.node import Node

        node = BTreeNode(t=3)
        assert isinstance(node, Node)

    def test_parent_property_inherited(self):
        """Test parent property from Node."""
        parent = BTreeNode(t=3, is_leaf=False)
        child = BTreeNode(t=3)

        parent.add_child(child)
        assert child.parent is parent

        # Test parent setter
        child.parent = None
        assert child.parent is None

    def test_data_property_inherited(self):
        """Test data property from Node."""
        node = BTreeNode(t=3)
        assert node.data is None

        # Should be able to set data (though not used in BTree)
        node.data = "test"
        assert node.data == "test"

    def test_slots_memory_efficiency(self):
        """Test that __slots__ is properly defined."""
        node = BTreeNode(t=3)

        # Should not be able to add arbitrary attributes
        with pytest.raises(AttributeError):
            node.arbitrary_attr = "value"  # type: ignore
