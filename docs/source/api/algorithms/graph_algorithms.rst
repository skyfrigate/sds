.. _api_algorithms_graph:

========================
Graph Algorithms
========================

.. currentmodule:: sds.algorithms.graph_algorithms

Overview
========

This subpackage provides the four classic graph algorithms: two traversals
and two optimization algorithms on weighted graphs.

.. list-table::
   :header-rows: 1
   :widths: 18 32 25 25

   * - Function
     - Computes
     - Accepts
     - Time
   * - :func:`bfs`
     - Nodes reachable from a source, by distance in edges
     - any ``AbstractGraph``
     - :math:`O(V + E)`
   * - :func:`dfs`
     - Nodes reachable from a source, deepest first
     - any ``AbstractGraph``
     - :math:`O(V + E)`
   * - :func:`dijkstra`
     - Shortest distances and paths from a source
     - any ``AbstractWeightedGraph``
     - :math:`O((V + E) \log V)`
   * - :func:`kruskal`
     - Minimum spanning forest
     - ``WeightedGraph``
     - :math:`O(E \log E)`

Each function reads the graph through its public interface and never
modifies it. Each one accepts the broadest abstraction that offers what it
needs: the traversals only need ``neighbors()``, Dijkstra needs weighted
outgoing edges, and Kruskal needs an *undirected* weighted graph plus a way
to build its result, which only the concrete ``WeightedGraph`` provides.

.. note::

   **Results are reproducible.** Graphs yield neighbors in edge insertion
   order, so a traversal visits nodes in the same order on every run, and
   ties between equal paths or equal weights are always broken the same way.

Traversals
==========

Both traversals start from a source node and visit every node reachable
from it exactly once. They differ in the data structure holding the nodes
still to explore: a **queue** for breadth-first search, a **stack** for
depth-first search.

.. mermaid::

   graph LR
       A((a)) --- B((b))
       A --- C((c))
       B --- D((d))
       B --- E((e))
       C --- E

       style A fill:#3498db,color:#fff

.. list-table:: Visiting order from ``a`` (edges inserted a-b, a-c, b-d, b-e, c-e)
   :header-rows: 1
   :widths: 20 30 50

   * - Traversal
     - Order
     - Why
   * - ``bfs``
     - a, b, c, d, e
     - distance 0, then distance 1 (b, c), then distance 2 (d, e)
   * - ``dfs``
     - a, b, d, e, c
     - follows a-b-d, backtracks to b, goes to e, reaches c from e

On a directed graph, both follow arcs from source to target only.

.. autofunction:: bfs

.. autofunction:: dfs

Shortest Paths: Dijkstra
========================

Given a weighted graph with non-negative weights, Dijkstra's algorithm
computes the shortest distance from a source to every reachable node. It
repeatedly *settles* the unsettled node closest to the source, then
*relaxes* each of its outgoing edges :math:`(u, v, w)`:

.. math::

   d(v) \leftarrow \min\big(d(v),\; d(u) + w\big)

Once settled, a node's distance never changes: any other path to it would
leave the settled region through a node at least as far away, and
non-negative weights cannot make that path shorter. This is why a negative
weight breaks the algorithm, and why the implementation raises
``ValueError`` when it meets one.

.. mermaid::

   graph LR
       S((s)) -- 10 --> T((t))
       S -- 5 --> Y((y))
       T -- 1 --> X((x))
       T -- 2 --> Y
       Y -- 3 --> T
       Y -- 9 --> X
       Y -- 2 --> Z((z))
       X -- 4 --> Z
       Z -- 7 --> S
       Z -- 6 --> X

       style S fill:#3498db,color:#fff

From ``s``: :math:`d(y) = 5`, :math:`d(z) = 7`, :math:`d(t) = 8` (through
``y``), :math:`d(x) = 9` (through ``y`` then ``t``).

The function returns two dictionaries: the distances, and for each node
its predecessor on a shortest path. Following predecessors back from a node
rebuilds the path:

.. code-block:: python

   from sds.algorithms.graph_algorithms import dijkstra

   dist, pred = dijkstra(graph, source)

   path, node = [], target
   while node is not None:
       path.append(node)
       node = pred[node]
   path.reverse()                    # source ... target

.. autofunction:: dijkstra

Minimum Spanning Forest: Kruskal
================================

A **minimum spanning tree** (MST) of a connected undirected graph connects
all its :math:`V` nodes with :math:`V - 1` edges of minimum total weight.
On a graph with :math:`C` connected components, the same construction
gives a **minimum spanning forest** of :math:`V - C` edges.

Kruskal's algorithm scans the edges by increasing weight and keeps an edge
whenever its two endpoints are not yet connected. A disjoint-set
(:class:`sds.advanced.DisjointSet`) answers that question in near-constant
time. The result is optimal by the **cut property**: for any split of the
nodes into two groups, the lightest edge crossing between them belongs to
some MST.

.. mermaid::

   graph LR
       A((a)) -- 1 --- B((b))
       B -. 4 .- C((c))
       A -- 3 --- C
       C -- 2 --- D((d))

   %% Kept: a-b (1), c-d (2), a-c (3). Rejected: b-c (4) would close a cycle.

Edges are sorted with :func:`~sds.algorithms.sorting.merge_sort`, which is
stable, so among edges of equal weight the one inserted first wins: the
forest returned is always the same.

.. autofunction:: kruskal

Usage Example: Road Network
===========================

.. code-block:: python

   from sds.graph import GraphNode, WeightedEdge, WeightedGraph
   from sds.algorithms.graph_algorithms import bfs, dijkstra, kruskal

   cities = {name: GraphNode(name, name) for name in
             ["Paris", "Lyon", "Lille", "Nantes", "Bordeaux"]}
   roads = WeightedGraph()
   for city in cities.values():
       roads.add_node(city)
   for a, b, km in [("Paris", "Lyon", 465), ("Paris", "Lille", 225),
                    ("Paris", "Nantes", 385), ("Nantes", "Bordeaux", 345),
                    ("Lyon", "Bordeaux", 555), ("Paris", "Bordeaux", 585)]:
       roads.add_edge(WeightedEdge(cities[a], cities[b], km))

   # Which cities can be reached from Lille, closest (in hops) first?
   [c.id for c in bfs(roads, cities["Lille"])]

   # Shortest driving distance from Lille to Bordeaux
   dist, pred = dijkstra(roads, cities["Lille"])
   dist[cities["Bordeaux"]]          # 810: Lille - Paris - Bordeaux

   # Cheapest set of roads keeping every city connected
   network = kruskal(roads)
   network.total_weight()            # 1420

Best Practices
==============

✅ Use ``bfs`` for shortest paths counted in edges; use ``dijkstra`` as
soon as edges carry weights.

✅ Keep the predecessor dictionary of ``dijkstra``: it holds every shortest
path from the source, not only one.

✅ Materialize a traversal with ``list(...)`` if the graph may change
afterwards: the traversals are lazy.

❌ Do not run ``dijkstra`` on graphs with negative weights; it raises
``ValueError`` as soon as it meets one.

❌ Do not pass a directed graph to ``kruskal``: minimum spanning trees are
defined on undirected graphs.

References
==========

* OpenDSA, *Graphs* chapters (traversals, shortest paths, minimum spanning
  trees) — https://opendsa-server.cs.vt.edu/ODSA/Books/Everything/html/GraphTraversal.html
* R. Sedgewick and K. Wayne, *Algorithms, 4th Edition*, chapter 4 (free
  online companion) — https://algs4.cs.princeton.edu/40graphs/
* J. Erickson, *Algorithms*, chapters 5–8 (open-access textbook) —
  https://jeffe.cs.illinois.edu/teaching/algorithms/
* R. Diestel, *Graph Theory* (free electronic edition) —
  https://diestel-graph-theory.com/
