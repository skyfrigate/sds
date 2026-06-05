.. _guide_advanced_interfaces:

===========================================
Abstract Interfaces for Advanced Structures
===========================================

.. contents:: Table of Contents
   :local:
   :depth: 3

Introduction
============

Abstract interfaces define formal contracts for advanced data structures,
ensuring consistency, enabling polymorphism, and facilitating code reuse.
This guide explores interface design patterns and best practices.

What Are Abstract Interfaces?
------------------------------

An abstract interface is a contract that:

* **Defines method signatures** without implementation
* **Specifies behavior** through documentation
* **Enforces consistency** across implementations
* **Enables polymorphism** for generic algorithms

.. mermaid::

   classDiagram
       class AbstractInterface {
           <<abstract>>
           +method1()
           +method2()
           +method3()
       }
       
       class ConcreteImplementation1 {
           +method1()
           +method2()
           +method3()
           +specific_feature1()
       }
       
       class ConcreteImplementation2 {
           +method1()
           +method2()
           +method3()
           +specific_feature2()
       }
       
       class GenericAlgorithm {
           +process(AbstractInterface)
       }
       
       AbstractInterface <|.. ConcreteImplementation1
       AbstractInterface <|.. ConcreteImplementation2
       GenericAlgorithm --> AbstractInterface

Why Use Abstract Interfaces?
-----------------------------

**1. Contract Definition**

Interfaces specify *what* operations are available, not *how* they work:

.. code-block:: python

   from abc import ABC, abstractmethod
   
   class AbstractStack(ABC):
       """Stack interface: LIFO behavior."""
       
       @abstractmethod
       def push(self, item):
           """Add item to top."""
           pass
       
       @abstractmethod
       def pop(self):
           """Remove and return top item."""
           pass
       
       @abstractmethod
       def is_empty(self) -> bool:
           """Check if stack is empty."""
           pass

**2. Polymorphism**

Write algorithms that work with any implementation:

.. code-block:: python

   def reverse_string(s: str, stack: AbstractStack) -> str:
       """Reverse string using any stack implementation."""
       for char in s:
           stack.push(char)
       
       result = []
       while not stack.is_empty():
           result.append(stack.pop())
       
       return ''.join(result)
   
   # Works with any stack
   from sds.linear import Stack, CircularStack
   
   print(reverse_string("hello", Stack()))          # "olleh"
   print(reverse_string("hello", CircularStack()))  # "olleh"

**3. Flexibility**

Swap implementations without changing client code:

.. code-block:: python

   # Development: use simple implementation
   cache = DictionaryCache()
   
   # Production: use optimized implementation
   cache = LRUCache()
   
   # Same interface, different performance

**4. Testing**

Create mock implementations for unit tests:

.. code-block:: python

   class MockDisjointSet(AbstractDisjointSet):
       """Mock for testing algorithms."""
       
       def __init__(self):
           self.operations = []  # Track calls
       
       def union(self, x, y):
           self.operations.append(('union', x, y))
           return True
       
       # Implement other methods...

Interface Design Patterns
=========================

Disjoint Set Interface
----------------------

The **AbstractDisjointSet** interface supports dynamic connectivity:

**Mathematical Foundation**

A partition of a set S is a collection of disjoint subsets whose union equals S:

.. math::

   \mathcal{P} = \{S_1, S_2, \ldots, S_k\}

Such that:

.. math::

   \bigcup_{i=1}^{k} S_i = S \quad \text{and} \quad S_i \cap S_j = \emptyset \text{ for } i \neq j

**Interface Contract**

.. code-block:: python

   from abc import ABC, abstractmethod
   from typing import Any, List, Set
   
   class AbstractDisjointSet(ABC):
       """Interface for Union-Find data structure."""
       
       @abstractmethod
       def make_set(self, element: Any) -> None:
           """Create singleton set {element}."""
           pass
       
       @abstractmethod
       def find(self, element: Any) -> Any:
           """Find representative of element's set."""
           pass
       
       @abstractmethod
       def union(self, x: Any, y: Any) -> bool:
           """Merge sets containing x and y."""
           pass
       
       @abstractmethod
       def connected(self, x: Any, y: Any) -> bool:
           """Check if x and y in same set."""
           pass

**Implementation Requirements**

