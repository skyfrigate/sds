.. _guide_tree_general:

==================
General Tree Guide
==================

.. currentmodule:: sds.tree

Introduction
============

A **general tree** (or n-ary tree) is a hierarchical data structure where each node can have
an arbitrary number of children. Unlike binary trees that restrict each node to at most two
children, general trees offer maximum flexibility for representing hierarchical relationships.

.. mermaid::

   graph TB
       A[Root] --> B[Child 1]
       A --> C[Child 2]
       A --> D[Child 3]
       A --> E[Child 4]
       
       B --> F[Grandchild 1]
       B --> G[Grandchild 2]
       
       C --> H[Grandchild 3]
       C --> I[Grandchild 4]
       C --> J[Grandchild 5]
       
       style A fill:#e74c3c,stroke:#c0392b,color:#fff
       style B fill:#3498db
       style C fill:#3498db
       style F fill:#2ecc71
       style H fill:#2ecc71

.. note::
   
   General trees are ideal for representing organizational charts, file systems,
   XML/HTML documents, and any data with variable branching.

Mathematical Model
==================

Formal Definition
-----------------

A general tree :math:`T` is defined recursively as:

.. math::

   T = (r, \{T_1, T_2, \ldots, T_k\})

where:
   * :math:`r` is the **root** node
   * :math:`T_1, T_2, \ldots, T_k` are **subtrees** (which are also trees)
   * :math:`k \geq 0` is the **degree** of the root (number of children)

Special cases:
   * If :math:`k = 0`, the tree is a single node (leaf)
   * Empty tree: :math:`T = \emptyset`

Tree Properties
---------------

Nodes and Relationships
^^^^^^^^^^^^^^^^^^^^^^^^

For a tree :math:`T` with node set :math:`N`:

**Parent-Child Relationship:**

.. math::

   \text{parent}: N \setminus \{root\} \rightarrow N

Every node except the root has exactly one parent.

**Children Relationship:**

.. math::

   \text{children}: N \rightarrow \mathcal{P}(N)

where :math:`\mathcal{P}(N)` is the power set of :math:`N`.

**Degree of a Node:**

.. math::

   degree(v) = |\text{children}(v)|

The degree of a node is the number of its children.

**Degree of a Tree:**

.. math::

   degree(T) = \max_{v \in N} degree(v)

Height and Depth
^^^^^^^^^^^^^^^^

**Depth of a node** :math:`v`:

.. math::

   depth(v) = \begin{cases}
   0 & \text{if } v = root \\
   depth(\text{parent}(v)) + 1 & \text{otherwise}
   \end{cases}

**Height of a node** :math:`v`:

.. math::

   height(v) = \begin{cases}
   0 & \text{if } v \text{ is a leaf} \\
   1 + \max_{c \in children(v)} height(c) & \text{otherwise}
   \end{cases}

**Height of the tree:**

.. math::

   height(T) = height(root)

Tree Size
^^^^^^^^^

**Number of nodes:**

.. math::

   |T| = 1 + \sum_{i=1}^{k} |T_i|

**Number of leaves:**

.. math::

   leaves(T) = \begin{cases}
   1 & \text{if } degree(root) = 0 \\
   \sum_{i=1}^{k} leaves(T_i) & \text{otherwise}
   \end{cases}

**Number of internal nodes:**

.. math::

   internal(T) = |T| - leaves(T)

Tree Invariants
---------------

A valid general tree satisfies:

1. **Single root**: Exactly one node has no parent

   .. math::
   
      |\{v \in N : \text{parent}(v) \text{ undefined}\}| = 1

2. **Acyclic**: No cycles exist

   .. math::
   
      \nexists \text{ path } v_1 \rightarrow v_2 \rightarrow \cdots \rightarrow v_n \rightarrow v_1

3. **Connected**: Path exists between any two nodes

   .. math::
   
      \forall u, v \in N : \exists \text{ path from } u \text{ to } v

4. **Unique parent**: Each non-root node has exactly one parent

   .. math::
   
      \forall v \in N \setminus \{root\} : |\{u : v \in children(u)\}| = 1

Algebraic Properties
--------------------

**Closure under subtrees:**

.. math::

   T \text{ is a tree} \implies \forall i : T_i \text{ is a tree}

**Node count relationship:**

.. math::

   |T| = 1 + \sum_{v \in children(root)} |subtree(v)|

**Height relationship:**

