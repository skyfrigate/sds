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

"""Unit tests for DirectedGraph class - Part 1."""

import pytest

from sds.graph.directed import DirectedGraph
from sds.graph.edge import DirectedEdge, Edge
from sds.graph.interfaces import AbstractDirectedGraph, AbstractGraph
from sds.graph.node import GraphNode


class TestDirectedGraphCreation:
    """Test DirectedGraph initialization."""

    def test_create_empty_graph(self) -> None:
        """Test creating an empty directed graph."""
        g = DirectedGraph()
        assert g.is_empty()
        assert g.node_count() == 0
        assert g.edge_count() == 0
        assert len(g) == 0

    def test_create_with_multi_edges_disabled(self) -> None:
        """Test creating graph with multi-edges disabled."""
        g = DirectedGraph(allow_multi_edges=False)
        assert g.allow_multi_edges is False

    def test_create_with_multi_edges_enabled(self) -> None:
        """Test creating graph with multi-edges enabled."""
        g = DirectedGraph(allow_multi_edges=True)
        assert g.allow_multi_edges is True

    def test_inherits_from_abstract_directed_graph(self) -> None:
        """Test that DirectedGraph inherits from AbstractDirectedGraph."""
        g = DirectedGraph()
        assert isinstance(g, AbstractDirectedGraph)
        assert isinstance(g, AbstractGraph)


class TestDirectedGraphNodeOperations:
    """Test node addition and removal."""

    def test_add_single_node(self) -> None:
        """Test adding a single node."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        g.add_node(n1)
        assert g.has_node(n1)
        assert g.node_count() == 1

    def test_add_multiple_nodes(self) -> None:
        """Test adding multiple nodes."""
        g = DirectedGraph()
        nodes = [GraphNode(f"Node{i}", f"n{i}") for i in range(5)]
        for node in nodes:
            g.add_node(node)
        assert g.node_count() == 5
        for node in nodes:
            assert g.has_node(node)

    def test_add_duplicate_node_raises_error(self) -> None:
        """Test that adding duplicate node raises ValueError."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        g.add_node(n1)
        with pytest.raises(ValueError, match="already exists"):
            g.add_node(n1)

    def test_add_non_graphnode_raises_error(self) -> None:
        """Test that adding non-GraphNode raises TypeError."""
        g = DirectedGraph()
        with pytest.raises(TypeError, match="Expected GraphNode"):
            g.add_node("not a node")  # type: ignore[arg-type]

    def test_remove_node(self) -> None:
        """Test removing a node."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        g.add_node(n1)
        g.remove_node(n1)
        assert g.has_node(n1) is False
        assert g.node_count() == 0

    def test_remove_node_with_edges(self) -> None:
        """Test removing node also removes incident edges."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        n3 = GraphNode("C", "n3")
        g.add_node(n1)
        g.add_node(n2)
        g.add_node(n3)
        g.add_edge(DirectedEdge(n1, n2))
        g.add_edge(DirectedEdge(n3, n1))

        assert g.edge_count() == 2
        g.remove_node(n1)
        assert g.edge_count() == 0

    def test_remove_nonexistent_node_raises_error(self) -> None:
        """Test removing nonexistent node raises ValueError."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        with pytest.raises(ValueError, match="not in graph"):
            g.remove_node(n1)

    def test_get_node_by_id(self) -> None:
        """Test getting node by ID."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        g.add_node(n1)
        found = g.get_node_by_id("n1")
        assert found is n1

    def test_get_node_by_id_nonexistent(self) -> None:
        """Test getting nonexistent node by ID returns None."""
        g = DirectedGraph()
        found = g.get_node_by_id("n999")
        assert found is None


