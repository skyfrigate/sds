.. _api_advanced_lru_cache:

=========
LRU Cache
=========

.. currentmodule:: sds.advanced.lru_cache

.. autoclass:: LRUCache
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
      * - ``get(key)``
        - O(1)
        - Promotes to MRU
      * - ``put(key, value)``
        - O(1)
        - Evicts LRU if full
      * - ``peek(key)``
        - O(1)
        - No recency update
      * - ``delete(key)``
        - O(1)
        - Does not count as eviction
      * - ``__contains__``
        - O(1)
        - No recency update
      * - ``keys()``
        - O(n)
        - LRU → MRU order
      * - ``items()``
        - O(n)
        - LRU → MRU order
      * - ``clear()``
        - O(n)
        - Does not increment evictions
      * - Space
        - O(capacity)
        - Bounded by capacity
