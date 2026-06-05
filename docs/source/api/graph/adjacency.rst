.. _api_graph_adjacency:

=========================
Adjacency Representations
=========================

.. currentmodule:: sds.graph.adjacency

Overview
========

This module provides explicit adjacency-based graph implementations that optimize
for different use cases. While the base Graph class already uses adjacency lists
internally, these classes make the representation explicit and provide specialized
optimizations.

.. mermaid::

   graph TB
       subgraph "Adjacency List"
       A["Node 0"] --> L0["[1, 2]"]
       B["Node 1"] --> L1["[0, 2, 3]"]
       C["Node 2"] --> L2["[0, 1]"]
       D["Node 3"] --> L3["[1]"]
       end
       
       subgraph "Adjacency Matrix"
       M["Matrix"] --> R0["[0,1,1,0]"]
       M --> R1["[1,0,1,1]"]
       M --> R2["[1,1,0,0]"]
       M --> R3["[0,1,0,0]"]
       end
       
       style A fill:#e74c3c,color:#fff
       style M fill:#3498db,color:#fff

Classes
=======

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   AdjacencyListGraph
   AdjacencyMatrixGraph

Detailed Documentation
======================

AdjacencyListGraph
------------------

.. autoclass:: AdjacencyListGraph
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

   .. rubric:: Edge Operations

   .. automethod:: add_edge
   .. automethod:: remove_edge
   .. automethod:: has_edge
   .. automethod:: get_edge

   .. rubric:: Adjacency Operations

   .. automethod:: get_adjacency_list
   .. automethod:: neighbors
   .. automethod:: degree

   .. rubric:: Traversal

   .. automethod:: nodes
   .. automethod:: edges

   .. rubric:: Graph Properties

   .. automethod:: node_count
   .. automethod:: edge_count
   .. automethod:: is_connected
   .. automethod:: is_empty
   .. automethod:: clear

   .. rubric:: Special Methods

   .. automethod:: __len__
   .. automethod:: __contains__
   .. automethod:: __iter__
   .. automethod:: __repr__
   .. automethod:: __str__

AdjacencyMatrixGraph
--------------------

.. autoclass:: AdjacencyMatrixGraph
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __len__, __contains__, __iter__, __repr__, __str__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Properties

   .. autoproperty:: max_nodes
   .. autoproperty:: allow_multi_edges

   .. rubric:: Node Operations

   .. automethod:: add_node
   .. automethod:: remove_node
   .. automethod:: has_node
   .. automethod:: get_node_by_id

   .. rubric:: Edge Operations

   .. automethod:: add_edge
   .. automethod:: remove_edge
   .. automethod:: has_edge
   .. automethod:: get_edge

   .. rubric:: Matrix Operations

   .. automethod:: get_matrix
   .. automethod:: neighbors
   .. automethod:: degree

   .. rubric:: Traversal

   .. automethod:: nodes
   .. automethod:: edges

   .. rubric:: Graph Properties

   .. automethod:: node_count
   .. automethod:: edge_count
   .. automethod:: is_connected
   .. automethod:: is_empty
   .. automethod:: clear

   .. rubric:: Special Methods

   .. automethod:: __len__
   .. automethod:: __contains__
   .. automethod:: __iter__
   .. automethod:: __repr__
   .. automethod:: __str__

Usage Examples
==============

AdjacencyListGraph Examples
----------------------------

Basic Operations
^^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.graph import AdjacencyListGraph, GraphNode, Edge

   # Create adjacency list graph
   graph = AdjacencyListGraph()

   # Add nodes
   n1 = GraphNode("A", "n1")
   n2 = GraphNode("B", "n2")
   n3 = GraphNode("C", "n3")
   
   graph.add_node(n1)
   graph.add_node(n2)
   graph.add_node(n3)

   # Add edges
   graph.add_edge(Edge(n1, n2))
   graph.add_edge(Edge(n2, n3))
   graph.add_edge(Edge(n1, n3))

   print(f"Nodes: {graph.node_count()}")  # Output: 3
   print(f"Edges: {graph.edge_count()}")  # Output: 3

