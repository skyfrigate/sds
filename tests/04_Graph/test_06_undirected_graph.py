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

"""Unit tests for UndirectedGraph class.

These tests verify that UndirectedGraph:
1. Inherits all functionality from Graph
2. Explicitly rejects DirectedEdge instances
3. Works identically to Graph for undirected edges
"""

import pytest

from sds.graph.directed import UndirectedGraph
from sds.graph.edge import DirectedEdge, Edge
from sds.graph.graph import Graph
from sds.graph.node import GraphNode


class TestUndirectedGraphInheritance:
    """Test that UndirectedGraph properly inherits from Graph."""

    def test_inherits_from_graph(self) -> None:
        """Test that UndirectedGraph is a Graph."""
        g = UndirectedGraph()
        assert isinstance(g, Graph)
        assert isinstance(g, UndirectedGraph)

    def test_has_all_graph_methods(self) -> None:
        """Test that UndirectedGraph has all Graph methods."""
        g = UndirectedGraph()
        # Node operations
        assert hasattr(g, "add_node")
        assert hasattr(g, "remove_node")
        assert hasattr(g, "has_node")
        # Edge operations
        assert hasattr(g, "add_edge")
        assert hasattr(g, "remove_edge")
        assert hasattr(g, "has_edge")
        assert hasattr(g, "get_edge")
        # Queries
        assert hasattr(g, "neighbors")
        assert hasattr(g, "degree")
        assert hasattr(g, "is_connected")


class TestUndirectedGraphEdgeValidation:
    """Test edge type validation (key feature of UndirectedGraph)."""

    def test_accepts_undirected_edge(self) -> None:
        """Test that regular Edge is accepted."""
        g = UndirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        # Should work fine
        g.add_edge(Edge(n1, n2))
        assert g.has_edge(n1, n2)

    def test_rejects_directed_edge(self) -> None:
        """Test that DirectedEdge is rejected."""
        g = UndirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        # Should raise TypeError
        with pytest.raises(TypeError, match="requires undirected Edge"):
            g.add_edge(DirectedEdge(n1, n2))  # type: ignore[arg-type]

    def test_error_message_includes_type_name(self) -> None:
        """Test that error message includes the actual type name."""
        g = UndirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        with pytest.raises(TypeError, match="DirectedEdge"):
            g.add_edge(DirectedEdge(n1, n2))  # type: ignore[arg-type]

    def test_graph_remains_unchanged_after_rejected_edge(self) -> None:
        """Test that graph is unchanged after edge rejection."""
        g = UndirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        initial_edge_count = g.edge_count()

        try:
            g.add_edge(DirectedEdge(n1, n2))  # type: ignore[arg-type]
        except TypeError:
            pass

        assert g.edge_count() == initial_edge_count
        assert not g.has_edge(n1, n2)


class TestUndirectedGraphFunctionality:
    """Test that all Graph functionality works in UndirectedGraph."""

    def test_basic_operations(self) -> None:
        """Test basic node and edge operations."""
        g = UndirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")

        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(Edge(n1, n2))

        assert g.node_count() == 2
        assert g.edge_count() == 1
        assert g.has_edge(n1, n2)
        assert g.has_edge(n2, n1)  # Bidirectional

    def test_neighbors(self) -> None:
        """Test neighbors query."""
        g = UndirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        n3 = GraphNode("C", "n3")

        g.add_node(n1)
        g.add_node(n2)
        g.add_node(n3)
        g.add_edge(Edge(n1, n2))
        g.add_edge(Edge(n1, n3))

        neighbors = {n.id for n in g.neighbors(n1)}
        assert neighbors == {"n2", "n3"}

    def test_degree(self) -> None:
        """Test degree calculation."""
        g = UndirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        n3 = GraphNode("C", "n3")

        g.add_node(n1)
        g.add_node(n2)
        g.add_node(n3)
        g.add_edge(Edge(n1, n2))
        g.add_edge(Edge(n1, n3))

        assert g.degree(n1) == 2
        assert g.degree(n2) == 1

    def test_connectivity(self) -> None:
        """Test connectivity checking."""
        g = UndirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        n3 = GraphNode("C", "n3")

        g.add_node(n1)
        g.add_node(n2)
        g.add_node(n3)

        assert not g.is_connected()  # Disconnected

        g.add_edge(Edge(n1, n2))
        g.add_edge(Edge(n2, n3))

        assert g.is_connected()  # Now connected

    def test_remove_operations(self) -> None:
        """Test remove operations."""
        g = UndirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")

        g.add_node(n1)
        g.add_node(n2)
        e = Edge(n1, n2)
        g.add_edge(e)

        g.remove_edge(e)
        assert g.edge_count() == 0

        g.remove_node(n1)
        assert g.node_count() == 1

    def test_clear(self) -> None:
        """Test clearing the graph."""
        g = UndirectedGraph()
        n1 = GraphNode("A", "n1")
        g.add_node(n1)

        g.clear()
        assert g.is_empty()


