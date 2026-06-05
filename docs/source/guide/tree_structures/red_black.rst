.. _guide_tree_red_black:

====================
Red-Black Tree Guide
====================

.. currentmodule:: sds.tree

Introduction
============

A **Red-Black tree** is a self-balancing binary search tree where each node has an additional color attribute (RED or BLACK). Through specific color-based rules and rotations, Red-Black trees maintain approximate balance, guaranteeing O(log n) operations while requiring fewer rotations than AVL trees during insertions and deletions.

.. mermaid::

   graph TB
       subgraph "Red-Black Tree Example"
       A[13<br/>BLACK] --> B[8<br/>RED]
       A --> C[17<br/>RED]
       B --> D[1<br/>BLACK]
       B --> E[11<br/>BLACK]
       C --> F[15<br/>BLACK]
       C --> G[25<br/>BLACK]
       G --> H[22<br/>RED]
       G --> I[27<br/>RED]
       end
       
       style A fill:#2c3e50,color:#fff
       style B fill:#e74c3c,color:#fff
       style C fill:#e74c3c,color:#fff
       style D fill:#2c3e50,color:#fff
       style E fill:#2c3e50,color:#fff
       style F fill:#2c3e50,color:#fff
       style G fill:#2c3e50,color:#fff
       style H fill:#e74c3c,color:#fff
       style I fill:#e74c3c,color:#fff

.. note::
   
   Red-Black trees are preferred over AVL trees when insertions and deletions
   are more frequent than searches, as they require fewer rotations to maintain
   balance while still guaranteeing logarithmic height.

Mathematical Model
==================

Formal Definition
-----------------

Red-Black Properties
^^^^^^^^^^^^^^^^^^^^

A Red-Black tree is a BST that satisfies five properties:

1. **Color Property**: Every node is either RED or BLACK

   .. math::

      \forall node \in T: color(node) \in \{\text{RED}, \text{BLACK}\}

2. **Root Property**: The root is BLACK

   .. math::

      color(root) = \text{BLACK}

3. **Leaf Property**: All leaves (NIL nodes) are BLACK

   .. math::

      color(NIL) = \text{BLACK}

4. **Red Property**: If a node is RED, both children are BLACK

   .. math::

      color(node) = \text{RED} \implies color(node.left) = color(node.right) = \text{BLACK}

5. **Black-Height Property**: All paths from a node to descendant leaves contain the same number of BLACK nodes

   .. math::

      \forall node \in T: bh(\text{all paths from node to leaves}) = \text{constant}

Black-Height Definition
^^^^^^^^^^^^^^^^^^^^^^^

The **black-height** :math:`bh(node)` of a node is the number of BLACK nodes on any path from (but not including) the node to a leaf:

.. math::

   bh(node) = \begin{cases}
   0 & \text{if } node = NIL \\
   bh(child) & \text{if } color(node) = \text{RED} \\
   bh(child) + 1 & \text{if } color(node) = \text{BLACK}
   \end{cases}

Tree Properties
---------------

Height Bounds
^^^^^^^^^^^^^

For a Red-Black tree with :math:`n` internal nodes and black-height :math:`bh`:

**Minimum nodes for black-height** :math:`bh`:

.. math::

   n \geq 2^{bh} - 1

**Maximum height**:

.. math::

   h \leq 2\log_2(n + 1)

This is at most twice the height of a perfectly balanced tree, making Red-Black trees "approximately balanced."

**Proof sketch**:
- Any path has at least :math:`bh` BLACK nodes
- At most half the nodes can be RED (Red Property)
- Therefore: :math:`h \leq 2 \cdot bh \leq 2\log_2(n + 1)`

Rotation Mathematics
^^^^^^^^^^^^^^^^^^^^

Red-Black trees use the same rotations as AVL trees but with color adjustments:

**Left Rotation with Recoloring**:

