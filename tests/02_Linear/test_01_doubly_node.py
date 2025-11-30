"""Tests for SimpleNode and DoublyNode classes."""

from sds.core.node import Node
from sds.linear.node import DoublyNode, SimpleNode

# =============================================================================
# DoublyNode Tests
# =============================================================================


class TestDoublyNodeCreation:
    """Tests for DoublyNode creation and initialization."""

    def test_doubly_node_creation_with_data_only(self):
        """Test creating a doubly node with only data."""
        node = DoublyNode(42)
        assert node.data == 42
        assert node.next is None
        assert node.prev is None

    def test_doubly_node_creation_with_next(self):
        """Test creating a doubly node with next node."""
        next_node = DoublyNode(10)
        node = DoublyNode(42, next_node)
        assert node.data == 42
        assert node.next is next_node

    def test_doubly_node_creation_with_prev(self):
        """Test creating a doubly node with prev node."""
        prev_node = DoublyNode(10)
        node = DoublyNode(42, None, prev_node)
        assert node.data == 42
        assert node.prev is prev_node

    def test_doubly_node_creation_with_both(self):
        """Test creating a doubly node with both next and prev."""
        next_node = DoublyNode(20)
        prev_node = DoublyNode(10)
        node = DoublyNode(42, next_node, prev_node)
        assert node.data == 42
        assert node.next is next_node
        assert node.prev is prev_node

    def test_doubly_node_inherits_from_node(self):
        """Test that DoublyNode inherits from Node."""
        assert issubclass(DoublyNode, Node)

    def test_doubly_node_has_refs(self):
        """Test that DoublyNode has _refs list."""
        node = DoublyNode(42)
        assert hasattr(node, "_refs")
        assert isinstance(node._refs, list)
        assert len(node._refs) == 2


class TestDoublyNodeDataProperty:
    """Tests for DoublyNode data property."""

    def test_doubly_node_data_getter(self, simple_doubly_node):
        """Test getting data from doubly node."""
        assert simple_doubly_node.data == 42

    def test_doubly_node_data_setter(self, simple_doubly_node):
        """Test setting data in doubly node."""
        simple_doubly_node.data = 100
        assert simple_doubly_node.data == 100

    def test_doubly_node_data_setter_accepts_none(self):
        """Test that data setter accepts None."""
        node = DoublyNode(42)
        node.data = None
        assert node.data is None

    def test_doubly_node_data_setter_with_various_types(self, sample_values):
        """Test data setter with various data types."""
        node = DoublyNode(0)
        node.data = sample_values
        assert node.data == sample_values


class TestDoublyNodeNextProperty:
    """Tests for DoublyNode next property."""

    def test_doubly_node_empty_getter(self):
        """Test getting next from doubly node."""
        node = DoublyNode(42)
        assert node.next is None
        assert node.prev is None

    def test_doubly_node_next_getter(self):
        """Test getting next node."""
        next_node = DoublyNode(10)
        node = DoublyNode(42, next_node)
        assert node.next is next_node

    def test_doubly_node_next_setter(self):
        """Test setting next node."""
        node = DoublyNode(42)
        next_node = DoublyNode(10)
        node.next = next_node
        assert node.next is next_node

    def test_doubly_node_next_can_be_none(self):
        """Test that next can be None."""
        node = DoublyNode(42)
        node.next = None
        assert node.next is None


class TestDoublyNodePrevProperty:
    """Tests for DoublyNode prev property."""

    def test_doubly_node_prev_getter(self):
        """Test getting prev node."""
        prev_node = DoublyNode(10)
        node = DoublyNode(42, None, prev_node)
        assert node.prev is prev_node

    def test_doubly_node_prev_setter(self):
        """Test setting prev node."""
        node = DoublyNode(42)
        prev_node = DoublyNode(10)
        node.prev = prev_node
        assert node.prev is prev_node

    def test_doubly_node_prev_can_be_none(self):
        """Test that prev can be None."""
        node = DoublyNode(42)
        node.prev = None
        assert node.prev is None


class TestDoublyNodeBidirectionalChain:
    """Tests for bidirectional chains of DoublyNodes."""

    def test_doubly_node_bidirectional_chain_creation(self, doubly_node_chain):
        """Test creating a bidirectional chain."""
        assert doubly_node_chain.data == 1
        assert doubly_node_chain.next.data == 2
        assert doubly_node_chain.next.next.data == 3

    def test_doubly_node_chain_forward_traversal(self, doubly_node_chain):
        """Test forward traversal."""
        current = doubly_node_chain
        values = []
        while current is not None:
            values.append(current.data)
            current = current.next
        assert values == [1, 2, 3]

    def test_doubly_node_chain_backward_traversal(self, doubly_node_chain):
        """Test backward traversal."""
        # Go to end
        current = doubly_node_chain
        while current.next is not None:
            current = current.next

        # Traverse backward
        values = []
        while current is not None:
            values.append(current.data)
            current = current.prev
        assert values == [3, 2, 1]

    def test_doubly_node_bidirectional_consistency(self):
        """Test that prev and next are consistent."""
        node1 = DoublyNode(1)
        node2 = DoublyNode(2)
        node3 = DoublyNode(3)

        node1.next = node2
        node2.prev = node1
        node2.next = node3
        node3.prev = node2

        assert node2.prev is node1
        assert node2.next is node3
        assert node1.next is node2
        assert node3.prev is node2


class TestDoublyNodeStringRepresentations:
    """Tests for DoublyNode __repr__ and __str__ methods."""

    def test_doubly_node_repr(self):
        """Test __repr__ method."""
        node = DoublyNode(42)
        assert repr(node) == "DoublyNode(42)"

    def test_doubly_node_repr_with_string_data(self):
        """Test __repr__ with string data."""
        node = DoublyNode("hello")
        assert repr(node) == "DoublyNode('hello')"

    def test_doubly_node_str(self):
        """Test __str__ method."""
        node = DoublyNode(42)
        assert str(node) == "42"


class TestDoublyNodeVariousDataTypes:
    """Tests for DoublyNode with various data types."""

    def test_doubly_node_accepts_various_data_types(self, sample_values):
        """Test that doubly node accepts various data types."""
        node = DoublyNode(sample_values)
        assert node.data == sample_values


# =============================================================================
# Comparison Tests
# =============================================================================


class TestSimpleNodeVsDoublyNode:
    """Tests comparing SimpleNode and DoublyNode."""

    def test_simple_node_has_no_prev(self):
        """Test that SimpleNode does not have prev attribute."""
        node = SimpleNode(42)
        # prev is not a property on SimpleNode
        assert not hasattr(type(node), "prev") or "prev" not in dir(type(node))

    def test_doubly_node_has_both_next_and_prev(self):
        """Test that DoublyNode has both next and prev."""
        node = DoublyNode(42)
        assert hasattr(node, "next")
        assert hasattr(node, "prev")

    def test_simple_node_refs_length(self):
        """Test that SimpleNode _refs has 1 element."""
        node = SimpleNode(42)
        assert len(node._refs) == 1

    def test_doubly_node_refs_length(self):
        """Test that DoublyNode _refs has 2 elements."""
        node = DoublyNode(42)
        assert len(node._refs) == 2

    def test_both_inherit_from_node(self):
        """Test that both inherit from Node."""
        assert issubclass(SimpleNode, Node)
        assert issubclass(DoublyNode, Node)
