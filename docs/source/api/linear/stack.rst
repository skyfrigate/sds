.. _api_linear_stack:

=====
Stack
=====

.. currentmodule:: sds.linear.stack

Overview
========

This module provides a Stack implementation using a linked list internally.
A stack follows the Last In First Out (LIFO) principle: the last element added
is the first one to be removed.

.. mermaid::

   graph TB
       subgraph "Stack (LIFO)"
       direction TB
       A["[3] ← top"]
       B["[2]"]
       C["[1]"]
       D["[bottom]"]
       
       A --> B
       B --> C
       C --> D
       end
       
       subgraph "Operations"
       E[push 4] --> F["[4,3,2,1]"]
       G["[3,2,1]"] --> H[pop → 3]
       I["[3,2,1]"] --> J[peek → 3]
       end
       
       style A fill:#e74c3c,color:#fff
       style F fill:#2ecc71,color:#fff
       style H fill:#f39c12,color:#fff

Classes
=======

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   Stack

Detailed Documentation
======================

Stack
-----

.. autoclass:: Stack
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __len__, __iter__, __contains__, __repr__, __str__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Properties

   .. autoproperty:: size

   .. rubric:: Core Operations

   .. automethod:: push
   .. automethod:: pop
   .. automethod:: peek

   .. rubric:: Utility Methods

   .. automethod:: is_empty
   .. automethod:: clear
   .. automethod:: add
   .. automethod:: remove

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

Creating and Using Stack
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.linear import Stack

   # Create empty stack
   stack = Stack()
   
   # Check if empty
   print(stack.is_empty())  # True
   
   # Push elements
   stack.push(1)
   stack.push(2)
   stack.push(3)
   
   print(len(stack))  # 3

Push and Pop
^^^^^^^^^^^^

.. code-block:: python

   stack = Stack()
   
   # Push elements (LIFO)
   stack.push("first")
   stack.push("second")
   stack.push("third")
   
   # Pop elements (reverse order)
   print(stack.pop())   # "third"
   print(stack.pop())   # "second"
   print(stack.pop())   # "first"
   
   # Stack is now empty
   print(stack.is_empty())  # True

Peek Operation
^^^^^^^^^^^^^^

.. code-block:: python

   stack = Stack()
   stack.push(1)
   stack.push(2)
   stack.push(3)
   
   # Peek doesn't remove
   print(stack.peek())   # 3
   print(len(stack))     # 3 (unchanged)
   
   # Pop does remove
   print(stack.pop())    # 3
   print(len(stack))     # 2 (changed)

Iteration
^^^^^^^^^

.. code-block:: python

   stack = Stack()
   for i in range(1, 4):
       stack.push(i)
   
   # Iterate from top to bottom
   for item in stack:
       print(item, end=' ')
   # Output: 3 2 1
   
   # Convert to list
   items = list(stack)
   print(items)  # [3, 2, 1]

Contains Check
^^^^^^^^^^^^^^

.. code-block:: python

   stack = Stack()
   stack.push(10)
   stack.push(20)
   stack.push(30)
   
   # Check membership
   print(20 in stack)   # True
   print(40 in stack)   # False

String Representation
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   stack = Stack()
   stack.push(1)
   stack.push(2)
   stack.push(3)
   
   print(repr(stack))
   # Output: Stack([3, 2, 1])
   
   print(str(stack))
   # Output:
   # Stack (top to bottom):
   #   [3]
   #   [2]
   #   [1]

Real-World Examples
===================

Example 1: Expression Evaluation
---------------------------------

Evaluating postfix expressions:

.. code-block:: python

   from sds.linear import Stack

   def evaluate_postfix(expression):
       """Evaluate postfix expression using stack."""
       stack = Stack()
       operators = {'+', '-', '*', '/'}
       
       for token in expression.split():
           if token not in operators:
               # Operand: push to stack
               stack.push(float(token))
           else:
               # Operator: pop two operands
               b = stack.pop()
               a = stack.pop()
               
               if token == '+':
                   result = a + b
               elif token == '-':
                   result = a - b
               elif token == '*':
                   result = a * b
               elif token == '/':
                   result = a / b
               
               stack.push(result)
       
       return stack.pop()
   
   # Usage
   expr = "3 4 + 2 * 7 /"  # ((3+4)*2)/7
   result = evaluate_postfix(expr)
   print(f"Result: {result}")  # 2.0

Example 2: Bracket Matching
----------------------------

Validating balanced brackets:

.. code-block:: python

   from sds.linear import Stack

   def is_balanced(expression):
       """Check if brackets are balanced."""
       stack = Stack()
       pairs = {'(': ')', '[': ']', '{': '}'}
       opening = set(pairs.keys())
       closing = set(pairs.values())
       
       for char in expression:
           if char in opening:
               stack.push(char)
           elif char in closing:
               if stack.is_empty():
                   return False
               
               top = stack.pop()
               if pairs[top] != char:
                   return False
       
       return stack.is_empty()
   
   # Usage
   print(is_balanced("()[]{}"))       # True
   print(is_balanced("([{}])"))       # True
   print(is_balanced("([)]"))         # False
   print(is_balanced("((()"))         # False

Example 3: Undo Functionality
------------------------------

Implementing undo/redo:

.. code-block:: python

   from sds.linear import Stack

   class TextEditor:
       """Simple text editor with undo/redo."""
       
       def __init__(self):
           self.text = ""
           self.undo_stack = Stack()
           self.redo_stack = Stack()
       
       def write(self, text):
           """Add text and save state."""
           self.undo_stack.push(self.text)
           self.text += text
           self.redo_stack.clear()  # Clear redo on new action
       
       def undo(self):
           """Undo last action."""
           if not self.undo_stack.is_empty():
               self.redo_stack.push(self.text)
               self.text = self.undo_stack.pop()
               return True
           return False
       
       def redo(self):
           """Redo last undone action."""
           if not self.redo_stack.is_empty():
               self.undo_stack.push(self.text)
               self.text = self.redo_stack.pop()
               return True
           return False
       
       def get_text(self):
           """Get current text."""
           return self.text
   
   # Usage
   editor = TextEditor()
   editor.write("Hello ")
   editor.write("World")
   print(editor.get_text())  # "Hello World"
   
   editor.undo()
   print(editor.get_text())  # "Hello "
   
   editor.undo()
   print(editor.get_text())  # ""
   
   editor.redo()
   print(editor.get_text())  # "Hello "

Example 4: Function Call Stack
-------------------------------

Simulating function call stack:

.. code-block:: python

   from sds.linear import Stack

   class CallStack:
       """Simulate function call stack."""
       
       def __init__(self):
           self.stack = Stack()
       
       def call_function(self, func_name, args):
           """Enter function."""
           frame = {
               'function': func_name,
               'args': args,
               'locals': {}
           }
           self.stack.push(frame)
           print(f"→ Entering {func_name}{args}")
       
       def return_from_function(self, return_value=None):
           """Exit function."""
           if not self.stack.is_empty():
               frame = self.stack.pop()
               print(f"← Leaving {frame['function']}, "
                     f"return: {return_value}")
               return frame
           return None
       
       def set_local(self, name, value):
           """Set local variable in current frame."""
           if not self.stack.is_empty():
               frame = self.stack.peek()
               frame['locals'][name] = value
       
       def get_local(self, name):
           """Get local variable from current frame."""
           if not self.stack.is_empty():
               frame = self.stack.peek()
               return frame['locals'].get(name)
           return None
       
       def print_stack_trace(self):
           """Print call stack."""
           print("\nCall Stack (bottom to top):")
           for i, frame in enumerate(reversed(list(self.stack))):
               print(f"  {i}: {frame['function']}{frame['args']}")
   
   # Usage
   call_stack = CallStack()
   
   call_stack.call_function("main", ())
   call_stack.call_function("process_data", ([1, 2, 3],))
   call_stack.call_function("helper", (42,))
   
   call_stack.print_stack_trace()
   
   call_stack.return_from_function(True)
   call_stack.return_from_function([1, 2, 3])
   call_stack.return_from_function(0)

Example 5: Depth-First Search
------------------------------

DFS traversal using stack:

.. code-block:: python

   from sds.linear import Stack

   def dfs_iterative(graph, start):
       """Depth-first search using stack."""
       visited = set()
       stack = Stack()
       result = []
       
       stack.push(start)
       
       while not stack.is_empty():
           node = stack.pop()
           
           if node not in visited:
               visited.add(node)
               result.append(node)
               
               # Push neighbors (reverse order for correct traversal)
               for neighbor in reversed(graph.get(node, [])):
                   if neighbor not in visited:
                       stack.push(neighbor)
       
       return result
   
   # Usage
   graph = {
       'A': ['B', 'C'],
       'B': ['D', 'E'],
       'C': ['F'],
       'D': [],
       'E': ['F'],
       'F': []
   }
   
   path = dfs_iterative(graph, 'A')
   print(f"DFS path: {path}")
   # Output: ['A', 'B', 'D', 'E', 'F', 'C']

Performance Characteristics
===========================

Time Complexity
---------------

