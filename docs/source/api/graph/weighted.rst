.. _api_graph_weighted:

===============
Weighted Graphs
===============

.. currentmodule:: sds.graph.weighted

Overview
========

This module provides weighted graph implementations where edges have associated numeric
weights representing costs, distances, capacities, or other metrics. WeightedGraph handles
undirected weighted edges, while WeightedDirectedGraph combines direction with weights.

.. mermaid::

   graph TB
       subgraph "Weighted Undirected Graph"
       A1[A] ---|5| B1[B]
       A1 ---|3| C1[C]
       B1 ---|7| C1
       end
       
       subgraph "Weighted Directed Graph"
       A2[A] -->|5| B2[B]
       A2 -->|3| C2[C]
       B2 -->|7| C2
       C2 -->|2| A2
       end
       
       style A1 fill:#e74c3c,color:#fff
       style A2 fill:#3498db,color:#fff

Classes
=======

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   WeightedGraph
   WeightedDirectedGraph

Detailed Documentation
======================

WeightedGraph
-------------

.. autoclass:: WeightedGraph
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

   .. rubric:: Weight Operations

   .. automethod:: get_edge_weight
   .. automethod:: total_weight
   .. automethod:: incident_edges

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

WeightedDirectedGraph
---------------------

.. autoclass:: WeightedDirectedGraph
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

   .. rubric:: Weight Operations

   .. automethod:: get_edge_weight
   .. automethod:: total_weight
   .. automethod:: incident_edges

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

   .. rubric:: Special Methods

   .. automethod:: __len__
   .. automethod:: __contains__
   .. automethod:: __iter__
   .. automethod:: __repr__
   .. automethod:: __str__

Usage Examples
==============

WeightedGraph Examples
----------------------

Creating a Weighted Graph
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.graph import WeightedGraph, GraphNode, WeightedEdge

   # Create weighted graph
   g = WeightedGraph()
   
   # Create with multi-edge support
   mg = WeightedGraph(allow_multi_edges=True)
   
   print(g.is_empty())  # Output: True

Adding Weighted Edges
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Create nodes
   paris = GraphNode("Paris", "paris")
   london = GraphNode("London", "london")
   berlin = GraphNode("Berlin", "berlin")
   
   g.add_node(paris)
   g.add_node(london)
   g.add_node(berlin)
   
   # Add weighted edges (distances in km)
   g.add_edge(WeightedEdge(paris, london, weight=344.0))
   g.add_edge(WeightedEdge(paris, berlin, weight=878.0))
   g.add_edge(WeightedEdge(london, berlin, weight=932.0))
   
   print(f"Nodes: {g.node_count()}")  # Output: 3
   print(f"Edges: {g.edge_count()}")  # Output: 3

Getting Edge Weights
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Get weight of specific edge
   weight = g.get_edge_weight(paris, london)
   print(f"Paris to London: {weight} km")  # Output: 344.0
   
   # Get total weight of all edges
   total = g.total_weight()
   print(f"Total distance: {total} km")  # Output: 2154.0

Working with Weighted Edges
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Get all incident edges with weights
   edges = g.incident_edges(paris)
   
   for edge in edges:
       other = edge.other_node(paris)
       print(f"Paris to {other.data}: {edge.weight} km")
   # Output:
   # Paris to London: 344.0 km
   # Paris to Berlin: 878.0 km

Finding Shortest/Longest Paths
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Find shortest edge from node
   def shortest_edge(graph, node):
       edges = graph.incident_edges(node)
       if not edges:
           return None
       return min(edges, key=lambda e: e.weight)
   
   shortest = shortest_edge(g, paris)
   other = shortest.other_node(paris)
   print(f"Shortest from Paris: {other.data} ({shortest.weight} km)")
   # Output: Shortest from Paris: London (344.0 km)
   
   # Find longest edge
   def longest_edge(graph, node):
       edges = graph.incident_edges(node)
       if not edges:
           return None
       return max(edges, key=lambda e: e.weight)
   
   longest = longest_edge(g, paris)
   other = longest.other_node(paris)
   print(f"Longest from Paris: {other.data} ({longest.weight} km)")
   # Output: Longest from Paris: Berlin (878.0 km)

