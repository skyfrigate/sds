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

"""Unit tests for WeightedGraph class - Part 1."""

import pytest

from sds.graph.edge import Edge, WeightedDirectedEdge, WeightedEdge
from sds.graph.interfaces import AbstractWeightedGraph
from sds.graph.node import GraphNode
from sds.graph.weighted import WeightedGraph


class TestWeightedGraphCreation:
    """Test WeightedGraph initialization."""

    def test_create_empty_graph(self) -> None:
        """Test creating an empty weighted graph."""
        g = WeightedGraph()
        assert g.is_empty()
        assert g.node_count() == 0
        assert g.edge_count() == 0
        assert g.total_weight() == 0.0

    def test_create_with_multi_edges_disabled(self) -> None:
        """Test creating graph with multi-edges disabled."""
        g = WeightedGraph(allow_multi_edges=False)
        assert g.allow_multi_edges is False

    def test_create_with_multi_edges_enabled(self) -> None:
        """Test creating graph with multi-edges enabled."""
        g = WeightedGraph(allow_multi_edges=True)
        assert g.allow_multi_edges is True

    def test_inherits_from_abstract_weighted_graph(self) -> None:
        """Test that WeightedGraph inherits from AbstractWeightedGraph."""
        g = WeightedGraph()
        assert isinstance(g, AbstractWeightedGraph)


class TestWeightedGraphNodeOperations:
    """Test node operations (same as Graph)."""

    def test_add_node(self) -> None:
        """Test adding nodes."""
        g = WeightedGraph()
        n1 = GraphNode("A", "n1")
        g.add_node(n1)
        assert g.has_node(n1)
        assert g.node_count() == 1

    def test_add_duplicate_node_raises_error(self) -> None:
        """Test that duplicate node raises error."""
        g = WeightedGraph()
        n1 = GraphNode("A", "n1")
        g.add_node(n1)
        with pytest.raises(ValueError, match="already exists"):
            g.add_node(n1)

    def test_remove_node(self) -> None:
        """Test removing node."""
        g = WeightedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(WeightedEdge(n1, n2, weight=5.0))

        g.remove_node(n1)
        assert not g.has_node(n1)
        assert g.edge_count() == 0


class TestWeightedGraphEdgeOperations:
    """Test weighted edge operations."""

    def test_add_weighted_edge(self) -> None:
        """Test adding a weighted edge."""
        g = WeightedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        e = WeightedEdge(n1, n2, weight=10.0)
        g.add_edge(e)
        assert g.has_edge(n1, n2)
        assert g.edge_count() == 1

    def test_edge_is_bidirectional(self) -> None:
        """Test that weighted edge is bidirectional."""
        g = WeightedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(WeightedEdge(n1, n2, weight=5.0))

        assert g.has_edge(n1, n2)
        assert g.has_edge(n2, n1)

    def test_requires_weighted_edge(self) -> None:
        """Test that only WeightedEdge is accepted."""
        g = WeightedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        # Regular Edge should raise TypeError
        with pytest.raises(TypeError, match="Expected WeightedEdge"):
            g.add_edge(Edge(n1, n2))  # type: ignore[arg-type]

    def test_rejects_directed_weighted_edge(self) -> None:
        """Test that WeightedDirectedEdge is rejected."""

        g = WeightedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        with pytest.raises(TypeError, match="requires undirected"):
            g.add_edge(WeightedDirectedEdge(n1, n2, weight=5.0))  # type: ignore[arg-type]

    def test_add_duplicate_edge_raises_error(self) -> None:
        """Test that duplicate edge raises error in simple graph."""
        g = WeightedGraph(allow_multi_edges=False)
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        g.add_edge(WeightedEdge(n1, n2, weight=5.0))
        with pytest.raises(ValueError, match="already exists"):
            g.add_edge(WeightedEdge(n1, n2, weight=10.0))

    def test_multiple_edges_in_multigraph(self) -> None:
        """Test multiple edges in multigraph."""
        g = WeightedGraph(allow_multi_edges=True)
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        g.add_edge(WeightedEdge(n1, n2, weight=5.0))
        g.add_edge(WeightedEdge(n1, n2, weight=10.0))
        assert g.edge_count() == 2

    def test_remove_edge(self) -> None:
        """Test removing a weighted edge."""
        g = WeightedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        e = WeightedEdge(n1, n2, weight=5.0)
        g.add_edge(e)
        g.remove_edge(e)
        assert g.edge_count() == 0


