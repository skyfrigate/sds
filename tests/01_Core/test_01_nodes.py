import pytest

from sds.core.node import DoublyNode, Node


class TestNode:
    """Tests for the Node class (singly linked)."""

    def test_node_creation_with_data_only(self):
        """Test creating a node with only data."""
        node = Node(42)

        assert node.data == 42
        assert node.next is None

    def test_node_creation_with_data_and_next(self):
        """Test creating a node with data and next reference."""
        next_node = Node(10)
        node = Node(42, next_node)

        assert node.data == 42
        assert node.next is next_node
        assert node.next.data == 10

    def test_node_accepts_various_data_types(self, various_data_types):
        """Test that Node can store various data types using fixture.

        This test will run once for each value in the various_data_types fixture.
        """
        node = Node(various_data_types[0])
        assert node.data == various_data_types[0]
        assert type(node.data) is various_data_types[1]

    def test_node_next_can_be_modified(self):
        """Test that the next reference can be modified."""
        node1 = Node(1)
        node2 = Node(2)

        assert node1.next is None

        node1.next = node2
        assert node1.next is node2
        assert node1.next.data == 2

    def test_node_data_can_be_modified(self, simple_node):
        """Test that node data can be modified using fixture."""
        assert simple_node.data == 42

        simple_node.data = 100
        assert simple_node.data == 100

    def test_node_data_property_getter(self, simple_node):
        """Test that data property getter works correctly using fixture."""
        # Access via property
        assert simple_node.data == 42

        # Private attribute should exist
        assert hasattr(simple_node, "_data")
        assert simple_node._data == 42

    def test_node_data_property_setter(self, simple_node):
        """Test that data property setter works correctly using fixture."""
        # Modify via property
        simple_node.data = 100

        assert simple_node.data == 100
        assert simple_node._data == 100

    def test_node_next_property_getter(self):
        """Test that next property getter works correctly."""
        next_node = Node(10)
        node = Node(42, next_node)

        # Access via property
        assert node.next is next_node

        # Private attribute should exist
        assert hasattr(node, "_next")
        assert node._next is next_node

    def test_node_next_property_setter(self):
        """Test that next property setter works correctly."""
        node1 = Node(1)
        node2 = Node(2)

        # Modify via property
        node1.next = node2

        assert node1.next is node2
        assert node1._next is node2

    def test_node_chain_creation(self, node_chain):
        """Test working with a chain of nodes using fixture."""
        assert node_chain.data == 1
        assert node_chain.next.data == 2
        assert node_chain.next.next.data == 3
        assert node_chain.next.next.next is None

    def test_node_chain_traversal(self, node_chain):
        """Test traversing a chain of nodes using fixture."""
        # Collect all values by traversing
        values = []
        current = node_chain
        while current is not None:
            values.append(current.data)
            current = current.next

        assert values == [1, 2, 3]

    def test_node_repr(self):
        """Test the __repr__ method."""
        node = Node(42)
        assert repr(node) == "Node(42)"

        node_str = Node("hello")
        assert repr(node_str) == "Node('hello')"

    def test_node_str(self):
        """Test the __str__ method."""
        node = Node(42)
        assert str(node) == "42"

        node_str = Node("hello")
        assert str(node_str) == "hello"

    def test_node_with_node_as_data(self):
        """Test creating a node with another node as data."""
        inner_node = Node(10)
        outer_node = Node(inner_node)

        assert outer_node.data is inner_node
        assert outer_node.data.data == 10

    def test_multiple_nodes_independence(self):
        """Test that multiple nodes are independent."""
        node1 = Node(1)
        node2 = Node(2)

        assert node1.data != node2.data
        assert node1 is not node2

        node1.data = 100
        assert node2.data == 2  # node2 should not be affected

    def test_node_cannot_access_private_attributes_via_public_names(self, simple_node):
        """Test that private attributes are properly encapsulated using fixture."""
        # Can access via properties
        assert simple_node.data == 42
        assert simple_node.next is None

        # Private attributes exist
        assert hasattr(simple_node, "_data")
        assert hasattr(simple_node, "_next")


