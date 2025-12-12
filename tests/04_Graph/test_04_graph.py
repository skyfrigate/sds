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


import pytest

from sds.graph.edge import Edge
from sds.graph.graph import Graph
from sds.graph.interfaces import AbstractGraph
from sds.graph.node import GraphNode


class TestGraphCreation:
    """Test Graph initialization."""

    def test_create_empty_graph(self) -> None:
        """Test creating an empty graph."""
        g = Graph()
        assert g.is_empty()
        assert g.node_count() == 0
        assert g.edge_count() == 0
        assert len(g) == 0

    def test_create_with_multi_edges_disabled(self) -> None:
        """Test creating graph with multi-edges disabled."""
        g = Graph(allow_multi_edges=False)
        assert g.allow_multi_edges is False

    def test_create_with_multi_edges_enabled(self) -> None:
        """Test creating graph with multi-edges enabled."""
        g = Graph(allow_multi_edges=True)
        assert g.allow_multi_edges is True

    def test_inherits_from_abstract_graph(self) -> None:
        """Test that Graph inherits from AbstractGraph."""
        g = Graph()
        assert isinstance(g, AbstractGraph)


class TestGraphNodeOperations:
    """Test node addition and removal."""

    def test_add_single_node(self) -> None:
        """Test adding a single node."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        g.add_node(n1)
        assert g.has_node(n1)
        assert g.node_count() == 1

    def test_add_multiple_nodes(self) -> None:
        """Test adding multiple nodes."""
        g = Graph()
        nodes = [GraphNode(f"Node{i}", f"n{i}") for i in range(5)]
        for node in nodes:
            g.add_node(node)
        assert g.node_count() == 5
        for node in nodes:
            assert g.has_node(node)

    def test_add_duplicate_node_raises_error(self) -> None:
        """Test that adding duplicate node raises ValueError."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        g.add_node(n1)
        with pytest.raises(ValueError, match="already exists"):
            g.add_node(n1)

    def test_add_node_with_same_id_raises_error(self) -> None:
        """Test that adding node with same ID raises error."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n1")  # Same ID
        g.add_node(n1)
        with pytest.raises(ValueError, match="already exists"):
            g.add_node(n2)

    def test_add_non_graphnode_raises_error(self) -> None:
        """Test that adding non-GraphNode raises TypeError."""
        g = Graph()
        with pytest.raises(TypeError, match="Expected GraphNode"):
            g.add_node("not a node")  # type: ignore[arg-type]

    def test_has_node_returns_false_for_nonexistent(self) -> None:
        """Test has_node returns False for nonexistent node."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        assert g.has_node(n1) is False

    def test_remove_node(self) -> None:
        """Test removing a node."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        g.add_node(n1)
        g.remove_node(n1)
        assert g.has_node(n1) is False
        assert g.node_count() == 0

    def test_remove_node_with_edges(self) -> None:
        """Test removing node also removes incident edges."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        n3 = GraphNode("C", "n3")
        g.add_node(n1)
        g.add_node(n2)
        g.add_node(n3)
        g.add_edge(Edge(n1, n2))
        g.add_edge(Edge(n1, n3))

        assert g.edge_count() == 2
        g.remove_node(n1)
        assert g.edge_count() == 0
        assert g.has_node(n2)
        assert g.has_node(n3)

    def test_remove_nonexistent_node_raises_error(self) -> None:
        """Test removing nonexistent node raises ValueError."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        with pytest.raises(ValueError, match="not in graph"):
            g.remove_node(n1)

    def test_get_node_by_id(self) -> None:
        """Test getting node by ID."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        g.add_node(n1)
        found = g.get_node_by_id("n1")
        assert found is n1

    def test_get_node_by_id_nonexistent(self) -> None:
        """Test getting nonexistent node by ID returns None."""
        g = Graph()
        found = g.get_node_by_id("n999")
        assert found is None


