.. _guide_visualizer:

======================
Visualizing Structures
======================

Introduction
============

A data structure is easier to understand when it can be seen. ``print()``
on a structure gives its ``repr``, which says *what* it is but rarely
*how* it is organized. The visualizer answers that second question: it
draws the links of a list, the shape of a tree, the edges of a graph.

.. code-block:: python

   from sds.utils.visualizer import to_text, to_mermaid, to_dot, render, save_image

Concepts
========

From Structure to Drawing
-------------------------

Every structure has a natural picture: a list is a **chain**, a tree is a
**hierarchy** hanging from its root, a graph is a set of **nodes joined by
edges**. The visualizer reduces each structure to one of these three
shapes, a *view*, and then writes the view in the requested format.

.. mermaid::

   graph LR
       L[Linear structure] --> C[chain view]
       T[Tree] --> H[tree view]
       G[Graph] --> N[graph view]
       C --> F{format}
       H --> F
       N --> F
       F --> TX[text]
       F --> MM[Mermaid]
       F --> DT[DOT]
       F --> IM[image]

       style C fill:#3498db,color:#fff
       style H fill:#3498db,color:#fff
       style N fill:#3498db,color:#fff

The view is read through the **public interface** of the structure only:
iteration for linear structures, ``root`` and ``children()`` for trees,
``nodes()`` and ``edges()`` for graphs. The visualizer never looks at
private attributes, so it shows what the structure *is*, not how one
particular class happens to store it. A red-black tree, for instance,
keeps sentinel leaves internally; its ``children()`` hides them, and so
does its drawing.

Why Free Functions?
-------------------

The structures have no ``draw()`` or ``to_mermaid()`` method. Presentation
is kept out of the classes for the same reason algorithms are (see
:doc:`../algorithms/index`): a structure models a container, and adding
every possible output format to it would make each class larger and tie it
to formats that have nothing to do with storing data. As free functions,
the visualizer is written once and serves every structure.

Determinism
-----------

The same structure always gives the same output. Linear structures are
read in iteration order, trees from the root with children in their
stored order, graphs in node and edge **insertion order**. This matters
in practice:

* an output can be compared with an expected string in a test or a doctest;
* a diagram generated for the documentation does not change from one build
  to the next unless the structure does.

The Formats
===========

.. list-table::
   :header-rows: 1
   :widths: 15 30 30 25

   * - Format
     - Best for
     - Function
     - Needs
   * - Text
     - Terminals, logs, doctests
     - :func:`~sds.utils.visualizer.to_text`
     - nothing
   * - Mermaid
     - Sphinx, Markdown, GitHub and GitLab pages
     - :func:`~sds.utils.visualizer.to_mermaid`
     - nothing
   * - DOT
     - Graphviz, large graphs
     - :func:`~sds.utils.visualizer.to_dot` (graphs only)
     - Graphviz to render the source
   * - Image
     - Reports, slides, notebooks
     - :func:`~sds.utils.visualizer.save_image`
     - ``image`` extra

``render(structure, fmt)`` picks one of the three text formats by name;
the ``pysds`` command uses it for its ``--format`` option.

Linear Structures
=================

A linear structure renders as a chain in iteration order. Where the ends
have a meaning, they are named.

.. code-block:: python

   from sds.linear import CircularLinkedList, LinkedList, PriorityQueue, Queue, Stack
   from sds.utils.visualizer import to_mermaid, to_text

   stack, queue, ring = Stack(), Queue(), CircularLinkedList()
   for item in (3, 1, 2):
       stack.push(item)
       queue.enqueue(item)
       ring.append(item)

.. list-table:: Text output after adding 3, then 1, then 2
   :header-rows: 1
   :widths: 30 70

   * - Structure
     - ``to_text()``
   * - ``LinkedList``
     - ``3 -> 1 -> 2``
   * - ``DoublyLinkedList``
     - ``3 <-> 1 <-> 2``
   * - ``CircularLinkedList``
     - ``3 -> 1 -> 2 -> (3)``
   * - ``Stack``
     - ``top: 2 -> 1 -> 3``
   * - ``Queue``, ``Deque``
     - ``front: 3 -> 1 -> 2 :rear``
   * - ``PriorityQueue``
     - ``1 -> 2 -> 3``

