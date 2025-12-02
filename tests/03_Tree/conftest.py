"""Shared fixtures for trees module tests."""

import pytest

from sds.tree.node import BinaryNode, TreeNode

# ============================================================================
# BinaryNode Fixtures
# ============================================================================


@pytest.fixture
def simple_binary_node():
    """Create a simple binary node with data 42.

    Returns
    -------
    BinaryNode
        A binary node with data value 42, no children, and no parent.
    """
    return BinaryNode(42)


@pytest.fixture
def binary_tree_structure():
    """Create a simple binary tree structure:
           10
          /  \\
         5    15
        / \\
       2   7

    Returns
    -------
    BinaryNode
        The root node of the binary tree with data 10.
    """
    root = BinaryNode(10)
    root.left = BinaryNode(5)
    root.right = BinaryNode(15)
    root.left.left = BinaryNode(2)
    root.left.right = BinaryNode(7)
    return root


# ============================================================================
# TreeNode Fixtures
# ============================================================================


@pytest.fixture
def simple_tree_node():
    """Create a simple tree node with data 42.

    Returns
    -------
    TreeNode
        A tree node with data value 42, no children, and no parent.
    """
    return TreeNode(42)


@pytest.fixture
def tree_structure():
    """Create a simple tree structure:
              A
            / | \\
           B  C  D
          /|
         E F

    Returns
    -------
    TreeNode
        The root node of the tree with data "A".
    """
    root = TreeNode("A")
    b = TreeNode("B")
    c = TreeNode("C")
    d = TreeNode("D")
    e = TreeNode("E")
    f = TreeNode("F")

    root.add_child(b)
    root.add_child(c)
    root.add_child(d)
    b.add_child(e)
    b.add_child(f)

    return root


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
