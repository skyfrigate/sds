.. _guide_linear_stack:

===========
Stack Guide
===========

.. currentmodule:: sds.linear

Introduction
============

A **stack** is a fundamental linear data structure that follows the 
**Last-In-First-Out (LIFO)** principle. Think of it like a stack of plates:
you can only add or remove plates from the top.

.. mermaid::

   graph TB
       A[Top] --> B[Element 3<br/>Most Recent]
       B --> C[Element 2]
       C --> D[Element 1<br/>First Added]
       D --> E[Bottom]
       
       F[push] -.->|Add to top| A
       A -.->|Remove from top| G[pop]
       
       style A fill:#e74c3c,stroke:#c0392b,color:#fff
       style E fill:#3498db,stroke:#2980b9,color:#fff
       style B fill:#f39c12
       style F fill:#27ae60,stroke:#229954,color:#fff
       style G fill:#e74c3c,stroke:#c0392b,color:#fff

.. note::
   
   This guide covers the theoretical foundations, algorithmic implementation,
   and practical usage of stacks in the SDS library.

Mathematical Model
==================

Formal Definition
-----------------

A stack :math:`S` can be formally defined as an ordered collection with the following properties:

.. math::

   S = \langle e_1, e_2, \ldots, e_n \rangle

where :math:`e_n` is the **top** element (most recently added) and :math:`e_1` is the **bottom** element (first added).

Operations
----------

Push Operation
^^^^^^^^^^^^^^

The push operation adds an element to the top of the stack:

.. math::

   push(S, x) = \langle e_1, e_2, \ldots, e_n, x \rangle

where :math:`x` becomes the new top element.

**Properties:**
   * Time complexity: :math:`O(1)`
   * The size increases: :math:`|S'| = |S| + 1`
   * Previous top becomes second element: :math:`top(S') = x`

Pop Operation
^^^^^^^^^^^^^

The pop operation removes and returns the top element:

.. math::

   pop(\langle e_1, e_2, \ldots, e_n \rangle) = (e_n, \langle e_1, e_2, \ldots, e_{n-1} \rangle)

**Properties:**
   * Time complexity: :math:`O(1)`
   * Returns both the element and the modified stack
   * Undefined for empty stack: :math:`pop(\emptyset)` raises error
   * The size decreases: :math:`|S'| = |S| - 1`

Peek Operation
^^^^^^^^^^^^^^

The peek operation returns the top element without removing it:

.. math::

   peek(\langle e_1, e_2, \ldots, e_n \rangle) = e_n

**Properties:**
   * Time complexity: :math:`O(1)`
   * Non-destructive: :math:`peek(S) \rightarrow e_n` where :math:`S` unchanged
   * Undefined for empty stack

Stack Invariants
----------------

A valid stack maintains these invariants:

1. **LIFO ordering**: 
   
   .. math::
   
      \forall i, j : i < j \implies push_i \text{ before } push_j \implies pop_j \text{ before } pop_i

2. **Size constraint**: 
   
   .. math::
   
      |S| \geq 0

3. **Empty state**: 
   
   .. math::
   
      pop(\emptyset) \text{ is undefined}

4. **Top element accessibility**: 
   
   .. math::
   
      \text{If } |S| > 0 \text{ then } \exists e : e = top(S)

Algebraic Properties
--------------------

Stacks satisfy several algebraic properties:

**Identity Law:**

.. math::

   pop(push(S, x)) = (x, S)

**Associativity (of operations sequence):**

.. math::

   pop(pop(push(push(S, x), y))) = pop(push(S, x))

**Size preservation:**

.. math::

   |push(pop(S)_1, pop(S)_0)| = |S|

where :math:`pop(S)_0` is the returned element and :math:`pop(S)_1` is the resulting stack.

Algorithmic Model
=================

Abstract Data Type (ADT)
-------------------------

The Stack ADT defines the following interface:

.. code-block:: text

   ADT Stack:
       Data:
           - elements: sequence of items
           - top: reference to top element
           - size: number of elements
       
       Operations:
           - Stack(): creates an empty stack
           - push(item): adds item to top
           - pop(): removes and returns top item
           - peek(): returns top item without removing
           - is_empty(): returns true if stack is empty
           - size(): returns number of elements
       
       Axioms:
           - pop(push(S, x)) = x
           - is_empty(Stack()) = true
           - size(push(S, x)) = size(S) + 1

Implementation Strategies
--------------------------

Array-Based Implementation
^^^^^^^^^^^^^^^^^^^^^^^^^^

Using a dynamic array (Python list):

.. mermaid::

   graph LR
       A[Array] --> B["[0]: bottom"]
       A --> C["[1]: ..."]
       A --> D["[n-1]: top"]
       
       E[top pointer] -.-> D
       
       style B fill:#3498db
       style D fill:#e74c3c
       style E fill:#f39c12

**Advantages:**
   * Cache-friendly (contiguous memory)
   * Simple implementation
   * :math:`O(1)` amortized push/pop

**Disadvantages:**
   * Possible reallocation cost
   * Wasted space if stack shrinks
   * Fixed maximum size (without reallocation)

**Pseudocode:**

.. code-block:: text

   Array-Based Stack:
       array: fixed or dynamic array
       top: integer (index of top element)
       capacity: integer (array size)
   
   push(item):
       if top + 1 >= capacity:
           resize(2 * capacity)
       top ← top + 1
       array[top] ← item
   
   pop():
       if top < 0:
           error "Stack underflow"
       item ← array[top]
       top ← top - 1
       if top < capacity / 4:
           resize(capacity / 2)
       return item

Linked List Implementation
^^^^^^^^^^^^^^^^^^^^^^^^^^

Using a singly linked list:

.. mermaid::

   graph LR
       A[Top] --> B[Node 3]
       B --> C[Node 2]
       C --> D[Node 1]
       D --> E[None]
       
       style A fill:#e74c3c
       style E fill:#95a5a6

**Advantages:**
   * No reallocation needed
   * True :math:`O(1)` for all operations
   * Memory allocated on-demand
   * No maximum size

**Disadvantages:**
   * Extra memory for pointers
   * Less cache-friendly
   * Slightly more complex code

**Pseudocode:**

.. code-block:: text

   Linked List Stack:
       top: reference to top node
       size: integer
   
   Node:
       data: any type
       next: reference to next node
   
   push(item):
       new_node ← Node(item)
       new_node.next ← top
       top ← new_node
       size ← size + 1
   
   pop():
       if top = null:
           error "Stack underflow"
       item ← top.data
       top ← top.next
       size ← size - 1
       return item

Algorithm Pseudocode
--------------------

Core Operations
^^^^^^^^^^^^^^^

**Push Algorithm:**

.. code-block:: text

   Algorithm: PUSH(S, item)
   Input: Stack S, element item
   Output: Modified stack S with item at top
   
   1. Create new_node with data = item
   2. new_node.next ← S.top
   3. S.top ← new_node
   4. S.size ← S.size + 1

**Pop Algorithm:**

.. code-block:: text

   Algorithm: POP(S)
   Input: Stack S
   Output: Top element of S
   Precondition: S is not empty
   
   1. if S.top = null then
   2.     raise EmptyStructureError
   3. end if
   4. item ← S.top.data
   5. S.top ← S.top.next
   6. S.size ← S.size - 1
   7. return item

**Peek Algorithm:**

.. code-block:: text

   Algorithm: PEEK(S)
   Input: Stack S
   Output: Top element of S (without removal)
   Precondition: S is not empty
   
   1. if S.top = null then
   2.     raise EmptyStructureError
   3. end if
   4. return S.top.data

Complexity Analysis
-------------------

Time Complexity
^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 25 25 20

   * - Operation
     - Best Case
     - Average Case
     - Worst Case
   * - **Push**
     - :math:`O(1)`
     - :math:`O(1)`
     - :math:`O(n)` *
   * - **Pop**
     - :math:`O(1)`
     - :math:`O(1)`
     - :math:`O(n)` *
   * - **Peek**
     - :math:`O(1)`
     - :math:`O(1)`
     - :math:`O(1)`
   * - **Is Empty**
     - :math:`O(1)`
     - :math:`O(1)`
     - :math:`O(1)`
   * - **Size**
     - :math:`O(1)`
     - :math:`O(1)`
     - :math:`O(1)`

