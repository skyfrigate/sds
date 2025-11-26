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


class IndexStructureError(DataStructureError):
    """Exception raised when an invalid index is accessed."""

    def __init__(self, message: str = "Index out of range"):
        self.message = message
        super().__init__(self.message)