.. code-block:: text

    z(c1)              y(c2)
     / \                / \
    A   y(c2)   →   z(c1)  C
       / \            / \
      B   C          A   B

Colors :math:`c1, c2` are adjusted based on the violation being fixed.

Algorithmic Model
=================

Abstract Data Type
------------------

.. code-block:: text

   ADT RedBlackTree:
       Data:
           - root: RedBlackNode with color
           - NIL: sentinel BLACK node
           - size: number of nodes
       
       RedBlackNode:
           - data: stored value
           - color: RED or BLACK
           - left: RedBlackNode or NIL
           - right: RedBlackNode or NIL
           - parent: RedBlackNode or NIL
       
       Operations:
           - RedBlackTree(): create empty tree
           - insert(item): add item with rebalancing
           - remove(item): remove item with rebalancing
           - search(item): find item (O(log n))
           - height(): return tree height
       
       Invariants:
           - All 5 Red-Black properties maintained
           - BST property maintained

Insertion Algorithm
-------------------

Basic Insertion
^^^^^^^^^^^^^^^

.. code-block:: text

   Algorithm: RB_INSERT(tree, key)
   Input: RedBlackTree tree, value key
   Output: Updated tree maintaining RB properties
   
   1. // Standard BST insertion
   2. new_node ← Node(key, color=RED)
   3. new_node.left ← NIL
   4. new_node.right ← NIL
   5. 
   6. parent ← NIL
   7. current ← tree.root
   8. 
   9. while current ≠ NIL do
   10.    parent ← current
   11.    if key < current.data then
   12.        current ← current.left
   13.    else
   14.        current ← current.right
   15.    end if
   16. end while
   17. 
   18. new_node.parent ← parent
   19. 
   20. if parent = NIL then
   21.    tree.root ← new_node  // Tree was empty
   22. else if key < parent.data then
   23.    parent.left ← new_node
   24. else
   25.    parent.right ← new_node
   26. end if
   27. 
   28. // Fix Red-Black properties
   29. RB_INSERT_FIXUP(tree, new_node)

**Time complexity**: O(log n)

Insertion Fixup
^^^^^^^^^^^^^^^

After standard BST insertion, fix violations:

.. code-block:: text

   Algorithm: RB_INSERT_FIXUP(tree, node)
   Input: Tree tree, newly inserted RED node
   Output: Tree with RB properties restored
   
   1. while node.parent.color = RED do
   2.    if node.parent = node.parent.parent.left then
   3.        uncle ← node.parent.parent.right
   4.        
   5.        if uncle.color = RED then
   6.            // Case 1: Uncle is RED - recolor
   7.            node.parent.color ← BLACK
   8.            uncle.color ← BLACK
   9.            node.parent.parent.color ← RED
   10.           node ← node.parent.parent
   11.       else
   12.           if node = node.parent.right then
   13.               // Case 2: Uncle BLACK, node is right child
   14.               node ← node.parent
   15.               LEFT_ROTATE(tree, node)
   16.           end if
   17.           // Case 3: Uncle BLACK, node is left child
   18.           node.parent.color ← BLACK
   19.           node.parent.parent.color ← RED
   20.           RIGHT_ROTATE(tree, node.parent.parent)
   21.       end if
   22.   else
   23.       // Symmetric cases (parent is right child)
   24.       // ... mirror image of above
   25.   end if
   26. end while
   27. 
   28. tree.root.color ← BLACK  // Maintain root property

**Cases explained**:

1. **Uncle RED**: Recolor parent, uncle, and grandparent
2. **Uncle BLACK, zig-zag**: Rotate to convert to case 3
3. **Uncle BLACK, zig-zig**: Rotate and recolor

Deletion Algorithm
------------------

Deletion is more complex than insertion:

.. code-block:: text

   Algorithm: RB_DELETE(tree, key)
   Input: Tree tree, key to delete
   Output: Updated tree
   
   1. // Find node to delete (standard BST deletion logic)
   2. node_to_delete ← SEARCH(tree, key)
   3. 
   4. // Determine node to actually remove
   5. if node_to_delete.left = NIL or node_to_delete.right = NIL then
   6.     y ← node_to_delete
   7. else
   8.     y ← SUCCESSOR(node_to_delete)
   9. end if
   10. 
   11. // y has at most one child
   12. if y.left ≠ NIL then
   13.     x ← y.left
   14. else
   15.     x ← y.right
   16. end if
   17. 
   18. x.parent ← y.parent
   19. 
   20. if y.parent = NIL then
   21.     tree.root ← x
   22. else if y = y.parent.left then
   23.     y.parent.left ← x
   24. else
   25.     y.parent.right ← x
   26. end if
   27. 
   28. if y ≠ node_to_delete then
   29.     node_to_delete.data ← y.data
   30. end if
   31. 
   32. if y.color = BLACK then
   33.     RB_DELETE_FIXUP(tree, x)
   34. end if

**Time complexity**: O(log n)
**Rotations per delete**: At most 3

Complexity Analysis
-------------------

Time Complexity
^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 35 20 20 25

   * - Operation
     - Best
     - Average
     - Worst
   * - **Insert**
     - O(log n)
     - O(log n)
     - O(log n)
   * - **Delete**
     - O(log n)
     - O(log n)
     - O(log n)
   * - **Search**
     - O(1)
     - O(log n)
     - O(log n)
   * - **Find Min/Max**
     - O(log n)
     - O(log n)
     - O(log n)
   * - **Height**
     - O(n)
     - O(n)
     - O(n)
   * - **Traversal**
     - O(n)
     - O(n)
     - O(n)

**Guaranteed O(log n) for all operations!**

Rotation Count Comparison
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Operation
     - AVL Tree
     - Red-Black Tree
   * - **Insert**
     - 2 rotations max
     - 2 rotations max
   * - **Delete**
     - O(log n) rotations
     - 3 rotations max
   * - **Recoloring**
     - N/A
     - O(log n) per operation

Red-Black trees perform fewer rotations on average, making them faster for insertion/deletion-heavy workloads.

Space Complexity
^^^^^^^^^^^^^^^^

* **Tree storage**: O(n) for n nodes
* **Color storage**: O(n) - one bit per node
* **NIL sentinel**: O(1) shared across all leaves
* **Recursion stack**: O(log n) - bounded by height

Practical Usage
===============

Installation and Import
-----------------------

.. code-block:: python

   # Install
   pip install sds-tools
   
   # Import
   from sds.tree import RedBlackTree

Basic Operations
----------------

Creating and Populating
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.tree import RedBlackTree

   # Create Red-Black tree
   rbt = RedBlackTree()
   
   # Insert values
   for val in [10, 20, 30, 40, 50, 25]:
       rbt.insert(val)
   
   print(f"Size: {len(rbt)}")        # Output: 6
   print(f"Height: {rbt.height()}")  # Output: 3 or less
   
   # Tree is automatically balanced!

Automatic Balancing
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Even inserting sorted data stays balanced
   rbt = RedBlackTree()
   for i in range(1, 8):
       rbt.insert(i)
   
   # Height is logarithmic (slightly taller than AVL)
   print(rbt.height())  # Output: 4 (vs AVL's 2)
   
   # But requires fewer rotations during insertion!

Searching
^^^^^^^^^

.. code-block:: python

   rbt = RedBlackTree()
   for val in [50, 30, 70, 20, 40, 60, 80]:
       rbt.insert(val)
   
   # O(log n) search guaranteed
   print(rbt.search(40))   # Output: True
   print(40 in rbt)        # Output: True
   print(rbt.search(25))   # Output: False

Deletion
^^^^^^^^

.. code-block:: python

   # Remove maintains balance
   rbt.remove(30)
   print(list(rbt))
   # Output: [20, 40, 50, 60, 70, 80]
   
   # Height still logarithmic
   print(rbt.height())  # Still O(log n)

