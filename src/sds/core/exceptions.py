"""Custom exceptions for data structures."""


class DataStructureError(Exception):
    """Base exception for all data structure errors."""

    pass


class EmptyStructureError(DataStructureError):
    """Exception raised when attempting to access/remove from an empty structure."""

    def __init__(self, message: str = "Cannot perform operation on empty structure"):
        self.message = message
        super().__init__(self.message)


class FullStructureError(DataStructureError):
    """Exception raised when attempting to add to a full structure."""

    def __init__(self, message: str = "Cannot add to full structure"):
        self.message = message
        super().__init__(self.message)


class InvalidOperationError(DataStructureError):
    """Exception raised when an invalid operation is attempted."""

    def __init__(self, message: str = "Invalid operation"):
        self.message = message
        super().__init__(self.message)


class IndexStructureError(DataStructureError, IndexError):
    """Exception raised when an invalid index is accessed."""

    def __init__(self, message: str = "Index out of range"):
        self.message = message
        super().__init__(self.message)


class ElementNotFoundError(DataStructureError, ValueError):
    """Exception raised when a requested element is not in the structure.

    Covers any item looked up by value or identity: a list item, a tree key,
    a graph node or edge, a model variable or state. Also a ``ValueError``,
    so code catching ``ValueError`` keeps working.
    """

    def __init__(self, message: str = "Element not found in structure"):
        self.message = message
        super().__init__(self.message)


class DuplicateElementError(DataStructureError, ValueError):
    """Exception raised when adding an element the structure already holds.

    Applies to structures that reject duplicates (graph nodes and edges,
    model variables, disjoint sets). A duplicate *inside an argument* is an
    :class:`InvalidParameterError`. Also a ``ValueError``.
    """

    def __init__(self, message: str = "Element already exists in structure"):
        self.message = message
        super().__init__(self.message)


class InvalidParameterError(DataStructureError, ValueError):
    """Exception raised when an argument value is invalid in itself.

    The argument is rejected whatever the state of the structure: a bound
    out of range, an empty input, inconsistent dimensions, evidence with
    probability zero under a model. Also a ``ValueError``.
    """

    def __init__(self, message: str = "Invalid parameter"):
        self.message = message
        super().__init__(self.message)


class StructureTypeError(DataStructureError, TypeError):
    """Exception raised when an argument has the wrong type.

    Raised by explicit type checks on nodes, edges, weights or the structure
    an algorithm expects. Also a ``TypeError``.
    """

    def __init__(self, message: str = "Invalid type for this structure"):
        self.message = message
        super().__init__(self.message)
