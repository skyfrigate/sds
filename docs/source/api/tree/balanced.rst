.. _api_tree_balanced:

==============
Balanced Trees
==============

.. currentmodule:: sds.tree.balanced

Overview
========

This module provides self-balancing binary search tree implementations that guarantee
O(log n) operations by automatically maintaining balance through rotations. These trees
ensure efficient performance even with arbitrary insertion and deletion patterns.

.. mermaid::

   graph TB
       subgraph "AVL Tree (height-balanced)"
       A1[50] --> B1[30]
       A1 --> C1[70]
       B1 --> D1[20]
       B1 --> E1[40]
       C1 --> F1[60]
       C1 --> G1[80]
       end
       
       subgraph "Red-Black Tree (color-balanced)"
       A2[50:B] --> B2[30:R]
       A2 --> C2[70:R]
       B2 --> D2[20:B]
       B2 --> E2[40:B]
       C2 --> F2[60:B]
       C2 --> G2[80:B]
       end
       
       style A1 fill:#e74c3c,color:#fff
       style A2 fill:#2c3e50,color:#fff
       style B2 fill:#e74c3c,color:#fff
       style C2 fill:#e74c3c,color:#fff

Classes
=======

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   AVLTree
   RedBlackTree

Detailed Documentation
======================

AVLTree
-------

.. autoclass:: AVLTree
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __len__, __iter__, __contains__, __repr__, __str__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Properties

   .. autoproperty:: root
   .. autoproperty:: size

   .. rubric:: Core Operations

   .. automethod:: insert
   .. automethod:: remove
   .. automethod:: search
   .. automethod:: height

   .. rubric:: Traversal Methods

   .. automethod:: inorder_traversal
   .. automethod:: preorder_traversal
   .. automethod:: postorder_traversal
   .. automethod:: level_order_traversal

   .. rubric:: Utility Methods

   .. automethod:: is_empty
   .. automethod:: clear

   .. rubric:: Special Methods

   .. automethod:: __len__
   .. automethod:: __iter__
   .. automethod:: __contains__
   .. automethod:: __repr__
   .. automethod:: __str__

RedBlackTree
------------

.. autoclass:: RedBlackTree
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __len__, __iter__, __contains__, __repr__, __str__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Properties

   .. autoproperty:: root
   .. autoproperty:: size

   .. rubric:: Core Operations

   .. automethod:: insert
   .. automethod:: remove
   .. automethod:: search

   .. rubric:: Traversal Methods

   .. automethod:: inorder_traversal
   .. automethod:: preorder_traversal
   .. automethod:: postorder_traversal
   .. automethod:: level_order_traversal

   .. rubric:: Utility Methods

   .. automethod:: is_empty
   .. automethod:: clear

   .. rubric:: Special Methods

   .. automethod:: __len__
   .. automethod:: __iter__
   .. automethod:: __contains__
   .. automethod:: __repr__
   .. automethod:: __str__

Usage Examples
==============

AVL Tree Examples
-----------------

Basic Operations
^^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.tree import AVLTree

   # Create AVL tree
   avl = AVLTree()
   
   # Insert values (automatic balancing)
   for val in [10, 20, 30, 40, 50, 25]:
       avl.insert(val)
   
   # Tree remains balanced
   print(f"Size: {len(avl)}")        # Output: 6
   print(f"Height: {avl.height()}")  # Output: 2 (log₂ 6 ≈ 2.58)
   
   # Inorder gives sorted sequence
   print(list(avl))
   # Output: [10, 20, 25, 30, 40, 50]

Guaranteed Balance
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Even inserting sorted data stays balanced!
   avl = AVLTree()
   for i in range(1, 8):
       avl.insert(i)
   
   # Height is logarithmic
   print(avl.height())  # Output: 2 (not 6!)
   
   # Compare to unbalanced BST which would have height 6
   from sds.tree import BinarySearchTree
   bst = BinarySearchTree()
   for i in range(1, 8):
       bst.insert(i)
   print(bst.height())  # Output: 6 (degenerate)

Search and Removal
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   avl = AVLTree()
   for val in [50, 30, 70, 20, 40, 60, 80]:
       avl.insert(val)
   
   # O(log n) search guaranteed
   print(avl.search(40))   # Output: True
   print(40 in avl)        # Output: True
   
   # Remove maintains balance
   avl.remove(30)
   print(list(avl))
   # Output: [20, 40, 50, 60, 70, 80]
   
   print(avl.height())  # Still balanced

Traversals
^^^^^^^^^^

