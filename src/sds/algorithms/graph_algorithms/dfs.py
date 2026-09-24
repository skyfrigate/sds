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

"""Depth-first search (DFS).

DFS follows one path as deep as it can, then backtracks to the most recent
node that still has an unexplored neighbor. It is the basis of cycle
detection, topological sorting and connected-component labelling.

.. code-block:: text

    DFS(G, u):
        mark u; emit u
        for v in neighbors(u):
            if v not marked: DFS(G, v)

The implementation below is iterative: it keeps a stack of *neighbor
iterators*, one per node on the current path. Resuming the iterator on top
of the stack is exactly what returning from a recursive call does, so the
visiting order is the same as the recursive version above, while the depth
of the graph is no longer bounded by Python's recursion limit.
"""

from typing import Iterator, List, Set

from ...graph.interfaces import AbstractGraph
from ...graph.node import GraphNode

__all__ = ["dfs"]


def dfs(graph: AbstractGraph, source: GraphNode) -> Iterator[GraphNode]:
    """Yield the nodes reachable from ``source`` in depth-first preorder.

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
        Every node reachable from ``source``, exactly once, in the order a
        recursive DFS first reaches them, exploring neighbors in the order
        the graph lists them (edge insertion order).

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
    >>> [n.id for n in dfs(g, a)]
    ['a', 'b', 'd', 'c']

    Notes
    -----
    Time complexity: O(V + E) over the reachable part of the graph.
    Space complexity: O(V) for the visited set and the stack.
    """
    if not graph.has_node(source):
        raise ValueError(f"Node {source.id} not in graph")
    visited: Set[GraphNode] = {source}
    yield source
    stack: List[Iterator[GraphNode]] = [graph.neighbors(source)]
    while stack:
        for neighbor in stack[-1]:
            if neighbor not in visited:
                visited.add(neighbor)
                yield neighbor
                stack.append(graph.neighbors(neighbor))
                break
        else:
            # Every neighbor of the node on top has been explored: backtrack.
            stack.pop()
