"""Core components for Simple Data Structures.

This module provides the fundamental building blocks used across all data structures:
- Node classes for linked structures
- Abstract base classes defining interfaces
- Common exceptions
"""

from .exceptions import (
    EmptyStructureError,
    FullStructureError,
    InvalidOperationError,
)
from .interfaces import Collection, LinearCollection
from .node import DoublyNode, Node

__all__ = [
    "Node",
    "DoublyNode",
    "Collection",
    "LinearCollection",
    "EmptyStructureError",
    "FullStructureError",
    "InvalidOperationError",
]
