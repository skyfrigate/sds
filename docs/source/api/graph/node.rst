.. _api_graph_node:

=================
Graph Node Class
=================

.. currentmodule:: sds.graph.node

Overview
========

This module provides the node implementation for graph data structures. GraphNode is 
a lightweight container optimized for graph operations, where connections between nodes 
are managed externally through Edge objects rather than stored within the node itself.

.. mermaid::

   classDiagram
       Node <|-- GraphNode
       
       class Node {
           <<abstract>>
           +data: Any
           +parent: Node
           #_refs: List
       }
       
       class GraphNode {
           -_id: str
           +id: str
           +__eq__(other)
           +__hash__()
       }
       
       note for GraphNode "Connections managed\nvia Edge objects"

Classes
=======

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   GraphNode

Detailed Documentation
======================

GraphNode
---------

.. autoclass:: GraphNode
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __eq__, __hash__, __repr__, __str__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Properties

   .. autoproperty:: id

   .. rubric:: Special Methods

   .. automethod:: __eq__
   .. automethod:: __hash__
   .. automethod:: __repr__
   .. automethod:: __str__

Usage Examples
==============

Basic Node Creation
-------------------

Creating nodes with automatic and explicit IDs:

.. code-block:: python

   from sds.graph import GraphNode

   # Automatic UUID generation
   node1 = GraphNode("Paris")
   node2 = GraphNode("London")
   
   print(node1.id)  # UUID string
   print(node1.data)  # "Paris"
   
   # Explicit IDs for named nodes
   paris = GraphNode("Paris", node_id="paris")
   london = GraphNode("London", node_id="london")
   
   print(paris.id)  # "paris"
   print(london.id)  # "london"

Node Equality and Hashing
--------------------------

Nodes are equal if they have the same ID:

.. code-block:: python

   from sds.graph import GraphNode

   # Nodes with same ID are equal
   node1 = GraphNode("Data A", node_id="node_1")
   node2 = GraphNode("Data B", node_id="node_1")
   
   print(node1 == node2)  # True (same ID)
   print(node1.data == node2.data)  # False (different data)
   
   # Can be used in sets and dicts
   nodes = {node1, node2}
   print(len(nodes))  # 1 (deduplicated by ID)
   
   node_map = {
       node1: "First entry",
       node2: "Second entry"  # Overwrites first
   }
   print(len(node_map))  # 1

Using Nodes in Collections
---------------------------

GraphNodes can be stored in sets and used as dictionary keys:

.. code-block:: python

   from sds.graph import GraphNode

   # Create a set of unique nodes
   nodes = set()
   
   for i in range(5):
       node = GraphNode(f"Node {i}", node_id=f"n{i}")
       nodes.add(node)
   
   print(len(nodes))  # 5
   
   # Use as dictionary keys
   node_data = {}
   for node in nodes:
       node_data[node] = {"processed": False, "weight": i}
   
   # Lookup by node
   target = GraphNode("Dummy", node_id="n3")  # Same ID
   if target in node_data:
       print(node_data[target])  # {'processed': False, 'weight': 3}

Storing Rich Data
-----------------

Nodes can store any type of data:

.. code-block:: python

   from sds.graph import GraphNode
   from dataclasses import dataclass

   # Store complex objects
   @dataclass
   class City:
       name: str
       population: int
       coordinates: tuple
   
   paris = City("Paris", 2_165_000, (48.8566, 2.3522))
   london = City("London", 8_982_000, (51.5074, -0.1278))
   
   node_paris = GraphNode(paris, node_id="paris")
   node_london = GraphNode(london, node_id="london")
   
   print(node_paris.data.name)  # "Paris"
   print(node_paris.data.population)  # 2165000

Node Identity vs Equality
--------------------------

Understanding node comparison:

.. code-block:: python

   from sds.graph import GraphNode

   # Identity (is) vs Equality (==)
   node1 = GraphNode("A", node_id="node_1")
   node2 = GraphNode("B", node_id="node_1")
   node3 = node1
   
   print(node1 == node2)  # True (same ID)
   print(node1 is node2)  # False (different objects)
   print(node1 is node3)  # True (same object)
   
   # Hash equality
   print(hash(node1) == hash(node2))  # True
   
   # This enables usage in graphs:
   visited = set()
   visited.add(node1)
   
   # node2 considered already visited (same ID)
   if node2 not in visited:
       print("Not visited")
   else:
       print("Already visited")  # This prints

Memory Layout
=============

Node Structure
--------------

.. code-block:: text

   GraphNode memory layout:

   ┌─────────────────────────┐
   │      GraphNode          │
   ├─────────────────────────┤
   │ _data: Any              │  ← Stored value
   │ _id: str                │  ← Unique identifier
   │ _parent: None           │  ← Unused (inherited)
   │ _refs: []               │  ← Empty (connections via Edges)
   └─────────────────────────┘

