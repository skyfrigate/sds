"""Tests for GraphNode class."""

import pytest

from sds.core.node import Node
from sds.graph.node import GraphNode


class TestGraphNodeCreation:
    """Tests for GraphNode creation and initialization."""

    def test_graph_node_creation_with_data_only(self):
        """Test creating a graph node with only data."""
        node = GraphNode(42)
        assert node.data == 42
        assert isinstance(node.id, str)
        assert len(node.id) > 0
        assert node.parent is None

    def test_graph_node_creation_with_custom_id(self):
        """Test creating a graph node with custom ID."""
        node = GraphNode(42, "node1")
        assert node.data == 42
        assert node.id == "node1"

    def test_graph_node_auto_generated_id_is_unique(self):
        """Test that auto-generated IDs are unique."""
        node1 = GraphNode(1)
        node2 = GraphNode(2)
        assert node1.id != node2.id

    def test_graph_node_inherits_from_node(self):
        """Test that GraphNode inherits from Node."""
        assert issubclass(GraphNode, Node)

    def test_graph_node_has_refs(self):
        """Test that GraphNode has _refs list."""
        node = GraphNode(42)
        assert hasattr(node, "_refs")
        assert isinstance(node._refs, list)

    def test_graph_node_refs_is_empty(self):
        """Test that GraphNode _refs is empty (not used)."""
        node = GraphNode(42)
        assert len(node._refs) == 0


class TestGraphNodeDataProperty:
    """Tests for GraphNode data property."""

    def test_graph_node_data_getter(self):
        """Test getting data from graph node."""
        node = GraphNode(42, "node1")
        assert node.data == 42

    def test_graph_node_data_setter(self):
        """Test setting data in graph node."""
        node = GraphNode(42, "node1")
        node.data = 100
        assert node.data == 100

    def test_graph_node_data_can_be_modified(self):
        """Test that node data can be modified."""
        node = GraphNode(42, "node1")
        node.data = 100
        assert node.data == 100

    def test_graph_node_data_setter_accepts_none(self):
        """Test that data setter accepts None."""
        node = GraphNode(42, "node1")
        node.data = None
        assert node.data is None

    def test_graph_node_data_setter_with_various_types(self, sample_values):
        """Test data setter with various data types."""
        node = GraphNode(0, "node1")
        node.data = sample_values
        assert node.data == sample_values


class TestGraphNodeIdProperty:
    """Tests for GraphNode id property."""

    def test_graph_node_id_getter(self):
        """Test getting ID from graph node."""
        node = GraphNode(42, "node1")
        assert node.id == "node1"

    def test_graph_node_id_is_read_only(self):
        """Test that ID cannot be changed after creation."""
        node = GraphNode(42, "node1")
        # ID has no setter, so this should raise AttributeError
        with pytest.raises(AttributeError):
            node.id = "node2"

    def test_graph_node_auto_id_format(self):
        """Test that auto-generated ID is a valid UUID string."""
        node = GraphNode(42)
        # UUID4 format: 8-4-4-4-12 characters
        assert isinstance(node.id, str)
        parts = node.id.split("-")
        assert len(parts) == 5
        assert len(parts[0]) == 8
        assert len(parts[1]) == 4
        assert len(parts[2]) == 4
        assert len(parts[3]) == 4
        assert len(parts[4]) == 12


class TestGraphNodeStringRepresentations:
    """Tests for __repr__ and __str__ methods."""

    def test_graph_node_repr(self):
        """Test __repr__ method."""
        node = GraphNode(42, "node1")
        assert repr(node) == "GraphNode(id='node1', data=42)"

    def test_graph_node_repr_with_string_data(self):
        """Test __repr__ with string data."""
        node = GraphNode("hello", "node1")
        assert repr(node) == "GraphNode(id='node1', data='hello')"

    def test_graph_node_str(self):
        """Test __str__ method."""
        node = GraphNode(42, "node1")
        assert str(node) == "node1: 42"

    def test_graph_node_str_with_string_data(self):
        """Test __str__ with string data."""
        node = GraphNode("hello", "node1")
        assert str(node) == "node1: hello"