.. math::

   height(T) = 1 + \max(\{height(T_i) : i = 1, \ldots, k\} \cup \{-1\})

**Leaf count for complete k-ary tree:**

For a complete tree where all internal nodes have exactly :math:`k` children:

.. math::

   leaves = \frac{(k-1) \cdot n + 1}{k}

where :math:`n` is the total number of nodes.

Algorithmic Model
=================

Abstract Data Type (ADT)
-------------------------

.. code-block:: text

   ADT GeneralTree:
       Data:
           - root: reference to root node
           - size: number of nodes
       
       Node:
           - data: stored value
           - parent: reference to parent node
           - children: list of child nodes
       
       Operations:
           - Tree(root_data): create tree with root
           - add_child(parent, child_data): add child to parent
           - remove_node(data): remove node and subtree
           - find_node(data): find node by data
           - height(): return tree height
           - is_leaf(node): check if node is leaf
           - get_children(node): return node's children
           - get_parent(node): return node's parent
       
       Axioms:
           - height(single_node) = 0
           - is_leaf(node) ⟺ children(node) = ∅
           - ∀ node ≠ root: parent(node) exists

Implementation Strategies
--------------------------

Child List Representation
^^^^^^^^^^^^^^^^^^^^^^^^^^

Each node stores a list of references to its children:

.. mermaid::

   graph LR
       A["Node A<br/>children: [B, C, D]"] --> B[Node B]
       A --> C[Node C]
       A --> D[Node D]
       
       C --> E[Node E]
       C --> F[Node F]
       
       style A fill:#e74c3c

**Advantages:**
   * Simple and intuitive
   * Easy to add/remove children
   * Direct access to all children
   * Flexible degree

**Disadvantages:**
   * Variable memory per node
   * Iteration over children is O(k)
   * Cache-unfriendly for many children

**Pseudocode:**

.. code-block:: text

   Node:
       data: any type
       parent: reference to Node
       children: list of Node references
   
   add_child(parent_node, child_data):
       child ← Node(child_data)
       child.parent ← parent_node
       parent_node.children.append(child)
       size ← size + 1
   
   remove_child(parent_node, child):
       parent_node.children.remove(child)
       child.parent ← null
       size ← size - count_subtree(child)

Left-Child Right-Sibling
^^^^^^^^^^^^^^^^^^^^^^^^^

Binary representation of general trees:

.. mermaid::

   graph LR
       A[A] --> B[B: left_child]
       B --> D[D: right_sibling]
       D --> E[E: right_sibling]
       
       B --> F[F: left_child of B]
       
       style A fill:#e74c3c
       style B fill:#3498db
       style F fill:#2ecc71

**Transformation:**
   * Left pointer → first child
   * Right pointer → next sibling

**Advantages:**
   * Fixed space per node (like binary tree)
   * Can use binary tree algorithms
   * Memory efficient

**Disadvantages:**
   * Less intuitive
   * Finding k-th child is O(k)
   * Parent traversal more complex

Core Algorithms
---------------

Tree Traversal
^^^^^^^^^^^^^^

**Preorder Traversal** (Root → Children):

.. code-block:: text

   Algorithm: PREORDER(node)
   Input: Node node
   Output: Sequence of nodes in preorder
   
   1. visit(node)
   2. for each child in node.children do
   3.     PREORDER(child)
   4. end for

**Time complexity**: :math:`O(n)`

**Postorder Traversal** (Children → Root):

.. code-block:: text

   Algorithm: POSTORDER(node)
   Input: Node node
   Output: Sequence of nodes in postorder
   
   1. for each child in node.children do
   2.     POSTORDER(child)
   3. end for
   4. visit(node)

**Time complexity**: :math:`O(n)`

**Level-Order Traversal** (BFS):

.. code-block:: text

   Algorithm: LEVEL_ORDER(root)
   Input: Root node
   Output: Nodes level by level
   
   1. queue ← Queue()
   2. queue.enqueue(root)
   3. while not queue.is_empty() do
   4.     node ← queue.dequeue()
   5.     visit(node)
   6.     for each child in node.children do
   7.         queue.enqueue(child)
   8.     end for
   9. end while

**Time complexity**: :math:`O(n)`

Height Calculation
^^^^^^^^^^^^^^^^^^

