.. _api_graph_directed:

================
Directed Graphs
================

.. currentmodule:: sds.graph.directed

Overview
========

This module provides directed and undirected graph implementations with explicit focus on
edge directionality. DirectedGraph maintains separate in/out adjacency lists for efficient
degree queries, while UndirectedGraph validates that only undirected edges are used.

.. mermaid::

   graph TB
       subgraph "Directed Graph"
       A1[A] --> B1[B]
       A1 --> C1[C]
       B1 --> D1[D]
       C1 --> D1
       end
       
       subgraph "Undirected Graph"
       A2[A] --- B2[B]
       A2 --- C2[C]
       B2 --- D2[D]
       C2 --- D2
       end
       
       style A1 fill:#e74c3c,color:#fff
       style A2 fill:#3498db,color:#fff

Classes
=======

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   DirectedGraph
   UndirectedGraph

Detailed Documentation
======================

DirectedGraph
-------------

.. autoclass:: DirectedGraph
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

   .. rubric:: Directed Graph Queries

   .. automethod:: in_degree
   .. automethod:: out_degree
   .. automethod:: predecessors
   .. automethod:: successors
   .. automethod:: is_acyclic

   .. rubric:: General Graph Queries

   .. automethod:: neighbors
   .. automethod:: degree
   .. automethod:: is_connected
   .. automethod:: is_empty

   .. rubric:: Utility Methods

   .. automethod:: clear

UndirectedGraph
---------------

.. autoclass:: UndirectedGraph
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __repr__, __str__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Edge Validation

   .. automethod:: add_edge

   Note: Inherits all other methods from :class:`~sds.graphs.graph.Graph`.

Usage Examples
==============

DirectedGraph Examples
----------------------

Creating a Directed Graph
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.graphs import DirectedGraph, GraphNode, DirectedEdge

   # Create directed graph
   g = DirectedGraph()
   
   # Create with multi-edge support
   mg = DirectedGraph(allow_multi_edges=True)
   
   print(g.is_empty())  # Output: True

Adding Nodes and Edges
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Create nodes
   n1 = GraphNode("A", "n1")
   n2 = GraphNode("B", "n2")
   n3 = GraphNode("C", "n3")
   
   g.add_node(n1)
   g.add_node(n2)
   g.add_node(n3)
   
   # Add directed edges (A→B, B→C, A→C)
   g.add_edge(DirectedEdge(n1, n2))
   g.add_edge(DirectedEdge(n2, n3))
   g.add_edge(DirectedEdge(n1, n3))
   
   print(f"Nodes: {g.node_count()}")  # Output: 3
   print(f"Edges: {g.edge_count()}")  # Output: 3

Direction Matters
^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Check edge existence - direction matters!
   print(g.has_edge(n1, n2))  # True  (A→B exists)
   print(g.has_edge(n2, n1))  # False (B→A doesn't exist)

In/Out Degree
^^^^^^^^^^^^^

.. code-block:: python

   # Out-degree: number of outgoing edges
   print(f"Out-degree of A: {g.out_degree(n1)}")  # Output: 2
   print(f"Out-degree of B: {g.out_degree(n2)}")  # Output: 1
   print(f"Out-degree of C: {g.out_degree(n3)}")  # Output: 0
   
   # In-degree: number of incoming edges
   print(f"In-degree of A: {g.in_degree(n1)}")   # Output: 0
   print(f"In-degree of B: {g.in_degree(n2)}")   # Output: 1
   print(f"In-degree of C: {g.in_degree(n3)}")   # Output: 2
   
   # Total degree
   print(f"Total degree of B: {g.degree(n2)}")   # Output: 2

Predecessors and Successors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Successors: nodes with edges FROM this node
   successors = list(g.successors(n1))
   print(f"A's successors: {[n.data for n in successors]}")
   # Output: ['B', 'C']
   
   # Predecessors: nodes with edges TO this node
   predecessors = list(g.predecessors(n3))
   print(f"C's predecessors: {[n.data for n in predecessors]}")
   # Output: ['A', 'B']
   
   # neighbors() returns successors for directed graphs
   neighbors = list(g.neighbors(n1))
   print(f"A's neighbors: {[n.data for n in neighbors]}")
   # Output: ['B', 'C']

Cycle Detection
^^^^^^^^^^^^^^^

.. code-block:: python

   # Check if graph is acyclic (DAG)
   print(g.is_acyclic())  # True
   
   # Add edge to create cycle
   g.add_edge(DirectedEdge(n3, n1))  # C→A
   print(g.is_acyclic())  # False