class TestGraphNodeEquality:
    """Tests for GraphNode equality (__eq__ and __hash__)."""

    def test_graph_nodes_equal_with_same_id(self):
        """Test that nodes with same ID are equal."""
        node1 = GraphNode("A", "id1")
        node2 = GraphNode("B", "id1")
        assert node1 == node2

    def test_graph_nodes_not_equal_with_different_id(self):
        """Test that nodes with different IDs are not equal."""
        node1 = GraphNode("A", "id1")
        node2 = GraphNode("A", "id2")
        assert node1 != node2

    def test_graph_node_not_equal_to_non_node(self):
        """Test that GraphNode is not equal to non-GraphNode objects."""
        node = GraphNode(42, "node1")
        assert node != 42
        assert node != "node1"
        assert node is not None

    def test_graph_nodes_with_same_id_have_same_hash(self):
        """Test that nodes with same ID have same hash."""
        node1 = GraphNode("A", "id1")
        node2 = GraphNode("B", "id1")
        assert hash(node1) == hash(node2)

    def test_graph_nodes_with_different_id_have_different_hash(self):
        """Test that nodes with different IDs typically have different hash."""
        node1 = GraphNode("A", "id1")
        node2 = GraphNode("A", "id2")
        # Note: Different hashes are not guaranteed, but very likely
        assert hash(node1) != hash(node2)

    def test_graph_nodes_can_be_used_in_set(self):
        """Test that GraphNodes can be added to sets."""
        node1 = GraphNode("A", "id1")
        node2 = GraphNode("B", "id2")
        node3 = GraphNode("C", "id1")  # Same ID as node1

        node_set = {node1, node2, node3}
        assert len(node_set) == 2  # node1 and node3 are considered same

    def test_graph_nodes_can_be_used_as_dict_keys(self):
        """Test that GraphNodes can be used as dictionary keys."""
        node1 = GraphNode("A", "id1")
        node2 = GraphNode("B", "id2")

        node_dict = {node1: "value1", node2: "value2"}
        assert node_dict[node1] == "value1"
        assert node_dict[node2] == "value2"


class TestGraphNodeVariousDataTypes:
    """Tests for GraphNode with various data types."""

    def test_graph_node_accepts_various_data_types(self, sample_values):
        """Test that graph node accepts various data types."""
        node = GraphNode(sample_values, "node1")
        assert node.data == sample_values

    def test_graph_node_with_complex_data(self):
        """Test GraphNode with complex data structures."""
        data = {"name": "Alice", "age": 30, "connections": ["Bob", "Charlie"]}
        node = GraphNode(data, "user1")
        assert node.data == data
        assert node.data["name"] == "Alice"


class TestGraphNodeDoesNotUseRefs:
    """Tests confirming GraphNode doesn't use _refs."""

    def test_graph_node_refs_remains_empty(self):
        """Test that _refs remains empty throughout node lifecycle."""
        node = GraphNode(42, "node1")
        assert len(node._refs) == 0

        node.data = 100
        assert len(node._refs) == 0

    def test_graph_node_does_not_expose_connection_properties(self):
        """Test that GraphNode doesn't have next/left/right/children properties."""
        node = GraphNode(42, "node1")

        # These properties should not exist on GraphNode
        assert not hasattr(node, "next")
        assert not hasattr(node, "prev")
        assert not hasattr(node, "left")
        assert not hasattr(node, "right")
        assert not hasattr(node, "children")


class TestGraphNodeEdgeCases:
    """Tests for edge cases."""

    def test_graph_node_with_none_data(self):
        """Test creating graph node with None data."""
        node = GraphNode(None, "node1")
        assert node.data is None

    def test_graph_node_with_empty_string_id(self):
        """Test creating graph node with empty string ID."""
        node = GraphNode(42, "")
        assert node.id == ""

    def test_graph_node_equality_with_empty_id(self):
        """Test equality when nodes have empty string IDs."""
        node1 = GraphNode("A", "")
        node2 = GraphNode("B", "")
        assert node1 == node2  # Both have empty ID

    def test_multiple_nodes_with_auto_ids_are_unique(self):
        """Test that multiple nodes with auto IDs have unique IDs."""
        nodes = [GraphNode(i) for i in range(100)]
        ids = [node.id for node in nodes]
        assert len(ids) == len(set(ids))  # All IDs are unique
