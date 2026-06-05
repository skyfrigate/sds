.. _api_linear_list:

============
Linked Lists
============

.. currentmodule:: sds.linear.list

Overview
========

This module provides concrete implementations of linked list variants. Linked lists
are fundamental linear data structures where elements are connected via references
rather than being stored contiguously in memory.

.. mermaid::

   graph LR
       subgraph "Singly Linked List"
       A1[1] --> B1[2]
       B1 --> C1[3]
       C1 --> D1[None]
       end

       subgraph "Doubly Linked List"
       A2[1] <--> B2[2]
       B2 <--> C2[3]
       end

       subgraph "Circular Linked List"
       A3[1] --> B3[2]
       B3 --> C3[3]
       C3 --> A3
       end

       style A1 fill:#e74c3c
       style A2 fill:#3498db
       style A3 fill:#2ecc71

Classes
=======

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   LinkedList
   DoublyLinkedList
   CircularLinkedList

Detailed Documentation
======================

LinkedList
----------

.. autoclass:: LinkedList
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __len__, __iter__, __contains__, __getitem__, __setitem__, __repr__, __str__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Properties

   .. autoproperty:: head
   .. autoproperty:: size

   .. rubric:: Core Operations

   .. automethod:: prepend
   .. automethod:: append
   .. automethod:: insert_at

   .. rubric:: Removal Operations

   .. automethod:: remove_first
   .. automethod:: remove_last
   .. automethod:: remove
   .. automethod:: remove_at

   .. rubric:: Query Methods

   .. automethod:: find

   .. rubric:: Utility Methods

   .. automethod:: reverse
   .. automethod:: clear

   .. rubric:: Special Methods

   .. automethod:: __len__
   .. automethod:: __iter__
   .. automethod:: __contains__
   .. automethod:: __getitem__
   .. automethod:: __setitem__
   .. automethod:: __repr__
   .. automethod:: __str__

DoublyLinkedList
----------------

.. autoclass:: DoublyLinkedList
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __len__, __iter__, __reversed__, __contains__, __getitem__, __setitem__, __repr__, __str__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Properties

   .. autoproperty:: head
   .. autoproperty:: tail
   .. autoproperty:: size

   .. rubric:: Core Operations

   .. automethod:: prepend
   .. automethod:: append
   .. automethod:: insert_at

   .. rubric:: Removal Operations

   .. automethod:: remove_first
   .. automethod:: remove_last
   .. automethod:: remove
   .. automethod:: remove_at

   .. rubric:: Query Methods

   .. automethod:: find

   .. rubric:: Utility Methods

   .. automethod:: reverse
   .. automethod:: clear

   .. rubric:: Special Methods

   .. automethod:: __len__
   .. automethod:: __iter__
   .. automethod:: __reversed__
   .. automethod:: __contains__
   .. automethod:: __getitem__
   .. automethod:: __setitem__
   .. automethod:: __repr__
   .. automethod:: __str__

CircularLinkedList
------------------

.. autoclass:: CircularLinkedList
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __len__, __iter__, __contains__, __getitem__, __setitem__, __repr__, __str__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Properties

   .. autoproperty:: tail
   .. autoproperty:: head
   .. autoproperty:: size

   .. rubric:: Core Operations

   .. automethod:: prepend
   .. automethod:: append
   .. automethod:: insert_at

   .. rubric:: Removal Operations

   .. automethod:: remove_first
   .. automethod:: remove_last
   .. automethod:: remove
   .. automethod:: remove_at

   .. rubric:: Query Methods

   .. automethod:: find

   .. rubric:: Utility Methods

   .. automethod:: reverse
   .. automethod:: rotate
   .. automethod:: clear

   .. rubric:: Special Methods

   .. automethod:: __len__
   .. automethod:: __iter__
   .. automethod:: __contains__
   .. automethod:: __getitem__
   .. automethod:: __setitem__
   .. automethod:: __repr__
   .. automethod:: __str__

Usage Examples
==============

LinkedList Examples
-------------------

Basic Operations
^^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.linear import LinkedList

   # Create and populate
   lst = LinkedList()
   lst.append(1)
   lst.append(2)
   lst.append(3)
   
   print(len(lst))    # 3
   print(list(lst))   # [1, 2, 3]

Insertion
^^^^^^^^^