class TestUndirectedGraphMultiEdges:
    """Test multi-edge support in UndirectedGraph."""

    def test_multi_edges_disabled_by_default(self) -> None:
        """Test that multi-edges are disabled by default."""
        g = UndirectedGraph()
        assert g.allow_multi_edges is False

    def test_multi_edges_can_be_enabled(self) -> None:
        """Test enabling multi-edges."""
        g = UndirectedGraph(allow_multi_edges=True)
        assert g.allow_multi_edges is True

    def test_duplicate_edge_rejected_in_simple_graph(self) -> None:
        """Test that duplicate edges are rejected in simple graph."""
        g = UndirectedGraph(allow_multi_edges=False)
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        g.add_edge(Edge(n1, n2))
        with pytest.raises(ValueError, match="already exists"):
            g.add_edge(Edge(n1, n2))

    def test_multiple_edges_allowed_in_multigraph(self) -> None:
        """Test that multiple edges work in multigraph."""
        g = UndirectedGraph(allow_multi_edges=True)
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        g.add_edge(Edge(n1, n2, data="edge1"))
        g.add_edge(Edge(n1, n2, data="edge2"))
        assert g.edge_count() == 2


class TestUndirectedGraphStringRepresentations:
    """Test string representations."""

    def test_repr(self) -> None:
        """Test __repr__ format."""
        g = UndirectedGraph()
        assert "UndirectedGraph" in repr(g)
        assert "nodes=0" in repr(g)
        assert "edges=0" in repr(g)

    def test_str(self) -> None:
        """Test __str__ format."""
        g = UndirectedGraph()
        assert "UndirectedGraph" in str(g)
        assert "0 nodes" in str(g)
        assert "0 edges" in str(g)

    def test_repr_with_data(self) -> None:
        """Test __repr__ with nodes and edges."""
        g = UndirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(Edge(n1, n2))

        assert "nodes=2" in repr(g)
        assert "edges=1" in repr(g)


class TestUndirectedGraphIterationProtocols:
    """Test iteration protocols."""

    def test_len(self) -> None:
        """Test __len__ returns node count."""
        g = UndirectedGraph()
        assert len(g) == 0

        g.add_node(GraphNode("A", "n1"))
        assert len(g) == 1

    def test_contains(self) -> None:
        """Test __contains__ checks node membership."""
        g = UndirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")

        g.add_node(n1)
        assert n1 in g
        assert n2 not in g

    def test_iter(self) -> None:
        """Test __iter__ iterates over nodes."""
        g = UndirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for node in nodes:
            g.add_node(node)

        node_ids = {n.id for n in g}
        assert node_ids == {"n0", "n1", "n2"}


class TestUndirectedGraphEdgeCases:
    """Test edge cases and special scenarios."""

    def test_empty_graph(self) -> None:
        """Test operations on empty graph."""
        g = UndirectedGraph()
        assert g.is_empty()
        assert g.node_count() == 0
        assert g.edge_count() == 0
        assert g.is_connected()  # Empty graph is connected

    def test_single_node(self) -> None:
        """Test graph with single node."""
        g = UndirectedGraph()
        n1 = GraphNode("A", "n1")
        g.add_node(n1)

        assert not g.is_empty()
        assert g.node_count() == 1
        assert g.degree(n1) == 0
        assert g.is_connected()

    def test_large_graph(self) -> None:
        """Test with many nodes."""
        g = UndirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(100)]

        for node in nodes:
            g.add_node(node)

        # Create chain
        for i in range(99):
            g.add_edge(Edge(nodes[i], nodes[i + 1]))

        assert g.node_count() == 100
        assert g.edge_count() == 99
        assert g.is_connected()


class TestUndirectedGraphVsGraph:
    """Test differences between UndirectedGraph and Graph."""

    def test_graph_accepts_directed_edge(self) -> None:
        """Test that Graph accepts DirectedEdge (treats as undirected)."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        # Graph accepts DirectedEdge (but treats as undirected)
        g.add_edge(DirectedEdge(n1, n2))  # type: ignore[arg-type]
        assert g.has_edge(n1, n2)

    def test_undirected_graph_rejects_directed_edge(self) -> None:
        """Test that UndirectedGraph explicitly rejects DirectedEdge."""
        g = UndirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        # UndirectedGraph rejects DirectedEdge
        with pytest.raises(TypeError):
            g.add_edge(DirectedEdge(n1, n2))  # type: ignore[arg-type]

    def test_functionality_identical_for_undirected_edges(self) -> None:
        """Test that functionality is identical when using Edge."""
        g1 = Graph()
        g2 = UndirectedGraph()

        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")

        for g in [g1, g2]:
            g.add_node(n1)
            g.add_node(n2)
            g.add_edge(Edge(n1, n2))

        # Both should behave identically
        assert g1.node_count() == g2.node_count()
        assert g1.edge_count() == g2.edge_count()
        assert g1.has_edge(n1, n2) == g2.has_edge(n1, n2)
        assert g1.degree(n1) == g2.degree(n1)
