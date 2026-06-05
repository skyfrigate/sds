.. _api_advanced_disjoint_set:

============
Disjoint Set
============

.. currentmodule:: sds.advanced.disjoint_set

The Disjoint Set (also known as Union-Find) is a data structure that efficiently
tracks partitions of elements into disjoint sets, supporting fast union and
connectivity queries.


Overview
========

The Disjoint Set maintains a forest of trees where each tree represents a distinct
set. With path compression and union by rank optimizations, operations achieve
nearly constant amortized time complexity.

Key Features
------------

* **Path Compression**: Flattens tree structure during queries
* **Union by Rank**: Keeps trees balanced during merges
* **Nearly O(1) Operations**: α(n) amortized complexity
* **Space Efficient**: O(n) space for n elements

Performance Characteristics
---------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Operation
     - Complexity
     - Notes
   * - make_set(x)
     - O(1)
     - Creates singleton set
   * - find(x)
     - O(α(n))
     - With path compression
   * - union(x, y)
     - O(α(n))
     - With union by rank
   * - connected(x, y)
     - O(α(n))
     - Equivalent to find
   * - size(x)
     - O(α(n))
     - Cached for roots
   * - count_sets()
     - O(1)
     - Maintained counter
   * - get_sets()
     - O(n)
     - Full traversal needed

.. note::
   α(n) is the inverse Ackermann function, which grows so slowly that
   α(n) ≤ 4 for all practical values of n (n < 10^80). Thus, operations
   are effectively constant time.

Visual Representation
=====================

**Initial State (Singleton Sets)**

.. mermaid::

   graph TB
       subgraph "Element 0"
           A0[0]
       end
       
       subgraph "Element 1"
           A1[1]
       end
       
       subgraph "Element 2"
           A2[2]
       end
       
       subgraph "Element 3"
           A3[3]
       end
       
       subgraph "Element 4"
           A4[4]
       end
       
       style A0 fill:#e1f5e1
       style A1 fill:#e1f5e1
       style A2 fill:#ffe1e1
       style A3 fill:#ffe1e1
       style A4 fill:#e1e1ff

**After union(0,1), union(2,3)**

.. mermaid::

   graph TB
       subgraph "Set 1"
           A0[0: rank=1]
           A1[1: rank=0]
           A0 --> A1
       end
       
       subgraph "Set 2"
           A2[2: rank=1]
           A3[3: rank=0]
           A2 --> A3
       end
       
       subgraph "Set 3"
           A4[4: rank=0]
       end
       
       style A0 fill:#90ee90
       style A1 fill:#e1f5e1
       style A2 fill:#ffb6b6
       style A3 fill:#ffe1e1
       style A4 fill:#b6b6ff

**After union(1,2) - Union by Rank**

.. mermaid::

   graph TB
       subgraph "Merged Set"
           A0[0: rank=1]
           A1[1: rank=0]
           A2[2: rank=1]
           A3[3: rank=0]
           
           A0 --> A1
           A0 --> A2
           A2 --> A3
       end
       
       subgraph "Set 2"
           A4[4: rank=0]
       end
       
       style A0 fill:#90ee90
       style A1 fill:#c8e6c9
       style A2 fill:#c8e6c9
       style A3 fill:#e1f5e1
       style A4 fill:#b6b6ff

**Path Compression Effect**

.. mermaid::

   graph LR
       subgraph "Before find(3)"
           B0[0: root]
           B1[1]
           B2[2]
           B3[3]
           
           B0 --> B1
           B1 --> B2
           B2 --> B3
       end
       
       subgraph "After find(3)"
           A0[0: root]
           A1[1]
           A2[2]
           A3[3]
           
           A0 --> A1
           A0 --> A2
           A0 --> A3
       end
       
       style B0 fill:#90ee90
       style A0 fill:#90ee90

Classes
=======

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   DisjointSet


Detailed API
============

Constructor
-----------

.. automethod:: DisjointSet.__init__

   Creates an empty disjoint set structure.
   
   **Example:**
   
   .. code-block:: python
   
      from sds.advanced import DisjointSet
      
      ds = DisjointSet()
      print(ds)  # DisjointSet: 0 elements in 0 sets

Properties
----------