Weak Connectivity
^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Weakly connected: connected if edges were undirected
   g = DirectedGraph()
   n1 = GraphNode("A", "n1")
   n2 = GraphNode("B", "n2")
   n3 = GraphNode("C", "n3")
   
   g.add_node(n1)
   g.add_node(n2)
   g.add_node(n3)
   
   # A→B→C (one direction only)
   g.add_edge(DirectedEdge(n1, n2))
   g.add_edge(DirectedEdge(n2, n3))
   
   print(g.is_connected())  # True (weakly connected)

UndirectedGraph Examples
------------------------

Type-Safe Undirected Graph
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.graphs import UndirectedGraph, Edge, DirectedEdge, GraphNode

   # Create undirected graph
   g = UndirectedGraph()
   
   # Add nodes
   n1 = GraphNode("A", "n1")
   n2 = GraphNode("B", "n2")
   
   g.add_node(n1)
   g.add_node(n2)
   
   # Add undirected edge - OK
   g.add_edge(Edge(n1, n2))
   print(g.has_edge(n1, n2))  # True
   print(g.has_edge(n2, n1))  # True (bidirectional)

Rejecting Directed Edges
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Try to add directed edge - ERROR
   try:
       g.add_edge(DirectedEdge(n1, n2))
   except TypeError as e:
       print(f"Error: {e}")
   # Output: Error: UndirectedGraph requires undirected Edge, not DirectedEdge

When to Use UndirectedGraph
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Use UndirectedGraph when:
   # 1. You want explicit type checking
   # 2. Need to ensure only undirected edges
   # 3. Want semantic clarity in code
   
   # Example: Friendship network (always bidirectional)
   friendships = UndirectedGraph()
   
   alice = GraphNode("Alice", "u1")
   bob = GraphNode("Bob", "u2")
   
   friendships.add_node(alice)
   friendships.add_node(bob)
   
   # Friendship is mutual - use Edge
   friendships.add_edge(Edge(alice, bob))

Real-World Examples
===================

Example 1: Task Dependencies (DAG)
-----------------------------------

Project task scheduling:

.. code-block:: python

   from sds.graphs import DirectedGraph, GraphNode, DirectedEdge

   class TaskScheduler:
       """Schedule tasks with dependencies using DAG."""
       
       def __init__(self):
           self.graph = DirectedGraph()
           self.tasks = {}
       
       def add_task(self, task_id, name, duration):
           """Add a task."""
           data = {
               'name': name,
               'duration': duration
           }
           node = GraphNode(data, task_id)
           self.graph.add_node(node)
           self.tasks[task_id] = node
       
       def add_dependency(self, task_id, depends_on_id):
           """Task depends on another task (depends_on must complete first)."""
           task = self.tasks[task_id]
           depends_on = self.tasks[depends_on_id]
           # Edge from prerequisite to dependent
           edge = DirectedEdge(depends_on, task)
           self.graph.add_edge(edge)
       
       def can_schedule(self):
           """Check if schedule is valid (no cycles)."""
           return self.graph.is_acyclic()
       
       def get_prerequisites(self, task_id):
           """Get tasks that must complete before this one."""
           task = self.tasks[task_id]
           predecessors = list(self.graph.predecessors(task))
           return [(n.id, n.data['name']) for n in predecessors]
       
       def get_dependent_tasks(self, task_id):
           """Get tasks that depend on this one."""
           task = self.tasks[task_id]
           successors = list(self.graph.successors(task))
           return [(n.id, n.data['name']) for n in successors]
       
       def topological_sort(self):
           """Get valid execution order (simplified)."""
           if not self.can_schedule():
               raise ValueError("Cannot schedule: cycle detected")
           
           # Simple topological sort using in-degree
           in_degree = {
               task_id: self.graph.in_degree(self.tasks[task_id])
               for task_id in self.tasks
           }
           
           queue = [tid for tid, deg in in_degree.items() if deg == 0]
           result = []
           
           while queue:
               task_id = queue.pop(0)
               result.append(task_id)
               
               task = self.tasks[task_id]
               for successor in self.graph.successors(task):
                   in_degree[successor.id] -= 1
                   if in_degree[successor.id] == 0:
                       queue.append(successor.id)
           
           return result
   
   # Usage
   scheduler = TaskScheduler()
   
   # Add tasks
   scheduler.add_task("t1", "Design", 3)
   scheduler.add_task("t2", "Implement", 5)
   scheduler.add_task("t3", "Test", 2)
   scheduler.add_task("t4", "Deploy", 1)
   
   # Add dependencies
   scheduler.add_dependency("t2", "t1")  # Implement depends on Design
   scheduler.add_dependency("t3", "t2")  # Test depends on Implement
   scheduler.add_dependency("t4", "t3")  # Deploy depends on Test
   
   # Validate and get order
   if scheduler.can_schedule():
       order = scheduler.topological_sort()
       print(f"Task order: {order}")
   else:
       print("Cannot schedule: cycle detected")