.. code-block:: text

   Algorithm: HEIGHT(node)
   Input: Node node
   Output: Height of subtree rooted at node
   
   1. if node.is_leaf() then
   2.     return 0
   3. end if
   4. 
   5. max_height ← -1
   6. for each child in node.children do
   7.     child_height ← HEIGHT(child)
   8.     if child_height > max_height then
   9.         max_height ← child_height
   10.    end if
   11. end for
   12. 
   13. return 1 + max_height

**Time complexity**: :math:`O(n)`
**Space complexity**: :math:`O(h)` for recursion stack

Finding Nodes
^^^^^^^^^^^^^

**Depth-First Search:**

.. code-block:: text

   Algorithm: FIND_DFS(node, target)
   Input: Node node, value target
   Output: Node with target value or null
   
   1. if node.data = target then
   2.     return node
   3. end if
   4. 
   5. for each child in node.children do
   6.     result ← FIND_DFS(child, target)
   7.     if result ≠ null then
   8.         return result
   9.     end if
   10. end for
   11. 
   12. return null

**Time complexity**: :math:`O(n)`
**Space complexity**: :math:`O(h)`

Node Removal
^^^^^^^^^^^^

.. code-block:: text

   Algorithm: REMOVE_SUBTREE(parent, target)
   Input: Node parent, value target
   Output: Removed node or null
   
   1. for i ← 0 to parent.children.size - 1 do
   2.     child ← parent.children[i]
   3.     if child.data = target then
   4.         parent.children.remove(i)
   5.         child.parent ← null
   6.         count ← COUNT_NODES(child)
   7.         size ← size - count
   8.         return child
   9.     end if
   10. end for
   11. return null
   
   Algorithm: COUNT_NODES(node)
   1. count ← 1
   2. for each child in node.children do
   3.     count ← count + COUNT_NODES(child)
   4. end for
   5. return count

**Time complexity**: :math:`O(n)` worst case
**Space complexity**: :math:`O(h)`

Complexity Analysis
-------------------

Time Complexity Summary
^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 35 20 20 25

   * - Operation
     - Average
     - Worst
     - Notes
   * - **add_child(parent)**
     - O(1)
     - O(1)
     - Direct append
   * - **remove_node()**
     - O(n)
     - O(n)
     - Must find node
   * - **find_node()**
     - O(n)
     - O(n)
     - Linear search
   * - **height()**
     - O(n)
     - O(n)
     - Visit all nodes
   * - **is_leaf()**
     - O(1)
     - O(1)
     - Check children list
   * - **get_children()**
     - O(1)
     - O(1)
     - Return list reference
   * - **preorder/postorder**
     - O(n)
     - O(n)
     - Visit all nodes
   * - **level_order**
     - O(n)
     - O(n)
     - BFS traversal

Space Complexity
^^^^^^^^^^^^^^^^

* **Node storage**: :math:`O(n)` for n nodes
* **Parent pointers**: :math:`O(n)`
* **Children lists**: :math:`O(n)` total across all nodes
* **Recursion stack**: :math:`O(h)` where h is height
  * Best case (balanced): :math:`O(\log n)`
  * Worst case (linear): :math:`O(n)`

Practical Usage
===============

Installation and Import
-----------------------

.. code-block:: python

   # Install
   pip install sds-tools
   
   # Import
   from sds.tree import Tree

Basic Operations
----------------

Creating a Tree
^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.tree import Tree

   # Create tree with root
   tree = Tree("CEO")
   
   # Check state
   print(tree.is_empty())  # Output: False
   print(len(tree))        # Output: 1
   print(tree.height())    # Output: 0

Adding Children
^^^^^^^^^^^^^^^

.. code-block:: python

   # Add children to root
   cto = tree.add_child("CTO")
   cfo = tree.add_child("CFO")
   coo = tree.add_child("COO")
   
   # Add grandchildren
   tree.add_child_to("CTO", "Dev Manager")
   tree.add_child_to("CTO", "QA Manager")
   tree.add_child_to("CFO", "Accountant")
   
   print(f"Tree size: {len(tree)}")    # Output: 7
   print(f"Tree height: {tree.height()}")  # Output: 2

Finding Nodes
^^^^^^^^^^^^^

.. code-block:: python

   # Find node by data
   node = tree.find_node("CTO")
   if node:
       print(f"Found: {node.data}")
       print(f"Children: {len(node.children)}")
   
   # Check if value exists
   print("CFO" in tree)  # Output: True
   print("CEO" in tree)  # Output: True