.. code-block:: python

   avl = AVLTree()
   for val in [50, 30, 70, 20, 40, 60, 80]:
       avl.insert(val)
   
   # Inorder (sorted)
   print("Inorder:", list(avl.inorder_traversal()))
   # Output: [20, 30, 40, 50, 60, 70, 80]
   
   # Preorder
   print("Preorder:", list(avl.preorder_traversal()))
   # Output: [50, 30, 20, 40, 70, 60, 80]
   
   # Level-order
   print("Level-order:", list(avl.level_order_traversal()))
   # Output: [50, 30, 70, 20, 40, 60, 80]

Red-Black Tree Examples
------------------------

Basic Operations
^^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.tree import RedBlackTree

   # Create Red-Black tree
   rbt = RedBlackTree()
   
   # Insert values (automatic balancing)
   for val in [10, 20, 30, 40, 50]:
       rbt.insert(val)
   
   # Tree is balanced
   print(f"Size: {len(rbt)}")  # Output: 5
   print(list(rbt))
   # Output: [10, 20, 30, 40, 50]

Fast Insertions
^^^^^^^^^^^^^^^

.. code-block:: python

   # Red-Black trees excel at frequent insertions
   rbt = RedBlackTree()
   
   # Insert 1000 elements
   import random
   values = list(range(1000))
   random.shuffle(values)
   
   for val in values:
       rbt.insert(val)
   
   # Height is still logarithmic
   print(f"Height: {rbt.height()}")  # ~O(log n)
   
   # Verify sorted order
   sorted_vals = list(rbt.inorder_traversal())
   print(sorted_vals == list(range(1000)))  # True

Search and Removal
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   rbt = RedBlackTree()
   for val in [50, 30, 70, 20, 40, 60, 80]:
       rbt.insert(val)
   
   # O(log n) search
   print(rbt.search(60))  # Output: True
   
   # Remove maintains balance
   rbt.remove(50)
   print(list(rbt))
   # Output: [20, 30, 40, 60, 70, 80]

Real-World Examples
===================

Example 1: Database Index with AVL
-----------------------------------

Using AVL tree for fast lookups:

.. code-block:: python

   from sds.tree import AVLTree

   class DatabaseIndex:
       """Fast database index using AVL tree."""
       
       def __init__(self):
           self.index = AVLTree()
           self.records = {}
       
       def add_record(self, key, record):
           """Add record to database."""
           self.index.insert(key)
           self.records[key] = record
       
       def find_record(self, key):
           """Find record by key (O(log n))."""
           if self.index.search(key):
               return self.records[key]
           return None
       
       def delete_record(self, key):
           """Delete record."""
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
       
       def count(self):
           """Get total records."""
           return len(self.index)
   
   # Usage
   db = DatabaseIndex()
   
   # Add records
   db.add_record(100, {"name": "Alice", "age": 30})
   db.add_record(50, {"name": "Bob", "age": 25})
   db.add_record(150, {"name": "Charlie", "age": 35})
   db.add_record(75, {"name": "David", "age": 28})
   
   # Fast lookup
   record = db.find_record(75)
   print(f"Found: {record}")
   
   # Range query
   results = db.range_query(50, 100)
   print(f"Records 50-100: {len(results)}")

Example 2: Real-Time Leaderboard
---------------------------------

Maintaining sorted rankings with frequent updates:

.. code-block:: python

   from sds.tree import RedBlackTree

   class Leaderboard:
       """Real-time game leaderboard using Red-Black tree."""
       
       def __init__(self):
           # Tree of (score, player) tuples
           self.scores = RedBlackTree()
           self.players = {}  # player -> score
       
       def update_score(self, player, new_score):
           """Update player's score."""
           # Remove old score
           if player in self.players:
               old_score = self.players[player]
               self.scores.remove((old_score, player))
           
           # Add new score
           self.scores.insert((new_score, player))
           self.players[player] = new_score
       
       def get_rank(self, player):
           """Get player's rank (1-indexed)."""
           if player not in self.players:
               return None
           
           score = self.players[player]
           rank = 1
           
           # Count players with higher scores
           for s, p in self.scores.inorder_traversal():
               if s > score or (s == score and p != player):
                   rank += 1
               elif s == score and p == player:
                   break
           
           return rank
       
       def get_top_n(self, n):
           """Get top n players."""
           # Reverse inorder for descending order
           all_scores = list(self.scores.inorder_traversal())
           top = all_scores[-n:] if len(all_scores) >= n else all_scores
           return [(player, score) for score, player in reversed(top)]
       
       def get_player_score(self, player):
           """Get player's current score."""
           return self.players.get(player)
   
   # Usage
   lb = Leaderboard()
   
   # Players join and play
   lb.update_score("Alice", 100)
   lb.update_score("Bob", 150)
   lb.update_score("Charlie", 120)
   lb.update_score("David", 180)
   
   # Check rankings
   print(f"Bob's rank: {lb.get_rank('Bob')}")
   
   # Bob improves
   lb.update_score("Bob", 200)
   print(f"Bob's new rank: {lb.get_rank('Bob')}")
   
   # Top 3 players
   top3 = lb.get_top_n(3)
   for i, (player, score) in enumerate(top3, 1):
       print(f"{i}. {player}: {score}")

