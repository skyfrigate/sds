# Copyright 2024-205, skyfrigate, biface
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

"""Segment Tree implementation for range queries.

This module provides a Segment Tree data structure, which efficiently answers
range queries (sum, min, max, etc.) and allows point updates on an array.

Classes
-------
SegmentTree
    Segment tree for efficient range queries and updates.

Examples
--------
Range sum queries:

>>> from sds.tree.segment_tree import SegmentTree
>>> arr = [1, 3, 5, 7, 9, 11]
>>> tree = SegmentTree(arr, operation='sum')
>>> tree.query(1, 3)  # Sum of arr[1:4] = 3+5+7
15
>>> tree.update(1, 10)  # arr[1] = 10
>>> tree.query(1, 3)  # New sum = 10+5+7
22

Range minimum queries:

>>> arr = [5, 2, 8, 1, 9, 3]
>>> tree = SegmentTree(arr, operation='min')
>>> tree.query(0, 3)  # Min of arr[0:4]
1
>>> tree.query(2, 5)  # Min of arr[2:6]
1

Notes
-----
Segment trees are useful for:
- Range sum/min/max queries
- Range updates (with lazy propagation)
- Finding k-th smallest element in a range
- Counting elements in a range

Time Complexity:
- Build: O(n)
- Query: O(log n)
- Update: O(log n)

Space Complexity: O(4n) ≈ O(n)

See Also
--------
sds.tree.binary : Binary tree implementations.
"""

from typing import Any, Callable, List, Optional

from ..core.exceptions import InvalidOperationError

__all__ = ["SegmentTree"]


