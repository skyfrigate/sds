.. _guide_graph_weighted:

===============
Weighted Graphs
===============

.. currentmodule:: sds.graph

Introduction
============

A **weighted graph** is a graph where each edge has an associated numeric value called a **weight**. Weights typically represent costs, distances, capacities, or other quantitative relationships between nodes. Weighted graphs are fundamental for modeling real-world networks where connections have varying strengths or costs.

.. mermaid::

   graph LR
       subgraph "Weighted Undirected Graph"
       A((Paris)) ---|344 km| B((London))
       A ---|878 km| C((Berlin))
       B ---|932 km| C
       A ---|1054 km| D((Rome))
       C ---|817 km| D
       end
       
       subgraph "Weighted Directed Graph"
       E((A)) -->|5| F((B))
       E -->|3| G((C))
       F -->|2| H((D))
       G -->|7| H
       G -->|1| F
       end
       
       style A fill:#e74c3c,color:#fff
       style E fill:#3498db,color:#fff

.. note::
   
   Weighted graphs enable sophisticated analysis like shortest path algorithms
   (Dijkstra, Bellman-Ford), minimum spanning trees (Kruskal, Prim), and
   network flow optimization that are impossible with unweighted graphs.

Mathematical Model
==================

Formal Definition
-----------------

Weighted Graph
^^^^^^^^^^^^^^

A weighted graph :math:`G = (V, E, w)` consists of:

1. **Vertex set** :math:`V`: finite set of nodes

   .. math::

      V = \{v_1, v_2, \ldots, v_n\}

2. **Edge set** :math:`E`: set of connections

   .. math::

      E \subseteq \{\{u, v\} : u, v \in V, u \neq v\}

   for undirected graphs, or

   .. math::

      E \subseteq \{(u, v) : u, v \in V, u \neq v\}

   for directed graphs

3. **Weight function** :math:`w`: maps edges to real numbers

   .. math::

      w: E \rightarrow \mathbb{R}

   where :math:`w(e)` represents the weight of edge :math:`e`

Edge Weight Properties
^^^^^^^^^^^^^^^^^^^^^^

For an edge :math:`e = \{u, v\}` (or :math:`(u, v)` for directed):

.. math::

   w(e) \in \mathbb{R}

**Common weight interpretations:**

* **Distance**: :math:`w(e) \geq 0` (non-negative)
* **Cost**: :math:`w(e) \geq 0` typically
* **Capacity**: :math:`w(e) > 0` (positive)
* **Profit**: :math:`w(e)` can be negative
* **Time**: :math:`w(e) \geq 0` usually

Graph Properties
----------------

Total Weight
^^^^^^^^^^^^

The **total weight** of a graph is the sum of all edge weights:

.. math::

   W(G) = \sum_{e \in E} w(e)

Path Weight
^^^^^^^^^^^

For a path :math:`P = (v_1, v_2, \ldots, v_k)`:

.. math::

   w(P) = \sum_{i=1}^{k-1} w(\{v_i, v_{i+1}\})

or for directed paths:

.. math::

   w(P) = \sum_{i=1}^{k-1} w((v_i, v_{i+1}))

Shortest Path
^^^^^^^^^^^^^

The **shortest path** from :math:`u` to :math:`v` is:

.. math::

   \delta(u, v) = \min\{w(P) : P \text{ is a path from } u \text{ to } v\}

If no path exists:

.. math::

   \delta(u, v) = \infty

Distance Matrix
^^^^^^^^^^^^^^^

For a graph with :math:`n` vertices, the **distance matrix** :math:`D` is:

.. math::

   D_{ij} = \begin{cases}
   0 & \text{if } i = j \\
   w(\{v_i, v_j\}) & \text{if } \{v_i, v_j\} \in E \\
   \infty & \text{otherwise}
   \end{cases}

Minimum Spanning Tree
^^^^^^^^^^^^^^^^^^^^^

For a connected weighted undirected graph, a **minimum spanning tree (MST)** :math:`T` is a spanning tree such that:

.. math::

   w(T) = \sum_{e \in T} w(e)

is minimized among all spanning trees.

**Properties of MST:**

1. **Uniqueness**: MST is unique if all edge weights are distinct
2. **Cut property**: Minimum weight edge crossing a cut is in some MST
3. **Cycle property**: Maximum weight edge in any cycle is not in any MST

Weighted Degree
^^^^^^^^^^^^^^^

The **weighted degree** of a vertex :math:`v`:

.. math::

   deg_w(v) = \sum_{\{v,u\} \in E} w(\{v, u\})

For directed graphs:

.. math::

   \begin{aligned}
   deg_w^{in}(v) &= \sum_{(u,v) \in E} w((u, v)) \\
   deg_w^{out}(v) &= \sum_{(v,u) \in E} w((v, u))
   \end{aligned}

Algorithmic Model
=================

Abstract Data Type
------------------