Example 3: Event Scheduler
---------------------------

Managing time-based events:

.. code-block:: python

   from sds.tree import AVLTree
   import time

   class EventScheduler:
       """Schedule events by timestamp using AVL tree."""
       
       def __init__(self):
           self.events = AVLTree()
       
       def schedule(self, timestamp, event):
           """Schedule an event."""
           self.events.insert((timestamp, event))
       
       def cancel(self, timestamp, event):
           """Cancel an event."""
           try:
               self.events.remove((timestamp, event))
               return True
           except:
               return False
       
       def get_next_event(self, current_time):
           """Get next event after current time."""
           for ts, event in self.events.inorder_traversal():
               if ts > current_time:
                   return (ts, event)
           return None
       
       def get_pending_events(self, current_time):
           """Get all events after current time."""
           pending = []
           for ts, event in self.events.inorder_traversal():
               if ts > current_time:
                   pending.append((ts, event))
           return pending
       
       def get_due_events(self, current_time):
           """Get events that are due now or overdue."""
           due = []
           for ts, event in self.events.inorder_traversal():
               if ts <= current_time:
                   due.append((ts, event))
               else:
                   break
           return due
   
   # Usage
   scheduler = EventScheduler()
   
   # Schedule events (using timestamps)
   now = time.time()
   scheduler.schedule(now + 60, "Task 1")     # 1 minute
   scheduler.schedule(now + 300, "Task 2")    # 5 minutes
   scheduler.schedule(now + 30, "Task 3")     # 30 seconds
   
   # Get next event
   next_event = scheduler.get_next_event(now)
   print(f"Next: {next_event[1]}")
   
   # Get all pending
   pending = scheduler.get_pending_events(now)
   print(f"Pending: {len(pending)} events")

Example 4: Auto-Complete Dictionary
------------------------------------

Fast word lookup with prefix search:

.. code-block:: python

   from sds.tree import AVLTree

   class Dictionary:
       """Dictionary with fast lookup using AVL tree."""
       
       def __init__(self):
           self.words = AVLTree()
       
       def add_word(self, word):
           """Add word to dictionary."""
           self.words.insert(word.lower())
       
       def add_words(self, word_list):
           """Add multiple words."""
           for word in word_list:
               self.add_word(word)
       
       def contains(self, word):
           """Check if word exists."""
           return self.words.search(word.lower())
       
       def find_prefix(self, prefix, max_results=10):
           """Find words with given prefix."""
           prefix = prefix.lower()
           results = []
           
           for word in self.words.inorder_traversal():
               if word.startswith(prefix):
                   results.append(word)
                   if len(results) >= max_results:
                       break
               elif word > prefix:
                   break
           
           return results
       
       def count_words(self):
           """Get total words."""
           return len(self.words)
   
   # Usage
   dictionary = Dictionary()
   
   # Load dictionary
   words = [
       "apple", "application", "apply", "appreciate",
       "banana", "band", "bandage",
       "cat", "catch", "category", "cathedral"
   ]
   dictionary.add_words(words)
   
   # Auto-complete
   suggestions = dictionary.find_prefix("app")
   print(f"Words starting with 'app': {suggestions}")
   
   # Check spelling
   print(f"'apple' in dictionary: {dictionary.contains('apple')}")

Performance Characteristics
===========================

Time Complexity
---------------

.. list-table::
   :header-rows: 1
   :widths: 30 20 20 30

   * - Operation
     - AVL Tree
     - Red-Black Tree
     - Notes
   * - **Insert**
     - O(log n)
     - O(log n)
     - Guaranteed
   * - **Delete**
     - O(log n)
     - O(log n)
     - Guaranteed
   * - **Search**
     - O(log n)
     - O(log n)
     - Guaranteed
   * - **Find Min/Max**
     - O(log n)
     - O(log n)
     - BST property
   * - **Height**
     - O(1)
     - O(n)
     - Cached in AVL
   * - **Inorder**
     - O(n)
     - O(n)
     - All nodes
   * - **Preorder**
     - O(n)
     - O(n)
     - All nodes
   * - **Postorder**
     - O(n)
     - O(n)
     - All nodes
   * - **Level-order**
     - O(n)
     - O(n)
     - BFS

Space Complexity
----------------

