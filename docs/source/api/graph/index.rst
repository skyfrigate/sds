.. _api_graph:

============================
Graph Structures (sds.graph)
============================

.. currentmodule:: sds.graph

Graph data structures represent relationships between entities as collections of nodes 
(vertices) connected by edges. They are fundamental for modeling networks, relationships, 
and interconnected systems.

Overview
========

The graph module provides comprehensive implementations of graph data structures:

* **Basic Graphs** - Simple undirected graphs
* **Directed Graphs** - Graphs with directed edges (digraphs)
* **Weighted Graphs** - Graphs with edge weights
* **Adjacency Representations** - List and matrix implementations
* **Specialized Graphs** - DAGs, trees as graphs, and more

Key Features
============

✓ **Flexible representations** - Adjacency list, matrix, and edge list formats
✓ **Multiple edge types** - Undirected, directed, weighted, and combinations
✓ **Efficient operations** - Optimized for common graph algorithms
✓ **Rich node/edge data** - Store arbitrary data on vertices and edges
✓ **Multi-graph support** - Allow multiple edges between same nodes
✓ **Consistent API** - Uniform interface across all graph types

Module Contents
===============

Node and Edge Classes
----------------------

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   GraphNode
   Edge
   DirectedEdge
   WeightedEdge
   WeightedDirectedEdge

Basic Graph Structures
-----------------------

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   Graph
   DirectedGraph
   UndirectedGraph

Weighted Graphs
---------------

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   WeightedGraph
   WeightedDirectedGraph

Adjacency Representations
--------------------------

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   AdjacencyListGraph
   AdjacencyMatrixGraph

Detailed Documentation
======================

.. toctree::
   :maxdepth: 2

   node
   edge
   interfaces
   graph
   directed
   weighted
   adjacency

Graph Type Comparison
=====================

.. list-table:: Graph Structure Comparison
   :header-rows: 1
   :widths: 20 15 15 15 35

   * - Structure
     - Add Edge
     - Check Edge
     - Space
     - Best Use Case
   * - Graph
     - O(1)
     - O(deg)
     - O(V + E)
     - General purpose
   * - DirectedGraph
     - O(1)
     - O(1)*
     - O(V + E)
     - Dependencies, flows
   * - WeightedGraph
     - O(1)
     - O(deg)
     - O(V + E)
     - Distances, costs
   * - AdjacencyList
     - O(1)
     - O(deg)
     - O(V + E)
     - Sparse graphs
   * - AdjacencyMatrix
     - O(1)
     - O(1)
     - O(V²)
     - Dense graphs

\* With adjacency set; deg = degree of node

Edge Type Comparison
--------------------

.. list-table:: Edge Types and Applications
   :header-rows: 1
   :widths: 25 25 50

   * - Edge Type
     - Properties
     - Common Use Cases
   * - **Edge**
     - Undirected, unweighted
     - Friendships, physical connections
   * - **DirectedEdge**
     - Directed, unweighted
     - Follows, citations, dependencies
   * - **WeightedEdge**
     - Undirected, weighted
     - Distances, similarities, costs
   * - **WeightedDirectedEdge**
     - Directed, weighted
     - Network flows, weighted paths

Graph Representations
=====================

Adjacency List vs Matrix
--------------------------

.. mermaid::

   graph TB
       subgraph "Adjacency List (Sparse)"
       A1[Node A] --> B1[B, C]
       B2[Node B] --> C2[A, C, D]
       C3[Node C] --> D3[A, B]
       D4[Node D] --> E4[B]
       end
       
       subgraph "Adjacency Matrix (Dense)"
       M["Matrix<br/>  A B C D<br/>A 0 1 1 0<br/>B 1 0 1 1<br/>C 1 1 0 0<br/>D 0 1 0 0"]
       end
       
       style A1 fill:#3498db
       style M fill:#e74c3c,color:#fff

**When to use each:**

- **Adjacency List**: Sparse graphs (E << V²), need to iterate neighbors
- **Adjacency Matrix**: Dense graphs (E ≈ V²), frequent edge existence checks

Directed vs Undirected
-----------------------

.. mermaid::

   graph LR
       subgraph "Undirected Graph"
       A1[A] --- B1[B]
       A1 --- C1[C]
       B1 --- C1
       end
       
       subgraph "Directed Graph"
       A2[A] --> B2[B]
       A2 --> C2[C]
       B2 --> C2
       C2 --> A2
       end
       
       style A1 fill:#2ecc71
       style A2 fill:#e74c3c

