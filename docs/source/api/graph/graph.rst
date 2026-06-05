.. _api_graph_graph:

=====
Graph
=====

.. currentmodule:: sds.graph.graph

Overview
========

The Graph class implements an undirected, unweighted graph using adjacency list representation.
This is the foundational graph structure in SDS-Tools, providing efficient storage and traversal
for sparse graphs.

.. mermaid::

   graph LR
       A[Node A] --- B[Node B]
       A --- C[Node C]
       B --- D[Node D]
       C --- D
       
       style A fill:#e74c3c,stroke:#c0392b,color:#fff
       style B fill:#3498db,stroke:#2980b9,color:#fff
       style C fill:#3498db,stroke:#2980b9,color:#fff
       style D fill:#2ecc71,stroke:#27ae60,color:#fff

Classes
=======

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   Graph

Detailed Documentation
======================

Graph Class
-----------

.. autoclass:: Graph
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __len__, __contains__, __iter__, __repr__, __str__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Properties

   .. autoproperty:: allow_multi_edges

   .. rubric:: Node Operations

   .. automethod:: add_node
   .. automethod:: remove_node
   .. automethod:: has_node
   .. automethod:: get_node_by_id
   .. automethod:: nodes
   .. automethod:: node_count

   .. rubric:: Edge Operations

   .. automethod:: add_edge
   .. automethod:: remove_edge
   .. automethod:: has_edge
   .. automethod:: get_edge
   .. automethod:: edges
   .. automethod:: edge_count

   .. rubric:: Graph Queries

   .. automethod:: neighbors
   .. automethod:: degree
   .. automethod:: is_connected
   .. automethod:: is_empty

   .. rubric:: Utility Methods

   .. automethod:: clear

   .. rubric:: Special Methods

   .. automethod:: __len__
   .. automethod:: __contains__
   .. automethod:: __iter__
   .. automethod:: __repr__
   .. automethod:: __str__

Usage Examples
==============

Basic Operations
----------------

Creating a Graph
^^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.graphs import Graph, GraphNode, Edge

   # Create empty graph
   g = Graph()
   
   # Create with multi-edge support
   mg = Graph(allow_multi_edges=True)
   
   print(g.is_empty())  # Output: True

Adding Nodes
^^^^^^^^^^^^

.. code-block:: python

   from sds.graphs import Graph, GraphNode

   g = Graph()
   
   # Create and add nodes
   n1 = GraphNode("Alice", "user1")
   n2 = GraphNode("Bob", "user2")
   n3 = GraphNode("Carol", "user3")
   
   g.add_node(n1)
   g.add_node(n2)
   g.add_node(n3)
   
   print(f"Nodes: {g.node_count()}")  # Output: 3

Adding Edges
^^^^^^^^^^^^

.. code-block:: python

   from sds.graphs import Edge

   # Connect nodes with edges
   e1 = Edge(n1, n2)
   e2 = Edge(n2, n3)
   e3 = Edge(n1, n3)
   
   g.add_edge(e1)
   g.add_edge(e2)
   g.add_edge(e3)
   
   print(f"Edges: {g.edge_count()}")  # Output: 3

Querying the Graph
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Check if nodes exist
   print(g.has_node(n1))  # Output: True
   print(n1 in g)         # Output: True
   
   # Check if edge exists
   print(g.has_edge(n1, n2))  # Output: True
   print(g.has_edge(n1, GraphNode("Unknown")))  # Output: False
   
   # Get node by ID
   node = g.get_node_by_id("user1")
   print(node.data)  # Output: Alice

Graph Traversal
^^^^^^^^^^^^^^^

.. code-block:: python

   # Iterate over all nodes
   for node in g:
       print(node.data)
   
   # Get all nodes explicitly
   all_nodes = list(g.nodes())
   print(f"All nodes: {[n.data for n in all_nodes]}")
   
   # Get all edges
   all_edges = list(g.edges())
   print(f"Total edges: {len(all_edges)}")

Neighbors and Degree
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Get neighbors of a node
   neighbors = list(g.neighbors(n1))
   print(f"{n1.data}'s neighbors: {[n.data for n in neighbors]}")
   # Output: Alice's neighbors: ['Bob', 'Carol']
   
   # Get node degree
   degree = g.degree(n1)
   print(f"Degree of {n1.data}: {degree}")  # Output: 2