Accessing Adjacency Lists
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Get adjacency list for a node
   adj_list = graph.get_adjacency_list("n1")
   print(f"Node n1 is connected to: {adj_list}")
   # Output: {'n2', 'n3'}

   # Check neighbors
   for neighbor in graph.neighbors(n1):
       print(f"Neighbor: {neighbor.id}")
   # Output:
   # Neighbor: n2
   # Neighbor: n3

   # Get degree
   degree = graph.degree(n1)
   print(f"Degree of n1: {degree}")  # Output: 2

Multigraph Support
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Create multigraph (allows parallel edges)
   multigraph = AdjacencyListGraph(allow_multi_edges=True)
   
   multigraph.add_node(n1)
   multigraph.add_node(n2)
   
   # Add multiple edges between same nodes
   multigraph.add_edge(Edge(n1, n2, data="road1"))
   multigraph.add_edge(Edge(n1, n2, data="road2"))
   multigraph.add_edge(Edge(n1, n2, data="road3"))
   
   print(f"Edges: {multigraph.edge_count()}")  # Output: 3
   print(f"Degree n1: {multigraph.degree(n1)}")  # Output: 3

Connectivity Check
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Check if graph is connected
   graph = AdjacencyListGraph()
   
   # Create disconnected graph
   n1 = GraphNode("A", "n1")
   n2 = GraphNode("B", "n2")
   n3 = GraphNode("C", "n3")
   n4 = GraphNode("D", "n4")
   
   graph.add_node(n1)
   graph.add_node(n2)
   graph.add_node(n3)
   graph.add_node(n4)
   
   graph.add_edge(Edge(n1, n2))
   graph.add_edge(Edge(n3, n4))
   
   print(graph.is_connected())  # Output: False
   
   # Connect the components
   graph.add_edge(Edge(n2, n3))
   print(graph.is_connected())  # Output: True

AdjacencyMatrixGraph Examples
------------------------------

Creating Matrix Graph
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.graph import AdjacencyMatrixGraph, GraphNode, Edge

   # Create matrix graph with max 10 nodes
   graph = AdjacencyMatrixGraph(max_nodes=10)

   # Add nodes
   n1 = GraphNode("A", "n1")
   n2 = GraphNode("B", "n2")
   n3 = GraphNode("C", "n3")
   
   graph.add_node(n1)
   graph.add_node(n2)
   graph.add_node(n3)

   # Add edges
   graph.add_edge(Edge(n1, n2))
   graph.add_edge(Edge(n2, n3))

   print(f"Capacity: {graph.max_nodes}")  # Output: 10
   print(f"Used: {graph.node_count()}")   # Output: 3

Matrix Access
^^^^^^^^^^^^^

.. code-block:: python

   # Get adjacency matrix
   matrix = graph.get_matrix()
   
   print("Adjacency Matrix:")
   for row in matrix:
       print(row)
   # Output:
   # [0, 1, 0]
   # [1, 0, 1]
   # [0, 1, 0]

   # Check edge existence - O(1)!
   print(graph.has_edge(n1, n2))  # Output: True
   print(graph.has_edge(n1, n3))  # Output: False

Dense Graph Operations
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Matrix graph is efficient for dense graphs
   dense_graph = AdjacencyMatrixGraph(max_nodes=5)
   
   # Create complete graph K5
   nodes = [GraphNode(f"N{i}", f"n{i}") for i in range(5)]
   for node in nodes:
       dense_graph.add_node(node)
   
   # Connect all pairs
   for i in range(5):
       for j in range(i + 1, 5):
           dense_graph.add_edge(Edge(nodes[i], nodes[j]))
   
   print(f"Complete graph K5:")
   print(f"Nodes: {dense_graph.node_count()}")  # Output: 5
   print(f"Edges: {dense_graph.edge_count()}")  # Output: 10
   
   # Every node has degree 4
   for node in nodes:
       print(f"{node.id}: degree {dense_graph.degree(node)}")

Multigraph with Matrix
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Matrix can store edge counts for multigraphs
   multigraph = AdjacencyMatrixGraph(max_nodes=5, allow_multi_edges=True)
   
   n1 = GraphNode("A", "n1")
   n2 = GraphNode("B", "n2")
   
   multigraph.add_node(n1)
   multigraph.add_node(n2)
   
   # Add multiple edges
   for i in range(3):
       multigraph.add_edge(Edge(n1, n2))
   
   # Matrix stores count
   matrix = multigraph.get_matrix()
   print(f"Matrix[0][1]: {matrix[0][1]}")  # Output: 3