Example 2: Web Page Links
--------------------------

Modeling hyperlinks:

.. code-block:: python

   from sds.graphs import DirectedGraph, GraphNode, DirectedEdge

   class WebGraph:
       """Model web pages and links."""
       
       def __init__(self):
           self.graph = DirectedGraph()
           self.pages = {}
       
       def add_page(self, url, title):
           """Add a web page."""
           node = GraphNode(title, url)
           self.graph.add_node(node)
           self.pages[url] = node
       
       def add_link(self, from_url, to_url):
           """Add hyperlink from one page to another."""
           from_page = self.pages[from_url]
           to_page = self.pages[to_url]
           edge = DirectedEdge(from_page, to_page)
           self.graph.add_edge(edge)
       
       def get_outgoing_links(self, url):
           """Get pages this page links to."""
           page = self.pages[url]
           successors = list(self.graph.successors(page))
           return [(n.id, n.data) for n in successors]
       
       def get_incoming_links(self, url):
           """Get pages that link to this page (backlinks)."""
           page = self.pages[url]
           predecessors = list(self.graph.predecessors(page))
           return [(n.id, n.data) for n in predecessors]
       
       def page_rank_simple(self, url):
           """Simple page rank based on incoming links."""
           page = self.pages[url]
           return self.graph.in_degree(page)
   
   # Usage
   web = WebGraph()
   
   # Add pages
   web.add_page("index.html", "Home")
   web.add_page("about.html", "About")
   web.add_page("contact.html", "Contact")
   web.add_page("blog.html", "Blog")
   
   # Add links
   web.add_link("index.html", "about.html")
   web.add_link("index.html", "contact.html")
   web.add_link("index.html", "blog.html")
   web.add_link("about.html", "contact.html")
   web.add_link("blog.html", "index.html")
   
   # Query
   outgoing = web.get_outgoing_links("index.html")
   print(f"Links from home: {outgoing}")
   
   incoming = web.get_incoming_links("contact.html")
   print(f"Links to contact: {incoming}")

Example 3: Social Network (Followers)
--------------------------------------

Asymmetric relationships:

.. code-block:: python

   from sds.graphs import DirectedGraph, GraphNode, DirectedEdge

   class FollowerNetwork:
       """Social network with follow relationships."""
       
       def __init__(self):
           self.graph = DirectedGraph(allow_multi_edges=False)
           self.users = {}
       
       def add_user(self, user_id, username):
           """Add a user."""
           node = GraphNode(username, user_id)
           self.graph.add_node(node)
           self.users[user_id] = node
       
       def follow(self, follower_id, followee_id):
           """User follows another user."""
           follower = self.users[follower_id]
           followee = self.users[followee_id]
           # Edge from follower to followee
           edge = DirectedEdge(follower, followee)
           
           try:
               self.graph.add_edge(edge)
               return True
           except ValueError:
               return False  # Already following
       
       def unfollow(self, follower_id, followee_id):
           """User unfollows another user."""
           follower = self.users[follower_id]
           followee = self.users[followee_id]
           edge = self.graph.get_edge(follower, followee)
           
           if edge:
               self.graph.remove_edge(edge)
               return True
           return False
       
       def is_following(self, follower_id, followee_id):
           """Check if user follows another."""
           follower = self.users[follower_id]
           followee = self.users[followee_id]
           return self.graph.has_edge(follower, followee)
       
       def get_following(self, user_id):
           """Get users this user follows."""
           user = self.users[user_id]
           following = list(self.graph.successors(user))
           return [n.data for n in following]
       
       def get_followers(self, user_id):
           """Get users who follow this user."""
           user = self.users[user_id]
           followers = list(self.graph.predecessors(user))
           return [n.data for n in followers]
       
       def follower_count(self, user_id):
           """Get number of followers."""
           user = self.users[user_id]
           return self.graph.in_degree(user)
       
       def following_count(self, user_id):
           """Get number of users being followed."""
           user = self.users[user_id]
           return self.graph.out_degree(user)
   
   # Usage
   network = FollowerNetwork()
   
   # Add users
   network.add_user("u1", "Alice")
   network.add_user("u2", "Bob")
   network.add_user("u3", "Carol")
   
   # Create follow relationships
   network.follow("u1", "u2")  # Alice follows Bob
   network.follow("u1", "u3")  # Alice follows Carol
   network.follow("u2", "u3")  # Bob follows Carol
   network.follow("u3", "u1")  # Carol follows Alice
   
   # Query relationships
   print(f"Alice follows: {network.get_following('u1')}")
   print(f"Carol's followers: {network.get_followers('u3')}")
   print(f"Carol has {network.follower_count('u3')} followers")