.. autoproperty:: DisjointSet.num_sets

   Returns the current number of disjoint sets.
   
   **Example:**
   
   .. code-block:: python
   
      ds = DisjointSet()
      for i in range(5):
          ds.make_set(i)
      
      print(ds.num_sets)  # 5
      ds.union(0, 1)
      print(ds.num_sets)  # 4

Set Creation
------------

.. automethod:: DisjointSet.make_set

   **Error Handling:**
   
   .. code-block:: python
   
      ds = DisjointSet()
      ds.make_set(1)
      
      # Duplicate element
      try:
          ds.make_set(1)
      except ValueError as e:
          print(e)  # Element 1 already exists in a set
      
      # Non-hashable element
      try:
          ds.make_set([1, 2, 3])
      except TypeError as e:
          print(e)  # Element must be hashable

Find Operations
---------------

.. automethod:: DisjointSet.find

   **Path Compression Visualization:**
   
   .. code-block:: python
   
      ds = DisjointSet()
      for i in range(4):
          ds.make_set(i)
      
      # Create chain: 0 -> 1 -> 2 -> 3
      ds.union(0, 1)
      ds.union(1, 2)
      ds.union(2, 3)
      
      # First find - follows chain
      root = ds.find(3)  # Traverses 3->2->1->0
      
      # After path compression, 3 points directly to root
      # Subsequent finds are faster

Union Operations
----------------

.. automethod:: DisjointSet.union

   **Union by Rank Strategy:**
   
   .. code-block:: python
   
      ds = DisjointSet()
      for i in range(6):
          ds.make_set(i)
      
      # Build tree with rank 2
      ds.union(0, 1)  # rank[0] = 1
      ds.union(0, 2)  # rank[0] stays 1
      
      # Build tree with rank 1
      ds.union(3, 4)  # rank[3] = 1
      
      # Union by rank: attach smaller under larger
      ds.union(0, 3)  # 3 becomes child of 0
      
      print(ds.get_sets())
      # [{0, 1, 2, 3, 4}, {5}]

Query Operations
----------------

.. automethod:: DisjointSet.connected

   **Practical Usage:**
   
   .. code-block:: python
   
      ds = DisjointSet()
      nodes = ['Alice', 'Bob', 'Carol', 'Dave']
      for node in nodes:
          ds.make_set(node)
      
      # Build social network
      ds.union('Alice', 'Bob')
      ds.union('Carol', 'Dave')
      
      print(ds.connected('Alice', 'Bob'))    # True
      print(ds.connected('Alice', 'Carol'))  # False
      
      # Bridge connection
      ds.union('Bob', 'Carol')
      print(ds.connected('Alice', 'Dave'))   # True

.. automethod:: DisjointSet.size

   **Tracking Component Sizes:**
   
   .. code-block:: python
   
      ds = DisjointSet()
      for i in range(10):
          ds.make_set(i)
      
      # Merge into components
      ds.union(0, 1)
      ds.union(1, 2)
      ds.union(2, 3)
      
      ds.union(5, 6)
      ds.union(6, 7)
      
      print(ds.size(0))  # 4 (elements 0,1,2,3)
      print(ds.size(1))  # 4 (same set as 0)
      print(ds.size(5))  # 3 (elements 5,6,7)
      print(ds.size(4))  # 1 (singleton)

.. automethod:: DisjointSet.count_sets

   **Monitoring Connectivity:**
   
   .. code-block:: python
   
      ds = DisjointSet()
      n = 100
      for i in range(n):
          ds.make_set(i)
      
      print(f"Initial sets: {ds.count_sets()}")  # 100
      
      # Random unions
      import random
      for _ in range(50):
          u, v = random.sample(range(n), 2)
          ds.union(u, v)
      
      print(f"After 50 unions: {ds.count_sets()}")

.. automethod:: DisjointSet.get_sets

   **Analyzing Partitions:**
   
   .. code-block:: python
   
      ds = DisjointSet()
      for i in range(10):
          ds.make_set(i)
      
      edges = [(0,1), (1,2), (3,4), (5,6), (6,7), (7,8)]
      for u, v in edges:
          ds.union(u, v)
      
      sets = ds.get_sets()
      print(f"Number of components: {len(sets)}")
      
      for i, component in enumerate(sorted(sets, key=len, reverse=True)):
          print(f"Component {i+1}: {sorted(component)}")
      
      # Output:
      # Number of components: 3
      # Component 1: [5, 6, 7, 8]
      # Component 2: [0, 1, 2]
      # Component 3: [3, 4]
      # Component 4: [9]

