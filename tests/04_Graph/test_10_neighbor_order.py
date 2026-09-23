# Copyright 2024-2026, skyfrigate, biface
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

"""Tests for deterministic neighbor ordering across graph classes (#91).

Every adjacency-holding graph yields neighbors (successors, predecessors)
in the order their first connecting edge was added, independently of
``PYTHONHASHSEED``. Node ids are deliberately chosen so that insertion
order differs from lexicographic order: a test passing by accident on
sorted output would not prove anything.
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Callable, List, Union

import pytest

from sds.graph import (
    AdjacencyListGraph,
    DirectedEdge,
    DirectedGraph,
    Edge,
    Graph,
    GraphNode,
    UndirectedGraph,
    WeightedDirectedEdge,
    WeightedDirectedGraph,
    WeightedEdge,
    WeightedGraph,
)
from sds.graph._incidence import IncidenceIndex

UndirectedAny = Union[Graph, AdjacencyListGraph, WeightedGraph]
DirectedAny = Union[DirectedGraph, WeightedDirectedGraph]

# Graph factories, paired with the edge type each one accepts.
UNDIRECTED = [
    pytest.param(Graph, Edge, id="Graph"),
    pytest.param(UndirectedGraph, Edge, id="UndirectedGraph"),
    pytest.param(AdjacencyListGraph, Edge, id="AdjacencyListGraph"),
    pytest.param(WeightedGraph, WeightedEdge, id="WeightedGraph"),
]
DIRECTED = [
    pytest.param(DirectedGraph, DirectedEdge, id="DirectedGraph"),
    pytest.param(
        WeightedDirectedGraph, WeightedDirectedEdge, id="WeightedDirectedGraph"
    ),
]


def _nodes(*ids: str) -> List[GraphNode]:
    return [GraphNode(node_id, node_id) for node_id in ids]


def _ids(nodes: object) -> List[str]:
    return [n.id for n in nodes]  # type: ignore[attr-defined]


# ============================================================================
# IncidenceIndex (internal building block)
# ============================================================================


class TestIncidenceIndex:
    """Unit tests for the shared insertion-ordered index."""

    def test_neighbors_follow_link_order(self) -> None:
        """Neighbor ids are yielded in first-link order."""
        a, d, b, c = _nodes("a", "d", "b", "c")
        index: IncidenceIndex[Edge] = IncidenceIndex()
        for n in (a, b, c, d):
            index.add_node(n.id)
        for other in (d, b, c):
            index.link_undirected(Edge(a, other))
        assert list(index.neighbor_ids("a")) == ["d", "b", "c"]

    def test_unlink_is_by_identity(self) -> None:
        """Unlinking removes the given parallel edge, not an equal one."""
        a, b = _nodes("a", "b")
        first, second = Edge(a, b, data=1), Edge(a, b, data=2)
        assert first == second  # same endpoints
        index: IncidenceIndex[Edge] = IncidenceIndex()
        index.add_node("a")
        index.add_node("b")
        index.link_undirected(first)
        index.link_undirected(second)
        index.unlink_undirected(second)
        assert [e.data for e in index.edges_of("a")] == [1]
        assert [e.data for e in index.edges_of("b")] == [1]

    def test_neighbor_leaves_row_with_last_edge(self) -> None:
        """A neighbor disappears only once its last edge is unlinked."""
        a, b = _nodes("a", "b")
        first, second = Edge(a, b), Edge(a, b)
        index: IncidenceIndex[Edge] = IncidenceIndex()
        index.add_node("a")
        index.add_node("b")
        index.link_undirected(first)
        index.link_undirected(second)
        index.unlink_undirected(first)
        assert index.has_link("a", "b")
        index.unlink_undirected(second)
        assert not index.has_link("a", "b")
        assert index.neighbor_count("a") == 0

    def test_parallel_edges_are_grouped(self) -> None:
        """edges_of groups parallel edges under their neighbor."""
        a, b, c = _nodes("a", "b", "c")
        e_ab1, e_ac, e_ab2 = Edge(a, b), Edge(a, c), Edge(a, b)
        index: IncidenceIndex[Edge] = IncidenceIndex()
        for n in ("a", "b", "c"):
            index.add_node(n)
        for e in (e_ab1, e_ac, e_ab2):
            index.link_undirected(e)
        assert [id(e) for e in index.edges_of("a")] == [
            id(e_ab1),
            id(e_ab2),
            id(e_ac),
        ]

    def test_self_loop_linked_once(self) -> None:
        """A self-loop sits once in its own row and unlinks cleanly."""
        (a,) = _nodes("a")
        loop = Edge(a, a, allow_self_loop=True)
        index: IncidenceIndex[Edge] = IncidenceIndex()
        index.add_node("a")
        index.link_undirected(loop)
        assert list(index.edges_of("a")) == [loop]
        index.unlink_undirected(loop)
        assert index.neighbor_count("a") == 0

    def test_drop_node_clears_mirrors(self) -> None:
        """drop_node removes the row and every mirror entry."""
        a, b, c = _nodes("a", "b", "c")
        index: IncidenceIndex[Edge] = IncidenceIndex()
        for n in ("a", "b", "c"):
            index.add_node(n)
        index.link_undirected(Edge(a, b))
        index.link_undirected(Edge(c, b))
        index.drop_node("b")
        assert index.neighbor_count("a") == 0
        assert index.neighbor_count("c") == 0

    def test_clear(self) -> None:
        """clear empties every row."""
        index: IncidenceIndex[Edge] = IncidenceIndex()
        index.add_node("a")
        index.clear()
        with pytest.raises(KeyError):
            list(index.neighbor_ids("a"))


# ============================================================================
# Undirected graphs
# ============================================================================


@pytest.mark.parametrize(("graph_cls", "edge_cls"), UNDIRECTED)
class TestUndirectedNeighborOrder:
    """Neighbor order on Graph, UndirectedGraph, AdjacencyListGraph,
    WeightedGraph."""

    @staticmethod
    def _star(
        graph_cls: Callable[..., UndirectedAny],
        edge_cls: Callable[..., Edge],
        multi: bool = False,
    ) -> "tuple[UndirectedAny, List[GraphNode]]":
        a, d, b, c = _nodes("a", "d", "b", "c")
        g = graph_cls(allow_multi_edges=multi)
        for n in (a, b, c, d):
            g.add_node(n)
        for other in (d, b, c):
            g.add_edge(edge_cls(a, other))
        return g, [a, d, b, c]

    def test_insertion_order(self, graph_cls, edge_cls) -> None:  # type: ignore
        """neighbors() follows edge insertion order, not id order."""
        g, (a, *_) = self._star(graph_cls, edge_cls)
        assert _ids(g.neighbors(a)) == ["d", "b", "c"]

    def test_mirror_row_order(self, graph_cls, edge_cls) -> None:  # type: ignore
        """The other endpoint records the edge in its own insertion order."""
        g, (a, d, b, c) = self._star(graph_cls, edge_cls)
        g.add_edge(edge_cls(b, d))
        assert _ids(g.neighbors(d)) == ["a", "b"]
        assert _ids(g.neighbors(b)) == ["a", "d"]

    def test_readd_moves_to_end(self, graph_cls, edge_cls) -> None:  # type: ignore
        """Remove then re-add places the neighbor last."""
        g, (a, d, b, c) = self._star(graph_cls, edge_cls)
        g.remove_edge(g.get_edge(a, d))
        g.add_edge(edge_cls(a, d))
        assert _ids(g.neighbors(a)) == ["b", "c", "d"]

    def test_parallel_edge_keeps_position(
        self, graph_cls, edge_cls  # type: ignore
    ) -> None:
        """Removing one of two parallel edges keeps the neighbor in place."""
        g, (a, d, b, c) = self._star(graph_cls, edge_cls, multi=True)
        g.add_edge(edge_cls(a, d))
        g.remove_edge(edge_cls(a, d))
        assert _ids(g.neighbors(a)) == ["d", "b", "c"]
        assert g.has_edge(a, d)
        g.remove_edge(edge_cls(a, d))
        assert _ids(g.neighbors(a)) == ["b", "c"]
        assert not g.has_edge(a, d)

    def test_remove_node_preserves_rest(
        self, graph_cls, edge_cls  # type: ignore
    ) -> None:
        """Removing a neighbor leaves the others in their original order."""
        g, (a, d, b, c) = self._star(graph_cls, edge_cls)
        g.remove_node(b)
        assert _ids(g.neighbors(a)) == ["d", "c"]
        assert g.degree(a) == 2

    def test_clear_then_rebuild(self, graph_cls, edge_cls) -> None:  # type: ignore
        """clear() resets the index; a rebuilt graph orders afresh."""
        g, (a, d, b, c) = self._star(graph_cls, edge_cls)
        g.clear()
        for n in (a, b, c):
            g.add_node(n)
        g.add_edge(edge_cls(a, c))
        g.add_edge(edge_cls(a, b))
        assert _ids(g.neighbors(a)) == ["c", "b"]


@pytest.mark.parametrize(
    "graph_cls", [Graph, UndirectedGraph, AdjacencyListGraph], ids=lambda c: c.__name__
)
class TestUndirectedSelfLoopOrder:
    """Self-loops (plain Edge only) in the undirected index."""

    def test_self_loop_listed_once(self, graph_cls) -> None:  # type: ignore
        """A self-loop appears once among the neighbors, in its position."""
        a, b = _nodes("a", "b")
        g = graph_cls()
        g.add_node(a)
        g.add_node(b)
        g.add_edge(Edge(a, a, allow_self_loop=True))
        g.add_edge(Edge(a, b))
        assert _ids(g.neighbors(a)) == ["a", "b"]
        g.remove_edge(Edge(a, a, allow_self_loop=True))
        assert _ids(g.neighbors(a)) == ["b"]

    def test_remove_node_with_self_loop(self, graph_cls) -> None:  # type: ignore
        """remove_node handles a node carrying a self-loop."""
        a, b = _nodes("a", "b")
        g = graph_cls()
        g.add_node(a)
        g.add_node(b)
        g.add_edge(Edge(a, a, allow_self_loop=True))
        g.add_edge(Edge(a, b))
        g.remove_node(a)
        assert list(g.neighbors(b)) == []


# ============================================================================
# Directed graphs
# ============================================================================


@pytest.mark.parametrize(("graph_cls", "edge_cls"), DIRECTED)
class TestDirectedNeighborOrder:
    """Successor/predecessor order on DirectedGraph, WeightedDirectedGraph."""

    @staticmethod
    def _build(
        graph_cls: Callable[..., DirectedAny],
        edge_cls: Callable[..., DirectedEdge],
        multi: bool = False,
    ) -> "tuple[DirectedAny, List[GraphNode]]":
        a, d, b, c = _nodes("a", "d", "b", "c")
        g = graph_cls(allow_multi_edges=multi)
        for n in (a, b, c, d):
            g.add_node(n)
        for other in (d, b, c):
            g.add_edge(edge_cls(a, other))
        for other in (c, b):
            g.add_edge(edge_cls(other, d))
        return g, [a, d, b, c]

    def test_successor_order(self, graph_cls, edge_cls) -> None:  # type: ignore
        """successors() and neighbors() follow insertion order."""
        g, (a, *_) = self._build(graph_cls, edge_cls)
        assert _ids(g.successors(a)) == ["d", "b", "c"]
        assert _ids(g.neighbors(a)) == ["d", "b", "c"]

    def test_predecessor_order(self, graph_cls, edge_cls) -> None:  # type: ignore
        """predecessors() follows incoming-edge insertion order."""
        g, (a, d, b, c) = self._build(graph_cls, edge_cls)
        assert _ids(g.predecessors(d)) == ["a", "c", "b"]

    def test_readd_moves_to_end(self, graph_cls, edge_cls) -> None:  # type: ignore
        """Remove then re-add moves the node last on both sides."""
        g, (a, d, b, c) = self._build(graph_cls, edge_cls)
        g.remove_edge(g.get_edge(a, d))
        g.add_edge(edge_cls(a, d))
        assert _ids(g.successors(a)) == ["b", "c", "d"]
        assert _ids(g.predecessors(d)) == ["c", "b", "a"]

    def test_parallel_edge_keeps_position(
        self, graph_cls, edge_cls  # type: ignore
    ) -> None:
        """Removing one of two parallel arcs keeps the successor in place."""
        g, (a, d, b, c) = self._build(graph_cls, edge_cls, multi=True)
        g.add_edge(edge_cls(a, d))
        g.remove_edge(edge_cls(a, d))
        assert _ids(g.successors(a)) == ["d", "b", "c"]
        assert _ids(g.predecessors(d)) == ["a", "c", "b"]
        g.remove_edge(edge_cls(a, d))
        assert _ids(g.successors(a)) == ["b", "c"]
        assert _ids(g.predecessors(d)) == ["c", "b"]

    def test_remove_node_preserves_rest(
        self, graph_cls, edge_cls  # type: ignore
    ) -> None:
        """Removing a node keeps the remaining order on both indexes."""
        g, (a, d, b, c) = self._build(graph_cls, edge_cls)
        g.remove_node(c)
        assert _ids(g.successors(a)) == ["d", "b"]
        assert _ids(g.predecessors(d)) == ["a", "b"]
        assert g.in_degree(d) == 2
        assert g.out_degree(a) == 2

    def test_opposite_arcs_are_distinct(
        self, graph_cls, edge_cls  # type: ignore
    ) -> None:
        """a->b and b->a live in separate rows and unlink independently."""
        g, (a, d, b, c) = self._build(graph_cls, edge_cls)
        g.add_edge(edge_cls(b, a))
        g.remove_edge(g.get_edge(a, b))
        assert _ids(g.successors(b)) == ["d", "a"]
        assert _ids(g.predecessors(a)) == ["b"]
        assert "b" not in _ids(g.successors(a))


class TestDirectedGraphUndirectedEdgeRemoval:
    """DirectedGraph.remove_edge also accepts a plain Edge, read node1->node2."""

    def test_plain_edge_removes_matching_arc(self) -> None:
        """A plain Edge(a, b) removes the arc a->b only."""
        a, b = _nodes("a", "b")
        g = DirectedGraph()
        g.add_node(a)
        g.add_node(b)
        g.add_edge(DirectedEdge(a, b))
        g.add_edge(DirectedEdge(b, a))
        g.remove_edge(Edge(a, b))
        assert not g.has_edge(a, b)
        assert g.has_edge(b, a)
        assert _ids(g.predecessors(a)) == ["b"]

    def test_plain_edge_without_matching_arc(self) -> None:
        """A plain Edge with no matching arc raises ValueError."""
        a, b = _nodes("a", "b")
        g = DirectedGraph()
        g.add_node(a)
        g.add_node(b)
        g.add_edge(DirectedEdge(b, a))
        with pytest.raises(ValueError):
            g.remove_edge(Edge(a, b))


# ============================================================================
# Hash-seed independence
# ============================================================================

_SCRIPT = """
from sds.graph import DirectedEdge, DirectedGraph, Edge, Graph, GraphNode
nodes = [GraphNode(i, i) for i in ("hub", "zeta", "alpha", "mu", "beta", "omega")]
g, dg = Graph(), DirectedGraph()
for n in nodes:
    g.add_node(n)
    dg.add_node(n)
for n in nodes[1:]:
    g.add_edge(Edge(nodes[0], n))
    dg.add_edge(DirectedEdge(nodes[0], n))
print([n.id for n in g.neighbors(nodes[0])], [n.id for n in dg.successors(nodes[0])])
"""


class TestHashSeedIndependence:
    """Order does not depend on PYTHONHASHSEED (the defect #91 fixes)."""

    def test_same_order_across_seeds(self) -> None:
        """Three hash seeds produce one and the same neighbor order."""
        src = Path(__file__).resolve().parents[2] / "src"
        outputs = set()
        for seed in ("0", "1", "12345"):
            env = {**os.environ, "PYTHONHASHSEED": seed, "PYTHONPATH": str(src)}
            result = subprocess.run(
                [sys.executable, "-c", _SCRIPT],
                env=env,
                capture_output=True,
                text=True,
                check=True,
            )
            outputs.add(result.stdout)
        assert len(outputs) == 1