Any implementation must guarantee:

1. **Correctness**: Operations maintain partition invariants
2. **Efficiency**: Nearly constant amortized time (O(α(n)))
3. **Consistency**: find(x) == find(y) ⟺ connected(x, y)

.. code-block:: python

   from sds.advanced import DisjointSet
   from sds.advanced.interfaces import AbstractDisjointSet
   
   def validate_implementation(ds: AbstractDisjointSet):
       """Verify interface contract."""
       # Test basic operations
       ds.make_set(1)
       ds.make_set(2)
       ds.make_set(3)
       
       assert not ds.connected(1, 2)
       
       ds.union(1, 2)
       assert ds.connected(1, 2)
       assert ds.find(1) == ds.find(2)
       
       assert not ds.connected(1, 3)
   
   # Works with any implementation
   validate_implementation(DisjointSet())

**Generic Algorithms**

.. code-block:: python

   from typing import List, Tuple
   from sds.advanced.interfaces import AbstractDisjointSet
   
   def count_connected_components(
       n: int,
       edges: List[Tuple[int, int]],
       ds: AbstractDisjointSet
   ) -> int:
       """
       Count components using any DisjointSet.
       
       Works with standard, weighted, or custom implementations.
       """
       # Initialize
       for i in range(n):
           ds.make_set(i)
       
       # Process edges
       for u, v in edges:
           ds.union(u, v)
       
       return ds.count_sets()

Probabilistic Set Interface
----------------------------

The **AbstractProbabilisticSet** interface supports approximate membership:

**Mathematical Foundation**

Probabilistic structures trade accuracy for space:

.. math::

   P(\text{false positive}) > 0 \quad \text{but} \quad P(\text{false negative}) = 0

**Interface Contract**

.. code-block:: python

   class AbstractProbabilisticSet(ABC):
       """Interface for space-efficient membership testing."""
       
       @abstractmethod
       def add(self, item: Any) -> None:
           """Add item (ensures future contains=True)."""
           pass
       
       @abstractmethod
       def __contains__(self, item: Any) -> bool:
           """
           Test membership.
           
           Returns:
               True: item might be present (possible false positive)
               False: item definitely not present (no false negative)
           """
           pass
       
       @abstractmethod
       def estimated_fill_ratio(self) -> float:
           """Return ratio of used capacity [0.0, 1.0]."""
           pass

**Probabilistic Guarantees**

Implementations must ensure:

.. math::

   \forall x: x \in S \Rightarrow \text{contains}(x) = \text{True}

But may have:

.. math::

   \exists x: x \notin S \wedge \text{contains}(x) = \text{True}

.. code-block:: python

   from sds.advanced.interfaces import AbstractProbabilisticSet
   
   def test_probabilistic_guarantees(pset: AbstractProbabilisticSet):
       """Verify probabilistic contract."""
       items = [1, 2, 3, 4, 5]
       
       # Add items
       for item in items:
           pset.add(item)
       
       # No false negatives
       for item in items:
           assert item in pset, "False negative not allowed!"
       
       # Count false positives
       false_positives = 0
       test_items = range(100, 200)
       for item in test_items:
           if item in pset:
               false_positives += 1
       
       fp_rate = false_positives / len(test_items)
       print(f"False positive rate: {fp_rate:.2%}")

**Generic Applications**

.. code-block:: python

   from typing import Iterable
   from sds.advanced.interfaces import AbstractProbabilisticSet
   
   def filter_seen_items(
       stream: Iterable[str],
       pset: AbstractProbabilisticSet
   ) -> Iterable[str]:
       """
       Filter duplicate items from stream.
       
       May have false positives (missed unique items),
       but no false negatives (no duplicate items pass).
       """
       for item in stream:
           if item not in pset:
               pset.add(item)
               yield item
   
   # Usage with any probabilistic set
   from sds.advanced import BloomFilter
   
   bf = BloomFilter(size=10000, num_hashes=3)
   unique_items = list(filter_seen_items(data_stream, bf))

Implementing Custom Interfaces
===============================

Step-by-Step Implementation
---------------------------

**1. Import Abstract Base**

.. code-block:: python

   from abc import ABC, abstractmethod
   from sds.advanced.interfaces import AbstractDisjointSet
   from typing import Any, List, Set, Dict