Multi-Weighted Edges
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Multiple weighted edges (e.g., different routes)
   mg = WeightedGraph(allow_multi_edges=True)
   
   mg.add_node(paris)
   mg.add_node(london)
   
   # Different routes with different costs
   mg.add_edge(WeightedEdge(paris, london, weight=344.0, data="highway"))
   mg.add_edge(WeightedEdge(paris, london, weight=420.0, data="scenic"))
   mg.add_edge(WeightedEdge(paris, london, weight=300.0, data="fast_train"))
   
   print(f"Routes: {mg.edge_count()}")  # Output: 3
   
   # Get all routes
   routes = mg.incident_edges(paris)
   for route in routes:
       print(f"{route.data}: {route.weight} km")

WeightedDirectedGraph Examples
-------------------------------

Creating Weighted Directed Graph
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.graph import WeightedDirectedGraph, GraphNode, WeightedDirectedEdge

   # Create weighted directed graph
   dg = WeightedDirectedGraph()
   
   # Add nodes (cities)
   paris = GraphNode("Paris", "paris")
   london = GraphNode("London", "london")
   berlin = GraphNode("Berlin", "berlin")
   
   dg.add_node(paris)
   dg.add_node(london)
   dg.add_node(berlin)

Directed Weighted Edges
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Add directed edges with weights (flight costs)
   dg.add_edge(WeightedDirectedEdge(paris, london, weight=120.0))
   dg.add_edge(WeightedDirectedEdge(london, paris, weight=150.0))
   dg.add_edge(WeightedDirectedEdge(paris, berlin, weight=200.0))
   dg.add_edge(WeightedDirectedEdge(berlin, london, weight=180.0))
   
   # Direction matters!
   print(dg.get_edge_weight(paris, london))  # 120.0
   print(dg.get_edge_weight(london, paris))  # 150.0

In/Out Degree with Weights
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Out-degree: number of outgoing edges
   print(f"Flights from Paris: {dg.out_degree(paris)}")  # Output: 2
   
   # In-degree: number of incoming edges
   print(f"Flights to London: {dg.in_degree(london)}")  # Output: 2
   
   # Total cost of outgoing flights
   outgoing = [e for e in dg.incident_edges(paris) if e.source.id == paris.id]
   total_out = sum(e.weight for e in outgoing)
   print(f"Total cost from Paris: €{total_out}")  # Output: €320.0

Weighted Paths
^^^^^^^^^^^^^^

.. code-block:: python

   # Find cheapest outgoing flight
   def cheapest_flight(graph, from_city):
       flights = [
           e for e in graph.incident_edges(from_city)
           if e.source.id == from_city.id
       ]
       if not flights:
           return None
       return min(flights, key=lambda e: e.weight)
   
   cheap = cheapest_flight(dg, paris)
   print(f"Cheapest from Paris: {cheap.target.data} (€{cheap.weight})")
   # Output: Cheapest from Paris: London (€120.0)

Weighted DAG Operations
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Create task graph with time estimates
   tasks = WeightedDirectedGraph()
   
   design = GraphNode("Design", "t1")
   implement = GraphNode("Implement", "t2")
   test = GraphNode("Test", "t3")
   deploy = GraphNode("Deploy", "t4")
   
   tasks.add_node(design)
   tasks.add_node(implement)
   tasks.add_node(test)
   tasks.add_node(deploy)
   
   # Dependencies with time estimates (hours)
   tasks.add_edge(WeightedDirectedEdge(design, implement, weight=40.0))
   tasks.add_edge(WeightedDirectedEdge(implement, test, weight=20.0))
   tasks.add_edge(WeightedDirectedEdge(test, deploy, weight=5.0))
   
   # Check if valid DAG
   print(f"Valid schedule: {tasks.is_acyclic()}")  # True
   
   # Calculate critical path (longest path)
   total = tasks.total_weight()
   print(f"Total project time: {total} hours")  # 65.0

Real-World Examples
===================

Example 1: City Distance Map
-----------------------------

Weighted graph for city distances:

.. code-block:: python

   from sds.graph import WeightedGraph, GraphNode, WeightedEdge

   class CityDistanceMap:
       """City network with distances."""
       
       def __init__(self):
           self.graph = WeightedGraph()
           self.cities = {}
       
       def add_city(self, city_id, name):
           """Add a city."""
           node = GraphNode(name, city_id)
           self.graph.add_node(node)
           self.cities[city_id] = node
       
       def add_road(self, city1_id, city2_id, distance):
           """Add road between cities with distance."""
           city1 = self.cities[city1_id]
           city2 = self.cities[city2_id]
           edge = WeightedEdge(city1, city2, weight=distance)
           self.graph.add_edge(edge)
       
       def get_distance(self, city1_id, city2_id):
           """Get distance between cities."""
           city1 = self.cities[city1_id]
           city2 = self.cities[city2_id]
           return self.graph.get_edge_weight(city1, city2)
       
       def nearest_cities(self, city_id, n=3):
           """Find n nearest cities."""
           city = self.cities[city_id]
           edges = self.graph.incident_edges(city)
           
           # Sort by distance
           edges_sorted = sorted(edges, key=lambda e: e.weight)
           
           nearest = []
           for edge in edges_sorted[:n]:
               other = edge.other_node(city)
               nearest.append((other.data, edge.weight))
           
           return nearest
       
       def total_road_length(self):
           """Get total length of all roads."""
           return self.graph.total_weight()
   
   # Usage
   distance_map = CityDistanceMap()
   
   # Add cities
   distance_map.add_city("paris", "Paris")
   distance_map.add_city("london", "London")
   distance_map.add_city("berlin", "Berlin")
   distance_map.add_city("rome", "Rome")
   distance_map.add_city("madrid", "Madrid")
   
   # Add roads with distances (km)
   distance_map.add_road("paris", "london", 344)
   distance_map.add_road("paris", "berlin", 878)
   distance_map.add_road("paris", "rome", 1105)
   distance_map.add_road("paris", "madrid", 1053)
   distance_map.add_road("london", "berlin", 932)
   distance_map.add_road("berlin", "rome", 1184)
   
   # Query distances
   dist = distance_map.get_distance("paris", "london")
   print(f"Paris to London: {dist} km")
   
   # Find nearest cities
   nearest = distance_map.nearest_cities("paris", n=3)
   print(f"Nearest to Paris: {nearest}")
   
   # Total road network
   total = distance_map.total_road_length()
   print(f"Total road network: {total} km")

Example 2: Flight Network
--------------------------

Weighted directed graph for flight routes:

.. code-block:: python

   from sds.graph import WeightedDirectedGraph, GraphNode, WeightedDirectedEdge

   class FlightNetwork:
       """Airline flight network with costs."""
       
       def __init__(self):
           self.graph = WeightedDirectedGraph()
           self.airports = {}
       
       def add_airport(self, code, name):
           """Add an airport."""
           node = GraphNode(name, code)
           self.graph.add_node(node)
           self.airports[code] = node
       
       def add_flight(self, from_code, to_code, cost):
           """Add direct flight with cost."""
           from_airport = self.airports[from_code]
           to_airport = self.airports[to_code]
           edge = WeightedDirectedEdge(from_airport, to_airport, weight=cost)
           self.graph.add_edge(edge)
       
       def get_flight_cost(self, from_code, to_code):
           """Get direct flight cost."""
           from_airport = self.airports[from_code]
           to_airport = self.airports[to_code]
           return self.graph.get_edge_weight(from_airport, to_airport)
       
       def outgoing_flights(self, airport_code):
           """Get all outgoing flights."""
           airport = self.airports[airport_code]
           flights = []
           
           for successor in self.graph.successors(airport):
               cost = self.graph.get_edge_weight(airport, successor)
               flights.append({
                   'to': successor.data,
                   'code': successor.id,
                   'cost': cost
               })
           
           return flights
       
       def incoming_flights(self, airport_code):
           """Get all incoming flights."""
           airport = self.airports[airport_code]
           flights = []
           
           for predecessor in self.graph.predecessors(airport):
               cost = self.graph.get_edge_weight(predecessor, airport)
               flights.append({
                   'from': predecessor.data,
                   'code': predecessor.id,
                   'cost': cost
               })
           
           return flights
       
       def cheapest_outgoing(self, airport_code):
           """Find cheapest outgoing flight."""
           flights = self.outgoing_flights(airport_code)
           if not flights:
               return None
           return min(flights, key=lambda f: f['cost'])
       
       def hub_importance(self, airport_code):
           """Calculate hub importance (total connections)."""
           airport = self.airports[airport_code]
           return self.graph.degree(airport)
   
   # Usage
   network = FlightNetwork()
   
   # Add airports
   network.add_airport("CDG", "Paris Charles de Gaulle")
   network.add_airport("LHR", "London Heathrow")
   network.add_airport("FRA", "Frankfurt")
   network.add_airport("AMS", "Amsterdam")
   
   # Add flights (different costs for different directions)
   network.add_flight("CDG", "LHR", 120)
   network.add_flight("LHR", "CDG", 150)
   network.add_flight("CDG", "FRA", 180)
   network.add_flight("FRA", "CDG", 160)
   network.add_flight("LHR", "AMS", 100)
   network.add_flight("AMS", "LHR", 110)
   network.add_flight("FRA", "AMS", 90)
   
   # Query network
   outgoing = network.outgoing_flights("CDG")
   print(f"Flights from Paris: {outgoing}")
   
   cheapest = network.cheapest_outgoing("CDG")
   print(f"Cheapest from Paris: {cheapest}")
   
   importance = network.hub_importance("LHR")
   print(f"London hub importance: {importance}")

