.. _guide_raph:

=================
Graph Structures
=================

Introduction
============

Graph data structures represent relationships between objects through nodes (vertices)
and edges (connections). Unlike linear structures with sequential relationships or trees
with hierarchical relationships, graphs can represent arbitrary connections, making them
ideal for modeling networks, dependencies, and complex relationships.

.. mermaid::

   graph LR
       A((A)) --- B((B))
       A --- C((C))
       B --- D((D))
       C --- D
       C --- E((E))
       D --- E
       
       style A fill:#e74c3c,stroke:#c0392b,color:#fff
       style B fill:#3498db,stroke:#2980b9,color:#fff
       style C fill:#3498db,stroke:#2980b9,color:#fff
       style D fill:#2ecc71,stroke:#27ae60,color:#fff
       style E fill:#2ecc71,stroke:#27ae60,color:#fff

This section covers all graph structures provided by SDS-Tools, from basic undirected
graphs to weighted directed graphs and specialized representations.

Overview
========

Types of Graph Structures
--------------------------

SDS-Tools provides several graph implementations, each optimized for specific use cases:

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Structure
     - Key Property
     - Primary Use Cases
   * - **Graph**
     - Undirected, unweighted
     - Social networks, connections
   * - **DirectedGraph**
     - Directed edges
     - Dependencies, workflows, citations
   * - **UndirectedGraph**
     - Explicit undirected validation
     - Symmetric relationships
   * - **WeightedGraph**
     - Undirected with edge weights
     - Distance networks, costs
   * - **WeightedDirectedGraph**
     - Directed with edge weights
     - Routing, flow networks
   * - **AdjacencyListGraph**
     - Explicit list representation
     - Sparse graphs, memory-efficient
   * - **AdjacencyMatrixGraph**
     - 2D matrix representation
     - Dense graphs, O(1) edge lookup

Graph Terminology
-----------------

.. mermaid::

   graph TB
       subgraph "Directed Graph"
       A1[Vertex A<br/>out-degree: 2<br/>in-degree: 0] -->|Edge 1| B1[Vertex B<br/>out: 1, in: 2]
       A1 -->|Edge 2| C1[Vertex C<br/>out: 1, in: 1]
       B1 -->|Edge 3| D1[Vertex D<br/>out: 0, in: 2]
       C1 -->|Edge 4| D1
       end
       
       subgraph "Weighted Graph"
       A2((A)) -->|5| B2((B))
       A2 -->|3| C2((C))
       B2 -->|7| D2((D))
       C2 -->|2| D2
       end
       
       style A1 fill:#e74c3c,color:#fff
       style A2 fill:#3498db,color:#fff

**Key Terms:**

* **Vertex (Node)**: A point in the graph representing an entity
* **Edge (Arc)**: A connection between two vertices
* **Adjacent**: Two vertices connected by an edge
* **Degree**: Number of edges incident to a vertex
  * **In-degree**: Number of incoming edges (directed graphs)
  * **Out-degree**: Number of outgoing edges (directed graphs)
* **Path**: Sequence of vertices connected by edges
* **Cycle**: Path that starts and ends at the same vertex
* **Connected**: Every vertex reachable from every other vertex
* **Weight**: Numeric value associated with an edge
* **Directed**: Edges have a direction (source → target)
* **Undirected**: Edges are bidirectional

Choosing the Right Graph
-------------------------

