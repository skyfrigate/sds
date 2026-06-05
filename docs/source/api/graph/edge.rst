.. _api_graph_edge:

==================
Graph Edge Classes
==================

.. currentmodule:: sds.graph.edge

Overview
========

This module provides edge implementations for connecting nodes in graph structures. 
Edges can be directed or undirected, weighted or unweighted, allowing representation 
of various graph types and relationships.

.. mermaid::

   classDiagram
       Edge <|-- DirectedEdge
       Edge <|-- WeightedEdge
       DirectedEdge <|-- WeightedDirectedEdge
       
       class Edge {
           -_node1: GraphNode
           -_node2: GraphNode
           -_data: Any
           +connects(a, b) bool
           +incident_to(node) bool
           +other_node(node) GraphNode
           +is_self_loop() bool
       }
       
       class DirectedEdge {
           +source: GraphNode
           +target: GraphNode
           +connects(a, b) bool
       }
       
       class WeightedEdge {
           -_weight: float
           +weight: float
       }
       
       class WeightedDirectedEdge {
           +source: GraphNode
           +target: GraphNode
           +weight: float
       }

Classes
=======

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   Edge
   DirectedEdge
   WeightedEdge
   WeightedDirectedEdge

Detailed Documentation
======================

Edge (Base Class)
-----------------

.. autoclass:: Edge
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __eq__, __hash__, __repr__, __str__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Properties

   .. autoproperty:: node1
   .. autoproperty:: node2
   .. autoproperty:: data

   .. rubric:: Methods

   .. automethod:: connects
   .. automethod:: incident_to
   .. automethod:: other_node
   .. automethod:: is_self_loop

   .. rubric:: Special Methods

   .. automethod:: __eq__
   .. automethod:: __hash__
   .. automethod:: __repr__
   .. automethod:: __str__

DirectedEdge
------------

.. autoclass:: DirectedEdge
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __eq__, __hash__, __repr__, __str__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Properties

   .. autoproperty:: source
   .. autoproperty:: target
   .. autoproperty:: node1
   .. autoproperty:: node2

   .. rubric:: Methods

   .. automethod:: connects

WeightedEdge
------------

.. autoclass:: WeightedEdge
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __repr__, __str__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Properties

   .. autoproperty:: weight

WeightedDirectedEdge
--------------------

.. autoclass:: WeightedDirectedEdge
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __repr__, __str__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Properties

   .. autoproperty:: source
   .. autoproperty:: target
   .. autoproperty:: weight

Usage Examples
==============

Undirected Edges
----------------

Basic undirected edge connecting two nodes:

.. code-block:: python

   from sds.graph import GraphNode, Edge

   # Create nodes
   paris = GraphNode("Paris", node_id="paris")
   london = GraphNode("London", node_id="london")
   
   # Create undirected edge
   edge = Edge(paris, london)
   
   # Check connections (bidirectional)
   print(edge.connects(paris, london))  # True
   print(edge.connects(london, paris))  # True (undirected!)
   
   # Check incidence
   print(edge.incident_to(paris))   # True
   print(edge.incident_to(london))  # True
   
   # Get other endpoint
   print(edge.other_node(paris))   # london
   print(edge.other_node(london))  # paris

Edge with Data
--------------

Storing additional information on edges:

.. code-block:: python

   from sds.graph import GraphNode, Edge

   alice = GraphNode("Alice", node_id="alice")
   bob = GraphNode("Bob", node_id="bob")
   
   # Edge with relationship data
   friendship = Edge(alice, bob, data={
       'since': '2020-01-15',
       'strength': 0.8,
       'interactions': 142
   })
   
   print(friendship.data['since'])      # '2020-01-15'
   print(friendship.data['strength'])   # 0.8

Directed Edges
--------------

Edges with explicit direction:

