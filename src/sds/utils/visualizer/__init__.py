# Copyright 2024-2026, skyfrigate, biface
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Text, Mermaid, DOT and image rendering of data structures.

The visualiser is a set of free functions (#102): presentation stays out
of the structure classes (#14), and the text formats need no dependency.
Rendering reads public accessors only, so the output order is the one of
the structures themselves, deterministic since #91.

Supported structures: every linear structure, binary search trees (plain,
AVL, red-black), general trees, B-trees, and every graph. Heaps, tries,
segment trees and the structures of ``sds.advanced`` and
``sds.probabilistic`` are not supported yet.

Labels
------
Every function takes an optional ``label`` callable. It receives the
node for trees and graphs, the item for linear structures and the key
for B-trees, and returns the text to display. By default the visualiser
shows ``str(node.data)``, or ``str(item)``.
"""

import os
from typing import Any, Union

from ...core.exceptions import InvalidParameterError, StructureTypeError
from ._dot import graph_dot
from ._image import save_drawing
from ._layout import layout
from ._mermaid import view_mermaid
from ._text import view_text
from ._views import GraphView, Label, build_view

__all__ = ["FORMATS", "render", "save_image", "to_dot", "to_mermaid", "to_text"]

#: Text formats accepted by :func:`render`.
FORMATS = ("text", "mermaid", "dot")


def to_text(structure: Any, *, label: Label = None) -> str:
    """Render a structure as plain text.

    Linear structures render on one line, with named ends where they have
    a meaning (``top`` of a stack, ``front``/``rear`` of a queue). Trees
    render one node per line with box-drawing branches; children of a
    binary tree are tagged ``L``/``R``. Graphs render as an adjacency list
    in insertion order, with ``->`` for directed and ``--`` for undirected
    graphs, and the weight of each edge in parentheses.

    Parameters
    ----------
    structure : Any
        A supported structure (see the module documentation).
    label : Callable[[Any], str], optional
        Labelling function; see the module documentation.

    Returns
    -------
    str
        The rendering, ``(empty)`` for an empty structure.

    Raises
    ------
    StructureTypeError
        If the structure is not supported.

    Examples
    --------
    >>> from sds.linear import Stack
    >>> stack = Stack()
    >>> for item in (1, 2, 3):
    ...     stack.push(item)
    >>> print(to_text(stack))
    top: 3 -> 2 -> 1

    >>> from sds.tree import BinarySearchTree
    >>> tree = BinarySearchTree()
    >>> for key in (50, 30, 70, 20, 40):
    ...     tree.insert(key)
    >>> print(to_text(tree))
    50
    ├── L: 30
    │   ├── L: 20
    │   └── R: 40
    └── R: 70
    """
    return view_text(build_view(structure, label))


def to_mermaid(structure: Any, *, label: Label = None) -> str:
    """Render a structure as a Mermaid flowchart.

    Linear structures and graphs are drawn left to right (``flowchart LR``),
    trees top-down (``flowchart TD``). Directed graphs use ``-->``,
    undirected graphs ``---``; weights and the L/R side of binary-tree
    children become edge labels. Named ends of stacks and queues become
    rounded nodes. Node ids are generated (``n0``, ``n1``...) and labels
    are escaped, so any label is safe to embed in a Markdown or reST page.

    Parameters
    ----------
    structure : Any
        A supported structure (see the module documentation).
    label : Callable[[Any], str], optional
        Labelling function; see the module documentation.

    Returns
    -------
    str
        The Mermaid source, without the surrounding code fence. An empty
        structure gives the ``flowchart`` line alone.

    Raises
    ------
    StructureTypeError
        If the structure is not supported.

    Examples
    --------
    >>> from sds.tree import BinarySearchTree
    >>> tree = BinarySearchTree()
    >>> for key in (2, 1, 3):
    ...     tree.insert(key)
    >>> print(to_mermaid(tree))
    flowchart TD
        n0["2"]
        n1["1"]
        n0 -->|L| n1
        n2["3"]
        n0 -->|R| n2
    """
    return view_mermaid(build_view(structure, label))


def to_dot(graph: Any, *, label: Label = None) -> str:
    """Render a graph as Graphviz DOT source.

    Directed graphs become a ``digraph`` with ``->`` edges, the others a
    ``graph`` with ``--`` edges. Nodes are identified by their ``id`` and
    labelled with ``label``; weights become edge labels. Producing the
    source needs no Graphviz install; rendering it does.

    Parameters
    ----------
    graph : AbstractGraph
        The graph to render.
    label : Callable[[Any], str], optional
        Labelling function; it receives each node.

    Returns
    -------
    str
        The DOT source.

    Raises
    ------
    StructureTypeError
        If ``graph`` is not a graph: DOT is offered for graphs only.

    Examples
    --------
    >>> from sds.graph import DirectedEdge, DirectedGraph, GraphNode
    >>> graph = DirectedGraph()
    >>> a, b = GraphNode("A", "n1"), GraphNode("B", "n2")
    >>> graph.add_node(a)
    >>> graph.add_node(b)
    >>> graph.add_edge(DirectedEdge(a, b))
    >>> print(to_dot(graph))
    digraph {
        "n1" [label="A"];
        "n2" [label="B"];
        "n1" -> "n2";
    }
    """
    view = build_view(graph, label)
    if not isinstance(view, GraphView):
        raise StructureTypeError(
            f"DOT output is for graphs only, not {type(graph).__name__}"
        )
    return graph_dot(view)


def save_image(
    structure: Any,
    path: Union[str, "os.PathLike[str]"],
    *,
    label: Label = None,
) -> None:
    """Draw a structure and save the image to ``path``.

    Needs the ``image`` extra: ``pip install "pysds-tools[image]"``. The
    format follows the file extension (``.png``, ``.svg``, ``.pdf``, or
    any other format matplotlib writes). Nodes are placed by the
    visualiser: a row for linear structures, in-order columns for binary
    trees, children-centred parents for other trees, a circle for graphs.

    Parameters
    ----------
    structure : Any
        A supported structure (see the module documentation).
    path : str or os.PathLike
        Destination file; its extension selects the format.
    label : Callable[[Any], str], optional
        Labelling function; see the module documentation.

    Raises
    ------
    StructureTypeError
        If the structure is not supported.
    OptionalDependencyError
        If matplotlib is not installed.
    InvalidParameterError
        If the extension names no format matplotlib can write.

    Notes
    -----
    The figure is built with matplotlib's object API: no window opens and
    the global pyplot state is not touched.
    """
    save_drawing(layout(build_view(structure, label)), path)


def render(structure: Any, fmt: str = "text", *, label: Label = None) -> str:
    """Render a structure in one of the text formats.

    Dispatches to :func:`to_text`, :func:`to_mermaid` or :func:`to_dot`;
    the command line uses it to honour its format option.

    Parameters
    ----------
    structure : Any
        A supported structure (see the module documentation).
    fmt : str, default "text"
        One of :data:`FORMATS`: ``"text"``, ``"mermaid"`` or ``"dot"``.
    label : Callable[[Any], str], optional
        Labelling function; see the module documentation.

    Returns
    -------
    str
        The rendering.

    Raises
    ------
    InvalidParameterError
        If ``fmt`` is not one of :data:`FORMATS`.
    StructureTypeError
        If the structure is not supported, or ``fmt`` is ``"dot"`` and the
        structure is not a graph.

    Examples
    --------
    >>> from sds.linear import Queue
    >>> queue = Queue()
    >>> for item in (1, 2):
    ...     queue.enqueue(item)
    >>> print(render(queue))
    front: 1 -> 2 :rear
    >>> render(queue, "svg")
    Traceback (most recent call last):
        ...
    sds.core.exceptions.InvalidParameterError: Unknown format 'svg': use one of text, mermaid, dot
    """
    if fmt == "text":
        return to_text(structure, label=label)
    if fmt == "mermaid":
        return to_mermaid(structure, label=label)
    if fmt == "dot":
        return to_dot(structure, label=label)
    raise InvalidParameterError(
        f"Unknown format {fmt!r}: use one of {', '.join(FORMATS)}"
    )
