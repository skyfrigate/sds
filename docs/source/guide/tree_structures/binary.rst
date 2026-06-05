.. _guide_tree_binary:

==================
Binary Trees Guide
==================

.. currentmodule:: sds.tree

Introduction
============

A **binary tree** is a hierarchical data structure where each node has at most two children,
referred to as the **left child** and **right child**. A **binary search tree (BST)** is a
special type of binary tree that maintains an ordering property: for each node, all values
in the left subtree are less than the node's value, and all values in the right subtree
are greater.

.. mermaid::

   graph TB
       subgraph "Binary Tree (unordered)"
       A1[10] --> B1[5]
       A1 --> C1[15]
       B1 --> D1[3]
       B1 --> E1[7]
       end
       
       subgraph "Binary Search Tree (ordered)"
       A2[50] --> B2[30]
       A2 --> C2[70]
       B2 --> D2[20]
       B2 --> E2[40]
       C2 --> F2[60]
       C2 --> G2[80]
       end
       
       style A1 fill:#95a5a6
       style A2 fill:#e74c3c,color:#fff

.. note::
   
   Binary trees are fundamental structures used in compilers, expression evaluation,
   and many search algorithms. BSTs enable efficient searching, insertion, and deletion
   when properly balanced.

Mathematical Model
==================

Formal Definition
-----------------

Binary Tree
^^^^^^^^^^^

A binary tree :math:`T` is defined recursively as either:

1. Empty: :math:`T = \emptyset`
2. A node with two subtrees:

.. math::

   T = (root, T_L, T_R)

where:
   * :math:`root` is the root node containing data
   * :math:`T_L` is the left subtree (also a binary tree)
   * :math:`T_R` is the right subtree (also a binary tree)

Binary Search Tree
^^^^^^^^^^^^^^^^^^

A BST is a binary tree that satisfies the **BST property**:

.. math::

   \forall node \in T: \begin{cases}
   \forall x \in T_L: x.data < node.data \\
   \forall y \in T_R: y.data > node.data \\
   T_L \text{ and } T_R \text{ are BSTs}
   \end{cases}

This property must hold recursively for all nodes in the tree.

Tree Properties
---------------

Height and Depth
^^^^^^^^^^^^^^^^

**Height of a node** :math:`h(v)`:

.. math::

   h(v) = \begin{cases}
   0 & \text{if } v \text{ is a leaf} \\
   1 + \max(h(v.left), h(v.right)) & \text{otherwise}
   \end{cases}

**Height of the tree**:

.. math::

   height(T) = h(root)

**Depth of a node** :math:`d(v)`:

.. math::

   d(v) = \begin{cases}
   0 & \text{if } v = root \\
   1 + d(parent(v)) & \text{otherwise}
   \end{cases}

Size and Balance
^^^^^^^^^^^^^^^^

**Number of nodes**:

.. math::

   |T| = \begin{cases}
   0 & \text{if } T = \emptyset \\
   1 + |T_L| + |T_R| & \text{otherwise}
   \end{cases}

**Balance factor** (for node :math:`v`):

.. math::

   BF(v) = height(v.left) - height(v.right)

A tree is **balanced** if :math:`|BF(v)| \leq 1` for all nodes :math:`v`.

Height Bounds
^^^^^^^^^^^^^

For a binary tree with :math:`n` nodes:

**Minimum height** (perfect tree):

.. math::

   h_{min} = \lfloor \log_2 n \rfloor

**Maximum height** (degenerate tree):

.. math::

   h_{max} = n - 1

**Average height** (random insertion):

.. math::

   h_{avg} \approx 1.386 \log_2 n \approx 1.386 \ln n

Node Count Bounds
^^^^^^^^^^^^^^^^^

For a binary tree of height :math:`h`:

**Minimum nodes**:

.. math::

   n_{min} = h + 1

**Maximum nodes** (perfect tree):

.. math::

   n_{max} = 2^{h+1} - 1

**Number of leaves**:

.. math::

   leaves = \lceil \frac{n + 1}{2} \rceil

Tree Invariants
---------------

Binary Tree Invariants
^^^^^^^^^^^^^^^^^^^^^^

