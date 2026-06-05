.. _api_graph_interfaces:

===================
Graph Interfaces
===================

.. currentmodule:: sds.graph.interfaces

Overview
========

This module defines the abstract base classes (interfaces) for all graph data structures
in the SDS library. These interfaces ensure a consistent API across different graph
implementations and provide a foundation for polymorphic graph operations.

.. mermaid::

   classDiagram
       Collection <|-- AbstractGraph
       AbstractGraph <|-- AbstractDirectedGraph
       
       class Collection {
           <<abstract>>
           +size: int
           +is_empty() bool
           +clear()
       }
       
       class AbstractGraph {
           <<abstract>>
           +add_node(node)
           +remove_node(node)
           +has_node(node) bool
           +add_edge(edge)
           +remove_edge(edge)
           +has_edge(n1, n2) bool
           +get_edge(n1, n2) Edge
           +neighbors(node) Iterator
           +degree(node) int
           +nodes() Iterator
           +edges() Iterator
           +node_count() int
           +edge_count() int
           +is_connected() bool
           +get_node_by_id(id) GraphNode
       }
       
       class AbstractDirectedGraph {
           <<abstract>>
           +in_degree(node) int
           +out_degree(node) int
           +predecessors(node) Iterator
           +successors(node) Iterator
           +is_acyclic() bool
       }

Classes
=======

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   AbstractGraph
   AbstractDirectedGraph

Detailed Documentation
======================

AbstractGraph
-------------

.. autoclass:: AbstractGraph
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __len__, __contains__, __iter__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Properties

   .. autoproperty:: size

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

   .. rubric:: Query Methods

   .. automethod:: neighbors
   .. automethod:: degree
   .. automethod:: nodes
   .. automethod:: edges
   .. automethod:: node_count
   .. automethod:: edge_count
   .. automethod:: is_connected

   .. rubric:: Special Methods

   .. automethod:: __len__
   .. automethod:: __contains__
   .. automethod:: __iter__

AbstractDirectedGraph
---------------------

.. autoclass:: AbstractDirectedGraph
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Directed Graph Operations

   .. automethod:: in_degree
   .. automethod:: out_degree
   .. automethod:: predecessors
   .. automethod:: successors
   .. automethod:: is_acyclic

Interface Hierarchy
===================

The graph interface hierarchy provides increasing specialization:

.. code-block:: text

   Collection (from sds.core)
       ↓
       └── AbstractGraph
           ├── Graph (undirected, unweighted)
           ├── WeightedGraph (undirected, weighted)
           ├── AdjacencyListGraph (explicit list representation)
           ├── AdjacencyMatrixGraph (matrix representation)
           └── AbstractDirectedGraph
               ├── DirectedGraph (directed, unweighted)
               └── WeightedDirectedGraph (directed, weighted)

**Interface guarantees:**

- All graph types support common operations (add_node, add_edge, etc.)
- Directed graphs add direction-specific operations (in_degree, successors, etc.)
- Consistent API enables polymorphic graph algorithms

Usage Examples
==============

Implementing Custom Graphs
---------------------------

Using AbstractGraph as a base:

.. code-block:: python

   from sds.graph.interfaces import AbstractGraph
   from sds.graph import GraphNode, Edge
   from typing import Iterator, Optional

   class SimpleGraph(AbstractGraph):
       """Minimal graph implementation using dictionaries."""
       
       def __init__(self):
           super().__init__()
           self._nodes = {}
           self._edges = []
           self._adjacency = {}
       
       def add_node(self, node: GraphNode) -> None:
           """Add a node to the graph."""
           if node.id in self._nodes:
               raise ValueError(f"Node {node.id} already exists")
           self._nodes[node.id] = node
           self._adjacency[node.id] = set()
           self._size += 1
       
       def remove_node(self, node: GraphNode) -> None:
           """Remove node and incident edges."""
           if node.id not in self._nodes:
               raise ValueError(f"Node {node.id} not in graph")
           
           # Remove incident edges
           self._edges = [e for e in self._edges 
                         if not e.incident_to(node)]
           
           # Update adjacency
           for neighbor_id in self._adjacency[node.id]:
               self._adjacency[neighbor_id].discard(node.id)
           
           del self._nodes[node.id]
           del self._adjacency[node.id]
           self._size -= 1
       
       def has_node(self, node: GraphNode) -> bool:
           """Check if node exists."""
           return node.id in self._nodes
       
       def add_edge(self, edge: Edge) -> None:
           """Add an edge."""
           if not self.has_node(edge.node1) or not self.has_node(edge.node2):
               raise ValueError("Both nodes must be in graph")
           
           self._edges.append(edge)
           self._adjacency[edge.node1.id].add(edge.node2.id)
           self._adjacency[edge.node2.id].add(edge.node1.id)
       
       def remove_edge(self, edge: Edge) -> None:
           """Remove an edge."""
           if edge not in self._edges:
               raise ValueError("Edge not in graph")
           
           self._edges.remove(edge)
           self._adjacency[edge.node1.id].discard(edge.node2.id)
           self._adjacency[edge.node2.id].discard(edge.node1.id)
       
       def has_edge(self, node1: GraphNode, node2: GraphNode) -> bool:
           """Check if edge exists."""
           if not self.has_node(node1) or not self.has_node(node2):
               return False
           return node2.id in self._adjacency[node1.id]
       
       def get_edge(self, node1: GraphNode, 
                    node2: GraphNode) -> Optional[Edge]:
           """Get edge between nodes."""
           for edge in self._edges:
               if edge.connects(node1, node2):
                   return edge
           return None
       
       def neighbors(self, node: GraphNode) -> Iterator[GraphNode]:
           """Get all neighbors."""
           if not self.has_node(node):
               raise ValueError(f"Node {node.id} not in graph")
           
           for neighbor_id in self._adjacency[node.id]:
               yield self._nodes[neighbor_id]
       
       def degree(self, node: GraphNode) -> int:
           """Get node degree."""
           if not self.has_node(node):
               raise ValueError(f"Node {node.id} not in graph")
           return len(self._adjacency[node.id])
       
       def nodes(self) -> Iterator[GraphNode]:
           """Iterate over all nodes."""
           yield from self._nodes.values()
       
       def edges(self) -> Iterator[Edge]:
           """Iterate over all edges."""
           yield from self._edges
       
       def node_count(self) -> int:
           """Get number of nodes."""
           return len(self._nodes)
       
       def edge_count(self) -> int:
           """Get number of edges."""
           return len(self._edges)
       
       def is_connected(self) -> bool:
           """Check if graph is connected (BFS)."""
           if self.is_empty():
               return True
           
           start = next(iter(self._nodes.values()))
           visited = {start.id}
           queue = [start]
           
           while queue:
               current = queue.pop(0)
               for neighbor in self.neighbors(current):
                   if neighbor.id not in visited:
                       visited.add(neighbor.id)
                       queue.append(neighbor)
           
           return len(visited) == self.node_count()
       
       def get_node_by_id(self, node_id: str) -> Optional[GraphNode]:
           """Get node by ID."""
           return self._nodes.get(node_id)

   # Usage
   graph = SimpleGraph()
   
   n1 = GraphNode("A", node_id="n1")
   n2 = GraphNode("B", node_id="n2")
   
   graph.add_node(n1)
   graph.add_node(n2)
   graph.add_edge(Edge(n1, n2))
   
   print(f"Nodes: {graph.node_count()}")
   print(f"Connected: {graph.is_connected()}")

Polymorphic Graph Operations
-----------------------------

Working with any graph type through the interface:

.. code-block:: python

   from sds.graph.interfaces import AbstractGraph
   from sds.graph import GraphNode
   from typing import Set, List

   def find_isolated_nodes(graph: AbstractGraph) -> List[GraphNode]:
       """Find all nodes with degree 0."""
       isolated = []
       for node in graph.nodes():
           if graph.degree(node) == 0:
               isolated.append(node)
       return isolated

   def graph_density(graph: AbstractGraph) -> float:
       """Calculate graph density."""
       n = graph.node_count()
       if n < 2:
           return 0.0
       m = graph.edge_count()
       max_edges = n * (n - 1) / 2
       return m / max_edges if max_edges > 0 else 0.0

   def common_neighbors(graph: AbstractGraph, 
                       node1: GraphNode, 
                       node2: GraphNode) -> Set[GraphNode]:
       """Find common neighbors of two nodes."""
       neighbors1 = set(graph.neighbors(node1))
       neighbors2 = set(graph.neighbors(node2))
       return neighbors1 & neighbors2

   def average_degree(graph: AbstractGraph) -> float:
       """Calculate average node degree."""
       if graph.is_empty():
           return 0.0
       total_degree = sum(graph.degree(node) for node in graph.nodes())
       return total_degree / graph.node_count()

   # Works with any graph implementation
   from sds.graph import Graph, AdjacencyListGraph

   g1 = Graph()
   # ... populate g1 ...
   print(f"Density: {graph_density(g1):.3f}")

   g2 = AdjacencyListGraph()
   # ... populate g2 ...
   print(f"Avg degree: {average_degree(g2):.2f}")

Implementing Directed Graphs
-----------------------------

Using AbstractDirectedGraph:

.. code-block:: python

   from sds.graph.interfaces import AbstractDirectedGraph
   from sds.graph import GraphNode, DirectedEdge
   from typing import Iterator

   class SimpleDirectedGraph(AbstractDirectedGraph):
       """Minimal directed graph implementation."""
       
       def __init__(self):
           super().__init__()
           self._nodes = {}
           self._edges = []
           self._out_adjacency = {}  # source -> targets
           self._in_adjacency = {}   # target -> sources
       
       # ... implement AbstractGraph methods ...
       # (add_node, remove_node, has_node, etc.)
       
       def in_degree(self, node: GraphNode) -> int:
           """Get number of incoming edges."""
           if not self.has_node(node):
               raise ValueError(f"Node {node.id} not in graph")
           return len(self._in_adjacency[node.id])
       
       def out_degree(self, node: GraphNode) -> int:
           """Get number of outgoing edges."""
           if not self.has_node(node):
               raise ValueError(f"Node {node.id} not in graph")
           return len(self._out_adjacency[node.id])
       
       def predecessors(self, node: GraphNode) -> Iterator[GraphNode]:
           """Get nodes with edges to this node."""
           if not self.has_node(node):
               raise ValueError(f"Node {node.id} not in graph")
           
           for predecessor_id in self._in_adjacency[node.id]:
               yield self._nodes[predecessor_id]
       
       def successors(self, node: GraphNode) -> Iterator[GraphNode]:
           """Get nodes with edges from this node."""
           if not self.has_node(node):
               raise ValueError(f"Node {node.id} not in graph")
           
           for successor_id in self._out_adjacency[node.id]:
               yield self._nodes[successor_id]
       
       def is_acyclic(self) -> bool:
           """Check if graph is a DAG (no cycles)."""
           # DFS with colors: 0=white, 1=gray, 2=black
           color = {node_id: 0 for node_id in self._nodes}
           
           def has_cycle(node_id):
               color[node_id] = 1  # gray (visiting)
               
               for successor_id in self._out_adjacency[node_id]:
                   if color[successor_id] == 1:  # back edge
                       return True
                   if color[successor_id] == 0:  # not visited
                       if has_cycle(successor_id):
                           return True
               
               color[node_id] = 2  # black (done)
               return False
           
           # Check all components
           for node_id in self._nodes:
               if color[node_id] == 0:
                   if has_cycle(node_id):
                       return False
           
           return True

Type-Safe Graph Algorithms
---------------------------

Using type hints with interfaces:

.. code-block:: python

   from sds.graph.interfaces import AbstractGraph, AbstractDirectedGraph
   from sds.graph import GraphNode
   from typing import Dict, List, Optional, TypeVar

   T = TypeVar('T')

   def breadth_first_search(
       graph: AbstractGraph,
       start: GraphNode,
       goal: GraphNode
   ) -> Optional[List[GraphNode]]:
       """Find shortest path using BFS."""
       if not graph.has_node(start) or not graph.has_node(goal):
           return None
       
       visited = {start}
       queue = [(start, [start])]
       
       while queue:
           current, path = queue.pop(0)
           
           if current == goal:
               return path
           
           for neighbor in graph.neighbors(current):
               if neighbor not in visited:
                   visited.add(neighbor)
                   queue.append((neighbor, path + [neighbor]))
       
       return None

   def topological_sort(
       graph: AbstractDirectedGraph
   ) -> Optional[List[GraphNode]]:
       """Return topological ordering if DAG, None otherwise."""
       if not graph.is_acyclic():
           return None
       
       in_degree = {
           node: graph.in_degree(node)
           for node in graph.nodes()
       }
       
       queue = [node for node, deg in in_degree.items() if deg == 0]
       result = []
       
       while queue:
           node = queue.pop(0)
           result.append(node)
           
           for successor in graph.successors(node):
               in_degree[successor] -= 1
               if in_degree[successor] == 0:
                   queue.append(successor)
       
       return result if len(result) == graph.node_count() else None