Example 3: Network Bandwidth
-----------------------------

Network links with bandwidth capacities:

.. code-block:: python

   from sds.graph import WeightedGraph, GraphNode, WeightedEdge

   class NetworkBandwidth:
       """Computer network with link capacities."""
       
       def __init__(self):
           self.graph = WeightedGraph()
           self.nodes = {}
       
       def add_node(self, node_id, name):
           """Add network node."""
           node = GraphNode(name, node_id)
           self.graph.add_node(node)
           self.nodes[node_id] = node
       
       def add_link(self, node1_id, node2_id, bandwidth_mbps):
           """Add network link with bandwidth (Mbps)."""
           node1 = self.nodes[node1_id]
           node2 = self.nodes[node2_id]
           edge = WeightedEdge(node1, node2, weight=bandwidth_mbps)
           self.graph.add_edge(edge)
       
       def get_bandwidth(self, node1_id, node2_id):
           """Get link bandwidth."""
           node1 = self.nodes[node1_id]
           node2 = self.nodes[node2_id]
           return self.graph.get_edge_weight(node1, node2)
       
       def bottleneck_links(self, threshold=100):
           """Find links below bandwidth threshold."""
           bottlenecks = []
           
           for edge in self.graph.edges():
               if edge.weight < threshold:
                   bottlenecks.append({
                       'link': f"{edge.node1.data} - {edge.node2.data}",
                       'bandwidth': edge.weight
                   })
           
           return bottlenecks
       
       def total_capacity(self):
           """Calculate total network capacity."""
           return self.graph.total_weight()
       
       def node_capacity(self, node_id):
           """Calculate total capacity connected to node."""
           node = self.nodes[node_id]
           edges = self.graph.incident_edges(node)
           return sum(e.weight for e in edges)
   
   # Usage
   network = NetworkBandwidth()
   
   # Add nodes
   network.add_node("r1", "Router 1")
   network.add_node("r2", "Router 2")
   network.add_node("r3", "Router 3")
   network.add_node("s1", "Switch 1")
   network.add_node("s2", "Switch 2")
   
   # Add links with bandwidth (Mbps)
   network.add_link("r1", "r2", 1000)  # 1 Gbps
   network.add_link("r1", "r3", 1000)
   network.add_link("r2", "s1", 100)   # 100 Mbps
   network.add_link("r2", "s2", 100)
   network.add_link("r3", "s1", 100)
   network.add_link("r3", "s2", 100)
   
   # Analyze network
   total = network.total_capacity()
   print(f"Total capacity: {total} Mbps")
   
   bottlenecks = network.bottleneck_links(threshold=500)
   print(f"Bottleneck links: {bottlenecks}")
   
   capacity = network.node_capacity("r1")
   print(f"Router 1 capacity: {capacity} Mbps")

Example 4: Weighted Task Graph
-------------------------------

Project tasks with durations:

.. code-block:: python

   from sds.graph import WeightedDirectedGraph, GraphNode, WeightedDirectedEdge

   class ProjectSchedule:
       """Project tasks with time estimates."""
       
       def __init__(self):
           self.graph = WeightedDirectedGraph()
           self.tasks = {}
       
       def add_task(self, task_id, name, duration):
           """Add task with duration (hours)."""
           data = {'name': name, 'duration': duration}
           node = GraphNode(data, task_id)
           self.graph.add_node(node)
           self.tasks[task_id] = node
       
       def add_dependency(self, from_task_id, to_task_id, setup_time=0):
           """Add dependency with optional setup time."""
           from_task = self.tasks[from_task_id]
           to_task = self.tasks[to_task_id]
           edge = WeightedDirectedEdge(from_task, to_task, weight=setup_time)
           self.graph.add_edge(edge)
       
       def is_valid(self):
           """Check if schedule has no cycles."""
           return self.graph.is_acyclic()
       
       def task_duration(self, task_id):
           """Get task duration."""
           task = self.tasks[task_id]
           return task.data['duration']
       
       def setup_time(self, from_task_id, to_task_id):
           """Get setup time between tasks."""
           from_task = self.tasks[from_task_id]
           to_task = self.tasks[to_task_id]
           return self.graph.get_edge_weight(from_task, to_task)
       
       def critical_path_length(self):
           """Estimate critical path (simplified)."""
           if not self.is_valid():
               raise ValueError("Schedule has cycles")
           
           # Sum all task durations + setup times
           total = sum(t.data['duration'] for t in self.tasks.values())
           total += self.graph.total_weight()  # Add all setup times
           
           return total
   
   # Usage
   project = ProjectSchedule()
   
   # Add tasks
   project.add_task("design", "Design", 40)
   project.add_task("implement", "Implement", 80)
   project.add_task("test", "Test", 20)
   project.add_task("deploy", "Deploy", 5)
   
   # Add dependencies with setup times
   project.add_dependency("design", "implement", setup_time=2)
   project.add_dependency("implement", "test", setup_time=1)
   project.add_dependency("test", "deploy", setup_time=0.5)
   
   # Validate and analyze
   if project.is_valid():
       total = project.critical_path_length()
       print(f"Total project time: {total} hours")
   else:
       print("Invalid schedule: cycle detected")

Performance Characteristics
===========================

WeightedGraph Time Complexity
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
     - O(1) or O(degree)
     - Check duplicates in simple graph
   * - ``get_edge_weight(n1, n2)``
     - O(E)
     - Must find edge
   * - ``total_weight()``
     - O(E) or O(1)
     - O(1) if cached
   * - ``incident_edges(node)``
     - O(E)
     - Filter edge list
   * - ``neighbors(node)``
     - O(degree)
     - Iterate adjacency

WeightedDirectedGraph Time Complexity
--------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 20 40

   * - Operation
     - Complexity
     - Notes
   * - ``add_edge(edge)``
     - O(1) or O(out_degree)
     - Check duplicates
   * - ``get_edge_weight(n1, n2)``
     - O(E)
     - Must find directed edge
   * - ``in_degree(node)``
     - O(1)
     - Cached in adjacency
   * - ``out_degree(node)``
     - O(1)
     - Cached in adjacency
   * - ``is_acyclic()``
     - O(V + E)
     - DFS with caching

Space Complexity
----------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Component
     - Space
   * - **Nodes**
     - O(V)
   * - **Adjacency lists**
     - O(V + E)
   * - **Edge list**
     - O(E)
   * - **Weights**
     - O(E) - stored in edges
   * - **Total**
     - O(V + E)

Comparison with Unweighted Graphs
==================================

.. list-table::
   :header-rows: 1
   :widths: 30 20 20 30

   * - Feature
     - Graph
     - WeightedGraph
     - Additional Cost
   * - **Edge Storage**
     - Edge
     - WeightedEdge
     - +8 bytes (float)
   * - **Weight Query**
     - N/A
     - O(E)
     - New operation
   * - **Total Weight**
     - N/A
     - O(E)
     - New operation
   * - **Pathfinding**
     - BFS
     - Dijkstra/A*
     - More complex
   * - **Use Cases**
     - Topology
     - Routing, planning
     - Cost-aware

When to Use Weighted Graphs
============================

Use WeightedGraph When
-----------------------

✅ **Modeling costs, distances, or capacities**

.. code-block:: python

   # Road networks, distances
   roads = WeightedGraph()
   
   # Network capacities
   network = WeightedGraph()

✅ **Need shortest/longest path algorithms**

.. code-block:: python

   # Dijkstra, Bellman-Ford require weights
   def dijkstra(graph, start, end):
       # Use edge weights for path calculation
       pass

✅ **Optimizing routes or flows**

.. code-block:: python

   # Minimize cost
   def min_cost_path(graph, start, end):
       # Consider edge weights
       pass

Use WeightedDirectedGraph When
-------------------------------

✅ **Asymmetric costs (A→B ≠ B→A)**