* **AVL Tree**: O(n) + O(n) for height storage
* **Red-Black Tree**: O(n) + O(n) for color bits
* **Recursion Stack**: O(log n) guaranteed (balanced height)

Comparison: AVL vs Red-Black
=============================

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - Aspect
     - AVL Tree
     - Red-Black Tree
   * - **Balance**
     - More strictly balanced
     - Less strictly balanced
   * - **Height**
     - h ≤ 1.44 log(n+2)
     - h ≤ 2 log(n+1)
   * - **Rotations (Insert)**
     - Max 2, more retracing
     - Max 2, less retracing
   * - **Rotations (Delete)**
     - Up to O(log n)
     - Max 3
   * - **Lookup Speed**
     - Faster (shorter)
     - Slightly slower
   * - **Insert/Delete**
     - Slower (more rotations)
     - Faster (fewer rotations)
   * - **Memory**
     - Height per node
     - Color bit per node
   * - **Best For**
     - Frequent searches
     - Frequent insertions/deletions
   * - **Used In**
     - Databases, memory management
     - Java TreeMap, C++ map

When to Use Each
----------------

**Use AVL Tree when:**
   - Searches vastly outnumber insertions/deletions
   - Need absolute minimum height
   - Memory for height storage is acceptable
   - Example: Static or mostly-read databases

**Use Red-Black Tree when:**
   - Insertions and deletions are frequent
   - Need good all-around performance
   - Prefer less balancing overhead
   - Example: Dynamic ordered maps, system libraries

**Use Regular BST when:**
   - Data arrives in random order
   - Simplicity is more important than guaranteed performance
   - Working with small datasets

Performance Metrics
===================

Rotation Counts
---------------

For n insertions in random order:

**AVL Tree:**
   - Average rotations per insert: 0.5
   - Maximum rotations per insert: 2
   - Total: ~0.5n rotations

**Red-Black Tree:**
   - Average rotations per insert: 0.24
   - Maximum rotations per insert: 2
   - Total: ~0.24n rotations

Height Guarantees
-----------------

For n nodes:

**AVL Tree:**

.. math::

   h_{AVL} \leq 1.44 \log_2(n+2) - 0.328

**Red-Black Tree:**

.. math::

   h_{RBT} \leq 2 \log_2(n+1)

**Example**: For n = 1,000,000:
   - AVL height: ≤ 28
   - Red-Black height: ≤ 40

Best Practices
==============

Do's
----

✅ **Use balanced trees for unpredictable data**

.. code-block:: python

   # Good: Always O(log n)
   avl = AVLTree()
   for value in potentially_sorted_data:
       avl.insert(value)

✅ **Choose based on operation frequency**

.. code-block:: python

   # Many searches → AVL
   if search_heavy:
       tree = AVLTree()
   
   # Many inserts/deletes → Red-Black
   if update_heavy:
       tree = RedBlackTree()

✅ **Trust the automatic balancing**

.. code-block:: python

   # No need to manually balance
   tree = AVLTree()
   tree.insert(1)
   tree.insert(2)
   tree.insert(3)
   # Already balanced!

Don'ts
------

❌ **Don't try to manually balance**

.. code-block:: python

   # Bad: Balanced trees handle this
   # No need to pre-shuffle or pre-arrange data

❌ **Don't assume equal performance**

.. code-block:: python

   # AVL is faster for lookups
   # Red-Black is faster for updates
   # Choose based on your use case

❌ **Don't forget about memory**

.. code-block:: python

   # AVL uses more memory (height storage)
   # Red-Black uses less (color bit)
   # Consider for very large datasets

Common Pitfalls
===============

1. **Not considering operation patterns**

.. code-block:: python

   # Analyze your workload first
   # 90% searches → AVL
   # 50/50 mix → Red-Black

2. **Ignoring constant factors**

.. code-block:: python

   # Both are O(log n), but:
   # AVL: shorter tree, faster search
   # Red-Black: fewer rotations, faster updates

3. **Unnecessary conversions**

.. code-block:: python

   # Don't convert between types
   # Choose once and stick with it

See Also
========

* :doc:`binary` - Unbalanced binary search trees
* :doc:`../../guide/tree_structures/avl` - AVL tree theory and guide
* :doc:`../../guide/tree_structures/red_black` - Red-Black tree guide

References
==========

.. [1] Adelson-Velsky, G., Landis, E. M. "An algorithm for the organization of information", 1962
.. [2] Guibas, L. J., Sedgewick, R. "A Dichromatic Framework for Balanced Trees", 1978
.. [3] Cormen, T. H., et al. "Introduction to Algorithms", 3rd Edition, Chapter 13
.. [4] Pfaff, B. "Performance Analysis of BSTs in System Software", 2004
