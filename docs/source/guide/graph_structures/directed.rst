.. _guide_graph_directed:

====================
Directed Graph Guide
====================

.. currentmodule:: sds.graphs

Introduction
============

A **directed graph** (or digraph) is a graph where edges have a direction, flowing from a source
vertex to a target vertex. Unlike undirected graphs where relationships are symmetric, directed
graphs model asymmetric relationships such as web page links, task dependencies, and social media
followers.

.. mermaid::

   graph LR
       subgraph "Directed Graph (Digraph)"
       A[A] --> B[B]
       A --> C[C]
       B --> D[D]
       C --> D
       D --> A
       end
       
       subgraph "DAG (Directed Acyclic)"
       E[Task 1] --> F[Task 2]
       E --> G[Task 3]
       F --> H[Task 4]
       G --> H
       end
       
       style A fill:#e74c3c,color:#fff
       style E fill:#3498db,color:#fff

.. note::
   
   Directed graphs are essential for modeling flows, dependencies, and hierarchies.
   Understanding directed graphs is crucial for tasks like scheduling, compilation,
   and analyzing causal relationships.

Mathematical Model
==================

Formal Definition
-----------------

Directed Graph
^^^^^^^^^^^^^^

A directed graph :math:`G` is defined as:

.. math::

   G = (V, E)

where:
   * :math:`V` is the **set of vertices**
   * :math:`E \subseteq V \times V` is the **set of directed edges**

Each edge :math:`(u, v) \in E` has:
   * :math:`u` as the **source** (tail)
   * :math:`v` as the **target** (head)

**Important**: :math:`(u, v) \neq (v, u)` - direction matters!

**Example**: :math:`G = (\{A, B, C\}, \{(A,B), (B,C), (A,C)\})`

Directed Edge Properties
^^^^^^^^^^^^^^^^^^^^^^^^^

For an edge :math:`e = (u, v)`:

.. math::

   \begin{aligned}
   \text{source}(e) &= u \\
   \text{target}(e) &= v \\
   \text{reverse}(e) &= (v, u)
   \end{aligned}

An edge :math:`(u, v)` is an **outgoing edge** from :math:`u` and an **incoming edge** to :math:`v`.

Degree in Directed Graphs
--------------------------

In-Degree and Out-Degree
^^^^^^^^^^^^^^^^^^^^^^^^^

**Out-degree** of vertex :math:`v`:

.. math::

   deg^{out}(v) = |\{u \in V : (v, u) \in E\}|

Number of edges **leaving** :math:`v`.

**In-degree** of vertex :math:`v`:

.. math::

   deg^{in}(v) = |\{u \in V : (u, v) \in E\}|

Number of edges **entering** :math:`v`.

**Total degree**:

.. math::

   deg(v) = deg^{in}(v) + deg^{out}(v)

Degree Sum Properties
^^^^^^^^^^^^^^^^^^^^^

**Out-degree sum**:

.. math::

   \sum_{v \in V} deg^{out}(v) = |E|

**In-degree sum**:

.. math::

   \sum_{v \in V} deg^{in}(v) = |E|

**Total degree sum**:

.. math::

   \sum_{v \in V} deg(v) = 2|E|

Paths in Directed Graphs
-------------------------

Directed Path
^^^^^^^^^^^^^

A **directed path** from :math:`u` to :math:`v` is a sequence:

.. math::

   P = (v_0, v_1, \ldots, v_k) \text{ where } (v_i, v_{i+1}) \in E \text{ for all } i

:math:`v_0 = u` is the start, :math:`v_k = v` is the end.

**Path length**: :math:`k` (number of edges)

Reachability
^^^^^^^^^^^^

Vertex :math:`v` is **reachable** from :math:`u` if there exists a directed path from :math:`u` to :math:`v`:

.. math::

   v \text{ reachable from } u \iff \exists \text{ directed path } u \rightsquigarrow v

