.. _guide_linear_list:

==================
Linked Lists Guide
==================

.. currentmodule:: sds.linear

Introduction
============

**Linked lists** are fundamental linear data structures where elements are stored
in nodes connected by references (pointers) rather than in contiguous memory locations.
Unlike arrays, linked lists do not require contiguous memory allocation, making them
highly flexible for dynamic insertion and deletion operations.

Types of Linked Lists
----------------------

There are three main variants of linked lists, each with specific use cases and
characteristics:

Singly Linked List
^^^^^^^^^^^^^^^^^^

In a **singly linked list**, each node contains data and a reference to the **next**
node in the sequence. Traversal is unidirectional (forward only).

.. mermaid::

   flowchart LR
       A1[Node 1<br/>data: 10<br/>next →] -->|next| A2[Node 2<br/>data: 20<br/>next →]
       A2 -->|next| A3[Node 3<br/>data: 30<br/>next →]
       A3 -->|next| A4[null]

       style A1 fill:#3498db,color:#fff
       style A2 fill:#3498db,color:#fff
       style A3 fill:#3498db,color:#fff
       style A4 fill:#95a5a6,color:#fff

**Characteristics:**

* **Memory efficient**: Only one pointer per node
* **Forward traversal only**: Cannot move backward
* **Prepend**: O(1) - efficient insertion at head
* **Append**: O(n) without tail pointer, O(1) with tail pointer
* **Best for**: Stacks, forward-only iteration

Doubly Linked List
^^^^^^^^^^^^^^^^^^

In a **doubly linked list**, each node contains data and references to both the
**next** and **previous** nodes. This enables bidirectional traversal.

.. mermaid::

   flowchart LR
       B1["Node 1<br/>data: 10<br/>prev | next"] <-->|"prev/next"| B2["Node 2<br/>data: 20<br/>prev | next"]
       B2 <-->|"prev/next"| B3["Node 3<br/>data: 30<br/>prev | next"]

       N1[null] -.->|"prev"| B1
       B3 -.->|"next"| N2[null]

       style B1 fill:#f39c12,color:#fff
       style B2 fill:#f39c12,color:#fff
       style B3 fill:#f39c12,color:#fff
       style N1 fill:#95a5a6,color:#fff
       style N2 fill:#95a5a6,color:#fff

**Characteristics:**

* **Bidirectional**: Can traverse forward and backward
* **Extra memory**: Two pointers per node
* **Efficient operations at both ends**: O(1) prepend and append
* **Remove from tail**: O(1) (unlike singly linked)
* **Best for**: Deques, LRU cache, undo/redo systems

Circular Linked List
^^^^^^^^^^^^^^^^^^^^

In a **circular linked list**, the last node points back to the first node,
forming a cycle. No node points to null.

.. mermaid::

   flowchart LR
       C1[Node 1<br/>data: 10] -->|next| C2[Node 2<br/>data: 20]
       C2 -->|next| C3[Node 3<br/>data: 30]
       C3 -->|next| C1

       style C1 fill:#e74c3c,color:#fff
       style C2 fill:#e74c3c,color:#fff
       style C3 fill:#e74c3c,color:#fff

**Characteristics:**

* **No endpoints**: Circular structure with no null references
* **Continuous traversal**: Can loop indefinitely through nodes
* **Rotation operations**: Efficient O(1) rotation
* **Risk**: Easy to create infinite loops if not handled carefully
* **Best for**: Round-robin scheduling, circular buffers, music playlists

Choosing the Right Type
^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 25 25 25

   * - Feature
     - Singly Linked
     - Doubly Linked
     - Circular
   * - **Memory per node**
     - 1 pointer
     - 2 pointers
     - 1+ pointers
   * - **Traversal**
     - Forward only
     - Bidirectional
     - Continuous loop
   * - **Remove from tail**
     - O(n)
     - O(1)
     - O(n)
   * - **Complexity**
     - Simple
     - Moderate
     - Moderate
   * - **Typical use**
     - Stacks, queues
     - Deques, caches
     - Schedulers, playlists

Mathematical Model
==================

Formal Definition
-----------------

A linked list :math:`L` is a sequence of nodes:

.. math::

   L = \langle n_1, n_2, \ldots, n_k \rangle

where each node :math:`n_i` contains:
   * **data**: :math:`d_i \in D` (data domain)
   * **next**: :math:`n_{i+1}` or :math:`\text{null}`

