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

"""Unit tests for graph interface classes."""

from typing import Iterator, List, Optional

import pytest

from sds.core.interfaces import Collection
from sds.graph.edge import DirectedEdge, Edge, WeightedDirectedEdge, WeightedEdge
from sds.graph.interfaces import (
    AbstractDirectedGraph,
    AbstractGraph,
    AbstractUndirectedGraph,
    AbstractWeightedGraph,
)
from sds.graph.node import GraphNode


class TestAbstractGraphInterface:
    """Test AbstractGraph interface."""

    def test_is_abstract(self) -> None:
        """Test that AbstractGraph cannot be instantiated."""
        with pytest.raises(TypeError, match="abstract"):
            AbstractGraph()  # type: ignore[abstract]

    def test_inherits_from_collection(self) -> None:
        """Test that AbstractGraph inherits from Collection."""
        assert issubclass(AbstractGraph, Collection)

    def test_has_required_abstract_methods(self) -> None:
        """Test that AbstractGraph defines required abstract methods."""
        required_methods = {
            "add_node",
            "remove_node",
            "has_node",
            "add_edge",
            "remove_edge",
            "has_edge",
            "get_edge",
            "neighbors",
            "degree",
            "nodes",
            "edges",
            "node_count",
            "edge_count",
            "is_connected",
            "get_node_by_id",
        }
        abstract_methods = {
            name
            for name in dir(AbstractGraph)
            if getattr(
                getattr(AbstractGraph, name, None), "__isabstractmethod__", False
            )
        }
        # Check that all required methods are abstract
        for method in required_methods:
            assert method in abstract_methods, f"{method} should be abstract"


class TestConcreteGraphImplementation:
    """Test concrete implementation of AbstractGraph."""

    def test_minimal_implementation(self) -> None:
        """Test minimal concrete implementation of AbstractGraph."""

        class MinimalGraph(AbstractGraph):
            """Minimal concrete graph for testing."""

            def __init__(self) -> None:
                super().__init__()
                self._nodes: dict[str, GraphNode] = {}
                self._edges: List[Edge] = []

            def add_node(self, node: GraphNode) -> None:
                self._nodes[node.id] = node

            def remove_node(self, node: GraphNode) -> None:
                del self._nodes[node.id]

            def has_node(self, node: GraphNode) -> bool:
                return node.id in self._nodes

            def add_edge(self, edge: Edge) -> None:
                self._edges.append(edge)

            def remove_edge(self, edge: Edge) -> None:
                self._edges.remove(edge)

            def has_edge(self, node1: GraphNode, node2: GraphNode) -> bool:
                return any(e.connects(node1, node2) for e in self._edges)

            def get_edge(self, node1: GraphNode, node2: GraphNode) -> Optional[Edge]:
                for e in self._edges:
                    if e.connects(node1, node2):
                        return e
                return None

            def neighbors(self, node: GraphNode) -> Iterator[GraphNode]:
                for e in self._edges:
                    if e.incident_to(node):
                        yield e.other_node(node)

            def degree(self, node: GraphNode) -> int:
                return sum(1 for e in self._edges if e.incident_to(node))

            def nodes(self) -> Iterator[GraphNode]:
                yield from self._nodes.values()

            def edges(self) -> Iterator[Edge]:
                yield from self._edges

            def node_count(self) -> int:
                return len(self._nodes)

            def edge_count(self) -> int:
                return len(self._edges)

            def is_connected(self) -> bool:
                return True  # Simplified

            def get_node_by_id(self, node_id: str) -> Optional[GraphNode]:
                return self._nodes.get(node_id)

            def is_empty(self) -> bool:
                return len(self._nodes) == 0

            def __len__(self) -> int:
                return len(self._nodes)

            def __contains__(self, item: object) -> bool:
                if isinstance(item, GraphNode):
                    return self.has_node(item)
                return False

            def __iter__(self) -> Iterator[GraphNode]:
                return self.nodes()

            def clear(self) -> None:
                self._nodes.clear()
                self._edges.clear()

        # Should be able to instantiate
        graph = MinimalGraph()
        assert isinstance(graph, AbstractGraph)
        assert isinstance(graph, Collection)

        # Test basic operations
        n1 = GraphNode("A", "n1")
        graph.add_node(n1)
        assert graph.has_node(n1)
        assert graph.node_count() == 1