1. **Binary constraint**: Each node has at most 2 children

   .. math::
   
      \forall v \in T: |\{v.left, v.right\}| \leq 2

2. **Acyclic**: No cycles exist

   .. math::
   
      \nexists \text{ path } v_1 \rightarrow v_2 \rightarrow \cdots \rightarrow v_n \rightarrow v_1

3. **Single parent**: Each non-root node has exactly one parent

   .. math::
   
      \forall v \neq root: \exists! p : v \in \{p.left, p.right\}

BST Invariants
^^^^^^^^^^^^^^

In addition to binary tree invariants:

4. **Ordering property**: Left < Parent < Right

   .. math::
   
      \forall v: (v.left \implies v.left.data < v.data) \land (v.right \implies v.right.data > v.data)

5. **Recursive property**: Subtrees are BSTs

   .. math::
   
      isBST(T) \iff isBST(T_L) \land isBST(T_R) \land \text{ordering holds}

Algebraic Properties
--------------------

**Inorder traversal of BST yields sorted sequence**:

.. math::

   inorder(BST) = \text{sorted}(\{v.data : v \in BST\})

**Height after :math:`n` random insertions**:

.. math::

   E[h] = O(\log n)

**Search time in BST**:

.. math::

   T(n) = \begin{cases}
   O(\log n) & \text{if balanced} \\
   O(n) & \text{if degenerate}
   \end{cases}

**Number of different BSTs with :math:`n` nodes** (Catalan number):

.. math::

   C_n = \frac{1}{n+1}\binom{2n}{n} = \frac{(2n)!}{(n+1)!n!}

Algorithmic Model
=================

Abstract Data Type (ADT)
-------------------------

.. code-block:: text

   ADT BinarySearchTree:
       Data:
           - root: reference to root node
           - size: number of nodes
       
       Node:
           - data: stored value
           - left: reference to left child
           - right: reference to right child
           - parent: reference to parent (optional)
       
       Operations:
           - BinarySearchTree(): create empty tree
           - insert(item): add item maintaining BST property
           - remove(item): remove item maintaining BST property
           - search(item): find if item exists
           - find_min(): return minimum value
           - find_max(): return maximum value
           - height(): return tree height
           - inorder(): return sorted sequence
           - preorder(): return preorder sequence
           - postorder(): return postorder sequence
       
       Axioms:
           - inorder(BST) is sorted
           - search(insert(T, x), x) = true
           - find_min() returns leftmost node
           - find_max() returns rightmost node

Implementation Strategies
--------------------------

Node Representation
^^^^^^^^^^^^^^^^^^^

Each node stores:

.. code-block:: text

   Node:
       data: any comparable type
       left: Node or null
       right: Node or null
       parent: Node or null (optional)

.. mermaid::

   graph LR
       A["Node<br/>data: 50"] --> B["left<br/>→ 30"]
       A --> C["right<br/>→ 70"]
       
       style A fill:#e74c3c,color:#fff

**Memory layout**:

.. code-block:: text

   For n nodes:
   - Data: n × sizeof(data)
   - Pointers: n × 2 pointers (left, right)
   - Optional parent: n × 1 pointer
   - Total: O(n)

Core Algorithms
---------------

Search Algorithm
^^^^^^^^^^^^^^^^

**Recursive search**:

.. code-block:: text

   Algorithm: SEARCH_BST(node, key)
   Input: Node node, value key
   Output: true if key found, false otherwise
   
   1. if node = null then
   2.     return false
   3. end if
   4. 
   5. if key = node.data then
   6.     return true
   7. else if key < node.data then
   8.     return SEARCH_BST(node.left, key)
   9. else
   10.    return SEARCH_BST(node.right, key)
   11. end if

**Time complexity**: 
   - Best: :math:`O(1)` (root)
   - Average: :math:`O(\log n)` (balanced)
   - Worst: :math:`O(n)` (degenerate)

**Space complexity**: :math:`O(h)` for recursion stack

Insertion Algorithm
^^^^^^^^^^^^^^^^^^^

**Recursive insertion**:

.. code-block:: text

   Algorithm: INSERT_BST(node, key)
   Input: Node node, value key
   Output: Updated node after insertion
   
   1. if node = null then
   2.     return Node(key)
   3. end if
   4. 
   5. if key < node.data then
   6.     node.left ← INSERT_BST(node.left, key)
   7. else
   8.     node.right ← INSERT_BST(node.right, key)
   9. end if
   10. 
   11. return node

**Iterative insertion**:

.. code-block:: text

   Algorithm: INSERT_BST_ITERATIVE(root, key)
   Input: Node root, value key
   Output: Root of updated tree
   
   1. new_node ← Node(key)
   2. 
   3. if root = null then
   4.     return new_node
   5. end if
   6. 
   7. current ← root
   8. parent ← null
   9. 
   10. while current ≠ null do
   11.     parent ← current
   12.     if key < current.data then
   13.         current ← current.left
   14.     else
   15.         current ← current.right
   16.     end if
   17. end while
   18. 
   19. if key < parent.data then
   20.     parent.left ← new_node
   21. else
   22.     parent.right ← new_node
   23. end if
   24. 
   25. return root

**Time complexity**: Same as search

Deletion Algorithm
^^^^^^^^^^^^^^^^^^

**Three cases**:

1. **Node has no children** (leaf): Simply remove
2. **Node has one child**: Replace with child
3. **Node has two children**: Replace with inorder successor

.. code-block:: text

   Algorithm: DELETE_BST(node, key)
   Input: Node node, value key
   Output: Updated node after deletion
   
   1. if node = null then
   2.     return null
   3. end if
   4. 
   5. // Find the node to delete
   6. if key < node.data then
   7.     node.left ← DELETE_BST(node.left, key)
   8. else if key > node.data then
   9.     node.right ← DELETE_BST(node.right, key)
   10. else
   11.     // Node found, handle three cases
   12.     
   13.     // Case 1: No left child
   14.     if node.left = null then
   15.         return node.right
   16.     end if
   17.     
   18.     // Case 2: No right child
   19.     if node.right = null then
   20.         return node.left
   21.     end if
   22.     
   23.     // Case 3: Two children
   24.     // Find inorder successor (min in right subtree)
   25.     successor ← FIND_MIN(node.right)
   26.     node.data ← successor.data
   27.     node.right ← DELETE_BST(node.right, successor.data)
   28. end if
   29. 
   30. return node

**Time complexity**: :math:`O(h)` where :math:`h` is height

Min/Max Operations
^^^^^^^^^^^^^^^^^^

.. code-block:: text

   Algorithm: FIND_MIN(node)
   Input: Node node
   Output: Minimum value in subtree
   
   1. if node = null then
   2.     error "Empty tree"
   3. end if
   4. 
   5. while node.left ≠ null do
   6.     node ← node.left
   7. end while
   8. 
   9. return node.data
   
   Algorithm: FIND_MAX(node)
   Input: Node node
   Output: Maximum value in subtree
   
   1. if node = null then
   2.     error "Empty tree"
   3. end if
   4. 
   5. while node.right ≠ null do
   6.     node ← node.right
   7. end while
   8. 
   9. return node.data

**Time complexity**: :math:`O(h)`

Tree Traversal Algorithms
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Inorder (Left-Root-Right)**:

.. code-block:: text

   Algorithm: INORDER(node)
   Input: Node node
   Output: Sequence of values in sorted order
   
   1. if node = null then
   2.     return
   3. end if
   4. 
   5. INORDER(node.left)
   6. visit(node)
   7. INORDER(node.right)

For BST, inorder traversal yields values in sorted order.

**Preorder (Root-Left-Right)**:

.. code-block:: text

   Algorithm: PREORDER(node)
   Input: Node node
   Output: Sequence of values (root first)
   
   1. if node = null then
   2.     return
   3. end if
   4. 
   5. visit(node)
   6. PREORDER(node.left)
   7. PREORDER(node.right)

Useful for creating a copy of the tree.

**Postorder (Left-Right-Root)**:

.. code-block:: text

   Algorithm: POSTORDER(node)
   Input: Node node
   Output: Sequence of values (root last)
   
   1. if node = null then
   2.     return
   3. end if
   4. 
   5. POSTORDER(node.left)
   6. POSTORDER(node.right)
   7. visit(node)

Useful for deleting the tree (children before parent).

**Level-order (BFS)**:

.. code-block:: text

   Algorithm: LEVEL_ORDER(root)
   Input: Node root
   Output: Nodes level by level
   
   1. if root = null then
   2.     return
   3. end if
   4. 
   5. queue ← Queue()
   6. queue.enqueue(root)
   7. 
   8. while not queue.is_empty() do
   9.     node ← queue.dequeue()
   10.    visit(node)
   11.    
   12.    if node.left ≠ null then
   13.        queue.enqueue(node.left)
   14.    end if
   15.    
   16.    if node.right ≠ null then
   17.        queue.enqueue(node.right)
   18.    end if
   19. end while

**Time complexity**: All traversals are :math:`O(n)`

Height Calculation
^^^^^^^^^^^^^^^^^^

.. code-block:: text

   Algorithm: HEIGHT(node)
   Input: Node node
   Output: Height of subtree rooted at node
   
   1. if node = null then
   2.     return -1
   3. end if
   4. 
   5. left_height ← HEIGHT(node.left)
   6. right_height ← HEIGHT(node.right)
   7. 
   8. return 1 + max(left_height, right_height)

**Time complexity**: :math:`O(n)`
**Space complexity**: :math:`O(h)` for recursion

Complexity Analysis
-------------------

Time Complexity
^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 20 20 20 10

   * - Operation
     - Best Case
     - Average Case
     - Worst Case
     - Notes
   * - **Search**
     - O(1)
     - O(log n)
     - O(n)
     - \*
   * - **Insert**
     - O(1)
     - O(log n)
     - O(n)
     - \*
   * - **Delete**
     - O(1)
     - O(log n)
     - O(n)
     - \*
   * - **Find Min**
     - O(1)
     - O(log n)
     - O(n)
     - \*
   * - **Find Max**
     - O(1)
     - O(log n)
     - O(n)
     - \*
   * - **Inorder**
     - O(n)
     - O(n)
     - O(n)
     - 
   * - **Preorder**
     - O(n)
     - O(n)
     - O(n)
     - 
   * - **Postorder**
     - O(n)
     - O(n)
     - O(n)
     - 
   * - **Level-order**
     - O(n)
     - O(n)
     - O(n)
     - 
   * - **Height**
     - O(n)
     - O(n)
     - O(n)
     - 

\* Depends on tree balance

**Key insight**: BST operations are :math:`O(h)` where :math:`h` is height.
For balanced tree: :math:`h = O(\log n)`, for degenerate: :math:`h = O(n)`.

Space Complexity
^^^^^^^^^^^^^^^^

* **Tree storage**: :math:`O(n)` for :math:`n` nodes
* **Recursion stack**: :math:`O(h)` for recursive operations
  * Balanced: :math:`O(\log n)`
  * Degenerate: :math:`O(n)`

Practical Usage
===============

Installation and Import
-----------------------

.. code-block:: python

   # Install
   pip install sds-tools
   
   # Import
   from sds.tree import BinaryTree, BinarySearchTree

Binary Tree Operations
----------------------

Creating and Populating
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.tree import BinaryTree

   # Create empty tree
   tree = BinaryTree()
   
   # Insert elements (level-order)
   tree.insert(10)
   tree.insert(5)
   tree.insert(15)
   tree.insert(3)
   tree.insert(7)
   
   print(f"Size: {len(tree)}")      # Output: 5
   print(f"Height: {tree.height()}")  # Output: 2

Searching
^^^^^^^^^

.. code-block:: python

   # Search for element
   print(tree.search(7))   # Output: True
   print(tree.search(20))  # Output: False
   
   # Using 'in' operator
   print(7 in tree)        # Output: True
   print(20 in tree)       # Output: False

Traversals
^^^^^^^^^^

.. code-block:: python

   # Inorder traversal
   print("Inorder:", list(tree.inorder_traversal()))
   # Output: [3, 5, 7, 10, 15]
   
   # Preorder traversal
   print("Preorder:", list(tree.preorder_traversal()))
   # Output: [10, 5, 3, 7, 15]
   
   # Postorder traversal
   print("Postorder:", list(tree.postorder_traversal()))
   # Output: [3, 7, 5, 15, 10]
   
   # Level-order traversal
   print("Level-order:", list(tree.level_order_traversal()))
   # Output: [10, 5, 15, 3, 7]

