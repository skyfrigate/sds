.. _guide_tree_btree:

============
B-Tree Guide
============

.. currentmodule:: sds.tree

Introduction
============

A **B-Tree** is a self-balancing search tree optimized for systems that read and write large blocks of data. Unlike binary trees where each node has at most 2 children, B-Tree nodes can have many children, reducing tree height and minimizing disk I/O operations. B-Trees are the fundamental data structure behind modern database systems and file systems.

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
       style G fill:#2ecc71,color:#fff
       style H fill:#2ecc71,color:#fff
       style I fill:#2ecc71,color:#fff

.. note::
   
   B-Trees are ideal for storage systems where reading/writing a block of data
   has similar cost regardless of block size. By storing multiple keys per node,
   B-Trees minimize the number of disk accesses required for operations.

Mathematical Model
==================

Formal Definition
-----------------

B-Tree of Minimum Degree t
^^^^^^^^^^^^^^^^^^^^^^^^^^^

A B-Tree of **minimum degree** :math:`t \geq 2` satisfies:

1. **Every node has at most** :math:`2t-1` **keys**

   .. math::

      \forall node \in T: |keys(node)| \leq 2t - 1

2. **Every non-root node has at least** :math:`t-1` **keys**

   .. math::

      \forall node \neq root: |keys(node)| \geq t - 1

3. **Root has at least 1 key** (if tree is non-empty)

   .. math::

      |keys(root)| \geq 1

4. **All leaves are at the same depth**

   .. math::

      \forall leaf_1, leaf_2: depth(leaf_1) = depth(leaf_2)

5. **A non-leaf node with** :math:`k` **keys has** :math:`k+1` **children**

   .. math::

      |children(node)| = |keys(node)| + 1

6. **Keys in each node are sorted**

   .. math::

      keys(node) = [k_1, k_2, \ldots, k_n] \implies k_1 < k_2 < \cdots < k_n

Node Structure
^^^^^^^^^^^^^^

For a node with keys :math:`[k_1, k_2, \ldots, k_n]` and children :math:`[c_0, c_1, \ldots, c_n]`:

.. math::

   \forall i: \max(c_i) < k_{i+1} < \min(c_{i+1})

This creates a search tree property across multiple keys per node.

Tree Properties
---------------

Height Bounds
^^^^^^^^^^^^^

For a B-Tree with :math:`n` keys and minimum degree :math:`t`:

**Minimum height** (maximum branching):

.. math::

   h_{min} = \lceil \log_{2t}(n+1) \rceil - 1

**Maximum height** (minimum branching):

.. math::

   h_{max} \leq \log_t\left(\frac{n+1}{2}\right)

**Key insight**: Height grows **logarithmically** with the number of keys, but the base is :math:`t`, not 2. Larger :math:`t` means shorter trees.

Node Capacity
^^^^^^^^^^^^^

For minimum degree :math:`t`:

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Property
     - Minimum
     - Maximum
   * - **Keys per node**
     - :math:`t-1` (except root)
     - :math:`2t-1`
   * - **Children per node**
     - :math:`t` (except root)
     - :math:`2t`
   * - **Keys in root**
     - 1
     - :math:`2t-1`
   * - **Total keys (height h)**
     - :math:`2t^h - 1`
     - :math:`(2t)^{h+1} - 1`

Disk Access Model
^^^^^^^^^^^^^^^^^

B-Trees minimize disk I/O by:

**Cost model**:

.. math::

   \text{Total I/O} = (\text{tree height}) \times (\text{cost per node access})

Since height :math:`= O(\log_t n)` and :math:`t` can be large (e.g., 1000), we achieve:

.. math::

   \text{I/O operations} = O(\log_{1000} n) \ll O(\log_2 n)

For 1 billion keys: :math:`\log_{1000}(10^9) \approx 3` disk accesses vs :math:`\log_2(10^9) \approx 30` for binary trees!

Algorithmic Model
=================

Abstract Data Type
------------------