\* For array-based implementation during resizing. With **amortized analysis**, push and pop are :math:`O(1)`.

**Amortized Analysis:**

Consider :math:`n` push operations on an initially empty stack:

.. math::

   T(n) = n + \sum_{i=0}^{\lfloor \log_2 n \rfloor} 2^i = n + 2n - 1 < 3n

Therefore, amortized cost per operation: :math:`\frac{3n}{n} = O(1)`

Space Complexity
^^^^^^^^^^^^^^^^

* **Array-based**: :math:`O(n)` with potential waste if stack shrinks
* **Linked list**: :math:`O(n)` with exact memory usage
* **Space for operations**: :math:`O(1)` auxiliary space

Practical Usage
===============

Installation
------------

.. code-block:: bash

   pip install sds-tools

Basic Usage
-----------

Creating a Stack
^^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.linear import Stack
   
   # Create an empty stack
   stack = Stack()
   
   # Check if empty
   print(stack.is_empty())  # Output: True
   print(len(stack))        # Output: 0

Adding Elements
^^^^^^^^^^^^^^^

.. code-block:: python

   stack = Stack()
   
   # Push elements
   stack.push(10)
   stack.push(20)
   stack.push(30)
   
   print(f"Stack size: {len(stack)}")  # Output: 3
   print(f"Top element: {stack.peek()}")  # Output: 30

Removing Elements
^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Pop elements (LIFO order)
   print(stack.pop())  # Output: 30
   print(stack.pop())  # Output: 20
   
   # Peek without removing
   print(stack.peek())  # Output: 10
   print(len(stack))    # Output: 1

Iteration
^^^^^^^^^

.. code-block:: python

   stack = Stack()
   for i in [1, 2, 3, 4, 5]:
       stack.push(i)
   
   # Iterate (non-destructive, top to bottom)
   for item in stack:
       print(item)  # Output: 5, 4, 3, 2, 1
   
   # Stack still intact
   print(len(stack))  # Output: 5

Real-World Applications
=======================

Application 1: Function Call Stack
-----------------------------------

Understanding recursion through stack visualization:

.. code-block:: python

   from sds.linear import Stack
   
   class CallStack:
       """Simulate function call stack."""
       
       def __init__(self):
           self.stack = Stack()
       
       def call_function(self, func_name, args):
           """Enter a function."""
           frame = {
               'function': func_name,
               'arguments': args,
               'local_vars': {}
           }
           self.stack.push(frame)
           print(f"→ Entering {func_name}{args}")
           print(f"  Stack depth: {len(self.stack)}")
       
       def return_from_function(self):
           """Return from a function."""
           if not self.stack.is_empty():
               frame = self.stack.pop()
               print(f"← Returning from {frame['function']}")
               print(f"  Stack depth: {len(self.stack)}")
               return frame
           return None
       
       def show_stack(self):
           """Display current call stack."""
           print("\nCurrent Call Stack (top to bottom):")
           for i, frame in enumerate(self.stack):
               print(f"  {i}: {frame['function']}{frame['arguments']}")
   
   # Simulate recursive factorial
   def factorial_simulation(n):
       call_stack = CallStack()
       
       def simulate_factorial(x):
           call_stack.call_function('factorial', (x,))
           
           if x <= 1:
               result = 1
           else:
               simulate_factorial(x - 1)
               result = x  # Simplified
           
           call_stack.return_from_function()
           return result
       
       call_stack.show_stack()
       simulate_factorial(n)
       call_stack.show_stack()
   
   factorial_simulation(4)

Application 2: Expression Evaluation
-------------------------------------

**Infix to Postfix Conversion:**