**2. Define Class Structure**

.. code-block:: python

   class CompressedDisjointSet(AbstractDisjointSet):
       """
       Union-Find with aggressive path compression.
       
       Uses iterative find with full path compression.
       """
       
       def __init__(self):
           self._parent: Dict[Any, Any] = {}
           self._rank: Dict[Any, int] = {}
           self._num_sets: int = 0

**3. Implement Required Methods**

.. code-block:: python

   def make_set(self, element: Any) -> None:
       if element in self._parent:
           raise ValueError(f"Element {element} already exists")
       
       self._parent[element] = element
       self._rank[element] = 0
       self._num_sets += 1
   
   def find(self, element: Any) -> Any:
       if element not in self._parent:
           raise ValueError(f"Element {element} not found")
       
       # Iterative with full compression
       root = element
       while self._parent[root] != root:
           root = self._parent[root]
       
       # Compress path
       while element != root:
           next_elem = self._parent[element]
           self._parent[element] = root
           element = next_elem
       
       return root
   
   def union(self, x: Any, y: Any) -> bool:
       root_x = self.find(x)
       root_y = self.find(y)
       
       if root_x == root_y:
           return False
       
       # Union by rank
       if self._rank[root_x] < self._rank[root_y]:
           self._parent[root_x] = root_y
       elif self._rank[root_x] > self._rank[root_y]:
           self._parent[root_y] = root_x
       else:
           self._parent[root_y] = root_x
           self._rank[root_x] += 1
       
       self._num_sets -= 1
       return True
   
   def connected(self, x: Any, y: Any) -> bool:
       return self.find(x) == self.find(y)
   
   def get_sets(self) -> List[Set[Any]]:
       sets_dict: Dict[Any, Set[Any]] = {}
       for element in self._parent:
           root = self.find(element)
           if root not in sets_dict:
               sets_dict[root] = set()
           sets_dict[root].add(element)
       return list(sets_dict.values())
   
   def count_sets(self) -> int:
       return self._num_sets
   
   def size(self, element: Any) -> int:
       root = self.find(element)
       return sum(1 for e in self._parent if self.find(e) == root)

**4. Add Optional Enhancements**

.. code-block:: python

   def __repr__(self) -> str:
       return f"CompressedDisjointSet(elements={len(self._parent)}, sets={self._num_sets})"
   
   def reset(self):
       """Clear all elements."""
       self._parent.clear()
       self._rank.clear()
       self._num_sets = 0

**5. Test Implementation**

.. code-block:: python

   def test_custom_implementation():
       ds = CompressedDisjointSet()
       
       # Basic operations
       for i in range(5):
           ds.make_set(i)
       
       assert ds.count_sets() == 5
       
       ds.union(0, 1)
       ds.union(2, 3)
       assert ds.count_sets() == 3
       
       assert ds.connected(0, 1)
       assert not ds.connected(0, 2)
       
       print("✓ All tests passed!")
   
   test_custom_implementation()

Advanced Implementation Patterns
---------------------------------

**Pattern 1: Weighted Union-Find**

.. code-block:: python

   class WeightedDisjointSet(AbstractDisjointSet):
       """Union-Find tracking component weights."""
       
       def __init__(self):
           self._parent: Dict[Any, Any] = {}
           self._size: Dict[Any, int] = {}
           self._weight: Dict[Any, float] = {}
           self._num_sets = 0
       
       def make_set(self, element: Any, weight: float = 1.0) -> None:
           if element in self._parent:
               raise ValueError(f"Element {element} exists")
           
           self._parent[element] = element
           self._size[element] = 1
           self._weight[element] = weight
           self._num_sets += 1
       
       def get_total_weight(self, element: Any) -> float:
           """Get total weight of element's component."""
           root = self.find(element)
           return self._weight[root]
       
       def union(self, x: Any, y: Any) -> bool:
           root_x = self.find(x)
           root_y = self.find(y)
           
           if root_x == root_y:
               return False
           
           # Merge smaller into larger
           if self._size[root_x] < self._size[root_y]:
               self._parent[root_x] = root_y
               self._size[root_y] += self._size[root_x]
               self._weight[root_y] += self._weight[root_x]
           else:
               self._parent[root_y] = root_x
               self._size[root_x] += self._size[root_y]
               self._weight[root_x] += self._weight[root_y]
           
           self._num_sets -= 1
           return True