.. code-block:: python

   from sds.graph import GraphNode, DirectedEdge

   # Create nodes
   user = GraphNode("User", node_id="user")
   page = GraphNode("Page", node_id="page")
   
   # Directed edge: user -> page
   follows = DirectedEdge(user, page, data="follows")
   
   # Direction matters!
   print(follows.connects(user, page))  # True (source -> target)
   print(follows.connects(page, user))  # False (wrong direction)
   
   # Access source and target
   print(follows.source)  # user
   print(follows.target)  # page
   
   # Also accessible as node1/node2 (aliases)
   print(follows.node1)   # user (source)
   print(follows.node2)   # page (target)

Weighted Edges
--------------

Edges with numeric weights:

.. code-block:: python

   from sds.graph import GraphNode, WeightedEdge

   # Cities
   paris = GraphNode("Paris", node_id="paris")
   london = GraphNode("London", node_id="london")
   
   # Weighted edge (distance in km)
   route = WeightedEdge(paris, london, weight=344.0)
   
   print(route.weight)  # 344.0
   print(f"{paris.data} to {london.data}: {route.weight} km")
   
   # Default weight is 1.0
   default_edge = WeightedEdge(paris, london)
   print(default_edge.weight)  # 1.0

Weighted Directed Edges
------------------------

Combining direction and weight:

.. code-block:: python

   from sds.graph import GraphNode, WeightedDirectedEdge

   # Nodes
   a = GraphNode("A", node_id="a")
   b = GraphNode("B", node_id="b")
   
   # Directed weighted edge
   edge = WeightedDirectedEdge(a, b, weight=5.5)
   
   print(edge.source)  # a
   print(edge.target)  # b
   print(edge.weight)  # 5.5
   
   # Direction matters
   print(edge.connects(a, b))  # True
   print(edge.connects(b, a))  # False

Self-Loops
----------

Edges connecting a node to itself:

.. code-block:: python

   from sds.graph import GraphNode, Edge

   # Self-referential node
   node = GraphNode("Node", node_id="node")
   
   # Create self-loop (must enable explicitly)
   loop = Edge(node, node, allow_self_loop=True)
   
   print(loop.is_self_loop())  # True
   print(loop.connects(node, node))  # True
   
   # Without allow_self_loop=True, raises ValueError
   try:
       bad_loop = Edge(node, node)  # Error!
   except ValueError as e:
       print(e)  # "Self-loops not allowed..."

Edge Equality and Hashing
--------------------------

Understanding edge comparison:

.. code-block:: python

   from sds.graph import GraphNode, Edge, DirectedEdge

   n1 = GraphNode("A", node_id="n1")
   n2 = GraphNode("B", node_id="n2")
   
   # Undirected edges are order-independent
   edge1 = Edge(n1, n2)
   edge2 = Edge(n2, n1)
   
   print(edge1 == edge2)  # True (same nodes, undirected)
   print(hash(edge1) == hash(edge2))  # True
   
   # Directed edges are order-dependent
   dir1 = DirectedEdge(n1, n2)
   dir2 = DirectedEdge(n2, n1)
   
   print(dir1 == dir2)  # False (different direction)
   print(hash(dir1) == hash(dir2))  # False
   
   # Can use edges in sets
   edges = {edge1, edge2}
   print(len(edges))  # 1 (deduplicated)

Real-World Examples
===================

Example 1: Social Network
--------------------------

Modeling friendships and follows:

.. code-block:: python

   from sds.graph import GraphNode, Edge, DirectedEdge

   # Create users
   users = {
       'alice': GraphNode("Alice", node_id="alice"),
       'bob': GraphNode("Bob", node_id="bob"),
       'carol': GraphNode("Carol", node_id="carol"),
       'dave': GraphNode("Dave", node_id="dave")
   }
   
   # Bidirectional friendships (undirected)
   friendships = [
       Edge(users['alice'], users['bob'], data={'since': '2020-01'}),
       Edge(users['bob'], users['carol'], data={'since': '2021-03'}),
       Edge(users['alice'], users['carol'], data={'since': '2019-06'})
   ]
   
   # Unidirectional follows (directed)
   follows = [
       DirectedEdge(users['dave'], users['alice'], data={'since': '2022-01'}),
       DirectedEdge(users['dave'], users['bob'], data={'since': '2022-02'}),
       DirectedEdge(users['alice'], users['dave'], data={'since': '2022-03'})
   ]
   
   # Query: Who are Alice's friends?
   alice_friends = [
       e.other_node(users['alice'])
       for e in friendships
       if e.incident_to(users['alice'])
   ]
   
   print(f"Alice's friends: {[f.data for f in alice_friends]}")
   # Output: ['Bob', 'Carol']
   
   # Query: Who does Dave follow?
   dave_follows = [
       e.target for e in follows
       if e.source == users['dave']
   ]
   
   print(f"Dave follows: {[u.data for u in dave_follows]}")
   # Output: ['Alice', 'Bob']

Example 2: Transportation Network
----------------------------------

Weighted graph for route planning:

.. code-block:: python

   from sds.graph import GraphNode, WeightedEdge

   # Cities
   cities = {
       'paris': GraphNode("Paris", node_id="paris"),
       'london': GraphNode("London", node_id="london"),
       'berlin': GraphNode("Berlin", node_id="berlin"),
       'madrid': GraphNode("Madrid", node_id="madrid"),
       'rome': GraphNode("Rome", node_id="rome")
   }
   
   # Routes with distances (km)
   routes = [
       WeightedEdge(cities['paris'], cities['london'], weight=344),
       WeightedEdge(cities['paris'], cities['berlin'], weight=878),
       WeightedEdge(cities['paris'], cities['madrid'], weight=1053),
       WeightedEdge(cities['london'], cities['berlin'], weight=932),
       WeightedEdge(cities['berlin'], cities['rome'], weight=1181),
       WeightedEdge(cities['madrid'], cities['rome'], weight=1365)
   ]
   
   # Find all routes from Paris
   paris_routes = [
       (e.other_node(cities['paris']), e.weight)
       for e in routes
       if e.incident_to(cities['paris'])
   ]
   
   print("Routes from Paris:")
   for city, distance in paris_routes:
       print(f"  → {city.data}: {distance} km")
   
   # Output:
   # → London: 344 km
   # → Berlin: 878 km
   # → Madrid: 1053 km
   
   # Find shortest route from Paris
   shortest = min(paris_routes, key=lambda x: x[1])
   print(f"\nClosest city: {shortest[0].data} ({shortest[1]} km)")

Example 3: Task Dependencies (DAG)
-----------------------------------

Directed acyclic graph for project planning:

.. code-block:: python

   from sds.graph import GraphNode, DirectedEdge

   # Tasks
   tasks = {
       'design': GraphNode("UI Design", node_id="design"),
       'backend': GraphNode("Backend API", node_id="backend"),
       'frontend': GraphNode("Frontend", node_id="frontend"),
       'testing': GraphNode("Testing", node_id="testing"),
       'deployment': GraphNode("Deployment", node_id="deployment")
   }
   
   # Dependencies (from → to means "from must complete before to")
   dependencies = [
       DirectedEdge(tasks['design'], tasks['frontend'], 
                    data="UI needed for frontend"),
       DirectedEdge(tasks['design'], tasks['backend'],
                    data="API design needed"),
       DirectedEdge(tasks['backend'], tasks['frontend'],
                    data="API must exist"),
       DirectedEdge(tasks['frontend'], tasks['testing'],
                    data="Code needed for tests"),
       DirectedEdge(tasks['backend'], tasks['testing'],
                    data="API needed for tests"),
       DirectedEdge(tasks['testing'], tasks['deployment'],
                    data="Tests must pass")
   ]
   
   # Find prerequisites for frontend
   frontend_prereqs = [
       e.source for e in dependencies
       if e.target == tasks['frontend']
   ]
   
   print("Frontend depends on:")
   for task in frontend_prereqs:
       print(f"  - {task.data}")
   
   # Output:
   # - UI Design
   # - Backend API