.. code-block:: text

   ADT WeightedGraph:
       Data:
           - vertices: set of GraphNode
           - edges: set of WeightedEdge
           - adjacency: map of node → neighbors with weights
       
       WeightedEdge:
           - node1: GraphNode (or source for directed)
           - node2: GraphNode (or target for directed)
           - weight: float
           - data: optional metadata
       
       Operations:
           - WeightedGraph(): create empty graph
           - add_node(node): add vertex
           - add_edge(edge): add weighted edge
           - remove_node(node): remove vertex and incident edges
           - remove_edge(edge): remove weighted edge
           - get_edge_weight(u, v): get weight of edge (u,v)
           - total_weight(): sum of all edge weights
           - incident_edges(node): edges touching node
           - neighbors(node): adjacent vertices
           - shortest_path(u, v): find minimum weight path
       
       Invariants:
           - All edges have numeric weights
           - Weights are preserved on edge operations
           - Graph structure consistent with base Graph

Core Operations
---------------

Get Edge Weight
^^^^^^^^^^^^^^^

.. code-block:: text

   Algorithm: GET_EDGE_WEIGHT(graph, u, v)
   Input: Weighted graph, vertices u and v
   Output: Weight of edge (u,v), or null if no edge
   
   1. edge ← GET_EDGE(graph, u, v)
   2. if edge = null then
   3.     return null
   4. end if
   5. return edge.weight

**Time complexity**: O(1) with adjacency structure

Total Weight Calculation
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   Algorithm: TOTAL_WEIGHT(graph)
   Input: Weighted graph
   Output: Sum of all edge weights
   
   1. total ← 0
   2. for each edge in graph.edges() do
   3.     total ← total + edge.weight
   4. end for
   5. return total

**Time complexity**: O(E)

Incident Edges
^^^^^^^^^^^^^^

.. code-block:: text

   Algorithm: INCIDENT_EDGES(graph, node)
   Input: Weighted graph, vertex node
   Output: List of weighted edges incident to node
   
   1. result ← []
   2. for each edge in graph.edges() do
   3.     if edge.incident_to(node) then
   4.         result.append(edge)
   5.     end if
   6. end for
   7. return result

**Time complexity**: O(E)

**Optimized with adjacency**:

.. code-block:: text

   Algorithm: INCIDENT_EDGES_FAST(graph, node)
   Input: Weighted graph with adjacency, vertex node
   Output: List of weighted edges incident to node
   
   1. result ← []
   2. for each neighbor in graph.neighbors(node) do
   3.     edge ← graph.get_edge(node, neighbor)
   4.     result.append(edge)
   5. end for
   6. return result

**Time complexity**: O(degree(node))

Shortest Path Algorithms
-------------------------

Dijkstra's Algorithm
^^^^^^^^^^^^^^^^^^^^

For graphs with **non-negative weights**:

.. code-block:: text

   Algorithm: DIJKSTRA(graph, source)
   Input: Weighted graph G=(V,E,w) with w(e)≥0, source vertex
   Output: Shortest distances and paths from source
   
   1. dist ← map with dist[v] = ∞ for all v ∈ V
   2. dist[source] ← 0
   3. prev ← map with prev[v] = null for all v ∈ V
   4. Q ← priority queue containing all vertices
   5. 
   6. while Q is not empty do
   7.     u ← vertex in Q with minimum dist[u]
   8.     remove u from Q
   9.     
   10.    if dist[u] = ∞ then
   11.        break  // Remaining vertices unreachable
   12.    end if
   13.    
   14.    for each neighbor v of u do
   15.        edge_weight ← get_edge_weight(u, v)
   16.        alt ← dist[u] + edge_weight
   17.        
   18.        if alt < dist[v] then
   19.            dist[v] ← alt
   20.            prev[v] ← u
   21.            decrease_key(Q, v, alt)
   22.        end if
   23.    end for
   24. end while
   25. 
   26. return (dist, prev)

**Time complexity**: 
- With binary heap: O((V + E) log V)
- With Fibonacci heap: O(E + V log V)

**Space complexity**: O(V)

**Visualization**:

.. code-block:: text

   Graph:        A --5--> B
                  \       |
                   3      2
                    \     |
                     C --1--> D
   
   Step 1: dist = {A:0, B:∞, C:∞, D:∞}
   Step 2: Process A → dist = {A:0, B:5, C:3, D:∞}
   Step 3: Process C → dist = {A:0, B:5, C:3, D:4}
   Step 4: Process D → dist = {A:0, B:5, C:3, D:4}
   Step 5: Process B → dist = {A:0, B:5, C:3, D:4}

Bellman-Ford Algorithm
^^^^^^^^^^^^^^^^^^^^^^^

For graphs that may have **negative weights**:

.. code-block:: text

   Algorithm: BELLMAN_FORD(graph, source)
   Input: Weighted graph G=(V,E,w), source vertex
   Output: Shortest distances, or False if negative cycle exists
   
   1. dist ← map with dist[v] = ∞ for all v ∈ V
   2. dist[source] ← 0
   3. prev ← map with prev[v] = null for all v ∈ V
   4. 
   5. // Relax all edges |V|-1 times
   6. for i ← 1 to |V| - 1 do
   7.     for each edge (u, v) with weight w in E do
   8.         if dist[u] + w < dist[v] then
   9.             dist[v] ← dist[u] + w
   10.            prev[v] ← u
   11.        end if
   12.    end for
   13. end for
   14. 
   15. // Check for negative-weight cycles
   16. for each edge (u, v) with weight w in E do
   17.    if dist[u] + w < dist[v] then
   18.        return False  // Negative cycle detected
   19.    end if
   20. end for
   21. 
   22. return (dist, prev)

