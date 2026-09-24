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

"""Kruskal's minimum spanning tree (forest).

A *spanning tree* of a connected undirected graph links every node with
exactly ``V - 1`` of its edges and no cycle; a *minimum* spanning tree
(MST) does so with the smallest total weight. On a disconnected graph the
same idea yields a *minimum spanning forest*: one MST per connected
component.

Kruskal's algorithm is greedy: it scans the edges from lightest to
heaviest and keeps an edge whenever it joins two nodes not yet connected
by the edges kept so far. A disjoint-set (union-find) structure answers
"already connected?" in near-constant time.

.. code-block:: text

    F <- graph with the nodes of G and no edge
    make_set(v) for every node v
    for (u, v, w) in edges of G sorted by w:
        if find(u) != find(v):          # u and v in different trees
            add (u, v, w) to F; union(u, v)
    return F

The *cut property* guarantees the result is minimal: the lightest edge
crossing any partition of the nodes belongs to some MST, and every edge
Kruskal keeps is the lightest one crossing the cut between its two trees.
"""

from typing import List

from ...advanced.disjoint_set import DisjointSet
from ...graph.edge import WeightedEdge
from ...graph.weighted import WeightedGraph
from ..sorting import merge_sort

__all__ = ["kruskal"]


def kruskal(graph: WeightedGraph) -> WeightedGraph:
    """Return a minimum spanning forest of an undirected weighted graph.

    Parameters
    ----------
    graph : WeightedGraph
        An undirected weighted graph. It is not modified. Directed graphs
        are not accepted: spanning trees are defined on undirected graphs
        (the directed analogue, the minimum arborescence, needs a different
        algorithm).

    Returns
    -------
    WeightedGraph
        A new graph holding every node of ``graph`` and the edges of a
        minimum spanning forest: ``V - C`` edges, with ``C`` the number of
        connected components. The edge objects are those of ``graph``,
        shared rather than copied.

    Raises
    ------
    TypeError
        If ``graph`` is not a :class:`~sds.graph.WeightedGraph`.

    Examples
    --------
    >>> from sds.graph import GraphNode, WeightedEdge, WeightedGraph
    >>> a, b, c, d = (GraphNode(x, x) for x in "abcd")
    >>> g = WeightedGraph()
    >>> for n in (a, b, c, d):
    ...     g.add_node(n)
    >>> for u, v, w in ((a, b, 1.0), (b, c, 4.0), (a, c, 3.0), (c, d, 2.0)):
    ...     g.add_edge(WeightedEdge(u, v, w))
    >>> mst = kruskal(g)
    >>> mst.edge_count(), mst.total_weight()
    (3, 6.0)

    Notes
    -----
    Time complexity: O(E log E) for sorting the edges, plus
    O(E α(V)) for the union-find operations.
    Space complexity: O(V + E).

    The parameter is typed on the concrete ``WeightedGraph`` rather than on
    ``AbstractWeightedGraph`` (#86): the algorithm needs an undirected
    weighted graph *and* a way to build the result, which no single
    abstract interface provides.

    Edges are sorted with :func:`~sds.algorithms.sorting.merge_sort`, which
    is stable: among edges of equal weight, the one inserted first in
    ``graph`` is considered first, so the forest returned is deterministic.
    """
    if not isinstance(graph, WeightedGraph):
        raise TypeError(f"kruskal expects a WeightedGraph, got {type(graph).__name__}")

    forest = WeightedGraph(allow_multi_edges=False)
    components = DisjointSet()
    for node in graph.nodes():
        forest.add_node(node)
        components.make_set(node.id)

    edges: List[WeightedEdge] = list(graph.edges())
    for edge in merge_sort(edges, key=lambda e: e.weight):
        if components.union(edge.node1.id, edge.node2.id):
            forest.add_edge(edge)
    return forest
