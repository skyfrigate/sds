.. _guide_tree_segment_tree:

==================
Segment Tree Guide
==================

.. currentmodule:: sds.tree

Introduction
============

A **Segment Tree** is a binary tree data structure that allows efficient range queries and updates on an array. Each node represents a segment (range) of the array, with leaves representing individual elements and internal nodes representing merged results. Segment trees are essential for competitive programming and applications requiring frequent range operations.

.. mermaid::

   graph TB
       subgraph "Segment Tree for array [1,3,5,7,9,11]"
       A["[0,5]: 36<br/>(sum)"] --> B["[0,2]: 9"]
       A --> C["[3,5]: 27"]
       
       B --> D["[0,1]: 4"]
       B --> E["[2,2]: 5"]
       
       C --> F["[3,4]: 16"]
       C --> G["[5,5]: 11"]
       
       D --> H["[0]: 1"]
       D --> I["[1]: 3"]
       
       F --> J["[3]: 7"]
       F --> K["[4]: 9"]
       end
       
       style A fill:#e74c3c,color:#fff
       style B fill:#3498db,color:#fff
       style C fill:#3498db,color:#fff
       style H fill:#2ecc71,color:#fff
       style I fill:#2ecc71,color:#fff
       style E fill:#2ecc71,color:#fff
       style J fill:#2ecc71,color:#fff
       style K fill:#2ecc71,color:#fff
       style G fill:#2ecc71,color:#fff

.. note::
   
   Segment trees excel when you need both queries and updates on ranges.
   If only queries are needed, consider prefix sums. If only updates matter,
   consider other structures. Segment trees are the sweet spot for both.

Mathematical Model
==================

Formal Definition
-----------------

Segment Tree Structure
^^^^^^^^^^^^^^^^^^^^^^

A Segment Tree :math:`T` for an array :math:`A[0..n-1]` is defined as:

1. **Leaves represent array elements**

   .. math::

      \forall i \in [0, n-1]: leaf_i = A[i]

2. **Internal nodes represent segment results**

   .. math::

      node_{[l,r]} = merge(node_{[l,m]}, node_{[m+1,r]})

   where :math:`m = \lfloor(l+r)/2\rfloor` and :math:`merge` is an associative operation (sum, min, max, gcd, etc.)

3. **Root represents entire array**

   .. math::

      root = node_{[0,n-1]}

Array Representation
^^^^^^^^^^^^^^^^^^^^

Using 0-indexed array with size :math:`4n`:

.. math::

   \begin{aligned}
   \text{Node at index } i &: segment_{[l,r]} \\
   \text{Left child} &: 2i + 1 \\
   \text{Right child} &: 2i + 2 \\
   \text{Parent} &: \lfloor(i-1)/2\rfloor
   \end{aligned}

Tree Properties
---------------

Height and Size
^^^^^^^^^^^^^^^

For an array of size :math:`n`:

**Height**:

.. math::

   h = \lceil \log_2 n \rceil

**Number of nodes**:

.. math::

   nodes \leq 4n

**Proof sketch**: Complete binary tree with :math:`n` leaves has at most :math:`2n-1` nodes. We allocate :math:`4n` for simplicity and to handle non-power-of-2 sizes.

**Leaves**: Exactly :math:`n` leaf nodes (one per array element)

Range Coverage
^^^^^^^^^^^^^^

For a node representing segment :math:`[l, r]`:

.. math::

   \begin{aligned}
   \text{Segment length} &= r - l + 1 \\
   \text{Middle point} &= \lfloor(l + r)/2\rfloor \\
   \text{Left child} &: [l, mid] \\
   \text{Right child} &: [mid+1, r]
   \end{aligned}

Query Decomposition
^^^^^^^^^^^^^^^^^^^

Any range :math:`[L, R]` can be decomposed into at most :math:`O(\log n)` disjoint segments:

.. math::

   [L, R] = \bigcup_{i=1}^{k} segment_i, \quad k = O(\log n)

This is the key to efficient range queries!

Algorithmic Model
=================

