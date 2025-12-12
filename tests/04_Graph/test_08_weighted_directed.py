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

"""Tests for WeightedDirectedGraph class.

This module contains comprehensive tests for the WeightedDirectedGraph
implementation, covering node/edge operations, weight management,
directed graph properties, and edge cases.
"""

import pytest

from sds.graph import (
    GraphNode,
    WeightedDirectedEdge,
    WeightedDirectedGraph,
    WeightedEdge,
)


class TestWeightedDirectedGraphCreation:
    """Test graph creation and initialization."""

    def test_empty_graph_creation(self) -> None:
        """Test creating an empty weighted directed graph."""
        g = WeightedDirectedGraph()
        assert g.is_empty()
        assert g.node_count() == 0
        assert g.edge_count() == 0
        assert not g.allow_multi_edges

    def test_multigraph_creation(self) -> None:
        """Test creating a multi-digraph."""
        g = WeightedDirectedGraph(allow_multi_edges=True)
        assert g.allow_multi_edges
        assert g.is_empty()


class TestNodeOperations:
    """Test node addition, removal, and queries."""

    def test_add_node(self) -> None:
        """Test adding nodes to the graph."""
        g = WeightedDirectedGraph()
        n1 = GraphNode("A", "n1")
        g.add_node(n1)
        assert g.has_node(n1)
        assert g.node_count() == 1

    def test_add_duplicate_node_raises_error(self) -> None:
        """Test that adding duplicate node raises ValueError."""
        g = WeightedDirectedGraph()
        n1 = GraphNode("A", "n1")
        g.add_node(n1)
        with pytest.raises(ValueError, match="already exists"):
            g.add_node(n1)

    def test_add_invalid_node_raises_error(self) -> None:
        """Test that adding non-GraphNode raises TypeError."""
        g = WeightedDirectedGraph()
        with pytest.raises(TypeError):
            g.add_node("not a node")  # type: ignore

    def test_remove_node(self) -> None:
        """Test removing a node."""
        g = WeightedDirectedGraph()
        n1 = GraphNode("A", "n1")
        g.add_node(n1)
        g.remove_node(n1)
        assert not g.has_node(n1)
        assert g.is_empty()

    def test_remove_node_with_edges(self) -> None:
        """Test that removing a node also removes incident edges."""
        g = WeightedDirectedGraph()
        n1, n2, n3 = (
            GraphNode("A", "n1"),
            GraphNode("B", "n2"),
            GraphNode("C", "n3"),
        )
        g.add_node(n1)
        g.add_node(n2)
        g.add_node(n3)
        g.add_edge(WeightedDirectedEdge(n1, n2, weight=1.0))
        g.add_edge(WeightedDirectedEdge(n2, n3, weight=2.0))
        g.remove_node(n2)
        assert g.edge_count() == 0
        assert g.node_count() == 2

    def test_remove_nonexistent_node_raises_error(self) -> None:
        """Test removing a node not in graph raises ValueError."""
        g = WeightedDirectedGraph()
        n1 = GraphNode("A", "n1")
        with pytest.raises(ValueError, match="not in graph"):
            g.remove_node(n1)