.. code-block:: python

   from sds.linear import Stack
   
   def infix_to_postfix(expression):
       """Convert infix expression to postfix notation."""
       precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
       right_associative = {'^'}
       
       stack = Stack()
       output = []
       
       tokens = expression.split()
       
       for token in tokens:
           if token.isalnum():
               # Operand
               output.append(token)
           
           elif token == '(':
               stack.push(token)
           
           elif token == ')':
               # Pop until matching '('
               while not stack.is_empty() and stack.peek() != '(':
                   output.append(stack.pop())
               if not stack.is_empty():
                   stack.pop()  # Remove '('
           
           elif token in precedence:
               # Operator
               while (not stack.is_empty() and 
                      stack.peek() != '(' and
                      stack.peek() in precedence):
                   
                   top_prec = precedence[stack.peek()]
                   curr_prec = precedence[token]
                   
                   if (top_prec > curr_prec or 
                       (top_prec == curr_prec and token not in right_associative)):
                       output.append(stack.pop())
                   else:
                       break
               
               stack.push(token)
       
       # Pop remaining operators
       while not stack.is_empty():
           output.append(stack.pop())
       
       return ' '.join(output)
   
   # Test
   infix = "A + B * C - D / E"
   postfix = infix_to_postfix(infix)
   print(f"Infix:   {infix}")
   print(f"Postfix: {postfix}")
   # Output: A B C * + D E / -

**Postfix Evaluation:**

.. code-block:: python

   def evaluate_postfix(expression):
       """Evaluate postfix expression."""
       stack = Stack()
       
       for token in expression.split():
           if token.lstrip('-').replace('.', '', 1).isdigit():
               # It's a number
               stack.push(float(token))
           else:
               # It's an operator
               b = stack.pop()
               a = stack.pop()
               
               if token == '+':
                   stack.push(a + b)
               elif token == '-':
                   stack.push(a - b)
               elif token == '*':
                   stack.push(a * b)
               elif token == '/':
                   stack.push(a / b)
               elif token == '^':
                   stack.push(a ** b)
       
       return stack.pop()
   
   # Test
   result = evaluate_postfix("5 1 2 + 4 * + 3 -")
   print(f"Result: {result}")  # Output: 14.0

Application 3: Backtracking (Maze Solver)
------------------------------------------

.. code-block:: python

   from sds.linear import Stack
   
   class MazeSolver:
       """Solve maze using stack-based DFS."""
       
       def __init__(self, maze):
           self.maze = maze
           self.rows = len(maze)
           self.cols = len(maze[0])
       
       def solve(self, start, end):
           """Find path from start to end using stack."""
           stack = Stack()
           visited = set()
           
           stack.push((start, [start]))
           
           while not stack.is_empty():
               (row, col), path = stack.pop()
               
               if (row, col) == end:
                   return path
               
               if (row, col) in visited:
                   continue
               
               visited.add((row, col))
               
               # Explore neighbors (up, right, down, left)
               for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                   new_row, new_col = row + dr, col + dc
                   
                   if (0 <= new_row < self.rows and 
                       0 <= new_col < self.cols and
                       self.maze[new_row][new_col] != 1 and
                       (new_row, new_col) not in visited):
                       
                       new_path = path + [(new_row, new_col)]
                       stack.push(((new_row, new_col), new_path))
           
           return None  # No path found
   
   # Test
   maze = [
       [0, 1, 0, 0, 0],
       [0, 1, 0, 1, 0],
       [0, 0, 0, 1, 0],
       [0, 1, 1, 1, 0],
       [0, 0, 0, 0, 0]
   ]
   
   solver = MazeSolver(maze)
   path = solver.solve((0, 0), (4, 4))
   
   if path:
       print("Path found:")
       for pos in path:
           print(f"  {pos}")
   else:
       print("No path exists")

Application 4: Undo/Redo System
--------------------------------