Example 4: Citation Network
----------------------------

Weighted directed graph for academic papers:

.. code-block:: python

   from sds.graph import GraphNode, WeightedDirectedEdge

   # Papers
   papers = {
       'p1': GraphNode("Attention Is All You Need", node_id="p1"),
       'p2': GraphNode("BERT", node_id="p2"),
       'p3': GraphNode("GPT-2", node_id="p3"),
       'p4': GraphNode("GPT-3", node_id="p4")
   }
   
   # Citations (source cites target, weight = importance)
   citations = [
       WeightedDirectedEdge(papers['p2'], papers['p1'], 
                           weight=1.0, data="Builds on Transformer"),
       WeightedDirectedEdge(papers['p3'], papers['p1'],
                           weight=1.0, data="Uses Transformer architecture"),
       WeightedDirectedEdge(papers['p3'], papers['p2'],
                           weight=0.5, data="Compares to BERT"),
       WeightedDirectedEdge(papers['p4'], papers['p3'],
                           weight=1.0, data="Extends GPT-2")
   ]
   
   # Find most cited paper
   citation_counts = {}
   for paper in papers.values():
       count = sum(
           1 for c in citations
           if c.target == paper
       )
       citation_counts[paper] = count
   
   most_cited = max(citation_counts.items(), key=lambda x: x[1])
   print(f"Most cited: {most_cited[0].data} ({most_cited[1]} citations)")

Edge Type Comparison
====================

Feature Matrix
--------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 20 20

   * - Feature
     - Edge
     - DirectedEdge
     - WeightedEdge
     - WeightedDirectedEdge
   * - **Direction**
     - None
     - Yes
     - None
     - Yes
   * - **Weight**
     - No
     - No
     - Yes
     - Yes
   * - **Symmetric**
     - Yes
     - No
     - Yes
     - No
   * - **Use case**
     - Friendship
     - Follows
     - Distance
     - Flow

When to Use Each Type
---------------------

.. mermaid::

   graph TD
       A{Need direction?}
       
       A -->|No| B{Need weight?}
       A -->|Yes| C{Need weight?}
       
       B -->|No| D[Edge]
       B -->|Yes| E[WeightedEdge]
       
       C -->|No| F[DirectedEdge]
       C -->|Yes| G[WeightedDirectedEdge]
       
       style D fill:#2ecc71
       style E fill:#3498db
       style F fill:#f39c12
       style G fill:#e74c3c

**Decision guide:**

- **Edge**: Symmetric relationships (friendship, physical connections)
- **DirectedEdge**: Asymmetric relationships (follows, parent-child, citations)
- **WeightedEdge**: Distances, costs, similarities
- **WeightedDirectedEdge**: Flow networks, weighted paths with direction

Best Practices
==============

Do's
----

✅ **Choose appropriate edge type**

.. code-block:: python

   # Good: Directed for asymmetric relationships
   follows = DirectedEdge(user1, user2)
   
   # Good: Weighted for distances
   route = WeightedEdge(city1, city2, weight=distance)
   
   # Good: Both for flow networks
   flow = WeightedDirectedEdge(source, sink, weight=capacity)

✅ **Store rich data in edge data attribute**

.. code-block:: python

   # Good: Structured edge data
   edge = Edge(node1, node2, data={
       'created': '2024-01-01',
       'type': 'strong_tie',
       'weight': 0.95,
       'metadata': {...}
   })

✅ **Use edge equality for deduplication**

.. code-block:: python

   # Good: Automatic deduplication
   edges = set()
   edges.add(Edge(n1, n2))
   edges.add(Edge(n2, n1))  # Same edge
   print(len(edges))  # 1

✅ **Handle self-loops explicitly**

.. code-block:: python

   # Good: Explicit self-loop handling
   if node1 == node2:
       edge = Edge(node1, node2, allow_self_loop=True)
   else:
       edge = Edge(node1, node2)

Don'ts
------