class TestEdgeOperations:
    """Test edge addition, removal, and queries."""

    def test_add_weighted_directed_edge(self) -> None:
        """Test adding a weighted directed edge."""
        g = WeightedDirectedGraph()
        n1, n2 = GraphNode("A", "n1"), GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        edge = WeightedDirectedEdge(n1, n2, weight=5.5)
        g.add_edge(edge)
        assert g.has_edge(n1, n2)
        assert not g.has_edge(n2, n1)  # Direction matters
        assert g.edge_count() == 1

    def test_add_edge_wrong_type_raises_error(self) -> None:
        """Test adding wrong edge type raises TypeError."""
        g = WeightedDirectedGraph()
        n1, n2 = GraphNode("A", "n1"), GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        with pytest.raises(TypeError):
            g.add_edge(WeightedEdge(n1, n2, weight=1.0))  # type: ignore

    def test_add_edge_with_missing_nodes_raises_error(self) -> None:
        """Test adding edge with missing nodes raises ValueError."""
        g = WeightedDirectedGraph()
        n1, n2 = GraphNode("A", "n1"), GraphNode("B", "n2")
        g.add_node(n1)
        with pytest.raises(ValueError, match="not in graph"):
            g.add_edge(WeightedDirectedEdge(n1, n2, weight=1.0))

    def test_add_duplicate_edge_raises_error(self) -> None:
        """Test adding duplicate edge raises ValueError."""
        g = WeightedDirectedGraph()
        n1, n2 = GraphNode("A", "n1"), GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(WeightedDirectedEdge(n1, n2, weight=1.0))
        with pytest.raises(ValueError, match="already exists"):
            g.add_edge(WeightedDirectedEdge(n1, n2, weight=2.0))

    def test_multi_edges_allowed(self) -> None:
        """Test that multi-digraph allows multiple edges."""
        g = WeightedDirectedGraph(allow_multi_edges=True)
        n1, n2 = GraphNode("A", "n1"), GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(WeightedDirectedEdge(n1, n2, weight=1.0))
        g.add_edge(WeightedDirectedEdge(n1, n2, weight=2.0))
        assert g.edge_count() == 2

    def test_remove_edge(self) -> None:
        """Test removing an edge."""
        g = WeightedDirectedGraph()
        n1, n2 = GraphNode("A", "n1"), GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        edge = WeightedDirectedEdge(n1, n2, weight=1.0)
        g.add_edge(edge)
        g.remove_edge(edge)
        assert not g.has_edge(n1, n2)
        assert g.edge_count() == 0

    def test_remove_nonexistent_edge_raises_error(self) -> None:
        """Test removing nonexistent edge raises ValueError."""
        g = WeightedDirectedGraph()
        n1, n2 = GraphNode("A", "n1"), GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        edge = WeightedDirectedEdge(n1, n2, weight=1.0)
        with pytest.raises(ValueError, match="not in graph"):
            g.remove_edge(edge)


class TestWeightOperations:
    """Test weight-specific operations."""

    def test_get_edge_weight(self) -> None:
        """Test getting edge weight."""
        g = WeightedDirectedGraph()
        n1, n2 = GraphNode("A", "n1"), GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(WeightedDirectedEdge(n1, n2, weight=7.5))
        assert g.get_edge_weight(n1, n2) == 7.5

    def test_get_edge_weight_nonexistent(self) -> None:
        """Test getting weight of nonexistent edge returns None."""
        g = WeightedDirectedGraph()
        n1, n2 = GraphNode("A", "n1"), GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        assert g.get_edge_weight(n1, n2) is None

    def test_total_weight(self) -> None:
        """Test calculating total weight of all edges."""
        g = WeightedDirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for n in nodes:
            g.add_node(n)
        g.add_edge(WeightedDirectedEdge(nodes[0], nodes[1], weight=2.0))
        g.add_edge(WeightedDirectedEdge(nodes[1], nodes[2], weight=3.0))
        g.add_edge(WeightedDirectedEdge(nodes[2], nodes[0], weight=5.0))
        assert g.total_weight() == 10.0

    def test_total_weight_caching(self) -> None:
        """Test that total weight is cached."""
        g = WeightedDirectedGraph()
        n1, n2 = GraphNode("A", "n1"), GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(WeightedDirectedEdge(n1, n2, weight=5.0))
        w1 = g.total_weight()
        w2 = g.total_weight()  # Should use cache
        assert w1 == w2 == 5.0

    def test_incident_edges(self) -> None:
        """Test getting incident edges for a node."""
        g = WeightedDirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for n in nodes:
            g.add_node(n)
        g.add_edge(WeightedDirectedEdge(nodes[0], nodes[1], weight=1.0))
        g.add_edge(WeightedDirectedEdge(nodes[1], nodes[2], weight=2.0))
        g.add_edge(WeightedDirectedEdge(nodes[0], nodes[2], weight=3.0))
        incident = g.incident_edges(nodes[0])
        assert len(incident) == 2


