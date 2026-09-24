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

"""Breadth-first search (BFS).

BFS explores a graph in rings around the source: first the source, then
every node one edge away, then every node two edges away, and so on. A
FIFO queue holds the frontier. Because nodes are discovered in order of
their distance from the source (counted in edges), BFS finds shortest
paths in *unweighted* graphs.

.. code-block:: text

    BFS(G, s):
        mark s; Q <- [s]
        while Q not empty:
            u <- Q.dequeue(); emit u
            for v in neighbors(u):
                if v not marked: mark v; Q.enqueue(v)

A node is marked when it is *enqueued*, not when it is dequeued, so it
enters the queue at most once.
"""

from collections import deque
from typing import Deque, Iterator, Set

from ...graph.interfaces import AbstractGraph
from ...graph.node import GraphNode

__all__ = ["bfs"]


def bfs(graph: AbstractGraph, source: GraphNode) -> Iterator[GraphNode]:
    """Yield the nodes reachable from ``source`` in breadth-first order.

    Parameters
    ----------
    graph : AbstractGraph
        Any graph. For a directed graph, edges are followed from source to
        target only (``neighbors()`` yields successors).
    source : GraphNode
        The starting node, yielded first.

    Yields
    ------
    GraphNode
        Every node reachable from ``source``, exactly once, by
        non-decreasing number of edges from the source. Nodes at the same
        distance come in the order their discoverer's neighbors are listed,
        i.e. edge insertion order.

    Raises
    ------
    ValueError
        If ``source`` is not in the graph (raised on the first ``next()``).

    Examples
    --------
    >>> from sds.graph import Edge, Graph, GraphNode
    >>> a, b, c, d = (GraphNode(x, x) for x in "abcd")
    >>> g = Graph()
    >>> for n in (a, b, c, d):
    ...     g.add_node(n)
    >>> for u, v in ((a, b), (a, c), (b, d)):
    ...     g.add_edge(Edge(u, v))
    >>> [n.id for n in bfs(g, a)]
    ['a', 'b', 'c', 'd']

    Notes
    -----
    Time complexity: O(V + E) over the reachable part of the graph.
    Space complexity: O(V) for the visited set and the queue.

    Nodes not reachable from ``source`` are not visited; call :func:`bfs`
    again from one of them to explore another connected component.
    """
    if not graph.has_node(source):
        raise ValueError(f"Node {source.id} not in graph")
    visited: Set[GraphNode] = {source}
    queue: Deque[GraphNode] = deque([source])
    while queue:
        node = queue.popleft()
        yield node
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
