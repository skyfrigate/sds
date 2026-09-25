# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Versions 0.1.0 to 0.5.0 were internal development milestones: they were
neither tagged nor published. 0.6.0 is the first release published on PyPI
(as `pysds-tools`) and ReadTheDocs.

## [Unreleased]

Work towards 0.7.0 — Algorithms.

### Added

- `sds.algorithms` package, holding the algorithmic logic kept out of the
  structure classes.
- `sds.algorithms.sorting`: `merge_sort()` (stable, returns a new list) and
  `quick_sort()` (in place, not stable). Both take `key` and `reverse` like
  `sorted()` and operate on Python lists only.
- `sds.algorithms.tree_algorithms`: `inorder()`, `preorder()`, `postorder()`
  and `level_order()`, taking any binary tree as argument. The depth-first
  traversals are iterative and handle trees deeper than the recursion limit.
- `sds.algorithms.tree_algorithms`: `is_balanced()` (AVL criterion, any binary
  tree) and `rebalance()` (rebuilds a `BinarySearchTree` to minimum height,
  in place).
- `sds.algorithms.graph_algorithms`: `bfs()` and `dfs()`, iterative and
  lazy, on any graph; `dijkstra()`, shortest distances and paths on weighted
  graphs with non-negative weights; `kruskal()`, minimum spanning forest of
  an undirected weighted graph.
- `sds.algorithms.probabilistic_algorithms`: `variable_elimination()`, the
  exact distribution of query variables given evidence, on Bayesian networks
  and Markov random fields.
- `sds.algorithms.probabilistic_algorithms`: `belief_propagation()`, every
  marginal at once by sum-product message passing (exact on tree-shaped
  models, approximate with a warning on loopy ones).
- `sds.algorithms.probabilistic_algorithms`: `forward()` (log-likelihood and
  filtered states) and `viterbi()` (most likely state path) for hidden Markov
  models.
- API reference and user guide for `sds.algorithms`, including a page on
  design paradigms (divide and conquer, greedy, dynamic programming).
- `AbstractBinaryTree.children(node)`: the real `(left, right)` children of a
  node, `None` where absent (the Red-Black `NIL` sentinel is never exposed).
- `AbstractWeightedGraph.outgoing_edges(node)`: a node's outgoing weighted
  edges in O(degree), implemented by `WeightedGraph` and
  `WeightedDirectedGraph`.
- `sds.linear.to_list()` and `sds.linear.from_list()`: conversion between
  Python lists and any linear structure.

### Changed

- Graph `neighbors()`, `successors()` and `predecessors()` now yield nodes in
  edge-insertion order instead of an order that varied with `PYTHONHASHSEED`.
  Removing the last edge to a neighbor and adding it again moves that
  neighbor to the end.

### Deprecated

- `AbstractBinaryTree.inorder_traversal()`, `preorder_traversal()`,
  `postorder_traversal()` and `level_order_traversal()` (and their overrides
  in `BinaryTree`, `BinarySearchTree`, `AVLTree` and `RedBlackTree`): use the
  matching functions of `sds.algorithms.tree_algorithms`, which take the tree
  as argument, e.g. `inorder(tree)`. The methods emit a `DeprecationWarning`
  and will be removed in 1.0.0. Iterating over a tree (`for x in tree`) is
  unaffected.

### Fixed

- The package now ships a `py.typed` marker (PEP 561), so type checkers use
  its inline annotations, as the `Typing :: Typed` classifier already
  claimed.

## [0.6.0] - 2026-08-05

First published release.

### Added

- `sds.probabilistic` module for probabilistic graphical models:
  - `RandomVariable` and `Factor` building blocks;
  - `AbstractGraphicalModel`, `AbstractBayesianNetwork` and
    `AbstractMarkovRandomField` interfaces, with `factors_for(variable)` to
    collect every factor referencing a variable;
  - `BayesianNetwork` and `MarkovRandomField`, whose topology is carried by
    `sds.graph.DirectedGraph` and `sds.graph.Graph` respectively;
  - `AbstractHiddenMarkovModel` and `HiddenMarkovModel`, with a derived
    `previous_states()` variable for the transition model.
- API reference and user guide for the probabilistic module.
- Distribution on PyPI as `pysds-tools` (the importable package stays `sds`)
  and documentation on ReadTheDocs.

### Fixed

- Documentation build on ReadTheDocs: the `furo` theme was missing from the
  documentation requirements.

## 0.5.0 - 2026-06-05

Internal milestone, not published.

### Added

- `sds.advanced` module for deterministic structures outside the
  linear/tree/graph families:
  - `DisjointSet` (union-find with path compression and union by rank);
  - `BloomFilter` and `CountMinSketch`;
  - `SkipList`;
  - `HashTableChaining` and `HashTableOpenAddressing`;
  - `LRUCache`;
  - `FenwickTree`;
  - the matching abstract interfaces.
- API reference and user guide for the advanced module.

## 0.4.0 - 2025-12-12

Internal milestone, not published.

### Added

- `sds.graph` module:
  - `GraphNode`, `Edge`, `DirectedEdge`, `WeightedEdge`,
    `WeightedDirectedEdge`;
  - `Graph`, `UndirectedGraph` (rejects directed edges), `DirectedGraph`
    (in/out degree, predecessors, successors, acyclicity);
  - `WeightedGraph` and `WeightedDirectedGraph`, with a cached
    `total_weight()`;
  - `AdjacencyListGraph` and `AdjacencyMatrixGraph`;
  - `AbstractGraph`, `AbstractDirectedGraph`, `AbstractUndirectedGraph` and
    `AbstractWeightedGraph` interfaces.
- API reference and user guide for the graph module.

### Changed

- Documentation theme switched from `sphinx_rtd_theme` to Furo.

## 0.3.0 - 2025-12-06

Internal milestone, not published.

### Added

- `sds.tree` module:
  - `BinaryTree`, `BinarySearchTree`, `AVLTree` and `RedBlackTree`;
  - general `Tree`;
  - `MinHeap`, `MaxHeap` and `HeapPriorityQueue`;
  - `BTree`, `Trie` and `SegmentTree`;
  - the matching node classes and abstract interfaces.
- API reference and user guide for the tree module.

## 0.2.0 - 2025-12-06

Internal milestone, not published.

### Added

- `sds.linear` module: `LinkedList`, `DoublyLinkedList`,
  `CircularLinkedList`, `Stack`, `Queue`, `Deque` and `PriorityQueue`, with
  `SimpleNode` and `DoublyNode`.
- API reference and user guide for the linear module.

## 0.1.0 - 2025-11-23

Internal milestone, not published.

### Added

- `sds.core` module: `Collection` and `LinearCollection` interfaces, the
  `Node` base class, and the exception hierarchy rooted at
  `DataStructureError` (`EmptyStructureError`, `FullStructureError`,
  `InvalidOperationError`, `IndexStructureError`).
- Project tooling: single `pyproject.toml`, pytest with coverage, mypy in
  strict mode, GitHub Actions CI, Sphinx documentation.

[Unreleased]: https://github.com/skyfrigate/sds/compare/v0.6.0...HEAD
[0.6.0]: https://github.com/skyfrigate/sds/releases/tag/v0.6.0