**Time complexity**: O(VE)
**Space complexity**: O(V)

**Handles negative weights**: Unlike Dijkstra
**Detects negative cycles**: Returns False if one exists

Minimum Spanning Tree
----------------------

Kruskal's Algorithm
^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   Algorithm: KRUSKAL(graph)
   Input: Weighted undirected graph G=(V,E,w)
   Output: Minimum spanning tree T
   
   1. T ← empty set of edges
   2. sort E by weight (non-decreasing)
   3. 
   4. // Initialize disjoint-set forest
   5. for each v in V do
   6.     MAKE_SET(v)
   7. end for
   8. 
   9. for each edge (u, v) in sorted E do
   10.    if FIND_SET(u) ≠ FIND_SET(v) then
   11.        T ← T ∪ {(u, v)}
   12.        UNION(u, v)
   13.        
   14.        if |T| = |V| - 1 then
   15.            break  // MST complete
   16.        end if
   17.    end if
   18. end for
   19. 
   20. return T

**Time complexity**: O(E log E) = O(E log V)
**Space complexity**: O(V)

Prim's Algorithm
^^^^^^^^^^^^^^^^

.. code-block:: text

   Algorithm: PRIM(graph, start)
   Input: Weighted undirected graph G=(V,E,w), starting vertex
   Output: Minimum spanning tree T
   
   1. T ← empty set of edges
   2. visited ← {start}
   3. Q ← priority queue of edges from start
   4. 
   5. while |visited| < |V| and Q not empty do
   6.     edge (u, v) ← Q.extract_min()
   7.     
   8.     if v not in visited then
   9.         T ← T ∪ {(u, v)}
   10.        visited ← visited ∪ {v}
   11.        
   12.        // Add edges from v to unvisited vertices
   13.        for each edge (v, w) where w not in visited do
   14.            Q.insert((v, w))
   15.        end for
   16.    end if
   17. end while
   18. 
   19. return T

**Time complexity**: O(E log V) with binary heap
**Space complexity**: O(V)

Complexity Analysis
-------------------

Operation Complexity
^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 35 20 40

   * - Operation
     - Complexity
     - Notes
   * - **add_node**
     - O(1)
     - Add vertex
   * - **add_edge**
     - O(1)
     - Add weighted edge
   * - **get_edge_weight**
     - O(1)
     - With adjacency structure
   * - **total_weight**
     - O(E)
     - Sum all edges
   * - **incident_edges**
     - O(degree)
     - Optimized lookup
   * - **shortest_path (Dijkstra)**
     - O((V+E) log V)
     - Non-negative weights
   * - **shortest_path (Bellman-Ford)**
     - O(VE)
     - Handles negative weights
   * - **MST (Kruskal)**
     - O(E log V)
     - Sort edges
   * - **MST (Prim)**
     - O(E log V)
     - Priority queue

Algorithm Selection
^^^^^^^^^^^^^^^^^^^

**Shortest Path:**

* **Non-negative weights only**: Use Dijkstra (faster)
* **May have negative weights**: Use Bellman-Ford
* **All pairs**: Use Floyd-Warshall O(V³)

**Minimum Spanning Tree:**

* **Sparse graph**: Use Kruskal
* **Dense graph**: Use Prim
* **Both work well** in most cases

Practical Usage
===============

Installation and Import
-----------------------

.. code-block:: python

   # Install
   pip install sds-tools
   
   # Import
   from sds.graph import WeightedGraph, WeightedDirectedGraph
   from sds.graph import GraphNode, WeightedEdge, WeightedDirectedEdge

Basic Operations
----------------

Creating Weighted Undirected Graph
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.graph import WeightedGraph, GraphNode, WeightedEdge

   # Create weighted graph
   g = WeightedGraph()

   # Add cities
   paris = GraphNode("Paris", "paris")
   london = GraphNode("London", "london")
   berlin = GraphNode("Berlin", "berlin")
   rome = GraphNode("Rome", "rome")

   g.add_node(paris)
   g.add_node(london)
   g.add_node(berlin)
   g.add_node(rome)

   # Add weighted edges (distances in km)
   g.add_edge(WeightedEdge(paris, london, weight=344))
   g.add_edge(WeightedEdge(paris, berlin, weight=878))
   g.add_edge(WeightedEdge(london, berlin, weight=932))
   g.add_edge(WeightedEdge(paris, rome, weight=1054))
   g.add_edge(WeightedEdge(berlin, rome, weight=817))

   print(f"Nodes: {g.node_count()}")  # Output: 4
   print(f"Edges: {g.edge_count()}")  # Output: 5