Common Use Cases
================

Social Networks
---------------

.. code-block:: python

   from sds.graph import Graph, GraphNode, Edge

   # Undirected friendship graph
   social = Graph()
   
   # Add users
   alice = GraphNode("Alice", node_id="alice")
   bob = GraphNode("Bob", node_id="bob")
   carol = GraphNode("Carol", node_id="carol")
   
   social.add_node(alice)
   social.add_node(bob)
   social.add_node(carol)
   
   # Add friendships (bidirectional)
   social.add_edge(Edge(alice, bob, data={'since': '2020'}))
   social.add_edge(Edge(bob, carol, data={'since': '2021'}))
   
   # Find friends
   alice_friends = list(social.neighbors(alice))
   print(f"Alice's friends: {[f.data for f in alice_friends]}")

Transportation Networks
-----------------------

.. code-block:: python

   from sds.graph import WeightedGraph, GraphNode, WeightedEdge

   # Cities with distances
   network = WeightedGraph()
   
   paris = GraphNode("Paris", node_id="paris")
   london = GraphNode("London", node_id="london")
   berlin = GraphNode("Berlin", node_id="berlin")
   
   network.add_node(paris)
   network.add_node(london)
   network.add_node(berlin)
   
   # Add routes with distances (km)
   network.add_edge(WeightedEdge(paris, london, weight=344))
   network.add_edge(WeightedEdge(paris, berlin, weight=878))
   network.add_edge(WeightedEdge(london, berlin, weight=932))
   
   # Find route weight
   route = network.get_edge(paris, london)
   print(f"Paris to London: {route.weight} km")

Task Dependencies (DAG)
-----------------------

.. code-block:: python

   from sds.graph import DirectedGraph, GraphNode, DirectedEdge

   # Task dependency graph
   tasks = DirectedGraph()
   
   design = GraphNode("Design", node_id="design")
   backend = GraphNode("Backend", node_id="backend")
   frontend = GraphNode("Frontend", node_id="frontend")
   testing = GraphNode("Testing", node_id="testing")
   
   for task in [design, backend, frontend, testing]:
       tasks.add_node(task)
   
   # Dependencies (from → to means "from before to")
   tasks.add_edge(DirectedEdge(design, backend))
   tasks.add_edge(DirectedEdge(design, frontend))
   tasks.add_edge(DirectedEdge(backend, frontend))
   tasks.add_edge(DirectedEdge(frontend, testing))
   
   # Check if DAG (no cycles)
   print(f"Is DAG: {tasks.is_acyclic()}")  # True

Web Page Links
--------------

.. code-block:: python

   from sds.graph import DirectedGraph, GraphNode, DirectedEdge

   # Web link graph
   web = DirectedGraph()
   
   home = GraphNode("Home", node_id="home")
   about = GraphNode("About", node_id="about")
   contact = GraphNode("Contact", node_id="contact")
   
   for page in [home, about, contact]:
       web.add_node(page)
   
   # Links (directed)
   web.add_edge(DirectedEdge(home, about))
   web.add_edge(DirectedEdge(home, contact))
   web.add_edge(DirectedEdge(about, home))
   
   # Find outgoing links
   home_links = list(web.successors(home))
   print(f"Links from home: {[p.data for p in home_links]}")

When to Use Each Graph Type
============================

Decision Guide
--------------

