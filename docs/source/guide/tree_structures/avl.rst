.. _guide_tree_avl:

==============
AVL Tree Guide
==============

.. currentmodule:: sds.tree

Introduction
============

An **AVL tree** is a self-balancing binary search tree where the heights of the two child
subtrees of any node differ by at most one. Named after inventors Adelson-Velsky and Landis,
AVL trees guarantee O(log n) time for search, insertion, and deletion operations by
automatically rebalancing through rotations.

.. mermaid::

   graph TB
       subgraph "Balanced AVL Tree"
       A[50<br/>h=2] --> B[30<br/>h=1]
       A --> C[70<br/>h=1]
       B --> D[20<br/>h=0]
       B --> E[40<br/>h=0]
       C --> F[60<br/>h=0]
       C --> G[80<br/>h=0]
       end
       
       subgraph "Balance Factors"
       H["BF = h(left) - h(right)"]
       I["Valid: -1, 0, +1"]
       end
       
       style A fill:#e74c3c,color:#fff
       style B fill:#3498db,color:#fff
       style C fill:#3498db,color:#fff

.. note::
   
   AVL trees are ideal when searches greatly outnumber insertions/deletions,
   as they maintain the strictest balance among self-balancing trees.

Mathematical Model
==================

Formal Definition
-----------------

AVL Tree Property
^^^^^^^^^^^^^^^^^

An AVL tree is a BST that satisfies the **AVL balance property**:

.. math::

   \forall node \in T: |height(node.left) - height(node.right)| \leq 1

where the **balance factor** is defined as:

.. math::

   BF(node) = height(node.left) - height(node.right)

Valid balance factors: :math:`BF \in \{-1, 0, +1\}`

Height Definition
^^^^^^^^^^^^^^^^^

**Height of a node**:

.. math::

   h(node) = \begin{cases}
   -1 & \text{if } node = null \\
   1 + \max(h(node.left), h(node.right)) & \text{otherwise}
   \end{cases}

**Height stored at each node** for O(1) access.

Tree Properties
---------------

Height Bounds
^^^^^^^^^^^^^

For an AVL tree with :math:`n` nodes:

**Minimum nodes for height** :math:`h`:

.. math::

   N(h) = N(h-1) + N(h-2) + 1

This is similar to Fibonacci: :math:`N(h) \approx \phi^{h+2}/\sqrt{5}` where :math:`\phi = \frac{1+\sqrt{5}}{2}`

**Maximum height for** :math:`n` **nodes**:

.. math::

   h_{max} \leq 1.44 \log_2(n+2) - 0.328

**Practical bound**:

.. math::

   h \approx 1.44 \log_2 n

This is only 44% taller than a perfect binary tree!

Balance Factor Properties
^^^^^^^^^^^^^^^^^^^^^^^^^^

**After insertion**:
   - Only ancestors of inserted node may become unbalanced
   - At most one rotation needed to restore balance

**After deletion**:
   - Multiple rotations may be needed (up to O(log n))
   - Rebalancing proceeds from deleted node to root

Rotation Mathematics
^^^^^^^^^^^^^^^^^^^^

**Right rotation** (LL case):

.. math::

   \begin{array}{c}
   z \\
   \downarrow \\
   y
   \end{array}
   \quad
   \text{where } y = z.left

**Left rotation** (RR case):

.. math::

   \begin{array}{c}
   z \\
   \downarrow \\
   y
   \end{array}
   \quad
   \text{where } y = z.right

**Height change after rotation**: At most decreases by 1

Tree Invariants
---------------

1. **BST property**: Left < Parent < Right (all nodes)

2. **Balance property**: :math:`|BF(node)| \leq 1` (all nodes)

3. **Height accuracy**: Stored height matches actual height

4. **Subtree property**: All subtrees are valid AVL trees

Algorithmic Model
=================

Abstract Data Type
------------------

.. code-block:: text

   ADT AVLTree:
       Data:
           - root: AVLNode with height
           - size: number of nodes
       
       AVLNode:
           - data: stored value
           - left: AVLNode or null
           - right: AVLNode or null
           - height: integer (subtree height)
       
       Operations:
           - AVLTree(): create empty tree
           - insert(item): add item with rebalancing
           - remove(item): remove item with rebalancing
           - search(item): find item (O(log n))
           - height(): return tree height (O(1))
       
       Invariants:
           - BST property maintained
           - |BF(node)| ≤ 1 for all nodes
           - height(node) = 1 + max(h(left), h(right))

Rotation Algorithms
-------------------