class TestDirectedGraphEdgeOperations:
    """Test edge addition and removal with direction."""

    def test_add_directed_edge(self) -> None:
        """Test adding a directed edge."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        e = DirectedEdge(n1, n2)
        g.add_edge(e)
        assert g.has_edge(n1, n2)
        assert g.edge_count() == 1

    def test_edge_direction_matters(self) -> None:
        """Test that edge direction is respected."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(DirectedEdge(n1, n2))

        # Edge exists in one direction only
        assert g.has_edge(n1, n2) is True
        assert g.has_edge(n2, n1) is False

    def test_add_edge_requires_directed_edge(self) -> None:
        """Test that add_edge requires DirectedEdge."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        # Regular Edge should raise TypeError
        with pytest.raises(TypeError, match="Expected DirectedEdge"):
            g.add_edge(Edge(n1, n2))  # type: ignore[arg-type]

    def test_add_edge_with_nonexistent_source(self) -> None:
        """Test adding edge with nonexistent source raises ValueError."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n2)
        # n1 not added
        with pytest.raises(ValueError, match="Source node.*not in graph"):
            g.add_edge(DirectedEdge(n1, n2))

    def test_add_edge_with_nonexistent_target(self) -> None:
        """Test adding edge with nonexistent target raises ValueError."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        # n2 not added
        with pytest.raises(ValueError, match="Target node.*not in graph"):
            g.add_edge(DirectedEdge(n1, n2))

    def test_add_duplicate_edge_raises_error(self) -> None:
        """Test adding duplicate edge raises ValueError."""
        g = DirectedGraph(allow_multi_edges=False)
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(DirectedEdge(n1, n2))
        with pytest.raises(ValueError, match="already exists"):
            g.add_edge(DirectedEdge(n1, n2))

    def test_add_multiple_edges_in_multidigraph(self) -> None:
        """Test adding multiple edges in multi-digraph."""
        g = DirectedGraph(allow_multi_edges=True)
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(DirectedEdge(n1, n2, data="edge1"))
        g.add_edge(DirectedEdge(n1, n2, data="edge2"))
        assert g.edge_count() == 2

    def test_bidirectional_edges_allowed(self) -> None:
        """Test that bidirectional edges (both directions) are allowed."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(DirectedEdge(n1, n2))
        g.add_edge(DirectedEdge(n2, n1))  # Opposite direction - OK
        assert g.edge_count() == 2

    def test_get_edge(self) -> None:
        """Test getting a directed edge."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        e = DirectedEdge(n1, n2, data="test")
        g.add_edge(e)
        found = g.get_edge(n1, n2)
        assert found is not None
        assert found.data == "test"

    def test_get_edge_respects_direction(self) -> None:
        """Test that get_edge respects direction."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(DirectedEdge(n1, n2))

        assert g.get_edge(n1, n2) is not None
        assert g.get_edge(n2, n1) is None  # Wrong direction

    def test_remove_edge(self) -> None:
        """Test removing a directed edge."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        e = DirectedEdge(n1, n2)
        g.add_edge(e)
        g.remove_edge(e)
        assert g.has_edge(n1, n2) is False
        assert g.edge_count() == 0

    def test_remove_nonexistent_edge_raises_error(self) -> None:
        """Test removing nonexistent edge raises ValueError."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        e = DirectedEdge(n1, n2)
        with pytest.raises(ValueError, match="not in graph"):
            g.remove_edge(e)


class TestDirectedGraphDegrees:
    """Test degree calculations for directed graphs."""

    def test_in_degree_isolated_node(self) -> None:
        """Test in-degree of isolated node is 0."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        g.add_node(n1)
        assert g.in_degree(n1) == 0

    def test_out_degree_isolated_node(self) -> None:
        """Test out-degree of isolated node is 0."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        g.add_node(n1)
        assert g.out_degree(n1) == 0

    def test_in_degree_with_incoming_edge(self) -> None:
        """Test in-degree with incoming edges."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(DirectedEdge(n1, n2))

        assert g.in_degree(n2) == 1
        assert g.in_degree(n1) == 0

    def test_out_degree_with_outgoing_edge(self) -> None:
        """Test out-degree with outgoing edges."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(DirectedEdge(n1, n2))

        assert g.out_degree(n1) == 1
        assert g.out_degree(n2) == 0

    def test_total_degree(self) -> None:
        """Test total degree (in + out)."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        n3 = GraphNode("C", "n3")
        g.add_node(n1)
        g.add_node(n2)
        g.add_node(n3)
        g.add_edge(DirectedEdge(n1, n2))
        g.add_edge(DirectedEdge(n3, n2))

        # n2 has 2 incoming, 0 outgoing
        assert g.degree(n2) == 2

    def test_in_degree_multiple_edges(self) -> None:
        """Test in-degree with multiple incoming edges."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        n3 = GraphNode("C", "n3")
        n4 = GraphNode("D", "n4")
        g.add_node(n1)
        g.add_node(n2)
        g.add_node(n3)
        g.add_node(n4)

        # Multiple edges to n4
        g.add_edge(DirectedEdge(n1, n4))
        g.add_edge(DirectedEdge(n2, n4))
        g.add_edge(DirectedEdge(n3, n4))

        assert g.in_degree(n4) == 3

    def test_out_degree_multiple_edges(self) -> None:
        """Test out-degree with multiple outgoing edges."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        n3 = GraphNode("C", "n3")
        n4 = GraphNode("D", "n4")
        g.add_node(n1)
        g.add_node(n2)
        g.add_node(n3)
        g.add_node(n4)

        # Multiple edges from n1
        g.add_edge(DirectedEdge(n1, n2))
        g.add_edge(DirectedEdge(n1, n3))
        g.add_edge(DirectedEdge(n1, n4))

        assert g.out_degree(n1) == 3

    def test_degree_in_multidigraph(self) -> None:
        """Test degree counts all edges in multi-digraph."""
        g = DirectedGraph(allow_multi_edges=True)
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        # Add multiple edges in same direction
        g.add_edge(DirectedEdge(n1, n2))
        g.add_edge(DirectedEdge(n1, n2))
        g.add_edge(DirectedEdge(n1, n2))

        assert g.out_degree(n1) == 3
        assert g.in_degree(n2) == 3

    def test_degree_nonexistent_node_raises_error(self) -> None:
        """Test degree queries on nonexistent node raise ValueError."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")

        with pytest.raises(ValueError, match="not in graph"):
            g.degree(n1)
        with pytest.raises(ValueError, match="not in graph"):
            g.in_degree(n1)
        with pytest.raises(ValueError, match="not in graph"):
            g.out_degree(n1)