.. mermaid::

   graph TD
       A{What's your<br/>requirement?}
       
       A -->|Bidirectional relationships| B{Need weights?}
       B -->|No| C[Graph / UndirectedGraph]
       B -->|Yes| D[WeightedGraph]
       
       A -->|Directional relationships| E{Need weights?}
       E -->|No| F[DirectedGraph]
       E -->|Yes| G[WeightedDirectedGraph]
       
       A -->|Dense graph<br/>O(1) edge lookup| H[AdjacencyMatrixGraph]
       A -->|Sparse graph<br/>Memory efficient| I[AdjacencyListGraph]
       
       style C fill:#3498db,color:#fff
       style D fill:#2ecc71,color:#fff
       style F fill:#e74c3c,color:#fff
       style G fill:#e67e22,color:#fff
       style H fill:#9b59b6,color:#fff
       style I fill:#1abc9c,color:#fff

Detailed Guides
===============

Basic Graphs
------------

.. toctree::
   :maxdepth: 2
   :caption: Foundation

   general
   directed

Weighted Graphs
---------------

.. toctree::
   :maxdepth: 2
   :caption: Graphs with Edge Weights

   weighted

Graph Representations
---------------------

.. toctree::
   :maxdepth: 2
   :caption: Implementation Strategies

   adjacency

Quick Start
===========

Undirected Graph
----------------

Basic graph for symmetric relationships:

.. code-block:: python

   from sds.graph import Graph, GraphNode, Edge

   # Create undirected graph
   g = Graph()

   # Add nodes
   alice = GraphNode("Alice", "alice")
   bob = GraphNode("Bob", "bob")
   carol = GraphNode("Carol", "carol")
   
   g.add_node(alice)
   g.add_node(bob)
   g.add_node(carol)

   # Add edges (bidirectional)
   g.add_edge(Edge(alice, bob))
   g.add_edge(Edge(bob, carol))
   g.add_edge(Edge(alice, carol))

   # Query the graph
   print(f"Nodes: {g.node_count()}")      # Output: 3
   print(f"Edges: {g.edge_count()}")      # Output: 3
   print(f"Connected: {g.is_connected()}") # Output: True
   
   # Check connections
   print(g.has_edge(alice, bob))  # Output: True
   print(g.degree(bob))           # Output: 2

Directed Graph
--------------

Graph with directed edges for asymmetric relationships:

.. code-block:: python

   from sds.graph import DirectedGraph, GraphNode, DirectedEdge

   # Create directed graph
   dg = DirectedGraph()

   # Add nodes
   a = GraphNode("Task A", "a")
   b = GraphNode("Task B", "b")
   c = GraphNode("Task C", "c")
   
   dg.add_node(a)
   dg.add_node(b)
   dg.add_node(c)

   # Add directed edges (A → B, B → C)
   dg.add_edge(DirectedEdge(a, b))
   dg.add_edge(DirectedEdge(b, c))

   # Direction matters!
   print(dg.has_edge(a, b))  # Output: True
   print(dg.has_edge(b, a))  # Output: False
   
   # Degree analysis
   print(f"A out-degree: {dg.out_degree(a)}")  # Output: 1
   print(f"A in-degree: {dg.in_degree(a)}")    # Output: 0
   print(f"B out-degree: {dg.out_degree(b)}")  # Output: 1
   print(f"B in-degree: {dg.in_degree(b)}")    # Output: 1

   # Check for cycles
   print(f"Is DAG: {dg.is_acyclic()}")  # Output: True

Weighted Graph
--------------

Graph with edge weights for costs or distances:

.. code-block:: python

   from sds.graph import WeightedGraph, GraphNode, WeightedEdge

   # Create weighted undirected graph
   wg = WeightedGraph()

   # Add cities as nodes
   paris = GraphNode("Paris", "paris")
   london = GraphNode("London", "london")
   berlin = GraphNode("Berlin", "berlin")
   
   wg.add_node(paris)
   wg.add_node(london)
   wg.add_node(berlin)

   # Add weighted edges (distances in km)
   wg.add_edge(WeightedEdge(paris, london, weight=344))
   wg.add_edge(WeightedEdge(london, berlin, weight=932))
   wg.add_edge(WeightedEdge(paris, berlin, weight=878))

   # Query weights
   distance = wg.get_edge_weight(paris, london)
   print(f"Paris-London: {distance} km")  # Output: 344 km
   
   # Total network distance
   total = wg.total_weight()
   print(f"Total distance: {total} km")  # Output: 2154 km

Adjacency Representations
--------------------------

Different representations for different use cases:

.. code-block:: python

   from sds.graph import AdjacencyListGraph, AdjacencyMatrixGraph
   from sds.graph import GraphNode, Edge

   # Adjacency List (sparse graphs)
   al_graph = AdjacencyListGraph()
   
   n1 = GraphNode("A", "n1")
   n2 = GraphNode("B", "n2")
   al_graph.add_node(n1)
   al_graph.add_node(n2)
   al_graph.add_edge(Edge(n1, n2))
   
   # Get adjacency list
   neighbors = al_graph.get_adjacency_list("n1")
   print(neighbors)  # Output: {'n2'}

   # Adjacency Matrix (dense graphs, O(1) lookup)
   am_graph = AdjacencyMatrixGraph(max_nodes=10)
   
   am_graph.add_node(n1)
   am_graph.add_node(n2)
   am_graph.add_edge(Edge(n1, n2))
   
   # Get matrix representation
   matrix = am_graph.get_matrix()
   print(matrix[0][1])  # Output: 1 (edge exists)

Common Patterns
===============

Pattern 1: Path Finding
------------------------

Find if a path exists between two nodes:

.. code-block:: python

   from sds.graph import Graph, GraphNode, Edge
   from collections import deque

   def has_path_bfs(graph, start, end):
       """Check if path exists using BFS."""
       if start == end:
           return True
       
       visited = set()
       queue = deque([start])
       visited.add(start.id)
       
       while queue:
           current = queue.popleft()
           
           for neighbor in graph.neighbors(current):
               if neighbor == end:
                   return True
               
               if neighbor.id not in visited:
                   visited.add(neighbor.id)
                   queue.append(neighbor)
       
       return False

   # Usage
   g = Graph()
   a = GraphNode("A", "a")
   b = GraphNode("B", "b")
   c = GraphNode("C", "c")
   
   g.add_node(a)
   g.add_node(b)
   g.add_node(c)
   g.add_edge(Edge(a, b))
   g.add_edge(Edge(b, c))
   
   print(has_path_bfs(g, a, c))  # Output: True

Pattern 2: Cycle Detection
---------------------------

Detect cycles in directed graphs:

.. code-block:: python

   from sds.graph import DirectedGraph

   def detect_cycle_dfs(graph):
       """Detect cycle using DFS with coloring."""
       color = {node.id: 'WHITE' for node in graph.nodes()}
       
       def has_cycle(node):
           color[node.id] = 'GRAY'
           
           for neighbor in graph.successors(node):
               if color[neighbor.id] == 'GRAY':
                   return True  # Back edge found
               if color[neighbor.id] == 'WHITE':
                   if has_cycle(neighbor):
                       return True
           
           color[node.id] = 'BLACK'
           return False
       
       for node in graph.nodes():
           if color[node.id] == 'WHITE':
               if has_cycle(node):
                   return True
       
       return False

   # Usage with DirectedGraph
   dg = DirectedGraph()
   # Add nodes and edges...
   
   # Or use built-in method
   has_cycle = not dg.is_acyclic()

Pattern 3: Shortest Path (Unweighted)
--------------------------------------

Find shortest path in unweighted graph:

.. code-block:: python

   from sds.graph import Graph
   from collections import deque

   def shortest_path_bfs(graph, start, end):
       """Find shortest path using BFS."""
       if start == end:
           return [start]
       
       visited = {start.id}
       queue = deque([(start, [start])])
       
       while queue:
           current, path = queue.popleft()
           
           for neighbor in graph.neighbors(current):
               if neighbor.id not in visited:
                   new_path = path + [neighbor]
                   
                   if neighbor == end:
                       return new_path
                   
                   visited.add(neighbor.id)
                   queue.append((neighbor, new_path))
       
       return None  # No path found

   # Usage
   path = shortest_path_bfs(g, a, c)
   if path:
       print(" -> ".join(node.data for node in path))

Pattern 4: Topological Sort
----------------------------

Order tasks by dependencies:

.. code-block:: python

   from sds.graph import DirectedGraph

   def topological_sort_dfs(graph):
       """Topological sort using DFS."""
       visited = set()
       stack = []
       
       def dfs(node):
           visited.add(node.id)
           
           for successor in graph.successors(node):
               if successor.id not in visited:
                   dfs(successor)
           
           stack.append(node)
       
       for node in graph.nodes():
           if node.id not in visited:
               dfs(node)
       
       return list(reversed(stack))

   # Usage for task scheduling
   tasks = DirectedGraph()
   # Add tasks with dependencies...
   
   execution_order = topological_sort_dfs(tasks)

Performance Comparison
======================

Operation Complexity
--------------------

.. list-table::
   :header-rows: 1
   :widths: 25 15 15 15 15 15

   * - Operation
     - Graph
     - DirectedGraph
     - AdjacencyList
     - AdjacencyMatrix
     - Notes
   * - **Add Node**
     - O(1)
     - O(1)
     - O(1)
     - O(1)
     - Constant time
   * - **Add Edge**
     - O(1)
     - O(1)
     - O(1)
     - O(1)
     - Amortized
   * - **Remove Node**
     - O(degree + E)
     - O(degree + E)
     - O(degree + E)
     - O(V)
     - Remove incident edges
   * - **Remove Edge**
     - O(E)
     - O(E)
     - O(E)
     - O(1)
     - Matrix: O(1)
   * - **Has Edge**
     - O(1)
     - O(1)
     - O(1)
     - O(1)
     - Using adjacency
   * - **Get Neighbors**
     - O(degree)
     - O(degree)
     - O(degree)
     - O(V)
     - Matrix: all nodes
   * - **Degree**
     - O(1)
     - O(1)
     - O(1)
     - O(V)
     - Amortized
   * - **Is Connected**
     - O(V + E)
     - O(V + E)
     - O(V + E)
     - O(V²)
     - BFS/DFS

Space Complexity
----------------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Representation
     - Space Complexity
     - Best For
   * - **Adjacency List**
     - O(V + E)
     - Sparse graphs (E << V²)
   * - **Adjacency Matrix**
     - O(V²)
     - Dense graphs (E ≈ V²)
   * - **Edge List**
     - O(E)
     - Simple storage

**Guidelines:**

* **Sparse graphs** (few edges): Use adjacency list
* **Dense graphs** (many edges): Use adjacency matrix
* **Edge-centric operations**: Use edge list

Graph Type Comparison
---------------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 20 20

   * - Aspect
     - Graph
     - DirectedGraph
     - WeightedGraph
     - Matrix
   * - **Directionality**
     - Undirected
     - Directed
     - Undirected
     - Both
   * - **Edge Weights**
     - No
     - No
     - Yes
     - Optional
   * - **Multi-edges**
     - Optional
     - Optional
     - Optional
     - No
   * - **Memory**
     - O(V + E)
     - O(V + E)
     - O(V + E)
     - O(V²)
   * - **Edge Lookup**
     - O(1)
     - O(1)
     - O(1)
     - O(1)

Best Practices
==============

Choosing Operations
-------------------

✅ **Use appropriate graph type**

.. code-block:: python

   # Symmetric relationships → Graph
   friendship_network = Graph()

   # Dependencies, workflows → DirectedGraph
   task_dependencies = DirectedGraph()

   # Distances, costs → WeightedGraph
   road_network = WeightedGraph()

   # Dense connections → AdjacencyMatrixGraph
   fully_connected = AdjacencyMatrixGraph(max_nodes=100)

✅ **Check connectivity before operations**

.. code-block:: python

   if graph.is_connected():
       # Safe to traverse entire graph
       pass
   else:
       # Handle disconnected components
       pass

✅ **Use iterators for large graphs**

.. code-block:: python

   # Good: Memory efficient
   for node in graph.nodes():
       process(node)

   # Avoid: Loads all into memory
   all_nodes = list(graph.nodes())

Common Pitfalls
---------------

❌ **Creating circular references manually**

.. code-block:: python

   # Bad: Can create cycles in DAG
   # Use add_edge() instead of manual manipulation

❌ **Not handling disconnected graphs**

.. code-block:: python

   # Bad: Assumes connected
   for node in graph.nodes():
       find_path_to_root(node)  # May not exist!

   # Good: Check connectivity
   if graph.is_connected():
       # Process
       pass

❌ **Using wrong representation**

.. code-block:: python

   # Bad: Matrix for sparse graph
   sparse_graph = AdjacencyMatrixGraph(max_nodes=10000)
   # Wastes 100M cells for 100 edges!

   # Good: List for sparse
   sparse_graph = AdjacencyListGraph()

❌ **Modifying during iteration**

.. code-block:: python

   # Bad: Modifying while iterating
   for node in graph.nodes():
       graph.remove_node(node)  # Dangerous!

   # Good: Collect then modify
   to_remove = list(graph.nodes())
   for node in to_remove:
       graph.remove_node(node)

Algorithm Integration
=====================

Common Graph Algorithms
-----------------------

**Traversal Algorithms:**

* **BFS (Breadth-First Search)**: Level-by-level exploration
* **DFS (Depth-First Search)**: Explore deeply before backtracking

**Shortest Path Algorithms:**

* **Dijkstra's Algorithm**: Shortest paths from source (weighted)
* **Bellman-Ford**: Handles negative weights
* **A* Search**: Heuristic-guided pathfinding

**Minimum Spanning Tree:**

* **Kruskal's Algorithm**: Sort edges, add if no cycle
* **Prim's Algorithm**: Grow tree from starting vertex

**Network Flow:**

* **Ford-Fulkerson**: Maximum flow in networks
* **Edmonds-Karp**: BFS-based Ford-Fulkerson

**Connectivity:**

* **Tarjan's Algorithm**: Strongly connected components
* **Kosaraju's Algorithm**: Alternative SCC algorithm

Example: BFS Implementation
----------------------------

.. code-block:: python

   from sds.graph import Graph
   from collections import deque

   def bfs(graph, start):
       """Breadth-first search traversal."""
       visited = set()
       queue = deque([start])
       visited.add(start.id)
       result = []
       
       while queue:
           node = queue.popleft()
           result.append(node.data)
           
           for neighbor in graph.neighbors(node):
               if neighbor.id not in visited:
                   visited.add(neighbor.id)
                   queue.append(neighbor)
       
       return result

Example: DFS Implementation
----------------------------

.. code-block:: python

   def dfs(graph, start):
       """Depth-first search traversal."""
       visited = set()
       result = []
       
       def dfs_recursive(node):
           visited.add(node.id)
           result.append(node.data)
           
           for neighbor in graph.neighbors(node):
               if neighbor.id not in visited:
                   dfs_recursive(neighbor)
       
       dfs_recursive(start)
       return result

Real-World Applications
=======================

1. **Social Networks**
   
   * Friendship graphs (undirected)
   * Follower networks (directed)
   * Community detection
   * Influence analysis

2. **Transportation Networks**
   
   * Road networks (weighted undirected)
   * Flight routes (weighted directed)
   * Public transit systems
   * Shortest path routing

3. **Dependency Management**
   
   * Software package dependencies (directed acyclic)
   * Build systems
   * Task scheduling
   * Prerequisites

4. **Web and Internet**
   
   * Web page links (directed)
   * Network topology
   * Citation networks
   * Recommendation systems

5. **Biology and Chemistry**
   
   * Protein interactions
   * Neural networks
   * Molecular structures
   * Evolutionary trees

6. **Computer Networks**
   
   * Network topology
   * Routing protocols
   * Load balancing
   * Fault tolerance

7. **Game Development**
   
   * Navigation meshes
   * State machines
   * Dialogue systems
   * AI pathfinding

8. **Project Management**
   
   * PERT charts
   * Critical path analysis
   * Resource allocation
   * Timeline dependencies

See Also
========

* :doc:`../../api/graph/index` - API reference for graph structures
* :doc:`../linear_structures/index` - Linear structures guide
* :doc:`../tree_structures/index` - Tree structures guide

External Resources
------------------

* `VisuAlgo: Graph Structures <https://visualgo.net/en/graphds>`_ - Interactive visualizations
* `Graph Visualization <https://www.cs.usfca.edu/~galles/visualization/>`_ - USFCA visualizations
* `NetworkX Documentation <https://networkx.org/>`_ - Python graph library
* `Boost Graph Library <https://www.boost.org/doc/libs/release/libs/graph/>`_ - C++ graph library

References
==========

Academic Resources (Open Access)
---------------------------------

.. [WikiGraph] Wikipedia contributors. "Graph (discrete mathematics)". Wikipedia.
   https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)
   
   Comprehensive overview of graph theory fundamentals and terminology.