Connectivity
^^^^^^^^^^^^

.. code-block:: python

   # Check if graph is connected
   print(g.is_connected())  # Output: True
   
   # Add isolated node
   n4 = GraphNode("Dave", "user4")
   g.add_node(n4)
   
   print(g.is_connected())  # Output: False

Removing Elements
^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Remove an edge
   g.remove_edge(e1)
   print(g.has_edge(n1, n2))  # Output: False
   
   # Remove a node (removes incident edges too)
   g.remove_node(n3)
   print(g.node_count())  # Output: 3
   print(g.edge_count())   # Output: 1

Multi-Edges
^^^^^^^^^^^

.. code-block:: python

   # Create multigraph
   mg = Graph(allow_multi_edges=True)
   
   mg.add_node(n1)
   mg.add_node(n2)
   
   # Add multiple edges between same nodes
   e1 = Edge(n1, n2, data="email")
   e2 = Edge(n1, n2, data="phone")
   e3 = Edge(n1, n2, data="meeting")
   
   mg.add_edge(e1)
   mg.add_edge(e2)
   mg.add_edge(e3)
   
   print(f"Edges: {mg.edge_count()}")    # Output: 3
   print(f"Degree of {n1.data}: {mg.degree(n1)}")  # Output: 3

Real-World Examples
===================

Example 1: Social Network
--------------------------

Modeling friendships:

.. code-block:: python

   from sds.graphs import Graph, GraphNode, Edge

   class SocialNetwork:
       """Simple social network using undirected graph."""
       
       def __init__(self):
           self.graph = Graph()
           self.users = {}
       
       def add_user(self, user_id, name):
           """Add a user to the network."""
           node = GraphNode(name, user_id)
           self.graph.add_node(node)
           self.users[user_id] = node
       
       def add_friendship(self, user1_id, user2_id):
           """Create friendship between two users."""
           user1 = self.users[user1_id]
           user2 = self.users[user2_id]
           edge = Edge(user1, user2)
           self.graph.add_edge(edge)
       
       def get_friends(self, user_id):
           """Get all friends of a user."""
           user = self.users[user_id]
           return [n.data for n in self.graph.neighbors(user)]
       
       def are_friends(self, user1_id, user2_id):
           """Check if two users are friends."""
           user1 = self.users[user1_id]
           user2 = self.users[user2_id]
           return self.graph.has_edge(user1, user2)
       
       def friend_count(self, user_id):
           """Get number of friends."""
           user = self.users[user_id]
           return self.graph.degree(user)
   
   # Usage
   network = SocialNetwork()
   
   # Add users
   network.add_user("u1", "Alice")
   network.add_user("u2", "Bob")
   network.add_user("u3", "Carol")
   network.add_user("u4", "Dave")
   
   # Create friendships
   network.add_friendship("u1", "u2")
   network.add_friendship("u1", "u3")
   network.add_friendship("u2", "u3")
   network.add_friendship("u3", "u4")
   
   # Query network
   print(f"Alice's friends: {network.get_friends('u1')}")
   print(f"Are Alice and Bob friends? {network.are_friends('u1', 'u2')}")
   print(f"Carol has {network.friend_count('u3')} friends")

Example 2: Network Topology
----------------------------

Computer network connections:

.. code-block:: python

   from sds.graphs import Graph, GraphNode, Edge

   class NetworkTopology:
       """Model computer network topology."""
       
       def __init__(self):
           self.graph = Graph()
           self.devices = {}
       
       def add_device(self, device_id, device_type, ip_address):
           """Add network device."""
           data = {
               'type': device_type,
               'ip': ip_address
           }
           node = GraphNode(data, device_id)
           self.graph.add_node(node)
           self.devices[device_id] = node
       
       def connect_devices(self, dev1_id, dev2_id, bandwidth=None):
           """Connect two devices."""
           dev1 = self.devices[dev1_id]
           dev2 = self.devices[dev2_id]
           edge = Edge(dev1, dev2, data={'bandwidth': bandwidth})
           self.graph.add_edge(edge)
       
       def get_connected_devices(self, device_id):
           """Get all devices connected to this one."""
           device = self.devices[device_id]
           neighbors = list(self.graph.neighbors(device))
           return [(n.id, n.data) for n in neighbors]
       
       def is_network_connected(self):
           """Check if all devices can reach each other."""
           return self.graph.is_connected()
       
       def device_connectivity(self, device_id):
           """Get number of direct connections."""
           device = self.devices[device_id]
           return self.graph.degree(device)
   
   # Usage
   network = NetworkTopology()
   
   # Add devices
   network.add_device("r1", "router", "192.168.1.1")
   network.add_device("s1", "switch", "192.168.1.2")
   network.add_device("s2", "switch", "192.168.1.3")
   network.add_device("pc1", "computer", "192.168.1.100")
   network.add_device("pc2", "computer", "192.168.1.101")
   
   # Connect devices
   network.connect_devices("r1", "s1", bandwidth="1Gbps")
   network.connect_devices("r1", "s2", bandwidth="1Gbps")
   network.connect_devices("s1", "pc1", bandwidth="100Mbps")
   network.connect_devices("s2", "pc2", bandwidth="100Mbps")
   
   # Query network
   print(f"Router connections: {network.device_connectivity('r1')}")
   print(f"Network connected: {network.is_network_connected()}")