class TestAbstractDirectedGraphInterface:
    """Test AbstractDirectedGraph interface."""

    def test_is_abstract(self) -> None:
        """Test that AbstractDirectedGraph cannot be instantiated."""
        with pytest.raises(TypeError, match="abstract"):
            AbstractDirectedGraph()  # type: ignore[abstract]

    def test_inherits_from_abstract_graph(self) -> None:
        """Test that AbstractDirectedGraph inherits from AbstractGraph."""
        assert issubclass(AbstractDirectedGraph, AbstractGraph)

    def test_has_directed_specific_methods(self) -> None:
        """Test that AbstractDirectedGraph defines directed-specific methods."""
        directed_methods = {
            "in_degree",
            "out_degree",
            "predecessors",
            "successors",
            "is_acyclic",
        }
        abstract_methods = {
            name
            for name in dir(AbstractDirectedGraph)
            if getattr(
                getattr(AbstractDirectedGraph, name, None),
                "__isabstractmethod__",
                False,
            )
        }
        for method in directed_methods:
            assert (
                method in abstract_methods
            ), f"{method} should be abstract in AbstractDirectedGraph"


class TestConcreteDirectedGraphImplementation:
    """Test concrete implementation of AbstractDirectedGraph."""

    def test_minimal_directed_implementation(self) -> None:
        """Test minimal concrete implementation of AbstractDirectedGraph."""

        class MinimalDirectedGraph(AbstractDirectedGraph):
            """Minimal concrete directed graph for testing."""

            def __init__(self) -> None:
                super().__init__()
                self._nodes: dict[str, GraphNode] = {}
                self._edges: List[DirectedEdge] = []

            def add_node(self, node: GraphNode) -> None:
                self._nodes[node.id] = node

            def remove_node(self, node: GraphNode) -> None:
                del self._nodes[node.id]

            def has_node(self, node: GraphNode) -> bool:
                return node.id in self._nodes

            def add_edge(self, edge: DirectedEdge) -> None:  # type: ignore[override]
                self._edges.append(edge)

            def remove_edge(self, edge: Edge) -> None:
                if isinstance(edge, DirectedEdge):
                    self._edges.remove(edge)

            def has_edge(self, node1: GraphNode, node2: GraphNode) -> bool:
                return any(e.connects(node1, node2) for e in self._edges)

            def get_edge(self, node1: GraphNode, node2: GraphNode) -> Optional[Edge]:
                for e in self._edges:
                    if e.connects(node1, node2):
                        return e
                return None

            def neighbors(self, node: GraphNode) -> Iterator[GraphNode]:
                yield from self.successors(node)

            def degree(self, node: GraphNode) -> int:
                return self.in_degree(node) + self.out_degree(node)

            def in_degree(self, node: GraphNode) -> int:
                return sum(1 for e in self._edges if e.target.id == node.id)

            def out_degree(self, node: GraphNode) -> int:
                return sum(1 for e in self._edges if e.source.id == node.id)

            def predecessors(self, node: GraphNode) -> Iterator[GraphNode]:
                for e in self._edges:
                    if e.target.id == node.id:
                        yield e.source

            def successors(self, node: GraphNode) -> Iterator[GraphNode]:
                for e in self._edges:
                    if e.source.id == node.id:
                        yield e.target

            def is_acyclic(self) -> bool:
                return True  # Simplified

            def nodes(self) -> Iterator[GraphNode]:
                yield from self._nodes.values()

            def edges(self) -> Iterator[Edge]:
                yield from self._edges

            def node_count(self) -> int:
                return len(self._nodes)

            def edge_count(self) -> int:
                return len(self._edges)

            def is_connected(self) -> bool:
                return True  # Simplified

            def get_node_by_id(self, node_id: str) -> Optional[GraphNode]:
                return self._nodes.get(node_id)

            def is_empty(self) -> bool:
                return len(self._nodes) == 0

            def __len__(self) -> int:
                return len(self._nodes)

            def __contains__(self, item: object) -> bool:
                if isinstance(item, GraphNode):
                    return self.has_node(item)
                return False

            def __iter__(self) -> Iterator[GraphNode]:
                return self.nodes()

            def clear(self) -> None:
                self._nodes.clear()
                self._edges.clear()

        # Should be able to instantiate
        graph = MinimalDirectedGraph()
        assert isinstance(graph, AbstractDirectedGraph)
        assert isinstance(graph, AbstractGraph)

        # Test directed operations
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        graph.add_node(n1)
        graph.add_node(n2)

        edge = DirectedEdge(n1, n2)
        graph.add_edge(edge)

        assert graph.out_degree(n1) == 1
        assert graph.in_degree(n1) == 0
        assert graph.out_degree(n2) == 0
        assert graph.in_degree(n2) == 1