.. code-block:: python

   from sds.linear import Stack
   
   class UndoRedoManager:
       """Manage undo/redo with two stacks."""
       
       def __init__(self):
           self.undo_stack = Stack()
           self.redo_stack = Stack()
           self.state = ""
       
       def execute(self, action):
           """Execute action and save for undo."""
           self.undo_stack.push((action, self.state))
           self.state = action.execute(self.state)
           
           # Clear redo stack on new action
           self.redo_stack.clear()
       
       def undo(self):
           """Undo last action."""
           if not self.undo_stack.is_empty():
               action, prev_state = self.undo_stack.pop()
               self.redo_stack.push((action, self.state))
               self.state = prev_state
               return True
           return False
       
       def redo(self):
           """Redo last undone action."""
           if not self.redo_stack.is_empty():
               action, prev_state = self.redo_stack.pop()
               self.undo_stack.push((action, self.state))
               self.state = prev_state
               return True
           return False
       
       def __str__(self):
           return self.state
   
   class Action:
       """Base action class."""
       def __init__(self, operation, data):
           self.operation = operation
           self.data = data
       
       def execute(self, state):
           if self.operation == "append":
               return state + self.data
           elif self.operation == "delete":
               return state[:-len(self.data)] if state.endswith(self.data) else state
           return state
   
   # Usage
   manager = UndoRedoManager()
   
   manager.execute(Action("append", "Hello"))
   print(manager)  # Hello
   
   manager.execute(Action("append", " World"))
   print(manager)  # Hello World
   
   manager.undo()
   print(manager)  # Hello
   
   manager.redo()
   print(manager)  # Hello World

Best Practices
==============

Do's
----

✅ **Always check before popping**

.. code-block:: python

   if not stack.is_empty():
       item = stack.pop()
   else:
       print("Stack is empty")

✅ **Use peek for inspection**

.. code-block:: python

   # Good: Check without removing
   if not stack.is_empty() and stack.peek() == target:
       process(stack.pop())

✅ **Handle exceptions properly**

.. code-block:: python

   from sds.core.exceptions import EmptyStructureError
   
   try:
       item = stack.pop()
   except EmptyStructureError:
       print("Cannot pop from empty stack")

✅ **Clear when done**

.. code-block:: python

   # Help garbage collection
   stack.clear()

Don'ts
------

❌ **Don't access by index**

.. code-block:: python

   # Bad: Violates stack abstraction
   item = stack._list[3]
   
   # Good: Use stack operations
   temp = Stack()
   for _ in range(4):
       temp.push(stack.pop())
   item = stack.pop()
   # Restore if needed

❌ **Don't iterate destructively unnecessarily**

.. code-block:: python

   # Bad: Destroys stack
   while not stack.is_empty():
       print(stack.pop())
   
   # Good: Preserve if needed
   for item in stack:
       print(item)

❌ **Don't forget error handling**

.. code-block:: python

   # Bad: May crash
   result = stack.pop()
   
   # Good: Safe
   if not stack.is_empty():
       result = stack.pop()

Performance Tips
----------------

1. **Pre-size if possible**: Know the maximum size ahead of time
2. **Batch operations**: Group multiple operations when possible
3. **Avoid frequent is_empty checks**: Cache the result if checking repeatedly
4. **Use iteration over index access**: Iteration is O(n), indexed access would be O(n²)

Common Pitfalls
===============

1. **Stack Overflow**
   
   Be aware of recursion depth limits:
   
   .. code-block:: python
   
      import sys
      print(sys.getrecursionlimit())  # Default: 1000

2. **Memory Leaks**
   
   Clear stacks when done:
   
   .. code-block:: python
   
      stack.clear()  # Free memory

3. **LIFO Confusion**
   
   Remember the order:
   
   .. code-block:: python
   
      stack.push(1)
      stack.push(2)
      stack.push(3)
      print(list(stack))  # [3, 2, 1] not [1, 2, 3]

4. **Peek vs Pop**
   
   Don't confuse them:
   
   .. code-block:: python
   
      x = stack.peek()  # Just looks, doesn't remove
      y = stack.pop()   # Removes and returns

Further Reading
===============

* :doc:`/api/linear/stack` - Complete API reference
* :doc:`queue` - FIFO alternative
* :doc:`linked_list` - Underlying implementation
