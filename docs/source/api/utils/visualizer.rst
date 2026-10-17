.. _api_utils_visualizer:

==========
Visualizer
==========

.. currentmodule:: sds.utils.visualizer

Overview
========

The visualizer shows a structure in four forms: plain text for a terminal
or a doctest, Mermaid for documentation pages, DOT for Graphviz, and an
image file. It is a set of free functions: presentation stays out of the
structure classes, which keep no drawing code and no dependency.

.. list-table::
   :header-rows: 1
   :widths: 18 30 27 25

   * - Function
     - Produces
     - Accepts
     - Dependency
   * - :func:`to_text`
     - Plain text, one line or one node per line
     - every supported structure
     - none
   * - :func:`to_mermaid`
     - Mermaid flowchart source
     - every supported structure
     - none
   * - :func:`to_dot`
     - Graphviz DOT source
     - graphs only
     - none (Graphviz only to render the source)
   * - :func:`render`
     - One of the three text formats, chosen by name
     - as the chosen format
     - none
   * - :func:`save_image`
     - PNG, SVG, PDF or any format matplotlib writes
     - every supported structure
     - ``image`` extra

.. mermaid::

   graph LR
       S[structure] --> V[view<br/>nodes, edges, labels]
       V --> T[to_text]
       V --> M[to_mermaid]
       V --> D[to_dot]
       V --> L[layout] --> I[save_image]

       style V fill:#3498db,color:#fff

Every function first reads the structure into the same intermediate view,
through public accessors only, then writes that view in its format. Two
formats of the same structure therefore always show the same nodes in the
same order.

.. note::

   **Output is deterministic.** Linear structures are read in iteration
   order, trees from the root, graphs in node and edge insertion order. The
   same structure always renders to the same text, which makes the output
   safe to compare in tests and to commit in documentation.

Supported Structures
====================

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Family
     - Classes
     - Rendered as
   * - Linear
     - ``LinkedList``, ``DoublyLinkedList``, ``CircularLinkedList``,
       ``Stack``, ``Queue``, ``Deque``, ``PriorityQueue``
     - A chain, with ``top`` for a stack and ``front`` / ``rear`` for
       queues; a circular list points back to its first item
   * - Binary trees
     - ``BinaryTree``, ``BinarySearchTree``, ``AVLTree``,
       ``RedBlackTree``
     - A tree whose children are tagged ``L`` or ``R``; the sentinel
       leaves of a red-black tree are not shown
   * - General trees
     - ``Tree``
     - A tree, children in insertion order
   * - B-trees
     - ``BTree``
     - A tree of nodes, each showing its keys
   * - Graphs
     - every graph of ``sds.graph``
     - Nodes and edges, with direction and weights

Heaps, tries, segment trees and the structures of ``sds.advanced`` and
``sds.probabilistic`` are not supported yet: passing one raises
:class:`~sds.core.exceptions.StructureTypeError`.

Labels
======

Every function takes an optional keyword argument ``label``: a callable
that returns the text to show for one element. What it receives depends on
the structure:

.. list-table::
   :header-rows: 1
   :widths: 35 30 35

   * - Structure
     - ``label`` receives
     - Default
   * - Linear structures
     - each item
     - ``str(item)``
   * - Binary and general trees, graphs
     - each node
     - ``str(node.data)``
   * - B-trees
     - each key
     - ``str(key)``

.. code-block:: python

   # Show the node ids of a graph instead of their data
   print(to_text(graph, label=lambda node: node.id))

Formats escape labels themselves: a label may hold quotes, pipes or line
breaks without breaking the Mermaid or DOT source.

Text Formats
============

to_text
-------

.. autofunction:: to_text

The three families render as follows. A doubly linked list shows its
two-way links:

.. code-block:: text

   1 <-> 2 <-> 3

A general tree uses box-drawing branches:

.. code-block:: text

   root
   ├── src
   │   └── main.py
   └── README