Cycles in Directed Graphs
--------------------------

Directed Cycle
^^^^^^^^^^^^^^

A **directed cycle** is a path :math:`C = (v_0, v_1, \ldots, v_k)` where:

.. math::

   v_0 = v_k \text{ and } k \geq 1

**Simple cycle**: All vertices except :math:`v_0 = v_k` are distinct.

Directed Acyclic Graph (DAG)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A **DAG** is a directed graph with **no directed cycles**:

.. math::

   \text{DAG} \iff \nexists \text{ directed cycle in } G

**Key property**: DAGs can be **topologically sorted**.

Topological Ordering
^^^^^^^^^^^^^^^^^^^^

A **topological ordering** of a DAG :math:`G = (V, E)` is a linear ordering of vertices:

.. math::

   v_1, v_2, \ldots, v_n

such that:

.. math::

   (v_i, v_j) \in E \implies i < j

Every DAG has at least one topological ordering.

Connectivity in Directed Graphs
--------------------------------

Strong Connectivity
^^^^^^^^^^^^^^^^^^^

Graph :math:`G` is **strongly connected** if:

.. math::

   \forall u, v \in V: u \rightsquigarrow v \text{ and } v \rightsquigarrow u

Every vertex can reach every other vertex via directed paths.

Weak Connectivity
^^^^^^^^^^^^^^^^^

Graph :math:`G` is **weakly connected** if the **underlying undirected graph** is connected.

Treat :math:`(u, v)` as :math:`\{u, v\}` and check connectivity.

Strongly Connected Components
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A **strongly connected component (SCC)** is a maximal set of vertices :math:`C \subseteq V` where:

.. math::

   \forall u, v \in C: u \rightsquigarrow v \text{ and } v \rightsquigarrow u

**Component graph**: Graph of SCCs, always a DAG.

Graph Types and Properties
---------------------------

Special Directed Graphs
^^^^^^^^^^^^^^^^^^^^^^^

**Tournament**: Complete directed graph (every pair connected)

.. math::

   \forall u, v \in V: (u,v) \in E \text{ or } (v,u) \in E

**Directed Tree**: Connected DAG with one root where every vertex (except root) has in-degree 1.

**Functional Graph**: Every vertex has out-degree exactly 1.

Graph Invariants
^^^^^^^^^^^^^^^^

1. **Edge count**: :math:`0 \leq |E| \leq |V|(|V|-1)`

2. **Degree balance**: :math:`\sum deg^{in} = \sum deg^{out} = |E|`

3. **DAG height**: Longest path in DAG is :math:`O(|V|)`

4. **Reachability transitivity**: If :math:`u \rightsquigarrow v` and :math:`v \rightsquigarrow w`, then :math:`u \rightsquigarrow w`

Algorithmic Model
=================

Abstract Data Type
------------------

.. code-block:: text

   ADT DirectedGraph:
       Data:
           - vertices: set V
           - edges: set E ⊆ V × V
           - in_adj: V → set of predecessors
           - out_adj: V → set of successors
       
       DirectedEdge:
           - source: source vertex
           - target: target vertex
           - data: optional edge data
       
       Operations:
           - DirectedGraph(): create empty digraph
           - add_vertex(v): add vertex
           - add_edge(u, v): add directed edge u → v
           - in_degree(v): count incoming edges
           - out_degree(v): count outgoing edges
           - predecessors(v): vertices with edges to v
           - successors(v): vertices with edges from v
           - is_acyclic(): check if DAG
           - topological_sort(): order vertices (DAG only)
       
       Invariants:
           - (u,v) ∈ E ⟹ u,v ∈ V
           - in_degree(v) = |predecessors(v)|
           - out_degree(v) = |successors(v)|

Core Algorithms
---------------

Cycle Detection (DFS with Colors)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Detect cycles using three colors:
- **White**: Unvisited
- **Gray**: Visiting (in current path)
- **Black**: Visited (complete)

