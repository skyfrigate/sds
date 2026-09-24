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

"""Tests for sds.algorithms.graph_algorithms.kruskal (#61, #62, #86)."""

import heapq
import itertools
import math
import random
from typing import Any, Callable, Dict, List, Set, Tuple

import pytest

from sds.algorithms.graph_algorithms import bfs, kruskal
from sds.graph import (
    Graph,
    GraphNode,
    WeightedDirectedGraph,
    WeightedEdge,
    WeightedGraph,
)

# --------------------------------------------------------------------------
# Builders
# --------------------------------------------------------------------------


def _weighted(
    graph_cls: Callable[..., Any],
    edge_cls: Callable[..., Any],
    ids: str,
    triples: List[Tuple[str, str, float]],
    **kwargs: Any,
) -> Tuple[Any, Dict[str, GraphNode]]:
    graph = graph_cls(**kwargs)
    nodes = {i: GraphNode(i, i) for i in ids}
    for node in nodes.values():
        graph.add_node(node)
    for u, v, w in triples:
        graph.add_edge(edge_cls(nodes[u], nodes[v], w))
    return graph, nodes


# --------------------------------------------------------------------------
# Kruskal
# --------------------------------------------------------------------------


def _prim_weight(graph: WeightedGraph) -> float:
    """Minimum spanning forest weight via Prim, the oracle for Kruskal."""
    total = 0.0
    seen: Set[GraphNode] = set()
    for start in graph.nodes():
        if start in seen:
            continue
        seen.add(start)
        heap: List[Tuple[float, int, GraphNode]] = []
        tie = itertools.count()
        for e in graph.outgoing_edges(start):
            heapq.heappush(heap, (e.weight, next(tie), e.other_node(start)))
        while heap:
            w, _, node = heapq.heappop(heap)
            if node in seen:
                continue
            seen.add(node)
            total += w
            for e in graph.outgoing_edges(node):
                heapq.heappush(heap, (e.weight, next(tie), e.other_node(node)))
    return total


def _components(graph: WeightedGraph) -> int:
    seen: Set[GraphNode] = set()
    count = 0
    for node in graph.nodes():
        if node not in seen:
            count += 1
            seen.update(bfs(graph, node))
    return count


class TestKruskal:
    """Minimum spanning forests."""

    EXAMPLE = [
        ("a", "b", 4.0),
        ("a", "h", 8.0),
        ("b", "c", 8.0),
        ("b", "h", 11.0),
        ("c", "d", 7.0),
        ("c", "f", 4.0),
        ("c", "i", 2.0),
        ("d", "e", 9.0),
        ("d", "f", 14.0),
        ("e", "f", 10.0),
        ("f", "g", 2.0),
        ("g", "h", 1.0),
        ("g", "i", 6.0),
        ("h", "i", 7.0),
    ]

    def test_textbook_example(self) -> None:
        """CLRS figure 23.1: nine nodes, MST weight 37."""
        g, _ = _weighted(WeightedGraph, WeightedEdge, "abcdefghi", self.EXAMPLE)
        mst = kruskal(g)
        assert mst.node_count() == 9
        assert mst.edge_count() == 8
        assert mst.total_weight() == 37.0
        assert mst.is_connected()

    def test_tie_break_is_insertion_order(self) -> None:
        """Among equal weights, the edge inserted first is kept."""
        g, _ = _weighted(
            WeightedGraph,
            WeightedEdge,
            "abc",
            [("a", "b", 1.0), ("b", "c", 1.0), ("a", "c", 1.0)],
        )
        kept = {frozenset((e.node1.id, e.node2.id)) for e in kruskal(g).edges()}
        assert kept == {frozenset("ab"), frozenset("bc")}

    def test_forest_on_disconnected_graph(self) -> None:
        """A disconnected graph gives V - C edges."""
        g, _ = _weighted(
            WeightedGraph,
            WeightedEdge,
            "abcdef",
            [("a", "b", 1.0), ("b", "c", 2.0), ("d", "e", 3.0)],
        )
        forest = kruskal(g)
        assert forest.node_count() == 6
        assert forest.edge_count() == 6 - 3

    def test_empty_graph(self) -> None:
        """An empty graph gives an empty forest."""
        forest = kruskal(WeightedGraph())
        assert forest.node_count() == 0
        assert forest.edge_count() == 0

    def test_input_unchanged_and_edges_shared(self) -> None:
        """The input is not modified; forest edges are the input's objects."""
        g, _ = _weighted(WeightedGraph, WeightedEdge, "abcdefghi", self.EXAMPLE)
        before = g.edge_count()
        forest = kruskal(g)
        assert g.edge_count() == before
        originals = {id(e) for e in g.edges()}
        assert all(id(e) in originals for e in forest.edges())

    def test_parallel_edges(self) -> None:
        """With parallel edges, only the lightest is kept."""
        g, _ = _weighted(
            WeightedGraph,
            WeightedEdge,
            "ab",
            [("a", "b", 5.0), ("a", "b", 2.0)],
            allow_multi_edges=True,
        )
        assert [e.weight for e in kruskal(g).edges()] == [2.0]

    @pytest.mark.parametrize(
        "bad",
        [WeightedDirectedGraph(), Graph(), None],
        ids=["WeightedDirectedGraph", "Graph", "None"],
    )
    def test_rejects_non_weighted_undirected(self, bad: Any) -> None:
        """Only undirected weighted graphs are accepted (#86)."""
        with pytest.raises(TypeError, match="WeightedGraph"):
            kruskal(bad)

    @pytest.mark.parametrize("seed", range(20))
    def test_random_against_prim(self, seed: int) -> None:
        """Random graphs: same forest weight as Prim, V - C edges, acyclic."""
        rng = random.Random(seed)
        nodes = [GraphNode(str(i), i) for i in range(rng.randint(1, 20))]
        g = WeightedGraph()
        for node in nodes:
            g.add_node(node)
        for u, v in itertools.combinations(nodes, 2):
            if rng.random() < 0.3:
                g.add_edge(WeightedEdge(u, v, float(rng.randint(1, 9))))
        forest = kruskal(g)
        assert math.isclose(forest.total_weight(), _prim_weight(g))
        assert forest.edge_count() == g.node_count() - _components(g)
        assert _components(forest) == _components(g)