The stack shows its last pushed item first, because that is where it will
be popped; the priority queue shows its items in the order it will serve
them.

In Mermaid, a named end becomes a rounded node and a circular list loops
back to its first item:

.. code-block:: text

   flowchart LR
       n0["1"]
       n1["2"]
       n2["3"]
       n0 --> n1
       n1 --> n2
       n2 --> n0

.. mermaid::

   flowchart LR
       n0["1"]
       n1["2"]
       n2["3"]
       n0 --> n1
       n1 --> n2
       n2 --> n0

Trees
=====

Binary Trees
------------

A binary tree renders one node per line; each child is tagged ``L`` or
``R`` so that a single child keeps its side.

.. code-block:: python

   from sds.tree import BinarySearchTree, RedBlackTree

   bst = BinarySearchTree()
   for key in (50, 30, 70, 20, 40):
       bst.insert(key)
   print(to_text(bst))

.. code-block:: text

   50
   ├── L: 30
   │   ├── L: 20
   │   └── R: 40
   └── R: 70

The same tree in Mermaid, top-down:

.. mermaid::

   flowchart TD
       n0["50"]
       n1["30"]
       n2["20"]
       n1 -->|L| n2
       n3["40"]
       n1 -->|R| n3
       n0 -->|L| n1
       n4["70"]
       n0 -->|R| n4

A red-black tree built from 1 to 5 shows its real shape, without its
sentinel leaves:

.. code-block:: text

   2
   ├── L: 1
   └── R: 4
       ├── L: 3
       └── R: 5

General Trees
-------------

Children of a general tree appear in the order they were added:

.. code-block:: python

   from sds.tree import Tree

   tree = Tree()
   root = tree.add_child("root")
   src = tree.add_child("src", root)
   tree.add_child("main.py", src)
   tree.add_child("README", root)
   print(to_text(tree))

.. code-block:: text

   root
   ├── src
   │   └── main.py
   └── README

B-Trees
-------

A B-tree node holds several keys; each node shows them between brackets.
With minimum degree 2, after inserting 1 to 7:

.. code-block:: text

   [2 | 4]
   ├── [1]
   ├── [3]
   └── [5 | 6 | 7]