.. code-block:: text

   Algorithm: HAS_CYCLE_DIRECTED(G)
   Input: Directed graph G = (V, E)
   Output: true if cycle exists
   
   1. color ← {v: WHITE for v in V}
   2. 
   3. for each v in V do
   4.     if color[v] = WHITE then
   5.         if DFS_CYCLE(v, color) then
   6.             return true
   7.         end if
   8.     end if
   9. end for
   10. return false
   
   Algorithm: DFS_CYCLE(v, color)
   1. color[v] ← GRAY  // Mark as visiting
   2. 
   3. for each u in successors(v) do
   4.     if color[u] = GRAY then
   5.         return true  // Back edge = cycle!
   6.     end if
   7.     if color[u] = WHITE then
   8.         if DFS_CYCLE(u, color) then
   9.             return true
   10.        end if
   11.    end if
   12. end for
   13. 
   14. color[v] ← BLACK  // Mark as complete
   15. return false

**Time Complexity**: :math:`O(|V| + |E|)`
**Space Complexity**: :math:`O(|V|)` for color map

**Key Insight**: Gray vertex in recursion stack indicates back edge → cycle.

Topological Sort (DFS)
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   Algorithm: TOPOLOGICAL_SORT(G)
   Input: DAG G = (V, E)
   Output: Linear ordering of vertices
   
   1. if not IS_ACYCLIC(G) then
   2.     error "Graph has cycles"
   3. end if
   4. 
   5. visited ← ∅
   6. result ← []
   7. 
   8. for each v in V do
   9.     if v not in visited then
   10.        DFS_TOPOLOGICAL(v, visited, result)
   11.    end if
   12. end for
   13. 
   14. return reverse(result)
   
   Algorithm: DFS_TOPOLOGICAL(v, visited, result)
   1. visited.add(v)
   2. 
   3. for each u in successors(v) do
   4.     if u not in visited then
   5.         DFS_TOPOLOGICAL(u, visited, result)
   6.     end if
   7. end for
   8. 
   9. result.append(v)  // Add after visiting successors

**Time Complexity**: :math:`O(|V| + |E|)`

