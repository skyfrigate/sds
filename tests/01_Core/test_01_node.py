"""Tests for abstract Node class."""

import pytest

from sds.core.node import Node


class TestNodeAbstract:
    """Tests for Node abstract class."""

    def test_cannot_instantiate_node_directly(self):
        """Test that Node cannot be instantiated directly."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            Node(42)

    def test_node_is_abstract_base_class(self):
        """Test that Node is an ABC."""
        from abc import ABC

        assert issubclass(Node, ABC)

    def test_node_has_required_slots(self):
        """Test that Node defines required slots."""
        assert hasattr(Node, "__slots__")
        slots = Node.__slots__
        assert "_data" in slots
        assert "_refs" in slots
        assert "_parent" in slots

    def test_node_has_data_property(self):
        """Test that Node has data property."""
        assert hasattr(Node, "data")
        assert isinstance(Node.data, property)

    def test_node_has_parent_property(self):
        """Test that Node has parent property."""
        assert hasattr(Node, "parent")
        assert isinstance(Node.parent, property)

    def test_node_has_abstract_repr(self):
        """Test that Node has abstract __repr__ method."""
        assert hasattr(Node, "__repr__")
        assert getattr(Node.__repr__, "__isabstractmethod__", False)

    def test_node_has_abstract_str(self):
        """Test that Node has abstract __str__ method."""
        assert hasattr(Node, "__str__")
        assert getattr(Node.__str__, "__isabstractmethod__", False)


class TestNodeConcreteImplementation:
    """Tests using a minimal concrete Node implementation."""

    @pytest.fixture
    def concrete_node_class(self):
        """Create a minimal concrete Node implementation for testing."""

        class ConcreteNode(Node):
            def __repr__(self):
                return f"ConcreteNode({self._data!r})"

            def __str__(self):
                return str(self._data)

        return ConcreteNode

    def test_can_instantiate_concrete_node(self, concrete_node_class):
        """Test that concrete Node subclass can be instantiated."""
        node = concrete_node_class(42)
        assert node.data == 42

    def test_concrete_node_has_data(self, concrete_node_class):
        """Test that concrete node has data property."""
        node = concrete_node_class(42)
        assert node.data == 42

    def test_concrete_node_data_can_be_set(self, concrete_node_class):
        """Test that data can be modified."""
        node = concrete_node_class(42)
        node.data = 100
        assert node.data == 100

    def test_concrete_node_has_refs_list(self, concrete_node_class):
        """Test that concrete node has _refs list."""
        node = concrete_node_class(42)
        assert hasattr(node, "_refs")
        assert isinstance(node._refs, list)

    def test_concrete_node_has_parent(self, concrete_node_class):
        """Test that concrete node has parent attribute."""
        node = concrete_node_class(42)
        assert node.parent is None

    def test_concrete_node_parent_can_be_set(self, concrete_node_class):
        """Test that parent can be set."""
        parent = concrete_node_class(100)
        child = concrete_node_class(42)
        child.parent = parent
        assert child.parent is parent

    def test_concrete_node_repr(self, concrete_node_class):
        """Test __repr__ implementation."""
        node = concrete_node_class(42)
        assert repr(node) == "ConcreteNode(42)"

    def test_concrete_node_str(self, concrete_node_class):
        """Test __str__ implementation."""
        node = concrete_node_class(42)
        assert str(node) == "42"

    def test_concrete_node_uses_slots(self, concrete_node_class):
        """Test that slots prevent dynamic attributes."""
        node = concrete_node_class(42)
        with pytest.raises(AttributeError):
            node.dynamic_attr == "test"


class TestNodeInheritance:
    """Tests for Node inheritance behavior."""

    def test_subclass_must_implement_repr(self):
        """Test that subclass without __repr__ cannot be instantiated."""

        class IncompleteNode(Node):
            def __str__(self):
                return str(self._data)

        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            IncompleteNode(42)

    def test_subclass_must_implement_str(self):
        """Test that subclass without __str__ cannot be instantiated."""

        class IncompleteNode(Node):
            def __repr__(self):
                return f"IncompleteNode({self._data!r})"

        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            IncompleteNode(42)

    def test_subclass_with_all_methods_can_be_instantiated(self):
        """Test that complete subclass can be instantiated."""

        class CompleteNode(Node):
            def __repr__(self):
                return f"CompleteNode({self._data!r})"

            def __str__(self):
                return str(self._data)

        node = CompleteNode(42)
        assert node.data == 42