For doubly linked lists, nodes also contain:
   * **prev**: :math:`n_{i-1}` or :math:`\text{null}`

Node Structure
--------------

**Singly Linked Node:**

.. math::

   Node_s = (data, next)

**Doubly Linked Node:**

.. math::

   Node_d = (data, next, prev)

Operations
----------

Insertion Operations
^^^^^^^^^^^^^^^^^^^^

**Prepend** (insert at head):

.. math::

   prepend(L, x) = \langle n_{new}, n_1, n_2, \ldots, n_k \rangle

where :math:`n_{new}.data = x` and :math:`n_{new}.next = n_1`

**Append** (insert at tail):

.. math::

   append(L, x) = \langle n_1, n_2, \ldots, n_k, n_{new} \rangle

where :math:`n_{new}.data = x` and :math:`n_k.next = n_{new}`

**Insert at position** :math:`i`:

.. math::

   insert\_at(L, i, x) = \langle n_1, \ldots, n_{i-1}, n_{new}, n_i, \ldots, n_k \rangle

Deletion Operations
^^^^^^^^^^^^^^^^^^^

**Remove first:**

.. math::

   remove\_first(\langle n_1, n_2, \ldots, n_k \rangle) = (n_1.data, \langle n_2, \ldots, n_k \rangle)

**Remove last:**

.. math::

   remove\_last(\langle n_1, \ldots, n_{k-1}, n_k \rangle) = (n_k.data, \langle n_1, \ldots, n_{k-1} \rangle)

List Properties
---------------

**Length:**

.. math::

   |L| = k \text{ where } L = \langle n_1, \ldots, n_k \rangle

**Access by index:**

.. math::

   L[i] = n_i.data \text{ for } 0 \leq i < k

**Invariants:**

1. **Chain integrity**: :math:`\forall i < k : n_i.next = n_{i+1}`
2. **Bidirectional consistency** (doubly linked): :math:`n_i.next.prev = n_i`
3. **Circularity** (circular): :math:`n_k.next = n_1`

Algorithmic Model
=================

Singly Linked List ADT
-----------------------

.. code-block:: text

   ADT LinkedList:
       Data:
           - head: reference to first node
           - size: number of nodes
       
       Node:
           - data: any type
           - next: reference to next node
       
       Operations:
           - LinkedList(): create empty list
           - prepend(item): add at beginning O(1)
           - append(item): add at end O(n) [O(1) with tail]
           - insert_at(index, item): insert at position O(n)
           - remove_first(): remove first O(1)
           - remove_last(): remove last O(n)
           - find(item): search for item O(n)
           - reverse(): reverse in place O(n)

Implementation Algorithms
-------------------------

Prepend (Insert at Head)
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   Algorithm: PREPEND(L, item)
   Input: LinkedList L, element item
   Output: Modified list L
   Time: O(1)
   
   1. new_node ← Node(item)
   2. new_node.next ← L.head
   3. L.head ← new_node
   4. L.size ← L.size + 1

Append (Insert at Tail)
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   Algorithm: APPEND(L, item)
   Input: LinkedList L, element item
   Output: Modified list L
   Time: O(n) without tail pointer
   
   1. new_node ← Node(item)
   2. if L.head = null then
   3.     L.head ← new_node
   4. else
   5.     current ← L.head
   6.     while current.next ≠ null do
   7.         current ← current.next
   8.     end while
   9.     current.next ← new_node
   10. end if
   11. L.size ← L.size + 1

Insert at Index
^^^^^^^^^^^^^^^

.. code-block:: text

   Algorithm: INSERT_AT(L, index, item)
   Input: LinkedList L, index i, element item
   Output: Modified list L
   Time: O(n)
   
   1. if index < 0 or index > L.size then
   2.     raise IndexError
   3. end if
   4. if index = 0 then
   5.     PREPEND(L, item)
   6. else
   7.     prev ← GET_NODE(L, index - 1)
   8.     new_node ← Node(item)
   9.     new_node.next ← prev.next
   10.     prev.next ← new_node
   11.     L.size ← L.size + 1
   12. end if

Remove First
^^^^^^^^^^^^

.. code-block:: text

   Algorithm: REMOVE_FIRST(L)
   Input: LinkedList L
   Output: Removed element
   Time: O(1)
   
   1. if L.head = null then
   2.     raise EmptyStructureError
   3. end if
   4. data ← L.head.data
   5. L.head ← L.head.next
   6. L.size ← L.size - 1
   7. return data

Reverse
^^^^^^^