Querying Edge Weights
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Get specific edge weight
   distance = g.get_edge_weight(paris, london)
   print(f"Paris-London: {distance} km")  # Output: 344 km

   # Get total network weight
   total = g.total_weight()
   print(f"Total distance: {total} km")  # Output: 4025 km

   # Check if edge exists
   if g.has_edge(paris, berlin):
       weight = g.get_edge_weight(paris, berlin)
       print(f"Paris-Berlin: {weight} km")

Working with Incident Edges
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Get all edges connected to Paris
   paris_edges = g.incident_edges(paris)
   
   print(f"Paris connections:")
   for edge in paris_edges:
       other = edge.other_node(paris)
       print(f"  → {other.data}: {edge.weight} km")
   
   # Output:
   # Paris connections:
   #   → London: 344 km
   #   → Berlin: 878 km
   #   → Rome: 1054 km

Creating Weighted Directed Graph
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.graph import WeightedDirectedGraph, WeightedDirectedEdge

   # Create directed weighted graph
   dg = WeightedDirectedGraph()

   # Add tasks
   a = GraphNode("Task A", "a")
   b = GraphNode("Task B", "b")
   c = GraphNode("Task C", "c")
   d = GraphNode("Task D", "d")

   dg.add_node(a)
   dg.add_node(b)
   dg.add_node(c)
   dg.add_node(d)

   # Add weighted directed edges (task durations)
   dg.add_edge(WeightedDirectedEdge(a, b, weight=5))
   dg.add_edge(WeightedDirectedEdge(a, c, weight=3))
   dg.add_edge(WeightedDirectedEdge(b, d, weight=2))
   dg.add_edge(WeightedDirectedEdge(c, d, weight=7))

   # Direction matters!
   print(dg.has_edge(a, b))  # True
   print(dg.has_edge(b, a))  # False

   # Get weight
   duration = dg.get_edge_weight(a, b)
   print(f"A→B duration: {duration} hours")

Updating Edge Weights
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Remove old edge
   old_edge = g.get_edge(paris, london)
   g.remove_edge(old_edge)

   # Add new edge with updated weight
   g.add_edge(WeightedEdge(paris, london, weight=350))

   # Verify update
   new_distance = g.get_edge_weight(paris, london)
   print(f"Updated distance: {new_distance} km")

Real-World Applications
=======================

Application 1: Route Planning System
-------------------------------------

GPS navigation with real-time traffic:

.. code-block:: python

   from sds.graph import WeightedGraph, GraphNode, WeightedEdge

   class RouteNavigator:
       """GPS navigation system using weighted graph."""
       
       def __init__(self):
           self.map = WeightedGraph()
           self.locations = {}
       
       def add_location(self, name, location_id):
           """Add a location to the map."""
           node = GraphNode(name, location_id)
           self.map.add_node(node)
           self.locations[location_id] = node
           return node
       
       def add_road(self, loc1_id, loc2_id, distance, bidirectional=True):
           """Add a road with distance."""
           loc1 = self.locations[loc1_id]
           loc2 = self.locations[loc2_id]
           
           edge = WeightedEdge(loc1, loc2, weight=distance)
           self.map.add_edge(edge)
       
       def update_traffic(self, loc1_id, loc2_id, traffic_factor):
           """Update road weight based on traffic (1.0 = normal, 2.0 = 2x slower)."""
           loc1 = self.locations[loc1_id]
           loc2 = self.locations[loc2_id]
           
           # Get current edge
           edge = self.map.get_edge(loc1, loc2)
           if edge:
               base_distance = edge.weight
               
               # Remove old edge
               self.map.remove_edge(edge)
               
               # Add new edge with traffic-adjusted weight
               new_weight = base_distance * traffic_factor
               self.map.add_edge(WeightedEdge(loc1, loc2, weight=new_weight))
       
       def find_shortest_path_dijkstra(self, start_id, end_id):
           """Find shortest path using Dijkstra's algorithm."""
           import heapq
           
           start = self.locations[start_id]
           end = self.locations[end_id]
           
           # Initialize distances
           distances = {node.id: float('infinity') for node in self.map.nodes()}
           distances[start.id] = 0
           
           # Track previous nodes for path reconstruction
           previous = {node.id: None for node in self.map.nodes()}
           
           # Priority queue: (distance, node)
           pq = [(0, start)]
           visited = set()
           
           while pq:
               current_dist, current = heapq.heappop(pq)
               
               if current.id in visited:
                   continue
               
               visited.add(current.id)
               
               if current == end:
                   break
               
               # Check all neighbors
               for neighbor in self.map.neighbors(current):
                   if neighbor.id in visited:
                       continue
                   
                   edge_weight = self.map.get_edge_weight(current, neighbor)
                   distance = current_dist + edge_weight
                   
                   if distance < distances[neighbor.id]:
                       distances[neighbor.id] = distance
                       previous[neighbor.id] = current
                       heapq.heappush(pq, (distance, neighbor))
           
           # Reconstruct path
           path = []
           current = end
           while current:
               path.append(current)
               current = previous[current.id]
           
           path.reverse()
           
           if path[0] != start:
               return None, float('infinity')
           
           return path, distances[end.id]
       
       def get_alternative_routes(self, start_id, end_id, num_routes=3):
           """Find multiple alternative routes."""
           # Simplified: find k-shortest paths
           routes = []
           
           # First route: optimal path
           path, distance = self.find_shortest_path_dijkstra(start_id, end_id)
           if path:
               routes.append((path, distance))
           
           # For demonstration: return just one route
           # Full k-shortest paths would require Yen's algorithm
           return routes
   
   # Usage
   nav = RouteNavigator()
   
   # Build city network
   nav.add_location("Home", "home")
   nav.add_location("Work", "work")
   nav.add_location("Mall", "mall")
   nav.add_location("School", "school")
   
   # Add roads (distances in km)
   nav.add_road("home", "work", 15)
   nav.add_road("home", "mall", 8)
   nav.add_road("mall", "work", 12)
   nav.add_road("mall", "school", 5)
   nav.add_road("school", "work", 7)
   
   # Find route
   path, distance = nav.find_shortest_path_dijkstra("home", "work")
   
   if path:
       route = " → ".join(node.data for node in path)
       print(f"Route: {route}")
       print(f"Total distance: {distance:.1f} km")
   
   # Update for traffic
   print("\nTraffic on Home-Work road (2x slower)...")
   nav.update_traffic("home", "work", 2.0)
   
   # Recalculate
   path, distance = nav.find_shortest_path_dijkstra("home", "work")
   route = " → ".join(node.data for node in path)
   print(f"New route: {route}")
   print(f"New distance: {distance:.1f} km")