Real-World Examples
===================

Example 1: Social Network (Adjacency List)
-------------------------------------------

.. code-block:: python

   from sds.graph import AdjacencyListGraph, GraphNode, Edge

   class SocialNetwork:
       """Social network using adjacency list (sparse graph)."""
       
       def __init__(self):
           self.graph = AdjacencyListGraph()
           self.users = {}
       
       def add_user(self, user_id, name):
           """Add a user to the network."""
           node = GraphNode(name, user_id)
           self.graph.add_node(node)
           self.users[user_id] = node
       
       def add_friendship(self, user1_id, user2_id):
           """Create friendship (bidirectional edge)."""
           if user1_id not in self.users or user2_id not in self.users:
               raise ValueError("User not found")
           
           user1 = self.users[user1_id]
           user2 = self.users[user2_id]
           
           self.graph.add_edge(Edge(user1, user2))
       
       def get_friends(self, user_id):
           """Get list of friends."""
           if user_id not in self.users:
               return []
           
           user = self.users[user_id]
           return [neighbor.data for neighbor in self.graph.neighbors(user)]
       
       def friend_count(self, user_id):
           """Get number of friends."""
           if user_id not in self.users:
               return 0
           
           user = self.users[user_id]
           return self.graph.degree(user)
       
       def suggest_friends(self, user_id):
           """Suggest friends of friends."""
           if user_id not in self.users:
               return []
           
           user = self.users[user_id]
           suggestions = set()
           
           # Get friends of friends
           for friend in self.graph.neighbors(user):
               for friend_of_friend in self.graph.neighbors(friend):
                   if friend_of_friend.id != user_id and friend_of_friend.id not in self.graph.get_adjacency_list(user_id):
                       suggestions.add(friend_of_friend.data)
           
           return list(suggestions)
   
   # Usage
   network = SocialNetwork()
   
   # Add users
   network.add_user("alice", "Alice Smith")
   network.add_user("bob", "Bob Jones")
   network.add_user("carol", "Carol White")
   network.add_user("dave", "Dave Brown")
   
   # Add friendships
   network.add_friendship("alice", "bob")
   network.add_friendship("bob", "carol")
   network.add_friendship("carol", "dave")
   
   # Query network
   print(f"Alice's friends: {network.get_friends('alice')}")
   print(f"Bob has {network.friend_count('bob')} friends")
   print(f"Suggestions for Alice: {network.suggest_friends('alice')}")

Example 2: Distance Matrix (Adjacency Matrix)
----------------------------------------------

