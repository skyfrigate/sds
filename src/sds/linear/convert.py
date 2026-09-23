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

"""Conversion between Python lists and linear structures.

Two free functions, generic over every
:class:`~sds.core.interfaces.LinearCollection` subclass, bridge the
``list``-based sorting functions of ``sds.algorithms.sorting`` and the
structures of this module (#94):

- :func:`to_list` materializes a structure in its iteration order;
- :func:`from_list` builds a structure by feeding items to its ``add()``.

Neither function knows about any particular class: they rely only on
``__iter__`` and ``add()``, which every linear structure already
implements with its own semantics (``append`` for linked lists, ``push``
for :class:`Stack`, ``enqueue`` for :class:`Queue` and
:class:`PriorityQueue`, ``add_rear`` for :class:`Deque`).

Round trip
----------
``to_list(from_list(cls, items)) == list(items)`` holds for
:class:`LinkedList`, :class:`DoublyLinkedList`,
:class:`CircularLinkedList`, :class:`Queue` and :class:`Deque`, which
preserve insertion order. It does **not** hold, by design, for:

- :class:`Stack`, which iterates top to bottom and therefore yields the
  items reversed;
- :class:`PriorityQueue`, which iterates in priority order.

Examples
--------
>>> from sds.linear import LinkedList, Stack, from_list, to_list
>>> to_list(from_list(LinkedList, [3, 1, 2]))
[3, 1, 2]
>>> to_list(from_list(Stack, [3, 1, 2]))
[2, 1, 3]

Sorting a structure and getting a structure back:

>>> from sds.linear import Queue
>>> queue = from_list(Queue, [3, 1, 2])
>>> to_list(from_list(Queue, sorted(to_list(queue))))
[1, 2, 3]
"""

from typing import Any, Iterable, List, Type, TypeVar

from ..core.interfaces import LinearCollection

C = TypeVar("C", bound=LinearCollection)

__all__ = ["from_list", "to_list"]


def to_list(structure: LinearCollection) -> List[Any]:
    """Return the items of a linear structure as a new ``list``.

    Items come out in the structure's own iteration order, so the result
    of a :class:`~sds.linear.Stack` starts with its top element and the
    result of a :class:`~sds.linear.PriorityQueue` starts with its
    highest-priority element.

    Parameters
    ----------
    structure : LinearCollection
        Any linear structure. It is left unchanged.

    Returns
    -------
    list
        A new list; mutating it does not affect ``structure``.

    Raises
    ------
    TypeError
        If ``structure`` is not a ``LinearCollection``.

    Examples
    --------
    >>> from sds.linear import Deque, to_list
    >>> d = Deque()
    >>> d.add_rear(1)
    >>> d.add_front(0)
    >>> to_list(d)
    [0, 1]

    Notes
    -----
    Time complexity: O(n). Space complexity: O(n).
    """
    if not isinstance(structure, LinearCollection):
        raise TypeError(f"Expected a LinearCollection, got {type(structure).__name__}")
    return list(structure)


def from_list(cls: Type[C], items: Iterable[Any], **kwargs: Any) -> C:
    """Build a linear structure of type ``cls`` from ``items``.

    A fresh ``cls(**kwargs)`` is created, then each item is passed, in
    order, to its ``add()`` method. What "adding" means is up to the
    structure: appended to a linked list, pushed on a stack, inserted at
    its priority in a priority queue.

    Parameters
    ----------
    cls : type
        A concrete ``LinearCollection`` subclass.
    items : iterable
        Items to add, in order. Any iterable is accepted, including
        another linear structure.
    **kwargs
        Forwarded to the constructor, e.g. ``key`` and ``reverse`` for
        :class:`~sds.linear.PriorityQueue`.

    Returns
    -------
    LinearCollection
        A new instance of ``cls``.

    Raises
    ------
    TypeError
        If ``cls`` is not a ``LinearCollection`` subclass, or if
        ``kwargs`` does not match its constructor.

    Examples
    --------
    >>> from sds.linear import PriorityQueue, from_list, to_list
    >>> pq = from_list(PriorityQueue, ["ccc", "a", "bb"], key=len, reverse=True)
    >>> to_list(pq)
    ['ccc', 'bb', 'a']

    Notes
    -----
    Time complexity: n times the cost of ``cls.add()``. That is O(n) for
    ``DoublyLinkedList``, ``CircularLinkedList``, ``Stack`` and ``Deque``,
    but O(n²) for ``LinkedList`` and ``Queue`` (appending walks the chain,
    no tail pointer) and for ``PriorityQueue`` (sorted insertion).
    """
    if not (isinstance(cls, type) and issubclass(cls, LinearCollection)):
        raise TypeError(f"Expected a LinearCollection subclass, got {cls!r}")
    structure = cls(**kwargs)
    for item in items:
        structure.add(item)
    return structure