.. [WikiGraphTheory] Wikipedia contributors. "Graph theory". Wikipedia.
   https://en.wikipedia.org/wiki/Graph_theory
   
   Mathematical foundations of graph theory with proofs and theorems.

.. [OpenDSA] Shaffer, C. A., et al. "OpenDSA Data Structures and Algorithms Modules Collection".
   https://opendsa-server.cs.vt.edu/ODSA/Books/Everything/html/
   
   Interactive textbook with modules on:
   
   - "Graph Representations"
   - "Graph Traversals" (BFS, DFS)
   - "Shortest Paths Algorithms"
   - "Minimum Spanning Trees"

.. [MIT6006] MIT OpenCourseWare. "6.006 Introduction to Algorithms".
   https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/
   
   Free course materials including lectures on:
   
   - Graph search (BFS, DFS)
   - Shortest paths (Dijkstra, Bellman-Ford)
   - All-pairs shortest paths

.. [VisuAlgo] Halim, S., Halim, F. "VisuAlgo - Graph Data Structures".
   https://visualgo.net/en/graphds
   
   Interactive visualizations for:
   
   - Graph representations
   - Graph traversals
   - Minimum spanning tree algorithms
   - Shortest path algorithms

.. [Stanford] Stanford CS Education Library. "Linked List Basics".
   http://cslibrary.stanford.edu/103/
   
   Fundamentals applicable to graph node structures.