class SegmentTree:
    """Segment Tree for efficient range queries.

    A segment tree is a binary tree used for storing intervals (segments).
    It allows querying which segments contain a given point efficiently.
    Most commonly used for range queries like sum, min, max on arrays.

    The tree is stored as an array where:
    - Node at index i has children at 2*i+1 and 2*i+2
    - Leaf nodes represent individual array elements
    - Internal nodes represent merged results of their children

    Attributes
    ----------
    size : int
        The size of the underlying array.

    Examples
    --------
    Create a segment tree for range sums:

    >>> arr = [1, 2, 3, 4, 5]
    >>> tree = SegmentTree(arr, operation='sum')
    >>> tree.query(0, 2)  # Sum of arr[0:3] = 1+2+3
    6
    >>> tree.query(2, 4)  # Sum of arr[2:5] = 3+4+5
    12

    Range minimum queries:

    >>> arr = [5, 2, 8, 1, 9]
    >>> tree = SegmentTree(arr, operation='min')
    >>> tree.query(0, 4)  # Min of entire array
    1
    >>> tree.query(0, 2)  # Min of first 3 elements
    2

    Update values:

    >>> arr = [1, 2, 3, 4, 5]
    >>> tree = SegmentTree(arr, operation='sum')
    >>> tree.update(2, 10)  # Change arr[2] from 3 to 10
    >>> tree.query(0, 2)  # New sum = 1+2+10
    13

    Custom operations:

    >>> def gcd_op(a, b):
    ...     import math
    ...     return math.gcd(a, b)
    >>> arr = [12, 18, 24, 30]
    >>> tree = SegmentTree(arr, operation=gcd_op, identity=0)
    >>> tree.query(0, 3)  # GCD of all elements
    6

    Notes
    -----
    The segment tree is built on an array and supports:
    - Range queries in O(log n)
    - Point updates in O(log n)
    - Space complexity O(4n)

    Operations must be associative: op(a, op(b, c)) = op(op(a, b), c)

    See Also
    --------
    sds.tree.binary : Binary tree structures.
    """

    # Type declarations for instance attributes (for static type checkers)
    _operation: Callable[[Any, Any], Any]
    _identity: Any
    _n: int
    _arr: List[Any]
    _tree: List[Any]

    def __init__(
        self,
        arr: List[Any],
        operation: str = "sum",
        identity: Optional[Any] = None,
    ):
        """Initialize a segment tree.

        Parameters
        ----------
        arr : List[Any]
            The underlying array for range queries.
        operation : str or callable, optional
            The operation to perform. Can be:
            - 'sum': Range sum queries
            - 'min': Range minimum queries
            - 'max': Range maximum queries
            - callable: Custom binary operation
            Default is 'sum'.
        identity : Any, optional
            Identity element for the operation.
            - For sum: 0
            - For min: float('inf')
            - For max: float('-inf')
            - For custom: must be provided

        Raises
        ------
        ValueError
            If array is empty or operation is invalid.

        Examples
        --------
        >>> tree = SegmentTree([1, 2, 3, 4], operation='sum')
        >>> tree = SegmentTree([5, 2, 8], operation='min')
        >>> tree = SegmentTree([1, 9, 3], operation='max')
        """
        if not arr:
            raise ValueError("Cannot create segment tree from empty array")

        self._n = len(arr)
        self._arr = arr.copy()

        # Set up operation and identity
        if isinstance(operation, str):
            self._setup_builtin_operation(operation)
        elif callable(operation):
            self._operation = operation
            if identity is None:
                raise ValueError("Identity element required for custom operation")
            self._identity = identity
        else:
            raise ValueError("Operation must be string or callable")

        # Build tree (size = 4*n is safe for any n)
        self._tree: List[Any] = [self._identity] * (4 * self._n)
        self._build(0, 0, self._n - 1)

    def _setup_builtin_operation(self, operation: str) -> None:
        """Set up built-in operations.

        Parameters
        ----------
        operation : str
            Operation name ('sum', 'min', 'max').
        """
        if operation == "sum":
            self._operation = lambda a, b: a + b
            self._identity = 0
        elif operation == "min":
            self._operation = min
            self._identity = float("inf")
        elif operation == "max":
            self._operation = max
            self._identity = float("-inf")
        else:
            raise ValueError(f"Unknown operation: {operation}")

    @property
    def size(self) -> int:
        """Get the size of the underlying array.

        Returns
        -------
        int
            Size of the array.

        Examples
        --------
        >>> tree = SegmentTree([1, 2, 3])
        >>> tree.size
        3
        """
        return self._n

    def _build(self, node: int, start: int, end: int) -> None:
        """Build the segment tree recursively.

        Parameters
        ----------
        node : int
            Current node index in the tree.
        start : int
            Start index of the segment.
        end : int
            End index of the segment.
        """
        if start == end:
            # Leaf node
            self._tree[node] = self._arr[start]
        else:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2

            # Build left and right subtrees
            self._build(left_child, start, mid)
            self._build(right_child, mid + 1, end)

            # Merge results
            self._tree[node] = self._operation(
                self._tree[left_child], self._tree[right_child]
            )

    def query(self, left: int, right: int) -> Any:
        """Query the result for a range.

        Parameters
        ----------
        left : int
            Start index of the range (inclusive).
        right : int
            End index of the range (inclusive).

        Returns
        -------
        Any
            Result of the operation on the range.

        Raises
        ------
        InvalidOperationError
            If range is invalid.

        Examples
        --------
        >>> tree = SegmentTree([1, 2, 3, 4, 5], operation='sum')
        >>> tree.query(0, 2)  # Sum of [1, 2, 3]
        6
        >>> tree.query(2, 4)  # Sum of [3, 4, 5]
        12

        Notes
        -----
        Time complexity: O(log n)
        """
        if left < 0 or right >= self._n or left > right:
            raise InvalidOperationError(
                f"Invalid range: [{left}, {right}] for array of size {self._n}"
            )

        return self._query_recursive(0, 0, self._n - 1, left, right)

    def _query_recursive(
        self, node: int, start: int, end: int, left: int, right: int
    ) -> Any:
        """Recursively query the segment tree.

        Parameters
        ----------
        node : int
            Current node index.
        start : int
            Start of current segment.
        end : int
            End of current segment.
        left : int
            Query range start.
        right : int
            Query range end.

        Returns
        -------
        Any
            Query result for the range.
        """
        # No overlap
        if right < start or left > end:
            return self._identity

        # Complete overlap
        if left <= start and end <= right:
            return self._tree[node]

        # Partial overlap
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2

        left_result = self._query_recursive(left_child, start, mid, left, right)
        right_result = self._query_recursive(right_child, mid + 1, end, left, right)

        return self._operation(left_result, right_result)

    def update(self, index: int, value: Any) -> None:
        """Update a single element in the array.

        Parameters
        ----------
        index : int
            Index of the element to update.
        value : Any
            New value.

        Raises
        ------
        InvalidOperationError
            If index is out of bounds.

        Examples
        --------
        >>> tree = SegmentTree([1, 2, 3, 4], operation='sum')
        >>> tree.query(0, 3)  # Sum = 10
        10
        >>> tree.update(1, 10)  # Change arr[1] from 2 to 10
        >>> tree.query(0, 3)  # New sum = 18
        18

        Notes
        -----
        Time complexity: O(log n)
        """
        if index < 0 or index >= self._n:
            raise InvalidOperationError(
                f"Index {index} out of bounds for array of size {self._n}"
            )

        self._arr[index] = value
        self._update_recursive(0, 0, self._n - 1, index, value)

    def _update_recursive(
        self, node: int, start: int, end: int, index: int, value: Any
    ) -> None:
        """Recursively update the segment tree.

        Parameters
        ----------
        node : int
            Current node index.
        start : int
            Start of current segment.
        end : int
            End of current segment.
        index : int
            Index to update.
        value : Any
            New value.
        """
        if start == end:
            # Leaf node
            self._tree[node] = value
        else:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2

            if index <= mid:
                self._update_recursive(left_child, start, mid, index, value)
            else:
                self._update_recursive(right_child, mid + 1, end, index, value)

            # Update current node
            self._tree[node] = self._operation(
                self._tree[left_child], self._tree[right_child]
            )

    def get(self, index: int) -> Any:
        """Get the value at a specific index.

        Parameters
        ----------
        index : int
            Index to query.

        Returns
        -------
        Any
            Value at the index.

        Raises
        ------
        InvalidOperationError
            If index is out of bounds.

        Examples
        --------
        >>> tree = SegmentTree([1, 2, 3, 4])
        >>> tree.get(2)
        3

        Notes
        -----
        Time complexity: O(1)
        """
        if index < 0 or index >= self._n:
            raise InvalidOperationError(
                f"Index {index} out of bounds for array of size {self._n}"
            )
        return self._arr[index]

    def to_array(self) -> List[Any]:
        """Get the current array representation.

        Returns
        -------
        List[Any]
            Copy of the underlying array.

        Examples
        --------
        >>> tree = SegmentTree([1, 2, 3])
        >>> tree.update(1, 10)
        >>> tree.to_array()
        [1, 10, 3]

        Notes
        -----
        Time complexity: O(n)
        """
        return self._arr.copy()

    def __len__(self) -> int:
        """Return the size of the array.

        Returns
        -------
        int
            Size of the array.

        Examples
        --------
        >>> tree = SegmentTree([1, 2, 3])
        >>> len(tree)
        3
        """
        return self._n

    def __getitem__(self, index: int) -> Any:
        """Get value at index using array notation.

        Parameters
        ----------
        index : int
            Index to access.

        Returns
        -------
        Any
            Value at the index.

        Examples
        --------
        >>> tree = SegmentTree([1, 2, 3])
        >>> tree[1]
        2
        """
        return self.get(index)

    def __setitem__(self, index: int, value: Any) -> None:
        """Update value at index using array notation.

        Parameters
        ----------
        index : int
            Index to update.
        value : Any
            New value.

        Examples
        --------
        >>> tree = SegmentTree([1, 2, 3])
        >>> tree[1] = 10
        >>> tree[1]
        10
        """
        self.update(index, value)

    def __repr__(self) -> str:
        """Return string representation.

        Returns
        -------
        str
            String representation.

        Examples
        --------
        >>> tree = SegmentTree([1, 2, 3])
        >>> repr(tree)
        'SegmentTree(size=3)'
        """
        return f"SegmentTree(size={self._n})"

    def __str__(self) -> str:
        """Return string showing current array.

        Returns
        -------
        str
            String representation.

        Examples
        --------
        >>> tree = SegmentTree([1, 2, 3])
        >>> str(tree)
        'SegmentTree: [1, 2, 3]'
        """
        return f"SegmentTree: {self._arr}"