Binary Search Tree Operations
------------------------------

Creating and Building BST
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.tree import BinarySearchTree

   # Create BST
   bst = BinarySearchTree()
   
   # Insert in random order
   values = [50, 30, 70, 20, 40, 60, 80]
   for val in values:
       bst.insert(val)
   
   # Inorder gives sorted output
   print(list(bst.inorder_traversal()))
   # Output: [20, 30, 40, 50, 60, 70, 80]

Efficient Searching
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # O(log n) average case search
   print(bst.search(40))   # Output: True
   print(40 in bst)        # Output: True
   
   # Search for non-existent
   print(bst.search(25))   # Output: False

Min/Max Operations
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Find minimum (leftmost)
   print(bst.find_min())   # Output: 20
   
   # Find maximum (rightmost)
   print(bst.find_max())   # Output: 80

Deletion
^^^^^^^^

.. code-block:: python

   # Delete leaf node
   bst.remove(20)
   print(list(bst.inorder_traversal()))
   # Output: [30, 40, 50, 60, 70, 80]
   
   # Delete node with one child
   bst.remove(30)
   print(list(bst.inorder_traversal()))
   # Output: [40, 50, 60, 70, 80]
   
   # Delete node with two children
   bst.remove(50)  # Replaced by successor (60)
   print(list(bst.inorder_traversal()))
   # Output: [40, 60, 70, 80]

Real-World Applications
=======================

Application 1: Expression Tree Evaluator
-----------------------------------------

Parsing and evaluating mathematical expressions:

.. code-block:: python

   from sds.tree import BinaryTree
   from sds.tree.node import BinaryNode

   class ExpressionTree(BinaryTree):
       """Evaluate arithmetic expressions using binary tree."""
       
       def build_from_postfix(self, postfix_expr):
           """Build expression tree from postfix notation."""
           from sds.linear import Stack
           
           stack = Stack()
           operators = {'+', '-', '*', '/', '^'}
           
           for token in postfix_expr.split():
               if token not in operators:
                   # Operand: create leaf node
                   node = BinaryNode(float(token))
                   stack.push(node)
               else:
                   # Operator: create internal node
                   node = BinaryNode(token)
                   node.right = stack.pop()
                   node.left = stack.pop()
                   stack.push(node)
           
           self._root = stack.pop()
           self._size = self._count_nodes(self._root)
       
       def _count_nodes(self, node):
           """Count nodes in subtree."""
           if node is None:
               return 0
           return 1 + self._count_nodes(node.left) + self._count_nodes(node.right)
       
       def evaluate(self):
           """Evaluate the expression tree."""
           return self._evaluate_node(self._root)
       
       def _evaluate_node(self, node):
           """Recursively evaluate a node."""
           if node is None:
               return 0
           
           # Leaf node: return the number
           if node.is_leaf():
               return node.data
           
           # Internal node: apply operator
           left_val = self._evaluate_node(node.left)
           right_val = self._evaluate_node(node.right)
           
           operators = {
               '+': lambda a, b: a + b,
               '-': lambda a, b: a - b,
               '*': lambda a, b: a * b,
               '/': lambda a, b: a / b if b != 0 else float('inf'),
               '^': lambda a, b: a ** b
           }
           
           return operators[node.data](left_val, right_val)
       
       def to_infix(self):
           """Convert to infix notation with parentheses."""
           return self._to_infix_node(self._root)
       
       def _to_infix_node(self, node):
           """Convert node to infix string."""
           if node is None:
               return ""
           
           if node.is_leaf():
               return str(node.data)
           
           left_expr = self._to_infix_node(node.left)
           right_expr = self._to_infix_node(node.right)
           
           return f"({left_expr} {node.data} {right_expr})"
   
   # Usage
   expr_tree = ExpressionTree()
   
   # Build from postfix: "3 4 + 2 * 7 /" = ((3+4)*2)/7
   expr_tree.build_from_postfix("3 4 + 2 * 7 /")
   
   print(f"Infix: {expr_tree.to_infix()}")
   # Output: ((3.0 + 4.0) * 2.0) / 7.0)
   
   print(f"Result: {expr_tree.evaluate()}")
   # Output: 2.0
   
   # More complex: "(5 + 3) * (7 - 2)" in postfix: "5 3 + 7 2 - *"
   expr_tree2 = ExpressionTree()
   expr_tree2.build_from_postfix("5 3 + 7 2 - *")
   
   print(f"Result: {expr_tree2.evaluate()}")
   # Output: 40.0