**Alternative (Kahn's Algorithm)**:

.. code-block:: text

   Algorithm: TOPOLOGICAL_SORT_KAHN(G)
   1. in_degree ← {v: in_degree(v) for v in V}
   2. queue ← [v for v in V if in_degree[v] = 0]
   3. result ← []
   4. 
   5. while queue not empty do
   6.     v ← queue.dequeue()
   7.     result.append(v)
   8.     
   9.     for each u in successors(v) do
   10.        in_degree[u] ← in_degree[u] - 1
   11.        if in_degree[u] = 0 then
   12.            queue.enqueue(u)
   13.        end if
   14.    end for
   15. end while
   16. 
   17. if |result| ≠ |V| then
   18.    error "Graph has cycles"
   19. end if
   20. return result

**Time Complexity**: :math:`O(|V| + |E|)`

Strongly Connected Components (Kosaraju)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   Algorithm: KOSARAJU_SCC(G)
   Input: Directed graph G
   Output: List of strongly connected components
   
   1. // Phase 1: Compute finish times
   2. visited ← ∅
   3. finish_order ← []
   4. 
   5. for each v in V do
   6.     if v not in visited then
   7.         DFS_FINISH(v, visited, finish_order)
   8.     end if
   9. end for
   10. 
   11. // Phase 2: Process vertices in reverse finish order on G^T
   12. G_transpose ← TRANSPOSE(G)
   13. visited ← ∅
   14. components ← []
   15. 
   16. for each v in reverse(finish_order) do
   17.    if v not in visited then
   18.        component ← []
   19.        DFS_COLLECT(G_transpose, v, visited, component)
   20.        components.append(component)
   21.    end if
   22. end for
   23. 
   24. return components

**Time Complexity**: :math:`O(|V| + |E|)`

Reachability
^^^^^^^^^^^^

.. code-block:: text

   Algorithm: IS_REACHABLE(G, u, v)
   Input: Graph G, source u, target v
   Output: true if v reachable from u
   
   1. visited ← {u}
   2. queue ← [u]
   3. 
   4. while queue not empty do
   5.     current ← queue.dequeue()
   6.     
   7.     if current = v then
   8.         return true
   9.     end if
   10.    
   11.    for each w in successors(current) do
   12.        if w not in visited then
   13.            visited.add(w)
   14.            queue.enqueue(w)
   15.        end if
   16.    end for
   17. end while
   18. 
   19. return false

**Time Complexity**: :math:`O(|V| + |E|)`

Complexity Analysis
-------------------

Time Complexity Summary
^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 35 25 40

   * - Operation
     - Complexity
     - Notes
   * - **Add edge**
     - O(1)
     - Adjacency list update
   * - **In-degree**
     - O(1)
     - Cached in in-adjacency
   * - **Out-degree**
     - O(1)
     - Cached in out-adjacency
   * - **Predecessors**
     - O(in-degree)
     - Iterate in-adjacency
   * - **Successors**
     - O(out-degree)
     - Iterate out-adjacency
   * - **Is cyclic**
     - O(V + E)
     - DFS with colors
   * - **Topological sort**
     - O(V + E)
     - DFS or Kahn's
   * - **SCCs**
     - O(V + E)
     - Kosaraju or Tarjan
   * - **Reachability**
     - O(V + E)
     - BFS/DFS

Space Complexity
^^^^^^^^^^^^^^^^

* **Adjacency lists**: :math:`O(|V| + |E|)` (in + out)
* **DFS recursion**: :math:`O(|V|)` stack depth
* **Transitive closure**: :math:`O(|V|^2)` for all-pairs reachability

Practical Usage
===============

Installation and Import
-----------------------

.. code-block:: python

   # Install
   pip install sds-tools
   
   # Import
   from sds.graphs import DirectedGraph, GraphNode, DirectedEdge

Basic Operations
----------------

Creating a Directed Graph
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.graphs import DirectedGraph

   # Create empty directed graph
   g = DirectedGraph()
   
   # Create multigraph
   mg = DirectedGraph(allow_multi_edges=True)

Adding Vertices and Edges
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.graphs import GraphNode, DirectedEdge

   # Create vertices
   a = GraphNode("A", "n1")
   b = GraphNode("B", "n2")
   c = GraphNode("C", "n3")
   
   g.add_node(a)
   g.add_node(b)
   g.add_node(c)
   
   # Add directed edges (A→B, B→C, A→C)
   g.add_edge(DirectedEdge(a, b))
   g.add_edge(DirectedEdge(b, c))
   g.add_edge(DirectedEdge(a, c))
   
   # Check edges - direction matters!
   print(g.has_edge(a, b))  # True
   print(g.has_edge(b, a))  # False

Querying Degrees
^^^^^^^^^^^^^^^^

.. code-block:: python

   # Out-degree: edges FROM vertex
   print(f"Out-degree of A: {g.out_degree(a)}")  # 2
   
   # In-degree: edges TO vertex
   print(f"In-degree of C: {g.in_degree(c)}")    # 2
   
   # Total degree
   print(f"Total degree of B: {g.degree(b)}")    # 2

Predecessors and Successors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Successors: vertices reachable via outgoing edges
   succ = list(g.successors(a))
   print(f"Successors of A: {[n.data for n in succ]}")  # ['B', 'C']
   
   # Predecessors: vertices with edges TO this vertex
   pred = list(g.predecessors(c))
   print(f"Predecessors of C: {[n.data for n in pred]}")  # ['A', 'B']

Cycle Detection
^^^^^^^^^^^^^^^

.. code-block:: python

   # Check if graph is acyclic (DAG)
   print(f"Is DAG: {g.is_acyclic()}")  # True
   
   # Add edge to create cycle
   g.add_edge(DirectedEdge(c, a))
   print(f"Is DAG: {g.is_acyclic()}")  # False

Real-World Applications
=======================

Application 1: Task Scheduler (DAG)
------------------------------------

Complete task scheduling system:

.. code-block:: python

   from sds.graphs import DirectedGraph, GraphNode, DirectedEdge

   class TaskScheduler:
       """Schedule tasks with dependencies using DAG."""
       
       def __init__(self):
           self.graph = DirectedGraph()
           self.tasks = {}
       
       def add_task(self, task_id, name, duration, resources=None):
           """Add a task."""
           data = {
               'name': name,
               'duration': duration,
               'resources': resources or []
           }
           node = GraphNode(data, task_id)
           self.graph.add_node(node)
           self.tasks[task_id] = node
       
       def add_dependency(self, task_id, depends_on_id):
           """Task depends on another (depends_on must finish first)."""
           task = self.tasks[task_id]
           prerequisite = self.tasks[depends_on_id]
           # Edge from prerequisite to dependent task
           self.graph.add_edge(DirectedEdge(prerequisite, task))
       
       def validate(self):
           """Check if schedule is valid (no cycles)."""
           return self.graph.is_acyclic()
       
       def get_execution_order(self):
           """Get valid task execution order (topological sort)."""
           if not self.validate():
               raise ValueError("Cannot schedule: circular dependencies")
           
           # Topological sort using Kahn's algorithm
           in_degree = {
               tid: self.graph.in_degree(self.tasks[tid])
               for tid in self.tasks
           }
           
           queue = [tid for tid, deg in in_degree.items() if deg == 0]
           order = []
           
           while queue:
               task_id = queue.pop(0)
               order.append(task_id)
               
               task = self.tasks[task_id]
               for successor in self.graph.successors(task):
                   in_degree[successor.id] -= 1
                   if in_degree[successor.id] == 0:
                       queue.append(successor.id)
           
           if len(order) != len(self.tasks):
               raise ValueError("Cycle detected during sort")
           
           return order
       
       def critical_path(self):
           """Calculate critical path (longest path in DAG)."""
           order = self.get_execution_order()
           
           # Calculate earliest start times
           earliest = {tid: 0 for tid in self.tasks}
           
           for task_id in order:
               task = self.tasks[task_id]
               duration = task.data['duration']
               
               for successor in self.graph.successors(task):
                   earliest[successor.id] = max(
                       earliest[successor.id],
                       earliest[task_id] + duration
                   )
           
           # Find critical path
           max_time = max(earliest.values())
           critical_tasks = []
           
           # Backtrack from tasks with max earliest time
           def backtrack(task_id, time):
               if time == 0:
                   return [[task_id]]
               
               paths = []
               task = self.tasks[task_id]
               for predecessor in self.graph.predecessors(task):
                   pred_time = earliest[predecessor.id]
                   pred_duration = predecessor.data['duration']
                   
                   if pred_time + pred_duration == time:
                       for path in backtrack(predecessor.id, pred_time):
                           paths.append(path + [task_id])
               
               return paths
           
           # Find all critical paths
           end_tasks = [tid for tid in order 
                       if earliest[tid] == max_time - self.tasks[tid].data['duration']]
           
           all_paths = []
           for end_task in end_tasks:
               all_paths.extend(backtrack(end_task, earliest[end_task]))
           
           return max_time, all_paths
       
       def get_prerequisites(self, task_id):
           """Get immediate prerequisites."""
           task = self.tasks[task_id]
           return [n.id for n in self.graph.predecessors(task)]
       
       def get_dependent_tasks(self, task_id):
           """Get tasks that depend on this one."""
           task = self.tasks[task_id]
           return [n.id for n in self.graph.successors(task)]
   
   # Usage
   scheduler = TaskScheduler()
   
   # Add tasks
   scheduler.add_task("design", "Design System", 5)
   scheduler.add_task("frontend", "Frontend Dev", 8)
   scheduler.add_task("backend", "Backend Dev", 10)
   scheduler.add_task("database", "Database Setup", 3)
   scheduler.add_task("testing", "Integration Test", 5)
   scheduler.add_task("deploy", "Deploy", 2)
   
   # Add dependencies
   scheduler.add_dependency("frontend", "design")
   scheduler.add_dependency("backend", "design")
   scheduler.add_dependency("backend", "database")
   scheduler.add_dependency("testing", "frontend")
   scheduler.add_dependency("testing", "backend")
   scheduler.add_dependency("deploy", "testing")
   
   # Get execution order
   if scheduler.validate():
       order = scheduler.get_execution_order()
       print(f"Execution order: {order}")
       
       # Critical path
       duration, paths = scheduler.critical_path()
       print(f"Project duration: {duration} days")
       print(f"Critical path: {paths[0]}")

Application 2: Citation Network
--------------------------------

Academic paper citations:

.. code-block:: python

   from sds.graphs import DirectedGraph, GraphNode, DirectedEdge

   class CitationNetwork:
       """Track academic paper citations."""
       
       def __init__(self):
           self.graph = DirectedGraph()
           self.papers = {}
       
       def add_paper(self, paper_id, title, year, authors):
           """Add a paper to the network."""
           data = {
               'title': title,
               'year': year,
               'authors': authors
           }
           node = GraphNode(data, paper_id)
           self.graph.add_node(node)
           self.papers[paper_id] = node
       
       def add_citation(self, citing_id, cited_id):
           """Add citation (citing paper → cited paper)."""
           citing = self.papers[citing_id]
           cited = self.papers[cited_id]
           # Edge from citing to cited
           self.graph.add_edge(DirectedEdge(citing, cited))
       
       def citation_count(self, paper_id):
           """Get number of times paper was cited (in-degree)."""
           paper = self.papers[paper_id]
           return self.graph.in_degree(paper)
       
       def references_count(self, paper_id):
           """Get number of papers cited by this paper (out-degree)."""
           paper = self.papers[paper_id]
           return self.graph.out_degree(paper)
       
       def get_references(self, paper_id):
           """Get papers cited by this paper."""
           paper = self.papers[paper_id]
           refs = list(self.graph.successors(paper))
           return [(r.id, r.data['title']) for r in refs]
       
       def get_citing_papers(self, paper_id):
           """Get papers that cite this paper."""
           paper = self.papers[paper_id]
           citing = list(self.graph.predecessors(paper))
           return [(c.id, c.data['title']) for c in citing]
       
       def h_index_simple(self, author):
           """Calculate simplified h-index for author."""
           # Find all papers by author
           author_papers = [
               pid for pid, paper in self.papers.items()
               if author in paper.data['authors']
           ]
           
           # Get citation counts
           citations = [
               self.citation_count(pid) for pid in author_papers
           ]
           citations.sort(reverse=True)
           
           # Calculate h-index
           h = 0
           for i, cites in enumerate(citations, 1):
               if cites >= i:
                   h = i
               else:
                   break
           
           return h
       
       def find_influential_papers(self, min_citations=10):
           """Find highly cited papers."""
           influential = []
           
           for paper_id, paper in self.papers.items():
               citations = self.citation_count(paper_id)
               if citations >= min_citations:
                   influential.append((paper_id, paper.data['title'], citations))
           
           influential.sort(key=lambda x: x[2], reverse=True)
           return influential
   
   # Usage
   citations = CitationNetwork()
   
   # Add papers
   citations.add_paper("p1", "Graph Theory Fundamentals", 2015, ["Smith"])
   citations.add_paper("p2", "Applications of Directed Graphs", 2016, ["Jones"])
   citations.add_paper("p3", "Advanced Graph Algorithms", 2017, ["Smith", "Brown"])
   citations.add_paper("p4", "Network Analysis", 2018, ["Johnson"])
   citations.add_paper("p5", "Social Network Models", 2019, ["Brown"])
   
   # Add citations
   citations.add_citation("p2", "p1")
   citations.add_citation("p3", "p1")
   citations.add_citation("p3", "p2")
   citations.add_citation("p4", "p1")
   citations.add_citation("p4", "p3")
   citations.add_citation("p5", "p3")
   
   # Query
   print(f"P1 cited by: {citations.citation_count('p1')} papers")
   print(f"P3 cites: {citations.references_count('p3')} papers")
   print(f"Smith's h-index: {citations.h_index_simple('Smith')}")

Application 3: Course Prerequisites
------------------------------------

University course dependencies:

.. code-block:: python

   from sds.graphs import DirectedGraph, GraphNode, DirectedEdge

   class CoursePlanner:
       """Plan course sequences with prerequisites."""
       
       def __init__(self):
           self.graph = DirectedGraph()
           self.courses = {}
       
       def add_course(self, course_id, name, credits, semester_offered):
           """Add a course."""
           data = {
               'name': name,
               'credits': credits,
               'semesters': semester_offered
           }
           node = GraphNode(data, course_id)
           self.graph.add_node(node)
           self.courses[course_id] = node
       
       def add_prerequisite(self, course_id, prereq_id):
           """Add prerequisite (prereq must be completed first)."""
           course = self.courses[course_id]
           prereq = self.courses[prereq_id]
           # Edge from prerequisite to course
           self.graph.add_edge(DirectedEdge(prereq, course))
       
       def can_graduate(self):
           """Check if degree requirements form valid sequence (no cycles)."""
           return self.graph.is_acyclic()
       
       def get_prerequisites(self, course_id):
           """Get immediate prerequisites."""
           course = self.courses[course_id]
           prereqs = list(self.graph.predecessors(course))
           return [(p.id, p.data['name']) for p in prereqs]
       
       def get_all_prerequisites(self, course_id):
           """Get all prerequisites (transitive)."""
           all_prereqs = set()
           visited = set()
           
           def collect_prereqs(cid):
               if cid in visited:
                   return
               visited.add(cid)
               
               for prereq in self.graph.predecessors(self.courses[cid]):
                   all_prereqs.add(prereq.id)
                   collect_prereqs(prereq.id)
           
           collect_prereqs(course_id)
           return list(all_prereqs)
       
       def plan_semesters(self, max_credits=15):
           """Plan course sequence over semesters."""
           if not self.can_graduate():
               raise ValueError("Circular prerequisites detected")
           
           # Get topological order
           order = self._topological_sort()
           
           # Distribute across semesters
           semesters = []
           current_semester = []
           current_credits = 0
           
           for course_id in order:
               course = self.courses[course_id]
               credits = course.data['credits']
               
               if current_credits + credits <= max_credits:
                   current_semester.append(course_id)
                   current_credits += credits
               else:
                   semesters.append(current_semester)
                   current_semester = [course_id]
                   current_credits = credits
           
           if current_semester:
               semesters.append(current_semester)
           
           return semesters
       
       def _topological_sort(self):
           """Topological sort using Kahn's algorithm."""
           in_degree = {
               cid: self.graph.in_degree(self.courses[cid])
               for cid in self.courses
           }
           
           queue = [cid for cid, deg in in_degree.items() if deg == 0]
           result = []
           
           while queue:
               course_id = queue.pop(0)
               result.append(course_id)
               
               course = self.courses[course_id]
               for successor in self.graph.successors(course):
                   in_degree[successor.id] -= 1
                   if in_degree[successor.id] == 0:
                       queue.append(successor.id)
           
           return result
   
   # Usage
   planner = CoursePlanner()
   
   # Add courses
   planner.add_course("CS101", "Intro to Programming", 3, ["Fall", "Spring"])
   planner.add_course("CS102", "Data Structures", 3, ["Fall", "Spring"])
   planner.add_course("CS201", "Algorithms", 3, ["Fall"])
   planner.add_course("CS202", "Computer Architecture", 3, ["Spring"])
   planner.add_course("MATH101", "Calculus I", 4, ["Fall", "Spring"])
   planner.add_course("MATH201", "Discrete Math", 3, ["Fall", "Spring"])
   
   # Add prerequisites
   planner.add_prerequisite("CS102", "CS101")
   planner.add_prerequisite("CS201", "CS102")
   planner.add_prerequisite("CS201", "MATH201")
   planner.add_prerequisite("CS202", "CS102")
   planner.add_prerequisite("MATH201", "MATH101")
   
   # Plan
   if planner.can_graduate():
       plan = planner.plan_semesters(max_credits=15)
       print(f"Degree plan: {len(plan)} semesters")
       for i, semester in enumerate(plan, 1):
           print(f"Semester {i}: {semester}")

Best Practices
==============

Do's
----

✅ **Use for asymmetric relationships**

.. code-block:: python

   # Good: One-way relationships
   followers = DirectedGraph()
   citations = DirectedGraph()
   task_deps = DirectedGraph()

✅ **Validate DAGs before topological sort**

.. code-block:: python

   if not dag.is_acyclic():
       raise ValueError("Cannot sort: contains cycles")
   order = topological_sort(dag)

✅ **Use appropriate degree measure**

.. code-block:: python

   # In-degree: popularity, dependencies satisfied
   popularity = graph.in_degree(node)
   
   # Out-degree: influence, dependencies required
   dependencies = graph.out_degree(node)

Don'ts
------

❌ **Don't confuse edge direction**

.. code-block:: python

   # Wrong: Backwards dependency
   scheduler.add_dependency(prerequisite, task)
   
   # Right: Task depends on prerequisite
   scheduler.add_dependency(task, prerequisite)

❌ **Don't assume symmetry**

.. code-block:: python

   # Just because A→B exists doesn't mean B→A exists
   if g.has_edge(a, b):
       # DON'T assume g.has_edge(b, a)
       pass

Further Reading
===============

* :doc:`general` - Undirected graphs
* :doc:`weighted` - Weighted directed graphs
* :doc:`/api/graph/directed` - Complete API reference

References
==========

.. [BangJensen] Bang-Jensen, J., Gutin, G. "Digraphs: Theory, Algorithms and Applications", Springer, 2008.
   https://link.springer.com/book/10.1007/978-1-84800-998-1
   
   Comprehensive treatment of directed graph theory. Many chapters available through academic access.

.. [WikiDAG] Wikipedia contributors. "Directed acyclic graph". Wikipedia.
   https://en.wikipedia.org/wiki/Directed_acyclic_graph
   
   Overview of DAGs and their applications.

.. [CLRS] Cormen, T. H., et al. "Introduction to Algorithms", 3rd Edition, Chapter 22.
   https://mitpress.mit.edu/9780262046305/
   
   Standard algorithms textbook covering graph algorithms.

.. [Sedgewick] Sedgewick, R., Wayne, K. "Algorithms", 4th Edition, Section 4.2.
   https://algs4.cs.princeton.edu/42digraph/
   
   Free online content on directed graphs and algorithms.

.. [WikiTopSort] Wikipedia contributors. "Topological sorting". Wikipedia.
   https://en.wikipedia.org/wiki/Topological_sorting
   
   Detailed explanation of topological sorting algorithms.

.. [WikiSCC] Wikipedia contributors. "Strongly connected component". Wikipedia.
   https://en.wikipedia.org/wiki/Strongly_connected_component
   
   Comprehensive overview of SCCs and algorithms.

.. [Algorithms] Erickson, J. "Algorithms".
   http://jeffe.cs.illinois.edu/teaching/algorithms/
   
   Free algorithms textbook with excellent graph coverage.
