.. _guide_advanced_disjoint_set:

===============================================
Disjoint Set (Union-Find) - Complete Guide
===============================================


Introduction
============

The Disjoint Set data structure, also known as **Union-Find** or **Merge-Find Set**,
is a fundamental structure for managing partitions of elements into disjoint subsets.
It efficiently supports two primary operations: uniting sets and finding which set
an element belongs to.

What is a Disjoint Set?
-----------------------

A disjoint set maintains a collection of **non-overlapping** (disjoint) sets:

.. math::

   \mathcal{F} = \{S_1, S_2, \ldots, S_k\}

Where:

* Each :math:`S_i` is a non-empty set
* :math:`S_i \cap S_j = \emptyset` for :math:`i \neq j` (disjoint property)
* :math:`\bigcup_{i=1}^{k} S_i = U` (covers all elements in universe U)

**Example Partition:**

.. code-block:: python

   U = {0, 1, 2, 3, 4, 5}
   
   # Initial: each element in its own set
   F0 = {{0}, {1}, {2}, {3}, {4}, {5}}
   
   # After union(0,1) and union(2,3):
   F1 = {{0,1}, {2,3}, {4}, {5}}
   
   # After union(1,2):
   F2 = {{0,1,2,3}, {4}, {5}}

Visual Representation
---------------------

.. mermaid::

   graph TB
       subgraph "Initial State - Singleton Sets"
           A0[0]
           A1[1]
           A2[2]
           A3[3]
           A4[4]
       end
       
       style A0 fill:#e1f5e1
       style A1 fill:#ffe1e1
       style A2 fill:#e1e1ff
       style A3 fill:#fff8dc
       style A4 fill:#ffe4e1

.. mermaid::

   graph TB
       subgraph "After Unions - Tree Forest"
           R0[0: root]
           C1[1]
           C2[2]
           R3[3: root]
           C4[4]
           
           R0 --> C1
           R0 --> C2
           R3 --> C4
       end
       
       style R0 fill:#90ee90
       style C1 fill:#e1f5e1
       style C2 fill:#e1f5e1
       style R3 fill:#ffb6b6
       style C4 fill:#ffe1e1

Why Use Disjoint Sets?
-----------------------

**Problem Domain:**

Disjoint sets excel at problems involving:

* **Dynamic Connectivity**: Track whether elements are connected
* **Equivalence Classes**: Group elements by equivalence relations
* **Network Components**: Find connected components in graphs
* **Image Segmentation**: Group similar pixels
* **Clustering**: Partition data by similarity

**Advantages:**

* Nearly constant time operations (α(n) ≈ O(1))
* Simple implementation
* Low memory overhead: O(n) space
* Efficient for large datasets

Mathematical Foundation
=======================

Set Theory Background
---------------------

**Partition Definition**

A partition :math:`\mathcal{P}` of set :math:`S` is a collection of subsets such that:

1. **Non-empty**: :math:`\forall P_i \in \mathcal{P}: P_i \neq \emptyset`
2. **Disjoint**: :math:`\forall P_i, P_j \in \mathcal{P}, i \neq j: P_i \cap P_j = \emptyset`
3. **Exhaustive**: :math:`\bigcup_{P \in \mathcal{P}} P = S`

**Equivalence Relations**

Partitions correspond to equivalence relations. A relation :math:`\sim` is an
equivalence relation if it is:

* **Reflexive**: :math:`\forall x: x \sim x`
* **Symmetric**: :math:`\forall x,y: x \sim y \Rightarrow y \sim x`
* **Transitive**: :math:`\forall x,y,z: (x \sim y) \wedge (y \sim z) \Rightarrow x \sim z`

.. code-block:: python

   from sds.advanced import DisjointSet
   
   # Equivalence relation: "same component"
   ds = DisjointSet()
   for i in range(5):
       ds.make_set(i)
   
   ds.union(0, 1)
   ds.union(1, 2)
   
   # Reflexive
   assert ds.connected(0, 0)  # True
   
   # Symmetric
   if ds.connected(0, 1):
       assert ds.connected(1, 0)  # True
   
   # Transitive
   if ds.connected(0, 1) and ds.connected(1, 2):
       assert ds.connected(0, 2)  # True

Operations & Invariants
-----------------------

**Core Operations:**

1. **make_set(x)**: Create singleton set :math:`\{x\}`

   .. math::
   
      \text{make\_set}(x): \mathcal{F} \rightarrow \mathcal{F} \cup \{\{x\}\}

2. **find(x)**: Return representative of set containing :math:`x`

   .. math::
   
      \text{find}(x) = r \text{ where } x \in S_r \in \mathcal{F}