class TestWeightedGraphWeightOperations:
    """Test weight-specific operations."""

    def test_get_edge_weight(self) -> None:
        """Test getting edge weight."""
        g = WeightedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        g.add_edge(WeightedEdge(n1, n2, weight=7.5))
        assert g.get_edge_weight(n1, n2) == 7.5

    def test_get_edge_weight_bidirectional(self) -> None:
        """Test that weight is same in both directions."""
        g = WeightedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        g.add_edge(WeightedEdge(n1, n2, weight=10.0))
        assert g.get_edge_weight(n1, n2) == 10.0
        assert g.get_edge_weight(n2, n1) == 10.0

    def test_get_edge_weight_nonexistent_edge(self) -> None:
        """Test getting weight of nonexistent edge."""
        g = WeightedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        assert g.get_edge_weight(n1, n2) is None

    def test_total_weight_empty_graph(self) -> None:
        """Test total weight of empty graph."""
        g = WeightedGraph()
        assert g.total_weight() == 0.0

    def test_total_weight_single_edge(self) -> None:
        """Test total weight with single edge."""
        g = WeightedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        g.add_edge(WeightedEdge(n1, n2, weight=5.0))
        assert g.total_weight() == 5.0

    def test_total_weight_multiple_edges(self) -> None:
        """Test total weight with multiple edges."""
        g = WeightedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(4)]
        for node in nodes:
            g.add_node(node)

        g.add_edge(WeightedEdge(nodes[0], nodes[1], weight=10.0))
        g.add_edge(WeightedEdge(nodes[1], nodes[2], weight=20.0))
        g.add_edge(WeightedEdge(nodes[2], nodes[3], weight=15.0))

        assert g.total_weight() == 45.0

    def test_total_weight_with_negative_weights(self) -> None:
        """Test total weight with negative weights."""
        g = WeightedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        n3 = GraphNode("C", "n3")
        for n in [n1, n2, n3]:
            g.add_node(n)

        g.add_edge(WeightedEdge(n1, n2, weight=10.0))
        g.add_edge(WeightedEdge(n2, n3, weight=-5.0))

        assert g.total_weight() == 5.0

    def test_total_weight_cached(self) -> None:
        """Test that total weight is cached."""
        g = WeightedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(WeightedEdge(n1, n2, weight=10.0))

        # First call - computes
        w1 = g.total_weight()
        # Second call - should use cache
        w2 = g.total_weight()

        assert w1 == w2 == 10.0
        assert g._cache_valid is True


class TestWeightedGraphIncidentEdges:
    """Test incident_edges() method."""

    def test_incident_edges_isolated_node(self) -> None:
        """Test incident edges for isolated node."""
        g = WeightedGraph()
        n1 = GraphNode("A", "n1")
        g.add_node(n1)

        edges = g.incident_edges(n1)
        assert len(edges) == 0

    def test_incident_edges_single(self) -> None:
        """Test incident edges with one edge."""
        g = WeightedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(WeightedEdge(n1, n2, weight=5.0))

        edges = g.incident_edges(n1)
        assert len(edges) == 1
        assert edges[0].weight == 5.0

    def test_incident_edges_multiple(self) -> None:
        """Test incident edges with multiple edges."""
        g = WeightedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        n3 = GraphNode("C", "n3")
        n4 = GraphNode("D", "n4")
        for n in [n1, n2, n3, n4]:
            g.add_node(n)

        g.add_edge(WeightedEdge(n1, n2, weight=10.0))
        g.add_edge(WeightedEdge(n1, n3, weight=20.0))
        g.add_edge(WeightedEdge(n1, n4, weight=30.0))

        edges = g.incident_edges(n1)
        assert len(edges) == 3
        total_weight = sum(e.weight for e in edges)
        assert total_weight == 60.0

    def test_incident_edges_returns_weighted_edges(self) -> None:
        """Test that incident_edges returns WeightedEdge instances."""
        g = WeightedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(WeightedEdge(n1, n2, weight=5.0))

        edges = g.incident_edges(n1)
        assert all(isinstance(e, WeightedEdge) for e in edges)

    def test_incident_edges_nonexistent_node(self) -> None:
        """Test incident_edges with nonexistent node."""
        g = WeightedGraph()
        n1 = GraphNode("A", "n1")

        with pytest.raises(ValueError, match="not in graph"):
            g.incident_edges(n1)