Abstract Data Type
------------------

.. code-block:: text

   ADT SegmentTree:
       Data:
           - array: underlying array of values
           - tree: segment tree array (size 4n)
           - size: array length
           - operation: merge operation (sum, min, max, etc.)
           - identity: identity element for operation
       
       Operations:
           - SegmentTree(array, op): build tree from array
           - query(left, right): get result for range [left, right]
           - update(index, value): update single element
           - get(index): get value at index
           - range_update(left, right, value): update range (lazy)
       
       Invariants:
           - Each node = merge of its children
           - Leaves = array elements
           - Tree maintains consistency after updates

Build Algorithm
---------------

Bottom-up construction:

.. code-block:: text

   Algorithm: BUILD_SEGMENT_TREE(array, operation, identity)
   Input: Array, associative operation, identity element
   Output: Segment tree
   
   1. n ← length(array)
   2. tree ← array of size 4n, initialized with identity
   3. 
   4. // Copy array to leaves
   5. // (but we build from leaves up instead)
   6. 
   7. BUILD_RECURSIVE(tree, array, 0, 0, n-1)
   8. return tree

.. code-block:: text

   Algorithm: BUILD_RECURSIVE(tree, array, node, start, end)
   Input: Tree array, source array, node index, segment [start, end]
   Output: Tree with node built
   
   1. if start = end then
   2.     // Leaf node
   3.     tree[node] ← array[start]
   4.     return
   5. end if
   6. 
   7. // Recursive case
   8. mid ← ⌊(start + end) / 2⌋
   9. left_child ← 2 × node + 1
   10. right_child ← 2 × node + 2
   11. 
   12. // Build left and right subtrees
   13. BUILD_RECURSIVE(tree, array, left_child, start, mid)
   14. BUILD_RECURSIVE(tree, array, right_child, mid+1, end)
   15. 
   16. // Merge results
   17. tree[node] ← operation(tree[left_child], tree[right_child])

**Time complexity**: O(n) - each element processed once
**Space complexity**: O(4n) = O(n)

Query Algorithm
---------------

.. code-block:: text

   Algorithm: QUERY(tree, node, start, end, L, R)
   Input: Tree, current node, segment [start,end], query [L,R]
   Output: Result for range [L, R]
   
   1. // No overlap
   2. if R < start or L > end then
   3.     return identity
   4. end if
   5. 
   6. // Complete overlap - return this node's value
   7. if L ≤ start and end ≤ R then
   8.     return tree[node]
   9. end if
   10. 
   11. // Partial overlap - query both children
   12. mid ← ⌊(start + end) / 2⌋
   13. left_child ← 2 × node + 1
   14. right_child ← 2 × node + 2
   15. 
   16. left_result ← QUERY(tree, left_child, start, mid, L, R)
   17. right_result ← QUERY(tree, right_child, mid+1, end, L, R)
   18. 
   19. return operation(left_result, right_result)

**Time complexity**: O(log n) - at most 2 nodes per level visited

**Visualization**:

.. code-block:: text

   Query [2, 5] on tree for [0, 7]:
   
   Level 0: [0,7] - partial overlap, recurse
   Level 1: [0,3] - partial, recurse  |  [4,7] - partial, recurse
   Level 2: [2,3] - complete overlap ✓ | [4,5] - complete overlap ✓
   
   Result = merge([2,3], [4,5])

Update Algorithm
----------------

Point update (single element):

.. code-block:: text

   Algorithm: UPDATE(tree, array, node, start, end, index, value)
   Input: Tree, array, node, segment, index to update, new value
   Output: Updated tree
   
   1. // Leaf node - update value
   2. if start = end then
   3.     tree[node] ← value
   4.     array[index] ← value
   5.     return
   6. end if
   7. 
   8. // Recursive case
   9. mid ← ⌊(start + end) / 2⌋
   10. left_child ← 2 × node + 1
   11. right_child ← 2 × node + 2
   12. 
   13. // Update appropriate child
   14. if index ≤ mid then
   15.    UPDATE(tree, array, left_child, start, mid, index, value)
   16. else
   17.    UPDATE(tree, array, right_child, mid+1, end, index, value)
   18. end if
   19. 
   20. // Recalculate current node
   21. tree[node] ← operation(tree[left_child], tree[right_child])