Traversals
^^^^^^^^^^

.. code-block:: python

   rbt = RedBlackTree()
   for val in [50, 30, 70, 20, 40, 60, 80]:
       rbt.insert(val)
   
   # Inorder gives sorted sequence
   print(list(rbt.inorder_traversal()))
   # Output: [20, 30, 40, 50, 60, 70, 80]
   
   # Level-order
   print(list(rbt.level_order_traversal()))
   # Output: [50, 30, 70, 20, 40, 60, 80]

Real-World Applications
=======================

Application 1: In-Memory Database Index
----------------------------------------

Red-Black trees in production databases:

.. code-block:: python

   from sds.tree import RedBlackTree

   class FastDatabaseIndex:
       """High-performance index with frequent updates."""
       
       def __init__(self):
           self.index = RedBlackTree()
           self.records = {}
       
       def insert_record(self, key, record):
           """Insert with fewer rotations than AVL."""
           self.index.insert(key)
           self.records[key] = record
       
       def bulk_update(self, updates):
           """Efficiently handle many updates."""
           # Red-Black trees excel here due to fewer rotations
           for key, record in updates:
               if self.index.search(key):
                   self.remove_record(key)
               self.insert_record(key, record)
       
       def find_record(self, key):
           """Find record - O(log n)."""
           if self.index.search(key):
               return self.records[key]
           return None
       
       def remove_record(self, key):
           """Delete with minimal rotations."""
           if self.index.search(key):
               self.index.remove(key)
               del self.records[key]
               return True
           return False
   
   # Usage
   db = FastDatabaseIndex()
   
   # Frequent insertions and deletions
   for i in range(10000):
       db.insert_record(i, {"data": f"record_{i}"})
   
   # Update half the records (RB-Tree stays efficient)
   updates = [(i, {"data": f"updated_{i}"}) for i in range(0, 10000, 2)]
   db.bulk_update(updates)

Application 2: Task Scheduler
------------------------------

Real-time task scheduling:

.. code-block:: python

   from sds.tree import RedBlackTree
   import time

   class TaskScheduler:
       """Schedule tasks with dynamic priorities."""
       
       def __init__(self):
           # Red-Black for frequent priority changes
           self.tasks = RedBlackTree()
           self.task_data = {}
       
       def schedule(self, task_id, priority, callback):
           """Schedule task with priority."""
           # Composite key: (priority, task_id)
           key = (priority, task_id)
           self.tasks.insert(key)
           self.task_data[key] = callback
       
       def reschedule(self, task_id, old_priority, new_priority):
           """Change task priority (common operation)."""
           old_key = (old_priority, task_id)
           new_key = (new_priority, task_id)
           
           if self.tasks.search(old_key):
               callback = self.task_data[old_key]
               self.tasks.remove(old_key)
               del self.task_data[old_key]
               
               self.tasks.insert(new_key)
               self.task_data[new_key] = callback
       
       def get_next_task(self):
           """Get highest priority task."""
           if self.tasks.is_empty():
               return None
           
           # Find minimum priority (leftmost)
           for key in self.tasks.inorder_traversal():
               callback = self.task_data[key]
               self.tasks.remove(key)
               del self.task_data[key]
               return callback
       
       def cancel_task(self, task_id, priority):
           """Cancel scheduled task."""
           key = (priority, task_id)
           if self.tasks.search(key):
               self.tasks.remove(key)
               del self.task_data[key]
   
   # Usage
   scheduler = TaskScheduler()
   
   def task1():
       print("High priority task")
   
   def task2():
       print("Low priority task")
   
   scheduler.schedule("task1", 1, task1)
   scheduler.schedule("task2", 10, task2)
   
   # Reschedule frequently (Red-Black excels here)
   scheduler.reschedule("task2", 10, 2)
   
   # Process tasks
   while task := scheduler.get_next_task():
       task()

