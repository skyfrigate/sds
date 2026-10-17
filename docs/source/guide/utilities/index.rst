.. _guide_utilities:

=========
Utilities
=========

Introduction
============

The previous parts of this guide describe structures and the algorithms
that run on them. This part covers the **tooling** around them: looking at
a structure, describing one in a file, and understanding the errors the
library reports.

All of it lives in :mod:`sds.utils`, the top layer of the package. The
structures never depend on it: ``sds.linear`` or ``sds.graph`` work exactly
the same whether the tooling is used or not.

.. mermaid::

   graph LR
       F[JSON / YAML file] -- pysds show --> S[structure]
       P[Python code] --> S
       S -- visualizer --> T[text]
       S -- visualizer --> M[Mermaid]
       S -- visualizer --> D[DOT]
       S -- visualizer --> I[image]

       style S fill:#3498db,color:#fff

.. list-table::
   :header-rows: 1
   :widths: 25 45 30

   * - Chapter
     - Covers
     - Needs
   * - :doc:`visualizer`
     - Showing any structure as text, Mermaid, DOT or an image, from
       Python
     - nothing; ``image`` extra for images
   * - :doc:`command_line`
     - The ``pysds`` command and the file format that describes a
       structure
     - nothing; ``yaml`` extra for YAML files, ``image`` extra for images
   * - :doc:`errors`
     - The exception hierarchy of the library and how to catch it
     - nothing

The base install has no dependency. The features that need one, images and
YAML files, take it from an *extra* of the distribution; see
:doc:`../installation` for the commands.

.. toctree::
   :maxdepth: 2

   visualizer
   command_line
   errors