**Time complexity**: O(log n) - one path from root to leaf

Lazy Propagation
----------------

For range updates, use lazy propagation:

.. code-block:: text

   Algorithm: LAZY_UPDATE(node, start, end, L, R, value)
   Input: Node, segment [start,end], update range [L,R], value
   Output: Updated tree with lazy flags
   
   1. // Apply pending updates
   2. if lazy[node] ≠ 0 then
   3.     tree[node] ← tree[node] + (end - start + 1) × lazy[node]
   4.     
   5.     if start ≠ end then
   6.         // Propagate to children
   7.         lazy[2×node+1] ← lazy[2×node+1] + lazy[node]
   8.         lazy[2×node+2] ← lazy[2×node+2] + lazy[node]
   9.     end if
   10.    
   11.    lazy[node] ← 0
   12. end if
   13. 
   14. // No overlap
   15. if R < start or L > end then
   16.    return
   17. end if
   18. 
   19. // Complete overlap - mark lazy
   20. if L ≤ start and end ≤ R then
   21.    tree[node] ← tree[node] + (end - start + 1) × value
   22.    
   23.    if start ≠ end then
   24.        lazy[2×node+1] ← lazy[2×node+1] + value
   25.        lazy[2×node+2] ← lazy[2×node+2] + value
   26.    end if
   27.    return
   28. end if
   29. 
   30. // Partial overlap - recurse
   31. mid ← ⌊(start + end) / 2⌋
   32. LAZY_UPDATE(2×node+1, start, mid, L, R, value)
   33. LAZY_UPDATE(2×node+2, mid+1, end, L, R, value)
   34. 
   35. // Recalculate
   36. tree[node] ← tree[2×node+1] + tree[2×node+2]

**Time complexity**: O(log n) per range update

Complexity Analysis
-------------------

Time Complexity
^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 35 20 40

   * - Operation
     - Complexity
     - Notes
   * - **Build**
     - O(n)
     - Bottom-up construction
   * - **Query range**
     - O(log n)
     - O(log n) segments
   * - **Update point**
     - O(log n)
     - Path to leaf
   * - **Update range (lazy)**
     - O(log n)
     - Amortized
   * - **Get element**
     - O(1)
     - Direct array access
   * - **Space**
     - O(n)
     - 4n array storage

Space Complexity
^^^^^^^^^^^^^^^^

* **Tree array**: 4n elements
* **Lazy array** (if needed): 4n elements
* **Total**: O(n)

Practical Usage
===============

Installation and Import
-----------------------

.. code-block:: python

   # Install
   pip install sds-tools
   
   # Import
   from sds.tree import SegmentTree

Basic Operations
----------------

Range Sum Queries
^^^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.tree import SegmentTree

   # Create segment tree for range sums
   arr = [1, 3, 5, 7, 9, 11]
   tree = SegmentTree(arr, operation='sum')
   
   # Query sum of range [1, 4] - O(log n)
   result = tree.query(1, 4)
   print(result)  # Output: 24 (3+5+7+9)
   
   # Update element - O(log n)
   tree.update(2, 10)  # arr[2] = 5 -> 10
   
   # Query again
   result = tree.query(1, 4)
   print(result)  # Output: 29 (3+10+7+9)

Range Minimum/Maximum
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Range minimum queries
   arr = [5, 2, 8, 1, 9, 3, 7]
   min_tree = SegmentTree(arr, operation='min')
   
   # Find minimum in range [1, 5]
   min_val = min_tree.query(1, 5)
   print(min_val)  # Output: 1
   
   # Range maximum queries
   max_tree = SegmentTree(arr, operation='max')
   max_val = max_tree.query(1, 5)
   print(max_val)  # Output: 9

Custom Operations
^^^^^^^^^^^^^^^^^