.. code-block:: python

   lst = LinkedList()
   
   # Insert at beginning - O(1)
   lst.prepend(3)
   lst.prepend(2)
   lst.prepend(1)
   print(list(lst))  # [1, 2, 3]
   
   # Insert at end - O(n)
   lst.append(4)
   print(list(lst))  # [1, 2, 3, 4]
   
   # Insert at index - O(n)
   lst.insert_at(2, 99)
   print(list(lst))  # [1, 2, 99, 3, 4]

Removal
^^^^^^^

.. code-block:: python

   # Remove first - O(1)
   first = lst.remove_first()
   print(first)       # 1
   
   # Remove last - O(n)
   last = lst.remove_last()
   print(last)        # 4
   
   # Remove by value - O(n)
   lst.remove(99)
   print(list(lst))   # [2, 3]
   
   # Remove at index - O(n)
   item = lst.remove_at(0)
   print(item)        # 2

Access and Search
^^^^^^^^^^^^^^^^^

.. code-block:: python

   lst = LinkedList()
   for i in range(5):
       lst.append(i)
   
   # Index access - O(n)
   print(lst[2])      # 2
   lst[2] = 99
   print(lst[2])      # 99
   
   # Search - O(n)
   index = lst.find(99)
   print(index)       # 2
   
   # Contains - O(n)
   print(99 in lst)   # True
   print(100 in lst)  # False

Reversal
^^^^^^^^

.. code-block:: python

   lst = LinkedList()
   for i in range(1, 6):
       lst.append(i)
   
   print(list(lst))   # [1, 2, 3, 4, 5]
   
   lst.reverse()
   print(list(lst))   # [5, 4, 3, 2, 1]

DoublyLinkedList Examples
--------------------------

Basic Operations
^^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.linear import DoublyLinkedList

   # Create and populate
   dll = DoublyLinkedList()
   dll.append(1)
   dll.append(2)
   dll.append(3)
   
   print(len(dll))    # 3
   print(list(dll))   # [1, 2, 3]

Bidirectional Traversal
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   dll = DoublyLinkedList()
   for i in range(1, 4):
       dll.append(i)
   
   # Forward iteration
   print(list(dll))           # [1, 2, 3]
   
   # Backward iteration
   print(list(reversed(dll))) # [3, 2, 1]

Efficient End Operations
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   dll = DoublyLinkedList()
   
   # Both O(1)
   dll.prepend(2)
   dll.append(3)
   dll.prepend(1)
   dll.append(4)
   
   print(list(dll))   # [1, 2, 3, 4]
   
   # Both O(1)
   first = dll.remove_first()
   last = dll.remove_last()
   
   print(first, last) # 1 4
   print(list(dll))   # [2, 3]

Optimized Index Access
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   dll = DoublyLinkedList()
   for i in range(100):
       dll.append(i)
   
   # Accessing near end is faster
   # Starts from tail for indices in second half
   print(dll[90])  # Faster: starts from tail
   print(dll[10])  # Starts from head

CircularLinkedList Examples
----------------------------

Basic Operations
^^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.linear import CircularLinkedList

   # Create and populate
   cll = CircularLinkedList()
   cll.append(1)
   cll.append(2)
   cll.append(3)
   
   print(len(cll))    # 3
   print(list(cll))   # [1, 2, 3]

Circular Structure
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   cll = CircularLinkedList()
   cll.append(1)
   cll.append(2)
   cll.append(3)
   
   # Tail points back to head
   print(cll.tail.next is cll.head)  # True
   
   # Visual: 1 -> 2 -> 3 -> (back to 1)

Rotation
^^^^^^^^

.. code-block:: python

   cll = CircularLinkedList()
   for i in range(1, 6):
       cll.append(i)
   
   print(list(cll))   # [1, 2, 3, 4, 5]
   
   # Rotate forward - O(1)
   cll.rotate(1)
   print(list(cll))   # [2, 3, 4, 5, 1]
   
   cll.rotate(2)
   print(list(cll))   # [4, 5, 1, 2, 3]
   
   # Rotate backward
   cll.rotate(-1)
   print(list(cll))   # [3, 4, 5, 1, 2]

Round-Robin Processing
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Simulate round-robin scheduling
   tasks = CircularLinkedList()
   for i in range(1, 4):
       tasks.append(f"Task{i}")
   
   # Process tasks in rotation
   for _ in range(6):
       print(tasks.head.data)
       tasks.rotate(1)
   
   # Output:
   # Task1
   # Task2
   # Task3
   # Task1
   # Task2
   # Task3

