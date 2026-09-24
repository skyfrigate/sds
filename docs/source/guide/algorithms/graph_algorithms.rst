.. _guide_algorithms_graph:

================
Graph Algorithms
================

.. currentmodule:: sds.algorithms.graph_algorithms

Introduction
============

This page covers four fundamental graph algorithms:

- **Breadth-first search** and **depth-first search**, which explore
  everything reachable from a node;
- **Dijkstra's algorithm**, which finds shortest paths in a weighted graph;
- **Kruskal's algorithm**, which finds a cheapest way to connect every node.

Throughout, :math:`V` is the number of nodes and :math:`E` the number of
edges. Graphs in ``sds`` list neighbors in edge insertion order, so every
traversal below is reproducible, and the orders shown are exactly those the
library produces.

Graph Traversals
================

Both traversals start from a source and visit each reachable node once.
They share one skeleton and differ only in the container holding the
*frontier*, the discovered nodes not yet explored:

.. list-table::
   :header-rows: 1
   :widths: 20 25 55

   * - Traversal
     - Frontier
     - Consequence
   * - BFS
     - queue (FIFO)
     - explores in rings of increasing distance from the source
   * - DFS
     - stack (LIFO)
     - follows one path as deep as possible, then backtracks

Running Example
---------------

Edges inserted in the order a–b, a–c, b–d, b–e, c–e, d–f:

.. mermaid::

   graph LR
       A((a)) --- B((b))
       A --- C((c))
       B --- D((d))
       B --- E((e))
       C --- E
       D --- F((f))

       style A fill:#3498db,color:#fff

Breadth-First Search
--------------------

.. code-block:: text

    BFS(G, s):
        mark s; Q <- [s]
        while Q not empty:
            u <- dequeue(Q); emit u
            for v in neighbors(u):
                if v not marked: mark v; enqueue(Q, v)

.. list-table:: BFS from ``a``
   :header-rows: 1
   :widths: 15 25 30 30

   * - Step
     - Dequeued
     - Newly discovered
     - Queue after
   * - 1
     - a
     - b, c
     - b, c
   * - 2
     - b
     - d, e
     - c, d, e
   * - 3
     - c
     - —
     - d, e
   * - 4
     - d
     - f
     - e, f
   * - 5
     - e
     - —
     - f
   * - 6
     - f
     - —
     - (empty)

Order: a, b, c, d, e, f.

.. mermaid::

   graph LR
       subgraph "distance 0"
       A((a))
       end
       subgraph "distance 1"
       B((b))
       C((c))
       end
       subgraph "distance 2"
       D((d))
       E((e))
       end
       subgraph "distance 3"
       F((f))
       end
       A --> B & C
       B --> D & E
       D --> F

**Lemma (shortest paths in edges).** BFS emits nodes by non-decreasing
distance :math:`d(s, v)` from the source, and the edge through which a
node is discovered lies on a shortest path.

*Proof sketch.* By induction on the dequeue order, the queue always holds
nodes of distance :math:`k` followed by nodes of distance :math:`k + 1`.
A node discovered from a node of distance :math:`k` has distance at most
:math:`k + 1`, and not less, otherwise it would have been discovered
earlier from a node of distance :math:`k - 1`.

**Cost.** Each reachable node is enqueued once (it is marked when
enqueued), and each adjacency list is scanned once:
:math:`O(V + E)` time, :math:`O(V)` memory.

Depth-First Search
------------------

.. code-block:: text

    DFS(G, u):
        mark u; emit u
        for v in neighbors(u):
            if v not marked: DFS(G, v)

.. mermaid::

   graph LR
       A((a)) -->|1| B((b))
       B -->|2| D((d))
       D -->|3| F((f))
       B -.->|back to b| E((e))
       E -->|5| C((c))

From ``a``: go to ``b``, then ``d``, then ``f``; ``f`` has no unvisited
neighbor, back up to ``d`` (none either), back to ``b``, go to ``e``,
then from ``e`` to ``c``. Order: a, b, d, f, e, c.

The library's ``dfs`` is iterative: it keeps a stack of *neighbor
iterators*, one per node on the current path. Resuming the iterator on top
of the stack is exactly what returning from a recursive call does, so the
order is that of the recursive definition, without Python's recursion
limit.

**Cost.** :math:`O(V + E)` time, :math:`O(V)` memory.

.. _guide_algorithms_shortest_paths:

Shortest Paths: Dijkstra
========================

Problem
-------

Given a graph with non-negative edge weights :math:`w(u, v) \ge 0` and a
source :math:`s`, find for every node :math:`v` the distance

.. math::

   \delta(s, v) = \min_{\text{paths } p : s \leadsto v} \sum_{(x, y) \in p} w(x, y)

Algorithm
---------

.. code-block:: text

    dist[s] <- 0; pred[s] <- None; push (0, s)
    while heap not empty:
        (d, u) <- pop min
        if u settled: continue
        settle u
        for each edge (u, v, w):
            if d + w < dist[v]:                 # relaxation
                dist[v] <- d + w; pred[v] <- u; push (dist[v], v)

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

.. list-table:: Nodes in the order they are settled
   :header-rows: 1
   :widths: 15 15 70

   * - Node
     - dist
     - Relaxations performed when settled
   * - s
     - 0
     - t ← 10, y ← 5
   * - y
     - 5
     - t ← 8 (was 10), x ← 14, z ← 7
   * - z
     - 7
     - x ← 13 (was 14)
   * - t
     - 8
     - x ← 9 (was 13)
   * - x
     - 9
     - —

Correctness
-----------