.. code-block:: python

   import math

   # GCD (Greatest Common Divisor) queries
   def gcd_op(a, b):
       return math.gcd(a, b)
   
   arr = [12, 18, 24, 30, 36]
   gcd_tree = SegmentTree(arr, operation=gcd_op, identity=0)
   
   # Find GCD of range [1, 3]
   result = gcd_tree.query(1, 3)
   print(result)  # Output: 6

Array-like Access
^^^^^^^^^^^^^^^^^

.. code-block:: python

   tree = SegmentTree([1, 2, 3, 4, 5])
   
   # Get element - O(1)
   print(tree[2])  # Output: 3
   
   # Update element - O(log n)
   tree[2] = 10
   
   # Get updated value
   print(tree[2])  # Output: 10

Real-World Applications
=======================

Application 1: Range Statistics
--------------------------------

Statistical queries on data streams:

.. code-block:: python

   from sds.tree import SegmentTree

   class RangeStatistics:
       """Compute statistics on array ranges efficiently."""
       
       def __init__(self, data):
           self.sum_tree = SegmentTree(data, operation='sum')
           self.min_tree = SegmentTree(data, operation='min')
           self.max_tree = SegmentTree(data, operation='max')
           self.size = len(data)
       
       def range_sum(self, left, right):
           """Sum of elements in range."""
           return self.sum_tree.query(left, right)
       
       def range_average(self, left, right):
           """Average of elements in range."""
           total = self.sum_tree.query(left, right)
           count = right - left + 1
           return total / count
       
       def range_min(self, left, right):
           """Minimum in range."""
           return self.min_tree.query(left, right)
       
       def range_max(self, left, right):
           """Maximum in range."""
           return self.max_tree.query(left, right)
       
       def update_value(self, index, value):
           """Update value and refresh all trees."""
           self.sum_tree.update(index, value)
           self.min_tree.update(index, value)
           self.max_tree.update(index, value)
   
   # Usage
   data = [5, 2, 8, 1, 9, 3, 7, 4, 6]
   stats = RangeStatistics(data)
   
   # Query range [2, 6]
   print(f"Sum: {stats.range_sum(2, 6)}")
   print(f"Average: {stats.range_average(2, 6):.2f}")
   print(f"Min: {stats.range_min(2, 6)}")
   print(f"Max: {stats.range_max(2, 6)}")
   
   # Update and re-query
   stats.update_value(3, 10)
   print(f"New min: {stats.range_min(2, 6)}")

Application 2: Hotel Booking System
------------------------------------

Track room availability:

.. code-block:: python

   from sds.tree import SegmentTree

   class HotelBooking:
       """Manage hotel room bookings with range queries."""
       
       def __init__(self, num_rooms, num_days):
           # 1 = available, 0 = booked
           # Track availability for each (room, day)
           self.rooms = num_rooms
           self.days = num_days
           
           # One tree per room
           self.availability = [
               SegmentTree([1] * num_days, operation='min')
               for _ in range(num_rooms)
           ]
       
       def is_available(self, room, start_day, end_day):
           """Check if room is available for date range."""
           # Min = 1 means all days available
           return self.availability[room].query(start_day, end_day) == 1
       
       def book_room(self, room, start_day, end_day):
           """Book room for date range."""
           if not self.is_available(room, start_day, end_day):
               return False
           
           # Mark days as booked
           for day in range(start_day, end_day + 1):
               self.availability[room].update(day, 0)
           
           return True
       
       def cancel_booking(self, room, start_day, end_day):
           """Cancel booking and free up room."""
           for day in range(start_day, end_day + 1):
               self.availability[room].update(day, 1)
       
       def find_available_room(self, start_day, end_day):
           """Find any available room for date range."""
           for room in range(self.rooms):
               if self.is_available(room, start_day, end_day):
                   return room
           return None
       
       def count_available_rooms(self, day):
           """Count available rooms on specific day."""
           count = 0
           for room in range(self.rooms):
               if self.availability[room].query(day, day) == 1:
                   count += 1
           return count
   
   # Usage
   hotel = HotelBooking(num_rooms=10, num_days=30)
   
   # Book room 3 for days 5-10
   success = hotel.book_room(3, 5, 10)
   print(f"Booking successful: {success}")
   
   # Check availability
   available = hotel.is_available(3, 7, 9)
   print(f"Room 3 available days 7-9: {available}")
   
   # Find any available room
   room = hotel.find_available_room(5, 7)
   print(f"Available room: {room}")