.. mermaid::

   graph TD
       A{What's your graph?}
       
       A -->|Undirected| B{Need weights?}
       A -->|Directed| C{Need weights?}
       
       B -->|No| D[Graph]
       B -->|Yes| E[WeightedGraph]
       
       C -->|No| F[DirectedGraph]
       C -->|Yes| G[WeightedDirectedGraph]
       
       D -->|Sparse| H[AdjacencyListGraph]
       D -->|Dense| I[AdjacencyMatrixGraph]
       
       style D fill:#2ecc71
       style E fill:#3498db
       style F fill:#f39c12
       style G fill:#e74c3c
       style H fill:#1abc9c
       style I fill:#9b59b6

**Selection criteria:**

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Graph Type
     - Use When...
   * - **Graph**
     - Symmetric relationships, no direction needed
   * - **DirectedGraph**
     - Asymmetric relationships, direction matters
   * - **WeightedGraph**
     - Distances, costs, or similarities between nodes
   * - **WeightedDirectedGraph**
     - Flow networks, shortest paths with direction
   * - **AdjacencyListGraph**
     - Sparse graphs (E << V²), memory efficient
   * - **AdjacencyMatrixGraph**
     - Dense graphs (E ≈ V²), fast edge lookups

Real-World Application Domains
===============================

Social Networks
---------------

- **Friendship graphs**: Undirected Graph
- **Follow relationships**: DirectedGraph
- **Influence weights**: WeightedDirectedGraph

Transportation
--------------

- **Road networks**: WeightedGraph (bidirectional roads)
- **Flight routes**: WeightedDirectedGraph (one-way, with distances)
- **Public transit**: DirectedGraph (scheduled routes)

Computer Science
----------------

- **Dependencies**: DirectedGraph (package/module dependencies)
- **Call graphs**: DirectedGraph (function calls)
- **Data flow**: DirectedGraph (information flow)

Biology
-------

- **Protein interactions**: Graph (undirected interactions)
- **Food webs**: DirectedGraph (predator-prey)
- **Neural networks**: WeightedDirectedGraph (synaptic weights)

Web & Internet
--------------

- **Hyperlinks**: DirectedGraph (one-way links)
- **Social media**: DirectedGraph (follows, likes)
- **Network topology**: Graph (physical connections)

Performance Guidelines
======================

Time Complexity Summary
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 25 15 15 15 15 15

   * - Operation
     - Add Node
     - Add Edge
     - Check Edge
     - Get Neighbors
     - Space
   * - **AdjacencyList**
     - O(1)
     - O(1)
     - O(deg)
     - O(deg)
     - O(V+E)
   * - **AdjacencyMatrix**
     - O(1)
     - O(1)
     - O(1)
     - O(V)
     - O(V²)
   * - **Graph**
     - O(1)
     - O(1)
     - O(deg)
     - O(deg)
     - O(V+E)

**Key insights:**

- **Adjacency List**: Best for sparse graphs, efficient neighbor iteration
- **Adjacency Matrix**: Best for dense graphs, O(1) edge existence checks
- **deg**: Degree of node (typically << V for sparse graphs)

Space Complexity
----------------

All graph structures store:

* **Nodes**: O(V) space
* **Edges**: 
  * Adjacency List: O(E)
  * Adjacency Matrix: O(V²)
* **Additional data**: O(V + E) for node/edge data

Graph Algorithms Support
========================

Common Graph Algorithms
-----------------------

The graph structures support efficient implementation of:

**Traversal Algorithms:**

- Breadth-First Search (BFS): O(V + E)
- Depth-First Search (DFS): O(V + E)

**Shortest Path:**

- Dijkstra's Algorithm: O((V + E) log V)
- Bellman-Ford: O(VE)

**Minimum Spanning Tree:**

- Kruskal's Algorithm: O(E log E)
- Prim's Algorithm: O((V + E) log V)

**Connectivity:**

- Connected Components: O(V + E)
- Strongly Connected Components: O(V + E)

**Topological Sort:**

- DAG Ordering: O(V + E)

Example: BFS Implementation
----------------------------

.. code-block:: python

   from sds.graph import Graph, GraphNode
   from collections import deque

   def bfs(graph: Graph, start: GraphNode):
       """Breadth-first search traversal."""
       visited = {start}
       queue = deque([start])
       result = []
       
       while queue:
           node = queue.popleft()
           result.append(node.data)
           
           for neighbor in graph.neighbors(node):
               if neighbor not in visited:
                   visited.add(neighbor)
                   queue.append(neighbor)
       
       return result

   # Usage
   g = Graph()
   # ... build graph ...
   traversal = bfs(g, start_node)

Best Practices
==============

Graph Design
------------

✅ **Choose appropriate representation**

.. code-block:: python

   # Sparse graph → Adjacency List
   sparse = Graph()  # O(V + E) space
   
   # Dense graph → Adjacency Matrix
   from sds.graph import AdjacencyMatrixGraph
   dense = AdjacencyMatrixGraph()  # O(V²) space

✅ **Use meaningful node IDs**

.. code-block:: python

   # Good: Semantic IDs
   user = GraphNode(user_data, node_id=f"user_{username}")
   city = GraphNode(city_data, node_id=city_name.lower())
   
   # Acceptable: Auto-generated for anonymous nodes
   temp = GraphNode(temp_data)  # UUID

✅ **Store rich data in nodes and edges**

.. code-block:: python

   # Nodes with data
   node = GraphNode({
       'name': 'Paris',
       'population': 2_165_000,
       'coordinates': (48.8566, 2.3522)
   })
   
   # Edges with data
   edge = WeightedEdge(n1, n2, weight=344, data={
       'mode': 'train',
       'duration_hours': 2.5
   })

Common Pitfalls
---------------

✗ **Don't mix directed and undirected edges**

.. code-block:: python

   # Bad: Inconsistent edge types
   graph.add_edge(Edge(n1, n2))           # Undirected
   graph.add_edge(DirectedEdge(n2, n3))   # Directed - inconsistent!
   
   # Good: Be consistent
   graph = DirectedGraph()
   graph.add_edge(DirectedEdge(n1, n2))
   graph.add_edge(DirectedEdge(n2, n3))

✗ **Don't forget to check for self-loops**

.. code-block:: python

   # Bad: Might create unwanted self-loop
   edge = Edge(node, node)  # Raises ValueError by default
   
   # Good: Explicit handling
   if node1 != node2:
       edge = Edge(node1, node2)
   else:
       edge = Edge(node1, node2, allow_self_loop=True)

✗ **Don't assume graph is connected**

.. code-block:: python

   # Bad: Assuming single component
   for node in graph.nodes():
       process(node)  # Might miss disconnected components
   
   # Good: Check connectivity first
   if graph.is_connected():
       # Process as single component
       pass
   else:
       # Handle multiple components
       pass

Comparison with Other Structures
=================================

Graphs vs Trees
---------------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Aspect
     - Trees
     - Graphs
   * - **Cycles**
     - Never (acyclic)
     - May have cycles
   * - **Parent nodes**
     - Exactly one (except root)
     - Any number
   * - **Structure**
     - Hierarchical
     - Network/mesh
   * - **Use cases**
     - Hierarchies, XML/DOM
     - Networks, relationships

Trees are special cases of graphs (directed, acyclic, connected).

Related Modules
===============

* :doc:`../../guide/graph_structures/index` - User guide for graph structures
* :doc:`../core/index` - Core abstractions
* :doc:`../linear/index` - Linear structures
* :doc:`../tree/index` - Tree structures

See Also
========

External Resources
------------------

* `Wikipedia: Graph (discrete mathematics) <https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)>`_
* `Wikipedia: Graph theory <https://en.wikipedia.org/wiki/Graph_theory>`_
* `VisuAlgo: Graph Data Structures <https://visualgo.net/en/graphds>`_
* `Graph Online <https://graphonline.ru/en/>`_ - Interactive graph visualizer

Interactive Visualizations
--------------------------

* `USFCA Graph Visualization <https://www.cs.usfca.edu/~galles/visualization/>`_
* `Algorithm Visualizer <https://algorithm-visualizer.org/>`_

Academic References
-------------------

.. [1] Cormen, T. H., et al. "Introduction to Algorithms", 3rd Edition, Part VI: Graph Algorithms
.. [2] Sedgewick, R., Wayne, K. "Algorithms", 4th Edition, Chapters 4.1-4.4
.. [3] West, D. B. "Introduction to Graph Theory", 2nd Edition, Prentice Hall
.. [4] Bondy, J. A., Murty, U. S. R. "Graph Theory", Graduate Texts in Mathematics
.. [5] Diestel, R. "Graph Theory", 5th Edition, Springer Graduate Texts in Mathematics

Open Educational Resources
--------------------------

.. [MIT6042] MIT OpenCourseWare. "6.042J Mathematics for Computer Science"
   https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/
   
   Excellent coverage of graph theory fundamentals in lectures 6-10.

.. [StanfordCS161] Stanford University. "CS161: Design and Analysis of Algorithms"
   http://web.stanford.edu/class/cs161/
   
   Comprehensive lecture notes on graph algorithms.

.. [Erickson] Erickson, J. "Algorithms", 2019
   http://jeffe.cs.illinois.edu/teaching/algorithms/
   
   Free textbook with detailed graph algorithms coverage (Chapters 5-8).
