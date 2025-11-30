"""Linear data structures module.

This module provides implementations of fundamental linear data structures:
- LinkedList: Singly linked list
- DoublyLinkedList: Doubly linked list
- CircularLinkedList: Circular singly linked list
- Stack: LIFO (Last In First Out) structure
- Queue: FIFO (First In First Out) structure
- Deque: Double-ended queue
- PriorityQueue: Queue with priority-based ordering
"""

from .list import CircularLinkedList, DoublyLinkedList, LinkedList
from .node import DoublyNode, SimpleNode
from .queue import Deque, PriorityQueue, Queue
from .stack import Stack

__all__ = [
    "SimpleNode",
    "DoublyNode",
    "LinkedList",
    "DoublyLinkedList",
    "CircularLinkedList",
    "Stack",
    "Queue",
    "Deque",
    "PriorityQueue",
]