class TestDirectedGraphPredecessorsSuccessors:
    """Test predecessor and successor queries."""

    def test_successors_empty(self) -> None:
        """Test successors of node with no outgoing edges."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        g.add_node(n1)
        successors = list(g.successors(n1))
        assert len(successors) == 0

    def test_predecessors_empty(self) -> None:
        """Test predecessors of node with no incoming edges."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        g.add_node(n1)
        predecessors = list(g.predecessors(n1))
        assert len(predecessors) == 0

    def test_successors_single(self) -> None:
        """Test successors with one outgoing edge."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(DirectedEdge(n1, n2))

        successors = list(g.successors(n1))
        assert len(successors) == 1
        assert successors[0].id == "n2"

    def test_predecessors_single(self) -> None:
        """Test predecessors with one incoming edge."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(DirectedEdge(n1, n2))

        predecessors = list(g.predecessors(n2))
        assert len(predecessors) == 1
        assert predecessors[0].id == "n1"

    def test_successors_multiple(self) -> None:
        """Test successors with multiple outgoing edges."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        n3 = GraphNode("C", "n3")
        n4 = GraphNode("D", "n4")
        g.add_node(n1)
        g.add_node(n2)
        g.add_node(n3)
        g.add_node(n4)

        g.add_edge(DirectedEdge(n1, n2))
        g.add_edge(DirectedEdge(n1, n3))
        g.add_edge(DirectedEdge(n1, n4))

        successor_ids = {n.id for n in g.successors(n1)}
        assert successor_ids == {"n2", "n3", "n4"}

    def test_predecessors_multiple(self) -> None:
        """Test predecessors with multiple incoming edges."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        n3 = GraphNode("C", "n3")
        n4 = GraphNode("D", "n4")
        g.add_node(n1)
        g.add_node(n2)
        g.add_node(n3)
        g.add_node(n4)

        g.add_edge(DirectedEdge(n1, n4))
        g.add_edge(DirectedEdge(n2, n4))
        g.add_edge(DirectedEdge(n3, n4))

        predecessor_ids = {n.id for n in g.predecessors(n4)}
        assert predecessor_ids == {"n1", "n2", "n3"}

    def test_neighbors_equals_successors(self) -> None:
        """Test that neighbors() returns successors for directed graphs."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        n3 = GraphNode("C", "n3")
        g.add_node(n1)
        g.add_node(n2)
        g.add_node(n3)
        g.add_edge(DirectedEdge(n1, n2))
        g.add_edge(DirectedEdge(n1, n3))

        neighbors = set(n.id for n in g.neighbors(n1))
        successors = set(n.id for n in g.successors(n1))
        assert neighbors == successors

    def test_predecessors_nonexistent_node_raises_error(self) -> None:
        """Test predecessors of nonexistent node raises ValueError."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        with pytest.raises(ValueError, match="not in graph"):
            list(g.predecessors(n1))

    def test_successors_nonexistent_node_raises_error(self) -> None:
        """Test successors of nonexistent node raises ValueError."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        with pytest.raises(ValueError, match="not in graph"):
            list(g.successors(n1))


class TestDirectedGraphAcyclicity:
    """Test cycle detection (is_acyclic)."""

    def test_empty_graph_is_acyclic(self) -> None:
        """Test empty graph is acyclic."""
        g = DirectedGraph()
        assert g.is_acyclic() is True

    def test_single_node_is_acyclic(self) -> None:
        """Test single node is acyclic."""
        g = DirectedGraph()
        g.add_node(GraphNode("A", "n1"))
        assert g.is_acyclic() is True

    def test_linear_chain_is_acyclic(self) -> None:
        """Test linear chain (DAG) is acyclic."""
        g = DirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(4)]
        for node in nodes:
            g.add_node(node)

        # Create chain: n0 -> n1 -> n2 -> n3
        g.add_edge(DirectedEdge(nodes[0], nodes[1]))
        g.add_edge(DirectedEdge(nodes[1], nodes[2]))
        g.add_edge(DirectedEdge(nodes[2], nodes[3]))

        assert g.is_acyclic() is True

    def test_simple_cycle_detected(self) -> None:
        """Test simple cycle is detected."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        # Create cycle: n1 -> n2 -> n1
        g.add_edge(DirectedEdge(n1, n2))
        g.add_edge(DirectedEdge(n2, n1))

        assert g.is_acyclic() is False

    def test_triangle_cycle_detected(self) -> None:
        """Test triangle cycle is detected."""
        g = DirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for node in nodes:
            g.add_node(node)

        # Create cycle: n0 -> n1 -> n2 -> n0
        g.add_edge(DirectedEdge(nodes[0], nodes[1]))
        g.add_edge(DirectedEdge(nodes[1], nodes[2]))
        g.add_edge(DirectedEdge(nodes[2], nodes[0]))

        assert g.is_acyclic() is False

    def test_complex_dag(self) -> None:
        """Test complex DAG structure."""
        g = DirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(6)]
        for node in nodes:
            g.add_node(node)

        # Create diamond DAG
        g.add_edge(DirectedEdge(nodes[0], nodes[1]))
        g.add_edge(DirectedEdge(nodes[0], nodes[2]))
        g.add_edge(DirectedEdge(nodes[1], nodes[3]))
        g.add_edge(DirectedEdge(nodes[2], nodes[3]))
        g.add_edge(DirectedEdge(nodes[3], nodes[4]))
        g.add_edge(DirectedEdge(nodes[3], nodes[5]))

        assert g.is_acyclic() is True

    def test_dag_becomes_cyclic(self) -> None:
        """Test DAG becomes cyclic when edge added."""
        g = DirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for node in nodes:
            g.add_node(node)

        # Create DAG: n0 -> n1 -> n2
        g.add_edge(DirectedEdge(nodes[0], nodes[1]))
        g.add_edge(DirectedEdge(nodes[1], nodes[2]))
        assert g.is_acyclic() is True

        # Add back edge to create cycle
        g.add_edge(DirectedEdge(nodes[2], nodes[0]))
        assert g.is_acyclic() is False

    def test_disconnected_acyclic_components(self) -> None:
        """Test disconnected acyclic components."""
        g = DirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(4)]
        for node in nodes:
            g.add_node(node)

        # Two separate chains
        g.add_edge(DirectedEdge(nodes[0], nodes[1]))
        g.add_edge(DirectedEdge(nodes[2], nodes[3]))

        assert g.is_acyclic() is True

    def test_cycle_in_one_component(self) -> None:
        """Test cycle in one of multiple components."""
        g = DirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(4)]
        for node in nodes:
            g.add_node(node)

        # One acyclic component, one with cycle
        g.add_edge(DirectedEdge(nodes[0], nodes[1]))  # Acyclic
        g.add_edge(DirectedEdge(nodes[2], nodes[3]))  # Cycle
        g.add_edge(DirectedEdge(nodes[3], nodes[2]))

        assert g.is_acyclic() is False


