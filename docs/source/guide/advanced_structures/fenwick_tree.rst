.. _guide_advanced_fenwick_tree:

============================
Fenwick Tree — User Guide
============================


Introduction
============

A **Fenwick Tree** (also called a *Binary Indexed Tree*, BIT) maintains a
mutable sequence of numbers and supports two operations in O(log n):

* **Point update**: ``update(i, delta)`` — add *delta* to position *i*
* **Prefix sum query**: ``prefix_sum(i)`` — sum of elements at positions 1..i

Mathematical Foundations
========================

Low-Bit Operation
-----------------

The structure relies entirely on one bitwise operation:

.. math::

   \text{lowbit}(i) = i \mathbin{\&} (-i)

``lowbit(i)`` isolates the least significant set bit of :math:`i`.

.. list-table::
   :header-rows: 1
   :widths: 15 20 20 45

   * - i
     - binary
     - lowbit(i)
     - Coverage
   * - 1
     - 0001
     - 1
     - Covers [1, 1]
   * - 2
     - 0010
     - 2
     - Covers [1, 2]
   * - 4
     - 0100
     - 4
     - Covers [1, 4]
   * - 6
     - 0110
     - 2
     - Covers [5, 6]

Each cell ``_tree[i]`` stores the sum of elements in
:math:`[i - \text{lowbit}(i) + 1,\ i]`.

Update (Upward Propagation)
---------------------------

.. code-block:: python

   while i <= n:
       tree[i] += delta
       i += lowbit(i)    # move toward root

Prefix Sum (Downward Accumulation)
-----------------------------------

.. code-block:: python

   total = 0
   while i > 0:
       total += tree[i]
       i -= lowbit(i)    # move toward 0

Both algorithms execute at most :math:`\lfloor \log_2 n \rfloor + 1`
iterations.

Range Query
-----------

.. math::

   \text{range\_sum}(l, r) = \text{prefix\_sum}(r) - \text{prefix\_sum}(l-1)

Tree Structure (8 elements)
----------------------------

.. mermaid::

   graph TB
       T8["tree[8] = sum(1..8)"]
       T4["tree[4] = sum(1..4)"]
       T6["tree[6] = sum(5..6)"]
       T2["tree[2] = sum(1..2)"]
       T1["tree[1] = A[1]"]
       T3["tree[3] = A[3]"]
       T5["tree[5] = A[5]"]
       T7["tree[7] = A[7]"]
       T8 --> T4
       T8 --> T6
       T4 --> T2
       T4 --> T3
       T6 --> T5
       T6 --> T7
       T2 --> T1

Usage
=====

.. code-block:: python

   from sds.advanced import FenwickTree

   # Build from a list
   ft = FenwickTree.from_list([3, 1, 4, 1, 5, 9, 2, 6])

   # Prefix sum
   print(ft.prefix_sum(4))       # 3+1+4+1 = 9.0
   print(ft.prefix_sum(8))       # total = 31.0

   # Range query
   print(ft.range_sum(3, 6))     # 4+1+5+9 = 19.0

   # Point query
   print(ft.point_query(3))      # 4.0

   # Point update
   ft.update(3, 10)              # A[3] += 10
   print(ft.prefix_sum(4))       # 19.0

   # Total
   print(ft.total())             # 41.0

   # Reconstruct array
   print(ft.to_list())           # [3.0, 1.0, 14.0, 1.0, 5.0, 9.0, 2.0, 6.0]

   # Reset
   ft.clear()
   assert ft.is_empty()

   # Empty construction
   ft2 = FenwickTree(size=10)
   for i, v in enumerate([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], start=1):
       ft2.update(i, v)

.. warning::

   Indexing is **1-based**: valid indices are ``1 .. size``.
   An out-of-bounds index raises
   :exc:`~sds.core.exceptions.IndexStructureError`.

Real-World Use Cases
====================

Frequency Table
---------------

.. code-block:: python

   # Count occurrences of values in [1, 100]
   ft = FenwickTree(size=100)
   data = [3, 7, 3, 1, 7, 7, 5]
   for v in data:
       ft.update(v, 1)

   # How many values ≤ 5?
   print(int(ft.prefix_sum(5)))      # 4  (1, 3, 3, 5)

   # How many values in [3, 7]?
   print(int(ft.range_sum(3, 7)))    # 6

Range Update via Difference Array
----------------------------------

To add *delta* to all elements in ``[l, r]`` in O(log n):

.. code-block:: python

   # Maintain a difference array D
   n = 10
   D = FenwickTree(size=n + 1)   # extra slot for D[n+1]

   def range_update(l, r, delta):
       D.update(l, delta)
       D.update(r + 1, -delta)

   def point_query(i):
       return D.prefix_sum(i)    # A[i] = sum of D[1..i]

   range_update(2, 5, 3)         # A[2..5] += 3
   print(point_query(3))         # 3.0
   print(point_query(6))         # 0.0

Order Statistics
----------------

.. code-block:: python

   # How many elements are ≤ x after n insertions?
   ft = FenwickTree(size=1000)
   values = [42, 17, 99, 17, 42, 55]
   for v in values:
       ft.update(v, 1)

   rank_42 = int(ft.prefix_sum(42))   # elements ≤ 42

Best Practices
==============

✅ Use ``from_list()`` to initialise from an existing array.

✅ Use ``range_sum(l, r)`` directly — more readable than manual subtraction.

✅ Use the difference array trick for bulk range updates.

❌ Do not confuse 1-based indexing (FenwickTree) with 0-based (Python lists).

❌ Do not call ``prefix_sum(0)`` — raises ``IndexStructureError``.

References
==========

.. [1] Fenwick, P. M. (1994). "A new data structure for cumulative frequency
   tables". *Software: Practice and Experience*, 24(3), 327-336.
   DOI: `10.1002/spe.4380240306 <https://doi.org/10.1002/spe.4380240306>`_

.. [2] OpenDSA — Binary Indexed Tree.
   https://opendsa-server.cs.vt.edu/ODSA/Books/Everything/html/BinaryIndexedTree.html

See Also
========

* :ref:`api_advanced_fenwick_tree` — API Reference
* :ref:`guide_advanced_count_min_sketch` — Frequency estimation over streams