3. **union(x, y)**: Merge sets containing :math:`x` and :math:`y`

   .. math::
   
      \text{union}(x,y): \mathcal{F} \setminus \{S_x, S_y\} \cup \{S_x \cup S_y\}

**Invariants:**

After any sequence of operations:

.. math::

   \forall x,y: \text{connected}(x,y) \Leftrightarrow \text{find}(x) = \text{find}(y)

.. math::

   |\mathcal{F}| + \sum_{i=1}^{m} [\text{union}_i \text{ merged}] = n

Where:
- :math:`n` = total elements
- :math:`m` = number of union operations
- :math:`[\cdot]` = Iverson bracket (1 if true, 0 if false)

Complexity Analysis
-------------------

**Without Optimizations:**

.. list-table::
   :header-rows: 1
   
   * - Operation
     - Worst Case
     - Amortized
   * - make_set
     - O(1)
     - O(1)
   * - find
     - O(n)
     - O(n)
   * - union
     - O(n)
     - O(n)

**With Path Compression + Union by Rank:**

.. list-table::
   :header-rows: 1
   
   * - Operation
     - Worst Case
     - Amortized
   * - make_set
     - O(1)
     - O(1)
   * - find
     - O(log n)
     - O(α(n))
   * - union
     - O(log n)
     - O(α(n))

Where :math:`\alpha(n)` is the **inverse Ackermann function**:

.. math::

   \alpha(n) = \min\{k: A_k(1) \geq n\}

**Practical Values:**

.. list-table::
   :header-rows: 1
   
   * - n
     - α(n)
     - Interpretation
   * - 10
     - 2
     - Very small
   * - 1,000
     - 3
     - Small
   * - 1,000,000
     - 4
     - Still small
   * - 10^80
     - ≤ 4
     - Effectively constant

.. note::
   For all practical purposes, :math:`\alpha(n) \leq 4`, making operations
   effectively constant time.

Implementation Details
======================

Forest Representation
---------------------

Disjoint sets are represented as a **forest of trees**:

* Each tree represents one set
* Root node represents the set
* Nodes point to their parent
* Root nodes point to themselves

.. mermaid::

   graph TB
       subgraph "Tree 1: {0,1,2,3}"
           R0[0: root<br/>size=4<br/>rank=2]
           N1[1: rank=0]
           N2[2: rank=1]
           N3[3: rank=0]
           
           R0 --> N1
           R0 --> N2
           N2 --> N3
       end
       
       subgraph "Tree 2: {4,5}"
           R4[4: root<br/>size=2<br/>rank=1]
           N5[5: rank=0]
           
           R4 --> N5
       end
       
       style R0 fill:#90ee90
       style R4 fill:#ffb6b6

**Data Structure:**

.. code-block:: python

   class DisjointSet:
       def __init__(self):
           self._parent = {}    # parent[x] = parent of x
           self._rank = {}      # rank[x] = upper bound on height
           self._set_size = {}  # set_size[root] = size of set
           self._num_sets = 0   # count of disjoint sets

Path Compression
----------------

**Problem**: Repeated find() operations traverse long chains.

**Solution**: Make all nodes on path point directly to root.

.. mermaid::

   graph LR
       subgraph "Before find(d)"
           A[a: root] --> B[b]
           B --> C[c]
           C --> D[d]
           
           style A fill:#90ee90
       end
       
       subgraph "After find(d)"
           A2[a: root]
           B2[b]
           C2[c]
           D2[d]
           
           A2 --> B2
           A2 --> C2
           A2 --> D2
           
           style A2 fill:#90ee90
       end

**Implementation:**

.. code-block:: python

   def find(self, element):
       """Find with path compression."""
       if element not in self._parent:
           raise ValueError(f"Element {element} not found")
       
       # Path compression: flatten tree
       if self._parent[element] != element:
           self._parent[element] = self.find(self._parent[element])
       
       return self._parent[element]

**Effect on Complexity:**

Without compression:

.. math::

   T_{\text{find}} = O(h) \text{ where } h = \text{tree height}

With compression:

.. math::

   T_{\text{find}} = O(\alpha(n)) \text{ amortized}

Union by Rank
-------------

**Problem**: Naive union creates unbalanced trees.

**Solution**: Always attach smaller tree under root of taller tree.

**Rank Definition:**

Rank is an upper bound on tree height:

.. math::

   \text{rank}(x) \leq \text{height}(x)

**Rules:**

1. New singleton: rank = 0
2. Union of different ranks: no change
3. Union of equal ranks: increase rank by 1