class TestDirectedGraphConnectivity:
    """Test weak connectivity checking."""

    def test_empty_graph_is_connected(self) -> None:
        """Test empty graph is considered connected."""
        g = DirectedGraph()
        assert g.is_connected() is True

    def test_single_node_is_connected(self) -> None:
        """Test single node is connected."""
        g = DirectedGraph()
        g.add_node(GraphNode("A", "n1"))
        assert g.is_connected() is True

    def test_two_nodes_with_edge_connected(self) -> None:
        """Test two nodes with directed edge are weakly connected."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(DirectedEdge(n1, n2))
        assert g.is_connected() is True

    def test_two_isolated_nodes_not_connected(self) -> None:
        """Test two isolated nodes are not connected."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        assert g.is_connected() is False

    def test_chain_is_connected(self) -> None:
        """Test directed chain is weakly connected."""
        g = DirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(5)]
        for node in nodes:
            g.add_node(node)

        for i in range(4):
            g.add_edge(DirectedEdge(nodes[i], nodes[i + 1]))

        assert g.is_connected() is True

    def test_cycle_is_connected(self) -> None:
        """Test cycle is connected."""
        g = DirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for node in nodes:
            g.add_node(node)

        g.add_edge(DirectedEdge(nodes[0], nodes[1]))
        g.add_edge(DirectedEdge(nodes[1], nodes[2]))
        g.add_edge(DirectedEdge(nodes[2], nodes[0]))

        assert g.is_connected() is True

    def test_disconnected_components(self) -> None:
        """Test graph with disconnected components."""
        g = DirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(4)]
        for node in nodes:
            g.add_node(node)

        # Two components: (n0->n1) and (n2->n3)
        g.add_edge(DirectedEdge(nodes[0], nodes[1]))
        g.add_edge(DirectedEdge(nodes[2], nodes[3]))

        assert g.is_connected() is False

    def test_weakly_connected_not_strongly(self) -> None:
        """Test weak connectivity vs strong connectivity."""
        g = DirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for node in nodes:
            g.add_node(node)

        # Chain: n0 -> n1 -> n2 (weakly connected but not strongly)
        g.add_edge(DirectedEdge(nodes[0], nodes[1]))
        g.add_edge(DirectedEdge(nodes[1], nodes[2]))

        # Weakly connected (can reach all via undirected path)
        assert g.is_connected() is True


