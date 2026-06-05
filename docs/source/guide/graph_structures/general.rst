.. _guide_graph_general:

===================
General Graph Guide
===================

.. currentmodule:: sds.graphs

Introduction
============

A **graph** is a fundamental mathematical structure consisting of vertices (or nodes) connected
by edges. Graphs model relationships and connections in countless real-world systems, from social
networks to transportation systems, making them one of the most versatile data structures in
computer science.

.. mermaid::

   graph LR
       subgraph "Undirected Graph"
       A1[A] --- B1[B]
       A1 --- C1[C]
       B1 --- D1[D]
       C1 --- D1
       end
       
       subgraph "Directed Graph"
       A2[A] --> B2[B]
       A2 --> C2[C]
       B2 --> D2[D]
       C2 --> D2
       end
       
       style A1 fill:#3498db,color:#fff
       style A2 fill:#e74c3c,color:#fff

.. note::
   
   Graphs are ubiquitous in computer science and beyond. Understanding graph theory
   is essential for solving problems in networking, optimization, data analysis,
   and artificial intelligence.

Mathematical Model
==================

Formal Definition
-----------------

Graph Definition
^^^^^^^^^^^^^^^^

A graph :math:`G` is defined as an ordered pair:

.. math::

   G = (V, E)

where:
   * :math:`V` is a **set of vertices** (or nodes)
   * :math:`E` is a **set of edges** connecting pairs of vertices

For undirected graphs:

.. math::

   E \subseteq \{\{u, v\} : u, v \in V, u \neq v\}

For directed graphs:

.. math::

   E \subseteq \{(u, v) : u, v \in V, u \neq v\}

**Example**: :math:`G = (\{A, B, C\}, \{\{A,B\}, \{B,C\}, \{A,C\}\})`

Special Graph Types
^^^^^^^^^^^^^^^^^^^

**Simple Graph**: No self-loops, no multiple edges

.. math::

   \forall e \in E: e = \{u, v\} \text{ where } u \neq v

**Multigraph**: Allows multiple edges between same vertices

.. math::

   E \text{ is a multiset}

**Complete Graph** :math:`K_n`: All vertices connected

.. math::

   |E| = \binom{n}{2} = \frac{n(n-1)}{2}

Graph Properties
----------------

Degree
^^^^^^

The **degree** of a vertex :math:`v` is the number of edges incident to it:

.. math::

   deg(v) = |\{e \in E : v \in e\}|

**Handshaking Lemma**:

.. math::

   \sum_{v \in V} deg(v) = 2|E|

This states that the sum of all degrees equals twice the number of edges.

For directed graphs:

.. math::

   \begin{aligned}
   deg^{in}(v) &= |\{(u, v) \in E\}| \quad \text{(in-degree)} \\
   deg^{out}(v) &= |\{(v, u) \in E\}| \quad \text{(out-degree)} \\
   deg(v) &= deg^{in}(v) + deg^{out}(v)
   \end{aligned}

Paths and Connectivity
^^^^^^^^^^^^^^^^^^^^^^

A **path** from :math:`u` to :math:`v` is a sequence of vertices:

.. math::

   P = (v_0, v_1, \ldots, v_k) \text{ where } v_0 = u, v_k = v, \text{ and } \{v_i, v_{i+1}\} \in E

**Path length**: Number of edges in the path (:math:`k`)

A graph is **connected** if there exists a path between every pair of vertices:

.. math::

   \forall u, v \in V: \exists \text{ path from } u \text{ to } v

**Distance** between vertices :math:`u` and :math:`v`:

.. math::

   d(u, v) = \min\{|P| : P \text{ is a path from } u \text{ to } v\}

Cycles
^^^^^^

A **cycle** is a path where :math:`v_0 = v_k` and :math:`k \geq 3`:

.. math::

   C = (v_0, v_1, \ldots, v_k) \text{ where } v_0 = v_k

A graph is **acyclic** if it contains no cycles.

For directed graphs, a **Directed Acyclic Graph (DAG)** has no directed cycles.

Subgraphs
^^^^^^^^^

:math:`G' = (V', E')` is a **subgraph** of :math:`G = (V, E)` if:

