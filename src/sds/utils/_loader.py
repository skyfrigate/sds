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

"""Build a structure from a plain-data description, for the command line.

The command line (#106) reads a JSON or YAML document and turns it into a
structure with :func:`build`. The document is an object naming the class
in ``type``, constructor arguments in an optional ``options`` object, and
the content in a key that depends on the kind of structure:

- linear structures and keyed trees (binary, search, AVL, red-black,
  B-tree): ``items``, a list added in order;
- general trees (``Tree``): ``root``, a nested ``{"data", "children"}``
  object;
- graphs: ``nodes``, a list of ``{"id", "data"}`` objects (``data``
  defaults to the id), and ``edges``, a list of ``[source, target]`` or
  ``[source, target, weight]`` lists of node ids. The edge class follows
  from the graph class.

This module is private: it serves the command line only and offers no
public API. Errors in the document raise :class:`InvalidParameterError`
prefixed with the place of the problem (``edges[2]: ...``); an unknown or
unsupported ``type`` raises :class:`StructureTypeError`.
"""

import inspect
from contextlib import contextmanager
from typing import Any, Dict, Iterator, List, Mapping, Optional, Tuple, Type

from ..core.exceptions import (
    DataStructureError,
    InvalidParameterError,
    StructureTypeError,
)
from ..graph import (
    AdjacencyListGraph,
    AdjacencyMatrixGraph,
    DirectedEdge,
    DirectedGraph,
    Edge,
    Graph,
    GraphNode,
    UndirectedGraph,
    WeightedDirectedEdge,
    WeightedDirectedGraph,
    WeightedEdge,
    WeightedGraph,
)
from ..graph.interfaces import AbstractGraph
from ..linear import (
    CircularLinkedList,
    Deque,
    DoublyLinkedList,
    LinkedList,
    PriorityQueue,
    Queue,
    Stack,
    from_list,
)
from ..tree import AVLTree, BinarySearchTree, BinaryTree, BTree, RedBlackTree, Tree

__all__ = ["SUPPORTED", "build"]

_LINEAR: Dict[str, type] = {
    cls.__name__: cls
    for cls in (
        LinkedList,
        DoublyLinkedList,
        CircularLinkedList,
        Stack,
        Queue,
        Deque,
        PriorityQueue,
    )
}

_KEYED_TREES: Dict[str, type] = {
    cls.__name__: cls
    for cls in (BinaryTree, BinarySearchTree, AVLTree, RedBlackTree, BTree)
}

#: Graph class name -> (graph class, edge class it takes).
_GRAPHS: Dict[str, Tuple[Type[AbstractGraph], type]] = {
    cls.__name__: (cls, edge)
    for cls, edge in (
        (Graph, Edge),
        (UndirectedGraph, Edge),
        (AdjacencyListGraph, Edge),
        (AdjacencyMatrixGraph, Edge),
        (DirectedGraph, DirectedEdge),
        (WeightedGraph, WeightedEdge),
        (WeightedDirectedGraph, WeightedDirectedEdge),
    )
}

_WEIGHTED_EDGES = (WeightedEdge, WeightedDirectedEdge)

#: Class names :func:`build` accepts, in alphabetical order.
SUPPORTED = tuple(
    sorted([*_LINEAR, *_KEYED_TREES, Tree.__name__, *_GRAPHS], key=str.lower)
)


@contextmanager
def _at(place: str) -> Iterator[None]:
    """Prefix any error raised by the structure with ``place``.

    ``TypeError`` is included: comparing items of different types while
    inserting them in a search tree or a priority queue raises it.
    """
    try:
        yield
    except (DataStructureError, TypeError) as exc:
        raise InvalidParameterError(f"{place}: {exc}") from exc


def _expect(value: Any, kind: type, place: str, what: str) -> Any:
    if not isinstance(value, kind):
        raise InvalidParameterError(f"{place}: expected {what}")
    return value


def _check_keys(document: Mapping[str, Any], content: Tuple[str, ...]) -> None:
    unknown = sorted(set(document) - {"type", "options", *content})
    if unknown:
        allowed = ", ".join(repr(key) for key in content)
        raise InvalidParameterError(
            f"unknown key {unknown[0]!r} for {document['type']}: "
            f"use 'type', 'options' and {allowed}"
        )


def _check_options(cls: type, options: Dict[str, Any]) -> None:
    """Reject options the constructor of ``cls`` does not take.

    Checking the signature before any call keeps the error at ``options``
    even when the structure is built inside :func:`from_list`, whose own
    errors are reported at ``items``.
    """
    try:
        inspect.signature(cls).bind(**options)
    except TypeError as exc:
        raise InvalidParameterError(f"options: {cls.__name__}() {exc}") from exc


def _construct(cls: type, options: Dict[str, Any]) -> Any:
    _check_options(cls, options)
    try:
        return cls(**options)
    except DataStructureError:
        raise
    except TypeError as exc:
        raise InvalidParameterError(f"options: {exc}") from exc