Application 2: Network Optimization
------------------------------------

Minimum spanning tree for network design:

.. code-block:: python

   from sds.graph import WeightedGraph, GraphNode, WeightedEdge

   class NetworkDesigner:
       """Design minimum-cost network using MST."""
       
       def __init__(self):
           self.graph = WeightedGraph()
           self.locations = {}
       
       def add_location(self, name, location_id):
           """Add a location to connect."""
           node = GraphNode(name, location_id)
           self.graph.add_node(node)
           self.locations[location_id] = node
       
       def add_possible_connection(self, loc1_id, loc2_id, cost):
           """Add a possible connection with its cost."""
           loc1 = self.locations[loc1_id]
           loc2 = self.locations[loc2_id]
           
           edge = WeightedEdge(loc1, loc2, weight=cost)
           self.graph.add_edge(edge)
       
       def find_minimum_spanning_tree_kruskal(self):
           """Find MST using Kruskal's algorithm."""
           # Get all edges sorted by weight
           edges = list(self.graph.edges())
           edges.sort(key=lambda e: e.weight)
           
           # Initialize disjoint set (Union-Find)
           parent = {node.id: node.id for node in self.graph.nodes()}
           rank = {node.id: 0 for node in self.graph.nodes()}
           
           def find(x):
               if parent[x] != x:
                   parent[x] = find(parent[x])
               return parent[x]
           
           def union(x, y):
               px, py = find(x), find(y)
               if px == py:
                   return False
               
               if rank[px] < rank[py]:
                   parent[px] = py
               elif rank[px] > rank[py]:
                   parent[py] = px
               else:
                   parent[py] = px
                   rank[px] += 1
               return True
           
           # Build MST
           mst_edges = []
           total_cost = 0
           
           for edge in edges:
               if union(edge.node1.id, edge.node2.id):
                   mst_edges.append(edge)
                   total_cost += edge.weight
                   
                   # MST complete when we have V-1 edges
                   if len(mst_edges) == self.graph.node_count() - 1:
                       break
           
           return mst_edges, total_cost
       
       def analyze_network(self):
           """Analyze network costs."""
           mst, min_cost = self.find_minimum_spanning_tree_kruskal()
           total_possible_cost = self.graph.total_weight()
           
           savings = total_possible_cost - min_cost
           savings_percent = (savings / total_possible_cost) * 100
           
           return {
               'mst_edges': mst,
               'minimum_cost': min_cost,
               'total_possible_cost': total_possible_cost,
               'savings': savings,
               'savings_percent': savings_percent
           }
   
   # Usage
   designer = NetworkDesigner()
   
   # Add cities to connect
   cities = ["A", "B", "C", "D", "E"]
   for city in cities:
       designer.add_location(f"City {city}", city)
   
   # Add all possible connections with costs
   connections = [
       ("A", "B", 4),
       ("A", "C", 2),
       ("B", "C", 1),
       ("B", "D", 5),
       ("C", "D", 8),
       ("C", "E", 10),
       ("D", "E", 2)
   ]
   
   for loc1, loc2, cost in connections:
       designer.add_possible_connection(loc1, loc2, cost)
   
   # Find optimal network
   analysis = designer.analyze_network()
   
   print("Minimum Spanning Tree:")
   for edge in analysis['mst_edges']:
       print(f"  {edge.node1.data} — {edge.node2.data}: ${edge.weight}M")
   
   print(f"\nMinimum cost: ${analysis['minimum_cost']}M")
   print(f"Total possible cost: ${analysis['total_possible_cost']}M")
   print(f"Savings: ${analysis['savings']}M ({analysis['savings_percent']:.1f}%)")