class TestGraphEdgeOperations:
    """Test edge addition and removal."""

    def test_add_edge(self) -> None:
        """Test adding an edge."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        e = Edge(n1, n2)
        g.add_edge(e)
        assert g.has_edge(n1, n2)
        assert g.edge_count() == 1

    def test_add_edge_bidirectional(self) -> None:
        """Test that edge works in both directions (undirected)."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(Edge(n1, n2))
        assert g.has_edge(n1, n2)
        assert g.has_edge(n2, n1)  # Bidirectional

    def test_add_edge_with_nonexistent_node_raises_error(self) -> None:
        """Test adding edge with nonexistent node raises ValueError."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        # n2 not added
        with pytest.raises(ValueError, match="not in graph"):
            g.add_edge(Edge(n1, n2))

    def test_add_non_edge_raises_error(self) -> None:
        """Test adding non-Edge raises TypeError."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        g.add_node(n1)
        with pytest.raises(TypeError, match="Expected Edge"):
            g.add_edge("not an edge")  # type: ignore[arg-type]

    def test_add_duplicate_edge_raises_error(self) -> None:
        """Test adding duplicate edge raises ValueError in simple graph."""
        g = Graph(allow_multi_edges=False)
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(Edge(n1, n2))
        with pytest.raises(ValueError, match="already exists"):
            g.add_edge(Edge(n1, n2))

    def test_add_multiple_edges_in_multigraph(self) -> None:
        """Test adding multiple edges between same nodes in multigraph."""
        g = Graph(allow_multi_edges=True)
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(Edge(n1, n2, data="edge1"))
        g.add_edge(Edge(n1, n2, data="edge2"))
        assert g.edge_count() == 2

    def test_get_edge(self) -> None:
        """Test getting an edge."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        e = Edge(n1, n2, data="test")
        g.add_edge(e)
        found = g.get_edge(n1, n2)
        assert found is not None
        assert found.data == "test"

    def test_get_edge_bidirectional(self) -> None:
        """Test getting edge works in both directions."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(Edge(n1, n2))
        assert g.get_edge(n1, n2) is not None
        assert g.get_edge(n2, n1) is not None

    def test_get_nonexistent_edge(self) -> None:
        """Test getting nonexistent edge returns None."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        assert g.get_edge(n1, n2) is None

    def test_remove_edge(self) -> None:
        """Test removing an edge."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        e = Edge(n1, n2)
        g.add_edge(e)
        g.remove_edge(e)
        assert g.has_edge(n1, n2) is False
        assert g.edge_count() == 0

    def test_remove_nonexistent_edge_raises_error(self) -> None:
        """Test removing nonexistent edge raises ValueError."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        e = Edge(n1, n2)
        with pytest.raises(ValueError, match="not in graph"):
            g.remove_edge(e)

    def test_remove_edge_in_multigraph(self) -> None:
        """Test removing one edge in multigraph keeps others."""
        g = Graph(allow_multi_edges=True)
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        e1 = Edge(n1, n2, data="edge1")
        e2 = Edge(n1, n2, data="edge2")
        g.add_edge(e1)
        g.add_edge(e2)
        g.remove_edge(e1)
        assert g.edge_count() == 1
        assert g.has_edge(n1, n2)  # e2 still exists


class TestGraphNeighborsAndDegree:
    """Test neighbor queries and degree calculations."""

    def test_neighbors_empty(self) -> None:
        """Test neighbors of isolated node."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        g.add_node(n1)
        neighbors = list(g.neighbors(n1))
        assert len(neighbors) == 0

    def test_neighbors_single(self) -> None:
        """Test neighbors with one connection."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(Edge(n1, n2))
        neighbors = list(g.neighbors(n1))
        assert len(neighbors) == 1
        assert neighbors[0].id == "n2"

    def test_neighbors_multiple(self) -> None:
        """Test neighbors with multiple connections."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        n3 = GraphNode("C", "n3")
        n4 = GraphNode("D", "n4")
        g.add_node(n1)
        g.add_node(n2)
        g.add_node(n3)
        g.add_node(n4)
        g.add_edge(Edge(n1, n2))
        g.add_edge(Edge(n1, n3))
        g.add_edge(Edge(n1, n4))

        neighbor_ids = {n.id for n in g.neighbors(n1)}
        assert neighbor_ids == {"n2", "n3", "n4"}

    def test_neighbors_nonexistent_node_raises_error(self) -> None:
        """Test neighbors of nonexistent node raises ValueError."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        with pytest.raises(ValueError, match="not in graph"):
            list(g.neighbors(n1))

    def test_degree_isolated_node(self) -> None:
        """Test degree of isolated node is 0."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        g.add_node(n1)
        assert g.degree(n1) == 0

    def test_degree_with_edges(self) -> None:
        """Test degree calculation with edges."""
        g = Graph()
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
        assert g.degree(n3) == 1

    def test_degree_in_multigraph(self) -> None:
        """Test degree counts all edges in multigraph."""
        g = Graph(allow_multi_edges=True)
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(Edge(n1, n2))
        g.add_edge(Edge(n1, n2))
        g.add_edge(Edge(n1, n2))

        assert g.degree(n1) == 3
        assert g.degree(n2) == 3

    def test_degree_nonexistent_node_raises_error(self) -> None:
        """Test degree of nonexistent node raises ValueError."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        with pytest.raises(ValueError, match="not in graph"):
            g.degree(n1)


class TestGraphIteration:
    """Test iteration over nodes and edges."""

    def test_nodes_iteration(self) -> None:
        """Test iterating over nodes."""
        g = Graph()
        nodes = [GraphNode(f"Node{i}", f"n{i}") for i in range(3)]
        for node in nodes:
            g.add_node(node)

        node_ids = {n.id for n in g.nodes()}
        assert node_ids == {"n0", "n1", "n2"}

    def test_edges_iteration(self) -> None:
        """Test iterating over edges."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        n3 = GraphNode("C", "n3")
        g.add_node(n1)
        g.add_node(n2)
        g.add_node(n3)
        g.add_edge(Edge(n1, n2))
        g.add_edge(Edge(n2, n3))

        edges = list(g.edges())
        assert len(edges) == 2

    def test_iter_protocol(self) -> None:
        """Test __iter__ iterates over nodes."""
        g = Graph()
        nodes = [GraphNode(f"Node{i}", f"n{i}") for i in range(3)]
        for node in nodes:
            g.add_node(node)

        node_ids = {n.id for n in g}
        assert node_ids == {"n0", "n1", "n2"}

    def test_contains_protocol(self) -> None:
        """Test __contains__ checks node membership."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)

        assert n1 in g
        assert n2 not in g


class TestGraphConnectivity:
    """Test connectivity checking."""

    def test_empty_graph_is_connected(self) -> None:
        """Test empty graph is considered connected."""
        g = Graph()
        assert g.is_connected() is True

    def test_single_node_is_connected(self) -> None:
        """Test single node graph is connected."""
        g = Graph()
        g.add_node(GraphNode("A", "n1"))
        assert g.is_connected() is True

    def test_two_connected_nodes(self) -> None:
        """Test two nodes with edge are connected."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(Edge(n1, n2))
        assert g.is_connected() is True

    def test_two_disconnected_nodes(self) -> None:
        """Test two nodes without edge are not connected."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        assert g.is_connected() is False

    def test_connected_component(self) -> None:
        """Test connected component."""
        g = Graph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(4)]
        for node in nodes:
            g.add_node(node)

        # Create path: n0 - n1 - n2 - n3
        g.add_edge(Edge(nodes[0], nodes[1]))
        g.add_edge(Edge(nodes[1], nodes[2]))
        g.add_edge(Edge(nodes[2], nodes[3]))

        assert g.is_connected() is True

    def test_disconnected_components(self) -> None:
        """Test graph with multiple disconnected components."""
        g = Graph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(4)]
        for node in nodes:
            g.add_node(node)

        # Two separate components: (n0-n1) and (n2-n3)
        g.add_edge(Edge(nodes[0], nodes[1]))
        g.add_edge(Edge(nodes[2], nodes[3]))

        assert g.is_connected() is False

    def test_cycle_is_connected(self) -> None:
        """Test cycle graph is connected."""
        g = Graph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(4)]
        for node in nodes:
            g.add_node(node)

        # Create cycle: n0 - n1 - n2 - n3 - n0
        g.add_edge(Edge(nodes[0], nodes[1]))
        g.add_edge(Edge(nodes[1], nodes[2]))
        g.add_edge(Edge(nodes[2], nodes[3]))
        g.add_edge(Edge(nodes[3], nodes[0]))

        assert g.is_connected() is True


class TestGraphCaching:
    """Test caching of expensive operations."""

    def test_connectivity_is_cached(self) -> None:
        """Test that connectivity result is cached."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(Edge(n1, n2))

        # First call - computes
        result1 = g.is_connected()
        # Second call - should use cache
        result2 = g.is_connected()

        assert result1 is True
        assert result2 is True
        assert g._cache_valid is True

    def test_cache_invalidated_on_node_add(self) -> None:
        """Test cache is invalidated when node is added."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        g.add_node(n1)

        # Cache result
        g.is_connected()
        assert g._cache_valid is True

        # Add node - should invalidate
        n2 = GraphNode("B", "n2")
        g.add_node(n2)
        assert g._cache_valid is False

    def test_cache_invalidated_on_edge_add(self) -> None:
        """Test cache is invalidated when edge is added."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        # Cache result
        g.is_connected()
        assert g._cache_valid is True

        # Add edge - should invalidate
        g.add_edge(Edge(n1, n2))
        assert g._cache_valid is False

    def test_cache_invalidated_on_node_remove(self) -> None:
        """Test cache is invalidated when node is removed."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        # Cache result
        g.is_connected()
        assert g._cache_valid is True

        # Remove node - should invalidate
        g.remove_node(n1)
        assert g._cache_valid is False

    def test_cache_invalidated_on_edge_remove(self) -> None:
        """Test cache is invalidated when edge is removed."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        e = Edge(n1, n2)
        g.add_edge(e)

        # Cache result
        g.is_connected()
        assert g._cache_valid is True

        # Remove edge - should invalidate
        g.remove_edge(e)
        assert g._cache_valid is False

    def test_cache_invalidated_on_clear(self) -> None:
        """Test cache is invalidated when graph is cleared."""
        g = Graph()
        g.add_node(GraphNode("A", "n1"))

        # Cache result
        g.is_connected()
        assert g._cache_valid is True

        # Clear - should invalidate
        g.clear()
        assert g._cache_valid is False