def build(document: Any) -> Any:
    """Return the structure described by ``document``.

    Parameters
    ----------
    document : Any
        The decoded JSON or YAML document; see the module documentation.

    Returns
    -------
    Any
        A new structure of the class named by ``document["type"]``.

    Raises
    ------
    StructureTypeError
        If ``type`` names no class :func:`build` supports.
    InvalidParameterError
        If the document is malformed, or the structure rejects its
        content (a duplicate node, an edge to an unknown node...).

    Examples
    --------
    >>> stack = build({"type": "Stack", "items": [1, 2, 3]})
    >>> stack.peek()
    3
    >>> graph = build({"type": "DirectedGraph", "nodes": [{"id": "a"}, {"id": "b"}],
    ...                "edges": [["a", "b"]]})
    >>> graph.edge_count()
    1
    """
    if not isinstance(document, dict):
        raise InvalidParameterError("expected an object with a 'type' key")
    name = document.get("type")
    if not isinstance(name, str):
        raise InvalidParameterError("'type' must name a structure class")
    options = _expect(document.get("options", {}), dict, "options", "an object")

    if name in _LINEAR:
        _check_keys(document, ("items",))
        linear_cls = _LINEAR[name]
        _check_options(linear_cls, options)
        items = _expect(document.get("items", []), list, "items", "a list")
        with _at("items"):
            return from_list(linear_cls, items, **options)
    if name in _KEYED_TREES:
        _check_keys(document, ("items",))
        return _keyed_tree(_KEYED_TREES[name], options, document.get("items", []))
    if name == Tree.__name__:
        _check_keys(document, ("root",))
        if options:
            raise InvalidParameterError(
                "options: Tree takes no options; describe the tree in 'root'"
            )
        return _general_tree(document.get("root"))
    if name in _GRAPHS:
        _check_keys(document, ("nodes", "edges"))
        graph_cls, edge_cls = _GRAPHS[name]
        return _graph(
            _construct(graph_cls, options),
            edge_cls,
            document.get("nodes", []),
            document.get("edges", []),
        )
    raise StructureTypeError(
        f"unsupported type {name!r}: use one of {', '.join(SUPPORTED)}"
    )


def _keyed_tree(cls: type, options: Dict[str, Any], items: Any) -> Any:
    tree = _construct(cls, options)
    for index, item in enumerate(_expect(items, list, "items", "a list")):
        with _at(f"items[{index}]"):
            tree.insert(item)
    return tree


def _general_tree(root: Any) -> Tree:
    tree = Tree()
    if root is None:
        return tree

    def add(spec: Any, parent: Optional[Any], place: str) -> None:
        spec = _expect(spec, dict, place, "an object with 'data' and 'children'")
        unknown = sorted(set(spec) - {"data", "children"})
        if unknown:
            raise InvalidParameterError(
                f"{place}: unknown key {unknown[0]!r}: use 'data' and 'children'"
            )
        if "data" not in spec:
            raise InvalidParameterError(f"{place}: missing 'data'")
        node = tree.add_child(spec["data"], parent)
        children = _expect(spec.get("children", []), list, place, "a list")
        for index, child in enumerate(children):
            add(child, node, f"{place}.children[{index}]")

    add(root, None, "root")
    return tree


def _node_id(value: Any, place: str) -> str:
    # bool is an int, but True is no sensible node id.
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise InvalidParameterError(f"{place}: a node id is a string or an integer")
    return str(value)


def _graph(graph: Any, edge_cls: type, nodes: Any, edges: Any) -> Any:
    by_id: Dict[str, GraphNode] = {}
    for index, spec in enumerate(_expect(nodes, list, "nodes", "a list")):
        place = f"nodes[{index}]"
        spec = _expect(spec, dict, place, "an object with 'id' and 'data'")
        unknown = sorted(set(spec) - {"id", "data"})
        if unknown:
            raise InvalidParameterError(
                f"{place}: unknown key {unknown[0]!r}: use 'id' and 'data'"
            )
        if "id" not in spec:
            raise InvalidParameterError(f"{place}: missing 'id'")
        node_id = _node_id(spec["id"], place)
        node = GraphNode(spec.get("data", node_id), node_id)
        with _at(place):
            graph.add_node(node)
        by_id[node_id] = node

    weighted = issubclass(edge_cls, _WEIGHTED_EDGES)
    for index, spec in enumerate(_expect(edges, list, "edges", "a list")):
        place = f"edges[{index}]"
        spec = _expect(
            spec, list, place, "[source, target] or [source, target, weight]"
        )
        if len(spec) not in (2, 3):
            raise InvalidParameterError(
                f"{place}: expected [source, target] or [source, target, weight]"
            )
        ends: List[GraphNode] = []
        for value in spec[:2]:
            node_id = _node_id(value, place)
            if node_id not in by_id:
                raise InvalidParameterError(f"{place}: unknown node {node_id!r}")
            ends.append(by_id[node_id])
        args: List[Any] = list(ends)
        if len(spec) == 3:
            if not weighted:
                raise InvalidParameterError(
                    f"{place}: {type(graph).__name__} is not weighted; "
                    "give [source, target]"
                )
            weight = spec[2]
            if isinstance(weight, bool) or not isinstance(weight, (int, float)):
                raise InvalidParameterError(f"{place}: the weight must be a number")
            args.append(weight)
        with _at(place):
            graph.add_edge(edge_cls(*args))
    return graph