Special Methods
---------------

.. automethod:: DisjointSet.__len__

   **Element Count:**
   
   .. code-block:: python
   
      ds = DisjointSet()
      print(len(ds))  # 0
      
      for i in range(5):
          ds.make_set(i)
      print(len(ds))  # 5
      
      # Length unchanged by unions
      ds.union(0, 1)
      ds.union(2, 3)
      print(len(ds))  # 5

.. automethod:: DisjointSet.__contains__

   **Membership Testing:**
   
   .. code-block:: python
   
      ds = DisjointSet()
      ds.make_set('A')
      ds.make_set('B')
      
      print('A' in ds)  # True
      print('C' in ds)  # False

.. automethod:: DisjointSet.__repr__

   **Debugging Information:**
   
   .. code-block:: python
   
      ds = DisjointSet()
      for i in range(10):
          ds.make_set(i)
      ds.union(0, 1)
      ds.union(2, 3)
      
      print(repr(ds))
      # DisjointSet(elements=10, sets=8)

.. automethod:: DisjointSet.__str__

   **Human-Readable Output:**
   
   .. code-block:: python
   
      ds = DisjointSet()
      for i in range(5):
          ds.make_set(i)
      
      print(str(ds))
      # DisjointSet: 5 elements in 5 sets

Examples
========

Basic Usage
-----------

**Connected Components**

.. code-block:: python

   from sds.advanced import DisjointSet
   
   # Create graph with 6 vertices
   ds = DisjointSet()
   for i in range(6):
       ds.make_set(i)
   
   # Add edges
   edges = [(0, 1), (1, 2), (3, 4)]
   for u, v in edges:
       ds.union(u, v)
   
   # Query connectivity
   print(ds.connected(0, 2))  # True (same component)
   print(ds.connected(0, 3))  # False (different components)
   print(ds.connected(3, 5))  # False
   
   # Analyze components
   components = ds.get_sets()
   print(f"Number of components: {len(components)}")
   for comp in components:
       print(f"  Component: {sorted(comp)}")
   
   # Output:
   # Number of components: 3
   #   Component: [0, 1, 2]
   #   Component: [3, 4]
   #   Component: [5]

Graph Algorithms
----------------

**Cycle Detection**

.. code-block:: python

   from sds.advanced import DisjointSet
   from typing import List, Tuple
   
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
           True if graph contains a cycle
       """
       ds = DisjointSet()
       
       # Initialize vertices
       for v in range(n):
           ds.make_set(v)
       
       # Process edges
       for u, v in edges:
           if ds.connected(u, v):
               return True  # Edge creates cycle
           ds.union(u, v)
       
       return False
   
   # Test
   edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 1)]  # Has cycle
   print(has_cycle(5, edges))  # True
   
   edges = [(0, 1), (1, 2), (2, 3), (3, 4)]  # Tree
   print(has_cycle(5, edges))  # False

**Kruskal's Minimum Spanning Tree**

.. code-block:: python

   from sds.advanced import DisjointSet
   from typing import List, Tuple
   
   def kruskal_mst(n: int, edges: List[Tuple[int, int, float]]) -> List[Tuple[int, int, float]]:
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
       List[Tuple[int, int, float]]
           Edges in MST
       """
       ds = DisjointSet()
       for v in range(n):
           ds.make_set(v)
       
       # Sort edges by weight
       edges_sorted = sorted(edges, key=lambda e: e[2])
       
       mst = []
       for u, v, weight in edges_sorted:
           if not ds.connected(u, v):
               ds.union(u, v)
               mst.append((u, v, weight))
               
               if len(mst) == n - 1:
                   break  # MST complete
       
       return mst
   
   # Example graph
   edges = [
       (0, 1, 4), (0, 2, 3),
       (1, 2, 1), (1, 3, 2),
       (2, 3, 4), (3, 4, 2),
       (4, 5, 6)
   ]
   
   mst = kruskal_mst(6, edges)
   total_weight = sum(w for _, _, w in mst)
   print(f"MST edges: {mst}")
   print(f"Total weight: {total_weight}")

**Network Connectivity**