class TestWeightedGraphNeighborsAndDegree:
    """Test neighbors and degree operations."""

    def test_neighbors(self) -> None:
        """Test getting neighbors."""
        g = WeightedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        n3 = GraphNode("C", "n3")
        for n in [n1, n2, n3]:
            g.add_node(n)

        g.add_edge(WeightedEdge(n1, n2, weight=5.0))
        g.add_edge(WeightedEdge(n1, n3, weight=10.0))

        neighbor_ids = {n.id for n in g.neighbors(n1)}
        assert neighbor_ids == {"n2", "n3"}

    def test_degree(self) -> None:
        """Test degree calculation."""
        g = WeightedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        n3 = GraphNode("C", "n3")
        for n in [n1, n2, n3]:
            g.add_node(n)

        g.add_edge(WeightedEdge(n1, n2, weight=5.0))
        g.add_edge(WeightedEdge(n1, n3, weight=10.0))

        assert g.degree(n1) == 2
        assert g.degree(n2) == 1

    def test_degree_in_multigraph(self) -> None:
        """Test degree counts all edges in multigraph."""
        g = WeightedGraph(allow_multi_edges=True)
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        g.add_edge(WeightedEdge(n1, n2, weight=5.0))
        g.add_edge(WeightedEdge(n1, n2, weight=10.0))
        g.add_edge(WeightedEdge(n1, n2, weight=15.0))

        assert g.degree(n1) == 3


class TestWeightedGraphConnectivity:
    """Test connectivity checking."""

    def test_empty_graph_is_connected(self) -> None:
        """Test empty graph is connected."""
        g = WeightedGraph()
        assert g.is_connected() is True

    def test_single_node_is_connected(self) -> None:
        """Test single node is connected."""
        g = WeightedGraph()
        g.add_node(GraphNode("A", "n1"))
        assert g.is_connected() is True

    def test_connected_graph(self) -> None:
        """Test connected graph."""
        g = WeightedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for node in nodes:
            g.add_node(node)

        g.add_edge(WeightedEdge(nodes[0], nodes[1], weight=5.0))
        g.add_edge(WeightedEdge(nodes[1], nodes[2], weight=10.0))

        assert g.is_connected() is True

    def test_disconnected_graph(self) -> None:
        """Test disconnected graph."""
        g = WeightedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(4)]
        for node in nodes:
            g.add_node(node)

        g.add_edge(WeightedEdge(nodes[0], nodes[1], weight=5.0))
        g.add_edge(WeightedEdge(nodes[2], nodes[3], weight=10.0))

        assert g.is_connected() is False


class TestWeightedGraphCaching:
    """Test caching of expensive operations."""

    def test_connectivity_cached(self) -> None:
        """Test connectivity caching."""
        g = WeightedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(WeightedEdge(n1, n2, weight=5.0))

        # First call
        r1 = g.is_connected()
        # Second call - cached
        r2 = g.is_connected()

        assert r1 is True
        assert r2 is True
        assert g._cache_valid is True

    def test_cache_invalidated_on_edge_add(self) -> None:
        """Test cache invalidated when edge added."""
        g = WeightedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        # Cache result
        g.is_connected()
        g.total_weight()
        assert g._cache_valid is True

        # Add edge - invalidate
        g.add_edge(WeightedEdge(n1, n2, weight=5.0))
        assert g._cache_valid is False

    def test_cache_invalidated_on_node_remove(self) -> None:
        """Test cache invalidated when node removed."""
        g = WeightedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        # Cache result
        g.is_connected()
        assert g._cache_valid is True

        # Remove node
        g.remove_node(n1)
        assert g._cache_valid is False