.. code-block:: python

   # Flight costs differ by direction
   flights = WeightedDirectedGraph()
   flights.add_edge(WeightedDirectedEdge(paris, london, 120))
   flights.add_edge(WeightedDirectedEdge(london, paris, 150))

✅ **Directed flows with capacities**

.. code-block:: python

   # Network flow, pipeline capacity
   pipeline = WeightedDirectedGraph()

✅ **Task scheduling with durations**

.. code-block:: python

   # Project tasks with time estimates
   schedule = WeightedDirectedGraph()

Best Practices
==============

Do's
----

✅ **Use appropriate weight types**

.. code-block:: python

   # Weights must be numeric
   edge = WeightedEdge(n1, n2, weight=10.5)  # float
   edge = WeightedEdge(n1, n2, weight=10)    # int (converted to float)

✅ **Cache total weight if needed frequently**

.. code-block:: python

   # total_weight() caches result until graph changes
   total = graph.total_weight()  # Cached on subsequent calls

✅ **Store additional data in edge data**

.. code-block:: python

   # Use data for metadata
   edge = WeightedEdge(n1, n2, weight=100, data={
       'type': 'highway',
       'lanes': 4,
       'speed_limit': 120
   })

✅ **Validate weights for your domain**

.. code-block:: python

   def add_valid_road(graph, city1, city2, distance):
       if distance <= 0:
           raise ValueError("Distance must be positive")
       graph.add_edge(WeightedEdge(city1, city2, weight=distance))

Don'ts
------

❌ **Don't use string weights**

.. code-block:: python

   # Bad: Raises TypeError
   edge = WeightedEdge(n1, n2, weight="100")
   
   # Good: Use numeric
   edge = WeightedEdge(n1, n2, weight=100)

❌ **Don't mix weighted and unweighted edges**

.. code-block:: python

   # Bad: Type error
   wg = WeightedGraph()
   wg.add_edge(Edge(n1, n2))  # Wrong edge type
   
   # Good: Use WeightedEdge
   wg.add_edge(WeightedEdge(n1, n2, weight=1.0))

❌ **Don't forget direction in WeightedDirectedGraph**

.. code-block:: python

   # Bad: Using WeightedEdge instead of WeightedDirectedEdge
   dg = WeightedDirectedGraph()
   # This will fail
   # dg.add_edge(WeightedEdge(n1, n2))
   
   # Good: Use directed version
   dg.add_edge(WeightedDirectedEdge(n1, n2, weight=10))

Common Pitfalls
===============

1. **Confusing edge weight with data**

.. code-block:: python

   # Weight is separate from data
   edge = WeightedEdge(n1, n2, weight=100.0, data="highway")
   print(edge.weight)  # 100.0
   print(edge.data)    # "highway"

2. **Negative weights in shortest path**

.. code-block:: python

   # Be careful with negative weights
   # Dijkstra doesn't work with negative weights
   # Use Bellman-Ford instead
   edge = WeightedEdge(n1, n2, weight=-10.0)  # Valid but problematic

3. **Not considering direction in costs**

.. code-block:: python

   # Different costs for different directions
   dg = WeightedDirectedGraph()
   dg.add_edge(WeightedDirectedEdge(n1, n2, weight=100))
   
   # Must add reverse edge separately if needed
   dg.add_edge(WeightedDirectedEdge(n2, n1, weight=120))

4. **Forgetting to update weights**

.. code-block:: python

   # Weights are immutable
   # To change weight, remove and re-add edge
   graph.remove_edge(old_edge)
   new_edge = WeightedEdge(n1, n2, weight=new_weight)
   graph.add_edge(new_edge)

See Also
========

* :doc:`graph` - Base unweighted graph
* :doc:`directed` - Directed graphs without weights
* :doc:`../../guide/graph_structures/weighted` - Weighted graphs user guide
* :doc:`../../algorithms/graph_algorithms` - Algorithms for weighted graphs

References
==========

.. [1] Cormen, T. H., et al. "Introduction to Algorithms", 3rd Edition, Chapter 24
.. [2] Sedgewick, R., Wayne, K. "Algorithms", 4th Edition, Chapter 4.4
.. [3] Ahuja, R. K., et al. "Network Flows", Prentice Hall, 1993
.. [4] Tarjan, R. E. "Data Structures and Network Algorithms", SIAM, 1983