.. mermaid::

   graph TB
       subgraph "Union by Rank"
           subgraph "Tree A: rank=2"
               A[A: rank=2]
               A1[rank=1]
               A2[rank=0]
               A3[rank=0]
               
               A --> A1
               A --> A2
               A1 --> A3
           end
           
           subgraph "Tree B: rank=1"
               B[B: rank=1]
               B1[rank=0]
               
               B --> B1
           end
       end
       
       subgraph "After union(A, B)"
           R[A: rank=2]
           C1[rank=1]
           C2[rank=0]
           C3[rank=0]
           CB[B: rank=1]
           CB1[rank=0]
           
           R --> C1
           R --> C2
           R --> CB
           C1 --> C3
           CB --> CB1
       end
       
       style A fill:#90ee90
       style B fill:#ffb6b6
       style R fill:#90ee90

**Implementation:**

.. code-block:: python

   def union(self, x, y):
       """Union with union by rank."""
       root_x = self.find(x)
       root_y = self.find(y)
       
       if root_x == root_y:
           return False  # Already same set
       
       # Attach smaller rank tree under larger
       if self._rank[root_x] < self._rank[root_y]:
           self._parent[root_x] = root_y
           self._set_size[root_y] += self._set_size[root_x]
           del self._set_size[root_x]
       elif self._rank[root_x] > self._rank[root_y]:
           self._parent[root_y] = root_x
           self._set_size[root_x] += self._set_size[root_y]
           del self._set_size[root_y]
       else:
           # Equal rank: increase rank of new root
           self._parent[root_y] = root_x
           self._rank[root_x] += 1
           self._set_size[root_x] += self._set_size[root_y]
           del self._set_size[root_y]
       
       self._num_sets -= 1
       return True

**Theorem**: With union by rank alone:

.. math::

   \text{height}(T) \leq \log_2(n)

Proof sketch: A tree of rank :math:`k` has at least :math:`2^k` nodes.

Basic Usage
===========

Getting Started
---------------

.. code-block:: python

   from sds.advanced import DisjointSet
   
   # Create empty structure
   ds = DisjointSet()
   
   # Add elements
   for i in range(6):
       ds.make_set(i)
   
   print(ds)  # DisjointSet: 6 elements in 6 sets
   
   # Merge sets
   ds.union(0, 1)  # Merge {0} and {1} → {0,1}
   ds.union(2, 3)  # Merge {2} and {3} → {2,3}
   ds.union(4, 5)  # Merge {4} and {5} → {4,5}
   
   print(ds)  # DisjointSet: 6 elements in 3 sets
   
   # Query connectivity
   print(ds.connected(0, 1))  # True
   print(ds.connected(0, 2))  # False
   
   # Bridge components
   ds.union(1, 2)  # Merge {0,1} and {2,3} → {0,1,2,3}
   print(ds.connected(0, 3))  # True
   
   # Get all sets
   sets = ds.get_sets()
   for i, s in enumerate(sets):
       print(f"Component {i}: {sorted(s)}")
   
   # Output:
   # Component 0: [0, 1, 2, 3]
   # Component 1: [4, 5]

Common Operations
-----------------

**Creating Elements**

.. code-block:: python

   ds = DisjointSet()
   
   # Integers
   for i in range(10):
       ds.make_set(i)
   
   # Strings
   names = ['Alice', 'Bob', 'Carol', 'Dave']
   for name in names:
       ds.make_set(name)
   
   # Tuples (any hashable type)
   for i in range(3):
       for j in range(3):
           ds.make_set((i, j))

**Finding Representatives**

.. code-block:: python

   ds = DisjointSet()
   for i in range(5):
       ds.make_set(i)
   
   ds.union(0, 1)
   ds.union(1, 2)
   
   # All return same representative
   root = ds.find(0)
   assert ds.find(1) == root
   assert ds.find(2) == root

**Checking Connectivity**

.. code-block:: python

   # Direct check
   if ds.connected(x, y):
       print(f"{x} and {y} are in same set")
   
   # Equivalent to
   if ds.find(x) == ds.find(y):
       print(f"{x} and {y} are in same set")

**Component Analysis**

.. code-block:: python

   # Number of components
   num_components = ds.count_sets()
   
   # Size of a component
   component_size = ds.size(element)
   
   # All components
   components = ds.get_sets()
   
   # Largest component
   largest = max(components, key=len)
   print(f"Largest component: {len(largest)} elements")
   
   # Component size distribution
   sizes = sorted([len(s) for s in components], reverse=True)
   print(f"Component sizes: {sizes}")

Graph Algorithms
================

Connected Components
--------------------

**Problem**: Find all connected components in an undirected graph.

**Algorithm:**

1. Create singleton set for each vertex
2. For each edge (u, v): union(u, v)
3. Count remaining sets