Application 3: Stock Price Analysis
------------------------------------

Technical analysis on stock prices:

.. code-block:: python

   from sds.tree import SegmentTree

   class StockAnalyzer:
       """Analyze stock price movements."""
       
       def __init__(self, prices):
           self.prices = prices
           self.min_tree = SegmentTree(prices, operation='min')
           self.max_tree = SegmentTree(prices, operation='max')
           self.sum_tree = SegmentTree(prices, operation='sum')
       
       def support_level(self, start, end):
           """Find support (minimum) in time period."""
           return self.min_tree.query(start, end)
       
       def resistance_level(self, start, end):
           """Find resistance (maximum) in time period."""
           return self.max_tree.query(start, end)
       
       def average_price(self, start, end):
           """Calculate average price in period."""
           total = self.sum_tree.query(start, end)
           count = end - start + 1
           return total / count
       
       def price_range(self, start, end):
           """Get price range (volatility indicator)."""
           min_price = self.min_tree.query(start, end)
           max_price = self.max_tree.query(start, end)
           return max_price - min_price
       
       def update_price(self, day, new_price):
           """Update price for a day (correction/split)."""
           self.prices[day] = new_price
           self.min_tree.update(day, new_price)
           self.max_tree.update(day, new_price)
           self.sum_tree.update(day, new_price)
       
       def find_best_buy_sell(self):
           """Find best buy/sell days for max profit."""
           n = len(self.prices)
           max_profit = 0
           buy_day = 0
           sell_day = 0
           
           for i in range(n):
               # Find minimum before day i
               if i > 0:
                   min_price = self.min_tree.query(0, i-1)
                   profit = self.prices[i] - min_price
                   
                   if profit > max_profit:
                       max_profit = profit
                       # Find which day had min price
                       for j in range(i):
                           if self.prices[j] == min_price:
                               buy_day = j
                               sell_day = i
                               break
           
           return buy_day, sell_day, max_profit
   
   # Usage
   prices = [100, 105, 98, 110, 95, 108, 115, 102, 120, 118]
   analyzer = StockAnalyzer(prices)
   
   # Analysis for last week (days 3-9)
   print(f"Support: ${analyzer.support_level(3, 9):.2f}")
   print(f"Resistance: ${analyzer.resistance_level(3, 9):.2f}")
   print(f"Average: ${analyzer.average_price(3, 9):.2f}")
   print(f"Volatility: ${analyzer.price_range(3, 9):.2f}")
   
   # Find best trading opportunity
   buy, sell, profit = analyzer.find_best_buy_sell()
   print(f"Best trade: Buy day {buy}, sell day {sell}, profit ${profit:.2f}")

Application 4: Leaderboard System
----------------------------------

Gaming leaderboard with range queries:

.. code-block:: python

   from sds.tree import SegmentTree

   class Leaderboard:
       """Gaming leaderboard with efficient queries."""
       
       def __init__(self, num_players):
           # Initial scores = 0
           self.scores = [0] * num_players
           self.sum_tree = SegmentTree(self.scores, operation='sum')
           self.max_tree = SegmentTree(self.scores, operation='max')
       
       def update_score(self, player_id, score):
           """Update player's score."""
           self.scores[player_id] = score
           self.sum_tree.update(player_id, score)
           self.max_tree.update(player_id, score)
       
       def add_points(self, player_id, points):
           """Add points to player's score."""
           new_score = self.scores[player_id] + points
           self.update_score(player_id, new_score)
       
       def get_score(self, player_id):
           """Get player's current score."""
           return self.scores[player_id]
       
       def total_score_range(self, start_id, end_id):
           """Get total score for player range."""
           return self.sum_tree.query(start_id, end_id)
       
       def top_score_range(self, start_id, end_id):
           """Get highest score in player range."""
           return self.max_tree.query(start_id, end_id)
       
       def average_score_range(self, start_id, end_id):
           """Get average score for player range."""
           total = self.sum_tree.query(start_id, end_id)
           count = end_id - start_id + 1
           return total / count
   
   # Usage
   leaderboard = Leaderboard(num_players=1000)
   
   # Players score points
   leaderboard.update_score(42, 1500)
   leaderboard.update_score(100, 2000)
   leaderboard.update_score(250, 1800)
   leaderboard.add_points(42, 200)
   
   # Query top 100 players (0-99)
   total = leaderboard.total_score_range(0, 99)
   top = leaderboard.top_score_range(0, 99)
   avg = leaderboard.average_score_range(0, 99)
   
   print(f"Top 100 - Total: {total}, Max: {top}, Avg: {avg:.1f}")

Best Practices
==============

Do's
----

✅ **Use for frequent range queries with updates**

.. code-block:: python

   # Perfect for:
   # - Range sum/min/max queries
   # - Dynamic arrays with modifications
   # - Statistical queries on changing data

✅ **Choose appropriate operation**

.. code-block:: python

   # Sum, min, max, gcd, lcm all work
   # Operation must be associative!

✅ **Consider lazy propagation for range updates**

.. code-block:: python

   # If many range updates, use lazy propagation
   # Avoids updating every element individually

Don'ts
------

❌ **Don't use for static data with no updates**

.. code-block:: python

   # Use prefix sums instead - simpler and faster
   # Segment trees are for dynamic data

❌ **Don't use for non-associative operations**

.. code-block:: python

   # Bad: subtraction (not associative)
   # Good: addition, min, max, gcd

❌ **Don't forget 0-indexing**

.. code-block:: python

   # Most implementations use 0-based indexing
   # query(0, n-1) for entire array

Comparison with Alternatives
=============================

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 20 15

   * - Structure
     - Range Query
     - Point Update
     - Range Update
     - Space
   * - **Segment Tree**
     - O(log n)
     - O(log n)
     - O(log n)*
     - O(n)
   * - **Prefix Sum**
     - O(1)
     - O(n)
     - O(n)
     - O(n)
   * - **Fenwick Tree**
     - O(log n)
     - O(log n)
     - O(log n)
     - O(n)
   * - **Sqrt Decomp**
     - O(√n)
     - O(1)
     - O(√n)
     - O(n)

\* With lazy propagation

When to Use Segment Trees
--------------------------

**Use Segment Tree when:**
   - Need both queries and updates
   - Operations are associative
   - O(log n) per operation acceptable
   - Various types of queries needed

**Use alternatives when:**
   - Prefix sums: Static data, only range sums
   - Fenwick tree: Only sum operations, less space
   - Sqrt decomposition: Simpler implementation needs

Further Reading
===============

* :doc:`/api/tree/segment_tree` - Complete API reference
* :doc:`binary` - Binary tree basics
* :doc:`heap` - Priority queue structures

References
==========

.. [WikiSegTree] Wikipedia contributors. "Segment tree". Wikipedia.
   https://en.wikipedia.org/wiki/Segment_tree
   
   Overview of segment tree variants and applications.

.. [CP3] Halim, S., Halim, F. "Competitive Programming 3"
   
   Comprehensive treatment of segment trees for competitive programming.

.. [CLRS] Cormen, T. H., et al. "Introduction to Algorithms"
   
   Related interval tree structures.

.. [TopCoder] TopCoder. "Range Minimum Query and Lowest Common Ancestor"
   https://www.topcoder.com/community/competitive-programming/tutorials/range-minimum-query-and-lowest-common-ancestor/
   
   Tutorial on RMQ problems and segment trees.

.. [CPAlgorithms] CP-Algorithms. "Segment Tree"
   https://cp-algorithms.com/data_structures/segment_tree.html
   
   Detailed segment tree tutorial with code examples.