class TestDirectedGraphProperties:
    """Test directed graph specific properties."""

    def test_in_degree(self) -> None:
        """Test calculating in-degree."""
        g = WeightedDirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for n in nodes:
            g.add_node(n)
        g.add_edge(WeightedDirectedEdge(nodes[0], nodes[2], weight=1.0))
        g.add_edge(WeightedDirectedEdge(nodes[1], nodes[2], weight=1.0))
        assert g.in_degree(nodes[2]) == 2
        assert g.in_degree(nodes[0]) == 0

    def test_out_degree(self) -> None:
        """Test calculating out-degree."""
        g = WeightedDirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for n in nodes:
            g.add_node(n)
        g.add_edge(WeightedDirectedEdge(nodes[0], nodes[1], weight=1.0))
        g.add_edge(WeightedDirectedEdge(nodes[0], nodes[2], weight=1.0))
        assert g.out_degree(nodes[0]) == 2
        assert g.out_degree(nodes[2]) == 0

    def test_total_degree(self) -> None:
        """Test total degree calculation."""
        g = WeightedDirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for n in nodes:
            g.add_node(n)
        g.add_edge(WeightedDirectedEdge(nodes[0], nodes[1], weight=1.0))
        g.add_edge(WeightedDirectedEdge(nodes[1], nodes[2], weight=1.0))
        assert g.degree(nodes[1]) == 2  # 1 in + 1 out

    def test_predecessors(self) -> None:
        """Test getting predecessor nodes."""
        g = WeightedDirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for n in nodes:
            g.add_node(n)
        g.add_edge(WeightedDirectedEdge(nodes[0], nodes[2], weight=1.0))
        g.add_edge(WeightedDirectedEdge(nodes[1], nodes[2], weight=1.0))
        preds = sorted([n.id for n in g.predecessors(nodes[2])])
        assert preds == ["n0", "n1"]

    def test_successors(self) -> None:
        """Test getting successor nodes."""
        g = WeightedDirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for n in nodes:
            g.add_node(n)
        g.add_edge(WeightedDirectedEdge(nodes[0], nodes[1], weight=1.0))
        g.add_edge(WeightedDirectedEdge(nodes[0], nodes[2], weight=1.0))
        succs = sorted([n.id for n in g.successors(nodes[0])])
        assert succs == ["n1", "n2"]

    def test_neighbors_returns_successors(self) -> None:
        """Test that neighbors() returns successors for directed graphs."""
        g = WeightedDirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for n in nodes:
            g.add_node(n)
        g.add_edge(WeightedDirectedEdge(nodes[0], nodes[1], weight=1.0))
        neighbors = list(g.neighbors(nodes[0]))
        successors = list(g.successors(nodes[0]))
        assert len(neighbors) == len(successors) == 1


class TestAcyclicity:
    """Test acyclicity detection."""

    def test_empty_graph_is_acyclic(self) -> None:
        """Test that empty graph is acyclic."""
        g = WeightedDirectedGraph()
        assert g.is_acyclic()

    def test_single_node_is_acyclic(self) -> None:
        """Test that single node graph is acyclic."""
        g = WeightedDirectedGraph()
        g.add_node(GraphNode("A", "n1"))
        assert g.is_acyclic()

    def test_dag_is_acyclic(self) -> None:
        """Test that DAG is detected as acyclic."""
        g = WeightedDirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for n in nodes:
            g.add_node(n)
        g.add_edge(WeightedDirectedEdge(nodes[0], nodes[1], weight=1.0))
        g.add_edge(WeightedDirectedEdge(nodes[1], nodes[2], weight=1.0))
        assert g.is_acyclic()

    def test_cycle_detected(self) -> None:
        """Test that cycles are detected."""
        g = WeightedDirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for n in nodes:
            g.add_node(n)
        g.add_edge(WeightedDirectedEdge(nodes[0], nodes[1], weight=1.0))
        g.add_edge(WeightedDirectedEdge(nodes[1], nodes[2], weight=1.0))
        g.add_edge(WeightedDirectedEdge(nodes[2], nodes[0], weight=1.0))
        assert not g.is_acyclic()

    def test_acyclic_caching(self) -> None:
        """Test that acyclicity check is cached."""
        g = WeightedDirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for n in nodes:
            g.add_node(n)
        g.add_edge(WeightedDirectedEdge(nodes[0], nodes[1], weight=1.0))
        r1 = g.is_acyclic()
        r2 = g.is_acyclic()  # Should use cache
        assert r1 == r2 == True  # noqa: E712