class TestAbstractUndirectedGraphInterface:
    """Test AbstractUndirectedGraph interface."""

    def test_is_abstract(self) -> None:
        """Test that AbstractUndirectedGraph cannot be instantiated."""
        with pytest.raises(TypeError, match="abstract"):
            AbstractUndirectedGraph()  # type: ignore[abstract]

    def test_inherits_from_abstract_graph(self) -> None:
        """Test that AbstractUndirectedGraph inherits from AbstractGraph."""
        assert issubclass(AbstractUndirectedGraph, AbstractGraph)

    def test_no_additional_abstract_methods(self) -> None:
        """Test that AbstractUndirectedGraph doesn't add new abstract methods."""
        # It should have the same abstract methods as AbstractGraph
        graph_methods = {
            name
            for name in dir(AbstractGraph)
            if getattr(
                getattr(AbstractGraph, name, None), "__isabstractmethod__", False
            )
        }
        undirected_methods = {
            name
            for name in dir(AbstractUndirectedGraph)
            if getattr(
                getattr(AbstractUndirectedGraph, name, None),
                "__isabstractmethod__",
                False,
            )
        }
        # AbstractUndirectedGraph should not add new abstract methods
        assert undirected_methods == graph_methods


class TestAbstractWeightedGraphInterface:
    """Test AbstractWeightedGraph interface."""

    def test_is_abstract(self) -> None:
        """Test that AbstractWeightedGraph cannot be instantiated."""
        with pytest.raises(TypeError, match="abstract"):
            AbstractWeightedGraph()  # type: ignore[abstract]

    def test_inherits_from_abstract_graph(self) -> None:
        """Test that AbstractWeightedGraph inherits from AbstractGraph."""
        assert issubclass(AbstractWeightedGraph, AbstractGraph)

    def test_has_weighted_specific_methods(self) -> None:
        """Test that AbstractWeightedGraph defines weighted-specific methods."""
        weighted_methods = {"get_edge_weight", "total_weight", "incident_edges"}
        abstract_methods = {
            name
            for name in dir(AbstractWeightedGraph)
            if getattr(
                getattr(AbstractWeightedGraph, name, None),
                "__isabstractmethod__",
                False,
            )
        }
        for method in weighted_methods:
            assert (
                method in abstract_methods
            ), f"{method} should be abstract in AbstractWeightedGraph"