.. list-table::
   :header-rows: 1
   :widths: 40 20 40

   * - Operation
     - Complexity
     - Notes
   * - ``push(item)``
     - O(1)
     - Prepend to internal list
   * - ``pop()``
     - O(1)
     - Remove from front
   * - ``peek()``
     - O(1)
     - Access first element
   * - ``is_empty()``
     - O(1)
     - Check size
   * - ``clear()``
     - O(1)
     - Reset internal list
   * - ``__len__()``
     - O(1)
     - Cached size
   * - ``__contains__(item)``
     - O(n)
     - Linear search
   * - ``__iter__()``
     - O(n)
     - Traverse all elements

Space Complexity
----------------

* **Storage**: O(n) for n elements
* **Per element overhead**: ~16 bytes (SimpleNode)
* **Stack object**: O(1) additional space

Comparison with Alternatives
=============================

Stack vs List
-------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Aspect
     - Stack (LinkedList)
     - Python list
   * - **Push**
     - O(1)
     - O(1) amortized
   * - **Pop**
     - O(1)
     - O(1)
   * - **Peek**
     - O(1)
     - O(1)
   * - **Memory**
     - More per element
     - More contiguous
   * - **Cache**
     - Poor locality
     - Good locality
   * - **Semantics**
     - LIFO only
     - Full list access

When to Use Stack
-----------------

**Use Stack when:**
   - Only LIFO operations needed
   - Semantic clarity important
   - Implementing recursion iteratively
   - Backtracking algorithms
   - Expression evaluation

**Use Python list when:**
   - Need random access
   - Memory efficiency critical
   - Performance critical (cache locality)
   - Mix of operations needed

Best Practices
==============

Do's
----

✅ **Use for LIFO semantics**

.. code-block:: python

   # Good: Clear intent
   stack = Stack()
   stack.push(item)
   top = stack.pop()
   
   # Less clear: List as stack
   lst = []
   lst.append(item)
   top = lst.pop()

✅ **Check before pop/peek**

.. code-block:: python

   # Good: Safe operation
   if not stack.is_empty():
       item = stack.pop()
   
   # Bad: May raise error
   item = stack.pop()

✅ **Use for recursion elimination**

.. code-block:: python

   # Iterative with stack instead of recursive
   def iterative_traversal(root):
       stack = Stack()
       stack.push(root)
       # Process using stack

Don'ts
------

❌ **Don't use for FIFO operations**

.. code-block:: python

   # Bad: Wrong data structure
   # Use Queue instead

❌ **Don't access middle elements**

.. code-block:: python

   # Bad: Not a stack operation
   # If you need this, use a list

❌ **Don't iterate if you just need to empty**

.. code-block:: python

   # Bad: Inefficient
   while not stack.is_empty():
       item = stack.pop()
   
   # Good: If you don't need items
   stack.clear()

Common Pitfalls
===============

1. **Using wrong data structure**

.. code-block:: python

   # If you need FIFO, use Queue not Stack
   # If you need random access, use list

2. **Not handling empty stack**

.. code-block:: python

   # Always check before pop/peek
   if not stack.is_empty():
       item = stack.pop()

3. **Confusing with Queue**

.. code-block:: python

   # Stack: Last In First Out (LIFO)
   # Queue: First In First Out (FIFO)

Design Patterns
===============

Command Pattern
---------------

.. code-block:: python

   class Command:
       def execute(self):
           pass
       
       def undo(self):
           pass
   
   class CommandHistory:
       def __init__(self):
           self.history = Stack()
       
       def execute(self, command):
           command.execute()
           self.history.push(command)
       
       def undo(self):
           if not self.history.is_empty():
               command = self.history.pop()
               command.undo()

Memento Pattern
---------------

.. code-block:: python

   class Memento:
       def __init__(self, state):
           self.state = state
   
   class Originator:
       def __init__(self):
           self.state = None
           self.history = Stack()
       
       def set_state(self, state):
           self.history.push(Memento(self.state))
           self.state = state
       
       def undo(self):
           if not self.history.is_empty():
               memento = self.history.pop()
               self.state = memento.state

See Also
========

* :doc:`queue` - FIFO queue structures
* :doc:`list` - Linked list implementations
* :doc:`../../guide/linear_structures/stack` - Stack theory and guide

References
==========

.. [1] Cormen, T. H., et al. "Introduction to Algorithms", 3rd Edition, Chapter 10
.. [2] Knuth, D. E. "The Art of Computer Programming, Volume 1", Section 2.2
.. [3] Sedgewick, R., Wayne, K. "Algorithms", 4th Edition, Section 1.3
.. [4] Aho, A. V., et al. "Compilers: Principles, Techniques, and Tools", Chapter 3