class TestGraphClearAndEmpty:
    """Test clear and empty operations."""

    def test_clear_empty_graph(self) -> None:
        """Test clearing empty graph."""
        g = Graph()
        g.clear()
        assert g.is_empty()

    def test_clear_removes_all_nodes(self) -> None:
        """Test clear removes all nodes."""
        g = Graph()
        for i in range(5):
            g.add_node(GraphNode(f"N{i}", f"n{i}"))
        g.clear()
        assert g.node_count() == 0
        assert g.is_empty()

    def test_clear_removes_all_edges(self) -> None:
        """Test clear removes all edges."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(Edge(n1, n2))
        g.clear()
        assert g.edge_count() == 0

    def test_is_empty_true_initially(self) -> None:
        """Test is_empty returns True for new graph."""
        g = Graph()
        assert g.is_empty() is True

    def test_is_empty_false_after_adding_node(self) -> None:
        """Test is_empty returns False after adding node."""
        g = Graph()
        g.add_node(GraphNode("A", "n1"))
        assert g.is_empty() is False

    def test_is_empty_true_after_clear(self) -> None:
        """Test is_empty returns True after clear."""
        g = Graph()
        g.add_node(GraphNode("A", "n1"))
        g.clear()
        assert g.is_empty() is True


class TestGraphStringRepresentations:
    """Test string representations."""

    def test_repr_empty_graph(self) -> None:
        """Test __repr__ for empty graph."""
        g = Graph()
        assert repr(g) == "Graph(nodes=0, edges=0, multi_edges=False)"

    def test_repr_with_nodes_and_edges(self) -> None:
        """Test __repr__ with nodes and edges."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(Edge(n1, n2))
        assert repr(g) == "Graph(nodes=2, edges=1, multi_edges=False)"

    def test_repr_multigraph(self) -> None:
        """Test __repr__ for multigraph."""
        g = Graph(allow_multi_edges=True)
        assert "multi_edges=True" in repr(g)

    def test_str_empty_graph(self) -> None:
        """Test __str__ for empty graph."""
        g = Graph()
        assert str(g) == "Graph: 0 nodes, 0 edges"

    def test_str_with_nodes_and_edges(self) -> None:
        """Test __str__ with nodes and edges."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(Edge(n1, n2))
        assert str(g) == "Graph: 2 nodes, 1 edges"


class TestGraphEdgeCases:
    """Test edge cases and special scenarios."""

    def test_large_graph(self) -> None:
        """Test graph with many nodes."""
        g = Graph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(100)]
        for node in nodes:
            g.add_node(node)

        # Create chain
        for i in range(99):
            g.add_edge(Edge(nodes[i], nodes[i + 1]))

        assert g.node_count() == 100
        assert g.edge_count() == 99
        assert g.is_connected() is True

    def test_complete_graph_small(self) -> None:
        """Test complete graph (all nodes connected)."""
        g = Graph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(5)]
        for node in nodes:
            g.add_node(node)

        # Connect all pairs
        for i in range(5):
            for j in range(i + 1, 5):
                g.add_edge(Edge(nodes[i], nodes[j]))

        assert g.edge_count() == 10  # n*(n-1)/2 = 5*4/2
        assert g.is_connected() is True
        for node in nodes:
            assert g.degree(node) == 4

    def test_star_graph(self) -> None:
        """Test star graph (one central node connected to all others)."""
        g = Graph()
        center = GraphNode("Center", "center")
        g.add_node(center)

        periphery = [GraphNode(f"N{i}", f"n{i}") for i in range(5)]
        for node in periphery:
            g.add_node(node)
            g.add_edge(Edge(center, node))

        assert g.degree(center) == 5
        for node in periphery:
            assert g.degree(node) == 1
        assert g.is_connected() is True

    def test_path_graph(self) -> None:
        """Test path graph (linear chain)."""
        g = Graph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(5)]
        for node in nodes:
            g.add_node(node)

        for i in range(4):
            g.add_edge(Edge(nodes[i], nodes[i + 1]))

        assert g.degree(nodes[0]) == 1  # Endpoints
        assert g.degree(nodes[4]) == 1
        assert g.degree(nodes[2]) == 2  # Middle nodes
        assert g.is_connected() is True

    def test_adding_same_edge_object_twice_in_multigraph(self) -> None:
        """Test adding same edge object twice in multigraph."""
        g = Graph(allow_multi_edges=True)
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        e = Edge(n1, n2)
        g.add_edge(e)
        g.add_edge(e)  # Same object
        assert g.edge_count() == 2

    def test_graph_with_only_edges_no_isolated_nodes(self) -> None:
        """Test graph where all nodes have edges."""
        g = Graph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(4)]
        for node in nodes:
            g.add_node(node)

        g.add_edge(Edge(nodes[0], nodes[1]))
        g.add_edge(Edge(nodes[2], nodes[3]))

        # All nodes have degree > 0
        for node in nodes:
            assert g.degree(node) > 0

    def test_remove_edge_updates_adjacency(self) -> None:
        """Test that removing edge updates adjacency correctly."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        n3 = GraphNode("C", "n3")
        g.add_node(n1)
        g.add_node(n2)
        g.add_node(n3)

        e1 = Edge(n1, n2)
        e2 = Edge(n1, n3)
        g.add_edge(e1)
        g.add_edge(e2)

        assert g.degree(n1) == 2
        g.remove_edge(e1)
        assert g.degree(n1) == 1
        assert list(g.neighbors(n1))[0].id == "n3"