class TestDirectedGraphCaching:
    """Test caching of expensive operations."""

    def test_acyclic_cache(self) -> None:
        """Test that acyclicity result is cached."""
        g = DirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for node in nodes:
            g.add_node(node)
        g.add_edge(DirectedEdge(nodes[0], nodes[1]))

        # First call - computes
        result1 = g.is_acyclic()
        # Second call - should use cache
        result2 = g.is_acyclic()

        assert result1 is True
        assert result2 is True
        assert g._cache_valid is True

    def test_connectivity_cache(self) -> None:
        """Test that connectivity result is cached."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(DirectedEdge(n1, n2))

        # First call - computes
        result1 = g.is_connected()
        # Second call - should use cache
        result2 = g.is_connected()

        assert result1 is True
        assert result2 is True
        assert g._cache_valid is True

    def test_cache_invalidated_on_node_add(self) -> None:
        """Test cache invalidated when node added."""
        g = DirectedGraph()
        g.add_node(GraphNode("A", "n1"))

        # Cache results
        g.is_acyclic()
        g.is_connected()
        assert g._cache_valid is True

        # Add node - invalidates
        g.add_node(GraphNode("B", "n2"))
        assert g._cache_valid is False

    def test_cache_invalidated_on_edge_add(self) -> None:
        """Test cache invalidated when edge added."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        # Cache results
        g.is_acyclic()
        g.is_connected()
        assert g._cache_valid is True

        # Add edge - invalidates
        g.add_edge(DirectedEdge(n1, n2))
        assert g._cache_valid is False

    def test_cache_invalidated_on_node_remove(self) -> None:
        """Test cache invalidated when node removed."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        # Cache results
        g.is_acyclic()
        assert g._cache_valid is True

        # Remove node - invalidates
        g.remove_node(n1)
        assert g._cache_valid is False

    def test_cache_invalidated_on_edge_remove(self) -> None:
        """Test cache invalidated when edge removed."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        e = DirectedEdge(n1, n2)
        g.add_edge(e)

        # Cache results
        g.is_acyclic()
        assert g._cache_valid is True

        # Remove edge - invalidates
        g.remove_edge(e)
        assert g._cache_valid is False

    def test_cache_invalidated_on_clear(self) -> None:
        """Test cache invalidated when graph cleared."""
        g = DirectedGraph()
        g.add_node(GraphNode("A", "n1"))

        # Cache results
        g.is_acyclic()
        assert g._cache_valid is True

        # Clear - invalidates
        g.clear()
        assert g._cache_valid is False


class TestDirectedGraphIteration:
    """Test iteration protocols."""

    def test_nodes_iteration(self) -> None:
        """Test iterating over nodes."""
        g = DirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for node in nodes:
            g.add_node(node)

        node_ids = {n.id for n in g.nodes()}
        assert node_ids == {"n0", "n1", "n2"}

    def test_edges_iteration(self) -> None:
        """Test iterating over edges."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        n3 = GraphNode("C", "n3")
        g.add_node(n1)
        g.add_node(n2)
        g.add_node(n3)
        g.add_edge(DirectedEdge(n1, n2))
        g.add_edge(DirectedEdge(n2, n3))

        edges = list(g.edges())
        assert len(edges) == 2

    def test_iter_protocol(self) -> None:
        """Test __iter__ iterates over nodes."""
        g = DirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for node in nodes:
            g.add_node(node)

        node_ids = {n.id for n in g}
        assert node_ids == {"n0", "n1", "n2"}

    def test_contains_protocol(self) -> None:
        """Test __contains__ checks node membership."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)

        assert n1 in g
        assert n2 not in g

    def test_len_protocol(self) -> None:
        """Test __len__ returns node count."""
        g = DirectedGraph()
        assert len(g) == 0

        for i in range(5):
            g.add_node(GraphNode(f"N{i}", f"n{i}"))

        assert len(g) == 5


class TestDirectedGraphStringRepresentations:
    """Test string representations."""

    def test_repr_empty_graph(self) -> None:
        """Test __repr__ for empty graph."""
        g = DirectedGraph()
        assert repr(g) == "DirectedGraph(nodes=0, edges=0, multi_edges=False)"

    def test_repr_with_nodes_and_edges(self) -> None:
        """Test __repr__ with nodes and edges."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(DirectedEdge(n1, n2))
        assert repr(g) == "DirectedGraph(nodes=2, edges=1, multi_edges=False)"

    def test_repr_multidigraph(self) -> None:
        """Test __repr__ for multi-digraph."""
        g = DirectedGraph(allow_multi_edges=True)
        assert "multi_edges=True" in repr(g)

    def test_str_empty_graph(self) -> None:
        """Test __str__ for empty graph."""
        g = DirectedGraph()
        assert str(g) == "DirectedGraph: 0 nodes, 0 edges"

    def test_str_with_nodes_and_edges(self) -> None:
        """Test __str__ with nodes and edges."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(DirectedEdge(n1, n2))
        assert str(g) == "DirectedGraph: 2 nodes, 1 edges"


class TestDirectedGraphClearAndEmpty:
    """Test clear and empty operations."""

    def test_clear_empty_graph(self) -> None:
        """Test clearing empty graph."""
        g = DirectedGraph()
        g.clear()
        assert g.is_empty()

    def test_clear_removes_all_nodes(self) -> None:
        """Test clear removes all nodes."""
        g = DirectedGraph()
        for i in range(5):
            g.add_node(GraphNode(f"N{i}", f"n{i}"))
        g.clear()
        assert g.node_count() == 0
        assert g.is_empty()

    def test_clear_removes_all_edges(self) -> None:
        """Test clear removes all edges."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(DirectedEdge(n1, n2))
        g.clear()
        assert g.edge_count() == 0

    def test_is_empty_true_initially(self) -> None:
        """Test is_empty returns True for new graph."""
        g = DirectedGraph()
        assert g.is_empty() is True

    def test_is_empty_false_after_adding_node(self) -> None:
        """Test is_empty returns False after adding node."""
        g = DirectedGraph()
        g.add_node(GraphNode("A", "n1"))
        assert g.is_empty() is False

    def test_is_empty_true_after_clear(self) -> None:
        """Test is_empty returns True after clear."""
        g = DirectedGraph()
        g.add_node(GraphNode("A", "n1"))
        g.clear()
        assert g.is_empty() is True


class TestDirectedGraphCounters:
    """Test counter methods."""

    def test_node_count_empty(self) -> None:
        """Test node_count on empty graph."""
        g = DirectedGraph()
        assert g.node_count() == 0

    def test_edge_count_empty(self) -> None:
        """Test edge_count on empty graph."""
        g = DirectedGraph()
        assert g.edge_count() == 0

    def test_counters_update_on_add(self) -> None:
        """Test counters update on add operations."""
        g = DirectedGraph()
        assert g.node_count() == 0
        assert g.edge_count() == 0

        n1 = GraphNode("A", "n1")
        g.add_node(n1)
        assert g.node_count() == 1

        n2 = GraphNode("B", "n2")
        g.add_node(n2)
        assert g.node_count() == 2

        g.add_edge(DirectedEdge(n1, n2))
        assert g.edge_count() == 1

    def test_counters_update_on_remove(self) -> None:
        """Test counters update on remove operations."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        e = DirectedEdge(n1, n2)
        g.add_edge(e)

        g.remove_edge(e)
        assert g.edge_count() == 0

        g.remove_node(n1)
        assert g.node_count() == 1


