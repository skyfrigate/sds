.. _api_tree_segment_tree:

============
Segment Tree
============

.. currentmodule:: sds.tree.segment_tree

Overview
========

This module provides a Segment Tree implementation for efficient range queries and
updates on arrays. Segment trees support operations like range sum, range minimum,
range maximum, and other associative operations in O(log n) time.

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

Classes
=======

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   SegmentTree

Detailed Documentation
======================

SegmentTree
-----------

.. autoclass:: SegmentTree
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __len__, __getitem__, __setitem__, __repr__, __str__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Properties

   .. autoproperty:: size

   .. rubric:: Core Operations

   .. automethod:: query
   .. automethod:: update

   .. rubric:: Utility Methods

   .. automethod:: get

   .. rubric:: Special Methods

   .. automethod:: __len__
   .. automethod:: __getitem__
   .. automethod:: __setitem__
   .. automethod:: __repr__
   .. automethod:: __str__

Usage Examples
==============

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

Real-World Examples
===================

Example 1: Range Statistics
----------------------------

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

Example 2: Hotel Booking System
--------------------------------

Track room availability:

.. code-block:: python

   from sds.tree import SegmentTree

   class HotelBooking:
       """Manage hotel room bookings with range queries."""
       
       def __init__(self, num_rooms, num_days):
           # 1 = available, 0 = booked
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
   
   # Usage
   hotel = HotelBooking(num_rooms=10, num_days=30)
   
   # Book room 3 for days 5-10
   success = hotel.book_room(3, 5, 10)
   print(f"Booking successful: {success}")
   
   # Check availability
   available = hotel.is_available(3, 7, 9)
   print(f"Room 3 available days 7-9: {available}")

Example 3: Stock Price Analysis
--------------------------------

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
   
   # Usage
   prices = [100, 105, 98, 110, 95, 108, 115, 102, 120, 118]
   analyzer = StockAnalyzer(prices)
   
   # Analysis for last week (days 3-9)
   print(f"Support: ${analyzer.support_level(3, 9):.2f}")
   print(f"Resistance: ${analyzer.resistance_level(3, 9):.2f}")
   print(f"Average: ${analyzer.average_price(3, 9):.2f}")

Example 4: Leaderboard System
------------------------------

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
   leaderboard.add_points(42, 200)
   
   # Query top 100 players (0-99)
   total = leaderboard.total_score_range(0, 99)
   top = leaderboard.top_score_range(0, 99)
   avg = leaderboard.average_score_range(0, 99)
   
   print(f"Top 100 - Total: {total}, Max: {top}, Avg: {avg:.1f}")

Performance Characteristics
===========================

Time Complexity
---------------

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
----------------

* **Tree array**: 4n elements
* **Lazy array** (if needed): 4n elements
* **Total**: O(n)

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

Common Pitfalls
===============

1. **Using for static data**

.. code-block:: python

   # If no updates, prefix sums are simpler
   # Segment trees add unnecessary complexity

2. **Wrong operation choice**

.. code-block:: python

   # Operation must be associative
   # (a op b) op c = a op (b op c)

3. **Not considering alternatives**

.. code-block:: python

   # Fenwick trees are simpler for sum-only
   # Consider implementation complexity

See Also
========

* :doc:`binary` - Binary tree basics
* :doc:`heap` - Priority queue structures
* :doc:`../../guide/tree_structures/segment_tree` - Segment tree theory and guide

References
==========

.. [1] Cormen, T. H., et al. "Introduction to Algorithms"
.. [2] Halim, S., Halim, F. "Competitive Programming 3"
.. [3] CP-Algorithms. "Segment Tree"
   https://cp-algorithms.com/data_structures/segment_tree.html
.. [4] TopCoder. "Range Minimum Query and Lowest Common Ancestor"