Working with Children
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Get children of a node
   cto_children = tree.get_children("CTO")
   for child in cto_children:
       print(child.data)
   
   # Get parent
   parent = tree.get_parent("Dev Manager")
   print(parent.data)  # Output: CTO
   
   # Check degree
   degree = tree.degree("CTO")
   print(f"CTO has {degree} direct reports")
   
   # Check if leaf
   is_leaf = tree.is_leaf("Accountant")
   print(is_leaf)  # Output: True

Traversals
^^^^^^^^^^

.. code-block:: python

   # Preorder (parent before children)
   print("Preorder:")
   for item in tree.preorder_traversal():
       print(f"  {item}")
   
   # Postorder (children before parent)
   print("Postorder:")
   for item in tree.postorder_traversal():
       print(f"  {item}")
   
   # Level-order (breadth-first)
   print("Level-order:")
   for item in tree.level_order_traversal():
       print(f"  {item}")

Removing Nodes
^^^^^^^^^^^^^^

.. code-block:: python

   # Remove node and its subtree
   tree.remove_node("QA Manager")
   
   # Check updated structure
   print(f"New size: {len(tree)}")
   
   # Get all leaf nodes
   leaves = tree.leaves()
   print(f"Leaves: {leaves}")

Real-World Applications
=======================

Application 1: File System
---------------------------

Representing directory structure:

.. code-block:: python

   from sds.tree import Tree

   class FileSystem:
       """Hierarchical file system using general tree."""
       
       def __init__(self):
           self.tree = Tree("/")  # Root directory
           self.current_path = ["/"]
       
       def mkdir(self, name, parent_path=None):
           """Create directory."""
           if parent_path is None:
               parent_path = "/".join(self.current_path)
           
           try:
               self.tree.add_child_to(parent_path, name)
               return True
           except ValueError:
               print(f"Parent {parent_path} not found")
               return False
       
       def touch(self, filename, parent_path=None):
           """Create file."""
           if parent_path is None:
               parent_path = "/".join(self.current_path)
           
           # Prefix with . to mark as file
           self.tree.add_child_to(parent_path, f".{filename}")
       
       def ls(self, path=None):
           """List directory contents."""
           if path is None:
               path = "/".join(self.current_path)
           
           try:
               children = self.tree.get_children(path)
               dirs = [c.data for c in children if not c.data.startswith('.')]
               files = [c.data[1:] for c in children if c.data.startswith('.')]
               
               print(f"\nContents of {path}:")
               print(f"Directories: {', '.join(dirs) if dirs else 'none'}")
               print(f"Files: {', '.join(files) if files else 'none'}")
           except ValueError:
               print(f"Path {path} not found")
       
       def tree_view(self):
           """Display tree structure."""
           print(self.tree)
       
       def du(self, path="/"):
           """Calculate directory size (count of files)."""
           node = self.tree.find_node(path)
           if not node:
               return 0
           
           count = 0
           
           def count_files(n):
               nonlocal count
               if n.data.startswith('.'):
                   count += 1
               for child in n.children:
                   count_files(child)
           
           count_files(node)
           return count
       
       def find(self, pattern):
           """Find all files matching pattern."""
           results = []
           
           for item in self.tree.preorder_traversal():
               if item.startswith('.') and pattern in item:
                   results.append(item[1:])
           
           return results
   
   # Usage
   fs = FileSystem()
   
   # Build structure
   fs.mkdir("home")
   fs.mkdir("usr")
   fs.mkdir("var")
   
   fs.mkdir("user1", "/home")
   fs.mkdir("user2", "/home")
   
   fs.touch("readme.txt", "/home/user1")
   fs.touch("profile.py", "/home/user1")
   fs.touch("data.csv", "/home/user2")
   
   # Operations
   fs.ls("/home")
   fs.ls("/home/user1")
   
   print(f"\nTotal files in /home: {fs.du('/home')}")
   print(f"Python files: {fs.find('.py')}")
   
   fs.tree_view()

Application 2: Organization Chart
----------------------------------

Managing company hierarchy:

.. code-block:: python

   from sds.tree import Tree
   from dataclasses import dataclass
   from typing import List

   @dataclass
   class Employee:
       """Employee information."""
       name: str
       title: str
       email: str
       department: str
       
       def __repr__(self):
           return f"{self.name} ({self.title})"
   
   class OrganizationChart:
       """Company organizational structure."""
       
       def __init__(self, ceo: Employee):
           self.tree = Tree(ceo)
       
       def add_employee(self, employee: Employee, manager: Employee):
           """Add employee under manager."""
           try:
               self.tree.add_child_to(manager, employee)
               print(f"Added {employee.name} under {manager.name}")
           except ValueError:
               print(f"Manager {manager.name} not found")
       
       def get_direct_reports(self, manager: Employee) -> List[Employee]:
           """Get direct reports of a manager."""
           try:
               children = self.tree.get_children(manager)
               return [child.data for child in children]
           except ValueError:
               return []
       
       def get_all_reports(self, manager: Employee) -> List[Employee]:
           """Get all reports (recursive) under manager."""
           node = self.tree.find_node(manager)
           if not node:
               return []
           
           reports = []
           
           def collect(n):
               for child in n.children:
                   reports.append(child.data)
                   collect(child)
           
           collect(node)
           return reports
       
       def find_manager(self, employee: Employee) -> Employee:
           """Find employee's manager."""
           try:
               parent = self.tree.get_parent(employee)
               return parent.data if parent else None
           except ValueError:
               return None
       
       def get_department_size(self, head: Employee) -> int:
           """Get total employees in department."""
           all_reports = self.get_all_reports(head)
           return len(all_reports) + 1  # Include head
       
       def reorganize(self, employee: Employee, new_manager: Employee):
           """Move employee to new manager."""
           # Remove from current position
           self.tree.remove_node(employee)
           # Add under new manager
           self.add_employee(employee, new_manager)
       
       def print_hierarchy(self, employee: Employee = None, indent: int = 0):
           """Print org chart hierarchy."""
           if employee is None:
               employee = self.tree.root.data
           
           print("  " * indent + f"- {employee}")
           
           reports = self.get_direct_reports(employee)
           for report in reports:
               self.print_hierarchy(report, indent + 1)
   
   # Usage
   ceo = Employee("Alice Johnson", "CEO", "alice@company.com", "Executive")
   org = OrganizationChart(ceo)
   
   # Build org chart
   cto = Employee("Bob Smith", "CTO", "bob@company.com", "Engineering")
   cfo = Employee("Carol White", "CFO", "carol@company.com", "Finance")
   
   org.add_employee(cto, ceo)
   org.add_employee(cfo, ceo)
   
   dev_mgr = Employee("Dave Brown", "Dev Manager", "dave@company.com", "Engineering")
   qa_mgr = Employee("Eve Davis", "QA Manager", "eve@company.com", "Engineering")
   
   org.add_employee(dev_mgr, cto)
   org.add_employee(qa_mgr, cto)
   
   # Query org chart
   print("\n=== Organization Hierarchy ===")
   org.print_hierarchy()
   
   print(f"\nCTO's direct reports: {org.get_direct_reports(cto)}")
   print(f"Engineering dept size: {org.get_department_size(cto)}")
   print(f"Dave's manager: {org.find_manager(dev_mgr)}")

Application 3: XML/HTML Parser
-------------------------------

Parsing hierarchical markup:

.. code-block:: python

   from sds.tree import Tree
   from sds.tree.node import TreeNode

   class XMLNode:
       """Represent XML element."""
       def __init__(self, tag, attributes=None, text=None):
           self.tag = tag
           self.attributes = attributes or {}
           self.text = text
       
       def __repr__(self):
           attrs = ' '.join(f'{k}="{v}"' for k, v in self.attributes.items())
           if attrs:
               return f"<{self.tag} {attrs}>"
           return f"<{self.tag}>"
   
   class XMLTree:
       """Simple XML document tree."""
       
       def __init__(self, root_tag):
           root_element = XMLNode(root_tag)
           self.tree = Tree(root_element)
       
       def add_element(self, parent_tag, tag, attributes=None, text=None):
           """Add XML element under parent."""
           # Find parent node
           parent_node = None
           for item in self.tree.preorder_traversal():
               if item.tag == parent_tag:
                   parent_node = item
                   break
           
           if parent_node:
               element = XMLNode(tag, attributes, text)
               self.tree.add_child_to(parent_node, element)
           else:
               raise ValueError(f"Parent tag '{parent_tag}' not found")
       
       def find_by_tag(self, tag):
           """Find all elements with given tag."""
           results = []
           for item in self.tree.preorder_traversal():
               if item.tag == tag:
                   results.append(item)
           return results
       
       def find_by_attribute(self, attr_name, attr_value):
           """Find elements by attribute."""
           results = []
           for item in self.tree.preorder_traversal():
               if attr_name in item.attributes and item.attributes[attr_name] == attr_value:
                   results.append(item)
           return results
       
       def to_xml_string(self, node=None, indent=0):
           """Generate XML string."""
           if node is None:
               node = self.tree.root.data
           
           indent_str = "  " * indent
           xml = f"{indent_str}<{node.tag}"
           
           # Add attributes
           for key, val in node.attributes.items():
               xml += f' {key}="{val}"'
           
           # Find children
           children = []
           tree_node = self.tree.find_node(node)
           if tree_node:
               children = [c.data for c in tree_node.children]
           
           if not children and not node.text:
               xml += " />\n"
           else:
               xml += ">"
               
               if node.text:
                   xml += node.text
               
               if children:
                   xml += "\n"
                   for child in children:
                       xml += self.to_xml_string(child, indent + 1)
                   xml += indent_str
               
               xml += f"</{node.tag}>\n"
           
           return xml
   
   # Usage
   doc = XMLTree("html")
   
   # Build document
   doc.add_element("html", "head")
   doc.add_element("head", "title", text="My Page")
   doc.add_element("head", "meta", {"charset": "UTF-8"})
   
   doc.add_element("html", "body")
   doc.add_element("body", "div", {"class": "container"})
   doc.add_element("div", "h1", text="Welcome")
   doc.add_element("div", "p", {"id": "intro"}, text="This is a paragraph.")
   
   # Query
   print("All div elements:")
   for div in doc.find_by_tag("div"):
       print(f"  {div}")
   
   print("\nElements with class attribute:")
   for elem in doc.find_by_attribute("class", "container"):
       print(f"  {elem}")
   
   # Generate XML
   print("\nGenerated XML:")
   print(doc.to_xml_string())

Application 4: Game Tree (Decision Making)
-------------------------------------------

AI decision tree for games:

.. code-block:: python

   from sds.tree import Tree
   from enum import Enum

   class Player(Enum):
       MAX = "MAX"
       MIN = "MIN"
   
   class GameState:
       """Represent game state."""
       def __init__(self, board, player, score=0):
           self.board = board
           self.player = player
           self.score = score
       
       def __repr__(self):
           return f"GameState(player={self.player.value}, score={self.score})"
   
   class GameTree:
       """Game tree for minimax algorithm."""
       
       def __init__(self, initial_state):
           self.tree = Tree(initial_state)
       
       def build_tree(self, state, depth, max_depth=3):
           """Build game tree to given depth."""
           if depth >= max_depth:
               return
           
           # Generate possible moves
           moves = self.generate_moves(state)
           
           for move in moves:
               new_state = self.apply_move(state, move)
               self.tree.add_child_to(state, new_state)
               self.build_tree(new_state, depth + 1, max_depth)
       
       def generate_moves(self, state):
           """Generate possible moves (simplified)."""
           # In real game, generate valid moves
           moves = []
           for i in range(3):  # Simplified: 3 possible moves
               next_player = Player.MIN if state.player == Player.MAX else Player.MAX
               new_score = state.score + (1 if state.player == Player.MAX else -1) * (i + 1)
               moves.append(GameState(state.board, next_player, new_score))
           return moves
       
       def apply_move(self, state, move):
           """Apply move to state."""
           return move
       
       def minimax(self, state, is_maximizing):
           """Minimax algorithm."""
           node = self.tree.find_node(state)
           if not node or node.is_leaf():
               return state.score
           
           children = [c.data for c in node.children]
           
           if is_maximizing:
               max_eval = float('-inf')
               for child in children:
                   eval_score = self.minimax(child, False)
                   max_eval = max(max_eval, eval_score)
               return max_eval
           else:
               min_eval = float('inf')
               for child in children:
                   eval_score = self.minimax(child, True)
                   min_eval = min(min_eval, eval_score)
               return min_eval
       
       def find_best_move(self, root_state):
           """Find best move using minimax."""
           node = self.tree.find_node(root_state)
           if not node:
               return None
           
           children = [c.data for c in node.children]
           best_move = None
           best_score = float('-inf') if root_state.player == Player.MAX else float('inf')
           
           for child in children:
               score = self.minimax(child, root_state.player == Player.MIN)
               
               if root_state.player == Player.MAX:
                   if score > best_score:
                       best_score = score
                       best_move = child
               else:
                   if score < best_score:
                       best_score = score
                       best_move = child
           
           return best_move, best_score
   
   # Usage
   initial = GameState("initial_board", Player.MAX, 0)
   game_tree = GameTree(initial)
   
   # Build game tree
   game_tree.build_tree(initial, depth=0, max_depth=3)
   
   # Find best move
   best_move, score = game_tree.find_best_move(initial)
   print(f"Best move: {best_move}")
   print(f"Expected score: {score}")

