"""Tests for SimpleNode and DoublyNode classes."""

from sds.core.node import Node
from sds.linear.node import SimpleNode

# =============================================================================
# SimpleNode Tests
# =============================================================================


class TestSimpleNodeCreation:
    """Tests for SimpleNode creation and initialization."""

    def test_simple_node_creation_with_data_only(self):
        """Test creating a simple node with only data."""
        node = SimpleNode(42)
        assert node.data == 42
        assert node.next is None

    def test_simple_node_creation_with_next(self):
        """Test creating a simple node with next node."""
        next_node = SimpleNode(10)
        node = SimpleNode(42, next_node)
        assert node.data == 42
        assert node.next is next_node
        assert node.next.data == 10

    def test_simple_node_inherits_from_node(self):
        """Test that SimpleNode inherits from Node."""
        assert issubclass(SimpleNode, Node)

    def test_simple_node_has_refs(self):
        """Test that SimpleNode has _refs list."""
        node = SimpleNode(42)
        assert hasattr(node, "_refs")
        assert isinstance(node._refs, list)
        assert len(node._refs) == 1

    def test_simple_node_without_next(self):
        node = SimpleNode(42)
        assert len(node._refs) == 1
        assert node.next is None

    def test_simple_node_with_next(self):
        """Test creating a simple node with next node."""
        next_node = SimpleNode(10)
        node = SimpleNode(42, next_node)
        assert hasattr(node, "_refs")
        assert isinstance(node._refs, list)
        assert len(node._refs) == 1


class TestSimpleNodeDataProperty:
    """Tests for SimpleNode data property."""

    def test_simple_node_data_getter(self, simple_node):
        """Test getting data from simple node."""
        assert simple_node.data == 42

    def test_simple_node_data_setter(self, simple_node):
        """Test setting data in simple node."""
        simple_node.data = 100
        assert simple_node.data == 100

    def test_simple_node_data_can_be_modified(self):
        """Test that node data can be modified."""
        node = SimpleNode(42)
        node.data = 100
        assert node.data == 100

    def test_simple_node_data_setter_accepts_none(self):
        """Test that data setter accepts None."""
        node = SimpleNode(42)
        node.data = None
        assert node.data is None

    def test_simple_node_data_setter_with_various_types(self, sample_values):
        """Test data setter with various data types."""
        node = SimpleNode(0)
        node.data = sample_values
        assert node.data == sample_values


class TestSimpleNodeNextProperty:
    """Tests for SimpleNode next property."""

    def test_simple_node_next_getter(self):
        """Test getting next node."""
        next_node = SimpleNode(10)
        node = SimpleNode(42, next_node)
        assert node.next is next_node

    def test_simple_node_next_setter(self):
        """Test setting next node."""
        node = SimpleNode(42)
        next_node = SimpleNode(10)
        node.next = next_node
        assert node.next is next_node

    def test_simple_node_next_can_be_none(self):
        """Test that next can be None."""
        node = SimpleNode(42)
        node.next = None
        assert node.next is None

    def test_simple_node_next_can_be_replaced(self):
        """Test that next can be replaced."""
        node = SimpleNode(42)
        next1 = SimpleNode(10)
        next2 = SimpleNode(20)
        node.next = next1
        assert node.next is next1
        node.next = next2
        assert node.next is next2


class TestSimpleNodeChaining:
    """Tests for chaining SimpleNodes."""

    def test_simple_node_chain_creation(self, node_chain):
        """Test creating a chain of nodes."""
        assert node_chain.data == 1
        assert node_chain.next.data == 2
        assert node_chain.next.next.data == 3

    def test_simple_node_chain_traversal(self, node_chain):
        """Test traversing a chain."""
        current = node_chain
        values = []
        while current is not None:
            values.append(current.data)
            current = current.next
        assert values == [1, 2, 3]


class TestSimpleNodeStringRepresentations:
    """Tests for SimpleNode __repr__ and __str__ methods."""

    def test_simple_node_repr(self):
        """Test __repr__ method."""
        node = SimpleNode(42)
        assert repr(node) == "SimpleNode(42)"

    def test_simple_node_repr_with_string_data(self):
        """Test __repr__ with string data."""
        node = SimpleNode("hello")
        assert repr(node) == "SimpleNode('hello')"

    def test_simple_node_str(self):
        """Test __str__ method."""
        node = SimpleNode(42)
        assert str(node) == "42"


class TestSimpleNodeVariousDataTypes:
    """Tests for SimpleNode with various data types."""

    def test_simple_node_accepts_various_data_types(self, sample_values):
        """Test that simple node accepts various data types."""
        node = SimpleNode(sample_values)
        assert node.data == sample_values