Right Rotation (LL Case)
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   Algorithm: ROTATE_RIGHT(z)
   Input: Node z (root of subtree to rotate)
   Output: New root after rotation
   
   1. y ← z.left
   2. T2 ← y.right
   3. 
   4. // Perform rotation
   5. y.right ← z
   6. z.left ← T2
   7. 
   8. // Update heights
   9. z.height ← 1 + max(height(z.left), height(z.right))
   10. y.height ← 1 + max(height(y.left), height(y.right))
   11. 
   12. return y

**Visual**:

.. code-block:: text

        z                  y
       / \                / \
      y   C    →         A   z
     / \                    / \
    A   B                  B   C

**Time complexity**: O(1)

Left Rotation (RR Case)
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   Algorithm: ROTATE_LEFT(z)
   Input: Node z (root of subtree to rotate)
   Output: New root after rotation
   
   1. y ← z.right
   2. T2 ← y.left
   3. 
   4. // Perform rotation
   5. y.left ← z
   6. z.right ← T2
   7. 
   8. // Update heights
   9. z.height ← 1 + max(height(z.left), height(z.right))
   10. y.height ← 1 + max(height(y.left), height(y.right))
   11. 
   12. return y

**Visual**:

.. code-block:: text

      z                    y
     / \                  / \
    A   y      →         z   C
       / \              / \
      B   C            A   B

Left-Right Rotation (LR Case)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   Algorithm: ROTATE_LEFT_RIGHT(z)
   Input: Node z (unbalanced node)
   Output: New root after double rotation
   
   1. z.left ← ROTATE_LEFT(z.left)
   2. return ROTATE_RIGHT(z)

**Visual**:

.. code-block:: text

      z              z              x
     / \            / \            / \
    y   C    →     x   C    →     y   z
     \            /                   / \
      x          y                   B   C
       \          \
        B          B

Right-Left Rotation (RL Case)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   Algorithm: ROTATE_RIGHT_LEFT(z)
   Input: Node z (unbalanced node)
   Output: New root after double rotation
   
   1. z.right ← ROTATE_RIGHT(z.right)
   2. return ROTATE_LEFT(z)

**Visual**:

.. code-block:: text

    z                z                x
   / \              / \              / \
  A   y      →     A   x      →     z   y
     /                  \          / \
    x                    y        A   B
   /                    /
  B                    B

Insertion Algorithm
-------------------

.. code-block:: text

   Algorithm: AVL_INSERT(node, key)
   Input: Node node, value key
   Output: New root after insertion and rebalancing
   
   1. // Standard BST insertion
   2. if node = null then
   3.     return AVLNode(key, height=0)
   4. end if
   5. 
   6. if key < node.data then
   7.     node.left ← AVL_INSERT(node.left, key)
   8. else
   9.     node.right ← AVL_INSERT(node.right, key)
   10. end if
   11. 
   12. // Update height
   13. node.height ← 1 + max(height(node.left), height(node.right))
   14. 
   15. // Get balance factor
   16. balance ← height(node.left) - height(node.right)
   17. 
   18. // Left-Left Case
   19. if balance > 1 and key < node.left.data then
   20.     return ROTATE_RIGHT(node)
   21. end if
   22. 
   23. // Right-Right Case
   24. if balance < -1 and key >= node.right.data then
   25.     return ROTATE_LEFT(node)
   26. end if
   27. 
   28. // Left-Right Case
   29. if balance > 1 and key >= node.left.data then
   30.     node.left ← ROTATE_LEFT(node.left)
   31.     return ROTATE_RIGHT(node)
   32. end if
   33. 
   34. // Right-Left Case
   35. if balance < -1 and key < node.right.data then
   36.     node.right ← ROTATE_RIGHT(node.right)
   37.     return ROTATE_LEFT(node)
   38. end if
   39. 
   40. return node

**Time complexity**: O(log n)
**Rotations per insert**: At most 2

Deletion Algorithm
------------------