A B-tree of minimum degree 2 after inserting 1 to 7 shows the keys of each
node:

.. code-block:: text

   [2 | 4]
   ├── [1]
   ├── [3]
   └── [5 | 6 | 7]

A weighted directed graph is an adjacency list, one line per node:

.. code-block:: text

   A -> B (4.0), C (1.0)
   B
   C -> B (2.0)

to_mermaid
----------

.. autofunction:: to_mermaid

The source can be pasted into any Mermaid renderer, including the
``.. mermaid::`` directive of this documentation. The weighted directed
graph above gives:

.. code-block:: text

   flowchart LR
       n0["A"]
       n1["B"]
       n2["C"]
       n0 -->|4.0| n1
       n0 -->|1.0| n2
       n2 -->|2.0| n1

which renders as:

.. mermaid::

   flowchart LR
       n0["A"]
       n1["B"]
       n2["C"]
       n0 -->|4.0| n1
       n0 -->|1.0| n2
       n2 -->|2.0| n1

to_dot
------

.. autofunction:: to_dot

The DOT source is plain text; turning it into an image is Graphviz's job,
for instance ``dot -Tpng graph.dot -o graph.png``. The same graph gives:

.. code-block:: text

   digraph {
       "A" [label="A"];
       "B" [label="B"];
       "C" [label="C"];
       "A" -> "B" [label="4.0"];
       "A" -> "C" [label="1.0"];
       "C" -> "B" [label="2.0"];
   }

render
------

.. autofunction:: render

.. autodata:: FORMATS
   :no-value:

``FORMATS`` is the tuple ``("text", "mermaid", "dot")``.

Image Output
============

save_image
----------

.. autofunction:: save_image

The visualizer places the nodes itself, so the drawing needs nothing but
matplotlib:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Structure
     - Layout
   * - Linear structures
     - One row, left to right
   * - Binary trees
     - One column per node in in-order position, one row per level
   * - General trees and B-trees
     - Each parent centred above its children
   * - Graphs
     - Nodes on a circle, from the top, clockwise in insertion order;
       two opposite edges are bent so both stay visible

Usage Example: Documenting a Graph
==================================

.. code-block:: python

   from sds.graph import GraphNode, WeightedDirectedEdge, WeightedDirectedGraph
   from sds.utils.visualizer import render, save_image, to_text

   a, b, c = (GraphNode(name, name) for name in "ABC")
   graph = WeightedDirectedGraph()
   for node in (a, b, c):
       graph.add_node(node)
   graph.add_edge(WeightedDirectedEdge(a, b, 4))
   graph.add_edge(WeightedDirectedEdge(a, c, 1))
   graph.add_edge(WeightedDirectedEdge(c, b, 2))

   print(to_text(graph))                       # quick look in a terminal
   with open("graph.mmd", "w") as stream:      # for a Markdown page
       stream.write(render(graph, "mermaid"))
   save_image(graph, "graph.svg")              # needs the image extra

Best Practices
==============

✅ Use ``to_text`` in doctests and assertions: its output is short,
deterministic and dependency-free.

✅ Use ``to_mermaid`` for documentation pages, and ``to_dot`` when Graphviz
is already part of the toolchain or the graph is large.

✅ Pass a ``label`` callable rather than changing the data stored in the
structure to get a readable drawing.

❌ Do not call ``to_dot`` on a tree or a list: DOT output is offered for
graphs only and raises ``StructureTypeError`` otherwise.

❌ Do not import ``matplotlib.pyplot`` just to save an image:
``save_image`` builds its figure with matplotlib's object API and leaves
the pyplot state untouched.

References
==========

* Mermaid, *Flowchart syntax* — https://mermaid.js.org/syntax/flowchart.html
* Graphviz, *The DOT Language* — https://graphviz.org/doc/info/lang.html
* matplotlib, *Figure.savefig* (output formats) —
  https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.savefig.html
