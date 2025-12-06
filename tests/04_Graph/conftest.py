"""Shared fixtures for graphs module tests."""

import pytest

from sds.graph.node import GraphNode

# ============================================================================
# GraphNode Fixtures
# ============================================================================


@pytest.fixture
def simple_graph_node():
    """Create a simple graph node with data 42 and custom ID.

    Returns
    -------
    GraphNode
        A graph node with data value 42 and id "node1".
    """
    return GraphNode(42, "node1")


@pytest.fixture
def graph_nodes():
    """Create a collection of graph nodes for testing.

    Returns
    -------
    dict
        Dictionary with node IDs as keys and GraphNode objects as values.
    """
    return {
        "A": GraphNode("Node A", "A"),
        "B": GraphNode("Node B", "B"),
        "C": GraphNode("Node C", "C"),
        "D": GraphNode("Node D", "D"),
        "E": GraphNode("Node E", "E"),
    }


@pytest.fixture
def auto_id_nodes():
    """Create nodes with auto-generated IDs.

    Returns
    -------
    list
        List of GraphNode objects with auto-generated UUIDs.
    """
    return [GraphNode(i) for i in range(5)]


# ============================================================================
# Parametrized Fixtures
# ============================================================================


@pytest.fixture(
    params=[
        0,
        42,
        -10,
        3.14,
        -2.5,
        "string",
        "hello world",
        "",
        [],
        [1, 2, 3],
        {},
        {"key": "value"},
        True,
        False,
        None,
    ]
)
def sample_values(request):
    """Provide various data types for testing nodes.

    This fixture is parametrized to return different types of data.

    Parameters
    ----------
    request : FixtureRequest
        pytest fixture request object.

    Returns
    -------
    Any
        One of the parametrized values.
    """
    return request.param