class TestWeightedGraphIteration:
    """Test iteration protocols."""

    def test_nodes_iteration(self) -> None:
        """Test iterating over nodes."""
        g = WeightedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for node in nodes:
            g.add_node(node)

        node_ids = {n.id for n in g.nodes()}
        assert node_ids == {"n0", "n1", "n2"}

    def test_edges_iteration(self) -> None:
        """Test iterating over edges."""
        g = WeightedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        n3 = GraphNode("C", "n3")
        for n in [n1, n2, n3]:
            g.add_node(n)

        g.add_edge(WeightedEdge(n1, n2, weight=5.0))
        g.add_edge(WeightedEdge(n2, n3, weight=10.0))

        edges = list(g.edges())
        assert len(edges) == 2
        assert all(isinstance(e, WeightedEdge) for e in edges)

    def test_iter_protocol(self) -> None:
        """Test __iter__ protocol."""
        g = WeightedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for node in nodes:
            g.add_node(node)

        node_ids = {n.id for n in g}
        assert node_ids == {"n0", "n1", "n2"}

    def test_contains_protocol(self) -> None:
        """Test __contains__ protocol."""
        g = WeightedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)

        assert n1 in g
        assert n2 not in g

    def test_len_protocol(self) -> None:
        """Test __len__ protocol."""
        g = WeightedGraph()
        assert len(g) == 0

        for i in range(5):
            g.add_node(GraphNode(f"N{i}", f"n{i}"))

        assert len(g) == 5


class TestWeightedGraphStringRepresentations:
    """Test string representations."""

    def test_repr_empty(self) -> None:
        """Test __repr__ for empty graph."""
        g = WeightedGraph()
        assert repr(g) == "WeightedGraph(nodes=0, edges=0, multi_edges=False)"

    def test_repr_with_data(self) -> None:
        """Test __repr__ with nodes and edges."""
        g = WeightedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(WeightedEdge(n1, n2, weight=5.0))

        assert repr(g) == "WeightedGraph(nodes=2, edges=1, multi_edges=False)"

    def test_str_empty(self) -> None:
        """Test __str__ for empty graph."""
        g = WeightedGraph()
        assert str(g) == "WeightedGraph: 0 nodes, 0 edges"

    def test_str_with_data(self) -> None:
        """Test __str__ with data."""
        g = WeightedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(WeightedEdge(n1, n2, weight=5.0))

        assert str(g) == "WeightedGraph: 2 nodes, 1 edges"


class TestWeightedGraphClearAndEmpty:
    """Test clear and empty operations."""

    def test_clear(self) -> None:
        """Test clearing the graph."""
        g = WeightedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(WeightedEdge(n1, n2, weight=5.0))

        g.clear()
        assert g.is_empty()
        assert g.node_count() == 0
        assert g.edge_count() == 0
        assert g.total_weight() == 0.0

    def test_is_empty(self) -> None:
        """Test is_empty()."""
        g = WeightedGraph()
        assert g.is_empty()

        g.add_node(GraphNode("A", "n1"))
        assert not g.is_empty()

        g.clear()
        assert g.is_empty()


