# SDS Tools - Simple Data Structures

[![PyPI version](https://img.shields.io/pypi/v/pysds-tools.svg)](https://pypi.org/project/pysds-tools/)
[![Documentation](https://readthedocs.org/projects/pysds-tools/badge/?version=latest)](https://pysds-tools.readthedocs.io/en/latest/?badge=latest)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Type Checked](https://img.shields.io/badge/type%20checked-mypy-informational)](http://mypy-lang.org/)
[![Code Style](https://img.shields.io/badge/code%20style-flake8-informational)](https://flake8.pycqa.org/)
[![Static Badge](https://img.shields.io/badge/security-bandit-informational)](https://github.com/PyCQA/bandit)

A comprehensive and educational Python library of fundamental data structures — from
linked lists to probabilistic graphical models — implemented with object-oriented
programming principles and extensive academic-style documentation.

> **Package name note**: the PyPI/pip distribution is named **`pysds-tools`**
> (`sds-tools` collides with an existing, unrelated package once PyPI normalizes
> names). The importable module is unaffected — it's still `sds`
> (`import sds.linear`, `import sds.probabilistic`, ...).

## Goals

- **Educational**: Clear, well-documented code for learning — not just working
  code, but code that explains *why*
- **Comprehensive**: Exhaustive coverage of classic and advanced data structures
- **Typed**: Full MyPy strict-mode support, pyright/basedpyright compatible
- **Tested**: 80–90%+ coverage target per module, enforced via pytest-cov
- **Performant**: `__slots__` on every node and structure class

## Installation

```bash
pip install pysds-tools
```

## Quick Start

```python
from sds.linear import Stack
from sds.graph import DirectedGraph, GraphNode, DirectedEdge
from sds.probabilistic import BayesianNetwork, Factor, RandomVariable

# Linear structures
stack = Stack()
stack.push(1)
stack.push(2)
stack.pop()  # 2

# Graphs
task_graph = DirectedGraph()
design, backend = GraphNode("Design"), GraphNode("Backend")
task_graph.add_node(design)
task_graph.add_node(backend)
task_graph.add_edge(DirectedEdge(design, backend))
task_graph.is_acyclic()  # True

# Probabilistic graphical models
rain = RandomVariable("Rain", ("true", "false"))
bn = BayesianNetwork()
bn.add_variable(rain)
bn.set_cpt(rain, Factor((rain,), {("true",): 0.2, ("false",): 0.8}))
```

## Architecture

The project is organized into thematic modules, one per family of structures:

```plaintext
src/sds/
├── core/           # Foundations: AbstractNode, AbstractContainer, exceptions
├── linear/         # Linear structures (linked list, stack, queue)
├── tree/           # Tree structures (binary, AVL, heaps, B-tree, trie, segment tree)
├── graph/          # Graph structures (directed, weighted, adjacency representations)
├── advanced/       # Deterministic advanced structures (disjoint set, Bloom filter, ...)
├── probabilistic/  # Probabilistic graphical models (Bayesian networks, MRF, HMM)
├── algorithms/      # (planned) sorting, graph algorithms, tree traversals, inference
└── utils/          # (planned) visualizer, extended exceptions
```

## Available Structures

### `sds.core` — Foundations

Base abstractions shared by every other module: `AbstractNode`,
`AbstractContainer`, and the common exception hierarchy. Contains no concrete
data structure by design — every other module imports from here, never the
reverse.

### `sds.linear` — Linear Structures

- **`LinkedList`**: doubly linked list — O(1) prepend/append
- **`Stack`**: LIFO — `push()`, `pop()`, `peek()`, all O(1)
- **`Queue`**: FIFO — `enqueue()`, `dequeue()`, all O(1)

### `sds.tree` — Tree Structures

- **`BinaryTree`**, **`AVLTree`** (self-balancing, guaranteed O(log n)),
  **`GeneralTree`** (n-ary)
- **`MinHeap`**, **`MaxHeap`**
- **`BTree`**, **`Trie`** (prefix search), **`SegmentTree`** (range queries)

### `sds.graph` — Graph Structures

- **`Graph`**, **`DirectedGraph`**, **`UndirectedGraph`** (strict wrapper —
  rejects directed edges explicitly rather than silently converting them)
- **`WeightedGraph`**, **`WeightedDirectedGraph`**
- **`AdjacencyListGraph`** (sparse, O(V+E) space), **`AdjacencyMatrixGraph`**
  (dense, O(1) edge lookup)

### `sds.advanced` — Advanced Structures

Deterministic structures that don't fit cleanly into linear/tree/graph:

- **`DisjointSet`** (Union-Find, path compression + union-by-rank — O(α(n)) amortized)
- **`BloomFilter`** (probabilistic set membership), **`SkipList`** (probabilistic sorted structure)
- **`HashTableChaining`**, **`HashTableOpenAddressing`**
- **`LRUCache`**, **`FenwickTree`** (binary indexed tree), **`CountMinSketch`**
  (frequency estimation over streams)

### `sds.probabilistic` — Probabilistic Graphical Models

Structures encoding probability distributions over discrete random variables.
No inference logic (marginal queries, most-likely-explanation) is implemented
here — that's planned for `sds.algorithms`.

- **`RandomVariable`**, **`Factor`**: shared building blocks (a discrete
  variable and a potential/CPT table over a scope of variables)
- **`BayesianNetwork`**: directed acyclic graphical model with locally
  normalized CPTs, composes `sds.graph.DirectedGraph` for topology
- **`MarkovRandomField`**: undirected graphical model (cycles allowed) with
  unnormalized potentials, composes `sds.graph.Graph`
- **`HiddenMarkovModel`**: sequential model over a fixed states/observations
  pair, with initial/transition/emission components

## Documentation

Full API reference and user guide, including mathematical foundations, Mermaid
diagrams, complexity tables, and real-world examples for every module:

**https://pysds-tools.readthedocs.io**

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=sds --cov-report=html

# Run tests for a specific module
pytest tests/06_Probabilistic/

# Run in verbose mode
pytest -v
```

Test suite layout (mirrors the source tree, one directory per module):

```plaintext
tests/
├── 01_Core/
├── 02_Linear/
├── 03_Tree/
├── 04_Graph/
├── 05_Advanced/
└── 06_Probabilistic/
```

## Static Analysis

The project is fully typed and verified with mypy, flake8, and bandit:

```bash
mypy src/sds/
flake8 src/sds/
bandit -r src/sds/
```

Or, via `tox`:

```bash
tox -e mypy,flake8,bandit
```

## Contributing

Contributions are welcome!

1. **Fork** the project
2. Create a **branch** for your feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes following [Conventional Commits](https://www.conventionalcommits.org/)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. Open a **Pull Request**

Full project conventions (labels, issue templates, commit format, versioning,
releases) are documented in
[`CONVENTIONS.md`](https://github.com/skyfrigate/.github/blob/main/CONVENTIONS.md)
in the shared `.github` repository.

### Quality Standards

- ✅ Type-checked with mypy (strict mode)
- ✅ Style-compliant with flake8
- ✅ Security-checked with bandit
- ✅ Tests with pytest (80–90%+ coverage target)
- ✅ NumPy-style docstrings
- ✅ `__slots__` on all node and structure classes

## Roadmap

### `v0.1.0`–`v0.5.0` — Foundations through Advanced Structures ✅ *Completed*

- `sds.core`, `sds.linear`, `sds.tree`, `sds.graph`, `sds.advanced` — fully
  implemented, tested, and documented

### `v0.6.0` — Probabilistic Structures ✅ *Completed (this release)*

- `sds.probabilistic`: `BayesianNetwork`, `MarkovRandomField`, `HiddenMarkovModel`

### `v0.7.0` — Algorithms *Planned*

- Sorting (QuickSort, MergeSort), graph algorithms (DFS, BFS, Dijkstra,
  Kruskal), tree traversals — and probabilistic inference (Variable
  Elimination, Belief Propagation, Forward, Viterbi)

### `v0.8.0` — Utilities *Planned*

- Shared visualizer, extended exception hierarchy

### `v0.9.0`–`v1.0.0` — Quality Consolidation & Stable Release *Planned*

- Full coverage/mypy sweep, documentation polish, first stable API

### `v1.1.0`–`v1.2.0` — French Translation *Planned*

- Bilingual documentation via a dedicated ReadTheDocs project

## License

This project is licensed under the Apache License 2.0 — see the
[LICENSE](LICENSE.md) file for details. Documentation is licensed separately
under CC BY-NC 4.0 — see [`docs/source/license.rst`](docs/source/license.rst).

## Acknowledgments

- Inspired by classic data structures and algorithms courses
- Designed for learning
- Thanks to the Python community for exceptional tools
  ([pytest](https://docs.pytest.org/en/stable/),
  [mypy](https://mypy-lang.org/), [flake8](https://flake8.pycqa.org/en/latest/),
  [bandit](https://bandit.readthedocs.io/en/latest/), [Sphinx](https://www.sphinx-doc.org/),
  [Furo](https://pradyunsg.me/furo/))

## Resources

- [Python Documentation](https://docs.python.org/3/)
- [Type Hints — PEP 484](https://www.python.org/dev/peps/pep-0484/)
- [NumPy Docstring Guide](https://numpydoc.readthedocs.io/en/latest/format.html)
- [Probabilistic Graphical Models — Stanford CS228 notes](https://ermongroup.github.io/cs228-notes/)
  (open-access reference for `sds.probabilistic`)

---

**GitLab mirror**: https://gitlab.com/open-works/sds
