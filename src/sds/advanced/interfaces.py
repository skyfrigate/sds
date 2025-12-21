# Copyright 2024-2025, skyfrigate, biface
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

"""Abstract interfaces for advanced data structures.

This module provides abstract base classes that define contracts for
advanced data structures like disjoint sets, probabilistic structures,
and specialized trees.

Classes
-------
AbstractDisjointSet
    Interface for Union-Find / Disjoint Set data structure.
AbstractProbabilisticSet
    Interface for probabilistic membership structures.

Notes
-----
These interfaces ensure consistency across different implementations
and enable polymorphic usage of advanced structures.

See Also
--------
sds.core.interfaces : Core collection interfaces.
sds.advanced.disjoint_set : Concrete disjoint set implementation.
"""

from abc import ABC, abstractmethod
from typing import Any, List, Set

__all__ = ["AbstractDisjointSet", "AbstractProbabilisticSet"]


class AbstractDisjointSet(ABC):
    """Abstract base class for Disjoint Set (Union-Find) data structure.

    A disjoint-set data structure maintains a collection of disjoint sets
    and supports efficient union and find operations. This is fundamental
    for algorithms like Kruskal's MST and cycle detection.

    Notes
    -----
    Implementations should use:
    - Path compression in find() for O(α(n)) amortized complexity
    - Union by rank or size for balanced trees
    - α(n) is the inverse Ackermann function, effectively constant

    See Also
    --------
    DisjointSet : Concrete implementation with optimizations.
    """

    @abstractmethod
    def make_set(self, element: Any) -> None:
        """Create a new set containing only the given element.

        Parameters
        ----------
        element : Any
            Element to create a set for (must be hashable).

        Raises
        ------
        ValueError
            If element already exists in a set.

        Notes
        -----
        Time complexity: O(1)
        """
        pass

    @abstractmethod
    def find(self, element: Any) -> Any:
        """Find the representative of the set containing element.

        Parameters
        ----------
        element : Any
            Element to find the representative for.

        Returns
        -------
        Any
            Representative (root) of the set containing element.

        Raises
        ------
        ValueError
            If element is not in any set.

        Notes
        -----
        Time complexity: O(α(n)) amortized with path compression.
        """
        pass

    @abstractmethod
    def union(self, x: Any, y: Any) -> bool:
        """Unite the sets containing x and y.

        Parameters
        ----------
        x : Any
            Element in first set.
        y : Any
            Element in second set.

        Returns
        -------
        bool
            True if sets were merged (were different), False otherwise.

        Raises
        ------
        ValueError
            If x or y is not in any set.

        Notes
        -----
        Time complexity: O(α(n)) amortized with union by rank.
        """
        pass

    @abstractmethod
    def connected(self, x: Any, y: Any) -> bool:
        """Check if x and y are in the same set.

        Parameters
        ----------
        x : Any
            First element.
        y : Any
            Second element.

        Returns
        -------
        bool
            True if x and y are in the same set.

        Raises
        ------
        ValueError
            If x or y is not in any set.

        Notes
        -----
        Time complexity: O(α(n)) amortized.
        """
        pass

    @abstractmethod
    def get_sets(self) -> List[Set[Any]]:
        """Get all disjoint sets.

        Returns
        -------
        List[Set[Any]]
            List of all disjoint sets.

        Notes
        -----
        Time complexity: O(n)
        """
        pass

    @abstractmethod
    def count_sets(self) -> int:
        """Get the number of disjoint sets.

        Returns
        -------
        int
            Number of disjoint sets.

        Notes
        -----
        Time complexity: O(1)
        """
        pass

    @abstractmethod
    def size(self, element: Any) -> int:
        """Get the size of the set containing element.

        Parameters
        ----------
        element : Any
            Element in the set.

        Returns
        -------
        int
            Number of elements in the set.

        Raises
        ------
        ValueError
            If element is not in any set.

        Notes
        -----
        Time complexity: O(α(n)) amortized.
        """
        pass


class AbstractProbabilisticSet(ABC):
    """Abstract base class for probabilistic set membership structures.

    Probabilistic structures like Bloom Filters trade perfect accuracy
    for space efficiency, allowing false positives but no false negatives.

    Notes
    -----
    These structures are useful when:
    - Space is limited
    - Approximate answers are acceptable
    - False positives can be handled
    - False negatives are unacceptable

    See Also
    --------
    BloomFilter : Space-efficient probabilistic set.
    """

    @abstractmethod
    def add(self, item: Any) -> None:
        """Add an item to the set.

        Parameters
        ----------
        item : Any
            Item to add (must be hashable).

        Notes
        -----
        After adding, contains(item) will always return True.
        """
        pass

    @abstractmethod
    def __contains__(self, item: Any) -> bool:
        """Test if item might be in the set.

        Parameters
        ----------
        item : Any
            Item to test.

        Returns
        -------
        bool
            True if item might be in set (possible false positive).
            False if item is definitely not in set (no false negatives).

        Notes
        -----
        False positives are possible, false negatives are not.
        """
        pass

    @abstractmethod
    def estimated_fill_ratio(self) -> float:
        """Get the estimated fill ratio of the structure.

        Returns
        -------
        float
            Ratio of filled slots (0.0 to 1.0).

        Notes
        -----
        Higher fill ratios increase false positive probability.
        """
        pass