Real-World Examples
===================

Example 1: Browser History (LinkedList)
----------------------------------------

.. code-block:: python

   from sds.linear import LinkedList

   class BrowserHistory:
       """Browser history using linked list."""
       
       def __init__(self):
           self.history = LinkedList()
           self.current_index = -1
       
       def visit(self, url):
           """Visit new page."""
           # Remove forward history
           while len(self.history) > self.current_index + 1:
               self.history.remove_last()
           
           # Add new page
           self.history.append(url)
           self.current_index += 1
       
       def back(self):
           """Go back one page."""
           if self.current_index > 0:
               self.current_index -= 1
               return self.history[self.current_index]
           return None
       
       def forward(self):
           """Go forward one page."""
           if self.current_index < len(self.history) - 1:
               self.current_index += 1
               return self.history[self.current_index]
           return None
       
       def current_page(self):
           """Get current page."""
           if self.current_index >= 0:
               return self.history[self.current_index]
           return None
   
   # Usage
   browser = BrowserHistory()
   browser.visit("google.com")
   browser.visit("github.com")
   browser.visit("stackoverflow.com")
   
   print(browser.current_page())  # stackoverflow.com
   print(browser.back())          # github.com
   print(browser.back())          # google.com
   print(browser.forward())       # github.com

Example 2: LRU Cache (DoublyLinkedList)
----------------------------------------

.. code-block:: python

   from sds.linear import DoublyLinkedList

   class LRUCache:
       """LRU Cache using doubly linked list."""
       
       def __init__(self, capacity):
           self.capacity = capacity
           self.cache = {}  # key -> (value, node_ref)
           self.order = DoublyLinkedList()  # Most recent at front
       
       def get(self, key):
           """Get value and mark as recently used."""
           if key not in self.cache:
               return None
           
           value = self.cache[key]
           
           # Move to front (most recent)
           self.order.remove(key)
           self.order.prepend(key)
           
           return value
       
       def put(self, key, value):
           """Put key-value pair."""
           if key in self.cache:
               # Update existing
               self.cache[key] = value
               self.order.remove(key)
               self.order.prepend(key)
           else:
               # Add new
               if len(self.cache) >= self.capacity:
                   # Evict least recently used
                   lru_key = self.order.remove_last()
                   del self.cache[lru_key]
               
               self.cache[key] = value
               self.order.prepend(key)
   
   # Usage
   cache = LRUCache(capacity=3)
   
   cache.put("a", 1)
   cache.put("b", 2)
   cache.put("c", 3)
   print(cache.get("a"))  # 1
   
   cache.put("d", 4)  # Evicts "b" (least recent)
   print(cache.get("b"))  # None (evicted)

Example 3: Music Playlist (CircularLinkedList)
-----------------------------------------------

.. code-block:: python

   from sds.linear import CircularLinkedList

   class MusicPlaylist:
       """Music playlist with repeat mode."""
       
       def __init__(self):
           self.songs = CircularLinkedList()
           self.repeat_mode = True
       
       def add_song(self, song):
           """Add song to playlist."""
           self.songs.append(song)
       
       def remove_song(self, song):
           """Remove song from playlist."""
           self.songs.remove(song)
       
       def play_next(self):
           """Get next song."""
           if self.songs.is_empty():
               return None
           
           song = self.songs.head.data
           
           if self.repeat_mode:
               # Rotate for circular play
               self.songs.rotate(1)
           
           return song
       
       def shuffle(self):
           """Shuffle playlist."""
           import random
           songs_list = list(self.songs)
           random.shuffle(songs_list)
           
           self.songs.clear()
           for song in songs_list:
               self.songs.append(song)
       
       def set_repeat(self, enabled):
           """Toggle repeat mode."""
           self.repeat_mode = enabled
   
   # Usage
   playlist = MusicPlaylist()
   playlist.add_song("Song A")
   playlist.add_song("Song B")
   playlist.add_song("Song C")
   
   # Play in repeat
   for _ in range(5):
       print(playlist.play_next())
   # Output: Song A, Song B, Song C, Song A, Song B

Performance Characteristics
===========================

Time Complexity
---------------

