.. _guide_errors:

======
Errors
======

Introduction
============

When an operation cannot be carried out, ``sds`` raises an exception from
one hierarchy, rooted at :class:`~sds.core.exceptions.DataStructureError`.
Knowing that hierarchy answers two practical questions: *what went wrong*,
and *which* ``except`` *clause catches it*.

.. code-block:: python

   from sds.core import DataStructureError, EmptyStructureError
   from sds.utils import OptionalDependencyError

The Hierarchy
=============

.. mermaid::

   graph TD
       X[Exception] --> B[DataStructureError]

       B --> E[EmptyStructureError]
       B --> F[FullStructureError]
       B --> O[InvalidOperationError]

       B --> IX[IndexStructureError]
       B --> NF[ElementNotFoundError]
       B --> DU[DuplicateElementError]
       B --> IP[InvalidParameterError]
       B --> TY[StructureTypeError]
       B --> OD[OptionalDependencyError]

       IE[IndexError] --> IX
       VE[ValueError] --> NF
       VE --> DU
       VE --> IP
       TE[TypeError] --> TY
       ME[ImportError] --> OD

       style B fill:#bbf,stroke:#333
       style E fill:#fdb,stroke:#333
       style F fill:#fdb,stroke:#333
       style O fill:#fdb,stroke:#333
       style IX fill:#bfb,stroke:#333
       style NF fill:#bfb,stroke:#333
       style DU fill:#bfb,stroke:#333
       style IP fill:#bfb,stroke:#333
       style TY fill:#bfb,stroke:#333
       style OD fill:#bfb,stroke:#333

Every class derives from ``DataStructureError``. The classes in orange
report a problem with the **state** of the structure; those in green
report a problem with an **argument**, and also derive from the built-in
exception Python code would expect for that kind of argument.

``OptionalDependencyError`` lives in :mod:`sds.utils`, since only the
tooling raises it; all the others live in :mod:`sds.core.exceptions` and
are exported by :mod:`sds.core`.

Arguments versus State
======================

The split follows one question: *would the call succeed with another
argument?*

* **Argument errors.** The argument is wrong in itself or for this
  structure: an index past the end, an element that is not there, a
  negative capacity, a string where a node is expected. Another argument
  would work. These errors are also ``ValueError``, ``TypeError`` or
  ``IndexError``, so code written for the built-in containers keeps
  working: ``except ValueError`` still catches a missing element, as it
  would for ``list.remove()``.

* **State errors.** The argument may be perfectly valid, but the structure
  is not in a state that allows the operation: popping from an empty stack,
  adding a node to a full adjacency matrix, adding an edge that would close
  a cycle in a Bayesian network. Calling again with another argument would
  not help; the structure must change first. These errors are
  ``DataStructureError`` only, on purpose: they are not ``ValueError``,
  because no value was wrong.

.. mermaid::

   graph TD
       Q{Would another argument<br/>make the call succeed?}
       Q -- yes --> A[argument error<br/>also ValueError / TypeError / IndexError]
       Q -- no --> S[state error<br/>DataStructureError only]

       style A fill:#bfb,stroke:#333
       style S fill:#fdb,stroke:#333

Reference
=========

Each row below shows a real message produced by the library.

.. list-table::
   :header-rows: 1
   :widths: 24 16 30 30

   * - Exception
     - Also a
     - Raised when
     - Example
   * - ``EmptyStructureError``
     - —
     - Reading or removing from an empty structure
     - ``Stack().pop()``: *Cannot pop from empty stack*
   * - ``FullStructureError``
     - —
     - Adding to a structure at its capacity
     - third node in ``AdjacencyMatrixGraph(max_nodes=2)``: *Graph is
       full. Maximum 2 nodes allowed*
   * - ``InvalidOperationError``
     - —
     - The state of the structure forbids the operation
     - ``Y -> X`` after ``X -> Y`` in a ``BayesianNetwork``: *Adding edge
       'Y' -> 'X' would introduce a cycle*
   * - ``IndexStructureError``
     - ``IndexError``
     - An index lies outside the structure
     - ``lst[5]`` on a one-item ``LinkedList``: *Index 5 out of range for
       list of size 1*
   * - ``ElementNotFoundError``
     - ``ValueError``
     - The requested element is absent
     - ``bst.remove(9)``: *Item 9 not found in tree*
   * - ``DuplicateElementError``
     - ``ValueError``
     - The element is already present where duplicates are not allowed
     - same node id added twice to a graph: *Node a already exists in
       graph*
   * - ``InvalidParameterError``
     - ``ValueError``
     - An argument value is invalid in itself
     - ``BTree(t=1)``: *Minimum degree t must be at least 2*
   * - ``StructureTypeError``
     - ``TypeError``
     - An argument has the wrong type
     - ``graph.add_node("a")``: *Expected GraphNode, got str*
   * - ``OptionalDependencyError``
     - ``ImportError``
     - A feature needs an extra that is not installed
     - ``save_image()`` without matplotlib: *matplotlib is required for
       this feature: pip install "pysds-tools[image]"*

The API reference of each class is in :doc:`../../api/core/exceptions`
and :doc:`../../api/utils/exceptions`.

Catching Errors
===============

Choose the clause by what the code can actually handle.

**One expected situation.** Catch the precise class:

.. code-block:: python

   from sds.core import EmptyStructureError

   try:
       task = pending.pop()
   except EmptyStructureError:
       task = None          # nothing left to do

**Any problem reported by the library.** Catch the base class, for
instance at the boundary of an application that turns errors into
messages:

.. code-block:: python

   from sds.core import DataStructureError

   try:
       network.add_edge(cause, effect)
   except DataStructureError as err:
       print(f"Rejected: {err}")

``pysds`` does exactly this: every ``DataStructureError`` becomes a
one-line message and exit status 1 (see :doc:`command_line`).

**Code shared with built-in containers.** The built-in parents keep the
usual idioms valid: removing an absent item raises a ``ValueError``, as
``list.remove()`` does. One difference remains: removing from an *empty*
structure is a state error, so ``EmptyStructureError`` must be caught as
well.

.. code-block:: python

   from sds.core import EmptyStructureError

   def discard(container, item):
       """Remove item if present: a list, LinkedList, BST, Tree..."""
       try:
           container.remove(item)
       except (ValueError, EmptyStructureError):
           pass

**An optional feature.** Catch ``OptionalDependencyError`` around the
call, not the import; importing ``sds.utils.visualizer`` never fails:

.. code-block:: python

   from sds.utils import OptionalDependencyError
   from sds.utils.visualizer import save_image, to_text

   try:
       save_image(tree, "tree.png")
   except OptionalDependencyError as err:
       print(err)            # names the pip install command
       print(to_text(tree))

Best Practices
==============

✅ Catch the narrowest class that the code can handle; let the others
propagate.

✅ Catch ``DataStructureError`` only where every library error gets the
same treatment, such as a user interface or a command-line boundary.

✅ Show ``str(err)``: messages name the element, index or option involved.

❌ Do not catch ``ValueError`` to detect an empty structure: emptiness is
a state error, and ``EmptyStructureError`` is not a ``ValueError``.

❌ Do not use a bare ``except Exception`` around library calls: it also
hides programming errors such as a misspelled attribute.

References
==========

* Python documentation, *Errors and Exceptions* (tutorial) —
  https://docs.python.org/3/tutorial/errors.html
* Python documentation, *Built-in Exceptions*, including the exception
  hierarchy — https://docs.python.org/3/library/exceptions.html