Best Practices
==============

Do's
----

✅ **Use appropriate traversal for the task**

.. code-block:: python

   # Preorder: Process parent before children (e.g., copy tree)
   for item in tree.preorder_traversal():
       copy_node(item)
   
   # Postorder: Process children before parent (e.g., delete tree, calculate sizes)
   for item in tree.postorder_traversal():
       process_children_first(item)
   
   # Level-order: Process by levels (e.g., print hierarchy)
   for item in tree.level_order_traversal():
       print_by_level(item)

✅ **Check node existence before operations**

.. code-block:: python

   node = tree.find_node("target")
   if node:
       children = tree.get_children("target")
   else:
       print("Node not found")

✅ **Use helper methods for common queries**

.. code-block:: python

   # Check if leaf
   if tree.is_leaf("node_data"):
       print("This is a leaf node")
   
   # Get degree
   degree = tree.degree("node_data")
   print(f"Node has {degree} children")
   
   # Get all leaves
   leaves = tree.leaves()

Don'ts
------

❌ **Don't create circular references**

.. code-block:: python

   # Bad: Creates cycle
   node1 = tree.find_node("A")
   node2 = tree.find_node("B")
   # If B is descendant of A, adding A as child of B creates cycle!

❌ **Don't modify tree during iteration**

.. code-block:: python

   # Bad: Modifying while iterating
   for item in tree.preorder_traversal():
       tree.remove_node(item)  # Dangerous!
   
   # Good: Collect first, then modify
   to_remove = list(tree.preorder_traversal())
   for item in to_remove:
       tree.remove_node(item)

❌ **Don't assume specific child order**

.. code-block:: python

   # Bad: Assuming order
   children = tree.get_children("parent")
   first_child = children[0]  # Order may not be preserved
   
   # Good: Search by property
   target_child = next((c for c in children if c.data.startswith("A")), None)

Performance Tips
----------------

1. **Cache frequently accessed nodes**

.. code-block:: python

   # Cache important nodes
   root = tree.root
   frequently_accessed = tree.find_node("important")

2. **Use BFS for shallow searches**

.. code-block:: python

   # Level-order is better for shallow targets
   for item in tree.level_order_traversal():
       if matches(item):
           return item

3. **Batch operations when possible**

.. code-block:: python

   # Collect all operations first
   operations = [("add", "A", "B"), ("add", "C", "D")]
   for op, child, parent in operations:
       tree.add_child_to(parent, child)

Common Pitfalls
===============

1. **Forgetting to update size**

The Tree class handles this automatically, but if implementing your own:

.. code-block:: python

   # Wrong
   parent.children.append(child)
   
   # Right
   parent.add_child(child)
   size += 1

2. **Deep recursion on large trees**

.. code-block:: python

   import sys
   
   # Check recursion limit
   print(sys.getrecursionlimit())  # Default: 1000
   
   # Increase if needed
   sys.setrecursionlimit(5000)
   
   # Or use iterative approach
   def iterative_traversal(tree):
       stack = [tree.root]
       while stack:
           node = stack.pop()
           # Process node
           stack.extend(node.children)

3. **Memory leaks with large trees**

.. code-block:: python

   # Clear tree when done
   tree.clear()
   
   # Break circular references if any
   for node in all_nodes:
       node.parent = None
       node.children.clear()

Further Reading
===============

* :doc:`/api/tree/general` - Complete API reference
* :doc:`binary` - Binary tree structures
* :doc:`../tree_structures/index` - Overview of all tree structures

References
==========

Academic and Educational Resources
-----------------------------------

.. [WikiTree] Wikipedia contributors. "Tree (data structure)". Wikipedia, The Free Encyclopedia.
   https://en.wikipedia.org/wiki/Tree_(data_structure)
   
   Comprehensive overview of tree terminology, properties, and types. Excellent starting point
   for understanding tree fundamentals and mathematical definitions.

