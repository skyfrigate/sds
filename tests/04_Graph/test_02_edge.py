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

"""Unit tests for Edge classes."""

import pytest

from sds.graph.edge import DirectedEdge, Edge, WeightedDirectedEdge, WeightedEdge
from sds.graph.node import GraphNode


class TestEdgeCreation:
    """Test Edge initialization and basic properties."""

    def test_create_edge(self) -> None:
        """Test creating a simple edge."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge = Edge(n1, n2)
        assert edge.node1.id == "n1"
        assert edge.node2.id == "n2"
        assert edge.data is None

    def test_create_edge_with_data(self) -> None:
        """Test creating edge with additional data."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge = Edge(n1, n2, data={"type": "friend"})
        assert edge.data == {"type": "friend"}

    def test_create_edge_requires_graphnodes(self) -> None:
        """Test that edge requires GraphNode instances."""
        n1 = GraphNode("A", "n1")
        with pytest.raises(TypeError, match="must be GraphNode"):
            Edge(n1, "not a node")  # type: ignore[arg-type]

        with pytest.raises(TypeError, match="must be GraphNode"):
            Edge("not a node", n1)  # type: ignore[arg-type]

    def test_self_loop_not_allowed(self) -> None:
        """Test that self-loops are not allowed."""
        n1 = GraphNode("A", "n1")
        with pytest.raises(ValueError, match="Self-loops not allowed"):
            Edge(n1, n1)


class TestEdgeProperties:
    """Test Edge properties and methods."""

    def test_node_properties(self) -> None:
        """Test accessing node properties."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge = Edge(n1, n2)
        assert edge.node1 is n1
        assert edge.node2 is n2

    def test_nodes_are_read_only(self) -> None:
        """Test that nodes cannot be modified."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge = Edge(n1, n2)
        with pytest.raises(AttributeError):
            edge.node1 = n2  # type: ignore[misc]

    def test_data_is_read_only(self) -> None:
        """Test that data cannot be modified."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge = Edge(n1, n2, data="test")
        with pytest.raises(AttributeError):
            edge.data = "new"  # type: ignore[misc]


class TestEdgeConnectsMethod:
    """Test Edge.connects() method."""

    def test_connects_in_order(self) -> None:
        """Test connects() with nodes in same order."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge = Edge(n1, n2)
        assert edge.connects(n1, n2) is True

    def test_connects_reverse_order(self) -> None:
        """Test connects() with nodes in reverse order (undirected)."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge = Edge(n1, n2)
        assert edge.connects(n2, n1) is True

    def test_connects_wrong_nodes(self) -> None:
        """Test connects() with wrong nodes."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        n3 = GraphNode("C", "n3")
        edge = Edge(n1, n2)
        assert edge.connects(n1, n3) is False
        assert edge.connects(n3, n2) is False


class TestEdgeIncidentTo:
    """Test Edge.incident_to() method."""

    def test_incident_to_node1(self) -> None:
        """Test edge is incident to node1."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge = Edge(n1, n2)
        assert edge.incident_to(n1) is True

    def test_incident_to_node2(self) -> None:
        """Test edge is incident to node2."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge = Edge(n1, n2)
        assert edge.incident_to(n2) is True

    def test_not_incident_to_other_node(self) -> None:
        """Test edge is not incident to unrelated node."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        n3 = GraphNode("C", "n3")
        edge = Edge(n1, n2)
        assert edge.incident_to(n3) is False


class TestEdgeOtherNode:
    """Test Edge.other_node() method."""

    def test_other_node_from_node1(self) -> None:
        """Test getting other node from node1."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge = Edge(n1, n2)
        assert edge.other_node(n1) is n2

    def test_other_node_from_node2(self) -> None:
        """Test getting other node from node2."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge = Edge(n1, n2)
        assert edge.other_node(n2) is n1

    def test_other_node_with_invalid_node(self) -> None:
        """Test other_node() with node not in edge."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        n3 = GraphNode("C", "n3")
        edge = Edge(n1, n2)
        with pytest.raises(ValueError, match="not part of this edge"):
            edge.other_node(n3)


class TestEdgeEquality:
    """Test Edge equality and hashing."""

    def test_equality_same_order(self) -> None:
        """Test edges are equal with same nodes in same order."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge1 = Edge(n1, n2)
        edge2 = Edge(n1, n2)
        assert edge1 == edge2

    def test_equality_reverse_order(self) -> None:
        """Test edges are equal with same nodes in reverse order."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge1 = Edge(n1, n2)
        edge2 = Edge(n2, n1)
        assert edge1 == edge2

    def test_inequality_different_nodes(self) -> None:
        """Test edges are not equal with different nodes."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        n3 = GraphNode("C", "n3")
        edge1 = Edge(n1, n2)
        edge2 = Edge(n1, n3)
        assert edge1 != edge2

    def test_equality_with_non_edge(self) -> None:
        """Test equality with non-Edge objects."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge = Edge(n1, n2)
        assert edge != "edge"
        assert edge != 42
        assert edge is not None

    def test_hash_same_for_equal_edges(self) -> None:
        """Test hash is same for equal edges."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge1 = Edge(n1, n2)
        edge2 = Edge(n2, n1)
        assert hash(edge1) == hash(edge2)

    def test_can_be_used_in_set(self) -> None:
        """Test edges can be used in sets."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge1 = Edge(n1, n2)
        edge2 = Edge(n2, n1)  # Same edge, reverse order
        edge_set = {edge1, edge2}
        assert len(edge_set) == 1


class TestEdgeStringRepresentations:
    """Test Edge string representations."""

    def test_repr(self) -> None:
        """Test __repr__ format."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge = Edge(n1, n2)
        assert repr(edge) == "Edge(n1 -- n2)"

    def test_str(self) -> None:
        """Test __str__ format."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge = Edge(n1, n2)
        assert str(edge) == "n1 -- n2"