.. code-block:: text

   ADT BTree:
       Data:
           - root: BTreeNode
           - t: minimum degree (t ≥ 2)
           - size: number of keys
       
       BTreeNode:
           - keys: sorted array [k₁, k₂, ..., kₙ]
           - children: array [c₀, c₁, ..., cₙ]
           - is_leaf: boolean
           - parent: reference to parent
       
       Operations:
           - BTree(t): create empty tree with degree t
           - search(key): find key in O(log n) disk reads
           - insert(key): add key maintaining properties
           - remove(key): delete key maintaining properties
           - split_child(parent, index): split full child
           - merge_child(parent, index): merge minimal children
       
       Invariants:
           - All leaves at same depth
           - Node keys: t-1 to 2t-1 (root: 1 to 2t-1)
           - Node children: t to 2t (root: 2 to 2t)
           - Keys sorted within and across nodes

Search Algorithm
----------------

.. code-block:: text

   Algorithm: BTREE_SEARCH(node, key)
   Input: BTreeNode node, key to search
   Output: (node, index) if found, else None
   
   1. i ← 0
   2. // Find position in current node
   3. while i < node.n_keys and key > node.keys[i] do
   4.     i ← i + 1
   5. end while
   6. 
   7. // Check if key found
   8. if i < node.n_keys and key = node.keys[i] then
   9.     return (node, i)
   10. end if
   11. 
   12. // If leaf, key not in tree
   13. if node.is_leaf then
   14.    return None
   15. end if
   16. 
   17. // Recurse to appropriate child
   18. DISK_READ(node.children[i])
   19. return BTREE_SEARCH(node.children[i], key)

**Disk I/O**: :math:`O(h) = O(\log_t n)` reads

**CPU time**: :math:`O(t \cdot h) = O(t \log_t n)` comparisons

Insertion Algorithm
-------------------

Two-Pass Insertion (Splitting on the Way Down)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   Algorithm: BTREE_INSERT(tree, key)
   Input: BTree tree, key to insert
   Output: Updated tree
   
   1. root ← tree.root
   2. 
   3. // Split root if full
   4. if root.is_full() then
   5.     new_root ← BTreeNode(t, is_leaf=false)
   6.     new_root.children[0] ← root
   7.     SPLIT_CHILD(new_root, 0)
   8.     tree.root ← new_root
   9. end if
   10. 
   11. BTREE_INSERT_NONFULL(tree.root, key)

.. code-block:: text

   Algorithm: BTREE_INSERT_NONFULL(node, key)
   Input: Non-full node, key to insert
   Output: Key inserted maintaining properties
   
   1. i ← node.n_keys - 1
   2. 
   3. if node.is_leaf then
   4.     // Insert key in sorted position
   5.     while i ≥ 0 and key < node.keys[i] do
   6.         node.keys[i+1] ← node.keys[i]
   7.         i ← i - 1
   8.     end while
   9.     node.keys[i+1] ← key
   10.    node.n_keys ← node.n_keys + 1
   11.    DISK_WRITE(node)
   12. else
   13.    // Find child to insert into
   14.    while i ≥ 0 and key < node.keys[i] do
   15.        i ← i - 1
   16.    end while
   17.    i ← i + 1
   18.    DISK_READ(node.children[i])
   19.    
   20.    // Split child if full
   21.    if node.children[i].is_full() then
   22.        SPLIT_CHILD(node, i)
   23.        if key > node.keys[i] then
   24.            i ← i + 1
   25.        end if
   26.    end if
   27.    
   28.    BTREE_INSERT_NONFULL(node.children[i], key)
   29. end if

