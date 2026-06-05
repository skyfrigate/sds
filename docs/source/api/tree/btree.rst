.. _api_tree_btree:

======
B-Tree
======

.. currentmodule:: sds.tree.btree

Overview
========

This module provides a B-Tree implementation optimized for disk-based storage systems.
B-Trees maintain sorted data and allow searches, insertions, and deletions in logarithmic
time with a base determined by the node capacity, minimizing disk I/O operations.

.. mermaid::

   graph TB
       subgraph "B-Tree of order t=3"
       A["[50]"] --> B["[20, 30]"]
       A --> C["[70, 80]"]
       B --> D["[10, 15]"]
       B --> E["[25, 28]"]
       B --> F["[40, 45]"]
       C --> G["[60, 65]"]
       C --> H["[75, 77]"]
       C --> I["[90, 95]"]
       end
       
       style A fill:#e74c3c,color:#fff
       style B fill:#3498db,color:#fff
       style C fill:#3498db,color:#fff
       style D fill:#2ecc71,color:#fff
       style E fill:#2ecc71,color:#fff
       style F fill:#2ecc71,color:#fff

Classes
=======

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   BTree

Detailed Documentation
======================

BTree
-----

.. autoclass:: BTree
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __len__, __iter__, __contains__, __repr__, __str__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Properties

   .. autoproperty:: root
   .. autoproperty:: size
   .. autoproperty:: t

   .. rubric:: Core Operations

   .. automethod:: insert
   .. automethod:: remove
   .. automethod:: search
   .. automethod:: height

   .. rubric:: Traversal Methods

   .. automethod:: inorder_traversal
   .. automethod:: level_order_traversal

   .. rubric:: Utility Methods

   .. automethod:: is_empty
   .. automethod:: clear
   .. automethod:: find_min
   .. automethod:: find_max

   .. rubric:: Special Methods

   .. automethod:: __len__
   .. automethod:: __iter__
   .. automethod:: __contains__
   .. automethod:: __repr__
   .. automethod:: __str__

Usage Examples
==============

Basic Operations
----------------

Creating and Configuring
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.tree import BTree

   # Create B-Tree with minimum degree t=3
   # Each node: 2 to 5 keys, 3 to 6 children
   btree = BTree(t=3)
   
   # For small datasets (testing)
   small_tree = BTree(t=2)  # 1-3 keys per node
   
   # For large datasets (production)
   large_tree = BTree(t=100)  # 99-199 keys per node

Insertion and Search
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   btree = BTree(t=3)
   
   # Insert keys
   for key in [10, 20, 30, 40, 50, 60, 70, 80, 90]:
       btree.insert(key)
   
   print(f"Size: {len(btree)}")      # Output: 9
   print(f"Height: {btree.height()}")  # Output: 1 or 2
   
   # Search for keys - O(log_t n)
   print(btree.search(50))  # Output: True
   print(50 in btree)       # Output: True
   print(btree.search(45))  # Output: False

Deletion
^^^^^^^^

.. code-block:: python

   # Remove keys
   btree.remove(30)
   btree.remove(60)
   
   print(list(btree))
   # Output: [10, 20, 40, 50, 70, 80, 90]

Range Queries
^^^^^^^^^^^^^

.. code-block:: python

   btree = BTree(t=3)
   for key in range(0, 100, 10):
       btree.insert(key)
   
   # Get all keys in sorted order (inorder traversal)
   all_keys = list(btree.inorder_traversal())
   print(all_keys)
   # Output: [0, 10, 20, 30, ..., 90]
   
   # Range query: keys between 20 and 60
   range_keys = [k for k in btree.inorder_traversal() if 20 <= k <= 60]
   print(range_keys)
   # Output: [20, 30, 40, 50, 60]

Min/Max Operations
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Find minimum and maximum
   print(btree.find_min())  # Output: 0
   print(btree.find_max())  # Output: 90

Real-World Examples
===================

Example 1: Database Index
--------------------------

Disk-based database index using B-Tree:

.. code-block:: python

   from sds.tree import BTree

   class DatabaseIndex:
       """Disk-based database index using B-Tree."""
       
       def __init__(self, block_size=4096):
           # Calculate optimal t for disk blocks
           key_size = 8  # 64-bit integer key
           pointer_size = 8  # 64-bit pointer
           entry_size = key_size + pointer_size
           
           # Max keys per node to fit in one block
           max_keys = (block_size - 64) // entry_size  # 64 bytes overhead
           self.t = max(2, max_keys // 2)
           
           self.btree = BTree(t=self.t)
           self.records = {}
       
       def insert_record(self, key, record):
           """Insert record - one disk seek + O(log n) reads."""
           self.btree.insert(key)
           self.records[key] = record
       
       def find_record(self, key):
           """Find record - O(log_t n) disk reads."""
           if self.btree.search(key):
               return self.records[key]
           return None
       
       def range_scan(self, low, high):
           """Efficient range query."""
           results = []
           for key in self.btree.inorder_traversal():
               if low <= key <= high:
                   results.append(self.records[key])
               elif key > high:
                   break
           return results
       
       def delete_record(self, key):
           """Delete record - O(log_t n) disk operations."""
           if self.btree.search(key):
               self.btree.remove(key)
               del self.records[key]
               return True
           return False
   
   # Usage
   db_index = DatabaseIndex(block_size=4096)
   
   # Insert millions of records
   for i in range(1000000):
       db_index.insert_record(i, {"name": f"Record {i}", "data": "..."})
   
   # Fast lookup: only ~3-4 disk reads for 1M records!
   record = db_index.find_record(500000)
   print(record)
   
   # Range query
   results = db_index.range_scan(1000, 2000)
   print(f"Found {len(results)} records in range")

Example 2: File System Directory
---------------------------------

B-Trees in file systems (like ext4, NTFS):

.. code-block:: python

   from sds.tree import BTree
   from datetime import datetime

   class FileSystemDirectory:
       """File system directory using B-Tree."""
       
       def __init__(self):
           # Larger t for many files per directory
           self.btree = BTree(t=64)
           self.files = {}
       
       def create_file(self, filename, size, metadata=None):
           """Create file entry."""
           if self.btree.search(filename):
               raise ValueError(f"File {filename} already exists")
           
           self.btree.insert(filename)
           self.files[filename] = {
               'size': size,
               'created': datetime.now(),
               'modified': datetime.now(),
               'metadata': metadata or {}
           }
       
       def delete_file(self, filename):
           """Delete file entry."""
           if not self.btree.search(filename):
               raise ValueError(f"File {filename} not found")
           
           self.btree.remove(filename)
           del self.files[filename]
       
       def find_file(self, filename):
           """Lookup file - very fast even with millions of files."""
           if self.btree.search(filename):
               return self.files[filename]
           return None
       
       def list_files(self, prefix=None):
           """List files, optionally filtered by prefix."""
           if prefix is None:
               return list(self.btree.inorder_traversal())
           
           # Efficient prefix search
           results = []
           for filename in self.btree.inorder_traversal():
               if filename.startswith(prefix):
                   results.append(filename)
               elif filename > prefix:
                   # Can stop once past prefix range
                   if not filename.startswith(prefix):
                       break
           return results
       
       def get_directory_size(self):
           """Calculate total size of all files."""
           total = 0
           for filename in self.btree.inorder_traversal():
               total += self.files[filename]['size']
           return total
   
   # Usage
   fs = FileSystemDirectory()
   
   # Create many files (scales to millions)
   for i in range(10000):
       fs.create_file(f"file_{i:05d}.txt", size=1024 * (i % 100))
   
   # Fast lookup
   file_info = fs.find_file("file_05000.txt")
   print(file_info)
   
   # List files with prefix
   txt_files = fs.list_files(prefix="file_050")
   print(f"Found {len(txt_files)} files matching prefix")

Example 3: Time-Series Database
--------------------------------

Efficient time-range queries:

.. code-block:: python

   from sds.tree import BTree
   from datetime import datetime, timedelta

   class TimeSeriesDB:
       """Time-series data store with B-Tree index."""
       
       def __init__(self):
           # Index on timestamp
           self.index = BTree(t=100)
           self.data = {}
       
       def insert(self, timestamp, value, tags=None):
           """Insert time-series data point."""
           # Use timestamp as key
           ts_key = int(timestamp.timestamp() * 1000)  # milliseconds
           
           self.index.insert(ts_key)
           self.data[ts_key] = {
               'timestamp': timestamp,
               'value': value,
               'tags': tags or {}
           }
       
       def query_range(self, start_time, end_time):
           """Query data in time range - very efficient."""
           start_key = int(start_time.timestamp() * 1000)
           end_key = int(end_time.timestamp() * 1000)
           
           results = []
           for ts_key in self.index.inorder_traversal():
               if start_key <= ts_key <= end_key:
                   results.append(self.data[ts_key])
               elif ts_key > end_key:
                   break
           
           return results
       
       def aggregate(self, start_time, end_time, func):
           """Aggregate data in time range."""
           data_points = self.query_range(start_time, end_time)
           values = [dp['value'] for dp in data_points]
           
           if not values:
               return None
           
           if func == 'avg':
               return sum(values) / len(values)
           elif func == 'sum':
               return sum(values)
           elif func == 'min':
               return min(values)
           elif func == 'max':
               return max(values)
           elif func == 'count':
               return len(values)
   
   # Usage
   tsdb = TimeSeriesDB()
   
   # Insert sensor data
   base_time = datetime.now()
   for i in range(10000):
       timestamp = base_time + timedelta(seconds=i)
       value = 20 + (i % 10)  # Simulated temperature
       tsdb.insert(timestamp, value, tags={'sensor': 'temp_01'})
   
   # Query last hour
   end = datetime.now()
   start = end - timedelta(hours=1)
   recent_data = tsdb.query_range(start, end)
   print(f"Data points in last hour: {len(recent_data)}")

Performance Characteristics
===========================

Time Complexity
---------------

.. list-table::
   :header-rows: 1
   :widths: 25 20 25 30

   * - Operation
     - Disk I/O
     - CPU Time
     - Notes
   * - **Search**
     - O(log_t n)
     - O(t log_t n)
     - h disk reads
   * - **Insert**
     - O(log_t n)
     - O(t log_t n)
     - Split cascade
   * - **Delete**
     - O(log_t n)
     - O(t log_t n)
     - Merge cascade
   * - **Split**
     - O(1)
     - O(t)
     - 3 disk writes
   * - **Merge**
     - O(1)
     - O(t)
     - 2 disk writes
   * - **Traverse**
     - O(n/t)
     - O(n)
     - Visit all nodes

Space Complexity
----------------

* **Node storage**: O(n) keys total
* **Wasted space**: Up to 50% per node (when nodes are minimally filled)
* **Average fill**: Typically 69% (from theoretical analysis)
* **Pointers**: O(n) child pointers

Optimal Degree Selection
-------------------------

For disk-based systems:

.. math::

   t = \left\lceil \frac{\text{disk block size}}{\text{key size + pointer size}} \right\rceil

**Example**: 
- Block size: 4KB = 4096 bytes
- Key + pointer: 16 bytes
- Optimal t ≈ 256

This gives :math:`\log_{256}(10^9) \approx 3.8` disk accesses for 1 billion keys!

Comparison with Other Trees
============================

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 20 20

   * - Aspect
     - B-Tree
     - Binary BST
     - AVL Tree
     - Red-Black
   * - **Node capacity**
     - Many keys
     - 1 key
     - 1 key
     - 1 key
   * - **Height (1M keys)**
     - ~3 (t=100)
     - ~20
     - ~20
     - ~20
   * - **Disk I/O**
     - Minimal
     - High
     - High
     - High
   * - **Cache efficiency**
     - Excellent
     - Poor
     - Poor
     - Poor
   * - **Best for**
     - Databases
     - General
     - Searches
     - Updates

When to Use B-Trees
-------------------

**Use B-Trees when:**
   - Data stored on disk/SSD
   - Minimizing I/O is critical
   - Dealing with millions+ records
   - Range queries are common
   - Block-oriented storage

**Don't use B-Trees when:**
   - All data fits in memory
   - Only equality searches
   - Very small datasets (< 1000)
   - Random access memory only

Best Practices
==============

Do's
----

✅ **Choose t based on storage block size**

.. code-block:: python

   # For disk-based systems
   block_size = 4096  # bytes
   key_size = 16      # bytes per entry
   optimal_t = block_size // (key_size * 2)
   
   btree = BTree(t=optimal_t)

✅ **Use B-Trees for disk-based storage**

.. code-block:: python

   # Perfect for:
   # - Database indexes
   # - File systems
   # - Any system with block I/O

✅ **Leverage range query efficiency**

.. code-block:: python

   # B-Trees excel at range scans
   results = [k for k in btree.inorder_traversal() 
              if start <= k <= end]

Don'ts
------

❌ **Don't use small t for large datasets**

.. code-block:: python

   # Bad: t=2 means tall tree
   btree = BTree(t=2)  # Binary tree height
   
   # Good: larger t means shorter tree
   btree = BTree(t=100)  # Much shorter

❌ **Don't use B-Trees for in-memory only**

.. code-block:: python

   # For in-memory data, simpler structures may be better:
   # - AVL/Red-Black for small datasets
   # - Hash tables for equality lookups
   # - Skip lists for alternative
   
   # Use B-Trees when disk I/O matters

❌ **Don't forget about cache effects**

.. code-block:: python

   # Consider:
   # - CPU cache line size
   # - Memory page size
   # - Disk sector size

Common Pitfalls
===============

1. **Choosing wrong t value**

.. code-block:: python

   # Too small: tall tree, many I/O operations
   # Too large: wasted space per node
   # Calculate based on block size!

2. **Using for small datasets**

.. code-block:: python

   # B-Trees have overhead
   # For < 1000 elements, simpler structures work fine

3. **Ignoring disk access patterns**

.. code-block:: python

   # B-Trees optimize sequential access
   # Random access patterns still expensive

See Also
========

* :doc:`binary` - Binary search trees
* :doc:`balanced` - AVL and Red-Black trees
* :doc:`../../guide/tree_structures/btree` - B-Tree theory and guide

References
==========

.. [1] Bayer, R., McCreight, E. "Organization and Maintenance of Large Ordered Indices", 1972
.. [2] Comer, D. "The Ubiquitous B-Tree", ACM Computing Surveys, 1979
.. [3] Cormen, T. H., et al. "Introduction to Algorithms", 3rd Edition, Chapter 18
.. [4] Knuth, D. E. "The Art of Computer Programming, Volume 3", Section 6.2.4
