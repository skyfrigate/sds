# SDS - Simple Data Structures

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Type Checked](https://img.shields.io/badge/type%20checked-mypy-informational)](http://mypy-lang.org/)
[![Code Style](https://img.shields.io/badge/code%20style-flake8-informational)](https://flake8.pycqa.org/)
[![Static Badge](https://img.shields.io/badge/security-bandit-informational)](https://github.com/PyCQA/bandit)


A comprehensive and educational Python library of fundamental data structures, implemented with object-oriented 
programming principles and extensive documentation.

## 🎯 Goals

- **Educational**: Clear and well-documented code for learning
- **Comprehensive**: Exhaustive coverage of classic data structures
- **Typed**: Full MyPy support with strict type hints
- **Tested**: Complete test coverage with pytest
- **Performant**: Using `__slots__` for memory optimization

## 📦 Installation

```bash
# Install from repository
pip install git+https://github.com/your-username/sds.git

# Install in development mode
git clone https://github.com/your-username/sds.git
cd sds
pip install -e .
```

## 🏗️ Architecture

The project is organized into thematic modules:

```
sds/
├── core/           # Fundamental components (abstract Node, interfaces, exceptions)
├── linear/         # Linear structures (lists, stacks, queues)
├── trees/          # Tree structures (binary trees, BST, AVL, heaps)
└── graphs/         # Graph structures (graphs, edges, algorithms)
```

## 📚 Available Structures

### 🔗 Nodes - `sds.core.node`

All node types inherit from a common abstract `Node` class using a unified reference system (`_refs`).

#### Linear nodes - `sds.linear.node`
- **`SimpleNode`**: Node for singly linked lists (`next` reference)
- **`DoublyNode`**: Node for doubly linked lists (`next` and `prev` references)

#### Tree nodes - `sds.trees.node`
- **`BinaryNode`**: Node for binary trees (`left` and `right` references)
- **`TreeNode`**: Node for general trees (list of `children`)

#### Graph nodes - `sds.graphs.node`
- **`GraphNode`**: Node for graphs (unique identifier, no internal references)

```python
from sds.linear.node import SimpleNode, DoublyNode
from sds.tree.node import BinaryNode, TreeNode
from sds.graph.node import GraphNode

# Singly linked list
node1 = SimpleNode(1)
node2 = SimpleNode(2)
node1.next = node2

# Binary tree
root = BinaryNode(10)
root.left = BinaryNode(5)
root.right = BinaryNode(15)

# Graph
node_a = GraphNode("A", "node_a")
node_b = GraphNode("B", "node_b")
```

### 📋 Linear Structures - `sds.linear`

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

```python
from sds.linear.list import LinkedList, DoublyLinkedList, CircularLinkedList

# Singly linked list
ll = LinkedList()
ll.append(1)
ll.append(2)
ll.prepend(0)
print(list(ll))  # [0, 1, 2]

# Doubly linked list
dll = DoublyLinkedList()
dll.append(1)
dll.append(2)
print(list(reversed(dll)))  # [2, 1]

# Circular linked list
cll = CircularLinkedList()
cll.append(1)
cll.append(2)
cll.append(3)
cll.rotate(1)
print(list(cll))  # [2, 3, 1]
```

#### Stack - `sds.linear.stack`
- **`Stack`**: LIFO (Last In First Out) stack
  - Operations: `push()`, `pop()`, `peek()`
  - All operations in O(1)
  - Uses `LinkedList` internally

```python
from sds.linear.stack import Stack

stack = Stack()
stack.push(1)
stack.push(2)
stack.push(3)
print(stack.pop())  # 3
print(stack.peek()) # 2
```

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

```python
from sds.linear.queue import Queue, Deque, PriorityQueue

# FIFO queue
queue = Queue()
queue.enqueue(1)
queue.enqueue(2)
print(queue.dequeue())  # 1

# Deque
deque = Deque()
deque.add_front(1)
deque.add_rear(2)
print(list(deque))  # [1, 2]

# Priority queue
pq = PriorityQueue()
pq.enqueue(5)
pq.enqueue(1)
pq.enqueue(3)
print(pq.dequeue())  # 1 (minimum priority)
```

### 🌳 Tree Structures - `sds.trees`

#### Basic Trees
- **`BinaryTree`**: Simple binary tree *(coming soon)*
  - Traversals: inorder, preorder, postorder, level-order
  - Operations: height, node count, search
- **`BinarySearchTree` (BST)**: Binary search tree *(coming soon)*
  - Property: left < parent < right
  - Search, insertion, deletion
  - O(log n) average, O(n) worst case
- **`GeneralTree`**: General (n-ary) tree *(coming soon)*
  - Variable number of children per node
  - DFS/BFS traversal

#### Balanced Trees
- **`AVLTree`**: Self-balancing AVL tree *(coming soon)*
  - Guaranteed O(log n) for all operations
  - Automatic rotations after insertion/deletion
- **`RedBlackTree`**: Red-Black tree *(coming soon)*
  - Self-balancing with color properties
  - Fewer rotations than AVL

#### Heaps
- **`MinHeap`**: Minimum heap *(coming soon)*
  - Parent ≤ children
  - Extract-min in O(log n)
- **`MaxHeap`**: Maximum heap *(coming soon)*
  - Parent ≥ children
  - Extract-max in O(log n)

#### Specialized Trees
- **`Trie`**: Prefix tree for strings *(coming soon)*
  - Auto-completion, prefix search
- **`SegmentTree`**: Segment tree *(coming soon)*
  - Efficient range queries
- **`BTree`**: B-tree for databases *(coming soon)*

### 🕸️ Graph Structures - `sds.graphs`

#### Nodes and Edges
- **`GraphNode`**: Graph node with unique identifier
- **`Edge`**: Edge between two nodes *(coming soon)*
- **`DirectedEdge`**: Directed arc *(coming soon)*
- **`WeightedEdge`**: Weighted edge *(coming soon)*

#### Graphs
- **`Graph`**: Basic graph *(coming soon)*
- **`DirectedGraph`**: Directed graph *(coming soon)*
- **`UndirectedGraph`**: Undirected graph *(coming soon)*
- **`WeightedGraph`**: Weighted graph *(coming soon)*

```python
from sds.graph.node import GraphNode

# Create nodes
node_a = GraphNode("A", "node_a")
node_b = GraphNode("B", "node_b")

# Connections will be managed by Edge and Graph
```

## 🧪 Testing

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
├── 01_core/        # Tests for core (abstract Node, interfaces, exceptions)
├── 02_linear/      # Tests for linear structures
├── 03_trees/       # Tests for tree structures
└── 04_graphs/      # Tests for graph structures
```

## 🔍 Static Analysis

The project is fully typed and verified with MyPy and Flake8:

```bash
# Type checking with MyPy (strict mode)
mypy --strict sds/

# Style checking with Flake8
flake8 sds/ --max-line-length=88

# Combined verification
mypy --strict sds/ && flake8 sds/ --max-line-length=88
```

## 📖 Documentation

The documentation uses NumPy format for docstrings and can be generated with Sphinx:

```bash
# Install documentation dependencies
pip install sphinx numpydoc sphinx-rtd-theme

# Generate documentation
cd docs
sphinx-build -b html . _build
```

## 🤝 Contributing

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

## 📋 Roadmap

### ✅ Phase 1: Foundations (Completed)
- [x] Modular architecture
- [x] Abstract nodes with unified `_refs` system
- [x] Nodes for lists (SimpleNode, DoublyNode)
- [x] Nodes for trees (BinaryNode, TreeNode)
- [x] Nodes for graphs (GraphNode)
- [x] Complete linear structures
- [x] Exhaustive tests for linear

### 🚧 Phase 2: Trees (In Progress)
- [ ] Abstract interfaces (AbstractTree, AbstractBinaryTree)
- [ ] BinaryTree and BinarySearchTree
- [ ] MinHeap and MaxHeap
- [ ] AVLTree
- [ ] RedBlackTree
- [ ] Trie
- [ ] Exhaustive tests for trees

### 📅 Phase 3: Graphs (Planned)
- [ ] Edge, DirectedEdge, WeightedEdge
- [ ] Graph, DirectedGraph, UndirectedGraph
- [ ] Algorithms: DFS, BFS, Dijkstra, Kruskal
- [ ] Exhaustive tests for graphs

### 🔮 Phase 4: Advanced Structures (Planned)
- [ ] Union-Find (Disjoint Set)
- [ ] Bloom Filter
- [ ] Skip List
- [ ] Segment Tree
- [ ] B-Tree

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE.md) file for details.

## 👥 Authors

- **Your Name** - *Initial work* - [your-github](https://github.com/your-username)

## 🙏 Acknowledgments

- Inspired by classic data structures courses
- Designed for learning and teaching
- Thanks to the Python community for exceptional tools (pytest, mypy, flake8)

## 📚 Resources

- [Python Documentation](https://docs.python.org/3/)
- [Type Hints PEP 484](https://www.python.org/dev/peps/pep-0484/)
- [NumPy Docstring Guide](https://numpydoc.readthedocs.io/en/latest/format.html)
- [Introduction to Algorithms (CLRS)](https://mitpress.mit.edu/books/introduction-algorithms-third-edition)

---

**Note**: This project is under active development. Features marked *(coming soon)* are planned but not yet implemented.