Example 3: Course Prerequisites
--------------------------------

Modeling course dependencies:

.. code-block:: python

   from sds.graphs import Graph, GraphNode, Edge

   class CoursePrerequisites:
       """Model course prerequisite relationships (simplified)."""
       
       def __init__(self):
           # Note: Using undirected graph - in reality, use DirectedGraph
           self.graph = Graph()
           self.courses = {}
       
       def add_course(self, course_id, name, credits):
           """Add a course."""
           data = {
               'name': name,
               'credits': credits
           }
           node = GraphNode(data, course_id)
           self.graph.add_node(node)
           self.courses[course_id] = node
       
       def add_related_course(self, course1_id, course2_id):
           """Link related courses."""
           course1 = self.courses[course1_id]
           course2 = self.courses[course2_id]
           edge = Edge(course1, course2)
           self.graph.add_edge(edge)
       
       def get_related_courses(self, course_id):
           """Get courses related to this one."""
           course = self.courses[course_id]
           neighbors = list(self.graph.neighbors(course))
           return [(n.id, n.data['name']) for n in neighbors]
       
       def total_courses(self):
           """Get total number of courses."""
           return self.graph.node_count()
   
   # Usage
   catalog = CoursePrerequisites()
   
   # Add courses
   catalog.add_course("CS101", "Intro to Programming", 3)
   catalog.add_course("CS102", "Data Structures", 3)
   catalog.add_course("CS201", "Algorithms", 3)
   catalog.add_course("MATH101", "Calculus I", 4)
   
   # Add relationships
   catalog.add_related_course("CS101", "CS102")
   catalog.add_related_course("CS102", "CS201")
   catalog.add_related_course("MATH101", "CS201")
   
   # Query
   related = catalog.get_related_courses("CS102")
   print(f"CS102 related courses: {related}")

Performance Characteristics
===========================

Time Complexity
---------------

.. list-table::
   :header-rows: 1
   :widths: 40 20 40

   * - Operation
     - Complexity
     - Notes
   * - ``add_node(node)``
     - O(1)
     - Hash table insertion
   * - ``remove_node(node)``
     - O(degree + E)
     - Must update adjacency lists
   * - ``has_node(node)``
     - O(1)
     - Hash table lookup
   * - ``add_edge(edge)``
     - O(1) or O(degree)
     - O(degree) if checking duplicates
   * - ``remove_edge(edge)``
     - O(E)
     - Must find edge in list
   * - ``has_edge(n1, n2)``
     - O(1) amortized
     - Set membership check
   * - ``get_edge(n1, n2)``
     - O(E)
     - Linear search in edge list
   * - ``neighbors(node)``
     - O(degree)
     - Iterate adjacency set
   * - ``degree(node)``
     - O(1) or O(E)
     - O(1) for simple graph
   * - ``is_connected()``
     - O(V + E)
     - BFS traversal, cached
   * - ``nodes()``
     - O(V)
     - Iterate all nodes
   * - ``edges()``
     - O(E)
     - Iterate all edges
   * - ``clear()``
     - O(1)
     - Clear references

Space Complexity
----------------

* **Node storage**: O(V) where V = number of vertices
* **Adjacency lists**: O(V + E) where E = number of edges
* **Edge list**: O(E)
* **Total**: O(V + E)

This is optimal for sparse graphs where E << V².