.. [GeeksforGeeks] GeeksforGeeks. "Graph Data Structure".
   https://www.geeksforgeeks.org/graph-data-structure-and-algorithms/
   
   Practical tutorials covering:
   
   - Graph representations
   - Graph traversal algorithms
   - Shortest path algorithms
   - Minimum spanning trees
   - Interview questions

Classic Literature
------------------

While not freely available online, these are cited as authoritative references:

.. [CLRS] Cormen, T. H., Leiserson, C. E., Rivest, R. L., Stein, C.
   "Introduction to Algorithms", 3rd Edition, 2009. MIT Press.
   
   Part VI: Graph Algorithms (Chapters 22-26)
   
   - Elementary graph algorithms
   - Minimum spanning trees
   - Single-source shortest paths
   - All-pairs shortest paths
   - Maximum flow

.. [DPV] Dasgupta, S., Papadimitriou, C., Vazirani, U.
   "Algorithms", 2008. McGraw-Hill.
   
   Chapter 3-4: Graphs and paths
   
   *Note: Free PDF available from authors' websites*

.. [Sedgewick] Sedgewick, R., Wayne, K.
   "Algorithms", 4th Edition, 2011. Addison-Wesley.
   
   Part 4: Graphs
   
   Companion website: https://algs4.cs.princeton.edu/

