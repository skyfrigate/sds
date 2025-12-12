# Copyright 2024-2025, skyfrigate, biface
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for adjacency-based graph implementations.

This module contains comprehensive tests for AdjacencyListGraph and
AdjacencyMatrixGraph classes, verifying correct behavior for different
internal representations.
"""

import pytest

from sds.graph import AdjacencyListGraph, AdjacencyMatrixGraph, Edge, GraphNode


class TestAdjacencyListGraphCreation:
    """Test adjacency list graph creation."""

    def test_empty_graph_creation(self) -> None:
        """Test creating an empty adjacency list graph."""
        g = AdjacencyListGraph()
        assert g.is_empty()
        assert g.node_count() == 0
        assert g.edge_count() == 0

    def test_multigraph_creation(self) -> None:
        """Test creating a multigraph."""
        g = AdjacencyListGraph(allow_multi_edges=True)
        assert g.allow_multi_edges


class TestAdjacencyListOperations:
    """Test adjacency list specific operations."""

    def test_get_adjacency_list(self) -> None:
        """Test getting adjacency list for a node."""
        g = AdjacencyListGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for n in nodes:
            g.add_node(n)
        g.add_edge(Edge(nodes[0], nodes[1]))
        g.add_edge(Edge(nodes[0], nodes[2]))
        adj = g.get_adjacency_list("n0")
        assert "n1" in adj
        assert "n2" in adj
        assert len(adj) == 2

    def test_get_adjacency_list_nonexistent_node(self) -> None:
        """Test getting adjacency list for nonexistent node."""
        g = AdjacencyListGraph()
        with pytest.raises(ValueError, match="not in graph"):
            g.get_adjacency_list("nonexistent")

    def test_adjacency_list_isolation(self) -> None:
        """Test that returned adjacency list is a copy."""
        g = AdjacencyListGraph()
        n1, n2 = GraphNode("A", "n1"), GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(Edge(n1, n2))
        adj = g.get_adjacency_list("n1")
        adj.clear()  # Modify copy
        assert len(g.get_adjacency_list("n1")) == 1  # Original unchanged


class TestAdjacencyListBasicOperations:
    """Test basic graph operations for adjacency list."""

    def test_add_node(self) -> None:
        """Test adding nodes."""
        g = AdjacencyListGraph()
        n1 = GraphNode("A", "n1")
        g.add_node(n1)
        assert g.has_node(n1)
        assert g.node_count() == 1

    def test_add_edge(self) -> None:
        """Test adding edges."""
        g = AdjacencyListGraph()
        n1, n2 = GraphNode("A", "n1"), GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(Edge(n1, n2))
        assert g.has_edge(n1, n2)
        assert g.has_edge(n2, n1)  # Undirected

    def test_neighbors(self) -> None:
        """Test getting neighbors."""
        g = AdjacencyListGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for n in nodes:
            g.add_node(n)
        g.add_edge(Edge(nodes[0], nodes[1]))
        g.add_edge(Edge(nodes[0], nodes[2]))
        neighbors = sorted([n.id for n in g.neighbors(nodes[0])])
        assert neighbors == ["n1", "n2"]

    def test_is_connected(self) -> None:
        """Test connectivity check."""
        g = AdjacencyListGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for n in nodes:
            g.add_node(n)
        g.add_edge(Edge(nodes[0], nodes[1]))
        g.add_edge(Edge(nodes[1], nodes[2]))
        assert g.is_connected()


class TestAdjacencyMatrixGraphCreation:
    """Test adjacency matrix graph creation."""

    def test_empty_graph_creation(self) -> None:
        """Test creating an empty adjacency matrix graph."""
        g = AdjacencyMatrixGraph()
        assert g.is_empty()
        assert g.max_nodes == 100

    def test_custom_max_nodes(self) -> None:
        """Test creating graph with custom max nodes."""
        g = AdjacencyMatrixGraph(max_nodes=50)
        assert g.max_nodes == 50

    def test_invalid_max_nodes_raises_error(self) -> None:
        """Test that invalid max_nodes raises ValueError."""
        with pytest.raises(ValueError, match="must be positive"):
            AdjacencyMatrixGraph(max_nodes=0)
        with pytest.raises(ValueError, match="must be positive"):
            AdjacencyMatrixGraph(max_nodes=-5)


class TestAdjacencyMatrixOperations:
    """Test adjacency matrix specific operations."""

    def test_get_matrix(self) -> None:
        """Test getting the adjacency matrix."""
        g = AdjacencyMatrixGraph(max_nodes=5)
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for n in nodes:
            g.add_node(n)
        g.add_edge(Edge(nodes[0], nodes[1]))
        g.add_edge(Edge(nodes[1], nodes[2]))
        matrix = g.get_matrix()
        assert len(matrix) == 3
        assert len(matrix[0]) == 3
        assert matrix[0][1] == 1  # Edge 0-1
        assert matrix[1][2] == 1  # Edge 1-2
        assert matrix[0][2] == 0  # No edge 0-2

    def test_matrix_symmetry(self) -> None:
        """Test that matrix is symmetric for undirected graph."""
        g = AdjacencyMatrixGraph(max_nodes=5)
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for n in nodes:
            g.add_node(n)
        g.add_edge(Edge(nodes[0], nodes[2]))
        matrix = g.get_matrix()
        assert matrix[0][2] == matrix[2][0]  # Symmetric

    def test_matrix_isolation(self) -> None:
        """Test that returned matrix is a copy."""
        g = AdjacencyMatrixGraph(max_nodes=5)
        n1, n2 = GraphNode("A", "n1"), GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(Edge(n1, n2))
        matrix = g.get_matrix()
        matrix[0][1] = 99  # Modify copy
        assert g.get_matrix()[0][1] == 1  # Original unchanged


class TestAdjacencyMatrixBasicOperations:
    """Test basic graph operations for adjacency matrix."""

    def test_add_node(self) -> None:
        """Test adding nodes."""
        g = AdjacencyMatrixGraph(max_nodes=5)
        n1 = GraphNode("A", "n1")
        g.add_node(n1)
        assert g.has_node(n1)

    def test_add_node_exceeds_capacity(self) -> None:
        """Test adding node beyond capacity raises error."""
        g = AdjacencyMatrixGraph(max_nodes=2)
        g.add_node(GraphNode("A", "n1"))
        g.add_node(GraphNode("B", "n2"))
        with pytest.raises(ValueError, match="full"):
            g.add_node(GraphNode("C", "n3"))

    def test_add_edge(self) -> None:
        """Test adding edges updates matrix."""
        g = AdjacencyMatrixGraph(max_nodes=5)
        n1, n2 = GraphNode("A", "n1"), GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(Edge(n1, n2))
        assert g.has_edge(n1, n2)
        assert g.get_matrix()[0][1] == 1

    def test_remove_edge(self) -> None:
        """Test removing edge updates matrix."""
        g = AdjacencyMatrixGraph(max_nodes=5)
        n1, n2 = GraphNode("A", "n1"), GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        edge = Edge(n1, n2)
        g.add_edge(edge)
        g.remove_edge(edge)
        assert not g.has_edge(n1, n2)
        assert g.get_matrix()[0][1] == 0

    def test_remove_node_compacts_matrix(self) -> None:
        """Test that removing node compacts matrix properly."""
        g = AdjacencyMatrixGraph(max_nodes=5)
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for n in nodes:
            g.add_node(n)
        g.add_edge(Edge(nodes[0], nodes[1]))
        g.add_edge(Edge(nodes[1], nodes[2]))
        g.remove_node(nodes[1])
        assert g.node_count() == 2
        assert not g.has_edge(nodes[0], nodes[2])

    def test_neighbors(self) -> None:
        """Test getting neighbors from matrix."""
        g = AdjacencyMatrixGraph(max_nodes=5)
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for n in nodes:
            g.add_node(n)
        g.add_edge(Edge(nodes[0], nodes[1]))
        g.add_edge(Edge(nodes[0], nodes[2]))
        neighbors = sorted([n.id for n in g.neighbors(nodes[0])])
        assert neighbors == ["n1", "n2"]

    def test_degree(self) -> None:
        """Test degree calculation with matrix."""
        g = AdjacencyMatrixGraph(max_nodes=5)
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(4)]
        for n in nodes:
            g.add_node(n)
        g.add_edge(Edge(nodes[0], nodes[1]))
        g.add_edge(Edge(nodes[0], nodes[2]))
        g.add_edge(Edge(nodes[0], nodes[3]))
        assert g.degree(nodes[0]) == 3


class TestMultiEdges:
    """Test multi-edge support."""

    def test_adjacency_list_multi_edges(self) -> None:
        """Test adjacency list allows multi-edges."""
        g = AdjacencyListGraph(allow_multi_edges=True)
        n1, n2 = GraphNode("A", "n1"), GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(Edge(n1, n2, data="edge1"))
        g.add_edge(Edge(n1, n2, data="edge2"))
        assert g.edge_count() == 2

    def test_adjacency_matrix_multi_edges(self) -> None:
        """Test adjacency matrix counts multi-edges."""
        g = AdjacencyMatrixGraph(max_nodes=5, allow_multi_edges=True)
        n1, n2 = GraphNode("A", "n1"), GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(Edge(n1, n2))
        g.add_edge(Edge(n1, n2))
        matrix = g.get_matrix()
        assert matrix[0][1] == 2  # Two edges


class TestConnectivity:
    """Test connectivity for both representations."""

    def test_adjacency_list_connected(self) -> None:
        """Test connected graph detection in adjacency list."""
        g = AdjacencyListGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(4)]
        for n in nodes:
            g.add_node(n)
        g.add_edge(Edge(nodes[0], nodes[1]))
        g.add_edge(Edge(nodes[1], nodes[2]))
        g.add_edge(Edge(nodes[2], nodes[3]))
        assert g.is_connected()

    def test_adjacency_list_disconnected(self) -> None:
        """Test disconnected graph detection in adjacency list."""
        g = AdjacencyListGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(4)]
        for n in nodes:
            g.add_node(n)
        g.add_edge(Edge(nodes[0], nodes[1]))
        g.add_edge(Edge(nodes[2], nodes[3]))
        assert not g.is_connected()

    def test_adjacency_matrix_connected(self) -> None:
        """Test connected graph detection in adjacency matrix."""
        g = AdjacencyMatrixGraph(max_nodes=5)
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(4)]
        for n in nodes:
            g.add_node(n)
        g.add_edge(Edge(nodes[0], nodes[1]))
        g.add_edge(Edge(nodes[1], nodes[2]))
        g.add_edge(Edge(nodes[2], nodes[3]))
        assert g.is_connected()

    def test_adjacency_matrix_disconnected(self) -> None:
        """Test disconnected graph detection in adjacency matrix."""
        g = AdjacencyMatrixGraph(max_nodes=5)
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(4)]
        for n in nodes:
            g.add_node(n)
        g.add_edge(Edge(nodes[0], nodes[1]))
        g.add_edge(Edge(nodes[2], nodes[3]))
        assert not g.is_connected()


class TestClearOperation:
    """Test clearing graphs."""

    def test_adjacency_list_clear(self) -> None:
        """Test clearing adjacency list graph."""
        g = AdjacencyListGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for n in nodes:
            g.add_node(n)
        g.add_edge(Edge(nodes[0], nodes[1]))
        g.clear()
        assert g.is_empty()
        assert g.node_count() == 0

    def test_adjacency_matrix_clear(self) -> None:
        """Test clearing adjacency matrix graph."""
        g = AdjacencyMatrixGraph(max_nodes=5)
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for n in nodes:
            g.add_node(n)
        g.add_edge(Edge(nodes[0], nodes[1]))
        g.clear()
        assert g.is_empty()
        matrix = g.get_matrix()
        assert len(matrix) == 0


class TestSpecialMethods:
    """Test dunder methods."""

    def test_adjacency_list_repr(self) -> None:
        """Test __repr__ for adjacency list."""
        g = AdjacencyListGraph()
        assert "AdjacencyListGraph" in repr(g)
        assert "nodes=0" in repr(g)

    def test_adjacency_matrix_repr(self) -> None:
        """Test __repr__ for adjacency matrix."""
        g = AdjacencyMatrixGraph(max_nodes=50)
        assert "AdjacencyMatrixGraph" in repr(g)
        assert "max_nodes=50" in repr(g)

    def test_len_and_contains(self) -> None:
        """Test __len__ and __contains__ for both types."""
        for GraphClass in [AdjacencyListGraph, AdjacencyMatrixGraph]:
            g = GraphClass() if GraphClass == AdjacencyListGraph else GraphClass(max_nodes=5)  # type: ignore
            n1 = GraphNode("A", "n1")
            assert len(g) == 0
            assert n1 not in g
            g.add_node(n1)
            assert len(g) == 1
            assert n1 in g


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_get_edge_nonexistent(self) -> None:
        """Test getting nonexistent edge returns None."""
        for GraphClass in [AdjacencyListGraph, AdjacencyMatrixGraph]:
            g = GraphClass() if GraphClass == AdjacencyListGraph else GraphClass(max_nodes=5)  # type: ignore
            n1, n2 = GraphNode("A", "n1"), GraphNode("B", "n2")
            g.add_node(n1)
            g.add_node(n2)
            assert g.get_edge(n1, n2) is None

    def test_neighbors_isolated_node(self) -> None:
        """Test neighbors of isolated node."""
        g = AdjacencyListGraph()
        n1 = GraphNode("A", "n1")
        g.add_node(n1)
        neighbors = list(g.neighbors(n1))
        assert len(neighbors) == 0

    def test_degree_isolated_node(self) -> None:
        """Test degree of isolated node is zero."""
        g = AdjacencyMatrixGraph(max_nodes=5)
        n1 = GraphNode("A", "n1")
        g.add_node(n1)
        assert g.degree(n1) == 0