Split Child Operation
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   Algorithm: SPLIT_CHILD(parent, index)
   Input: Parent node, index of full child to split
   Output: Child split into two nodes
   
   1. full_child ← parent.children[index]
   2. new_child ← BTreeNode(t, is_leaf=full_child.is_leaf)
   3. 
   4. mid_index ← t - 1
   5. middle_key ← full_child.keys[mid_index]
   6. 
   7. // Move upper half of keys to new child
   8. new_child.keys ← full_child.keys[mid_index+1 : 2t-1]
   9. full_child.keys ← full_child.keys[0 : mid_index]
   10. 
   11. // If not leaf, move children too
   12. if not full_child.is_leaf then
   13.    new_child.children ← full_child.children[mid_index+1 : 2t]
   14.    full_child.children ← full_child.children[0 : mid_index+1]
   15. end if
   16. 
   17. // Move middle key up to parent
   18. parent.keys.insert(index, middle_key)
   19. parent.children.insert(index+1, new_child)
   20. 
   21. DISK_WRITE(full_child)
   22. DISK_WRITE(new_child)
   23. DISK_WRITE(parent)

**Visualization**:

.. code-block:: text

   Before split (node with 2t-1 keys):
   [k₁ k₂ ... k_{t-1} | k_t | k_{t+1} ... k_{2t-1}]
   
   After split:
   Parent gets: k_t
   Left child:  [k₁ k₂ ... k_{t-1}]
   Right child: [k_{t+1} ... k_{2t-1}]

**Disk I/O**: 3 writes (constant)

Deletion Algorithm
------------------

Deletion is more complex, requiring merges and redistributions:

.. code-block:: text

   Algorithm: BTREE_DELETE(node, key)
   Input: Node and key to delete
   Output: Updated tree
   
   1. i ← FIND_KEY_INDEX(node, key)
   2. 
   3. if i < node.n_keys and node.keys[i] = key then
   4.     // Key found in this node
   5.     if node.is_leaf then
   6.         REMOVE_FROM_LEAF(node, i)
   7.     else
   8.         REMOVE_FROM_INTERNAL(node, i)
   9.     end if
   10. else if not node.is_leaf then
   11.    // Key in subtree
   12.    is_in_last_child ← (i = node.n_keys)
   13.    
   14.    // Ensure child has enough keys
   15.    if node.children[i].n_keys < t then
   16.        FILL(node, i)
   17.    end if
   18.    
   19.    if is_in_last_child and i > node.n_keys then
   20.        BTREE_DELETE(node.children[i-1], key)
   21.    else
   22.        BTREE_DELETE(node.children[i], key)
   23.    end if
   24. end if

Merge Operation
^^^^^^^^^^^^^^^

When a child has only :math:`t-1` keys:

.. code-block:: text

   Algorithm: MERGE(parent, index)
   Input: Parent node, index of key to pull down
   Output: Two children merged into one
   
   1. child ← parent.children[index]
   2. sibling ← parent.children[index+1]
   3. 
   4. // Pull key from parent
   5. child.keys.append(parent.keys[index])
   6. 
   7. // Append sibling's keys
   8. child.keys.extend(sibling.keys)
   9. 
   10. // If not leaf, move children too
   11. if not child.is_leaf then
   12.    child.children.extend(sibling.children)
   13. end if
   14. 
   15. // Remove key and child from parent
   16. parent.keys.remove(index)
   17. parent.children.remove(index+1)
   18. 
   19. DISK_WRITE(child)
   20. DISK_WRITE(parent)

**Visualization**:

.. code-block:: text

   Before merge:
   Parent:     [... k ...]
               /           \
   Child:    [a b]      [c d]
   
   After merge:
   Parent:     [...]
                |
   Merged:   [a b k c d]

Complexity Analysis
-------------------

Time Complexity
^^^^^^^^^^^^^^^

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

**Key insight**: Disk I/O dominates. With large :math:`t` (e.g., 1000), height is extremely small.

Space Complexity
^^^^^^^^^^^^^^^^

* **Node storage**: O(n) keys total
* **Wasted space**: Up to 50% per node (when nodes are minimally filled)
* **Average fill**: Typically 69% (from theoretical analysis)
* **Pointers**: O(n) child pointers

Optimal Degree Selection
^^^^^^^^^^^^^^^^^^^^^^^^^

For disk-based systems:

.. math::

   t = \left\lceil \frac{\text{disk block size}}{\text{key size + pointer size}} \right\rceil