.. code-block:: python

   from sds.advanced import DisjointSet
   from typing import List, Tuple
   
   def find_components(
       n: int,
       edges: List[Tuple[int, int]]
   ) -> List[List[int]]:
       """
       Find connected components.
       
       Parameters
       ----------
       n : int
           Number of vertices
       edges : List[Tuple[int, int]]
           List of edges
       
       Returns
       -------
       List[List[int]]
           List of components
       """
       ds = DisjointSet()
       
       # Initialize vertices
       for v in range(n):
           ds.make_set(v)
       
       # Process edges
       for u, v in edges:
           ds.union(u, v)
       
       # Extract components
       components = ds.get_sets()
       return [sorted(list(comp)) for comp in components]
   
   # Example
   n = 7
   edges = [(0,1), (1,2), (3,4), (5,6)]
   
   components = find_components(n, edges)
   print(f"Found {len(components)} components:")
   for i, comp in enumerate(components):
       print(f"  Component {i+1}: {comp}")
   
   # Output:
   # Found 3 components:
   #   Component 1: [0, 1, 2]
   #   Component 2: [3, 4]
   #   Component 3: [5, 6]

**Complexity:**

.. math::

   O(|V| \cdot \alpha(|V|) + |E| \cdot \alpha(|V|)) \approx O(|V| + |E|)

Cycle Detection
---------------

**Problem**: Determine if an undirected graph contains a cycle.

**Insight**: Adding edge (u, v) creates cycle iff u and v already connected.

.. code-block:: python

   def has_cycle(n: int, edges: List[Tuple[int, int]]) -> bool:
       """
       Detect cycle in undirected graph.
       
       Parameters
       ----------
       n : int
           Number of vertices
       edges : List[Tuple[int, int]]
           List of edges
       
       Returns
       -------
       bool
           True if graph contains cycle
       
       Examples
       --------
       >>> has_cycle(3, [(0,1), (1,2)])
       False
       
       >>> has_cycle(3, [(0,1), (1,2), (2,0)])
       True
       """
       ds = DisjointSet()
       
       for v in range(n):
           ds.make_set(v)
       
       for u, v in edges:
           if ds.connected(u, v):
               return True  # Edge creates cycle
           ds.union(u, v)
       
       return False
   
   # Test cases
   print(has_cycle(4, [(0,1), (1,2), (2,3)]))        # False (tree)
   print(has_cycle(4, [(0,1), (1,2), (2,3), (3,0)]))  # True (cycle)
   print(has_cycle(5, [(0,1), (2,3)]))               # False (forest)

**Complexity**: O((V + E) · α(V))