Comparison with Other Representations
======================================

.. list-table:: Graph Representation Comparison
   :header-rows: 1
   :widths: 25 25 25 25

   * - Operation
     - Adjacency List
     - Adjacency Matrix
     - Edge List
   * - **Space**
     - O(V + E)
     - O(V²)
     - O(E)
   * - **Add Edge**
     - O(1)
     - O(1)
     - O(1)
   * - **Has Edge**
     - O(degree)
     - O(1)
     - O(E)
   * - **Remove Edge**
     - O(E)
     - O(1)
     - O(E)
   * - **Get Neighbors**
     - O(degree)
     - O(V)
     - O(E)
   * - **Best For**
     - Sparse graphs
     - Dense graphs
     - Simple storage

Graph Type Comparison
=====================

.. mermaid::

   graph TB
       subgraph "Undirected Graph (this class)"
       A1[A] --- B1[B]
       A1 --- C1[C]
       B1 --- C1
       end
       
       subgraph "Directed Graph"
       A2[A] --> B2[B]
       A2 --> C2[C]
       B2 --> C2
       end
       
       subgraph "Weighted Graph"
       A3[A] ---|5| B3[B]
       A3 ---|3| C3[C]
       B3 ---|7| C3
       end

Best Practices
==============

Do's
----

✅ **Use for sparse graphs**

.. code-block:: python

   # Adjacency list is efficient when E << V²
   # Good for social networks, web graphs, etc.
   g = Graph()

✅ **Check node existence before operations**

.. code-block:: python

   if g.has_node(node):
       neighbors = list(g.neighbors(node))
   else:
       print("Node not found")

✅ **Use cached connectivity**

.. code-block:: python

   # is_connected() caches result until graph changes
   connected = g.is_connected()  # Cached on subsequent calls

✅ **Iterate efficiently**

.. code-block:: python

   # Direct iteration over nodes
   for node in g:
       process_node(node)
   
   # Iterate over edges when needed
   for edge in g.edges():
       process_edge(edge)

Don'ts
------

❌ **Don't add duplicate nodes**

.. code-block:: python

   # Bad: Raises ValueError
   g.add_node(node)
   g.add_node(node)  # Error!
   
   # Good: Check first
   if not g.has_node(node):
       g.add_node(node)

❌ **Don't modify during iteration**

.. code-block:: python

   # Bad: Undefined behavior
   for node in g:
       g.remove_node(node)
   
   # Good: Collect then modify
   nodes_to_remove = list(g)
   for node in nodes_to_remove:
       g.remove_node(node)

❌ **Don't use for dense graphs**

.. code-block:: python

   # Bad: Adjacency list wastes space for dense graphs
   # If E ≈ V², use adjacency matrix instead
   
   # Good: Use AdjacencyMatrixGraph for dense graphs
   from sds.graphs import AdjacencyMatrixGraph
   dense_graph = AdjacencyMatrixGraph(max_nodes=100)

Common Pitfalls
===============

1. **Forgetting graph is undirected**

.. code-block:: python

   # Adding edge A-B also creates B-A
   g.add_edge(Edge(node_a, node_b))
   print(g.has_edge(node_b, node_a))  # True!

2. **Not handling multi-edges correctly**

.. code-block:: python

   # Simple graph (default) - duplicate edges raise error
   g = Graph()  # allow_multi_edges=False
   g.add_edge(Edge(n1, n2))
   g.add_edge(Edge(n1, n2))  # ValueError!
   
   # Use multigraph if needed
   mg = Graph(allow_multi_edges=True)
   mg.add_edge(Edge(n1, n2))
   mg.add_edge(Edge(n1, n2))  # OK

3. **Memory leaks with large graphs**

.. code-block:: python

   # Clear when done
   large_graph.clear()
   large_graph = None

See Also
========

* :doc:`directed` - Directed and undirected graphs with validation
* :doc:`weighted` - Weighted graphs
* :doc:`adjacency` - Alternative representations
* :doc:`../../guide/graph_structures/general` - User guide

References
==========

.. [1] Cormen, T. H., et al. "Introduction to Algorithms", 3rd Edition, Chapter 22
.. [2] Sedgewick, R., Wayne, K. "Algorithms", 4th Edition, Chapter 4
.. [3] West, D. B. "Introduction to Graph Theory", 2nd Edition, Pearson, 2001