class TestDirectedEdge:
    """Test DirectedEdge class."""

    def test_create_directed_edge(self) -> None:
        """Test creating a directed edge."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge = DirectedEdge(n1, n2)
        assert edge.source is n1
        assert edge.target is n2

    def test_source_target_aliases(self) -> None:
        """Test source/target are aliases for node1/node2."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge = DirectedEdge(n1, n2)
        assert edge.source is edge.node1
        assert edge.target is edge.node2

    def test_connects_respects_direction(self) -> None:
        """Test connects() respects direction."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge = DirectedEdge(n1, n2)
        assert edge.connects(n1, n2) is True
        assert edge.connects(n2, n1) is False

    def test_equality_respects_direction(self) -> None:
        """Test equality respects direction."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge1 = DirectedEdge(n1, n2)
        edge2 = DirectedEdge(n2, n1)
        assert edge1 != edge2

    def test_hash_respects_direction(self) -> None:
        """Test hash respects direction."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge1 = DirectedEdge(n1, n2)
        edge2 = DirectedEdge(n2, n1)
        assert hash(edge1) != hash(edge2)

    def test_repr_shows_direction(self) -> None:
        """Test __repr__ shows arrow for direction."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge = DirectedEdge(n1, n2)
        assert repr(edge) == "DirectedEdge(n1 -> n2)"

    def test_str_shows_direction(self) -> None:
        """Test __str__ shows arrow for direction."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge = DirectedEdge(n1, n2)
        assert str(edge) == "n1 -> n2"


class TestWeightedEdge:
    """Test WeightedEdge class."""

    def test_create_weighted_edge(self) -> None:
        """Test creating a weighted edge."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge = WeightedEdge(n1, n2, weight=5.0)
        assert edge.weight == 5.0

    def test_default_weight(self) -> None:
        """Test default weight is 1.0."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge = WeightedEdge(n1, n2)
        assert edge.weight == 1.0

    def test_weight_conversion_to_float(self) -> None:
        """Test weight is converted to float."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge = WeightedEdge(n1, n2, weight=5)
        assert edge.weight == 5.0
        assert isinstance(edge.weight, float)

    def test_weight_is_read_only(self) -> None:
        """Test that weight cannot be modified."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge = WeightedEdge(n1, n2, weight=5.0)
        with pytest.raises(AttributeError):
            edge.weight = 10.0  # type: ignore[misc]

    def test_invalid_weight_raises_error(self) -> None:
        """Test that non-numeric weight raises error."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        with pytest.raises(TypeError, match="Weight must be numeric"):
            WeightedEdge(n1, n2, weight="invalid")  # type: ignore[arg-type]

    def test_negative_weight_allowed(self) -> None:
        """Test that negative weights are allowed."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge = WeightedEdge(n1, n2, weight=-3.5)
        assert edge.weight == -3.5

    def test_repr_shows_weight(self) -> None:
        """Test __repr__ shows weight."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge = WeightedEdge(n1, n2, weight=5.0)
        assert repr(edge) == "WeightedEdge(n1 --5.0-- n2)"

    def test_str_shows_weight(self) -> None:
        """Test __str__ shows weight."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge = WeightedEdge(n1, n2, weight=5.0)
        assert str(edge) == "n1 --5.0-- n2"


class TestWeightedDirectedEdge:
    """Test WeightedDirectedEdge class."""

    def test_create_weighted_directed_edge(self) -> None:
        """Test creating a weighted directed edge."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge = WeightedDirectedEdge(n1, n2, weight=3.5)
        assert edge.source is n1
        assert edge.target is n2
        assert edge.weight == 3.5

    def test_default_weight(self) -> None:
        """Test default weight is 1.0."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge = WeightedDirectedEdge(n1, n2)
        assert edge.weight == 1.0

    def test_combines_directed_and_weighted_behavior(self) -> None:
        """Test that it combines both directed and weighted properties."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge = WeightedDirectedEdge(n1, n2, weight=5.0)

        # Directed behavior
        assert edge.connects(n1, n2) is True
        assert edge.connects(n2, n1) is False

        # Weighted behavior
        assert edge.weight == 5.0

    def test_repr_shows_weight_and_direction(self) -> None:
        """Test __repr__ shows both weight and direction."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge = WeightedDirectedEdge(n1, n2, weight=3.5)
        assert repr(edge) == "WeightedDirectedEdge(n1 -3.5-> n2)"

    def test_str_shows_weight_and_direction(self) -> None:
        """Test __str__ shows both weight and direction."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge = WeightedDirectedEdge(n1, n2, weight=3.5)
        assert str(edge) == "n1 -3.5-> n2"


class TestEdgeMemoryEfficiency:
    """Test memory efficiency using __slots__."""

    def test_edge_has_slots(self) -> None:
        """Test that Edge uses __slots__."""
        assert hasattr(Edge, "__slots__")

    def test_weighted_edge_has_slots(self) -> None:
        """Test that WeightedEdge adds slots."""
        assert hasattr(WeightedEdge, "__slots__")

    def test_cannot_add_arbitrary_attributes_to_edge(self) -> None:
        """Test that arbitrary attributes cannot be added to Edge."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge = Edge(n1, n2)
        with pytest.raises(AttributeError):
            edge.arbitrary = "value"  # type: ignore[attr-defined]

    def test_cannot_add_arbitrary_attributes_to_weighted_edge(self) -> None:
        """Test that arbitrary attributes cannot be added to WeightedEdge."""
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        edge = WeightedEdge(n1, n2)
        with pytest.raises(AttributeError):
            edge.arbitrary = "value"  # type: ignore[attr-defined]
