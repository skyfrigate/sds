.. _api_advanced_skip_list:

=========
Skip List
=========

.. currentmodule:: sds.advanced.skip_list

.. autoclass:: SkipList
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
      * - ``insert(key, value)``
        - O(log n)*
        - Updates value if key exists
      * - ``delete(key)``
        - O(log n)*
        - Returns False if absent
      * - ``search(key)``
        - O(log n)*
        - Returns None if absent
      * - ``__contains__(key)``
        - O(log n)*
        - No false negatives
      * - ``min_key()``
        - O(1)
        - First node in base list
      * - ``max_key()``
        - O(n)
        - Traverses base list
      * - ``items()``
        - O(n)
        - Sorted key-value pairs
      * - ``__iter__``
        - O(n)
        - Sorted ascending
      * - ``clear()``
        - O(1)
        - Resets sentinel pointers
      * - Space
        - O(n log n)*
        - Expected with p=0.5

   \\* Expected/amortised — p = promotion probability