class TestConnectivity:
    """Test weak connectivity."""

    def test_empty_graph_is_connected(self) -> None:
        """Test that empty graph is considered connected."""
        g = WeightedDirectedGraph()
        assert g.is_connected()

    def test_single_node_is_connected(self) -> None:
        """Test that single node is connected."""
        g = WeightedDirectedGraph()
        g.add_node(GraphNode("A", "n1"))
        assert g.is_connected()

    def test_weakly_connected_graph(self) -> None:
        """Test weakly connected graph detection."""
        g = WeightedDirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for n in nodes:
            g.add_node(n)
        g.add_edge(WeightedDirectedEdge(nodes[0], nodes[1], weight=1.0))
        g.add_edge(WeightedDirectedEdge(nodes[1], nodes[2], weight=1.0))
        assert g.is_connected()

    def test_disconnected_graph(self) -> None:
        """Test disconnected graph detection."""
        g = WeightedDirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(4)]
        for n in nodes:
            g.add_node(n)
        g.add_edge(WeightedDirectedEdge(nodes[0], nodes[1], weight=1.0))
        g.add_edge(WeightedDirectedEdge(nodes[2], nodes[3], weight=1.0))
        assert not g.is_connected()


class TestIterationAndAccess:
    """Test iteration and node/edge access."""

    def test_nodes_iteration(self) -> None:
        """Test iterating over nodes."""
        g = WeightedDirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for n in nodes:
            g.add_node(n)
        node_ids = sorted([n.id for n in g.nodes()])
        assert node_ids == ["n0", "n1", "n2"]

    def test_edges_iteration(self) -> None:
        """Test iterating over edges."""
        g = WeightedDirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for n in nodes:
            g.add_node(n)
        g.add_edge(WeightedDirectedEdge(nodes[0], nodes[1], weight=1.0))
        g.add_edge(WeightedDirectedEdge(nodes[1], nodes[2], weight=2.0))
        assert g.edge_count() == 2
        edges = list(g.edges())
        assert len(edges) == 2

    def test_get_node_by_id(self) -> None:
        """Test getting node by ID."""
        g = WeightedDirectedGraph()
        n1 = GraphNode("A", "n1")
        g.add_node(n1)
        found = g.get_node_by_id("n1")
        assert found is not None
        assert found.id == "n1"

    def test_get_edge(self) -> None:
        """Test getting edge between nodes."""
        g = WeightedDirectedGraph()
        n1, n2 = GraphNode("A", "n1"), GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        edge = WeightedDirectedEdge(n1, n2, weight=3.5)
        g.add_edge(edge)
        found = g.get_edge(n1, n2)
        assert found is not None
        assert found.weight == 3.5


class TestSpecialMethods:
    """Test dunder methods."""

    def test_len(self) -> None:
        """Test __len__ returns node count."""
        g = WeightedDirectedGraph()
        assert len(g) == 0
        g.add_node(GraphNode("A", "n1"))
        assert len(g) == 1

    def test_contains(self) -> None:
        """Test __contains__ for node membership."""
        g = WeightedDirectedGraph()
        n1 = GraphNode("A", "n1")
        assert n1 not in g
        g.add_node(n1)
        assert n1 in g

    def test_iter(self) -> None:
        """Test __iter__ over nodes."""
        g = WeightedDirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for n in nodes:
            g.add_node(n)
        node_ids = sorted([n.id for n in g])
        assert node_ids == ["n0", "n1", "n2"]

    def test_repr(self) -> None:
        """Test __repr__ string representation."""
        g = WeightedDirectedGraph()
        assert "WeightedDirectedGraph" in repr(g)
        assert "nodes=0" in repr(g)

    def test_str(self) -> None:
        """Test __str__ string representation."""
        g = WeightedDirectedGraph()
        assert "WeightedDirectedGraph" in str(g)


class TestClearOperation:
    """Test graph clearing."""

    def test_clear_empty_graph(self) -> None:
        """Test clearing an empty graph."""
        g = WeightedDirectedGraph()
        g.clear()
        assert g.is_empty()

    def test_clear_removes_all(self) -> None:
        """Test that clear removes all nodes and edges."""
        g = WeightedDirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for n in nodes:
            g.add_node(n)
        g.add_edge(WeightedDirectedEdge(nodes[0], nodes[1], weight=1.0))
        g.clear()
        assert g.is_empty()
        assert g.node_count() == 0
        assert g.edge_count() == 0