class TestWeightedGraphEdgeCases:
    """Test edge cases and special scenarios."""

    def test_zero_weight_edge(self) -> None:
        """Test edge with zero weight."""
        g = WeightedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        g.add_edge(WeightedEdge(n1, n2, weight=0.0))
        assert g.get_edge_weight(n1, n2) == 0.0
        assert g.total_weight() == 0.0

    def test_very_large_weights(self) -> None:
        """Test with very large weights."""
        g = WeightedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        large_weight = 1e10
        g.add_edge(WeightedEdge(n1, n2, weight=large_weight))
        assert g.get_edge_weight(n1, n2) == large_weight

    def test_very_small_weights(self) -> None:
        """Test with very small weights."""
        g = WeightedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        small_weight = 1e-10
        g.add_edge(WeightedEdge(n1, n2, weight=small_weight))
        assert g.get_edge_weight(n1, n2) == small_weight

    def test_floating_point_precision(self) -> None:
        """Test floating point precision."""
        g = WeightedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        n3 = GraphNode("C", "n3")
        for n in [n1, n2, n3]:
            g.add_node(n)

        g.add_edge(WeightedEdge(n1, n2, weight=0.1))
        g.add_edge(WeightedEdge(n2, n3, weight=0.2))

        # Should be 0.3, but floating point...
        assert abs(g.total_weight() - 0.3) < 1e-10

    def test_large_graph(self) -> None:
        """Test with many nodes and edges."""
        g = WeightedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(100)]
        for node in nodes:
            g.add_node(node)

        # Create chain with increasing weights
        for i in range(99):
            g.add_edge(WeightedEdge(nodes[i], nodes[i + 1], weight=float(i + 1)))

        assert g.node_count() == 100
        assert g.edge_count() == 99
        # Sum: 1 + 2 + ... + 99 = 99*100/2 = 4950
        assert g.total_weight() == 4950.0

    def test_complete_graph_weights(self) -> None:
        """Test complete graph with different weights."""
        g = WeightedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(5)]
        for node in nodes:
            g.add_node(node)

        weight = 1.0
        # Connect all pairs
        for i in range(5):
            for j in range(i + 1, 5):
                g.add_edge(WeightedEdge(nodes[i], nodes[j], weight=weight))
                weight += 1.0

        assert g.edge_count() == 10  # n*(n-1)/2
        # Sum: 1 + 2 + ... + 10 = 55
        assert g.total_weight() == 55.0


class TestWeightedGraphSpecialTopologies:
    """Test special graph topologies."""

    def test_star_graph(self) -> None:
        """Test star graph (central node connected to all others)."""
        g = WeightedGraph()
        center = GraphNode("Center", "center")
        g.add_node(center)

        periphery = [GraphNode(f"P{i}", f"p{i}") for i in range(5)]
        for node in periphery:
            g.add_node(node)

        for i, node in enumerate(periphery):
            g.add_edge(WeightedEdge(center, node, weight=float(i + 1)))

        assert g.degree(center) == 5
        # Weights: 1, 2, 3, 4, 5 → sum = 15
        assert g.total_weight() == 15.0

    def test_path_graph(self) -> None:
        """Test path graph (linear chain)."""
        g = WeightedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(5)]
        for node in nodes:
            g.add_node(node)

        for i in range(4):
            g.add_edge(WeightedEdge(nodes[i], nodes[i + 1], weight=10.0))

        assert g.degree(nodes[0]) == 1  # Endpoints
        assert g.degree(nodes[2]) == 2  # Middle
        assert g.total_weight() == 40.0

    def test_cycle_graph(self) -> None:
        """Test cycle graph."""
        g = WeightedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(4)]
        for node in nodes:
            g.add_node(node)

        for i in range(4):
            g.add_edge(WeightedEdge(nodes[i], nodes[(i + 1) % 4], weight=5.0))

        assert all(g.degree(n) == 2 for n in nodes)
        assert g.total_weight() == 20.0