Comparison: AVL vs Red-Black
=============================

Performance Characteristics
---------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Aspect
     - AVL Tree
     - Red-Black Tree
   * - **Height**
     - h ≤ 1.44 log n
     - h ≤ 2 log n
   * - **Search Speed**
     - Slightly faster
     - Slightly slower
   * - **Insert Rotations**
     - Up to 2
     - Up to 2
   * - **Delete Rotations**
     - Up to O(log n)
     - Up to 3
   * - **Rebalancing Cost**
     - Higher
     - Lower
   * - **Memory**
     - Height per node
     - 1 bit color per node

When to Use Each
----------------

**Use AVL Tree when:**
   - Searches greatly outnumber updates (90%+ reads)
   - Need the absolute minimum height
   - Search speed is critical
   - Memory for height storage is acceptable

**Use Red-Black Tree when:**
   - Frequent insertions and deletions (balanced workload)
   - Updates matter more than searches
   - Need stable, predictable performance
   - Minimal rebalancing overhead required

**Real-world examples:**
   - AVL: Read-heavy caches, static databases
   - Red-Black: Linux kernel, Java TreeMap, C++ std::map

Best Practices
==============

Do's
----

✅ **Use Red-Black for update-heavy workloads**

.. code-block:: python

   # Perfect for frequent modifications
   rbt = RedBlackTree()
   
   # Many insertions and deletions
   for i in range(10000):
       rbt.insert(i)
   
   for i in range(0, 10000, 2):
       rbt.remove(i)
   # Fewer rotations than AVL!

✅ **Trust the balancing guarantees**

.. code-block:: python

   # No need to worry about insertion order
   rbt = RedBlackTree()
   for val in sorted_data:  # Even sorted!
       rbt.insert(val)
   # Still balanced

✅ **Use for general-purpose balanced trees**

.. code-block:: python

   # Good default choice
   rbt = RedBlackTree()
   # Balanced performance across all operations

Don'ts
------

❌ **Don't use if searches dominate**

.. code-block:: python

   # If 95% searches, use AVL instead
   # Red-Black is slightly taller
   # Example: static lookup tables

❌ **Don't implement custom color management**

.. code-block:: python

   # Bad: Red-Black handles colors automatically
   # Never manually modify node colors

❌ **Don't forget about simpler alternatives**

.. code-block:: python

   # For small datasets, simple BST may suffice
   # For very large datasets, consider B-Trees

Further Reading
===============

* :doc:`/api/tree/balanced` - Complete API reference
* :doc:`avl` - Compare with AVL trees
* :doc:`binary` - BST fundamentals

References
==========

.. [WikiRB] Wikipedia contributors. "Red-Black Tree". Wikipedia.
   https://en.wikipedia.org/wiki/Red%E2%80%93black_tree
   
   Comprehensive overview of Red-Black tree properties and algorithms.

.. [CLRS] Cormen, T. H., et al. "Introduction to Algorithms", 3rd Edition, Chapter 13
   
   The definitive academic reference for Red-Black trees.

.. [Sedgewick] Sedgewick, R. "Left-Leaning Red-Black Trees", 2008
   https://www.cs.princeton.edu/~rs/talks/LLRB/LLRB.pdf
   
   Simplified Red-Black tree variant with cleaner implementation.

.. [VisuAlgoRB] Halim, S. "Red-Black Tree Visualization". VisuAlgo.
   https://visualgo.net/en/bst
   
   Interactive visualization of Red-Black tree operations.

.. [USFCARB] Galles, D. "Red-Black Tree Visualization". USFCA.
   https://www.cs.usfca.edu/~galles/visualization/RedBlack.html
   
   Step-by-step animated Red-Black tree operations.

.. [Guibas] Guibas, L. J., Sedgewick, R. "A Dichromatic Framework for Balanced Trees", 1978
   
   Original paper introducing the symmetric binary B-tree (Red-Black tree).