.. [WikiGeneral] Wikipedia contributors. "Tree (graph theory)". Wikipedia, The Free Encyclopedia.
   https://en.wikipedia.org/wiki/Tree_(graph_theory)
   
   Mathematical treatment of trees from graph theory perspective, including proofs of properties
   and relationships between nodes, edges, and tree characteristics.

.. [OpenDSA] Shaffer, C. A., et al. "OpenDSA Data Structures and Algorithms Modules Collection".
   https://opendsa-server.cs.vt.edu/ODSA/Books/Everything/html/
   
   Interactive, open-source textbook with visualizations and exercises. See chapters on:
   
   - "General Trees" for n-ary tree implementations
   - "Tree Traversals" for preorder, postorder, and level-order algorithms
   - "Space/Time Tradeoffs" for complexity analysis

.. [MIT6006] MIT OpenCourseWare. "6.006 Introduction to Algorithms, Fall 2011".
   https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/
   
   Free course materials including lecture notes and problem sets. Particularly relevant:
   
   - Lecture 5: Binary Search Trees, BST Sort
   - Lecture 6: AVL Trees, AVL Sort
   - Recitation notes on tree algorithms

.. [VisuAlgo] Halim, S., Halim, F. "VisuAlgo - Visualising Data Structures and Algorithms".
   https://visualgo.net/en
   
   Interactive visualizations for learning. Relevant modules:
   
   - Binary Search Tree: https://visualgo.net/en/bst
   - Heap: https://visualgo.net/en/heap
   
   Includes step-by-step animations of insertions, deletions, and traversals.

.. [USFViz] Galles, D. "Data Structure Visualizations". University of San Francisco.
   https://www.cs.usfca.edu/~galles/visualization/
   
   Excellent interactive visualizations for:
   
   - General Trees: https://www.cs.usfca.edu/~galles/visualization/Tree.html
   - AVL Trees: https://www.cs.usfca.edu/~galles/visualization/AVLtree.html
   - Red-Black Trees: https://www.cs.usfca.edu/~galles/visualization/RedBlack.html

.. [Stanford] Stanford CS Education Library. "Binary Trees".
   http://cslibrary.stanford.edu/110/BinaryTrees.html
   
   Comprehensive tutorial on binary tree problems and solutions, with detailed code examples
   and complexity analysis.

Classic Computer Science Literature
------------------------------------

While the following are not freely available online, they are cited as authoritative references:

.. [CLRS] Cormen, T. H., Leiserson, C. E., Rivest, R. L., Stein, C. 
   "Introduction to Algorithms", 3rd Edition, 2009. MIT Press.
   
   Chapter 10: Elementary Data Structures - covers tree fundamentals
   Chapter 12: Binary Search Trees - BST operations and analysis
   
   *Note: Some editions available through MIT OCW and university libraries*

.. [Knuth] Knuth, D. E. "The Art of Computer Programming, Volume 1: Fundamental Algorithms",
   3rd Edition, 1997. Addison-Wesley.
   
   Section 2.3: Trees - mathematical treatment and classical algorithms
   
   Author's website: https://www-cs-faculty.stanford.edu/~knuth/taocp.html

.. [AHU] Aho, A. V., Hopcroft, J. E., Ullman, J. D. 
   "Data Structures and Algorithms", 1983. Addison-Wesley.
   
   Chapter 4: Trees - comprehensive coverage of tree structures and algorithms

.. [Tarjan] Tarjan, R. E. "Data Structures and Network Algorithms", 1983. 
   Society for Industrial and Applied Mathematics.
   
   Advanced treatment of tree data structures with amortized analysis

Online Courses and Tutorials
-----------------------------

.. [Coursera] Princeton University. "Algorithms, Part I" (Sedgewick & Wayne).
   https://www.coursera.org/learn/algorithms-part1
   
   Free course with accompanying website: https://algs4.cs.princeton.edu/
   Week 4 covers elementary symbol tables and BSTs

.. [GeeksforGeeks] GeeksforGeeks. "Tree Data Structure".
   https://www.geeksforgeeks.org/tree-data-structure/
   
   Practical tutorials with code examples in multiple languages. Includes:
   
   - Tree traversals (all methods)
   - Applications and problems
   - Interview questions

.. [Programiz] Programiz. "Tree Data Structure".
   https://www.programiz.com/dsa/trees
   
   Beginner-friendly tutorials with clear explanations and visualizations