.. code-block:: python

   from sds.advanced import DisjointSet
   from typing import List, Tuple
   
   class NetworkConnectivity:
       """Monitor network connectivity over time."""
       
       def __init__(self, n: int):
           self.ds = DisjointSet()
           for i in range(n):
               self.ds.make_set(i)
           self.history = [n]  # Initial components
       
       def connect(self, u: int, v: int) -> bool:
           """Connect two nodes."""
           merged = self.ds.union(u, v)
           if merged:
               self.history.append(self.ds.count_sets())
           return merged
       
       def is_connected(self, u: int, v: int) -> bool:
           """Check if two nodes are connected."""
           return self.ds.connected(u, v)
       
       def is_fully_connected(self) -> bool:
           """Check if network is fully connected."""
           return self.ds.count_sets() == 1
       
       def get_component_sizes(self) -> List[int]:
           """Get sizes of all components."""
           sets = self.ds.get_sets()
           return sorted([len(s) for s in sets], reverse=True)
   
   # Simulation
   net = NetworkConnectivity(10)
   
   connections = [
       (0, 1), (1, 2), (2, 3),
       (4, 5), (5, 6),
       (7, 8),
       (0, 4),  # Bridge components
       (4, 7),  # Another bridge
       (3, 9)   # Connect remaining
   ]
   
   for u, v in connections:
       net.connect(u, v)
       print(f"After connecting {u}-{v}:")
       print(f"  Components: {net.ds.count_sets()}")
       print(f"  Sizes: {net.get_component_sizes()}")
       if net.is_fully_connected():
           print("  Network fully connected!")
           break

Advanced Applications
---------------------

**Image Segmentation**

.. code-block:: python

   from sds.advanced import DisjointSet
   import numpy as np
   
   def segment_image(image: np.ndarray, threshold: float) -> np.ndarray:
       """
       Segment image by color similarity.
       
       Parameters
       ----------
       image : np.ndarray
           Input image (H x W x 3)
       threshold : float
           Color similarity threshold
       
       Returns
       -------
       np.ndarray
           Segmentation labels (H x W)
       """
       h, w, _ = image.shape
       ds = DisjointSet()
       
       # Initialize pixels
       for i in range(h):
           for j in range(w):
               ds.make_set((i, j))
       
       # Merge similar neighboring pixels
       for i in range(h):
           for j in range(w):
               # Check right neighbor
               if j + 1 < w:
                   diff = np.linalg.norm(
                       image[i, j] - image[i, j+1]
                   )
                   if diff < threshold:
                       ds.union((i, j), (i, j+1))
               
               # Check bottom neighbor
               if i + 1 < h:
                   diff = np.linalg.norm(
                       image[i, j] - image[i+1, j]
                   )
                   if diff < threshold:
                       ds.union((i, j), (i+1, j))
       
       # Create label map
       segments = ds.get_sets()
       labels = np.zeros((h, w), dtype=int)
       for label, segment in enumerate(segments):
           for i, j in segment:
               labels[i, j] = label
       
       return labels

**Social Network Analysis**

.. code-block:: python

   from sds.advanced import DisjointSet
   from typing import Dict, List, Set
   
   class SocialNetwork:
       """Analyze social network communities."""
       
       def __init__(self):
           self.ds = DisjointSet()
           self.users: Set[str] = set()
       
       def add_user(self, user: str):
           """Add new user."""
           if user not in self.users:
               self.ds.make_set(user)
               self.users.add(user)
       
       def add_friendship(self, user1: str, user2: str):
           """Create friendship between users."""
           self.add_user(user1)
           self.add_user(user2)
           self.ds.union(user1, user2)
       
       def are_friends(self, user1: str, user2: str) -> bool:
           """Check if users are in same network."""
           return self.ds.connected(user1, user2)
       
       def get_communities(self) -> List[Set[str]]:
           """Get all communities."""
           return self.ds.get_sets()
       
       def community_stats(self) -> Dict:
           """Compute community statistics."""
           communities = self.get_communities()
           sizes = [len(c) for c in communities]
           
           return {
               'num_communities': len(communities),
               'num_users': len(self.users),
               'avg_community_size': sum(sizes) / len(sizes),
               'max_community_size': max(sizes),
               'min_community_size': min(sizes),
               'isolated_users': sum(1 for s in sizes if s == 1)
           }
   
   # Usage
   network = SocialNetwork()
   
   friendships = [
       ('Alice', 'Bob'), ('Bob', 'Carol'),
       ('Dave', 'Eve'), ('Eve', 'Frank'),
       ('Grace', 'Henry'), ('Henry', 'Ivy'),
       ('Bob', 'Dave')  # Bridge
   ]
   
   for u, v in friendships:
       network.add_friendship(u, v)
   
   stats = network.community_stats()
   print("Network Statistics:")
   for key, value in stats.items():
       print(f"  {key}: {value}")
   
   # Find specific user's community
   alice_community = None
   for community in network.get_communities():
       if 'Alice' in community:
           alice_community = community
           break
   
   print(f"\nAlice's network: {sorted(alice_community)}")