.. code-block:: text

   Algorithm: REVERSE(L)
   Input: LinkedList L
   Output: Reversed list L
   Time: O(n), Space: O(1)
   
   1. prev ← null
   2. current ← L.head
   3. while current ≠ null do
   4.     next ← current.next
   5.     current.next ← prev
   6.     prev ← current
   7.     current ← next
   8. end while
   9. L.head ← prev

Doubly Linked List Algorithms
------------------------------

Insert at Head
^^^^^^^^^^^^^^

.. code-block:: text

   Algorithm: PREPEND_DOUBLY(L, item)
   Time: O(1)
   
   1. new_node ← DoublyNode(item, next=L.head)
   2. if L.head ≠ null then
   3.     L.head.prev ← new_node
   4. else
   5.     L.tail ← new_node
   6. end if
   7. L.head ← new_node
   8. L.size ← L.size + 1

Insert at Tail
^^^^^^^^^^^^^^

.. code-block:: text

   Algorithm: APPEND_DOUBLY(L, item)
   Time: O(1) with tail pointer
   
   1. new_node ← DoublyNode(item, prev=L.tail)
   2. if L.tail ≠ null then
   3.     L.tail.next ← new_node
   4. else
   5.     L.head ← new_node
   6. end if
   7. L.tail ← new_node
   8. L.size ← L.size + 1

Complexity Analysis
-------------------

.. list-table::
   :header-rows: 1
   :widths: 30 20 20 20 10

   * - Operation
     - Singly
     - Doubly
     - Circular
     - Array
   * - **Access by index**
     - O(n)
     - O(n/2)*
     - O(n)
     - O(1)
   * - **Search**
     - O(n)
     - O(n)
     - O(n)
     - O(n)
   * - **Prepend**
     - O(1)
     - O(1)
     - O(1)
     - O(n)
   * - **Append**
     - O(n)**
     - O(1)
     - O(1)
     - O(1)***
   * - **Insert at i**
     - O(n)
     - O(n)
     - O(n)
     - O(n)
   * - **Remove first**
     - O(1)
     - O(1)
     - O(1)
     - O(n)
   * - **Remove last**
     - O(n)
     - O(1)
     - O(n)
     - O(1)
   * - **Reverse**
     - O(n)
     - O(n)
     - O(n)
     - O(n)
   * - **Space**
     - O(n)
     - O(n)
     - O(n)
     - O(n)

\* Can start from nearest end

\** O(1) with tail pointer

\*** Amortized

Practical Usage
===============

Singly Linked List
------------------

.. code-block:: python

   from sds.linear import LinkedList
   
   # Create and populate
   lst = LinkedList()
   lst.append(10)
   lst.append(20)
   lst.append(30)
   lst.prepend(5)
   
   # Access
   print(lst[0])        # Output: 5
   print(lst[-1])       # Output: 30
   
   # Modify
   lst[1] = 15
   lst.insert_at(2, 17)
   
   # Iterate
   for item in lst:
       print(item)
   
   # Operations
   lst.reverse()
   print(list(lst))     # Output: [30, 20, 17, 15, 5]

Doubly Linked List
------------------

.. code-block:: python

   from sds.linear import DoublyLinkedList
   
   dll = DoublyLinkedList()
   dll.append(1)
   dll.append(2)
   dll.append(3)
   
   # Bidirectional iteration
   print(list(dll))           # Forward: [1, 2, 3]
   print(list(reversed(dll))) # Backward: [3, 2, 1]
   
   # Efficient operations at both ends
   dll.prepend(0)     # O(1)
   dll.append(4)      # O(1)
   dll.remove_first() # O(1)
   dll.remove_last()  # O(1)

Circular Linked List
--------------------

.. code-block:: python

   from sds.linear import CircularLinkedList
   
   cll = CircularLinkedList()
   cll.append(1)
   cll.append(2)
   cll.append(3)
   
   # Rotation
   cll.rotate(1)   # [2, 3, 1]
   cll.rotate(-1)  # [1, 2, 3]
   
   # Circular property
   print(cll.tail.next is cll.head)  # True

Real-World Applications
=======================

Application 1: Music Playlist (Circular)
-----------------------------------------