Performance Characteristics
===========================

DirectedGraph Time Complexity
------------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 20 40

   * - Operation
     - Complexity
     - Notes
   * - ``add_node(node)``
     - O(1)
     - Hash table insertion
   * - ``add_edge(edge)``
     - O(1) or O(out_degree)
     - Check duplicates in simple graph
   * - ``in_degree(node)``
     - O(1)
     - Cached in adjacency list
   * - ``out_degree(node)``
     - O(1)
     - Cached in adjacency list
   * - ``predecessors(node)``
     - O(in_degree)
     - Iterate in-adjacency
   * - ``successors(node)``
     - O(out_degree)
     - Iterate out-adjacency
   * - ``is_acyclic()``
     - O(V + E)
     - DFS with coloring, cached
   * - ``is_connected()``
     - O(V + E)
     - Weak connectivity BFS

Space Complexity
----------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Component
     - Space
   * - **Nodes**
     - O(V)
   * - **Out-adjacency**
     - O(V + E)
   * - **In-adjacency**
     - O(V + E)
   * - **Edge list**
     - O(E)
   * - **Total**
     - O(V + E)

Note: DirectedGraph uses slightly more memory than Graph due to separate in/out lists.

Comparison: Graph Types
=======================

.. list-table::
   :header-rows: 1
   :widths: 25 25 25 25

   * - Feature
     - Graph
     - DirectedGraph
     - UndirectedGraph
   * - **Edge Type**
     - Undirected
     - Directed
     - Undirected (validated)
   * - **In/Out Degree**
     - No
     - Yes
     - No
   * - **Cycle Detection**
     - No
     - Yes
     - No
   * - **Type Checking**
     - Minimal
     - Edge type
     - Strict Edge type
   * - **Memory**
     - O(V + E)
     - O(V + E)
     - O(V + E)

Best Practices
==============

DirectedGraph
-------------

✅ **Use for asymmetric relationships**

.. code-block:: python

   # Good: One-way relationships
   followers = DirectedGraph()
   web_links = DirectedGraph()
   task_deps = DirectedGraph()

✅ **Check cycles for DAGs**

.. code-block:: python

   if not dag.is_acyclic():
       raise ValueError("Cycle detected in DAG")

✅ **Use predecessors/successors appropriately**

.. code-block:: python

   # Predecessors: who points TO this node
   incoming = list(g.predecessors(node))
   
   # Successors: who this node points TO
   outgoing = list(g.successors(node))

UndirectedGraph
---------------

✅ **Use for type safety**

.. code-block:: python

   # Ensures only undirected edges
   friendships = UndirectedGraph()
   
   # Type error if DirectedEdge used
   friendships.add_edge(Edge(a, b))  # OK
   # friendships.add_edge(DirectedEdge(a, b))  # TypeError

✅ **Use for semantic clarity**

.. code-block:: python

   # Makes code intent clear
   def build_friendship_graph():
       return UndirectedGraph()  # Clearly bidirectional

Common Pitfalls
===============

1. **Confusing edge direction**

.. code-block:: python

   # Remember: DirectedEdge(source, target)
   # means source → target
   edge = DirectedEdge(from_node, to_node)
   g.add_edge(edge)
   
   g.has_edge(from_node, to_node)  # True
   g.has_edge(to_node, from_node)  # False!

2. **Not checking for cycles in DAGs**

.. code-block:: python

   # Always validate DAG property
   if scheduler.is_acyclic():
       order = topological_sort()
   else:
       raise ValueError("Not a DAG")

3. **Mixing Graph and DirectedGraph**

.. code-block:: python

   # Be consistent with graph type
   g = Graph()  # Undirected
   # Later...
   g.add_edge(DirectedEdge(a, b))  # Wrong! Use Edge

See Also
========

* :doc:`graph` - Base undirected graph
* :doc:`weighted` - Weighted graphs
* :doc:`../../guide/graph_structures/directed` - User guide

References
==========

.. [1] Cormen, T. H., et al. "Introduction to Algorithms", 3rd Edition, Chapter 22
.. [2] Bang-Jensen, J., Gutin, G. "Digraphs: Theory, Algorithms and Applications", Springer, 2008
.. [3] Sedgewick, R., Wayne, K. "Algorithms", 4th Edition, Chapter 4.2