.. code-block:: text

   Algorithm: AVL_DELETE(node, key)
   Input: Node node, value key
   Output: New root after deletion and rebalancing
   
   1. // Standard BST deletion
   2. if node = null then
   3.     return null
   4. end if
   5. 
   6. if key < node.data then
   7.     node.left ← AVL_DELETE(node.left, key)
   8. else if key > node.data then
   9.     node.right ← AVL_DELETE(node.right, key)
   10. else
   11.     // Node found - delete it
   12.     if node.left = null then
   13.         return node.right
   14.     else if node.right = null then
   15.         return node.left
   16.     else
   17.         // Two children: get successor
   18.         successor ← FIND_MIN(node.right)
   19.         node.data ← successor.data
   20.         node.right ← AVL_DELETE(node.right, successor.data)
   21.     end if
   22. end if
   23. 
   24. // Update height
   25. node.height ← 1 + max(height(node.left), height(node.right))
   26. 
   27. // Get balance
   28. balance ← height(node.left) - height(node.right)
   29. 
   30. // Rebalance (4 cases, similar to insertion)
   31. // Left-Left Case
   32. if balance > 1 and BF(node.left) >= 0 then
   33.     return ROTATE_RIGHT(node)
   34. end if
   35. 
   36. // Left-Right Case
   37. if balance > 1 and BF(node.left) < 0 then
   38.     node.left ← ROTATE_LEFT(node.left)
   39.     return ROTATE_RIGHT(node)
   40. end if
   41. 
   42. // Right-Right Case
   43. if balance < -1 and BF(node.right) <= 0 then
   44.     return ROTATE_LEFT(node)
   45. end if
   46. 
   47. // Right-Left Case
   48. if balance < -1 and BF(node.right) > 0 then
   49.     node.right ← ROTATE_RIGHT(node.right)
   50.     return ROTATE_LEFT(node)
   51. end if
   52. 
   53. return node

**Time complexity**: O(log n)
**Rotations per delete**: Up to O(log n)

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
     - O(1)
     - O(1)
     - O(1)
   * - **Traversal**
     - O(n)
     - O(n)
     - O(n)

**All operations are O(log n) guaranteed!**

Space Complexity
^^^^^^^^^^^^^^^^

* **Tree storage**: O(n) for n nodes
* **Height storage**: O(n) - one integer per node
* **Recursion stack**: O(log n) - bounded by height

Practical Usage
===============

Installation and Import
-----------------------

.. code-block:: python

   # Install
   pip install sds-tools
   
   # Import
   from sds.tree import AVLTree

Basic Operations
----------------

Creating and Populating
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.tree import AVLTree

   # Create AVL tree
   avl = AVLTree()
   
   # Insert values
   for val in [10, 20, 30, 40, 50, 25]:
       avl.insert(val)
   
   print(f"Size: {len(avl)}")        # Output: 6
   print(f"Height: {avl.height()}")  # Output: 2
   
   # Tree is automatically balanced!

Guaranteed Balance
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Even inserting sorted data stays balanced
   avl = AVLTree()
   for i in range(1, 8):
       avl.insert(i)
   
   # Height is logarithmic
   print(avl.height())  # Output: 2 (not 6!)
   
   # Compare to BST
   from sds.tree import BinarySearchTree
   bst = BinarySearchTree()
   for i in range(1, 8):
       bst.insert(i)
   print(bst.height())  # Output: 6 (degenerate!)

Searching
^^^^^^^^^

.. code-block:: python

   avl = AVLTree()
   for val in [50, 30, 70, 20, 40, 60, 80]:
       avl.insert(val)
   
   # O(log n) search guaranteed
   print(avl.search(40))   # Output: True
   print(40 in avl)        # Output: True
   print(avl.search(25))   # Output: False

Deletion
^^^^^^^^

.. code-block:: python

   # Remove maintains balance
   avl.remove(30)
   print(list(avl))
   # Output: [20, 40, 50, 60, 70, 80]
   
   # Height still optimal
   print(avl.height())  # Still O(log n)

Traversals
^^^^^^^^^^

.. code-block:: python

   avl = AVLTree()
   for val in [50, 30, 70, 20, 40, 60, 80]:
       avl.insert(val)
   
   # Inorder gives sorted sequence
   print(list(avl.inorder_traversal()))
   # Output: [20, 30, 40, 50, 60, 70, 80]
   
   # Preorder
   print(list(avl.preorder_traversal()))
   # Output: [50, 30, 20, 40, 70, 60, 80]
   
   # Level-order
   print(list(avl.level_order_traversal()))
   # Output: [50, 30, 70, 20, 40, 60, 80]

Real-World Applications
=======================

Application 1: Database Index
------------------------------

High-performance database indexing:

.. code-block:: python

   from sds.tree import AVLTree

   class DatabaseIndex:
       """Fast database index using AVL tree."""
       
       def __init__(self):
           self.index = AVLTree()
           self.records = {}
       
       def insert_record(self, key, record):
           """Insert record with O(log n) time."""
           self.index.insert(key)
           self.records[key] = record
       
       def find_record(self, key):
           """Find record by key - O(log n)."""
           if self.index.search(key):
               return self.records[key]
           return None
       
       def delete_record(self, key):
           """Delete record - O(log n)."""
           if self.index.search(key):
               self.index.remove(key)
               del self.records[key]
               return True
           return False
       
       def range_query(self, low, high):
           """Find all records in range [low, high]."""
           results = []
           for key in self.index.inorder_traversal():
               if low <= key <= high:
                   results.append((key, self.records[key]))
               elif key > high:
                   break
           return results
       
       def count_range(self, low, high):
           """Count records in range."""
           count = 0
           for key in self.index.inorder_traversal():
               if low <= key <= high:
                   count += 1
               elif key > high:
                   break
           return count
   
   # Usage
   db = DatabaseIndex()
   
   # Insert million records efficiently
   for i in range(1000000):
       db.insert_record(i, {"data": f"record_{i}"})
   
   # Fast lookup (guaranteed O(log n))
   record = db.find_record(500000)
   
   # Range query
   results = db.range_query(100, 200)
   print(f"Found {len(results)} records in range")

Application 2: Memory Management
---------------------------------

Tracking free memory blocks:

.. code-block:: python

   from sds.tree import AVLTree

   class MemoryManager:
       """Manage free memory blocks using AVL tree."""
       
       def __init__(self, total_memory):
           self.free_blocks = AVLTree()
           # Initial: one big free block
           self.free_blocks.insert((0, total_memory))
       
       def allocate(self, size):
           """Allocate memory block of given size."""
           # Find smallest sufficient block (best-fit)
           best_block = None
           
           for start, block_size in self.free_blocks.inorder_traversal():
               if block_size >= size:
                   best_block = (start, block_size)
                   break
           
           if best_block is None:
               return None  # Out of memory
           
           start, block_size = best_block
           self.free_blocks.remove((start, block_size))
           
           # Split block if needed
           if block_size > size:
               # Return leftover to free list
               new_start = start + size
               new_size = block_size - size
               self.free_blocks.insert((new_start, new_size))
           
           return start
       
       def deallocate(self, start, size):
           """Free memory block."""
           # Add to free list
           self.free_blocks.insert((start, size))
           
           # TODO: Coalesce adjacent blocks
       
       def get_largest_free_block(self):
           """Get size of largest free block."""
           max_size = 0
           for start, size in self.free_blocks.inorder_traversal():
               max_size = max(max_size, size)
           return max_size
   
   # Usage
   mm = MemoryManager(1024)  # 1KB memory
   
   # Allocate blocks
   ptr1 = mm.allocate(100)
   ptr2 = mm.allocate(200)
   ptr3 = mm.allocate(150)
   
   # Free a block
   mm.deallocate(ptr2, 200)
   
   # Check available memory
   print(f"Largest free: {mm.get_largest_free_block()}")

Application 3: Autocomplete System
-----------------------------------

Fast prefix-based word suggestions:

.. code-block:: python

   from sds.tree import AVLTree

   class Autocomplete:
       """Autocomplete system using AVL tree."""
       
       def __init__(self):
           self.words = AVLTree()
           self.frequencies = {}  # word -> frequency
       
       def add_word(self, word, frequency=1):
           """Add word with frequency."""
           word = word.lower()
           self.words.insert(word)
           self.frequencies[word] = self.frequencies.get(word, 0) + frequency
       
       def add_corpus(self, text):
           """Add words from text."""
           import re
           words = re.findall(r'\w+', text.lower())
           for word in words:
               self.add_word(word)
       
       def get_completions(self, prefix, max_results=10):
           """Get word completions for prefix."""
           prefix = prefix.lower()
           results = []
           
           for word in self.words.inorder_traversal():
               if word.startswith(prefix):
                   results.append((word, self.frequencies[word]))
                   if len(results) >= max_results:
                       break
               elif word > prefix:
                   break
           
           # Sort by frequency (descending)
           results.sort(key=lambda x: x[1], reverse=True)
           return [word for word, freq in results]
       
       def search_exact(self, word):
           """Check if exact word exists."""
           return self.words.search(word.lower())
   
   # Usage
   ac = Autocomplete()
   
   # Add dictionary
   corpus = """
   apple application apply appreciate
   banana band bandage
   cat catch category cathedral
   """
   ac.add_corpus(corpus)
   
   # Get suggestions
   suggestions = ac.get_completions("app")
   print(f"Suggestions for 'app': {suggestions}")
   
   # Check spelling
   print(f"'apple' exists: {ac.search_exact('apple')}")

Application 4: Event Scheduler
-------------------------------