class TestDoublyNode:
    """Tests for the DoublyNode class (doubly linked)."""

    def test_doubly_node_creation_with_data_only(self):
        """Test creating a doubly node with only data."""
        node = DoublyNode(42)

        assert node.data == 42
        assert node.next is None
        assert node.prev is None

    def test_doubly_node_creation_with_all_parameters(self):
        """Test creating a doubly node with all parameters."""
        prev_node = DoublyNode(10)
        next_node = DoublyNode(20)
        node = DoublyNode(42, next_node, prev_node)

        assert node.data == 42
        assert node.next is next_node
        assert node.prev is prev_node

    def test_doubly_node_accepts_various_data_types(self, various_data_types):
        """Test that DoublyNode can store various data types using fixture.

        This test will run once for each value in the various_data_types fixture.
        """
        node = DoublyNode(various_data_types[0])
        assert node.data == various_data_types[0]
        assert type(node.data) is various_data_types[1]

    def test_doubly_node_next_can_be_modified(self):
        """Test that the next reference can be modified."""
        node1 = DoublyNode(1)
        node2 = DoublyNode(2)

        assert node1.next is None

        node1.next = node2
        assert node1.next is node2

    def test_doubly_node_prev_can_be_modified(self):
        """Test that the prev reference can be modified."""
        node1 = DoublyNode(1)
        node2 = DoublyNode(2)

        assert node2.prev is None

        node2.prev = node1
        assert node2.prev is node1

    def test_doubly_node_data_can_be_modified(self, simple_doubly_node):
        """Test that node data can be modified using fixture."""
        assert simple_doubly_node.data == 42

        simple_doubly_node.data = 100
        assert simple_doubly_node.data == 100

    def test_doubly_node_data_property_getter(self, simple_doubly_node):
        """Test that data property getter works correctly using fixture."""
        # Access via property
        assert simple_doubly_node.data == 42

        # Private attribute should exist
        assert hasattr(simple_doubly_node, "_data")
        assert simple_doubly_node._data == 42

    def test_doubly_node_data_property_setter(self, simple_doubly_node):
        """Test that data property setter works correctly using fixture."""
        # Modify via property
        simple_doubly_node.data = 100

        assert simple_doubly_node.data == 100
        assert simple_doubly_node._data == 100

    def test_doubly_node_next_property_getter(self):
        """Test that next property getter works correctly."""
        next_node = DoublyNode(10)
        node = DoublyNode(42, next_node=next_node)

        # Access via property
        assert node.next is next_node

        # Private attribute should exist
        assert hasattr(node, "_next")
        assert node._next is next_node

    def test_doubly_node_next_property_setter(self):
        """Test that next property setter works correctly."""
        node1 = DoublyNode(1)
        node2 = DoublyNode(2)

        # Modify via property
        node1.next = node2

        assert node1.next is node2
        assert node1._next is node2

    def test_doubly_node_prev_property_getter(self):
        """Test that prev property getter works correctly."""
        prev_node = DoublyNode(10)
        node = DoublyNode(42, prev_node=prev_node)

        # Access via property
        assert node.prev is prev_node

        # Private attribute should exist
        assert hasattr(node, "_prev")
        assert node._prev is prev_node

    def test_doubly_node_prev_property_setter(self):
        """Test that prev property setter works correctly."""
        node1 = DoublyNode(1)
        node2 = DoublyNode(2)

        # Modify via property
        node2.prev = node1

        assert node2.prev is node1
        assert node2._prev is node1

    def test_doubly_node_bidirectional_chain_creation(self, doubly_node_chain):
        """Test working with a bidirectional chain using fixture."""
        # Forward traversal
        assert doubly_node_chain.data == 1
        assert doubly_node_chain.next.data == 2
        assert doubly_node_chain.next.next.data == 3
        assert doubly_node_chain.next.next.next is None

        # Backward traversal
        node3 = doubly_node_chain.next.next
        assert node3.data == 3
        assert node3.prev.data == 2
        assert node3.prev.prev.data == 1
        assert node3.prev.prev.prev is None

    def test_doubly_node_chain_forward_traversal(self, doubly_node_chain):
        """Test forward traversal of a doubly linked chain using fixture."""
        values = []
        current = doubly_node_chain
        while current is not None:
            values.append(current.data)
            current = current.next

        assert values == [1, 2, 3]

    def test_doubly_node_chain_backward_traversal(self, doubly_node_chain):
        """Test backward traversal of a doubly linked chain using fixture."""
        # First, go to the end
        current = doubly_node_chain
        while current.next is not None:
            current = current.next

        # Now traverse backward
        values = []
        while current is not None:
            values.append(current.data)
            current = current.prev

        assert values == [3, 2, 1]

    def test_doubly_node_repr(self):
        """Test the __repr__ method."""
        node = DoublyNode(42)
        assert repr(node) == "DoublyNode(42)"

        node_str = DoublyNode("hello")
        assert repr(node_str) == "DoublyNode('hello')"

    def test_doubly_node_str(self):
        """Test the __str__ method."""
        node = DoublyNode(42)
        assert str(node) == "42"

        node_str = DoublyNode("hello")
        assert str(node_str) == "hello"

    def test_doubly_node_symmetric_linking(self):
        """Test that nodes can be symmetrically linked."""
        node1 = DoublyNode(1)
        node2 = DoublyNode(2)

        # Link them
        node1.next = node2
        node2.prev = node1

        # Verify symmetry
        assert node1.next is node2
        assert node2.prev is node1
        assert node1.next.prev is node1
        assert node2.prev.next is node2

    def test_doubly_node_with_doubly_node_as_data(self):
        """Test creating a doubly node with another doubly node as data."""
        inner_node = DoublyNode(10)
        outer_node = DoublyNode(inner_node)

        assert outer_node.data is inner_node
        assert outer_node.data.data == 10

    def test_multiple_doubly_nodes_independence(self):
        """Test that multiple doubly nodes are independent."""
        node1 = DoublyNode(1)
        node2 = DoublyNode(2)

        assert node1.data != node2.data
        assert node1 is not node2

        node1.data = 100
        assert node2.data == 2  # node2 should not be affected

    def test_doubly_node_cannot_access_private_attributes_via_public_names(
        self, simple_doubly_node
    ):
        """Test that private attributes are properly encapsulated using fixture."""
        # Can access via properties
        assert simple_doubly_node.data == 42
        assert simple_doubly_node.next is None
        assert simple_doubly_node.prev is None

        # Private attributes exist
        assert hasattr(simple_doubly_node, "_data")
        assert hasattr(simple_doubly_node, "_next")
        assert hasattr(simple_doubly_node, "_prev")