**Pattern 2: Persistent Union-Find**

.. code-block:: python

   from copy import deepcopy
   
   class PersistentDisjointSet(AbstractDisjointSet):
       """Union-Find with history tracking."""
       
       def __init__(self):
           self._parent: Dict[Any, Any] = {}
           self._rank: Dict[Any, int] = {}
           self._num_sets = 0
           self._history: List[Dict] = []
       
       def _save_state(self):
           """Save current state."""
           state = {
               'parent': deepcopy(self._parent),
               'rank': deepcopy(self._rank),
               'num_sets': self._num_sets
           }
           self._history.append(state)
       
       def union(self, x: Any, y: Any) -> bool:
           self._save_state()
           # ... standard union implementation ...
           return True
       
       def rollback(self, steps: int = 1):
           """Undo last `steps` operations."""
           if steps > len(self._history):
               raise ValueError("Not enough history")
           
           for _ in range(steps):
               state = self._history.pop()
               self._parent = state['parent']
               self._rank = state['rank']
               self._num_sets = state['num_sets']

**Pattern 3: Monitored Union-Find**

.. code-block:: python

   from typing import Callable
   
   class MonitoredDisjointSet(AbstractDisjointSet):
       """Union-Find with operation callbacks."""
       
       def __init__(self):
           self._parent: Dict[Any, Any] = {}
           self._rank: Dict[Any, int] = {}
           self._num_sets = 0
           self._callbacks: Dict[str, List[Callable]] = {
               'make_set': [],
               'union': [],
               'find': []
           }
       
       def add_callback(self, operation: str, callback: Callable):
           """Register callback for operation."""
           if operation in self._callbacks:
               self._callbacks[operation].append(callback)
       
       def make_set(self, element: Any) -> None:
           # ... implementation ...
           
           # Trigger callbacks
           for cb in self._callbacks['make_set']:
               cb(element)
       
       def union(self, x: Any, y: Any) -> bool:
           # ... implementation ...
           merged = True  # if actually merged
           
           # Trigger callbacks
           for cb in self._callbacks['union']:
               cb(x, y, merged)
           
           return merged
   
   # Usage
   ds = MonitoredDisjointSet()
   
   def log_union(x, y, merged):
       if merged:
           print(f"Merged sets containing {x} and {y}")
   
   ds.add_callback('union', log_union)

Testing Interface Implementations
==================================

Contract Verification
---------------------

**Generic Test Suite**

.. code-block:: python

   from sds.advanced.interfaces import AbstractDisjointSet
   import pytest
   
   class DisjointSetContractTests:
       """Test suite for any DisjointSet implementation."""
       
       @staticmethod
       def test_singleton_sets(ds: AbstractDisjointSet):
           """Test that make_set creates singletons."""
           ds.make_set(1)
           ds.make_set(2)
           
           assert not ds.connected(1, 2)
           assert ds.count_sets() == 2
           assert ds.size(1) == 1
       
       @staticmethod
       def test_union_merges(ds: AbstractDisjointSet):
           """Test that union merges sets."""
           ds.make_set(1)
           ds.make_set(2)
           
           result = ds.union(1, 2)
           assert result == True
           assert ds.connected(1, 2)
           assert ds.count_sets() == 1
       
       @staticmethod
       def test_union_idempotent(ds: AbstractDisjointSet):
           """Test that repeated unions don't change state."""
           ds.make_set(1)
           ds.make_set(2)
           
           ds.union(1, 2)
           result = ds.union(1, 2)
           assert result == False
           assert ds.count_sets() == 1
       
       @staticmethod
       def test_transitivity(ds: AbstractDisjointSet):
           """Test that connectivity is transitive."""
           for i in range(5):
               ds.make_set(i)
           
           ds.union(0, 1)
           ds.union(1, 2)
           ds.union(2, 3)
           
           assert ds.connected(0, 3)
           assert ds.find(0) == ds.find(3)
       
       @staticmethod
       def test_size_tracking(ds: AbstractDisjointSet):
           """Test that size is tracked correctly."""
           for i in range(5):
               ds.make_set(i)
           
           ds.union(0, 1)
           assert ds.size(0) == 2
           assert ds.size(1) == 2
           
           ds.union(1, 2)
           assert ds.size(0) == 3
           assert ds.size(1) == 3
           assert ds.size(2) == 3
       
       @staticmethod
       def test_error_conditions(ds: AbstractDisjointSet):
           """Test error handling."""
           with pytest.raises(ValueError):
               ds.find(999)  # Non-existent element
           
           ds.make_set(1)
           with pytest.raises(ValueError):
               ds.make_set(1)  # Duplicate element
   
   # Run tests on any implementation
   def test_implementation(ds_class):
       tests = DisjointSetContractTests()
       
       for test_name in dir(tests):
           if test_name.startswith('test_'):
               ds = ds_class()
               test_method = getattr(tests, test_name)
               test_method(ds)
               print(f"✓ {test_name}")
   
   # Test standard implementation
   from sds.advanced import DisjointSet
   test_implementation(DisjointSet)
   
   # Test custom implementation
   test_implementation(CompressedDisjointSet)