Application 3: Project Scheduling
----------------------------------

Critical path analysis with weighted directed graph:

.. code-block:: python

   from sds.graph import WeightedDirectedGraph, GraphNode, WeightedDirectedEdge

   class ProjectScheduler:
       """Project management with critical path analysis."""
       
       def __init__(self):
           self.graph = WeightedDirectedGraph()
           self.tasks = {}
       
       def add_task(self, name, task_id, duration):
           """Add a task with its duration."""
           node = GraphNode(name, task_id)
           self.graph.add_node(node)
           self.tasks[task_id] = {'node': node, 'duration': duration}
       
       def add_dependency(self, predecessor_id, successor_id):
           """Add task dependency."""
           pred = self.tasks[predecessor_id]['node']
           succ = self.tasks[successor_id]['node']
           duration = self.tasks[predecessor_id]['duration']
           
           # Edge weight = duration of predecessor task
           edge = WeightedDirectedEdge(pred, succ, weight=duration)
           self.graph.add_edge(edge)
       
       def find_critical_path(self, start_id, end_id):
           """Find critical path (longest path) from start to end."""
           start = self.tasks[start_id]['node']
           end = self.tasks[end_id]['node']
           
           # For longest path, use negative weights with shortest path
           # Or implement topological sort + dynamic programming
           
           # Topological sort
           visited = set()
           stack = []
           
           def dfs(node):
               visited.add(node.id)
               for successor in self.graph.successors(node):
                   if successor.id not in visited:
                       dfs(successor)
               stack.append(node)
           
           for node in self.graph.nodes():
               if node.id not in visited:
                   dfs(node)
           
           stack.reverse()
           
           # Calculate longest paths
           distances = {node.id: float('-infinity') for node in self.graph.nodes()}
           distances[start.id] = 0
           previous = {node.id: None for node in self.graph.nodes()}
           
           for node in stack:
               if distances[node.id] != float('-infinity'):
                   for successor in self.graph.successors(node):
                       edge_weight = self.graph.get_edge_weight(node, successor)
                       # Add task duration at current node
                       task_duration = self.tasks[node.id]['duration']
                       new_distance = distances[node.id] + edge_weight
                       
                       if new_distance > distances[successor.id]:
                           distances[successor.id] = new_distance
                           previous[successor.id] = node
           
           # Reconstruct path
           path = []
           current = end
           while current:
               path.append(current)
               current = previous[current.id]
           
           path.reverse()
           
           # Calculate total duration
           total_duration = distances[end.id] + self.tasks[end.id]['duration']
           
           return path, total_duration
       
       def calculate_slack(self, task_id, critical_path_duration):
           """Calculate slack time for a task."""
           # Simplified implementation
           return 0  # Would need forward/backward pass
   
   # Usage
   scheduler = ProjectScheduler()
   
   # Add tasks
   scheduler.add_task("Start", "start", 0)
   scheduler.add_task("Design", "design", 5)
   scheduler.add_task("Code Backend", "backend", 10)
   scheduler.add_task("Code Frontend", "frontend", 8)
   scheduler.add_task("Testing", "testing", 7)
   scheduler.add_task("Deploy", "deploy", 2)
   scheduler.add_task("End", "end", 0)
   
   # Add dependencies
   scheduler.add_dependency("start", "design")
   scheduler.add_dependency("design", "backend")
   scheduler.add_dependency("design", "frontend")
   scheduler.add_dependency("backend", "testing")
   scheduler.add_dependency("frontend", "testing")
   scheduler.add_dependency("testing", "deploy")
   scheduler.add_dependency("deploy", "end")
   
   # Find critical path
   path, duration = scheduler.find_critical_path("start", "end")
   
   print("Critical Path:")
   for task in path:
       print(f"  → {task.data}")
   
   print(f"\nProject duration: {duration} days")

Application 4: Currency Exchange
---------------------------------

Find best exchange rates using weighted directed graph:

.. code-block:: python

   from sds.graph import WeightedDirectedGraph, GraphNode, WeightedDirectedEdge
   import math

   class CurrencyExchange:
       """Currency exchange rate analysis."""
       
       def __init__(self):
           self.graph = WeightedDirectedGraph()
           self.currencies = {}
       
       def add_currency(self, code):
           """Add a currency."""
           node = GraphNode(code, code)
           self.graph.add_node(node)
           self.currencies[code] = node
       
       def add_exchange_rate(self, from_currency, to_currency, rate):
           """Add exchange rate (1 from_currency = rate to_currency)."""
           from_node = self.currencies[from_currency]
           to_node = self.currencies[to_currency]
           
           # Use negative log for finding best rate with shortest path
           # log(rate) becomes weight
           weight = -math.log(rate)
           
           edge = WeightedDirectedEdge(from_node, to_node, weight=weight)
           self.graph.add_edge(edge)
       
       def find_best_exchange(self, from_currency, to_currency):
           """Find best exchange path using Bellman-Ford."""
           start = self.currencies[from_currency]
           end = self.currencies[to_currency]
           
           # Bellman-Ford for negative weights
           distances = {node.id: float('infinity') for node in self.graph.nodes()}
           distances[start.id] = 0
           previous = {node.id: None for node in self.graph.nodes()}
           
           # Relax edges V-1 times
           for _ in range(self.graph.node_count() - 1):
               for edge in self.graph.edges():
                   u = edge.source
                   v = edge.target
                   
                   if distances[u.id] + edge.weight < distances[v.id]:
                       distances[v.id] = distances[u.id] + edge.weight
                       previous[v.id] = u
           
           # Check for arbitrage (negative cycle)
           for edge in self.graph.edges():
               u = edge.source
               v = edge.target
               if distances[u.id] + edge.weight < distances[v.id]:
                   print("Arbitrage opportunity detected!")
           
           # Reconstruct path
           path = []
           current = end
           while current:
               path.append(current)
               current = previous[current.id]
           
           path.reverse()
           
           # Calculate effective rate
           if distances[end.id] == float('infinity'):
               return None, 0
           
           effective_rate = math.exp(-distances[end.id])
           
           return path, effective_rate
   
   # Usage
   exchange = CurrencyExchange()
   
   # Add currencies
   for currency in ["USD", "EUR", "GBP", "JPY"]:
       exchange.add_currency(currency)
   
   # Add exchange rates
   exchange.add_exchange_rate("USD", "EUR", 0.92)
   exchange.add_exchange_rate("EUR", "USD", 1.09)
   exchange.add_exchange_rate("USD", "GBP", 0.79)
   exchange.add_exchange_rate("GBP", "USD", 1.27)
   exchange.add_exchange_rate("EUR", "GBP", 0.86)
   exchange.add_exchange_rate("GBP", "EUR", 1.16)
   exchange.add_exchange_rate("USD", "JPY", 149.50)
   exchange.add_exchange_rate("JPY", "USD", 0.0067)
   
   # Find best exchange path
   path, rate = exchange.find_best_exchange("USD", "GBP")
   
   if path:
       route = " → ".join(node.data for node in path)
       print(f"Best exchange route: {route}")
       print(f"Effective rate: 1 USD = {rate:.4f} GBP")
       print(f"For $1000: £{1000 * rate:.2f}")

Best Practices
==============

Do's
----

✅ **Choose appropriate weight representation**

.. code-block:: python

   # For distances: positive weights
   road = WeightedEdge(city1, city2, weight=150.5)
   
   # For costs: typically positive
   connection = WeightedEdge(server1, server2, weight=cost)
   
   # For profits: can be negative
   trade = WeightedDirectedEdge(stock1, stock2, weight=-loss)

✅ **Use Dijkstra for non-negative weights**

.. code-block:: python

   # Faster and simpler for non-negative weights
   # O((V + E) log V) vs O(VE) for Bellman-Ford
   
   if all_weights_non_negative:
       path = dijkstra(graph, start, end)
   else:
       path = bellman_ford(graph, start, end)

✅ **Cache total weight for static graphs**

.. code-block:: python

   class OptimizedWeightedGraph(WeightedGraph):
       def __init__(self):
           super().__init__()
           self._cached_total = None
       
       def total_weight(self):
           if self._cached_total is None:
               self._cached_total = super().total_weight()
           return self._cached_total
       
       def add_edge(self, edge):
           super().add_edge(edge)
           self._cached_total = None  # Invalidate cache

✅ **Validate weights in critical applications**

.. code-block:: python

   def add_safe_edge(graph, node1, node2, weight):
       """Add edge with weight validation."""
       if not isinstance(weight, (int, float)):
           raise TypeError(f"Weight must be numeric, got {type(weight)}")
       
       if math.isnan(weight) or math.isinf(weight):
           raise ValueError(f"Invalid weight: {weight}")
       
       edge = WeightedEdge(node1, node2, weight=weight)
       graph.add_edge(edge)

Don'ts
------

❌ **Don't use Dijkstra with negative weights**

.. code-block:: python

   # Bad: Dijkstra fails with negative weights
   graph_with_negatives = WeightedGraph()
   # ... add edges with negative weights ...
   # dijkstra(graph_with_negatives)  # WRONG RESULTS!
   
   # Good: Use Bellman-Ford instead
   bellman_ford(graph_with_negatives, start, end)

❌ **Don't ignore weight updates**

.. code-block:: python

   # Bad: Forgetting to update dependent calculations
   graph.add_edge(WeightedEdge(a, b, weight=10))
   cached_total = graph.total_weight()
   
   # ... later ...
   edge = graph.get_edge(a, b)
   graph.remove_edge(edge)
   graph.add_edge(WeightedEdge(a, b, weight=20))
   # cached_total is now wrong!
   
   # Good: Recalculate or invalidate cache
   cached_total = graph.total_weight()

❌ **Don't confuse directed/undirected weights**

