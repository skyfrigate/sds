"""Core components for Simple Data Structures.

This module provides the fundamental building blocks used across all data structures:

- Node classes for linked structures
- Abstract base classes defining interfaces
- Common exceptions
"""

from .exceptions import (
    DataStructureError,
    DuplicateElementError,
    ElementNotFoundError,
    EmptyStructureError,
    FullStructureError,
    IndexStructureError,
    InvalidOperationError,
    InvalidParameterError,
    StructureTypeError,
)
from .interfaces import Collection, LinearCollection
from .node import Node

__all__ = [
    # Node
    "Node",
    # Interfaces
    "Collection",
    "LinearCollection",
    # Exceptions
    "DataStructureError",
    "EmptyStructureError",
    "FullStructureError",
    "IndexStructureError",
    "InvalidOperationError",
    "ElementNotFoundError",
    "DuplicateElementError",
    "InvalidParameterError",
    "StructureTypeError",
]
