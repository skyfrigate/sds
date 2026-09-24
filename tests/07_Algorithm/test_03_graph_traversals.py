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

"""Tests for sds.algorithms.graph_algorithms BFS and DFS (#61, #62)."""

import itertools
import random
import sys
from typing import Any, Callable, Dict, Iterator, List, Set, Tuple

import pytest

from sds.algorithms.graph_algorithms import bfs, dfs
from sds.graph import (
    AdjacencyListGraph,
    AdjacencyMatrixGraph,
    DirectedEdge,
    DirectedGraph,
    Edge,
    Graph,
    GraphNode,
    WeightedDirectedEdge,
    WeightedDirectedGraph,
    WeightedEdge,
    WeightedGraph,
)
from sds.graph.interfaces import AbstractGraph

# --------------------------------------------------------------------------
# Builders
# --------------------------------------------------------------------------

UNDIRECTED: List[Any] = [
    pytest.param(Graph, Edge, id="Graph"),
    pytest.param(AdjacencyListGraph, Edge, id="AdjacencyListGraph"),
    pytest.param(AdjacencyMatrixGraph, Edge, id="AdjacencyMatrixGraph"),
    pytest.param(WeightedGraph, WeightedEdge, id="WeightedGraph"),
]
DIRECTED: List[Any] = [
    pytest.param(DirectedGraph, DirectedEdge, id="DirectedGraph"),
    pytest.param(
        WeightedDirectedGraph, WeightedDirectedEdge, id="WeightedDirectedGraph"
    ),
]
TRAVERSALS: List[Any] = [pytest.param(bfs, id="bfs"), pytest.param(dfs, id="dfs")]

Traversal = Callable[[AbstractGraph, GraphNode], Iterator[GraphNode]]


def _build(
    graph_cls: Callable[[], AbstractGraph],
    edge_cls: Callable[..., Edge],
    ids: str,
    pairs: List[Tuple[str, str]],
) -> Tuple[AbstractGraph, Dict[str, GraphNode]]:
    graph = graph_cls()
    nodes = {i: GraphNode(i, i) for i in ids}
    for node in nodes.values():
        graph.add_node(node)
    for u, v in pairs:
        graph.add_edge(edge_cls(nodes[u], nodes[v]))
    return graph, nodes


def _ids(nodes: Iterator[GraphNode]) -> List[str]:
    return [n.id for n in nodes]


# Reference graph, edges inserted in this order:
#
#     a --- b --- d
#     |     |
#     c --- e     f (isolated)
#
REF_PAIRS = [("a", "b"), ("a", "c"), ("b", "d"), ("b", "e"), ("c", "e")]


def _reference_dfs(graph: AbstractGraph, source: GraphNode) -> List[GraphNode]:
    """Textbook recursive DFS, used as the oracle for the iterative one."""
    order: List[GraphNode] = []
    seen: Set[GraphNode] = set()

    def visit(node: GraphNode) -> None:
        seen.add(node)
        order.append(node)
        for nxt in graph.neighbors(node):
            if nxt not in seen:
                visit(nxt)

    visit(source)
    return order


def _hop_distances(graph: AbstractGraph, source: GraphNode) -> Dict[GraphNode, int]:
    """Unweighted distances computed independently (level by level)."""
    dist = {source: 0}
    frontier = [source]
    while frontier:
        nxt = []
        for node in frontier:
            for neighbor in graph.neighbors(node):
                if neighbor not in dist:
                    dist[neighbor] = dist[node] + 1
                    nxt.append(neighbor)
        frontier = nxt
    return dist


# --------------------------------------------------------------------------
# BFS / DFS
# --------------------------------------------------------------------------


@pytest.mark.parametrize(("graph_cls", "edge_cls"), UNDIRECTED)
class TestTraversalOrder:
    """Exact visiting order on the reference graph, every representation."""

    def test_bfs(self, graph_cls: Any, edge_cls: Any) -> None:
        """BFS: by distance, ties in edge insertion order."""
        g, n = _build(graph_cls, edge_cls, "abcdef", REF_PAIRS)
        assert _ids(bfs(g, n["a"])) == ["a", "b", "c", "d", "e"]

    def test_dfs(self, graph_cls: Any, edge_cls: Any) -> None:
        """DFS: deepest first, neighbors in edge insertion order."""
        g, n = _build(graph_cls, edge_cls, "abcdef", REF_PAIRS)
        assert _ids(dfs(g, n["a"])) == ["a", "b", "d", "e", "c"]

    def test_isolated_source(self, graph_cls: Any, edge_cls: Any) -> None:
        """An isolated node reaches only itself."""
        g, n = _build(graph_cls, edge_cls, "abcdef", REF_PAIRS)
        assert _ids(bfs(g, n["f"])) == ["f"]
        assert _ids(dfs(g, n["f"])) == ["f"]


