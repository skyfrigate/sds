.. _api_algorithms_sorting:

========================
Sorting Algorithms
========================

.. currentmodule:: sds.algorithms.sorting

Overview
========

This subpackage provides two comparison sorts, chosen because they sit at
opposite ends of the classic trade-offs:

* **Merge sort** is *stable* and returns a *new* list; it runs in
  :math:`O(n \log n)` whatever the input, at the cost of :math:`O(n)` extra
  memory.
* **Quicksort** sorts *in place* with :math:`O(\log n)` extra memory and is
  usually faster in practice, but it is *not stable* and its worst case is
  :math:`O(n^2)`.

Both accept the ``key`` and ``reverse`` keywords of the built-in
:func:`sorted`, and both operate on a Python ``list`` only.

.. note::

   Why a ``list`` and not a linked list? Both algorithms rely on indexed
   access. On a linked list, ``structure[i]`` walks the chain and costs
   :math:`O(n)`, which would turn an :math:`O(n \log n)` sort into an
   :math:`O(n^2 \log n)` one. To sort the content of a linear structure,
   convert it first with :func:`sds.linear.to_list` and rebuild it with
   :func:`sds.linear.from_list`.

Mathematical Foundation
=======================

A **comparison sort** only learns about the order of its input by comparing
pairs of keys. Any such algorithm can be pictured as a binary decision tree
whose leaves are the :math:`n!` possible orderings, so its height, the
worst-case number of comparisons, satisfies

.. math::

   h \;\geq\; \log_2(n!) \;=\; \Theta(n \log n).

Merge sort meets this bound in every case, and quicksort meets it on
average: neither can be improved by more than a constant factor without
leaving the comparison model.

A sort is **stable** if items with equal keys keep their original relative
order. Stability matters when sorting by one key after another: sorting
records by name, then stably by department, yields records ordered by
department and, within a department, by name.

Merge Sort
==========

.. mermaid::

   graph TD
       A["[5, 2, 4, 1]"] --> B["[5, 2]"]
       A --> C["[4, 1]"]
       B --> D["[5]"]
       B --> E["[2]"]
       C --> F["[4]"]
       C --> G["[1]"]
       D --> H["[2, 5]"]
       E --> H
       F --> I["[1, 4]"]
       G --> I
       H --> J["[1, 2, 4, 5]"]
       I --> J

       style A fill:#3498db,color:#fff
       style J fill:#2ecc71,color:#fff

The input is split in halves down to single elements (top), then the
sorted halves are merged back pairwise (bottom). When the two candidates of
a merge compare equal, the element of the *left* half is taken first, which
is exactly what makes the algorithm stable.

.. autofunction:: merge_sort

Quicksort
=========

.. mermaid::

   graph TD
       A["[5, 2, 8, 1, 9, 3]<br/>pivot = median(5, 8, 3) = 5"] --> B["[3, 2, 1] ≤ 5"]
       A --> C["[9, 8, 5] ≥ 5"]
       B --> D["[1, 2, 3]"]
       C --> E["[5, 8, 9]"]
       D --> F["[1, 2, 3, 5, 8, 9]"]
       E --> F

       style A fill:#3498db,color:#fff
       style F fill:#2ecc71,color:#fff

Each partition step moves keys that come before the pivot to the left and
keys that come after it to the right, then both parts are sorted
independently. The implementation combines three standard refinements:
Hoare partitioning (robust to many equal keys), a median-of-three pivot
(sorted and reverse-sorted inputs are no longer worst cases), and recursion
on the smaller part only (the call stack stays :math:`O(\log n)` deep).

.. autofunction:: quick_sort

Comparison
==========

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Property
     - ``merge_sort``
     - ``quick_sort``
   * - Best / average time
     - :math:`O(n \log n)`
     - :math:`O(n \log n)`
   * - Worst-case time
     - :math:`O(n \log n)`
     - :math:`O(n^2)`
   * - Extra space
     - :math:`O(n)`
     - :math:`O(\log n)` (+ :math:`O(n)` with ``key``)
   * - Stable
     - Yes
     - No
   * - Input
     - Left unchanged
     - Sorted in place
   * - Returns
     - A new ``list``
     - ``None``

Usage Examples
==============

Sorting records by several keys
-------------------------------

Stability lets a secondary order survive a later sort on the primary key:

.. code-block:: python

   from sds.algorithms.sorting import merge_sort

   staff = [("Lina", "R&D"), ("Ahmed", "Sales"), ("Zoé", "R&D"), ("Bo", "Sales")]

   by_name = merge_sort(staff, key=lambda p: p[0])
   by_team = merge_sort(by_name, key=lambda p: p[1])
   # [('Lina', 'R&D'), ('Zoé', 'R&D'), ('Ahmed', 'Sales'), ('Bo', 'Sales')]

Sorting a large list in place
-----------------------------

.. code-block:: python

   import random
   from sds.algorithms.sorting import quick_sort

   data = [random.random() for _ in range(100_000)]
   quick_sort(data)            # data is now sorted; nothing is returned
   quick_sort(data, reverse=True)

Sorting a linear structure
--------------------------

.. code-block:: python

   from sds.linear import Queue, from_list, to_list
   from sds.algorithms.sorting import merge_sort

   queue = from_list(Queue, [3, 1, 2])
   queue = from_list(Queue, merge_sort(to_list(queue)))
   print(to_list(queue))       # [1, 2, 3]

Best Practices
==============

✅ Use ``merge_sort`` when equal keys must keep their order, or when the
original list must stay untouched.

✅ Use ``quick_sort`` when memory matters and stability does not.

✅ Pass ``key`` rather than pre-building ``(key, item)`` tuples: the key is
computed once per item and items themselves are never compared.

❌ Do not pass a linked structure directly; convert it with ``to_list()``
first.

References
==========

* OpenDSA, *Mergesort* and *Quicksort* chapters —
  https://opendsa-server.cs.vt.edu/ODSA/Books/Everything/html/Mergesort.html,
  https://opendsa-server.cs.vt.edu/ODSA/Books/Everything/html/Quicksort.html
* R. Sedgewick and K. Wayne, *Algorithms, 4th Edition*, sections 2.2 and 2.3
  (free online companion) — https://algs4.cs.princeton.edu/22mergesort/,
  https://algs4.cs.princeton.edu/23quicksort/
* Python documentation, *Sorting Techniques* (stability and multi-key
  sorts) — https://docs.python.org/3/howto/sorting.html