.. [GoodrichTamassia] Goodrich, M. T., Tamassia, R., Goldwasser, M. H.
   "Data Structures and Algorithms in Python", 2013. Wiley.
   
   Chapter 14: Graph Algorithms

.. [WestGraphTheory] West, D. B.
   "Introduction to Graph Theory", 2nd Edition, 2001. Prentice Hall.
   
   Comprehensive mathematical treatment of graph theory.

Online Courses
--------------

.. [Coursera] Princeton University. "Algorithms, Part II" (Sedgewick & Wayne).
   https://www.coursera.org/learn/algorithms-part2
   
   Free course covering:
   
   - Undirected graphs
   - Directed graphs
   - Minimum spanning trees
   - Shortest paths

.. [CourseraStanford] Stanford University. "Algorithms Specialization".
   https://www.coursera.org/specializations/algorithms
   
   Graph search, shortest paths, and data structures.

.. [YouTubeMIT] MIT OpenCourseWare. "Introduction to Algorithms".
   https://www.youtube.com/playlist?list=PLUl4u3cNGP61Oq3tWYp6V_F-5jb5L2iHb
   
   Video lectures on graph algorithms.

Research Papers (Open Access)
------------------------------

.. [Dijkstra] Dijkstra, E. W. "A note on two problems in connexion with graphs", 1959.
   Numerische Mathematik 1, 269-271.
   https://doi.org/10.1007/BF01386390

.. [Kruskal] Kruskal, J. B. "On the shortest spanning subtree of a graph", 1956.
   Proceedings of the American Mathematical Society 7(1), 48-50.

.. [Tarjan] Tarjan, R. E. "Depth-first search and linear graph algorithms", 1972.
   SIAM Journal on Computing 1(2), 146-160.

Tools and Software
------------------

.. [NetworkX] NetworkX Development Team. "NetworkX Documentation".
   https://networkx.org/documentation/
   
   Python library for complex networks (compatible with SDS-Tools).

.. [GraphViz] Graphviz. "Graph Visualization Software".
   https://graphviz.org/
   
   Open-source graph visualization tools.

.. [Gephi] Gephi Consortium. "Gephi - The Open Graph Viz Platform".
   https://gephi.org/
   
   Interactive visualization and exploration platform.