class TestConcreteWeightedGraphImplementation:
    """Test concrete implementation of AbstractWeightedGraph."""

    def test_minimal_weighted_implementation(self) -> None:
        """Test minimal concrete implementation of AbstractWeightedGraph."""

        class MinimalWeightedGraph(AbstractWeightedGraph):
            """Minimal concrete weighted graph for testing."""

            def __init__(self) -> None:
                super().__init__()
                self._nodes: dict[str, GraphNode] = {}
                self._edges: List[WeightedEdge | WeightedDirectedEdge] = []

            def add_node(self, node: GraphNode) -> None:
                self._nodes[node.id] = node

            def remove_node(self, node: GraphNode) -> None:
                del self._nodes[node.id]

            def has_node(self, node: GraphNode) -> bool:
                return node.id in self._nodes

            def add_edge(  # type: ignore[override]
                self, edge: WeightedEdge | WeightedDirectedEdge
            ) -> None:
                self._edges.append(edge)

            def remove_edge(self, edge: Edge) -> None:
                if isinstance(edge, (WeightedEdge, WeightedDirectedEdge)):
                    self._edges.remove(edge)

            def has_edge(self, node1: GraphNode, node2: GraphNode) -> bool:
                return any(e.connects(node1, node2) for e in self._edges)

            def get_edge(self, node1: GraphNode, node2: GraphNode) -> Optional[Edge]:
                for e in self._edges:
                    if e.connects(node1, node2):
                        return e
                return None

            def get_edge_weight(
                self, node1: GraphNode, node2: GraphNode
            ) -> Optional[float]:
                edge = self.get_edge(node1, node2)
                if edge and isinstance(edge, (WeightedEdge, WeightedDirectedEdge)):
                    return edge.weight
                return None

            def total_weight(self) -> float:
                return sum(e.weight for e in self._edges)

            def incident_edges(
                self, node: GraphNode
            ) -> List[WeightedEdge | WeightedDirectedEdge]:
                return [e for e in self._edges if e.incident_to(node)]

            def neighbors(self, node: GraphNode) -> Iterator[GraphNode]:
                for e in self._edges:
                    if e.incident_to(node):
                        yield e.other_node(node)

            def degree(self, node: GraphNode) -> int:
                return sum(1 for e in self._edges if e.incident_to(node))

            def nodes(self) -> Iterator[GraphNode]:
                yield from self._nodes.values()

            def edges(self) -> Iterator[Edge]:
                yield from self._edges

            def node_count(self) -> int:
                return len(self._nodes)

            def edge_count(self) -> int:
                return len(self._edges)

            def is_connected(self) -> bool:
                return True  # Simplified

            def get_node_by_id(self, node_id: str) -> Optional[GraphNode]:
                return self._nodes.get(node_id)

            def is_empty(self) -> bool:
                return len(self._nodes) == 0

            def __len__(self) -> int:
                return len(self._nodes)

            def __contains__(self, item: object) -> bool:
                if isinstance(item, GraphNode):
                    return self.has_node(item)
                return False

            def __iter__(self) -> Iterator[GraphNode]:
                return self.nodes()

            def clear(self) -> None:
                self._nodes.clear()
                self._edges.clear()

        # Should be able to instantiate
        graph = MinimalWeightedGraph()
        assert isinstance(graph, AbstractWeightedGraph)
        assert isinstance(graph, AbstractGraph)

        # Test weighted operations
        n1 = GraphNode("A", "n1")
        n2 = GraphNode("B", "n2")
        graph.add_node(n1)
        graph.add_node(n2)

        edge = WeightedEdge(n1, n2, weight=5.0)
        graph.add_edge(edge)

        assert graph.get_edge_weight(n1, n2) == 5.0
        assert graph.total_weight() == 5.0
        assert len(graph.incident_edges(n1)) == 1


class TestInterfaceHierarchy:
    """Test the interface hierarchy and relationships."""

    def test_directed_is_graph(self) -> None:
        """Test that directed graphs are graphs."""
        assert issubclass(AbstractDirectedGraph, AbstractGraph)

    def test_undirected_is_graph(self) -> None:
        """Test that undirected graphs are graphs."""
        assert issubclass(AbstractUndirectedGraph, AbstractGraph)

    def test_weighted_is_graph(self) -> None:
        """Test that weighted graphs are graphs."""
        assert issubclass(AbstractWeightedGraph, AbstractGraph)

    def test_all_are_collections(self) -> None:
        """Test that all graph types are collections."""
        assert issubclass(AbstractGraph, Collection)
        assert issubclass(AbstractDirectedGraph, Collection)
        assert issubclass(AbstractUndirectedGraph, Collection)
        assert issubclass(AbstractWeightedGraph, Collection)

    def test_interfaces_are_independent(self) -> None:
        """Test that directed, undirected, weighted are independent."""
        # Directed and undirected should not inherit from each other
        assert not issubclass(AbstractDirectedGraph, AbstractUndirectedGraph)
        assert not issubclass(AbstractUndirectedGraph, AbstractDirectedGraph)

        # Weighted should be independent from directed/undirected
        assert not issubclass(AbstractWeightedGraph, AbstractDirectedGraph)
        assert not issubclass(AbstractWeightedGraph, AbstractUndirectedGraph)