class TestNodeVsDoublyNode:
    """Comparison tests between Node and DoublyNode."""

    def test_node_has_no_prev_attribute(self, simple_node):
        """Test that Node doesn't have a prev attribute using fixture."""
        assert hasattr(simple_node, "data")
        assert hasattr(simple_node, "next")
        assert not hasattr(simple_node, "prev")

        # But has private attributes
        assert hasattr(simple_node, "_data")
        assert hasattr(simple_node, "_next")
        assert not hasattr(simple_node, "_prev")

    def test_doubly_node_has_prev_attribute(self, simple_doubly_node):
        """Test that DoublyNode has a prev attribute using fixture."""
        assert hasattr(simple_doubly_node, "data")
        assert hasattr(simple_doubly_node, "next")
        assert hasattr(simple_doubly_node, "prev")

        # And has all private attributes
        assert hasattr(simple_doubly_node, "_data")
        assert hasattr(simple_doubly_node, "_next")
        assert hasattr(simple_doubly_node, "_prev")

    def test_node_and_doubly_node_can_store_same_data(self, various_data_types):
        """Test that both node types can store the same data using fixture."""
        node = Node(various_data_types)
        doubly_node = DoublyNode(various_data_types)

        assert node.data == doubly_node.data
        assert node.data is various_data_types
        assert doubly_node.data is various_data_types

    def test_slots_usage_node(self, simple_node):
        """Test that Node uses __slots__ for memory efficiency using fixture."""
        # __slots__ should prevent dynamic attribute creation
        with pytest.raises(AttributeError):
            simple_node.custom_attribute = "test"

    def test_slots_usage_doubly_node(self, simple_doubly_node):
        """Test that DoublyNode uses __slots__ for memory efficiency using fixture."""
        # __slots__ should prevent dynamic attribute creation
        with pytest.raises(AttributeError):
            simple_doubly_node.custom_attribute = "test"

    def test_node_properties_are_writable(self, simple_node):
        """Test that Node properties can be written to using fixture."""
        # Test data property
        simple_node.data = 100
        assert simple_node.data == 100

        # Test next property
        node2 = Node(200)
        simple_node.next = node2
        assert simple_node.next is node2

    def test_doubly_node_properties_are_writable(self, simple_doubly_node):
        """Test that DoublyNode properties can be written to using fixture."""
        # Test data property
        simple_doubly_node.data = 100
        assert simple_doubly_node.data == 100

        # Test next property
        node2 = DoublyNode(200)
        simple_doubly_node.next = node2
        assert simple_doubly_node.next is node2

        # Test prev property
        node0 = DoublyNode(0)
        simple_doubly_node.prev = node0
        assert simple_doubly_node.prev is node0


class TestNodeProperties:
    """Specific tests for Node properties behavior."""

    def test_node_data_property_is_property_object(self):
        """Test that data is indeed a property."""
        assert isinstance(Node.data, property)

    def test_node_next_property_is_property_object(self):
        """Test that next is indeed a property."""
        assert isinstance(Node.next, property)

    def test_node_data_setter_accepts_none(self, simple_node):
        """Test that data setter accepts None using fixture."""
        simple_node.data = None
        assert simple_node.data is None

    def test_node_next_setter_accepts_none(self):
        """Test that next setter accepts None."""
        node1 = Node(1)
        node2 = Node(2)

        node1.next = node2
        assert node1.next is node2

        node1.next = None
        assert node1.next is None

    def test_node_data_setter_with_various_types(self, various_data_types):
        """Test that data setter accepts various types using fixture."""
        node = Node(0)
        node.data = various_data_types
        assert node.data == various_data_types
        assert node.data is various_data_types