.. list-table::
   :header-rows: 1
   :widths: 30 15 20 20

   * - Operation
     - LinkedList
     - DoublyLinkedList
     - CircularLinkedList
   * - ``prepend()``
     - O(1)
     - O(1)
     - O(1)
   * - ``append()``
     - O(n)
     - O(1)
     - O(1)
   * - ``insert_at(i)``
     - O(n)
     - O(n)
     - O(n)
   * - ``remove_first()``
     - O(1)
     - O(1)
     - O(1)
   * - ``remove_last()``
     - O(n)
     - O(1)
     - O(n)
   * - ``remove_at(i)``
     - O(n)
     - O(n)
     - O(n)
   * - ``remove(item)``
     - O(n)
     - O(n)
     - O(n)
   * - ``find(item)``
     - O(n)
     - O(n)
     - O(n)
   * - ``reverse()``
     - O(n)
     - O(n)
     - O(n)
   * - ``rotate(k)``
     - N/A
     - N/A
     - O(k)
   * - ``__getitem__[i]``
     - O(n)
     - O(n/2)
     - O(n)
   * - ``__setitem__[i]``
     - O(n)
     - O(n/2)
     - O(n)

Space Complexity
----------------

* **LinkedList**: O(n) + O(n) for references
* **DoublyLinkedList**: O(n) + O(2n) for references
* **CircularLinkedList**: O(n) + O(n) for references

Comparison Summary
==================

.. list-table::
   :header-rows: 1
   :widths: 25 20 25 30

   * - Feature
     - LinkedList
     - DoublyLinkedList
     - CircularLinkedList
   * - **Memory**
     - Lowest
     - Highest
     - Medium
   * - **Append**
     - O(n)
     - O(1)
     - O(1)
   * - **Remove Last**
     - O(n)
     - O(1)
     - O(n)
   * - **Backward Iter**
     - No
     - Yes
     - No
   * - **Rotation**
     - No
     - No
     - Yes O(k)
   * - **Best For**
     - Simple cases
     - Bidirectional
     - Circular ops

Best Practices
==============

Do's
----

✅ **Choose based on operations**

.. code-block:: python

   # Frequent append → DoublyLinkedList or CircularLinkedList
   dll = DoublyLinkedList()
   
   # Only prepend → LinkedList is fine
   lst = LinkedList()
   
   # Need rotation → CircularLinkedList
   cll = CircularLinkedList()

✅ **Use iteration, not indexing**

.. code-block:: python

   # Good: O(n) total
   for item in lst:
       process(item)
   
   # Bad: O(n²) total
   for i in range(len(lst)):
       process(lst[i])

✅ **Cache frequently accessed elements**

.. code-block:: python

   # Cache instead of repeated access
   first_item = lst[0]
   # Use first_item multiple times

Don'ts
------

❌ **Don't use for random access**

.. code-block:: python

   # Bad: Linked lists are slow for random access
   # Use Python list instead if you need this
   for i in [5, 10, 15, 20]:
       print(lst[i])  # Each access is O(n)

❌ **Don't forget complexity differences**

.. code-block:: python

   # LinkedList.append() is O(n)
   # DoublyLinkedList.append() is O(1)
   # Choose appropriately!

❌ **Don't modify during iteration**

.. code-block:: python

   # Bad: Undefined behavior
   for item in lst:
       lst.remove(item)
   
   # Good: Collect first
   to_remove = list(lst)
   for item in to_remove:
       lst.remove(item)

Common Pitfalls
===============

1. **Using wrong list type**

.. code-block:: python

   # If you need O(1) append, use DoublyLinkedList
   # not LinkedList

2. **Repeated indexing**

.. code-block:: python

   # Expensive: O(n) each time
   for i in range(len(lst)):
       print(lst[i])
   
   # Efficient: O(n) total
   for item in lst:
       print(item)

3. **Ignoring negative indices**

.. code-block:: python

   # Both lists support negative indices
   last = lst[-1]  # Works!

See Also
========

* :doc:`interfaces` - Abstract linked list interface
* :doc:`node` - Node implementations
* :doc:`../../guide/linear_structures/linked_list` - Linked list guide

References
==========

.. [1] Knuth, D. E. "The Art of Computer Programming, Volume 1", Section 2.2
.. [2] Cormen, T. H., et al. "Introduction to Algorithms", 3rd Edition, Chapter 10
.. [3] Sedgewick, R., Wayne, K. "Algorithms", 4th Edition, Section 1.3