**Memory characteristics:**
   - Fixed overhead per node: ~64 bytes (Python object + 2 attributes)
   - ID string: ~50-80 bytes (UUID) or custom length
   - Data: depends on stored object
   - No edge storage: connections managed externally

Comparison with Other Node Types
---------------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 25 25

   * - Feature
     - GraphNode
     - BinaryNode
     - TreeNode
   * - **Children storage**
     - None (external)
     - 2 pointers
     - List of pointers
   * - **Identity**
     - UUID or custom ID
     - Object identity
     - Object identity
   * - **Hashable**
     - Yes (by ID)
     - No
     - No
   * - **Connections**
     - Via Edge objects
     - Direct pointers
     - Direct pointers
   * - **Use in sets**
     - ✓ Yes
     - ✗ No
     - ✗ No

Real-World Examples
===================

Example 1: Social Network Users
--------------------------------

Representing users in a social network:

.. code-block:: python

   from sds.graph import GraphNode
   from dataclasses import dataclass
   from typing import List

   @dataclass
   class User:
       username: str
       email: str
       interests: List[str]
   
   # Create user nodes
   alice = User("alice", "alice@example.com", ["coding", "music"])
   bob = User("bob", "bob@example.com", ["gaming", "music"])
   carol = User("carol", "carol@example.com", ["coding", "art"])
   
   node_alice = GraphNode(alice, node_id="user_alice")
   node_bob = GraphNode(bob, node_id="user_bob")
   node_carol = GraphNode(carol, node_id="user_carol")
   
   # Find common interests
   def find_common_interests(node1, node2):
       interests1 = set(node1.data.interests)
       interests2 = set(node2.data.interests)
       return interests1 & interests2
   
   common = find_common_interests(node_alice, node_bob)
   print(f"Alice and Bob both like: {common}")
   # Output: {'music'}

Example 2: City Network
-----------------------

Representing cities in a transportation network:

.. code-block:: python

   from sds.graph import GraphNode

   # Create city nodes
   cities = {
       'paris': GraphNode(
           {'name': 'Paris', 'country': 'France', 'population': 2_165_000},
           node_id='paris'
       ),
       'london': GraphNode(
           {'name': 'London', 'country': 'UK', 'population': 8_982_000},
           node_id='london'
       ),
       'berlin': GraphNode(
           {'name': 'Berlin', 'country': 'Germany', 'population': 3_645_000},
           node_id='berlin'
       ),
       'madrid': GraphNode(
           {'name': 'Madrid', 'country': 'Spain', 'population': 3_223_000},
           node_id='madrid'
       )
   }
   
   # Query cities
   for node in cities.values():
       city = node.data
       if city['population'] > 3_000_000:
           print(f"{city['name']}: {city['population']:,} people")
   
   # Output:
   # London: 8,982,000 people
   # Berlin: 3,645,000 people
   # Madrid: 3,223,000 people

Example 3: Task Dependencies
-----------------------------

Representing tasks with dependencies:

.. code-block:: python

   from sds.graph import GraphNode
   from dataclasses import dataclass
   from datetime import datetime, timedelta

   @dataclass
   class Task:
       name: str
       duration: int  # hours
       priority: int
       deadline: datetime
   
   # Create task nodes
   tasks = {
       'design': GraphNode(
           Task("UI Design", 8, 1, datetime.now() + timedelta(days=3)),
           node_id="task_design"
       ),
       'backend': GraphNode(
           Task("Backend API", 16, 1, datetime.now() + timedelta(days=7)),
           node_id="task_backend"
       ),
       'frontend': GraphNode(
           Task("Frontend", 12, 2, datetime.now() + timedelta(days=10)),
           node_id="task_frontend"
       ),
       'testing': GraphNode(
           Task("Testing", 6, 3, datetime.now() + timedelta(days=12)),
           node_id="task_testing"
       )
   }
   
   # Find critical tasks (priority 1)
   critical = [
       node for node in tasks.values()
       if node.data.priority == 1
   ]
   
   print("Critical tasks:")
   for node in critical:
       task = node.data
       print(f"- {task.name}: {task.duration}h")

Best Practices
==============

Do's
----

✅ **Use meaningful IDs for named entities**

.. code-block:: python

   # Good: Semantic IDs
   user = GraphNode(user_data, node_id=f"user_{username}")
   city = GraphNode(city_data, node_id=city_name.lower())
   
   # Acceptable: Auto-generated for anonymous nodes
   temp = GraphNode(temp_data)  # UUID generated

✅ **Store rich data in nodes**

.. code-block:: python

   # Good: Store structured data
   node = GraphNode({
       'name': 'Paris',
       'lat': 48.8566,
       'lon': 2.3522,
       'population': 2_165_000
   })
   
   # Even better: Use dataclasses
   @dataclass
   class City:
       name: str
       lat: float
       lon: float
   
   node = GraphNode(City("Paris", 48.8566, 2.3522))