.. code-block:: python

   from sds.linear import CircularLinkedList
   
   class MusicPlayer:
       def __init__(self):
           self.playlist = CircularLinkedList()
           self.current = 0
       
       def add_song(self, title):
           self.playlist.append(title)
       
       def next_song(self):
           if self.playlist.is_empty():
               return None
           song = self.playlist[self.current]
           self.current = (self.current + 1) % len(self.playlist)
           return song
       
       def prev_song(self):
           if self.playlist.is_empty():
               return None
           self.current = (self.current - 1) % len(self.playlist)
           return self.playlist[self.current]
   
   # Usage
   player = MusicPlayer()
   player.add_song("Song A")
   player.add_song("Song B")
   player.add_song("Song C")
   
   for _ in range(5):  # Play 5 songs (circular)
       print(player.next_song())

Application 2: LRU Cache (Doubly Linked)
-----------------------------------------

.. code-block:: python

   from sds.linear import DoublyLinkedList
   
   class LRUCache:
       def __init__(self, capacity):
           self.capacity = capacity
           self.cache = {}
           self.order = DoublyLinkedList()
       
       def get(self, key):
           if key not in self.cache:
               return -1
           
           # Move to front (most recent)
           self.order.remove(key)
           self.order.prepend(key)
           return self.cache[key]
       
       def put(self, key, value):
           if key in self.cache:
               self.order.remove(key)
           elif len(self.order) >= self.capacity:
               # Evict least recent
               lru = self.order.remove_last()
               del self.cache[lru]
           
           self.order.prepend(key)
           self.cache[key] = value

Application 3: Polynomial Representation
-----------------------------------------

.. code-block:: python

   from sds.linear import LinkedList
   
   class Polynomial:
       def __init__(self):
           self.terms = LinkedList()
       
       def add_term(self, coef, exp):
           if coef != 0:
               self.terms.append((coef, exp))
       
       def evaluate(self, x):
           result = 0
           for coef, exp in self.terms:
               result += coef * (x ** exp)
           return result
       
       def __str__(self):
           terms = []
           for coef, exp in self.terms:
               if exp == 0:
                   terms.append(str(coef))
               elif exp == 1:
                   terms.append(f"{coef}x")
               else:
                   terms.append(f"{coef}x^{exp}")
           return " + ".join(terms)
   
   # Create 3x^2 + 2x + 1
   p = Polynomial()
   p.add_term(3, 2)
   p.add_term(2, 1)
   p.add_term(1, 0)
   
   print(p)             # 3x^2 + 2x + 1
   print(p.evaluate(2)) # 3(4) + 2(2) + 1 = 17

Best Practices
==============

Do's
----

✅ **Use iteration, not indexing**

.. code-block:: python

   # Good: O(n)
   for item in lst:
       process(item)
   
   # Bad: O(n²)
   for i in range(len(lst)):
       process(lst[i])

✅ **Choose right variant**

.. code-block:: python

   # Frequent appends → DoublyLinkedList
   dll = DoublyLinkedList()
   dll.append(x)  # O(1)
   
   # Circular iteration → CircularLinkedList
   cll = CircularLinkedList()
   cll.rotate(1)  # O(1)

✅ **Clear when done**

.. code-block:: python

   lst.clear()  # Help GC

Don'ts
------

❌ **Don't use for random access**

.. code-block:: python

   # Bad: Linked list
   for i in range(len(lst)):
       print(lst[i])  # O(n²)
   
   # Good: Array
   arr = list(lst)
   for i in range(len(arr)):
       print(arr[i])  # O(n)

❌ **Don't forget bounds checking**

.. code-block:: python

   # Bad
   item = lst[100]  # May crash
   
   # Good
   if 0 <= index < len(lst):
       item = lst[index]

When to Use
===========

Singly Linked List
------------------

**Use when:**
   * Frequent prepend operations
   * Memory is constrained
   * Only forward traversal needed

**Don't use when:**
   * Need frequent appends (use doubly)
   * Need random access (use array)

Doubly Linked List
------------------

**Use when:**
   * Need bidirectional traversal
   * Frequent operations at both ends
   * Implementing deque or LRU cache

**Don't use when:**
   * Memory is very limited
   * Only need forward traversal

Circular Linked List
--------------------

**Use when:**
   * Round-robin scheduling
   * Circular buffers
   * Music playlists

**Don't use when:**
   * Need clear endpoints
   * Risk of infinite loops

Common Pitfalls
===============

1. **Infinite loops in circular lists**
2. **Memory leaks from broken links**
3. **O(n²) from repeated indexing**
4. **Forgetting to update size**

See Also
========

* :doc:`/api/linear/list` - API reference
* :doc:`stack` - Built on linked lists
* :doc:`queue` - Queue implementations