Application 2: Autocomplete with BST
-------------------------------------

Simple autocomplete system using BST:

.. code-block:: python

   from sds.tree import BinarySearchTree

   class Autocomplete:
       """Autocomplete system using BST."""
       
       def __init__(self):
           self.bst = BinarySearchTree()
       
       def add_word(self, word):
           """Add word to dictionary."""
           self.bst.insert(word.lower())
       
       def add_words(self, words):
           """Add multiple words."""
           for word in words:
               self.add_word(word)
       
       def find_completions(self, prefix, max_results=10):
           """Find words starting with prefix."""
           prefix = prefix.lower()
           results = []
           
           # Get all words in sorted order
           for word in self.bst.inorder_traversal():
               if word.startswith(prefix):
                   results.append(word)
                   if len(results) >= max_results:
                       break
               elif word > prefix:  # Optimization: stop if past prefix
                   # Check if this word could start with prefix
                   if not word.startswith(prefix[:len(word)]):
                       break
           
           return results
       
       def contains(self, word):
           """Check if word exists."""
           return self.bst.search(word.lower())
   
   # Usage
   ac = Autocomplete()
   
   # Build dictionary
   words = [
       "apple", "application", "apply", "apricot",
       "banana", "band", "bandage",
       "cat", "catch", "category"
   ]
   ac.add_words(words)
   
   # Find completions
   print("Words starting with 'app':")
   print(ac.find_completions("app"))
   # Output: ['apple', 'application', 'apply']
   
   print("\nWords starting with 'ban':")
   print(ac.find_completions("ban"))
   # Output: ['banana', 'band', 'bandage']
   
   # Check existence
   print(f"\n'apple' in dictionary: {ac.contains('apple')}")
   # Output: True

Application 3: Range Query System
----------------------------------

Finding elements within a range using BST:

.. code-block:: python

   from sds.tree import BinarySearchTree

   class RangeQueryTree:
       """BST with range query support."""
       
       def __init__(self):
           self.bst = BinarySearchTree()
       
       def insert(self, value):
           """Insert value."""
           self.bst.insert(value)
       
       def range_query(self, low, high):
           """Find all values in range [low, high]."""
           results = []
           
           for value in self.bst.inorder_traversal():
               if value >= low and value <= high:
                   results.append(value)
               elif value > high:
                   break  # Optimization: stop early
           
           return results
       
       def count_in_range(self, low, high):
           """Count values in range."""
           return len(self.range_query(low, high))
       
       def closest_value(self, target):
           """Find value closest to target."""
           if self.bst.is_empty():
               return None
           
           closest = None
           min_diff = float('inf')
           
           for value in self.bst.inorder_traversal():
               diff = abs(value - target)
               if diff < min_diff:
                   min_diff = diff
                   closest = value
           
           return closest
   
   # Usage
   rq = RangeQueryTree()
   
   # Insert data
   data = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 65]
   for val in data:
       rq.insert(val)
   
   # Range queries
   print("Values in [30, 60]:", rq.range_query(30, 60))
   # Output: [30, 35, 40, 50, 60]
   
   print("Count in [20, 70]:", rq.count_in_range(20, 70))
   # Output: 9
   
   print("Closest to 55:", rq.closest_value(55))
   # Output: 50 or 60

Application 4: Binary Decision Tree
------------------------------------

Simple decision tree for classification:

.. code-block:: python

   from sds.tree.node import BinaryNode

   class DecisionTreeNode:
       """Node for binary decision tree."""
       def __init__(self, feature=None, threshold=None, 
                    left=None, right=None, value=None):
           self.feature = feature      # Feature to split on
           self.threshold = threshold  # Split threshold
           self.left = left           # Left subtree (<=)
           self.right = right         # Right subtree (>)
           self.value = value         # Prediction value (leaf)
       
       def is_leaf(self):
           """Check if this is a leaf node."""
           return self.value is not None
   
   class BinaryDecisionTree:
       """Simple binary decision tree classifier."""
       
       def __init__(self, max_depth=3):
           self.root = None
           self.max_depth = max_depth
       
       def fit(self, X, y, depth=0):
           """Build decision tree from data."""
           # Simplified: stop if pure or max depth
           if len(set(y)) == 1 or depth >= self.max_depth:
               return DecisionTreeNode(value=max(set(y), key=y.count))
           
           # Find best split (simplified)
           best_feature, best_threshold = self._find_best_split(X, y)
           
           # Split data
           left_mask = [X[i][best_feature] <= best_threshold for i in range(len(X))]
           right_mask = [not m for m in left_mask]
           
           X_left = [X[i] for i in range(len(X)) if left_mask[i]]
           y_left = [y[i] for i in range(len(y)) if left_mask[i]]
           X_right = [X[i] for i in range(len(X)) if right_mask[i]]
           y_right = [y[i] for i in range(len(y)) if right_mask[i]]
           
           # Build subtrees
           left = self.fit(X_left, y_left, depth + 1) if X_left else None
           right = self.fit(X_right, y_right, depth + 1) if X_right else None
           
           return DecisionTreeNode(
               feature=best_feature,
               threshold=best_threshold,
               left=left,
               right=right
           )
       
       def _find_best_split(self, X, y):
           """Find best feature and threshold to split on."""
           # Simplified: use first feature and median
           feature = 0
           values = [X[i][feature] for i in range(len(X))]
           threshold = sorted(values)[len(values) // 2]
           return feature, threshold
       
       def predict(self, node, sample):
           """Make prediction for a sample."""
           if node is None or node.is_leaf():
               return node.value if node else None
           
           if sample[node.feature] <= node.threshold:
               return self.predict(node.left, sample)
           else:
               return self.predict(node.right, sample)
   
   # Usage example
   # X = [[feature1, feature2, ...], ...]
   # y = [label1, label2, ...]

Best Practices
==============

Do's
----

✅ **Use BST for ordered data**

.. code-block:: python

   # When you need sorted access
   bst = BinarySearchTree()
   for val in data:
       bst.insert(val)
   
   # Get sorted sequence efficiently
   sorted_data = list(bst.inorder_traversal())

✅ **Check for empty before operations**

.. code-block:: python

   if not bst.is_empty():
       min_val = bst.find_min()
       max_val = bst.find_max()

✅ **Shuffle data before insertion for better balance**

.. code-block:: python

   import random
   
   data = list(range(1000))
   random.shuffle(data)
   
   bst = BinarySearchTree()
   for val in data:
       bst.insert(val)
   # Much better balanced than inserting sorted data

✅ **Use appropriate traversal for the task**

.. code-block:: python

   # Get sorted data → inorder
   sorted_values = list(bst.inorder_traversal())
   
   # Copy tree structure → preorder
   def copy_bst(original):
       new_tree = BinarySearchTree()
       for val in original.preorder_traversal():
           new_tree.insert(val)
       return new_tree
   
   # Delete tree → postorder (children before parent)
   def delete_nodes(tree):
       for val in tree.postorder_traversal():
           process_before_delete(val)

Don'ts
------

❌ **Don't insert sorted data into unbalanced BST**

.. code-block:: python

   # Bad: Creates degenerate tree (height = n)
   bst = BinarySearchTree()
   for i in range(1000):
       bst.insert(i)
   # Height: 999, Search: O(n)
   
   # Good: Use balanced tree or shuffle
   from sds.tree import AVLTree
   avl = AVLTree()
   for i in range(1000):
       avl.insert(i)
   # Height: ~10, Search: O(log n)

❌ **Don't assume BST is balanced**

.. code-block:: python

   # Bad: Assuming O(log n) always
   bst = BinarySearchTree()
   # ... insertions ...
   # Search might be O(n) if unbalanced!
   
   # Good: Check height or use balanced tree
   if bst.height() > 2 * math.log2(len(bst)):
       print("Warning: Tree is unbalanced")

❌ **Don't modify tree during traversal**

.. code-block:: python

   # Bad: Modifying during iteration
   for val in bst.inorder_traversal():
       if should_remove(val):
           bst.remove(val)  # Dangerous!
   
   # Good: Collect then modify
   to_remove = [val for val in bst.inorder_traversal() 
                if should_remove(val)]
   for val in to_remove:
       bst.remove(val)

Performance Tips
----------------

1. **Balance matters**

.. code-block:: python

   # Check tree balance
   import math
   
   def is_balanced(tree):
       n = len(tree)
       if n == 0:
           return True
       expected_height = math.ceil(math.log2(n + 1)) - 1
       actual_height = tree.height()
       return actual_height <= 2 * expected_height

2. **Batch operations**

.. code-block:: python

   # Build from sorted array (balanced)
   def build_balanced_bst(sorted_arr):
       if not sorted_arr:
           return None
       
       mid = len(sorted_arr) // 2
       root = BinaryNode(sorted_arr[mid])
       root.left = build_balanced_bst(sorted_arr[:mid])
       root.right = build_balanced_bst(sorted_arr[mid + 1:])
       return root

3. **Iterative vs Recursive**

.. code-block:: python

   # Iterative often faster for simple operations
   def search_iterative(root, key):
       current = root
       while current:
           if key == current.data:
               return True
           elif key < current.data:
               current = current.left
           else:
               current = current.right
       return False

Common Pitfalls
===============

1. **Forgetting BST property during manual construction**

.. code-block:: python

   # Wrong: Violates BST property
   root = BinaryNode(50)
   root.left = BinaryNode(60)   # 60 > 50, should be on right!
   root.right = BinaryNode(40)  # 40 < 50, should be on left!
   
   # Right: Use insert method
   bst = BinarySearchTree()
   bst.insert(50)
   bst.insert(60)
   bst.insert(40)

2. **Not handling edge cases**

.. code-block:: python

   # Handle empty tree
   if bst.is_empty():
       print("Tree is empty")
   else:
       min_val = bst.find_min()
   
   # Handle single node
   if len(bst) == 1:
       print("Single node tree")

3. **Memory leaks with large trees**

.. code-block:: python

   # Clear tree when done
   large_bst.clear()
   
   # Help garbage collector
   large_bst = None

4. **Stack overflow with deep trees**

.. code-block:: python

   import sys
   
   # Check and adjust recursion limit
   print(f"Recursion limit: {sys.getrecursionlimit()}")
   
   # For very deep trees
   if tree.height() > 900:
       sys.setrecursionlimit(tree.height() + 100)

Comparison: Binary Tree vs BST
===============================

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Aspect
     - Binary Tree
     - Binary Search Tree
   * - **Structure**
     - Any arrangement
     - Left < Parent < Right
   * - **Search**
     - O(n) - must check all
     - O(log n) avg - use ordering
   * - **Insert**
     - O(n) - find position
     - O(log n) avg - follow path
   * - **Inorder**
     - Random order
     - Sorted order
   * - **Use Case**
     - Expression trees, heaps
     - Searching, dictionaries
   * - **Balance**
     - Not required
     - Critical for performance

When to Use Each
----------------

**Use Binary Tree when:**
   - Representing hierarchical data without ordering
   - Building expression trees
   - Structure matters more than search speed

**Use BST when:**
   - Need fast search, insert, delete
   - Want sorted iteration
   - Implementing dictionaries or sets
   - Range queries are needed

**Use Balanced Tree (AVL/Red-Black) when:**
   - BST performance is critical
   - Can't control insertion order
   - Need guaranteed O(log n) operations

Further Reading
===============

* :doc:`/api/tree/binary` - Complete API reference
* :doc:`avl` - Always-balanced trees
* :doc:`red_black` - Balanced with less rotation
* :doc:`general` - Trees with more than 2 children

References
==========

.. [1] Cormen, T. H., et al. "Introduction to Algorithms", 3rd Edition, Chapter 12
.. [2] Knuth, D. E. "The Art of Computer Programming, Volume 1", Section 2.3
.. [3] Sedgewick, R., Wayne, K. "Algorithms", 4th Edition, Section 3.2
.. [4] Weiss, M. A. "Data Structures and Algorithm Analysis in C++", Chapter 4