class TestGraphCountersAndProperties:
    """Test counters and property methods."""

    def test_node_count_empty(self) -> None:
        """Test node_count on empty graph."""
        g = Graph()
        assert g.node_count() == 0

    def test_edge_count_empty(self) -> None:
        """Test edge_count on empty graph."""
        g = Graph()
        assert g.edge_count() == 0

    def test_len_equals_node_count(self) -> None:
        """Test that len() equals node_count()."""
        g = Graph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(5)]
        for node in nodes:
            g.add_node(node)

        assert len(g) == g.node_count()

    def test_counters_update_on_add(self) -> None:
        """Test counters update correctly on add operations."""
        g = Graph()
        assert g.node_count() == 0
        assert g.edge_count() == 0

        n1 = GraphNode("A", "n1")
        g.add_node(n1)
        assert g.node_count() == 1

        n2 = GraphNode("B", "n2")
        g.add_node(n2)
        assert g.node_count() == 2

        g.add_edge(Edge(n1, n2))
        assert g.edge_count() == 1

    def test_counters_update_on_remove(self) -> None:
        """Test counters update correctly on remove operations."""
        g = Graph()
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


class TestGraphComplexScenarios:
    """Test complex real-world scenarios."""

    def test_triangle_graph(self) -> None:
        """Test triangle graph (3 nodes all connected)."""
        g = Graph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for node in nodes:
            g.add_node(node)

        g.add_edge(Edge(nodes[0], nodes[1]))
        g.add_edge(Edge(nodes[1], nodes[2]))
        g.add_edge(Edge(nodes[2], nodes[0]))

        assert g.edge_count() == 3
        assert g.is_connected() is True
        for node in nodes:
            assert g.degree(node) == 2

    def test_bipartite_structure(self) -> None:
        """Test bipartite-like structure."""
        g = Graph()
        set_a = [GraphNode(f"A{i}", f"a{i}") for i in range(3)]
        set_b = [GraphNode(f"B{i}", f"b{i}") for i in range(2)]

        for node in set_a + set_b:
            g.add_node(node)

        # Connect each node in set_a to all nodes in set_b
        for a in set_a:
            for b in set_b:
                g.add_edge(Edge(a, b))

        assert g.edge_count() == 6  # 3 * 2
        for a in set_a:
            assert g.degree(a) == 2
        for b in set_b:
            assert g.degree(b) == 3

    def test_modify_after_query(self) -> None:
        """Test modifying graph after connectivity query."""
        g = Graph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        # Initially disconnected
        assert g.is_connected() is False

        # Add edge
        g.add_edge(Edge(n1, n2))

        # Now connected
        assert g.is_connected() is True

    def test_multigraph_degree_calculation(self) -> None:
        """Test degree calculation in multigraph with multiple edges."""
        g = Graph(allow_multi_edges=True)
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        # Add 3 edges between same nodes
        for i in range(3):
            g.add_edge(Edge(n1, n2, data=f"edge{i}"))

        # Degree should count all edges
        assert g.degree(n1) == 3
        assert g.degree(n2) == 3