Performance Benchmarking
------------------------

**Comparative Benchmarks**

.. code-block:: python

   import time
   from typing import Type
   from sds.advanced.interfaces import AbstractDisjointSet
   
   def benchmark_implementation(
       ds_class: Type[AbstractDisjointSet],
       n: int,
       operations: int
   ) -> Dict[str, float]:
       """Benchmark a DisjointSet implementation."""
       results = {}
       
       # Test make_set
       ds = ds_class()
       start = time.perf_counter()
       for i in range(n):
           ds.make_set(i)
       results['make_set'] = time.perf_counter() - start
       
       # Test union
       import random
       start = time.perf_counter()
       for _ in range(operations):
           u, v = random.sample(range(n), 2)
           ds.union(u, v)
       results['union'] = time.perf_counter() - start
       
       # Test find
       start = time.perf_counter()
       for _ in range(operations):
           x = random.randint(0, n-1)
           ds.find(x)
       results['find'] = time.perf_counter() - start
       
       # Test connected
       start = time.perf_counter()
       for _ in range(operations):
           u, v = random.sample(range(n), 2)
           ds.connected(u, v)
       results['connected'] = time.perf_counter() - start
       
       return results
   
   # Compare implementations
   implementations = [DisjointSet, CompressedDisjointSet, WeightedDisjointSet]
   
   for impl in implementations:
       results = benchmark_implementation(impl, n=10000, operations=50000)
       print(f"\n{impl.__name__}:")
       for op, time_taken in results.items():
           print(f"  {op}: {time_taken:.4f}s")

Best Practices
==============

Interface Design Principles
---------------------------

**1. Keep Interfaces Minimal**

Only include essential operations:

.. code-block:: python

   # ✓ Good: minimal interface
   class AbstractQueue(ABC):
       @abstractmethod
       def enqueue(self, item): pass
       
       @abstractmethod
       def dequeue(self): pass
       
       @abstractmethod
       def is_empty(self) -> bool: pass
   
   # ❌ Avoid: bloated interface
   class AbstractQueue(ABC):
       @abstractmethod
       def enqueue(self, item): pass
       
       @abstractmethod
       def dequeue(self): pass
       
       @abstractmethod
       def peek(self): pass
       
       @abstractmethod
       def is_empty(self): pass
       
       @abstractmethod
       def size(self): pass
       
       @abstractmethod
       def clear(self): pass
       
       @abstractmethod
       def to_list(self): pass
       # Too many requirements!

**2. Document Contracts Clearly**

Specify expected behavior:

.. code-block:: python

   class AbstractDisjointSet(ABC):
       @abstractmethod
       def union(self, x: Any, y: Any) -> bool:
           """
           Unite sets containing x and y.
           
           Parameters
           ----------
           x, y : Any
               Elements in (possibly different) sets.
           
           Returns
           -------
           bool
               True if sets were merged (different sets).
               False if already in same set.
           
           Raises
           ------
           ValueError
               If x or y not in any set.
           
           Notes
           -----
           After union(x, y):
           - connected(x, y) must be True
           - find(x) == find(y)
           - count_sets() decreases by 1 (if merged)
           """
           pass

**3. Design for Extension**

Allow implementations to add features:

.. code-block:: python

   class ExtendedDisjointSet(AbstractDisjointSet):
       """DisjointSet with additional features."""
       
       # Implement required methods...
       
       # Add optional features
       def get_component_graph(self) -> Dict:
           """Return graph of component relationships."""
           # Custom functionality
           pass

Usage Guidelines
----------------

**1. Program to Interfaces**

.. code-block:: python

   # ✓ Good: accept interface
   def process_data(ds: AbstractDisjointSet):
       # Works with any implementation
       pass
   
   # ❌ Avoid: require concrete class
   def process_data(ds: DisjointSet):
       # Only works with DisjointSet
       pass

**2. Use Type Hints**

.. code-block:: python

   from typing import Protocol
   from sds.advanced.interfaces import AbstractDisjointSet
   
   def analyze_connectivity(
       graph: Dict[int, List[int]],
       ds: AbstractDisjointSet
   ) -> Dict[str, int]:
       """Type hints enable static checking."""
       # Implementation...

**3. Verify Implementations**

.. code-block:: python

   from sds.advanced.interfaces import AbstractDisjointSet
   
   # Check inheritance
   assert isinstance(ds, AbstractDisjointSet)
   
   # Verify interface
   assert hasattr(ds, 'make_set')
   assert hasattr(ds, 'union')
   assert hasattr(ds, 'find')

Common Patterns
===============

Factory Pattern
---------------

.. code-block:: python

   from enum import Enum
   from typing import Type
   from sds.advanced.interfaces import AbstractDisjointSet
   
   class DisjointSetType(Enum):
       STANDARD = "standard"
       WEIGHTED = "weighted"
       COMPRESSED = "compressed"
   
   class DisjointSetFactory:
       """Factory for creating DisjointSet implementations."""
       
       _implementations: Dict[DisjointSetType, Type[AbstractDisjointSet]] = {
           DisjointSetType.STANDARD: DisjointSet,
           DisjointSetType.WEIGHTED: WeightedDisjointSet,
           DisjointSetType.COMPRESSED: CompressedDisjointSet
       }
       
       @classmethod
       def create(cls, ds_type: DisjointSetType) -> AbstractDisjointSet:
           """Create DisjointSet of specified type."""
           impl_class = cls._implementations.get(ds_type)
           if impl_class is None:
               raise ValueError(f"Unknown type: {ds_type}")
           return impl_class()
       
       @classmethod
       def register(cls, ds_type: DisjointSetType, 
                   impl_class: Type[AbstractDisjointSet]):
           """Register new implementation."""
           cls._implementations[ds_type] = impl_class
   
   # Usage
   ds = DisjointSetFactory.create(DisjointSetType.WEIGHTED)

Strategy Pattern
----------------

.. code-block:: python

   class GraphAnalyzer:
       """Analyze graphs using different DisjointSet strategies."""
       
       def __init__(self, ds: AbstractDisjointSet):
           self.ds = ds
       
       def count_components(self, edges: List[Tuple[int, int]]) -> int:
           """Count components using configured strategy."""
           vertices = set()
           for u, v in edges:
               vertices.add(u)
               vertices.add(v)
           
           for v in vertices:
               self.ds.make_set(v)
           
           for u, v in edges:
               self.ds.union(u, v)
           
           return self.ds.count_sets()
   
   # Different strategies
   analyzer1 = GraphAnalyzer(DisjointSet())
   analyzer2 = GraphAnalyzer(WeightedDisjointSet())

See Also
========

* :ref:`api_advanced_interfaces` - API documentation
* :ref:`guide_advanced_disjoint_set` - Disjoint Set guide
* :ref:`guide_design_patterns` - General design patterns

References
==========

.. [1] Gamma, E., et al. (1994). "Design Patterns: Elements of Reusable
       Object-Oriented Software". Addison-Wesley.
       
.. [2] Martin, R. C. (2017). "Clean Architecture: A Craftsman's Guide to
       Software Structure and Design". Prentice Hall.
       
.. [3] Bloch, J. (2018). "Effective Java" (3rd ed.). Addison-Wesley.
       Chapter 4: Classes and Interfaces.
       
.. [4] Phillips, D. (2018). "Python 3 Object-Oriented Programming" (3rd ed.).
       Packt Publishing. Chapter 5: When to Use Object-Oriented Programming.