class TestWeightedGraphMultigraph:
    """Test multigraph-specific scenarios."""

    def test_parallel_edges_different_weights(self) -> None:
        """Test parallel edges with different weights."""
        g = WeightedGraph(allow_multi_edges=True)
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        g.add_edge(WeightedEdge(n1, n2, weight=5.0))
        g.add_edge(WeightedEdge(n1, n2, weight=10.0))
        g.add_edge(WeightedEdge(n1, n2, weight=15.0))

        assert g.edge_count() == 3
        assert g.total_weight() == 30.0

    def test_get_edge_returns_first_in_multigraph(self) -> None:
        """Test that get_edge returns first edge in multigraph."""
        g = WeightedGraph(allow_multi_edges=True)
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        e1 = WeightedEdge(n1, n2, weight=5.0)
        e2 = WeightedEdge(n1, n2, weight=10.0)
        g.add_edge(e1)
        g.add_edge(e2)

        found = g.get_edge(n1, n2)
        assert found is e1  # First one added

    def test_remove_one_of_parallel_edges(self) -> None:
        """Test removing one of multiple parallel edges."""
        g = WeightedGraph(allow_multi_edges=True)
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        e1 = WeightedEdge(n1, n2, weight=5.0)
        e2 = WeightedEdge(n1, n2, weight=10.0)
        g.add_edge(e1)
        g.add_edge(e2)

        g.remove_edge(e1)
        assert g.edge_count() == 1
        assert g.total_weight() == 10.0
        assert g.has_edge(n1, n2)  # Still connected


class TestWeightedGraphUseCases:
    """Test real-world use cases."""

    def test_road_network(self) -> None:
        """Test road network with distances."""
        g = WeightedGraph()

        # Cities
        paris = GraphNode("Paris", "paris")
        lyon = GraphNode("Lyon", "lyon")
        marseille = GraphNode("Marseille", "marseille")

        for city in [paris, lyon, marseille]:
            g.add_node(city)

        # Roads with distances (km)
        g.add_edge(WeightedEdge(paris, lyon, weight=460))
        g.add_edge(WeightedEdge(lyon, marseille, weight=315))
        g.add_edge(WeightedEdge(paris, marseille, weight=775))

        # Total road length
        assert g.total_weight() == 1550.0

        # Direct vs via Lyon
        direct = g.get_edge_weight(paris, marseille)
        via_lyon = g.get_edge_weight(paris, lyon) + g.get_edge_weight(lyon, marseille)
        assert direct == 775.0
        assert via_lyon == 775.0

    def test_network_costs(self) -> None:
        """Test network with costs."""
        g = WeightedGraph()

        # Servers
        servers = [GraphNode(f"Server{i}", f"s{i}") for i in range(4)]
        for server in servers:
            g.add_node(server)

        # Connections with costs
        connections = [
            (servers[0], servers[1], 100),
            (servers[1], servers[2], 150),
            (servers[2], servers[3], 200),
            (servers[0], servers[3], 500),
        ]

        for src, dst, cost in connections:
            g.add_edge(WeightedEdge(src, dst, weight=cost))

        # Total infrastructure cost
        assert g.total_weight() == 950.0

    def test_weighted_social_network(self) -> None:
        """Test social network with interaction weights."""
        g = WeightedGraph()

        # People
        alice = GraphNode("Alice", "alice")
        bob = GraphNode("Bob", "bob")
        carol = GraphNode("Carol", "carol")

        for person in [alice, bob, carol]:
            g.add_node(person)

        # Interactions (number of messages)
        g.add_edge(WeightedEdge(alice, bob, weight=50))
        g.add_edge(WeightedEdge(bob, carol, weight=30))
        g.add_edge(WeightedEdge(alice, carol, weight=20))

        # Bob is most connected
        bob_edges = g.incident_edges(bob)
        bob_total = sum(e.weight for e in bob_edges)
        assert bob_total == 80.0


class TestWeightedGraphCounters:
    """Test counter methods."""

    def test_node_count(self) -> None:
        """Test node_count()."""
        g = WeightedGraph()
        assert g.node_count() == 0

        for i in range(5):
            g.add_node(GraphNode(f"N{i}", f"n{i}"))

        assert g.node_count() == 5

    def test_edge_count(self) -> None:
        """Test edge_count()."""
        g = WeightedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        assert g.edge_count() == 0

        g.add_edge(WeightedEdge(n1, n2, weight=5.0))
        assert g.edge_count() == 1

    def test_get_node_by_id(self) -> None:
        """Test get_node_by_id()."""
        g = WeightedGraph()
        n1 = GraphNode("A", "n1")
        g.add_node(n1)

        found = g.get_node_by_id("n1")
        assert found is n1

        not_found = g.get_node_by_id("n999")
        assert not_found is None