.. code-block:: python

   # In undirected graph: weight applies both directions
   undirected = WeightedGraph()
   undirected.add_edge(WeightedEdge(a, b, weight=10))
   # Both a→b and b→a have weight 10
   
   # In directed graph: weights are directional
   directed = WeightedDirectedGraph()
   directed.add_edge(WeightedDirectedEdge(a, b, weight=10))
   # Only a→b has weight 10; b→a doesn't exist

Comparison with Other Structures
=================================

.. list-table::
   :header-rows: 1
   :widths: 25 25 25 25

   * - Aspect
     - Unweighted Graph
     - Weighted Graph
     - Notes
   * - **Edge Information**
     - Binary (exists/not)
     - Numeric weight
     - More expressive
   * - **Shortest Path**
     - BFS (O(V+E))
     - Dijkstra/Bellman-Ford
     - More complex
   * - **MST**
     - N/A
     - Kruskal/Prim
     - Unique to weighted
   * - **Memory**
     - O(V+E)
     - O(V+E) + weights
     - Small overhead
   * - **Algorithms**
     - Simpler
     - More sophisticated
     - More powerful

When to Use Weighted Graphs
----------------------------

**Use weighted graphs when:**

* Connections have varying costs, distances, or capacities
* Need to find optimal paths (minimum cost/distance)
* Building network infrastructure (minimum spanning tree)
* Modeling flow networks
* Comparing multiple routes or solutions

**Use unweighted graphs when:**

* Only connectivity matters (not strength/cost)
* All edges are equivalent
* Simpler algorithms sufficient
* Memory is very constrained

Further Reading
===============

* :doc:`/api/graph/weighted` - Complete API reference
* :doc:`general` - Basic graph structures
* :doc:`directed` - Directed graphs
* :doc:`adjacency` - Graph representations

References
==========

Shortest Path Algorithms
-------------------------

.. [Dijkstra1959] Dijkstra, E. W. "A note on two problems in connexion with graphs", 1959.
   Numerische Mathematik 1, 269-271.
   https://doi.org/10.1007/BF01386390
   
   Original paper introducing Dijkstra's algorithm for shortest paths.

.. [BellmanFord] Bellman, R. "On a routing problem", 1958. Quarterly of Applied Mathematics.
   Ford, L. R. "Network Flow Theory", 1956. RAND Corporation.
   
   Foundations of the Bellman-Ford algorithm for negative weights.

Minimum Spanning Tree
----------------------

.. [Kruskal1956] Kruskal, J. B. "On the shortest spanning subtree of a graph", 1956.
   Proceedings of the American Mathematical Society 7(1), 48-50.
   
   Kruskal's algorithm for minimum spanning trees.

.. [Prim1957] Prim, R. C. "Shortest connection networks", 1957.
   Bell System Technical Journal 36(6), 1389-1401.
   
   Prim's algorithm for MST construction.

.. [Boruvka1926] Borůvka, O. "O jistém problému minimálním", 1926.
   Práce Moravské Přírodovědecké Společnosti 3, 37-58.
   
   First MST algorithm (Borůvka's algorithm), predates Kruskal and Prim.

Textbooks and Online Resources
-------------------------------

.. [CLRS] Cormen, T. H., et al. "Introduction to Algorithms", 3rd Edition, 2009.
   Chapters 22-25: Graph Algorithms
   
   * Single-source shortest paths
   * All-pairs shortest paths
   * Maximum flow
   * Minimum spanning trees

.. [OpenDSAGraphs] OpenDSA Project. "Graph Algorithms".
   https://opendsa-server.cs.vt.edu/ODSA/Books/Everything/html/
   
   Interactive modules on:
   
   * Dijkstra's algorithm
   * Minimum spanning trees
   * Network flow

.. [MIT6006] MIT OCW. "6.006 Introduction to Algorithms".
   https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/
   
   Lecture notes and videos on graph algorithms.

.. [WikiDijkstra] Wikipedia. "Dijkstra's algorithm".
   https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
   
   Comprehensive overview with visualizations and pseudocode.

.. [WikiMST] Wikipedia. "Minimum spanning tree".
   https://en.wikipedia.org/wiki/Minimum_spanning_tree
   
   Overview of MST algorithms and applications.

.. [VisuAlgoSSSP] VisuAlgo. "Single-Source Shortest Paths".
   https://visualgo.net/en/sssp
   
   Interactive visualizations of Dijkstra and Bellman-Ford.

.. [VisuAlgoMST] VisuAlgo. "Minimum Spanning Tree".
   https://visualgo.net/en/mst
   
   Interactive visualizations of Kruskal and Prim algorithms.

Applications and Advanced Topics
---------------------------------

.. [NetworkX] NetworkX Documentation. "Shortest Paths".
   https://networkx.org/documentation/stable/reference/algorithms/shortest_paths.html
   
   Python library with weighted graph algorithms.

.. [FloydWarshall] Floyd, R. W. "Algorithm 97: Shortest Path", 1962.
   Communications of the ACM 5(6), 345.
   
   All-pairs shortest path algorithm (O(V³)).

.. [Johnson] Johnson, D. B. "Efficient algorithms for shortest paths", 1977.
   Journal of the ACM 24(1), 1-13.
   
   All-pairs shortest paths with negative weights.