.. code-block:: python

   from sds.graph import AdjacencyMatrixGraph, GraphNode, Edge

   class CityDistanceMap:
       """City distances using adjacency matrix (dense, small graph)."""
       
       def __init__(self, max_cities=50):
           self.graph = AdjacencyMatrixGraph(max_nodes=max_cities)
           self.cities = {}
           self.city_indices = {}
       
       def add_city(self, city_id, name):
           """Add a city."""
           node = GraphNode(name, city_id)
           self.graph.add_node(node)
           self.cities[city_id] = node
           self.city_indices[city_id] = len(self.city_indices)
       
       def add_route(self, city1_id, city2_id, distance):
           """Add route between cities."""
           if city1_id not in self.cities or city2_id not in self.cities:
               raise ValueError("City not found")
           
           city1 = self.cities[city1_id]
           city2 = self.cities[city2_id]
           
           # Store distance as edge data
           self.graph.add_edge(Edge(city1, city2, data=distance))
       
       def get_distance(self, city1_id, city2_id):
           """Get distance between cities - O(1) lookup!"""
           if city1_id not in self.cities or city2_id not in self.cities:
               return None
           
           city1 = self.cities[city1_id]
           city2 = self.cities[city2_id]
           
           edge = self.graph.get_edge(city1, city2)
           return edge.data if edge else None
       
       def get_distance_matrix(self):
           """Get full distance matrix."""
           matrix = self.graph.get_matrix()
           
           # Convert to distances
           n = self.graph.node_count()
           dist_matrix = [[0] * n for _ in range(n)]
           
           for edge in self.graph.edges():
               i = self.city_indices[edge.node1.id]
               j = self.city_indices[edge.node2.id]
               dist_matrix[i][j] = edge.data
               dist_matrix[j][i] = edge.data
           
           return dist_matrix
       
       def nearest_cities(self, city_id, n=3):
           """Find n nearest cities."""
           if city_id not in self.cities:
               return []
           
           city = self.cities[city_id]
           distances = []
           
           for neighbor in self.graph.neighbors(city):
               edge = self.graph.get_edge(city, neighbor)
               distances.append((neighbor.data, edge.data))
           
           distances.sort(key=lambda x: x[1])
           return distances[:n]
   
   # Usage
   distance_map = CityDistanceMap(max_cities=10)
   
   # Add cities
   distance_map.add_city("paris", "Paris")
   distance_map.add_city("london", "London")
   distance_map.add_city("berlin", "Berlin")
   distance_map.add_city("rome", "Rome")
   
   # Add routes with distances (km)
   distance_map.add_route("paris", "london", 344)
   distance_map.add_route("paris", "berlin", 878)
   distance_map.add_route("paris", "rome", 1105)
   distance_map.add_route("london", "berlin", 932)
   distance_map.add_route("berlin", "rome", 1184)
   
   # Query distances - O(1)!
   print(f"Paris to London: {distance_map.get_distance('paris', 'london')} km")
   print(f"Nearest to Paris: {distance_map.nearest_cities('paris', 2)}")

Performance Characteristics
===========================

Time Complexity
---------------

.. list-table::
   :header-rows: 1
   :widths: 30 20 20 30

   * - Operation
     - Adjacency List
     - Adjacency Matrix
     - Notes
   * - **add_node**
     - O(1)
     - O(1)
     - Direct insertion
   * - **remove_node**
     - O(degree + E)
     - O(V²)
     - Matrix must compact
   * - **add_edge**
     - O(1)
     - O(1)
     - Both are constant
   * - **remove_edge**
     - O(degree)
     - O(1)
     - Matrix is faster
   * - **has_edge**
     - O(1) amortized
     - O(1)
     - Matrix guaranteed O(1)
   * - **get_neighbors**
     - O(degree)
     - O(V)
     - Must scan matrix row
   * - **degree**
     - O(1) amortized
     - O(V) or O(1)\*
     - \*O(1) if count stored
   * - **space**
     - O(V + E)
     - O(V²)
     - Matrix uses more space

Space Complexity
----------------

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - Graph Type
     - Adjacency List
     - Adjacency Matrix
   * - **Sparse (E << V²)**
     - O(V + E) - Efficient
     - O(V²) - Wasteful
   * - **Dense (E ≈ V²)**
     - O(V²)
     - O(V²)
   * - **Complete (E = V(V-1)/2)**
     - O(V²)
     - O(V²) - Same

When to Use Each
================

Use Adjacency List When
------------------------

âœ… **Sparse graphs** (few edges relative to nodes)

.. code-block:: python

   # Social network: most people have < 1000 friends
   # V = 1 million users, E ≈ 50 million friendships
   # List: 51M storage, Matrix: 1T storage
   network = AdjacencyListGraph()

âœ… **Need to iterate neighbors frequently**

.. code-block:: python

   # Fast neighbor iteration
   for neighbor in graph.neighbors(node):
       process(neighbor)

âœ… **Unknown number of nodes**

.. code-block:: python

   # Dynamic graph - no max size needed
   graph = AdjacencyListGraph()

Use Adjacency Matrix When
--------------------------

âœ… **Dense graphs** (many edges)

.. code-block:: python

   # Complete or near-complete graphs
   # K100 graph: 100 nodes, 4950 edges
   complete_graph = AdjacencyMatrixGraph(max_nodes=100)

âœ… **Need O(1) edge lookup**

.. code-block:: python

   # Fast edge existence check
   if matrix_graph.has_edge(n1, n2):  # O(1)
       # Adjacency list would be O(degree)

âœ… **Fixed, small number of nodes**

.. code-block:: python

   # City distance map: 50 cities max
   cities = AdjacencyMatrixGraph(max_nodes=50)