✗ **Don't mix edge types inconsistently**

.. code-block:: python

   # Bad: Mixing directed and undirected
   edges = [
       Edge(n1, n2),           # Undirected
       DirectedEdge(n2, n3)    # Directed - inconsistent!
   ]
   
   # Good: Be consistent
   directed_edges = [
       DirectedEdge(n1, n2),
       DirectedEdge(n2, n3)
   ]

✗ **Don't create self-loops without explicit permission**

.. code-block:: python

   # Bad: Will raise ValueError
   edge = Edge(node, node)  # Error!
   
   # Good: Explicit flag
   edge = Edge(node, node, allow_self_loop=True)

✗ **Don't assume edge mutability**

.. code-block:: python

   # Bad: Edges are immutable after creation
   edge = WeightedEdge(n1, n2, weight=10)
   edge._weight = 20  # DON'T DO THIS
   
   # Good: Create new edge
   new_edge = WeightedEdge(n1, n2, weight=20)

✗ **Don't ignore direction in DirectedEdge**

.. code-block:: python

   # Wrong: Treating directed edge as undirected
   edge = DirectedEdge(n1, n2)
   if edge.connects(n2, n1):  # False!
       process()
   
   # Correct: Check proper direction
   if edge.connects(n1, n2):  # True
       process()

Common Pitfalls
===============

1. **Confusing connects() semantics**

.. code-block:: python

   # Undirected: order doesn't matter
   edge = Edge(n1, n2)
   edge.connects(n1, n2)  # True
   edge.connects(n2, n1)  # True (same)
   
   # Directed: order matters
   dir_edge = DirectedEdge(n1, n2)
   dir_edge.connects(n1, n2)  # True (source -> target)
   dir_edge.connects(n2, n1)  # False (wrong direction!)

2. **Forgetting to handle None weights**

.. code-block:: python

   # Potential issue: comparing with None
   edge1 = WeightedEdge(n1, n2, weight=10)
   edge2 = WeightedEdge(n3, n4)  # weight defaults to 1.0
   
   # Always has numeric weight
   assert isinstance(edge1.weight, (int, float))
   assert isinstance(edge2.weight, (int, float))

3. **Not checking edge type**

.. code-block:: python

   def process_edge(edge):
       # Bad: Assuming all edges have weight
       print(edge.weight)  # AttributeError for Edge!
       
       # Good: Check type
       if isinstance(edge, (WeightedEdge, WeightedDirectedEdge)):
           print(edge.weight)
       else:
           print("No weight")

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
   * - Create edge
     - O(1)
     - All edge types
   * - Check connects
     - O(1)
     - Node ID comparison
   * - Check incident_to
     - O(1)
     - Node ID lookup
   * - Get other_node
     - O(1)
     - Direct access
   * - Edge equality
     - O(1)
     - ID comparison
   * - Edge hashing
     - O(1)
     - Hash of node IDs

Space Complexity
----------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Component
     - Space
   * - **Edge**
     - 2 node references + optional data
   * - **DirectedEdge**
     - Same as Edge
   * - **WeightedEdge**
     - Edge + 1 float (8 bytes)
   * - **WeightedDirectedEdge**
     - DirectedEdge + 1 float
   * - **Typical total**
     - ~80-120 bytes per edge

See Also
========

* :doc:`node` - GraphNode class for vertices
* :doc:`graph` - Graph implementations using edges
* :doc:`directed` - Directed graph implementations
* :doc:`weighted` - Weighted graph implementations
* :doc:`../../guide/graph_structures/index` - Graph structures guide

References
==========

.. [1] Cormen, T. H., et al. "Introduction to Algorithms", 3rd Edition, Chapter 22
.. [2] Sedgewick, R., Wayne, K. "Algorithms", 4th Edition, Section 4.1-4.2
.. [3] West, D. B. "Introduction to Graph Theory", 2nd Edition
.. [4] Bondy, J. A., Murty, U. S. R. "Graph Theory", Graduate Texts in Mathematics
