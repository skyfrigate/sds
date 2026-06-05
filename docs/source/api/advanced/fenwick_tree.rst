.. _api_advanced_fenwick_tree:

============
Fenwick Tree
============

.. currentmodule:: sds.advanced.fenwick_tree

.. autoclass:: FenwickTree
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __contains__, __len__, __iter__, __repr__, __str__

   .. rubric:: Complexity Summary

   .. list-table::
      :header-rows: 1
      :widths: 30 20 50

      * - Operation
        - Complexity
        - Notes
      * - ``update(i, delta)``
        - O(log n)
        - 1-based index; may be negative
      * - ``prefix_sum(i)``
        - O(log n)
        - Sum of positions 1..i
      * - ``range_sum(l, r)``
        - O(log n)
        - prefix_sum(r) − prefix_sum(l−1)
      * - ``point_query(i)``
        - O(log n)
        - prefix_sum(i) − prefix_sum(i−1)
      * - ``total()``
        - O(log n)
        - Equivalent to prefix_sum(size)
      * - ``to_list()``
        - O(n log n)
        - Reconstructs all values
      * - ``from_list(values)``
        - O(n log n)
        - Class method constructor
      * - ``clear()``
        - O(n)
        - Resets all counters to 0
      * - Space
        - O(n)
        - One array of size n+1

   .. note::

      Indexing is **1-based**: valid indices are ``1 .. size``.
      :exc:`~sds.core.exceptions.IndexStructureError` is raised for
      out-of-bounds access.