class TestDoublyNodeProperties:
    """Specific tests for DoublyNode properties behavior."""

    def test_doubly_node_data_property_is_property_object(self):
        """Test that data is indeed a property."""
        assert isinstance(DoublyNode.data, property)

    def test_doubly_node_next_property_is_property_object(self):
        """Test that next is indeed a property."""
        assert isinstance(DoublyNode.next, property)

    def test_doubly_node_prev_property_is_property_object(self):
        """Test that prev is indeed a property."""
        assert isinstance(DoublyNode.prev, property)

    def test_doubly_node_data_setter_accepts_none(self, simple_doubly_node):
        """Test that data setter accepts None using fixture."""
        simple_doubly_node.data = None
        assert simple_doubly_node.data is None

    def test_doubly_node_next_setter_accepts_none(self):
        """Test that next setter accepts None."""
        node1 = DoublyNode(1)
        node2 = DoublyNode(2)

        node1.next = node2
        assert node1.next is node2

        node1.next = None
        assert node1.next is None

    def test_doubly_node_prev_setter_accepts_none(self):
        """Test that prev setter accepts None."""
        node1 = DoublyNode(1)
        node2 = DoublyNode(2)

        node2.prev = node1
        assert node2.prev is node1

        node2.prev = None
        assert node2.prev is None

    def test_doubly_node_data_setter_with_various_types(self, various_data_types):
        """Test that data setter accepts various types using fixture."""
        node = DoublyNode(0)
        node.data = various_data_types
        assert node.data == various_data_types
        assert node.data is various_data_types


class TestNodeChainManipulation:
    """Tests for manipulating node chains using fixtures."""

    def test_insert_node_in_chain(self, node_chain):
        """Test inserting a node in the middle of a chain using fixture."""
        # Chain is: 1 -> 2 -> 3
        # Insert 1.5 between 1 and 2
        new_node = Node(1.5)
        new_node.next = node_chain.next
        node_chain.next = new_node

        # Chain should now be: 1 -> 1.5 -> 2 -> 3
        assert node_chain.data == 1
        assert node_chain.next.data == 1.5
        assert node_chain.next.next.data == 2
        assert node_chain.next.next.next.data == 3

    def test_remove_node_from_chain(self, node_chain):
        """Test removing a node from a chain using fixture."""
        # Chain is: 1 -> 2 -> 3
        # Remove node 2
        node_chain.next = node_chain.next.next

        # Chain should now be: 1 -> 3
        assert node_chain.data == 1
        assert node_chain.next.data == 3
        assert node_chain.next.next is None


class TestDoublyNodeChainManipulation:
    """Tests for manipulating doubly linked chains using fixtures."""

    def test_insert_node_in_doubly_chain(self, doubly_node_chain):
        """Test inserting a node in a doubly linked chain using fixture."""
        # Chain is: 1 <-> 2 <-> 3
        # Insert 1.5 between 1 and 2
        new_node = DoublyNode(1.5)

        node1 = doubly_node_chain
        node2 = doubly_node_chain.next

        new_node.next = node2
        new_node.prev = node1
        node1.next = new_node
        node2.prev = new_node

        # Chain should now be: 1 <-> 1.5 <-> 2 <-> 3
        assert doubly_node_chain.data == 1
        assert doubly_node_chain.next.data == 1.5
        assert doubly_node_chain.next.next.data == 2
        assert doubly_node_chain.next.next.next.data == 3

        # Verify backward links
        assert doubly_node_chain.next.prev.data == 1
        assert doubly_node_chain.next.next.prev.data == 1.5

    def test_remove_node_from_doubly_chain(self, doubly_node_chain):
        """Test removing a node from a doubly linked chain using fixture."""
        # Chain is: 1 <-> 2 <-> 3
        # Remove node 2
        node1 = doubly_node_chain
        # node2 = doubly_node_chain.next
        node3 = doubly_node_chain.next.next

        node1.next = node3
        node3.prev = node1

        # Chain should now be: 1 <-> 3
        assert doubly_node_chain.data == 1
        assert doubly_node_chain.next.data == 3
        assert doubly_node_chain.next.next is None

        # Verify backward link
        assert doubly_node_chain.next.prev.data == 1