Interface Method Requirements
==============================

AbstractGraph Methods
---------------------

All concrete graph classes must implement:

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Method
     - Required
     - Purpose
   * - ``add_node(node)``
     - Yes
     - Add node to graph
   * - ``remove_node(node)``
     - Yes
     - Remove node and incident edges
   * - ``has_node(node)``
     - Yes
     - Check node existence
   * - ``add_edge(edge)``
     - Yes
     - Add edge between nodes
   * - ``remove_edge(edge)``
     - Yes
     - Remove specific edge
   * - ``has_edge(n1, n2)``
     - Yes
     - Check edge existence
   * - ``get_edge(n1, n2)``
     - Yes
     - Retrieve edge object
   * - ``neighbors(node)``
     - Yes
     - Iterate node's neighbors
   * - ``degree(node)``
     - Yes
     - Get node degree
   * - ``nodes()``
     - Yes
     - Iterate all nodes
   * - ``edges()``
     - Yes
     - Iterate all edges
   * - ``node_count()``
     - Yes
     - Number of nodes
   * - ``edge_count()``
     - Yes
     - Number of edges
   * - ``is_connected()``
     - Yes
     - Check connectivity
   * - ``get_node_by_id(id)``
     - Yes
     - Lookup by ID
   * - ``size``
     - No
     - Inherited property
   * - ``is_empty()``
     - No
     - Inherited method
   * - ``clear()``
     - Yes
     - Remove all elements

AbstractDirectedGraph Additional Methods
-----------------------------------------

Directed graph classes must additionally implement:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Method
     - Purpose
   * - ``in_degree(node)``
     - Count incoming edges
   * - ``out_degree(node)``
     - Count outgoing edges
   * - ``predecessors(node)``
     - Iterate nodes pointing to this node
   * - ``successors(node)``
     - Iterate nodes this node points to
   * - ``is_acyclic()``
     - Check if graph is a DAG

Design Patterns
===============

Template Method Pattern
-----------------------

Abstract classes define the template, concrete classes fill in specifics:

.. code-block:: python

   # Template methods in AbstractGraph
   def __len__(self) -> int:
       """Template - always uses _size."""
       return self._size
   
   def is_empty(self) -> bool:
       """Template - built on __len__."""
       return self._size == 0
   
   # Concrete classes implement specifics
   class Graph(AbstractGraph):
       def add_node(self, node):
           """Graph-specific implementation."""
           # ... custom logic ...
           self._size += 1  # Template expects this

Strategy Pattern
----------------

Different implementations for different use cases:

.. code-block:: python

   from enum import Enum

   class GraphRepresentation(Enum):
       ADJACENCY_LIST = "list"
       ADJACENCY_MATRIX = "matrix"
       EDGE_LIST = "edges"

   def create_graph(representation: GraphRepresentation) -> AbstractGraph:
       """Factory for different graph representations."""
       strategies = {
           GraphRepresentation.ADJACENCY_LIST: AdjacencyListGraph,
           GraphRepresentation.ADJACENCY_MATRIX: AdjacencyMatrixGraph,
           GraphRepresentation.EDGE_LIST: Graph
       }
       return strategies[representation]()

   # Usage
   sparse_graph = create_graph(GraphRepresentation.ADJACENCY_LIST)
   dense_graph = create_graph(GraphRepresentation.ADJACENCY_MATRIX)

Visitor Pattern
---------------

Traverse graphs uniformly:

.. code-block:: python

   from abc import ABC, abstractmethod

   class GraphVisitor(ABC):
       """Abstract visitor for graph elements."""
       
       @abstractmethod
       def visit_node(self, node: GraphNode):
           pass
       
       @abstractmethod
       def visit_edge(self, edge: Edge):
           pass

   class PrintVisitor(GraphVisitor):
       """Visitor that prints graph elements."""
       
       def visit_node(self, node):
           print(f"Node: {node.data}")
       
       def visit_edge(self, edge):
           print(f"Edge: {edge.node1.data} -- {edge.node2.data}")

   def traverse_graph(graph: AbstractGraph, visitor: GraphVisitor):
       """Apply visitor to all graph elements."""
       for node in graph.nodes():
           visitor.visit_node(node)
       for edge in graph.edges():
           visitor.visit_edge(edge)

Best Practices
==============

Interface Implementation
------------------------

✅ **Always call super().__init__()**

.. code-block:: python

   class MyGraph(AbstractGraph):
       def __init__(self):
           super().__init__()  # Initialize _size
           # Your initialization here

✅ **Update _size consistently**

.. code-block:: python

   def add_node(self, node):
       # ... add node logic ...
       self._size += 1  # Don't forget!
   
   def remove_node(self, node):
       # ... remove node logic ...
       self._size -= 1

✅ **Implement all abstract methods**

.. code-block:: python

   # Type checkers will catch missing methods
   class IncompleteGraph(AbstractGraph):
       # Missing: add_node, add_edge, etc.
       pass  # Type error!

Using Interfaces
----------------

✅ **Program to interfaces, not implementations**

.. code-block:: python

   # Good: Flexible, works with any graph
   def analyze_graph(graph: AbstractGraph):
       return {
           'nodes': graph.node_count(),
           'edges': graph.edge_count(),
           'density': graph_density(graph)
       }
   
   # Less flexible: Tied to specific type
   def analyze_specific(graph: Graph):
       # Only works with Graph class
       pass

✅ **Use type hints for clarity**

.. code-block:: python

   from typing import List, Optional

   def find_path(
       graph: AbstractGraph,
       start: GraphNode,
       goal: GraphNode
   ) -> Optional[List[GraphNode]]:
       """Type-safe path finding."""
       # Implementation...

Common Patterns
===============

Graph Metrics
-------------

.. code-block:: python

   def graph_metrics(graph: AbstractGraph) -> dict:
       """Calculate common graph metrics."""
       n = graph.node_count()
       m = graph.edge_count()
       
       if n == 0:
           return {'nodes': 0, 'edges': 0}
       
       degrees = [graph.degree(node) for node in graph.nodes()]
       
       return {
           'nodes': n,
           'edges': m,
           'avg_degree': sum(degrees) / n,
           'max_degree': max(degrees) if degrees else 0,
           'min_degree': min(degrees) if degrees else 0,
           'density': (2 * m) / (n * (n - 1)) if n > 1 else 0
       }

Graph Transformation
--------------------

.. code-block:: python

   def complement_graph(graph: AbstractGraph) -> AbstractGraph:
       """Create complement graph."""
       complement = type(graph)()  # Same type
       
       # Add all nodes
       for node in graph.nodes():
           complement.add_node(node)
       
       # Add edges that don't exist in original
       nodes_list = list(graph.nodes())
       for i, node1 in enumerate(nodes_list):
           for node2 in nodes_list[i+1:]:
               if not graph.has_edge(node1, node2):
                   complement.add_edge(Edge(node1, node2))
       
       return complement

See Also
========

* :doc:`node` - GraphNode implementation
* :doc:`edge` - Edge implementations
* :doc:`graph` - Concrete graph classes
* :doc:`directed` - Directed graph implementations
* :doc:`../../guide/graph_structures/index` - Graph structures guide

References
==========

.. [1] Gamma, E., et al. "Design Patterns: Elements of Reusable Object-Oriented Software", 1994
.. [2] Martin, R. C. "Clean Architecture", Chapter 11: DIP
.. [3] Liskov, B. "Data Abstraction and Hierarchy", OOPSLA '87
.. [4] Cormen, T. H., et al. "Introduction to Algorithms", 3rd Edition, Part VI