class TestDirectedGraphComplexTopologies:
    """Test complex graph topologies."""

    def test_dag_topological_structure(self) -> None:
        """Test DAG with typical topological structure."""
        g = DirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(6)]
        for node in nodes:
            g.add_node(node)

        # Create typical DAG (dependency graph)
        g.add_edge(DirectedEdge(nodes[0], nodes[2]))
        g.add_edge(DirectedEdge(nodes[1], nodes[2]))
        g.add_edge(DirectedEdge(nodes[2], nodes[3]))
        g.add_edge(DirectedEdge(nodes[2], nodes[4]))
        g.add_edge(DirectedEdge(nodes[3], nodes[5]))
        g.add_edge(DirectedEdge(nodes[4], nodes[5]))

        assert g.is_acyclic() is True
        assert g.is_connected() is True

    def test_tournament_graph(self) -> None:
        """Test tournament graph (complete directed graph)."""
        g = DirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(4)]
        for node in nodes:
            g.add_node(node)

        # Create tournament (one direction for each pair)
        g.add_edge(DirectedEdge(nodes[0], nodes[1]))
        g.add_edge(DirectedEdge(nodes[0], nodes[2]))
        g.add_edge(DirectedEdge(nodes[0], nodes[3]))
        g.add_edge(DirectedEdge(nodes[1], nodes[2]))
        g.add_edge(DirectedEdge(nodes[1], nodes[3]))
        g.add_edge(DirectedEdge(nodes[2], nodes[3]))

        assert g.edge_count() == 6  # n*(n-1)/2
        assert g.is_acyclic() is True

    def test_out_tree(self) -> None:
        """Test out-tree (arborescence)."""
        g = DirectedGraph()
        root = GraphNode("Root", "root")
        g.add_node(root)

        # Create tree with root having out-edges
        children = [GraphNode(f"C{i}", f"c{i}") for i in range(3)]
        for child in children:
            g.add_node(child)
            g.add_edge(DirectedEdge(root, child))

        # Add grandchildren
        for i, child in enumerate(children):
            for j in range(2):
                grandchild = GraphNode(f"GC{i}_{j}", f"gc{i}_{j}")
                g.add_node(grandchild)
                g.add_edge(DirectedEdge(child, grandchild))

        assert g.is_acyclic() is True
        assert g.out_degree(root) == 3
        assert g.in_degree(root) == 0

    def test_in_tree(self) -> None:
        """Test in-tree (reverse arborescence)."""
        g = DirectedGraph()
        root = GraphNode("Root", "root")
        g.add_node(root)

        # Create tree with root having in-edges
        parents = [GraphNode(f"P{i}", f"p{i}") for i in range(3)]
        for parent in parents:
            g.add_node(parent)
            g.add_edge(DirectedEdge(parent, root))

        assert g.is_acyclic() is True
        assert g.in_degree(root) == 3
        assert g.out_degree(root) == 0

    def test_strongly_connected_component(self) -> None:
        """Test strongly connected component (cycle)."""
        g = DirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(4)]
        for node in nodes:
            g.add_node(node)

        # Create strongly connected component
        g.add_edge(DirectedEdge(nodes[0], nodes[1]))
        g.add_edge(DirectedEdge(nodes[1], nodes[2]))
        g.add_edge(DirectedEdge(nodes[2], nodes[3]))
        g.add_edge(DirectedEdge(nodes[3], nodes[0]))

        assert g.is_acyclic() is False
        assert g.is_connected() is True


class TestDirectedGraphEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_large_dag(self) -> None:
        """Test large DAG."""
        g = DirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(100)]
        for node in nodes:
            g.add_node(node)

        # Create long chain
        for i in range(99):
            g.add_edge(DirectedEdge(nodes[i], nodes[i + 1]))

        assert g.node_count() == 100
        assert g.edge_count() == 99
        assert g.is_acyclic() is True
        assert g.is_connected() is True

    def test_many_parallel_edges_in_multidigraph(self) -> None:
        """Test many parallel edges in multi-digraph."""
        g = DirectedGraph(allow_multi_edges=True)
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        # Add many parallel edges
        for i in range(10):
            g.add_edge(DirectedEdge(n1, n2, data=f"edge{i}"))

        assert g.edge_count() == 10
        assert g.out_degree(n1) == 10
        assert g.in_degree(n2) == 10

    def test_bidirectional_edges(self) -> None:
        """Test bidirectional edges (both directions)."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        # Add edges in both directions
        g.add_edge(DirectedEdge(n1, n2))
        g.add_edge(DirectedEdge(n2, n1))

        assert g.edge_count() == 2
        assert g.has_edge(n1, n2)
        assert g.has_edge(n2, n1)
        assert g.is_acyclic() is False  # Cycle!

    def test_isolated_nodes_with_connected_component(self) -> None:
        """Test isolated nodes alongside connected component."""
        g = DirectedGraph()
        # Connected component
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(DirectedEdge(n1, n2))

        # Isolated nodes
        n3 = GraphNode("C", "n3")
        n4 = GraphNode("D", "n4")
        g.add_node(n3)
        g.add_node(n4)

        assert g.is_connected() is False
        assert g.out_degree(n3) == 0
        assert g.in_degree(n3) == 0

    def test_hub_node(self) -> None:
        """Test hub node (high degree)."""
        g = DirectedGraph()
        hub = GraphNode("Hub", "hub")
        g.add_node(hub)

        # Create hub with many outgoing edges
        for i in range(20):
            node = GraphNode(f"N{i}", f"n{i}")
            g.add_node(node)
            g.add_edge(DirectedEdge(hub, node))

        assert g.out_degree(hub) == 20
        assert g.in_degree(hub) == 0
        assert len(list(g.successors(hub))) == 20

    def test_sink_node(self) -> None:
        """Test sink node (only incoming edges)."""
        g = DirectedGraph()
        sink = GraphNode("Sink", "sink")
        g.add_node(sink)

        # Create sink with many incoming edges
        for i in range(20):
            node = GraphNode(f"N{i}", f"n{i}")
            g.add_node(node)
            g.add_edge(DirectedEdge(node, sink))

        assert g.in_degree(sink) == 20
        assert g.out_degree(sink) == 0
        assert len(list(g.predecessors(sink))) == 20

    def test_source_node(self) -> None:
        """Test source node (only outgoing edges)."""
        g = DirectedGraph()
        source = GraphNode("Source", "source")
        g.add_node(source)

        # Source has no incoming edges
        node = GraphNode("Target", "target")
        g.add_node(node)
        g.add_edge(DirectedEdge(source, node))

        assert g.in_degree(source) == 0
        assert g.out_degree(source) == 1


class TestDirectedGraphSpecialScenarios:
    """Test special scenarios and use cases."""

    def test_dependency_graph(self) -> None:
        """Test dependency graph (common use case)."""
        g = DirectedGraph()

        # Tasks with dependencies
        tasks = {
            "compile": GraphNode("Compile", "compile"),
            "test": GraphNode("Test", "test"),
            "build": GraphNode("Build", "build"),
            "deploy": GraphNode("Deploy", "deploy"),
        }

        for task in tasks.values():
            g.add_node(task)

        # Dependencies
        g.add_edge(DirectedEdge(tasks["compile"], tasks["test"]))
        g.add_edge(DirectedEdge(tasks["test"], tasks["build"]))
        g.add_edge(DirectedEdge(tasks["build"], tasks["deploy"]))

        assert g.is_acyclic() is True
        assert g.out_degree(tasks["compile"]) == 1
        assert g.in_degree(tasks["deploy"]) == 1

    def test_state_machine(self) -> None:
        """Test state machine representation."""
        g = DirectedGraph(allow_multi_edges=True)

        states = {
            "idle": GraphNode("Idle", "idle"),
            "running": GraphNode("Running", "running"),
            "paused": GraphNode("Paused", "paused"),
            "stopped": GraphNode("Stopped", "stopped"),
        }

        for state in states.values():
            g.add_node(state)

        # Transitions
        g.add_edge(DirectedEdge(states["idle"], states["running"], data="start"))
        g.add_edge(DirectedEdge(states["running"], states["paused"], data="pause"))
        g.add_edge(DirectedEdge(states["paused"], states["running"], data="resume"))
        g.add_edge(DirectedEdge(states["running"], states["stopped"], data="stop"))
        g.add_edge(DirectedEdge(states["paused"], states["stopped"], data="stop"))

        # Has cycle (running <-> paused)
        assert g.is_acyclic() is False

    def test_citation_network(self) -> None:
        """Test citation network (papers citing other papers)."""
        g = DirectedGraph()

        papers = [GraphNode(f"Paper{i}", f"p{i}") for i in range(5)]
        for paper in papers:
            g.add_node(paper)

        # Citations (newer papers cite older ones)
        g.add_edge(DirectedEdge(papers[4], papers[0]))  # P4 cites P0
        g.add_edge(DirectedEdge(papers[4], papers[1]))  # P4 cites P1
        g.add_edge(DirectedEdge(papers[3], papers[0]))  # P3 cites P0
        g.add_edge(DirectedEdge(papers[3], papers[2]))  # P3 cites P2
        g.add_edge(DirectedEdge(papers[2], papers[0]))  # P2 cites P0

        assert g.is_acyclic() is True  # No paper cites future papers
        assert g.in_degree(papers[0]) == 3  # Most cited

    def test_remove_edge_in_multidigraph(self) -> None:
        """Test removing one of multiple parallel edges."""
        g = DirectedGraph(allow_multi_edges=True)
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        e1 = DirectedEdge(n1, n2, data="edge1")
        e2 = DirectedEdge(n1, n2, data="edge2")
        e3 = DirectedEdge(n1, n2, data="edge3")
        g.add_edge(e1)
        g.add_edge(e2)
        g.add_edge(e3)

        # Remove one edge
        g.remove_edge(e2)
        assert g.edge_count() == 2
        assert g.has_edge(n1, n2)  # Others still exist

    def test_modify_after_acyclic_check(self) -> None:
        """Test modifying graph after acyclicity check."""
        g = DirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(3)]
        for node in nodes:
            g.add_node(node)

        # Create DAG
        g.add_edge(DirectedEdge(nodes[0], nodes[1]))
        g.add_edge(DirectedEdge(nodes[1], nodes[2]))
        assert g.is_acyclic() is True

        # Add cycle
        g.add_edge(DirectedEdge(nodes[2], nodes[0]))
        assert g.is_acyclic() is False


class TestDirectedGraphDegreeProperties:
    """Test degree properties and invariants."""

    def test_sum_of_in_degrees_equals_sum_of_out_degrees(self) -> None:
        """Test that total in-degree equals total out-degree."""
        g = DirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(5)]
        for node in nodes:
            g.add_node(node)

        # Add various edges
        g.add_edge(DirectedEdge(nodes[0], nodes[1]))
        g.add_edge(DirectedEdge(nodes[1], nodes[2]))
        g.add_edge(DirectedEdge(nodes[2], nodes[3]))
        g.add_edge(DirectedEdge(nodes[3], nodes[4]))
        g.add_edge(DirectedEdge(nodes[0], nodes[4]))

        total_in = sum(g.in_degree(n) for n in nodes)
        total_out = sum(g.out_degree(n) for n in nodes)

        assert total_in == total_out
        assert total_in == g.edge_count()

    def test_degree_equals_in_plus_out(self) -> None:
        """Test that degree = in_degree + out_degree."""
        g = DirectedGraph()
        nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(4)]
        for node in nodes:
            g.add_node(node)

        g.add_edge(DirectedEdge(nodes[0], nodes[1]))
        g.add_edge(DirectedEdge(nodes[1], nodes[2]))
        g.add_edge(DirectedEdge(nodes[0], nodes[2]))

        for node in nodes:
            assert g.degree(node) == g.in_degree(node) + g.out_degree(node)

    def test_isolated_node_all_degrees_zero(self) -> None:
        """Test isolated node has all degrees = 0."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(DirectedEdge(n1, n2))

        # Add isolated node
        isolated = GraphNode("Isolated", "isolated")
        g.add_node(isolated)

        assert g.degree(isolated) == 0
        assert g.in_degree(isolated) == 0
        assert g.out_degree(isolated) == 0


