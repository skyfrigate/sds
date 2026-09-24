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

"""Dijkstra's single-source shortest paths.

Dijkstra's algorithm computes, for every node reachable from a source, the
minimum total weight of a path from the source, provided every edge weight
is non-negative. It grows a set of *settled* nodes whose distance is final,
always settling next the unsettled node with the smallest tentative
distance, then *relaxing* its outgoing edges:

.. code-block:: text

    dist[s] <- 0; push (0, s) on a min-priority queue
    while queue not empty:
        (d, u) <- pop minimum
        if u settled: continue            # stale entry
        settle u
        for each edge (u, v, w) leaving u:
            if d + w < dist[v]:           # relaxation
                dist[v] <- d + w; pred[v] <- u; push (dist[v], v)

With a binary heap the loop costs O((V + E) log V). Rather than decreasing
keys in place, a better distance is pushed as a new entry and outdated
entries are skipped when popped ("lazy deletion").

The relaxation step reads each settled node's outgoing edges through
``outgoing_edges()`` in O(degree) (#87), which is what keeps the whole
algorithm within its bound.
"""

import heapq
from itertools import count
from typing import Dict, List, Optional, Set, Tuple

from ...graph.interfaces import AbstractWeightedGraph
from ...graph.node import GraphNode

__all__ = ["dijkstra"]


def dijkstra(
    graph: AbstractWeightedGraph, source: GraphNode
) -> Tuple[Dict[GraphNode, float], Dict[GraphNode, Optional[GraphNode]]]:
    """Compute shortest distances and paths from ``source``.

    Parameters
    ----------
    graph : AbstractWeightedGraph
        A weighted graph, directed or not, with non-negative weights. On an
        undirected graph every edge can be followed both ways.
    source : GraphNode
        The node distances are measured from.

    Returns
    -------
    distances : dict of GraphNode to float
        The shortest distance from ``source`` to every reachable node
        (``distances[source] == 0``). Unreachable nodes are absent.
    predecessors : dict of GraphNode to GraphNode or None
        For every reachable node, the previous node on one shortest path
        from ``source`` (``None`` for ``source`` itself). Following it back
        from a node rebuilds that path in reverse.

    Raises
    ------
    ValueError
        If ``source`` is not in the graph, or if a negative edge weight is
        reached from ``source``.

    Examples
    --------
    >>> from sds.graph import GraphNode, WeightedEdge, WeightedGraph
    >>> a, b, c = (GraphNode(x, x) for x in "abc")
    >>> g = WeightedGraph()
    >>> for n in (a, b, c):
    ...     g.add_node(n)
    >>> g.add_edge(WeightedEdge(a, b, 4.0))
    >>> g.add_edge(WeightedEdge(a, c, 1.0))
    >>> g.add_edge(WeightedEdge(c, b, 2.0))
    >>> dist, pred = dijkstra(g, a)
    >>> dist[b], pred[b].id, pred[c].id
    (3.0, 'c', 'a')

    Rebuilding the path to ``b``:

    >>> path, node = [], b
    >>> while node is not None:
    ...     path.append(node.id)
    ...     node = pred[node]
    >>> path[::-1]
    ['a', 'c', 'b']

    Notes
    -----
    Time complexity: O((V + E) log V) with a binary heap.
    Space complexity: O(V + E) in the worst case (lazy deletion lets the
    heap hold one entry per successful relaxation).

    Among several shortest paths, the one recorded is the first found;
    since neighbors are visited in edge insertion order, the result is
    deterministic. Parallel edges are fine: only the lightest can relax.

    Negative weights break the greedy argument (a settled distance could
    later be improved), hence the ``ValueError``; use Bellman-Ford for such
    graphs.
    """
    if not graph.has_node(source):
        raise ValueError(f"Node {source.id} not in graph")

    distances: Dict[GraphNode, float] = {source: 0.0}
    predecessors: Dict[GraphNode, Optional[GraphNode]] = {source: None}
    settled: Set[GraphNode] = set()
    # The counter breaks ties between equal distances, so nodes themselves
    # are never compared, and equal distances pop in push order.
    tie = count()
    heap: List[Tuple[float, int, GraphNode]] = [(0.0, next(tie), source)]

    while heap:
        dist, _, node = heapq.heappop(heap)
        if node in settled:
            continue  # stale entry, superseded by a shorter one
        settled.add(node)
        for edge in graph.outgoing_edges(node):
            if edge.weight < 0:
                raise ValueError(
                    f"Negative weight {edge.weight} on an edge leaving "
                    f"{node.id}; Dijkstra requires non-negative weights"
                )
            neighbor = edge.other_node(node)
            candidate = dist + edge.weight
            if neighbor not in distances or candidate < distances[neighbor]:
                distances[neighbor] = candidate
                predecessors[neighbor] = node
                heapq.heappush(heap, (candidate, next(tie), neighbor))

    return distances, predecessors