Mermaid escapes the ``|`` separator itself (``#124;``), so the label is
safe:

.. mermaid::

   flowchart TD
       n0["[2 #124; 4]"]
       n1["[1]"]
       n0 --> n1
       n2["[3]"]
       n0 --> n2
       n3["[5 #124; 6 #124; 7]"]
       n0 --> n3

Graphs
======

A graph renders as an **adjacency list**: one line per node, in insertion
order, followed by its neighbors. ``->`` marks a directed graph, ``--`` an
undirected one, and weights appear in parentheses.

.. code-block:: python

   from sds.graph import GraphNode, WeightedEdge, WeightedGraph

   paris, lyon, lille, nantes = (
       GraphNode(name, key)
       for name, key in [("Paris", "par"), ("Lyon", "lyo"),
                         ("Lille", "lil"), ("Nantes", "nan")]
   )
   roads = WeightedGraph()
   for city in (paris, lyon, lille, nantes):
       roads.add_node(city)
   roads.add_edge(WeightedEdge(paris, lyon, 465))
   roads.add_edge(WeightedEdge(paris, lille, 225))
   roads.add_edge(WeightedEdge(paris, nantes, 385))
   print(to_text(roads))

.. code-block:: text

   Paris -- Lyon (465.0), Lille (225.0), Nantes (385.0)
   Lyon -- Paris (465.0)
   Lille -- Paris (225.0)
   Nantes -- Paris (385.0)

An undirected edge is listed under both of its ends: it can be read from
either.

Mermaid draws the same graph left to right:

.. mermaid::

   flowchart LR
       n0["Paris"]
       n1["Lyon"]
       n2["Lille"]
       n3["Nantes"]
       n0 ---|465.0| n1
       n0 ---|225.0| n2
       n0 ---|385.0| n3

DOT, the input language of Graphviz, is offered for graphs only. Nodes are
identified by their ``id``, so two cities with the same name stay
distinct:

.. code-block:: python

   with open("roads.dot", "w") as stream:
       stream.write(to_dot(roads))

.. code-block:: text

   graph {
       "par" [label="Paris"];
       "lyo" [label="Lyon"];
       "lil" [label="Lille"];
       "nan" [label="Nantes"];
       "par" -- "lyo" [label="465.0"];
       "par" -- "lil" [label="225.0"];
       "par" -- "nan" [label="385.0"];
   }

Graphviz turns it into an image with ``dot -Tsvg roads.dot -o roads.svg``.

Images
======

``save_image()`` draws any supported structure with matplotlib and writes
the file; the extension chooses the format.

.. code-block:: bash

   pip install "pysds-tools[image]"

.. code-block:: python

   from sds.utils.visualizer import save_image

   save_image(bst, "bst.png")
   save_image(roads, "roads.svg")

The visualizer places the nodes itself, with a classic layout for each
shape:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Shape
     - Placement
   * - Chain
     - One row, left to right; a circular list bends its last link back
   * - Binary tree
     - Each node in its own column, in in-order position, one row per
       level: a node always lies between its left and right subtrees
   * - Other trees
     - Each parent centred above its children
   * - Graph
     - Nodes evenly spaced on a circle, from the top, clockwise in
       insertion order; when two edges join the same nodes in opposite
       directions, both are bent so neither hides the other

These layouts are simple on purpose: they are predictable and need no
tuning. For large graphs, where crossings become a problem, export DOT and
let Graphviz compute the layout.

Labels
======

By default a node shows its data and an item shows itself. The ``label``
keyword accepted by every function changes that without touching the
structure:

.. code-block:: python

   print(to_text(roads, label=lambda node: node.id))

.. code-block:: text

   par -- lyo (465.0), lil (225.0), nan (385.0)
   lyo -- par (465.0)
   lil -- par (225.0)
   nan -- par (385.0)

.. list-table:: What ``label`` receives
   :header-rows: 1
   :widths: 40 60

   * - Structure
     - Argument
   * - Linear structures
     - each item
   * - Binary trees, general trees, graphs
     - each node (use ``node.data``, ``node.id``...)
   * - B-trees
     - each key

Typical uses are shortening long data, showing an attribute of stored
objects, or adding a computed value such as a node degree.

Visualizations in Practice
==========================

In Tests and Doctests
---------------------

The text format is deterministic and dependency-free, which makes it a
compact way to assert the shape of a structure:

.. code-block:: python

   def test_avl_rotates_on_sorted_input():
       tree = AVLTree()
       for key in (1, 2, 3):
           tree.insert(key)
       assert to_text(tree) == "2\n├── L: 1\n└── R: 3"

In Documentation
----------------

Mermaid source can go straight into a page. In Sphinx with
``sphinxcontrib-mermaid``, wrap it in a ``.. mermaid::`` directive; in
Markdown rendered by GitHub or GitLab, in a ``mermaid`` code fence:

.. code-block:: python

   with open("bst.md", "w") as stream:
       stream.write("```mermaid\n" + to_mermaid(bst) + "\n```\n")

Every diagram of this page was produced that way.

In Notebooks
------------

Save to SVG and display the file, or print the text form directly in a
cell; both stay readable for structures of a few dozen nodes.

Best Practices
==============

✅ Use ``to_text`` while exploring and testing; switch to Mermaid or an
image only when the result is meant for someone else.

✅ Give graph nodes meaningful ``id`` values: DOT uses them as node names,
and ``label=lambda n: n.id`` shows them.

✅ Generate documentation diagrams from code rather than drawing them by
hand: they then always match the library's behavior.

❌ Do not rely on ``repr()`` to inspect a structure's shape: it summarizes,
it does not draw.

❌ Do not expect the circle layout of ``save_image`` to stay readable for
graphs of hundreds of nodes; use DOT and Graphviz there.

References
==========

* R. Tamassia (ed.), *Handbook of Graph Drawing and Visualization*, CRC
  Press, 2013; chapter 5, A. Rusu, *Tree Drawing Algorithms* (freely
  available chapter) —
  https://cs.brown.edu/people/rtamassi/gdhandbook/chapters/trees.pdf
* Mermaid, *Flowchart syntax* — https://mermaid.js.org/syntax/flowchart.html
* Graphviz, *The DOT Language* — https://graphviz.org/doc/info/lang.html