@pytest.mark.parametrize("traversal", TRAVERSALS)
class TestTraversalContract:
    """Properties shared by BFS and DFS."""

    @pytest.mark.parametrize(("graph_cls", "edge_cls"), DIRECTED)
    def test_directed_follows_arcs(
        self, traversal: Traversal, graph_cls: Any, edge_cls: Any
    ) -> None:
        """Arcs are followed from source to target only."""
        g, n = _build(graph_cls, edge_cls, "abc", [("a", "b"), ("c", "b")])
        assert _ids(traversal(g, n["a"])) == ["a", "b"]
        assert _ids(traversal(g, n["b"])) == ["b"]

    def test_cycle_visits_once(self, traversal: Traversal) -> None:
        """A cycle does not make the traversal loop."""
        g, n = _build(
            Graph, Edge, "abcd", [("a", "b"), ("b", "c"), ("c", "d"), ("d", "a")]
        )
        assert sorted(_ids(traversal(g, n["a"]))) == ["a", "b", "c", "d"]

    def test_missing_source(self, traversal: Traversal) -> None:
        """A source outside the graph raises ValueError."""
        g, _ = _build(Graph, Edge, "ab", [("a", "b")])
        with pytest.raises(ValueError):
            list(traversal(g, GraphNode("z", "z")))

    def test_is_lazy(self, traversal: Traversal) -> None:
        """The first node is available before the traversal finishes."""
        g, n = _build(Graph, Edge, "abc", [("a", "b"), ("b", "c")])
        it = traversal(g, n["a"])
        assert next(it).id == "a"

    def test_does_not_modify_graph(self, traversal: Traversal) -> None:
        """The graph is left untouched."""
        g, n = _build(Graph, Edge, "abcdef", REF_PAIRS)
        before = (g.node_count(), g.edge_count())
        list(traversal(g, n["a"]))
        assert (g.node_count(), g.edge_count()) == before

    def test_deep_chain(self, traversal: Traversal) -> None:
        """A path three times longer than the recursion limit is explored."""
        length = sys.getrecursionlimit() * 3
        ids = [str(i) for i in range(length)]
        g = DirectedGraph()
        nodes = [GraphNode(i, i) for i in ids]
        for node in nodes:
            g.add_node(node)
        for u, v in zip(nodes, nodes[1:]):
            g.add_edge(DirectedEdge(u, v))
        assert _ids(traversal(g, nodes[0])) == ids


class TestAgainstReferences:
    """Random graphs checked against independent implementations."""

    @staticmethod
    def _random_graph(
        seed: int, directed: bool
    ) -> Tuple[AbstractGraph, List[GraphNode]]:
        rng = random.Random(seed)
        graph: AbstractGraph = DirectedGraph() if directed else Graph()
        nodes = [GraphNode(str(i), i) for i in range(rng.randint(1, 25))]
        for node in nodes:
            graph.add_node(node)
        for u, v in itertools.permutations(nodes, 2):
            if rng.random() < 0.12 and not graph.has_edge(u, v):
                graph.add_edge(DirectedEdge(u, v) if directed else Edge(u, v))
        return graph, nodes

    @pytest.mark.parametrize("directed", [False, True], ids=["undirected", "directed"])
    @pytest.mark.parametrize("seed", range(15))
    def test_dfs_matches_recursive(self, seed: int, directed: bool) -> None:
        """Iterative DFS visits in exactly the recursive order."""
        g, nodes = self._random_graph(seed, directed)
        assert list(dfs(g, nodes[0])) == _reference_dfs(g, nodes[0])

    @pytest.mark.parametrize("directed", [False, True], ids=["undirected", "directed"])
    @pytest.mark.parametrize("seed", range(15))
    def test_bfs_by_distance(self, seed: int, directed: bool) -> None:
        """BFS reaches the same nodes, in non-decreasing hop distance."""
        g, nodes = self._random_graph(seed, directed)
        dist = _hop_distances(g, nodes[0])
        order = list(bfs(g, nodes[0]))
        assert set(order) == set(dist)
        assert len(order) == len(set(order))
        levels = [dist[node] for node in order]
        assert levels == sorted(levels)
