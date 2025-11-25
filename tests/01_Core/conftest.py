"""Configuration and fixtures for core module tests."""

from types import NoneType

import pytest

from sds.core.node import DoublyNode, Node


@pytest.fixture
def simple_node():
    """Provide a simple Node with integer data."""
    return Node(42)


@pytest.fixture
def node_chain():
    """Provide a chain of 3 connected nodes: 1 -> 2 -> 3."""
    node3 = Node(3)
    node2 = Node(2, node3)
    node1 = Node(1, node2)
    return node1


@pytest.fixture
def simple_doubly_node():
    """Provide a simple DoublyNode with integer data."""
    return DoublyNode(42)


@pytest.fixture
def doubly_node_chain():
    """Provide a bidirectional chain of 3 nodes: 1 <-> 2 <-> 3."""
    node1 = DoublyNode(1)
    node2 = DoublyNode(2)
    node3 = DoublyNode(3)

    # Link forward
    node1.next = node2
    node2.next = node3

    # Link backward
    node2.prev = node1
    node3.prev = node2

    return node1


@pytest.fixture(
    params=[
        (0, int),
        (42, int),
        (-10, int),
        (3.14, float),
        ("hello", str),
        ("world", str),
        ([1, 2, 3], list),
        ({"key": "value"}, dict),
        ((1, 2), tuple),
        (None, NoneType),
    ]
)
def various_data_types(request):
    """Provide various data types for parametrized tests."""
    return request.param
