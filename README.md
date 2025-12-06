# SDS - Simple Data Structures

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Type Checked](https://img.shields.io/badge/type%20checked-mypy-informational)](http://mypy-lang.org/)
[![Code Style](https://img.shields.io/badge/code%20style-flake8-informational)](https://flake8.pycqa.org/)
[![Static Badge](https://img.shields.io/badge/security-bandit-informational)](https://github.com/PyCQA/bandit)


A comprehensive and educational Python library of fundamental data structures, implemented with object-oriented 
programming principles and extensive documentation.

## Goals

- **Educational**: Clear and well-documented code for learning
- **Comprehensive**: Exhaustive coverage of classic data structures
- **Typed**: Full MyPy support with strict type hints
- **Tested**: Complete test coverage with pytest
- **Performant**: Using `__slots__` for memory optimization

## Architecture

The project is organized into thematic modules:

```plaintext
sds/
├── core/           # Fundamental components (abstract Node, interfaces, exceptions)
├── linear/         # Linear structures (lists, stacks, queues)
├── trees/          # Tree structures (binary trees, BST, AVL, heaps)
└── graphs/         # Graph structures (graphs, edges, algorithms)
```

## Available Structures

### Nodes - `sds.core.node`

All node types inherit from a common abstract `Node` class using a unified reference system (`_refs`).

#### Linear nodes - `sds.linear.node`
- **`SimpleNode`**: Node for singly linked lists (`next` reference)
- **`DoublyNode`**: Node for doubly linked lists (`next` and `prev` references)

#### Tree nodes - `sds.trees.node`
- **`BinaryNode`**: Node for binary trees (`left` and `right` references)
- **`TreeNode`**: Node for general trees (list of `children`)

#### Graph nodes - `sds.graphs.node`
- **`GraphNode`**: Node for graphs (unique identifier, no internal references)


### Linear Structures - `sds.linear`

#### Linked Lists - `sds.linear.list`
- **`LinkedList`**: Singly linked list
  - Complexity: O(1) prepend, O(n) append, O(n) index access
  - Uses `SimpleNode`
- **`DoublyLinkedList`**: Doubly linked list
  - Complexity: O(1) prepend/append, O(n/2) optimized index access
  - Uses `DoublyNode`
  - Supports `__reversed__()` for reverse iteration
- **`CircularLinkedList`**: Circular linked list
  - `rotate()` method for O(1) rotation
  - Last node points to first

#### Stack - `sds.linear.stack`
- **`Stack`**: LIFO (Last In First Out) stack
  - Operations: `push()`, `pop()`, `peek()`
  - All operations in O(1)
  - Uses `LinkedList` internally

#### Queues - `sds.linear.queue`
- **`Queue`**: FIFO (First In First Out) queue
  - Operations: `enqueue()`, `dequeue()`, `front()`, `rear()`
  - Uses `LinkedList` internally
- **`Deque`**: Double-ended queue
  - Operations: `add_front()`, `add_rear()`, `remove_front()`, `remove_rear()`
  - All operations in O(1)
  - Uses `DoublyLinkedList` internally
- **`PriorityQueue`**: Priority queue
  - Element with minimum priority dequeued first
  - `enqueue()` in O(n), `dequeue()` in O(1)

### Tree Structures - `sds.trees`

#### Basic Trees
- **`BinaryTree`**: Simple binary tree
  - Traversals: inorder, preorder, postorder, level-order
  - Operations: height, node count, search
- **`BinarySearchTree` (BST)**: Binary search tree
  - Property: left < parent < right
  - Search, insertion, deletion
  - O(log n) average, O(n) worst case
- **`GeneralTree`**: General (n-ary) tree
  - Variable number of children per node
  - DFS/BFS traversal

#### Balanced Trees
- **`AVLTree`**: Self-balancing AVL tree
  - Guaranteed O(log n) for all operations
  - Automatic rotations after insertion/deletion
- **`RedBlackTree`**: Red-Black tree
  - Self-balancing with color properties
  - Fewer rotations than AVL

#### Heaps
- **`MinHeap`**: Minimum heap
  - Parent ≤ children
  - Extract-min in O(log n)
- **`MaxHeap`**: Maximum heap
  - Parent ≥ children
  - Extract-max in O(log n)

#### Specialized Trees
- **`Trie`**: Prefix tree for strings
  - Auto-completion, prefix search
- **`SegmentTree`**: Segment tree
  - Efficient range queries
- **`BTree`**: B-tree for databases

### Graph structures - `sds.graphs`

#### Nodes and edges
- **`GraphNode`**: Graph node with unique identifier
- **`Edge`**: Edge between two nodes *(coming soon)*
- **`DirectedEdge`**: Directed edge *(coming soon)*
- **`WeightedEdge`**: Weighted edge *(coming soon)*

#### Graphs
- **`Graph`**: Basic graph *(coming soon)*
- **`DirectedGraph`**: Directed graph *(coming soon)*
- **`UndirectedGraph`**: Undirected graph *(coming soon)*
- **`WeightedGraph`**: Weighted graph *(coming soon)*

Translated with DeepL.com (free version)

## Testing

The project uses pytest with complete test coverage:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=sds --cov-report=html

# Run tests for a specific module
pytest tests/02_linear/

# Run in verbose mode
pytest -v
```

Test structure:
```
tests/
├── 01_Core/        # Tests for core (abstract Node, interfaces, exceptions)
├── 02_Linear/      # Tests for linear structures
├── 03_Tree/       # Tests for tree structures
└── 04_Graph/      # Tests for graph structures
```

## Static Analysis

The project is fully typed and verified with MyPy and Flake8:

```bash
# Type checking with MyPy (strict mode)
mypy --strict sds/

# Style checking with Flake8
flake8 sds/ --max-line-length=88

# Combined verification
mypy --strict sds/ && flake8 sds/ --max-line-length=88
```

## Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork** the project
2. Create a **branch** for your feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. Open a **Pull Request**

### Quality Standards

- ✅ Type-checked code with MyPy (strict mode)
- ✅ Style compliant with Flake8 (PEP 8)
- ✅ Tests with pytest (coverage > 90%)
- ✅ NumPy format docstrings
- ✅ Use of `__slots__` for memory optimization

## Roadmap

### Phase 1: Foundations (Completed)
- [x] Modular architecture
- [x] Abstract nodes with unified `_refs` system
- [x] Nodes for lists (SimpleNode, DoublyNode)
- [x] Nodes for trees (BinaryNode, TreeNode)
- [x] Nodes for graphs (GraphNode)
- [x] Complete linear structures
- [x] Exhaustive tests for linear

### Phase 2: Trees (Completed)
- [x] Abstract interfaces (AbstractTree, AbstractBinaryTree)
- [x] BinaryTree and BinarySearchTree
- [x] B-Tree
- [x] MinHeap and MaxHeap
- [x] AVLTree
- [x] RedBlackTree
- [x] Trie
- [x] Segment Tree
- [x] Exhaustive tests for trees

### Phase 3: Graphs (Planned)
- [ ] Edge, DirectedEdge, WeightedEdge
- [ ] Graph, DirectedGraph, UndirectedGraph
- [ ] Algorithms: DFS, BFS, Dijkstra, Kruskal
- [ ] Exhaustive tests for graphs

### Phase 4: Advanced Structures (Planned)
- [ ] Union-Find (Disjoint Set)
- [ ] Bloom Filter
- [ ] Skip List

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE.md) file for details.

## Acknowledgments

- Inspired by classic data structures courses
- Designed for learning and teaching
- Thanks to the Python community for exceptional tools ([pytest](https://docs.pytest.org/en/stable/), 
  [mypy](https://mypy-lang.org/), [flake8](https://flake8.pycqa.org/en/latest/), 
  [bandit](https://bandit.readthedocs.io/en/latest/))

## Resources

- [Python Documentation](https://docs.python.org/3/)
- [Type Hints PEP 484](https://www.python.org/dev/peps/pep-0484/)
- [NumPy Docstring Guide](https://numpydoc.readthedocs.io/en/latest/format.html)

---

**Note**: This project is under development. Features marked *(coming soon)* are planned but not yet implemented.