.. math::

   V' \subseteq V \text{ and } E' \subseteq E

**Induced subgraph** on :math:`V' \subseteq V`:

.. math::

   G[V'] = (V', E') \text{ where } E' = \{e \in E : e \subseteq V'\}

Graph Representations
---------------------

Adjacency Matrix
^^^^^^^^^^^^^^^^

For graph :math:`G = (V, E)` with :math:`|V| = n`, the adjacency matrix :math:`A` is :math:`n \times n`:

.. math::

   A[i][j] = \begin{cases}
   1 & \text{if } \{v_i, v_j\} \in E \\
   0 & \text{otherwise}
   \end{cases}

**Properties**:
   * Symmetric for undirected graphs: :math:`A[i][j] = A[j][i]`
   * Space: :math:`\Theta(n^2)`
   * Edge query: :math:`O(1)`

Adjacency List
^^^^^^^^^^^^^^

For each vertex :math:`v`, store list of adjacent vertices:

.. math::

   Adj[v] = \{u \in V : \{v, u\} \in E\}

**Properties**:
   * Space: :math:`\Theta(|V| + |E|)`
   * Edge query: :math:`O(deg(v))`
   * Optimal for sparse graphs

Edge List
^^^^^^^^^

Simply store all edges:

.. math::

   E = \{e_1, e_2, \ldots, e_m\}

**Properties**:
   * Space: :math:`\Theta(|E|)`
   * Edge query: :math:`O(|E|)`

Graph Invariants
----------------

1. **Handshaking Lemma**: :math:`\sum deg(v) = 2|E|`

2. **Euler's Formula** (planar graphs):

   .. math::

      |V| - |E| + |F| = 2

   where :math:`F` is the number of faces

3. **Edge bound for simple graphs**:

   .. math::

      |E| \leq \binom{|V|}{2}

4. **Connected graph minimum edges**:

   .. math::

      |E| \geq |V| - 1

Algorithmic Model
=================

Abstract Data Type
------------------

.. code-block:: text

   ADT Graph:
       Data:
           - vertices: set of V nodes
           - edges: set of E edges
           - directed: boolean (directed/undirected)
           - weighted: boolean (weighted/unweighted)
       
       Vertex:
           - data: stored value
           - id: unique identifier
       
       Edge:
           - node1, node2: connected vertices
           - weight: numeric weight (if weighted)
           - directed: boolean (if directed)
       
       Operations:
           - Graph(): create empty graph
           - add_vertex(v): add vertex to G
           - remove_vertex(v): remove vertex and incident edges
           - add_edge(u, v): add edge {u, v}
           - remove_edge(u, v): remove edge
           - neighbors(v): return adjacent vertices
           - degree(v): return vertex degree
           - is_connected(): check connectivity
       
       Axioms:
           - {u, v} ∈ E ⟹ u, v ∈ V
           - neighbors(v) = {u : {v, u} ∈ E}
           - degree(v) = |neighbors(v)|

Core Algorithms
---------------

Graph Traversal: BFS
^^^^^^^^^^^^^^^^^^^^

**Breadth-First Search** explores graph level by level:

.. code-block:: text

   Algorithm: BFS(G, start)
   Input: Graph G, starting vertex start
   Output: Vertices in BFS order
   
   1. visited ← {start}
   2. queue ← Queue()
   3. queue.enqueue(start)
   4. result ← []
   5. 
   6. while not queue.is_empty() do
   7.     v ← queue.dequeue()
   8.     result.append(v)
   9.     
   10.    for each u in G.neighbors(v) do
   11.        if u not in visited then
   12.            visited.add(u)
   13.            queue.enqueue(u)
   14.        end if
   15.    end for
   16. end while
   17. 
   18. return result

**Time Complexity**: :math:`O(|V| + |E|)`
**Space Complexity**: :math:`O(|V|)` for visited set and queue

**Applications**:
- Shortest path in unweighted graphs
- Connected components
- Level-order traversal

Graph Traversal: DFS
^^^^^^^^^^^^^^^^^^^^

**Depth-First Search** explores as far as possible before backtracking:

.. code-block:: text

   Algorithm: DFS(G, start)
   Input: Graph G, starting vertex start
   Output: Vertices in DFS order
   
   1. visited ← {start}
   2. result ← []
   3. 
   4. DFS_VISIT(start, visited, result)
   5. return result
   
   Algorithm: DFS_VISIT(v, visited, result)
   1. result.append(v)
   2. 
   3. for each u in G.neighbors(v) do
   4.     if u not in visited then
   5.         visited.add(u)
   6.         DFS_VISIT(u, visited, result)
   7.     end if
   8. end for

**Time Complexity**: :math:`O(|V| + |E|)`
**Space Complexity**: :math:`O(|V|)` for recursion stack

**Applications**:
- Cycle detection
- Topological sorting
- Connected components
- Path finding

Connectivity Check
^^^^^^^^^^^^^^^^^^

.. code-block:: text

   Algorithm: IS_CONNECTED(G)
   Input: Graph G = (V, E)
   Output: true if connected, false otherwise
   
   1. if |V| = 0 then
   2.     return true
   3. end if
   4. 
   5. start ← any vertex in V
   6. visited ← BFS(G, start)
   7. 
   8. return |visited| = |V|

**Time Complexity**: :math:`O(|V| + |E|)`

Cycle Detection (Undirected)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   Algorithm: HAS_CYCLE_UNDIRECTED(G)
   Input: Undirected graph G
   Output: true if cycle exists
   
   1. visited ← ∅
   2. 
   3. for each v in V do
   4.     if v not in visited then
   5.         if HAS_CYCLE_DFS(v, null, visited) then
   6.             return true
   7.         end if
   8.     end if
   9. end for
   10. return false
   
   Algorithm: HAS_CYCLE_DFS(v, parent, visited)
   1. visited.add(v)
   2. 
   3. for each u in G.neighbors(v) do
   4.     if u not in visited then
   5.         if HAS_CYCLE_DFS(u, v, visited) then
   6.             return true
   7.         end if
   8.     else if u ≠ parent then
   9.         return true  # Back edge found
   10.    end if
   11. end for
   12. return false

**Time Complexity**: :math:`O(|V| + |E|)`

Complexity Analysis
-------------------

Time Complexity Summary
^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 35 25 40

   * - Operation
     - Adjacency List
     - Adjacency Matrix
   * - **Add vertex**
     - O(1)
     - O(V²) - resize matrix
   * - **Remove vertex**
     - O(E)
     - O(V²)
   * - **Add edge**
     - O(1)
     - O(1)
   * - **Remove edge**
     - O(V)
     - O(1)
   * - **Has edge**
     - O(V)
     - O(1)
   * - **Get neighbors**
     - O(degree)
     - O(V)
   * - **BFS/DFS**
     - O(V + E)
     - O(V²)
   * - **Is connected**
     - O(V + E)
     - O(V²)

Space Complexity
^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Representation
     - Space
   * - **Adjacency List**
     - O(V + E) - optimal for sparse graphs
   * - **Adjacency Matrix**
     - O(V²) - optimal for dense graphs
   * - **Edge List**
     - O(E) - minimal, but slow queries

When :math:`E = O(V^2)` (dense), matrix is better.
When :math:`E = O(V)` (sparse), list is better.

Practical Usage
===============

Installation and Import
-----------------------

.. code-block:: python

   # Install
   pip install sds-tools
   
   # Import
   from sds.graphs import Graph, GraphNode, Edge

Basic Operations
----------------

Creating a Graph
^^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.graphs import Graph

   # Create empty undirected graph
   g = Graph()
   
   # Create multigraph
   mg = Graph(allow_multi_edges=True)
   
   print(g.is_empty())  # True

Building a Graph
^^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.graphs import GraphNode, Edge

   # Create vertices
   alice = GraphNode("Alice", "u1")
   bob = GraphNode("Bob", "u2")
   carol = GraphNode("Carol", "u3")
   dave = GraphNode("Dave", "u4")
   
   # Add to graph
   g.add_node(alice)
   g.add_node(bob)
   g.add_node(carol)
   g.add_node(dave)
   
   # Add edges
   g.add_edge(Edge(alice, bob))
   g.add_edge(Edge(alice, carol))
   g.add_edge(Edge(bob, carol))
   g.add_edge(Edge(carol, dave))
   
   print(f"Graph: {g.node_count()} vertices, {g.edge_count()} edges")

Querying the Graph
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Check connectivity
   print(f"Connected: {g.is_connected()}")  # True
   
   # Get neighbors
   alice_friends = list(g.neighbors(alice))
   print(f"Alice's neighbors: {[n.data for n in alice_friends]}")
   
   # Check degree
   print(f"Carol's degree: {g.degree(carol)}")  # 3
   
   # Check edge
   print(f"Alice-Bob edge: {g.has_edge(alice, bob)}")  # True

Traversing the Graph
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Iterate over vertices
   for node in g:
       print(f"Vertex: {node.data}, Degree: {g.degree(node)}")
   
   # Iterate over edges
   for edge in g.edges():
       print(f"Edge: {edge}")

Real-World Applications
=======================

Application 1: Social Network
------------------------------

Complete social network implementation:

.. code-block:: python

   from sds.graphs import Graph, GraphNode, Edge

   class SocialNetwork:
       """Social network with friendships and communities."""
       
       def __init__(self):
           self.graph = Graph()
           self.users = {}
       
       def add_user(self, user_id, profile):
           """Add user to network."""
           node = GraphNode(profile, user_id)
           self.graph.add_node(node)
           self.users[user_id] = node
       
       def add_friendship(self, user1_id, user2_id):
           """Create mutual friendship."""
           user1 = self.users[user1_id]
           user2 = self.users[user2_id]
           self.graph.add_edge(Edge(user1, user2))
       
       def remove_friendship(self, user1_id, user2_id):
           """Remove friendship."""
           user1 = self.users[user1_id]
           user2 = self.users[user2_id]
           edge = self.graph.get_edge(user1, user2)
           if edge:
               self.graph.remove_edge(edge)
       
       def get_friends(self, user_id):
           """Get direct friends."""
           user = self.users[user_id]
           return [n.data for n in self.graph.neighbors(user)]
       
       def are_friends(self, user1_id, user2_id):
           """Check if users are friends."""
           user1 = self.users[user1_id]
           user2 = self.users[user2_id]
           return self.graph.has_edge(user1, user2)
       
       def friend_count(self, user_id):
           """Get number of friends."""
           user = self.users[user_id]
           return self.graph.degree(user)
       
       def mutual_friends(self, user1_id, user2_id):
           """Find mutual friends."""
           friends1 = set(self.graph.neighbors(self.users[user1_id]))
           friends2 = set(self.graph.neighbors(self.users[user2_id]))
           mutual = friends1 & friends2
           return [n.data for n in mutual]
       
       def suggest_friends(self, user_id, max_suggestions=5):
           """Suggest friends (friends of friends)."""
           user = self.users[user_id]
           friends = set(self.graph.neighbors(user))
           friends.add(user)
           
           suggestions = {}
           for friend in self.graph.neighbors(user):
               for fof in self.graph.neighbors(friend):
                   if fof not in friends:
                       suggestions[fof] = suggestions.get(fof, 0) + 1
           
           # Sort by number of mutual friends
           ranked = sorted(suggestions.items(), 
                          key=lambda x: x[1], 
                          reverse=True)
           
           return [node.data for node, count in ranked[:max_suggestions]]
       
       def find_path(self, user1_id, user2_id):
           """Find shortest path between users (BFS)."""
           start = self.users[user1_id]
           end = self.users[user2_id]
           
           if start == end:
               return [start.data]
           
           visited = {start}
           queue = [(start, [start])]
           
           while queue:
               current, path = queue.pop(0)
               
               for neighbor in self.graph.neighbors(current):
                   if neighbor == end:
                       return [n.data for n in path + [neighbor]]
                   
                   if neighbor not in visited:
                       visited.add(neighbor)
                       queue.append((neighbor, path + [neighbor]))
           
           return None  # No path
   
   # Usage
   network = SocialNetwork()
   
   # Add users
   network.add_user("u1", {"name": "Alice", "age": 25})
   network.add_user("u2", {"name": "Bob", "age": 30})
   network.add_user("u3", {"name": "Carol", "age": 28})
   network.add_user("u4", {"name": "Dave", "age": 32})
   network.add_user("u5", {"name": "Eve", "age": 27})
   
   # Create friendships
   network.add_friendship("u1", "u2")
   network.add_friendship("u1", "u3")
   network.add_friendship("u2", "u3")
   network.add_friendship("u3", "u4")
   network.add_friendship("u4", "u5")
   
   # Query
   print(f"Alice's friends: {network.get_friends('u1')}")
   print(f"Mutual friends (Alice, Carol): {network.mutual_friends('u1', 'u3')}")
   print(f"Friend suggestions for Alice: {network.suggest_friends('u1')}")
   print(f"Path from Alice to Eve: {network.find_path('u1', 'u5')}")

Application 2: Network Topology
--------------------------------

Computer network modeling:

.. code-block:: python

   from sds.graphs import Graph, GraphNode, Edge

   class NetworkTopology:
       """Model computer network infrastructure."""
       
       def __init__(self):
           self.graph = Graph()
           self.devices = {}
       
       def add_device(self, device_id, device_info):
           """Add network device."""
           node = GraphNode(device_info, device_id)
           self.graph.add_node(node)
           self.devices[device_id] = node
       
       def connect(self, dev1_id, dev2_id, link_info=None):
           """Create network link."""
           dev1 = self.devices[dev1_id]
           dev2 = self.devices[dev2_id]
           edge = Edge(dev1, dev2, data=link_info)
           self.graph.add_edge(edge)
       
       def disconnect(self, dev1_id, dev2_id):
           """Remove network link."""
           dev1 = self.devices[dev1_id]
           dev2 = self.devices[dev2_id]
           edge = self.graph.get_edge(dev1, dev2)
           if edge:
               self.graph.remove_edge(edge)
       
       def is_reachable(self, dev1_id, dev2_id):
           """Check if devices can communicate."""
           if not self.graph.is_connected():
               # Need to check path specifically
               path = self.find_route(dev1_id, dev2_id)
               return path is not None
           return True
       
       def find_route(self, dev1_id, dev2_id):
           """Find path between devices (shortest)."""
           start = self.devices[dev1_id]
           end = self.devices[dev2_id]
           
           visited = {start}
           queue = [(start, [start])]
           
           while queue:
               current, path = queue.pop(0)
               
               if current == end:
                   return [n.id for n in path]
               
               for neighbor in self.graph.neighbors(current):
                   if neighbor not in visited:
                       visited.add(neighbor)
                       queue.append((neighbor, path + [neighbor]))
           
           return None
       
       def find_critical_nodes(self):
           """Find devices whose failure would partition network."""
           critical = []
           
           for device_id in self.devices:
               # Temporarily remove device
               device = self.devices[device_id]
               self.graph.remove_node(device)
               
               # Check if still connected
               if not self.graph.is_connected():
                   critical.append(device_id)
               
               # Restore device
               self.graph.add_node(device)
               # Restore edges (simplified - would need to track them)
           
           return critical
       
       def network_diameter(self):
           """Calculate maximum distance between any two devices."""
           max_distance = 0
           device_list = list(self.devices.values())
           
           for i, dev1 in enumerate(device_list):
               for dev2 in device_list[i+1:]:
                   path = self.find_route(dev1.id, dev2.id)
                   if path:
                       max_distance = max(max_distance, len(path) - 1)
           
           return max_distance
   
   # Usage
   network = NetworkTopology()
   
   # Add devices
   network.add_device("r1", {"type": "router", "ip": "192.168.1.1"})
   network.add_device("r2", {"type": "router", "ip": "192.168.1.2"})
   network.add_device("s1", {"type": "switch", "ip": "192.168.1.10"})
   network.add_device("s2", {"type": "switch", "ip": "192.168.1.11"})
   network.add_device("pc1", {"type": "computer", "ip": "192.168.1.100"})
   network.add_device("pc2", {"type": "computer", "ip": "192.168.1.101"})
   
   # Connect devices
   network.connect("r1", "r2", {"bandwidth": "1Gbps"})
   network.connect("r1", "s1", {"bandwidth": "1Gbps"})
   network.connect("r2", "s2", {"bandwidth": "1Gbps"})
   network.connect("s1", "pc1", {"bandwidth": "100Mbps"})
   network.connect("s2", "pc2", {"bandwidth": "100Mbps"})
   
   # Query
   print(f"PC1 can reach PC2: {network.is_reachable('pc1', 'pc2')}")
   print(f"Route from PC1 to PC2: {network.find_route('pc1', 'pc2')}")
   print(f"Network diameter: {network.network_diameter()}")

Best Practices
==============

Do's
----

✅ **Choose appropriate representation**

.. code-block:: python

   # Sparse graph (E << V²) → Adjacency list
   social_network = Graph()
   
   # Dense graph (E ≈ V²) → Adjacency matrix
   from sds.graphs import AdjacencyMatrixGraph
   complete_graph = AdjacencyMatrixGraph(max_nodes=100)

✅ **Use BFS for shortest paths**

.. code-block:: python

   # BFS finds shortest path in unweighted graphs
   def shortest_path(g, start, end):
       visited = {start}
       queue = [(start, [start])]
       
       while queue:
           current, path = queue.pop(0)
           if current == end:
               return path
           
           for neighbor in g.neighbors(current):
               if neighbor not in visited:
                   visited.add(neighbor)
                   queue.append((neighbor, path + [neighbor]))
       
       return None

✅ **Cache expensive computations**

.. code-block:: python

   # is_connected() is cached automatically
   connected = g.is_connected()  # Computed once
   connected2 = g.is_connected()  # Cached result

Don'ts
------

❌ **Don't modify during traversal**

.. code-block:: python

   # Bad
   for node in g:
       if should_remove(node):
           g.remove_node(node)  # Dangerous!
   
   # Good
   to_remove = [n for n in g if should_remove(n)]
   for node in to_remove:
       g.remove_node(node)

❌ **Don't use wrong representation**

.. code-block:: python

   # Bad: Adjacency list for complete graph
   # Wastes space and time
   
   # Good: Use matrix for dense graphs
   if edge_count > node_count * node_count / 2:
       use_adjacency_matrix()

Further Reading
===============

* :doc:`directed` - Directed graphs and DAGs
* :doc:`weighted` - Weighted graphs and shortest paths
* :doc:`/api/graph/index` - Complete API reference

References
==========

.. [WikiGraph] Wikipedia contributors. "Graph (discrete mathematics)". Wikipedia.
   https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)
   
   Comprehensive overview of graph theory fundamentals.

.. [WikiGraphTheory] Wikipedia contributors. "Graph theory". Wikipedia.
   https://en.wikipedia.org/wiki/Graph_theory
   
   History and applications of graph theory.

.. [CLRS] Cormen, T. H., et al. "Introduction to Algorithms", 3rd Edition, Chapter 22.
   https://mitpress.mit.edu/9780262046305/
   
   Standard algorithms textbook with graph algorithms. Many university libraries provide access.

.. [Sedgewick] Sedgewick, R., Wayne, K. "Algorithms", 4th Edition, Part 4.
   https://algs4.cs.princeton.edu/
   
   Free online content accompanying the textbook. Excellent graph algorithms coverage.

.. [WestGraph] West, D. B. "Introduction to Graph Theory", 2nd Edition, Pearson, 2001.
   
   Classic graph theory textbook. Available through many academic institutions.

.. [WikiHandshaking] Wikipedia contributors. "Handshaking lemma". Wikipedia.
   https://en.wikipedia.org/wiki/Handshaking_lemma
   
   Proof and applications of the handshaking lemma.

.. [OpenDSAGraph] OpenDSA Project. "Graph Implementations".
   https://opendsa-server.cs.vt.edu/ODSA/Books/Everything/html/GraphImpl.html
   
   Interactive tutorials on graph data structures.

.. [VisuAlgoGraph] Halim, S. "Graph Data Structures". VisuAlgo.
   https://visualgo.net/en/graphds
   
   Interactive visualizations of graph algorithms.