**Example**: 
- Block size: 4KB = 4096 bytes
- Key + pointer: 16 bytes
- Optimal :math:`t \approx 256`

This gives :math:`\log_{256}(10^9) \approx 3.8` disk accesses for 1 billion keys!

Practical Usage
===============

Installation and Import
-----------------------

.. code-block:: python

   # Install
   pip install sds-tools
   
   # Import
   from sds.tree import BTree

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

Insertion
^^^^^^^^^

.. code-block:: python

   btree = BTree(t=3)
   
   # Insert keys
   for key in [10, 20, 30, 40, 50, 60, 70, 80, 90]:
       btree.insert(key)
   
   print(f"Size: {len(btree)}")      # Output: 9
   print(f"Height: {btree.height()}")  # Output: 1 or 2

Searching
^^^^^^^^^

.. code-block:: python

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

Real-World Applications
=======================

Application 1: Database Index
------------------------------

B-Trees are the foundation of database indexes:

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
       
       def bulk_load(self, sorted_records):
           """Efficiently load sorted data."""
           # In practice, build B-Tree bottom-up
           for key, record in sorted_records:
               self.insert_record(key, record)
   
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

Application 2: File System Directory
-------------------------------------

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
       
       def find_largest_files(self, n=10):
           """Find n largest files."""
           file_sizes = [
               (fname, self.files[fname]['size'])
               for fname in self.btree.inorder_traversal()
           ]
           file_sizes.sort(key=lambda x: x[1], reverse=True)
           return file_sizes[:n]
   
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
   
   # Statistics
   print(f"Total size: {fs.get_directory_size()} bytes")
   print(f"Largest files: {fs.find_largest_files(5)}")

Application 3: Time-Series Database
------------------------------------

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
       
       def downsample(self, start_time, end_time, interval_minutes):
           """Downsample data to intervals."""
           data_points = self.query_range(start_time, end_time)
           
           buckets = {}
           for dp in data_points:
               ts = dp['timestamp']
               bucket = ts - timedelta(
                   minutes=ts.minute % interval_minutes,
                   seconds=ts.second,
                   microseconds=ts.microsecond
               )
               
               if bucket not in buckets:
                   buckets[bucket] = []
               buckets[bucket].append(dp['value'])
           
           return {
               bucket: sum(values) / len(values)
               for bucket, values in buckets.items()
           }
   
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
   
   # Aggregate statistics
   avg_temp = tsdb.aggregate(start, end, 'avg')
   max_temp = tsdb.aggregate(start, end, 'max')
   print(f"Average: {avg_temp:.1f}°C, Max: {max_temp:.1f}°C")

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

Further Reading
===============

* :doc:`/api/tree/btree` - Complete API reference
* :doc:`binary` - Compare with binary trees
* :doc:`avl` - Compare with balanced binary trees

References
==========

.. [BayerMcCreight] Bayer, R., McCreight, E. "Organization and Maintenance of Large Ordered Indices", 1972
   
   Original B-Tree paper introducing the data structure.

.. [WikiBTree] Wikipedia contributors. "B-tree". Wikipedia.
   https://en.wikipedia.org/wiki/B-tree
   
   Comprehensive overview with visualizations.

.. [CLRS] Cormen, T. H., et al. "Introduction to Algorithms", 3rd Edition, Chapter 18
   
   Detailed mathematical analysis of B-Trees.

.. [USFCABTree] Galles, D. "B-Tree Visualization". USFCA.
   https://www.cs.usfca.edu/~galles/visualization/BTree.html
   
   Interactive B-Tree visualization tool.

.. [Knuth] Knuth, D. E. "The Art of Computer Programming, Volume 3", Section 6.2.4
   
   Comprehensive analysis of B-Trees and variants.

.. [SQLite] SQLite. "Database File Format".
   https://www.sqlite.org/fileformat.html
   
   Real-world B-Tree implementation in SQLite database engine.

.. [PostgreSQL] PostgreSQL. "B-Tree Indexes".
   https://www.postgresql.org/docs/current/btree.html
   
   PostgreSQL's B-Tree index implementation details.