Performance Considerations
==========================

Optimization Techniques
-----------------------

**1. Path Compression Variants**

.. code-block:: python

   # Full path compression (implemented)
   def find_full_compression(self, x):
       if parent[x] != x:
           parent[x] = self.find(parent[x])  # Recursive
       return parent[x]
   
   # Path halving (alternative)
   def find_path_halving(self, x):
       while parent[x] != x:
           parent[x] = parent[parent[x]]  # Skip one level
           x = parent[x]
       return x
   
   # Path splitting (another alternative)
   def find_path_splitting(self, x):
       while parent[x] != x:
           next_x = parent[x]
           parent[x] = parent[parent[x]]
           x = next_x
       return x

**2. Union Strategies**

.. code-block:: python

   # Union by rank (implemented)
   # Maintains upper bound on tree height
   
   # Union by size (alternative)
   # Always merges smaller set into larger
   # Similar performance, simpler to understand

**3. Batch Operations**

.. code-block:: python

   def batch_union(self, pairs: List[Tuple[Any, Any]]):
       """Perform multiple unions efficiently."""
       for x, y in pairs:
           if not self.connected(x, y):
               self.union(x, y)

Common Pitfalls
---------------

**1. Forgetting to Initialize Elements**

.. code-block:: python

   # ❌ Wrong
   ds = DisjointSet()
   ds.union(0, 1)  # ValueError: Element 0 is not in any set
   
   # ✓ Correct
   ds = DisjointSet()
   ds.make_set(0)
   ds.make_set(1)
   ds.union(0, 1)

**2. Assuming Size is O(1)**

.. code-block:: python

   # Size requires find(), which is O(α(n))
   # For frequent size queries, cache results
   
   root = ds.find(element)
   size = ds.size(element)  # Uses cached size at root

**3. Modifying Returned Sets**

.. code-block:: python

   # get_sets() returns new set objects
   sets = ds.get_sets()
   sets[0].add(new_element)  # Doesn't affect DisjointSet

Best Practices
--------------

**1. Pre-allocate Elements**

.. code-block:: python

   # If you know all elements upfront
   ds = DisjointSet()
   for element in all_elements:
       ds.make_set(element)

**2. Use Meaningful Element Types**

.. code-block:: python

   # ✓ Good: descriptive elements
   ds = DisjointSet()
   ds.make_set('server_1')
   ds.make_set('server_2')
   
   # ❌ Avoid: opaque indices when names available
   ds.make_set(0)
   ds.make_set(1)

**3. Monitor Component Count**

.. code-block:: python

   # Check progress of merging
   initial_sets = ds.count_sets()
   # ... perform unions ...
   final_sets = ds.count_sets()
   print(f"Merged {initial_sets - final_sets} components")

See Also
========

* :ref:`guide_advanced_disjoint_set` - Comprehensive usage guide
* :ref:`api_advanced_interfaces` - Abstract base class
* :ref:`guide_algorithms_graph` - Graph algorithms using DisjointSet
* :ref:`guide_algorithms_mst` - Kruskal's algorithm

References
==========

.. [1] Tarjan, R. E., & van Leeuwen, J. (1984). "Worst-case Analysis of
       Set Union Algorithms". *Journal of the ACM*, 31(2), 245-281.
       DOI: 10.1145/62.2160
       
.. [2] Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009).
       "Introduction to Algorithms" (3rd ed.). MIT Press.
       Chapter 21: Data Structures for Disjoint Sets.
       
.. [3] Galil, Z., & Italiano, G. F. (1991). "Data structures and algorithms
       for disjoint set union problems". *ACM Computing Surveys*, 23(3), 319-344.
       
.. [4] Tarjan, R. E. (1975). "Efficiency of a Good But Not Linear Set
       Union Algorithm". *Journal of the ACM*, 22(2), 215-225.