**Invariant.** When a node :math:`u` is settled, ``dist[u]`` equals
:math:`\delta(s, u)`.

*Proof.* Suppose :math:`u` is the first node settled with
``dist[u]`` :math:`> \delta(s, u)`. Take a shortest path from :math:`s` to
:math:`u` and let :math:`(x, y)` be its first edge leaving the settled set
(:math:`x` settled, :math:`y` not). By the choice of :math:`u`, :math:`x`
was settled with its true distance, and relaxing :math:`(x, y)` gave
:math:`\mathrm{dist}[y] = \delta(s, y)`. Weights are non-negative, so
:math:`\delta(s, y) \le \delta(s, u) < \mathrm{dist}[u]`: :math:`y` would
have been popped before :math:`u`, a contradiction.

The argument uses :math:`w \ge 0` exactly once, to say that the rest of
the path cannot decrease the distance. With negative weights it breaks,
which is why ``dijkstra()`` raises ``ValueError`` when it meets one.

Cost
----

Each edge is examined at most once from each endpoint, when that endpoint
is settled, pushing at most one heap entry; each heap operation costs
:math:`O(\log E) = O(\log V)`:

.. math::

   T = O\big((V + E) \log V\big)

This bound needs the outgoing edges of a node in :math:`O(\deg u)`, which
``outgoing_edges()`` provides; scanning every edge of the graph at each
step would cost :math:`O(V \cdot E)`.

.. _guide_algorithms_mst:

Minimum Spanning Trees: Kruskal
===============================

Problem
-------

A **spanning tree** of a connected undirected graph is a subset of
:math:`V - 1` edges connecting every node without a cycle. A **minimum
spanning tree** (MST) has the smallest total weight. On a graph with
:math:`C` connected components, one MST per component forms a **minimum
spanning forest** of :math:`V - C` edges; ``kruskal()`` returns that.

.. mermaid::

   graph LR
       A((a)) -- 4 --- B((b))
       A -- 8 --- H((h))
       B -. 8 .- C((c))
       B -. 11 .- H
       C -- 7 --- D((d))
       C -- 4 --- F((f))
       C -- 2 --- I((i))
       D -- 9 --- E((e))
       D -. 14 .- F
       E -. 10 .- F
       F -- 2 --- G((g))
       G -- 1 --- H
       G -. 6 .- I
       H -. 7 .- I

The classic example above (CLRS figure 23.1) has an MST of weight 37;
dotted edges are left out. Two edges weigh 8 (a–h and b–c) and either
completes a minimum tree; ``kruskal()`` keeps a–h because it was inserted
first and the edge sort is stable.

Algorithm
---------

.. code-block:: text

    F <- forest of the V nodes, no edge
    for (u, v, w) in edges sorted by w:        # stable sort
        if find(u) != find(v):                  # different trees
            add (u, v, w) to F; union(u, v)

A disjoint-set structure (:class:`sds.advanced.DisjointSet`) tracks which
tree each node belongs to, in near-constant amortized time per operation.

Correctness: the Cut Property
-----------------------------

**Cut property.** For any partition of the nodes into two groups
:math:`(S, V \setminus S)`, a lightest edge crossing the partition belongs
to some minimum spanning tree.

*Proof (exchange argument).* Let :math:`e` be a lightest crossing edge and
:math:`T` an MST without :math:`e`. Adding :math:`e` to :math:`T` closes a
cycle, which must cross the partition a second time through some edge
:math:`e'`. Then :math:`T' = T + e - e'` is a spanning tree and
:math:`w(T') = w(T) + w(e) - w(e') \le w(T)`, so :math:`T'` is also an MST,
and it contains :math:`e`.

When Kruskal adds an edge :math:`(u, v)`, take :math:`S` to be the tree
containing :math:`u`. No edge crossing this cut has been kept yet, and all
lighter edges have been examined already: :math:`(u, v)` is a lightest
crossing edge, safe by the cut property. Edges joining two nodes of the
same tree would close a cycle and are rightly skipped.

Cost
----

Sorting dominates:

.. math::

   T = O(E \log E) + O(E\, \alpha(V)) = O(E \log V)

since :math:`E \le V^2` gives :math:`\log E \le 2 \log V`, and
:math:`\alpha` (inverse Ackermann) is at most 4 for any practical size.

Summary
=======

.. list-table::
   :header-rows: 1
   :widths: 18 22 22 38

   * - Algorithm
     - Paradigm
     - Time
     - Requirement
   * - ``bfs``
     - graph search
     - :math:`O(V + E)`
     - any graph
   * - ``dfs``
     - graph search
     - :math:`O(V + E)`
     - any graph
   * - ``dijkstra``
     - greedy
     - :math:`O((V + E) \log V)`
     - non-negative weights
   * - ``kruskal``
     - greedy
     - :math:`O(E \log V)`
     - undirected weighted graph

References
==========

* CLRS, chapters 22 (BFS, DFS), 23 (minimum spanning trees) and 24
  (single-source shortest paths).
* OpenDSA, *Graph Traversals*, *Shortest-Paths Problems* and *Minimal
  Cost Spanning Trees* —
  https://opendsa-server.cs.vt.edu/ODSA/Books/Everything/html/GraphTraversal.html,
  https://opendsa-server.cs.vt.edu/ODSA/Books/Everything/html/GraphShortest.html,
  https://opendsa-server.cs.vt.edu/ODSA/Books/Everything/html/MCST.html
* J. Erickson, *Algorithms* (open-access), chapters 5–8 —
  https://jeffe.cs.illinois.edu/teaching/algorithms/
* R. Diestel, *Graph Theory* (free electronic edition) —
  https://diestel-graph-theory.com/