✅ **Leverage hashing for efficient lookups**

.. code-block:: python

   # Good: Use nodes as dictionary keys
   distances = {
       node_paris: 0,
       node_london: 344,
       node_berlin: 878
   }
   
   # Good: Use sets for visited tracking
   visited = set()
   visited.add(current_node)

Don'ts
------

✗ **Don't manually modify _id**

.. code-block:: python

   # Bad: Direct modification breaks immutability
   node._id = "new_id"  # DON'T DO THIS
   
   # Good: Create new node if ID needs to change
   new_node = GraphNode(node.data, node_id="new_id")

✗ **Don't use _refs for connections**

.. code-block:: python

   # Bad: _refs is inherited but unused in GraphNode
   node1._refs.append(node2)  # WRONG!
   
   # Good: Use Edge objects
   from sds.graph import Edge
   edge = Edge(node1, node2)

✗ **Don't rely on data for equality**

.. code-block:: python

   # Wrong assumption
   node1 = GraphNode("Paris", node_id="city_1")
   node2 = GraphNode("Paris", node_id="city_2")
   
   # node1 != node2 (different IDs)
   # node1.data == node2.data (same data)

Common Pitfalls
===============

1. **Confusing identity with equality**

.. code-block:: python

   node1 = GraphNode("A", node_id="1")
   node2 = GraphNode("A", node_id="1")
   
   # These are equal but not identical
   print(node1 == node2)  # True (same ID)
   print(node1 is node2)  # False (different objects)
   
   # Use == for logical equality
   # Use 'is' only for object identity

2. **Creating duplicate nodes with same ID**

.. code-block:: python

   # Problematic: Multiple nodes with same ID
   nodes = [
       GraphNode("Data 1", node_id="node_1"),
       GraphNode("Data 2", node_id="node_1"),  # Same ID!
   ]
   
   # In a set, only one remains
   unique_nodes = set(nodes)
   print(len(unique_nodes))  # 1, not 2!

3. **Forgetting nodes are hashable**

.. code-block:: python

   # Inefficient: Linear search
   visited_list = []
   if node not in visited_list:  # O(n)
       visited_list.append(node)
   
   # Efficient: Use set
   visited_set = set()
   if node not in visited_set:  # O(1)
       visited_set.add(node)

Design Rationale
================

Why External Connections?
--------------------------

GraphNode deliberately does not store connections internally:

**Advantages:**

1. **Flexibility**: Supports multiple graph representations (adjacency list, matrix, edge list)
2. **Memory efficiency**: Nodes can be shared across graphs without duplication
3. **Separation of concerns**: Node data separate from graph structure
4. **Multi-graph support**: Same nodes can exist in different graphs

**Trade-offs:**

- Requires separate Edge objects
- Can't navigate from node to neighbors without graph context
- Slightly more complex API (but more flexible)

.. code-block:: python

   # This design enables:
   
   # 1. Same nodes in multiple graphs
   node_paris = GraphNode("Paris", node_id="paris")
   
   graph_europe = Graph()
   graph_world = Graph()
   
   graph_europe.add_node(node_paris)  # Same node
   graph_world.add_node(node_paris)   # in two graphs
   
   # 2. Different graph representations
   adj_list_graph = AdjacencyListGraph()
   adj_matrix_graph = AdjacencyMatrixGraph()
   
   # Both use same GraphNode instances

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
   * - Create node
     - O(1)
     - UUID generation or copy ID
   * - Access data
     - O(1)
     - Direct attribute access
   * - Compare equality
     - O(1)
     - ID comparison
   * - Hash node
     - O(1)
     - Hash of ID string
   * - Use in set/dict
     - O(1)
     - Average case
   * - String representation
     - O(1)
     - Simple formatting

Space Complexity
----------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Component
     - Space
   * - Base object
     - ~64 bytes (Python overhead)
   * - ID string (UUID)
     - ~50-80 bytes
   * - ID string (custom)
     - Length-dependent
   * - Data reference
     - 8 bytes (pointer)
   * - Actual data
     - Depends on data type
   * - **Total (typical)**
     - **~120-150 bytes + data**

See Also
========

* :doc:`edge` - Edge classes for connecting nodes
* :doc:`graph` - Graph implementations using nodes
* :doc:`interfaces` - Abstract graph interfaces
* :doc:`../../guide/graph_structures/index` - Graph structures guide

References
==========

.. [1] Cormen, T. H., et al. "Introduction to Algorithms", 3rd Edition, Chapter 22
.. [2] Sedgewick, R., Wayne, K. "Algorithms", 4th Edition, Chapter 4.1
.. [3] West, D. B. "Introduction to Graph Theory", 2nd Edition, Chapter 1