class TestDirectedGraphAdjacencyUpdates:
    """Test that adjacency lists are properly maintained."""

    def test_adjacency_updated_on_edge_add(self) -> None:
        """Test adjacency lists updated when edge added."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        # Check empty adjacency
        assert len(list(g.successors(n1))) == 0
        assert len(list(g.predecessors(n2))) == 0

        # Add edge
        g.add_edge(DirectedEdge(n1, n2))

        # Check updated adjacency
        assert len(list(g.successors(n1))) == 1
        assert len(list(g.predecessors(n2))) == 1

    def test_adjacency_updated_on_edge_remove(self) -> None:
        """Test adjacency lists updated when edge removed."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)
        e = DirectedEdge(n1, n2)
        g.add_edge(e)

        # Remove edge
        g.remove_edge(e)

        # Check adjacency cleared
        assert len(list(g.successors(n1))) == 0
        assert len(list(g.predecessors(n2))) == 0

    def test_adjacency_updated_on_node_remove(self) -> None:
        """Test adjacency lists updated when node removed."""
        g = DirectedGraph()
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        n3 = GraphNode("C", "n3")
        g.add_node(n1)
        g.add_node(n2)
        g.add_node(n3)
        g.add_edge(DirectedEdge(n1, n2))
        g.add_edge(DirectedEdge(n2, n3))

        # Remove middle node
        g.remove_node(n2)

        # Check n1 and n3 have no connections
        assert len(list(g.successors(n1))) == 0
        assert len(list(g.predecessors(n3))) == 0

    def test_adjacency_preserved_in_multidigraph(self) -> None:
        """Test adjacency preserved with multiple edges."""
        g = DirectedGraph(allow_multi_edges=True)
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        g.add_node(n1)
        g.add_node(n2)

        e1 = DirectedEdge(n1, n2)
        e2 = DirectedEdge(n1, n2)
        g.add_edge(e1)
        g.add_edge(e2)

        # Remove one edge - adjacency should remain
        g.remove_edge(e1)
        assert g.has_edge(n1, n2)
        assert len(list(g.successors(n1))) == 1