Minimum Spanning Tree (Kruskal's Algorithm)
--------------------------------------------

**Problem**: Find minimum spanning tree of weighted graph.

**Algorithm** (Kruskal, 1956):

1. Sort edges by weight
2. Initialize each vertex as singleton set
3. For each edge (u, v, w) in sorted order:
   - If u and v in different sets: add edge to MST, union(u, v)
4. Stop when MST has V-1 edges

.. code-block:: python

   from typing import List, Tuple
   
   def kruskal_mst(
       n: int,
       edges: List[Tuple[int, int, float]]
   ) -> Tuple[List[Tuple[int, int, float]], float]:
       """
       Find minimum spanning tree using Kruskal's algorithm.
       
       Parameters
       ----------
       n : int
           Number of vertices
       edges : List[Tuple[int, int, float]]
           List of (u, v, weight) tuples
       
       Returns
       -------
       Tuple[List[Tuple[int, int, float]], float]
           MST edges and total weight
       
       Examples
       --------
       >>> n = 4
       >>> edges = [(0,1,1), (1,2,2), (2,3,3), (0,3,4), (1,3,5)]
       >>> mst_edges, total_weight = kruskal_mst(n, edges)
       >>> total_weight
       6.0
       """
       ds = DisjointSet()
       
       # Initialize sets
       for v in range(n):
           ds.make_set(v)
       
       # Sort edges by weight
       sorted_edges = sorted(edges, key=lambda e: e[2])
       
       mst = []
       total_weight = 0.0
       
       for u, v, weight in sorted_edges:
           # Add edge if doesn't create cycle
           if not ds.connected(u, v):
               ds.union(u, v)
               mst.append((u, v, weight))
               total_weight += weight
               
               # MST complete
               if len(mst) == n - 1:
                   break
       
       return mst, total_weight
   
   # Example: Complete graph K4 with weights
   n = 4
   edges = [
       (0, 1, 1.0),
       (0, 2, 4.0),
       (0, 3, 3.0),
       (1, 2, 2.0),
       (1, 3, 5.0),
       (2, 3, 6.0)
   ]
   
   mst, weight = kruskal_mst(n, edges)
   
   print(f"MST edges:")
   for u, v, w in mst:
       print(f"  {u} -- {v}: {w}")
   print(f"Total weight: {weight}")
   
   # Output:
   # MST edges:
   #   0 -- 1: 1.0
   #   1 -- 2: 2.0
   #   0 -- 3: 3.0
   # Total weight: 6.0

**Correctness**: Greedy choice property + optimal substructure.

**Complexity**:

.. math::

   O(E \log E + E \cdot \alpha(V)) \approx O(E \log V)

Dynamic Connectivity
--------------------

**Problem**: Maintain connectivity as edges are added dynamically.

.. code-block:: python

   class DynamicConnectivity:
       """
       Track graph connectivity over time.
       
       Supports queries:
       - Are u and v connected?
       - How many components?
       - What's the size of u's component?
       """
       
       def __init__(self, n: int):
           self.ds = DisjointSet()
           for i in range(n):
               self.ds.make_set(i)
       
       def add_edge(self, u: int, v: int) -> bool:
           """
           Add edge between u and v.
           
           Returns
           -------
           bool
               True if edge connected two components
           """
           return self.ds.union(u, v)
       
       def is_connected(self, u: int, v: int) -> bool:
           """Check if u and v are connected."""
           return self.ds.connected(u, v)
       
       def num_components(self) -> int:
           """Get current number of components."""
           return self.ds.count_sets()
       
       def component_size(self, v: int) -> int:
           """Get size of component containing v."""
           return self.ds.size(v)
       
       def is_fully_connected(self) -> bool:
           """Check if graph is fully connected."""
           return self.ds.count_sets() == 1
   
   # Simulation
   dc = DynamicConnectivity(10)
   
   print(f"Initial components: {dc.num_components()}")  # 10
   
   # Add edges progressively
   edges = [
       (0, 1), (1, 2), (2, 3),
       (4, 5), (5, 6),
       (7, 8),
       (0, 4),  # Bridge
       (4, 7),  # Another bridge
       (3, 9)
   ]
   
   for u, v in edges:
       merged = dc.add_edge(u, v)
       if merged:
           print(f"Added edge ({u}, {v}): {dc.num_components()} components")
       
       if dc.is_fully_connected():
           print("Graph fully connected!")
           break

Advanced Applications
=====================

Least Common Ancestor (LCA)
----------------------------

**Problem**: Find LCA of nodes in a tree using offline algorithm.

**Tarjan's Algorithm**:

.. code-block:: python

   from typing import Dict, List, Set, Tuple
   
   class LCA_Solver:
       """
       Offline LCA using Tarjan's algorithm with Union-Find.
       
       Processes all queries after DFS traversal.
       """
       
       def __init__(self, tree: Dict[int, List[int]], root: int):
           self.tree = tree
           self.root = root
           self.ds = DisjointSet()
           self.ancestor = {}
           self.visited = set()
       
       def solve(self, queries: List[Tuple[int, int]]) -> Dict[Tuple[int, int], int]:
           """
           Find LCA for all query pairs.
           
           Parameters
           ----------
           queries : List[Tuple[int, int]]
               List of (u, v) pairs
           
           Returns
           -------
           Dict[Tuple[int, int], int]
               Mapping from query to LCA
           """
           # Initialize
           for node in self.tree:
               self.ds.make_set(node)
               self.ancestor[node] = node
           
           # Group queries by node
           query_map: Dict[int, List[Tuple[int, int]]] = {}
           for u, v in queries:
               if u not in query_map:
                   query_map[u] = []
               if v not in query_map:
                   query_map[v] = []
               query_map[u].append((u, v))
               query_map[v].append((v, u))
           
           # DFS with Union-Find
           results = {}
           self._dfs(self.root, query_map, results)
           
           return results
       
       def _dfs(self, u: int, query_map: Dict, results: Dict):
           """DFS traversal with LCA computation."""
           self.visited.add(u)
           
           # Process children
           for v in self.tree.get(u, []):
               if v not in self.visited:
                   self._dfs(v, query_map, results)
                   self.ds.union(u, v)
                   self.ancestor[self.ds.find(u)] = u
           
           # Answer queries involving u
           for node1, node2 in query_map.get(u, []):
               if node2 in self.visited:
                   lca = self.ancestor[self.ds.find(node2)]
                   results[(min(node1, node2), max(node1, node2))] = lca
   
   # Example tree
   tree = {
       0: [1, 2],
       1: [3, 4],
       2: [5, 6],
       3: [], 4: [], 5: [], 6: []
   }
   
   solver = LCA_Solver(tree, root=0)
   queries = [(3, 4), (3, 5), (4, 6)]
   results = solver.solve(queries)
   
   for (u, v), lca in results.items():
       print(f"LCA({u}, {v}) = {lca}")

Image Segmentation
------------------

**Problem**: Segment image into regions of similar color.

.. code-block:: python

   import numpy as np
   from typing import Tuple
   
   def segment_image(
       image: np.ndarray,
       threshold: float
   ) -> Tuple[np.ndarray, int]:
       """
       Segment image by color similarity.
       
       Parameters
       ----------
       image : np.ndarray
           Input image (H x W x 3)
       threshold : float
           Color difference threshold
       
       Returns
       -------
       Tuple[np.ndarray, int]
           Segmentation labels (H x W) and number of segments
       """
       h, w, channels = image.shape
       ds = DisjointSet()
       
       # Initialize pixels
       for i in range(h):
           for j in range(w):
               ds.make_set((i, j))
       
       # Merge similar neighbors
       for i in range(h):
           for j in range(w):
               current_color = image[i, j]
               
               # Check right neighbor
               if j + 1 < w:
                   neighbor_color = image[i, j+1]
                   diff = np.linalg.norm(current_color - neighbor_color)
                   if diff < threshold:
                       ds.union((i, j), (i, j+1))
               
               # Check bottom neighbor
               if i + 1 < h:
                   neighbor_color = image[i+1, j]
                   diff = np.linalg.norm(current_color - neighbor_color)
                   if diff < threshold:
                       ds.union((i, j), (i+1, j))
       
       # Create label map
       segments = ds.get_sets()
       labels = np.zeros((h, w), dtype=int)
       
       for label, segment in enumerate(segments):
           for i, j in segment:
               labels[i, j] = label
       
       return labels, len(segments)
   
   # Example usage
   image = np.random.rand(100, 100, 3) * 255
   labels, num_segments = segment_image(image, threshold=30.0)
   print(f"Segmented into {num_segments} regions")

Social Network Analysis
-----------------------

**Problem**: Identify communities in social networks.

.. code-block:: python

   class SocialNetwork:
       """
       Analyze social network communities using Union-Find.
       """
       
       def __init__(self):
           self.ds = DisjointSet()
           self.users = set()
       
       def add_user(self, user: str):
           """Add user to network."""
           if user not in self.users:
               self.ds.make_set(user)
               self.users.add(user)
       
       def add_friendship(self, user1: str, user2: str):
           """Create friendship (bidirectional connection)."""
           self.add_user(user1)
           self.add_user(user2)
           self.ds.union(user1, user2)
       
       def are_friends(self, user1: str, user2: str) -> bool:
           """Check if users are in same network."""
           return self.ds.connected(user1, user2)
       
       def get_community(self, user: str) -> Set[str]:
           """Get user's entire community."""
           communities = self.ds.get_sets()
           for community in communities:
               if user in community:
                   return community
           return set()
       
       def community_stats(self) -> Dict:
           """Compute community statistics."""
           communities = self.ds.get_sets()
           sizes = [len(c) for c in communities]
           
           return {
               'total_users': len(self.users),
               'num_communities': len(communities),
               'avg_community_size': sum(sizes) / len(sizes),
               'max_community_size': max(sizes),
               'min_community_size': min(sizes),
               'isolated_users': sum(1 for s in sizes if s == 1)
           }
       
       def suggest_bridges(self) -> List[Tuple[str, str]]:
           """Suggest friendships to bridge communities."""
           communities = list(self.ds.get_sets())
           suggestions = []
           
           # Suggest connecting largest communities
           if len(communities) >= 2:
               largest = sorted(communities, key=len, reverse=True)[:2]
               u1 = list(largest[0])[0]
               u2 = list(largest[1])[0]
               suggestions.append((u1, u2))
           
           return suggestions
   
   # Example
   network = SocialNetwork()
   
   friendships = [
       ('Alice', 'Bob'),
       ('Bob', 'Carol'),
       ('Dave', 'Eve'),
       ('Eve', 'Frank'),
       ('Grace', 'Henry'),
       ('Henry', 'Ivy'),
   ]
   
   for u, v in friendships:
       network.add_friendship(u, v)
   
   stats = network.community_stats()
   print("Network Statistics:")
   for key, value in stats.items():
       print(f"  {key}: {value}")
   
   # Find Alice's community
   alice_community = network.get_community('Alice')
   print(f"\nAlice's network: {sorted(alice_community)}")
   
   # Suggest bridges
   bridges = network.suggest_bridges()
   print(f"\nSuggested connections: {bridges}")

Equivalence Relations
---------------------

**Problem**: Track equivalence classes dynamically.

.. code-block:: python

   class EquivalenceTracker:
       """
       Track equivalence relations using Union-Find.
       
       Example: Variable aliasing in compilers.
       """
       
       def __init__(self):
           self.ds = DisjointSet()
       
       def declare_equivalent(self, x, y):
           """Declare x and y equivalent."""
           # Ensure both exist
           if x not in self.ds:
               self.ds.make_set(x)
           if y not in self.ds:
               self.ds.make_set(y)
           
           self.ds.union(x, y)
       
       def are_equivalent(self, x, y) -> bool:
           """Check if x and y are equivalent."""
           if x not in self.ds or y not in self.ds:
               return False
           return self.ds.connected(x, y)
       
       def get_equivalence_class(self, x) -> Set:
           """Get all elements equivalent to x."""
           classes = self.ds.get_sets()
           for cls in classes:
               if x in cls:
                   return cls
           return {x}
       
       def canonical(self, x):
           """Get canonical representative of x's class."""
           if x not in self.ds:
               self.ds.make_set(x)
           return self.ds.find(x)
   
   # Example: Variable aliasing
   tracker = EquivalenceTracker()
   
   # Declare equivalences
   tracker.declare_equivalent('x', 'y')
   tracker.declare_equivalent('y', 'z')
   tracker.declare_equivalent('a', 'b')
   
   # Query equivalence
   print(tracker.are_equivalent('x', 'z'))  # True (transitive)
   print(tracker.are_equivalent('x', 'a'))  # False
   
   # Get equivalence classes
   print(tracker.get_equivalence_class('x'))  # {'x', 'y', 'z'}
   print(tracker.get_equivalence_class('a'))  # {'a', 'b'}

Performance Optimization
========================

Benchmarking
------------

.. code-block:: python

   import time
   import random
   
   def benchmark_disjoint_set(n: int, operations: int):
       """Benchmark DisjointSet performance."""
       ds = DisjointSet()
       
       # Measure make_set
       start = time.perf_counter()
       for i in range(n):
           ds.make_set(i)
       make_set_time = time.perf_counter() - start
       
       # Measure union
       start = time.perf_counter()
       for _ in range(operations):
           u, v = random.sample(range(n), 2)
           ds.union(u, v)
       union_time = time.perf_counter() - start
       
       # Measure find
       start = time.perf_counter()
       for _ in range(operations):
           x = random.randint(0, n-1)
           ds.find(x)
       find_time = time.perf_counter() - start
       
       # Measure connected
       start = time.perf_counter()
       for _ in range(operations):
           u, v = random.sample(range(n), 2)
           ds.connected(u, v)
       connected_time = time.perf_counter() - start
       
       print(f"\nBenchmark Results (n={n}, ops={operations}):")
       print(f"  make_set: {make_set_time:.4f}s ({n/make_set_time:.0f} ops/s)")
       print(f"  union:    {union_time:.4f}s ({operations/union_time:.0f} ops/s)")
       print(f"  find:     {find_time:.4f}s ({operations/find_time:.0f} ops/s)")
       print(f"  connected: {connected_time:.4f}s ({operations/connected_time:.0f} ops/s)")
       print(f"  Final components: {ds.count_sets()}")
   
   # Run benchmarks
   benchmark_disjoint_set(n=10000, operations=50000)
   benchmark_disjoint_set(n=100000, operations=500000)

Memory Optimization
-------------------

**For Integer Elements:**

.. code-block:: python

   class CompactDisjointSet:
       """Memory-efficient DisjointSet for integers 0..n-1."""
       
       def __init__(self, n: int):
           self._parent = list(range(n))
           self._rank = [0] * n
           self._size = [1] * n
           self._num_sets = n
       
       def find(self, x: int) -> int:
           if self._parent[x] != x:
               self._parent[x] = self.find(self._parent[x])
           return self._parent[x]
       
       def union(self, x: int, y: int) -> bool:
           root_x = self.find(x)
           root_y = self.find(y)
           
           if root_x == root_y:
               return False
           
           if self._rank[root_x] < self._rank[root_y]:
               self._parent[root_x] = root_y
               self._size[root_y] += self._size[root_x]
           elif self._rank[root_x] > self._rank[root_y]:
               self._parent[root_y] = root_x
               self._size[root_x] += self._size[root_y]
           else:
               self._parent[root_y] = root_x
               self._rank[root_x] += 1
               self._size[root_x] += self._size[root_y]
           
           self._num_sets -= 1
           return True
   
   # ~40% memory savings for integer elements

Best Practices
==============

Do's and Don'ts
---------------

**✓ DO:**

.. code-block:: python

   # Initialize all elements first
   ds = DisjointSet()
   for elem in all_elements:
       ds.make_set(elem)
   
   # Check before operations
   if elem in ds:
       root = ds.find(elem)
   
   # Use connected() for queries
   if ds.connected(x, y):
       # Elements in same set
       pass

**✗ DON'T:**

.. code-block:: python

   # Don't union without make_set
   ds = DisjointSet()
   ds.union(1, 2)  # ValueError!
   
   # Don't assume elements exist
   root = ds.find(elem)  # Might raise ValueError
   
   # Don't modify returned sets
   sets = ds.get_sets()
   sets[0].add(new_elem)  # Doesn't affect DisjointSet

Common Pitfalls
---------------

**1. Forgetting Initialization**

.. code-block:: python

   # ❌ Wrong
   ds = DisjointSet()
   for u, v in edges:
       ds.union(u, v)  # ValueError if u, v not initialized
   
   # ✓ Correct
   ds = DisjointSet()
   for v in vertices:
       ds.make_set(v)
   for u, v in edges:
       ds.union(u, v)

**2. Incorrect Cycle Detection**

.. code-block:: python

   # ❌ Wrong: union before check
   ds = DisjointSet()
   for u, v in edges:
       ds.union(u, v)
       if ds.connected(u, v):  # Always True after union!
           return True
   
   # ✓ Correct: check before union
   ds = DisjointSet()
   for v in vertices:
       ds.make_set(v)
   for u, v in edges:
       if ds.connected(u, v):
           return True  # Cycle detected
       ds.union(u, v)

**3. Inefficient Repeated Queries**

.. code-block:: python

   # ❌ Inefficient: repeated size queries
   for elem in large_list:
       if ds.size(elem) > threshold:
           process(elem)
   
   # ✓ Better: cache root and size
   root = ds.find(elem)
   size = ds.size(root)
   for elem in large_list:
       if ds.find(elem) == root:
           process(elem)

Design Patterns
---------------

**Pattern 1: Pre-check Union**

.. code-block:: python

   # Check if union needed
   if not ds.connected(u, v):
       merged = ds.union(u, v)
       if merged:
           # Handle merge event
           update_component_data()

**Pattern 2: Batch Processing**

.. code-block:: python

   def batch_union(ds: DisjointSet, pairs: List[Tuple]):
       """Process multiple unions efficiently."""
       merged_count = 0
       for u, v in pairs:
           if ds.union(u, v):
               merged_count += 1
       return merged_count

**Pattern 3: Component Tracking**

.. code-block:: python

   class ComponentTracker:
       """Track additional component properties."""
       
       def __init__(self):
           self.ds = DisjointSet()
           self.metadata = {}  # root -> metadata
       
       def union(self, u, v):
           root_u = self.ds.find(u)
           root_v = self.ds.find(v)
           
           if self.ds.union(u, v):
               # Merge metadata
               new_root = self.ds.find(u)
               if new_root == root_u:
                   self.metadata[root_u].update(self.metadata[root_v])
                   del self.metadata[root_v]
               else:
                   self.metadata[root_v].update(self.metadata[root_u])
                   del self.metadata[root_u]

See Also
========

* :ref:`api_advanced_disjoint_set` - API Reference
* :ref:`api_advanced_interfaces` - Abstract interfaces
* :ref:`guide_algorithms_graph` - Graph algorithms
* :ref:`guide_algorithms_mst` - Spanning trees

References
==========

**Open Access Resources:**

.. [1] Galler, B. A., & Fisher, M. J. (1964). "An improved equivalence algorithm".
       *Communications of the ACM*, 7(5), 301-303.
       DOI: 10.1145/364099.364331
       
.. [2] Tarjan, R. E. (1975). "Efficiency of a Good But Not Linear Set Union Algorithm".
       *Journal of the ACM*, 22(2), 215-225.
       DOI: 10.1145/321879.321884
       
.. [3] Tarjan, R. E., & van Leeuwen, J. (1984). "Worst-case Analysis of Set Union
       Algorithms". *Journal of the ACM*, 31(2), 245-281.
       DOI: 10.1145/62.2160
       
.. [4] Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009).
       "Introduction to Algorithms" (3rd ed.). MIT Press.
       Chapter 21: Data Structures for Disjoint Sets.
       Available: https://mitpress.mit.edu/
       
.. [5] Galil, Z., & Italiano, G. F. (1991). "Data structures and algorithms
       for disjoint set union problems". *ACM Computing Surveys*, 23(3), 319-344.
       DOI: 10.1145/116873.116878
       
.. [6] Kruskal, J. B. (1956). "On the shortest spanning subtree of a graph
       and the traveling salesman problem". *Proceedings of the American
       Mathematical Society*, 7(1), 48-50.
       DOI: 10.2307/2033241

**Further Reading:**

* Sedgewick, R., & Wayne, K. (2011). "Algorithms" (4th ed.). Addison-Wesley.
  Section 1.5: Union-Find.
  
* Kleinberg, J., & Tardos, É. (2005). "Algorithm Design". Pearson.
  Chapter 4: Greedy Algorithms (Minimum Spanning Trees).
  
* NIST Dictionary of Algorithms and Data Structures.
  https://www.nist.gov/dads/
