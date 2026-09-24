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

"""Tests for sds.algorithms.graph_algorithms.dijkstra (#61, #62, #87)."""

import itertools
import math
import random
from typing import Any, Callable, Dict, List, Optional, Tuple

import pytest

from sds.algorithms.graph_algorithms import dijkstra
from sds.graph import (
    GraphNode,
    WeightedDirectedEdge,
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
# Dijkstra
# --------------------------------------------------------------------------

# Directed example (CLRS figure 24.6 layout):
#   s->t 10, s->y 5, t->x 1, t->y 2, y->t 3, y->x 9, y->z 2, x->z 4, z->s 7, z->x 6
CLRS = [
    ("s", "t", 10.0),
    ("s", "y", 5.0),
    ("t", "x", 1.0),
    ("t", "y", 2.0),
    ("y", "t", 3.0),
    ("y", "x", 9.0),
    ("y", "z", 2.0),
    ("x", "z", 4.0),
    ("z", "s", 7.0),
    ("z", "x", 6.0),
]


def _brute_force(
    nodes: List[GraphNode], edges: List[Tuple[GraphNode, GraphNode, float]]
) -> Dict[GraphNode, float]:
    """Bellman-Ford distances from nodes[0], the oracle for Dijkstra."""
    dist = {node: math.inf for node in nodes}
    dist[nodes[0]] = 0.0
    for _ in range(len(nodes) - 1):
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return {node: d for node, d in dist.items() if d < math.inf}


class TestDijkstra:
    """Shortest paths on weighted graphs."""

    def test_clrs_distances(self) -> None:
        """Distances match the textbook example."""
        g, n = _weighted(WeightedDirectedGraph, WeightedDirectedEdge, "stxyz", CLRS)
        dist, _ = dijkstra(g, n["s"])
        assert {k.id: v for k, v in dist.items()} == {
            "s": 0.0,
            "t": 8.0,
            "x": 9.0,
            "y": 5.0,
            "z": 7.0,
        }

    def test_clrs_predecessors(self) -> None:
        """Predecessors describe a shortest-path tree."""
        g, n = _weighted(WeightedDirectedGraph, WeightedDirectedEdge, "stxyz", CLRS)
        _, pred = dijkstra(g, n["s"])
        parents = {k.id: (v.id if v is not None else None) for k, v in pred.items()}
        assert parents == {"s": None, "t": "y", "x": "t", "y": "s", "z": "y"}

    def test_path_reconstruction(self) -> None:
        """Following predecessors back from a target rebuilds the path."""
        g, n = _weighted(WeightedDirectedGraph, WeightedDirectedEdge, "stxyz", CLRS)
        _, pred = dijkstra(g, n["s"])
        path: List[str] = []
        node: Optional[GraphNode] = n["x"]
        while node is not None:
            path.append(node.id)
            node = pred[node]
        assert path[::-1] == ["s", "y", "t", "x"]

    def test_undirected_both_ways(self) -> None:
        """On an undirected graph, edges are usable in both directions."""
        g, n = _weighted(
            WeightedGraph, WeightedEdge, "abc", [("b", "a", 1.0), ("c", "b", 2.0)]
        )
        dist, _ = dijkstra(g, n["a"])
        assert dist[n["c"]] == 3.0

    def test_directed_respects_direction(self) -> None:
        """An arc cannot be followed backwards."""
        g, n = _weighted(
            WeightedDirectedGraph, WeightedDirectedEdge, "ab", [("b", "a", 1.0)]
        )
        dist, pred = dijkstra(g, n["a"])
        assert n["b"] not in dist
        assert n["b"] not in pred

    def test_unreachable_absent(self) -> None:
        """Nodes that cannot be reached are not in the results."""
        g, n = _weighted(WeightedGraph, WeightedEdge, "abc", [("a", "b", 1.0)])
        dist, _ = dijkstra(g, n["a"])
        assert set(dist) == {n["a"], n["b"]}

    def test_zero_weights(self) -> None:
        """Zero-weight edges are allowed."""
        g, n = _weighted(
            WeightedGraph, WeightedEdge, "abc", [("a", "b", 0.0), ("b", "c", 0.0)]
        )
        assert dijkstra(g, n["a"])[0][n["c"]] == 0.0

    def test_parallel_edges_lightest_wins(self) -> None:
        """With parallel edges, the lightest one gives the distance."""
        g, n = _weighted(
            WeightedGraph,
            WeightedEdge,
            "ab",
            [("a", "b", 5.0), ("a", "b", 2.0), ("a", "b", 7.0)],
            allow_multi_edges=True,
        )
        assert dijkstra(g, n["a"])[0][n["b"]] == 2.0

    def test_equal_paths_first_found(self) -> None:
        """Among equal-length paths, the first discovered is recorded."""
        g, n = _weighted(
            WeightedGraph,
            WeightedEdge,
            "abcd",
            [("a", "b", 1.0), ("a", "c", 1.0), ("b", "d", 1.0), ("c", "d", 1.0)],
        )
        _, pred = dijkstra(g, n["a"])
        assert pred[n["d"]] is n["b"]

    def test_negative_weight_raises(self) -> None:
        """A reachable negative weight raises ValueError."""
        g, n = _weighted(
            WeightedDirectedGraph,
            WeightedDirectedEdge,
            "abc",
            [("a", "b", 1.0), ("b", "c", -1.0)],
        )
        with pytest.raises(ValueError, match="Negative weight"):
            dijkstra(g, n["a"])

    def test_unreachable_negative_weight_ignored(self) -> None:
        """A negative weight never reached does not matter."""
        g, n = _weighted(
            WeightedDirectedGraph,
            WeightedDirectedEdge,
            "abc",
            [("a", "b", 1.0), ("c", "a", -1.0)],
        )
        assert dijkstra(g, n["a"])[0][n["b"]] == 1.0

    def test_missing_source(self) -> None:
        """A source outside the graph raises ValueError."""
        with pytest.raises(ValueError):
            dijkstra(WeightedGraph(), GraphNode("z", "z"))

    def test_uses_outgoing_edges_only(self) -> None:
        """Dijkstra never scans the flat edge list (O(degree) access)."""
        g, n = _weighted(WeightedDirectedGraph, WeightedDirectedEdge, "stxyz", CLRS)
        g._edges = []  # sabotage the O(E) accessors
        assert dijkstra(g, n["s"])[0][n["x"]] == 9.0

    @pytest.mark.parametrize("directed", [False, True], ids=["undirected", "directed"])
    @pytest.mark.parametrize("seed", range(20))
    def test_random_against_bellman_ford(self, seed: int, directed: bool) -> None:
        """Random non-negative graphs agree with Bellman-Ford."""
        rng = random.Random(seed)
        nodes = [GraphNode(str(i), i) for i in range(rng.randint(1, 15))]
        g: Any = WeightedDirectedGraph() if directed else WeightedGraph()
        for node in nodes:
            g.add_node(node)
        triples: List[Tuple[GraphNode, GraphNode, float]] = []
        for u, v in itertools.permutations(nodes, 2):
            if rng.random() < 0.25 and not g.has_edge(u, v):
                w = float(rng.randint(0, 20))
                g.add_edge(
                    WeightedDirectedEdge(u, v, w) if directed else WeightedEdge(u, v, w)
                )
                triples.append((u, v, w))
                if not directed:
                    triples.append((v, u, w))
        dist, pred = dijkstra(g, nodes[0])
        assert dist == _brute_force(nodes, triples)
        # Each predecessor link is a tight edge of the shortest-path tree.
        for node, parent in pred.items():
            if parent is not None:
                assert math.isclose(
                    dist[parent] + g.get_edge_weight(parent, node), dist[node]
                )