Time-based event management:

.. code-block:: python

   from sds.tree import AVLTree
   import time

   class EventScheduler:
       """Schedule events by timestamp using AVL tree."""
       
       def __init__(self):
           self.events = AVLTree()
           self.event_data = {}
       
       def schedule(self, timestamp, event_id, data):
           """Schedule an event."""
           self.events.insert(timestamp)
           self.event_data[timestamp] = (event_id, data)
       
       def cancel(self, timestamp):
           """Cancel an event."""
           if self.events.search(timestamp):
               self.events.remove(timestamp)
               del self.event_data[timestamp]
               return True
           return False
       
       def get_next_event(self, current_time):
           """Get next event after current time."""
           for ts in self.events.inorder_traversal():
               if ts > current_time:
                   return (ts, *self.event_data[ts])
           return None
       
       def process_due_events(self, current_time):
           """Get and remove all due events."""
           due = []
           to_remove = []
           
           for ts in self.events.inorder_traversal():
               if ts <= current_time:
                   due.append((ts, *self.event_data[ts]))
                   to_remove.append(ts)
               else:
                   break
           
           # Remove processed events
           for ts in to_remove:
               self.events.remove(ts)
               del self.event_data[ts]
           
           return due
       
       def count_pending(self, current_time):
           """Count events after current time."""
           count = 0
           for ts in self.events.inorder_traversal():
               if ts > current_time:
                   count += 1
           return count
   
   # Usage
   scheduler = EventScheduler()
   
   # Schedule events
   now = time.time()
   scheduler.schedule(now + 60, "task1", "Check email")
   scheduler.schedule(now + 300, "task2", "Meeting")
   scheduler.schedule(now + 30, "task3", "Quick call")
   
   # Get next event
   next_event = scheduler.get_next_event(now)
   if next_event:
       ts, event_id, data = next_event
       print(f"Next: {data} in {ts - now:.0f} seconds")
   
   # Process due events
   time.sleep(35)
   due = scheduler.process_due_events(time.time())
   print(f"Processed {len(due)} events")

Best Practices
==============

Do's
----

✅ **Use AVL for search-heavy workloads**

.. code-block:: python

   # Perfect for databases, indexes, lookups
   index = AVLTree()
   for key in millions_of_keys:
       index.insert(key)
   
   # Always O(log n) search
   found = index.search(target)

✅ **Trust the automatic balancing**

.. code-block:: python

   # No need to worry about insertion order
   avl = AVLTree()
   for val in sorted_data:  # Even sorted!
       avl.insert(val)
   # Still perfectly balanced

✅ **Leverage O(1) height access**

.. code-block:: python

   # Height is cached - very fast
   if avl.height() > threshold:
       print("Tree is getting large")

Don'ts
------

❌ **Don't use for insert-heavy workloads**

.. code-block:: python

   # If mostly insertions/deletions, use Red-Black instead
   # AVL does more rotations on updates
   
   # Bad for:
   # - Frequent insertions
   # - Frequent deletions
   # - Few searches
   
   # Good for:
   # - Many searches
   # - Few updates
   # - Need minimum height

❌ **Don't manually try to balance**

.. code-block:: python

   # Bad: AVL handles this automatically
   # No need to shuffle or pre-arrange data

❌ **Don't forget memory overhead**

.. code-block:: python

   # AVL stores height at each node
   # Extra O(n) memory vs regular BST
   # Consider for very large datasets

Common Pitfalls
===============

1. **Not considering operation ratio**

.. code-block:: python

   # Analyze your workload:
   # 90% searches → AVL is perfect
   # 50% updates → Consider Red-Black

2. **Ignoring deletion cost**

.. code-block:: python

   # AVL deletion can do O(log n) rotations
   # vs Red-Black's O(1) rotations
   # Matters for update-heavy applications

3. **Forgetting traversal cost**

.. code-block:: python

   # Traversals are still O(n)
   # Balance doesn't help here

Further Reading
===============

* :doc:`/api/tree/balanced` - Complete API reference
* :doc:`red_black` - Alternative balanced tree
* :doc:`binary` - Unbalanced BST comparison

References
==========

.. [1] Adelson-Velsky, G., Landis, E. M. "An algorithm for the organization of information", 1962
.. [2] Cormen, T. H., et al. "Introduction to Algorithms", 3rd Edition, Chapter 13
.. [3] Knuth, D. E. "The Art of Computer Programming, Volume 3", Section 6.2.3
.. [4] Weiss, M. A. "Data Structures and Algorithm Analysis", Chapter 4.4