âœ… **Graph algorithms needing matrix operations**

.. code-block:: python

   # Floyd-Warshall, matrix multiplication algorithms
   matrix = graph.get_matrix()
   # Perform matrix operations

Implementation Details
======================

Adjacency List Internal Structure
----------------------------------

.. code-block:: text

   AdjacencyListGraph storage:

   _nodes: {
       "n1": GraphNode("A", "n1"),
       "n2": GraphNode("B", "n2"),
       "n3": GraphNode("C", "n3")
   }

   _adjacency_list: {
       "n1": {"n2", "n3"},
       "n2": {"n1", "n3"},
       "n3": {"n1", "n2"}
   }

   _edges: [
       Edge(n1, n2),
       Edge(n2, n3),
       Edge(n1, n3)
   ]

Adjacency Matrix Internal Structure
------------------------------------

.. code-block:: text

   AdjacencyMatrixGraph storage:

   _matrix: [
       [0, 1, 1, 0, ...],  # Node 0 connections
       [1, 0, 1, 0, ...],  # Node 1 connections
       [1, 1, 0, 0, ...],  # Node 2 connections
       [0, 0, 0, 0, ...],
       ...
   ]

   _node_indices: {
       "n1": 0,  # Maps node ID to matrix index
       "n2": 1,
       "n3": 2
   }

   _index_to_node: {
       0: "n1",  # Reverse mapping
       1: "n2",
       2: "n3"
   }

Best Practices
==============

Do's
----

âœ… **Choose representation based on density**

.. code-block:: python

   # Sparse: use list
   if edges < nodes * nodes / 2:
       graph = AdjacencyListGraph()
   # Dense: use matrix
   else:
       graph = AdjacencyMatrixGraph(max_nodes=n)

âœ… **Use matrix for small, complete graphs**

.. code-block:: python

   # Perfect for small, dense graphs
   graph = AdjacencyMatrixGraph(max_nodes=20)

âœ… **Leverage O(1) operations**

.. code-block:: python

   # Matrix: O(1) edge check
   if matrix_graph.has_edge(n1, n2):
       # Very fast!
   
   # List: O(1) neighbor iteration
   for neighbor in list_graph.neighbors(node):
       # Efficient iteration!

Don'ts
------

âŒ **Don't use matrix for large sparse graphs**

.. code-block:: python

   # Bad: Wastes memory
   graph = AdjacencyMatrixGraph(max_nodes=100000)
   # 10 billion matrix cells for sparse graph!

âŒ **Don't use list if you need fast edge lookup**

.. code-block:: python

   # Bad: Slow edge checks
   list_graph = AdjacencyListGraph()
   # has_edge is O(degree), not O(1)

âŒ **Don't exceed matrix capacity**

.. code-block:: python

   matrix = AdjacencyMatrixGraph(max_nodes=10)
   # Will fail if you try to add 11th node

Common Pitfalls
===============

1. **Forgetting matrix capacity**

.. code-block:: python

   try:
       matrix = AdjacencyMatrixGraph(max_nodes=5)
       for i in range(10):  # Oops!
           matrix.add_node(GraphNode(i, f"n{i}"))
   except ValueError as e:
       print(f"Error: {e}")

2. **Using matrix for dynamic graphs**

.. code-block:: python

   # Bad: Don't know final size
   matrix = AdjacencyMatrixGraph(max_nodes=1000)  # Guess?
   
   # Good: List handles dynamic size
   list_graph = AdjacencyListGraph()

3. **Not considering space-time tradeoff**

.. code-block:: python

   # Matrix: More space, faster edge lookup
   # List: Less space, faster neighbor iteration
   # Choose based on your use case!

See Also
========

* :doc:`graph` - Base graph implementation
* :doc:`directed` - Directed graphs
* :doc:`weighted` - Weighted graphs
* :doc:`../../guide/graph_structures/adjacency` - Adjacency representations guide

References
==========

.. [1] Cormen, T. H., et al. "Introduction to Algorithms", 3rd Edition, Chapter 22
.. [2] Sedgewick, R., Wayne, K. "Algorithms", 4th Edition, Chapter 4.1
.. [3] Goodrich, M. T., Tamassia, R. "Algorithm Design and Applications", Chapter 13
