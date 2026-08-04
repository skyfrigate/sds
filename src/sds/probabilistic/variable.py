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

"""Random variable building block for probabilistic graphical models.

This module provides ``RandomVariable``, the discrete random variable type
shared by every structure in ``sds.probabilistic`` (Bayesian networks,
Markov random fields, hidden Markov models). It plays the same structural
role for this module that ``GraphNode`` plays for ``sds.graph``: a small,
immutable, hashable building block referenced by the container classes.

Classes
-------
RandomVariable
    A named discrete random variable with a finite domain of states.

Examples
--------
>>> from sds.probabilistic.variable import RandomVariable
>>> rain = RandomVariable("Rain", ("true", "false"))
>>> rain.name
'Rain'
>>> rain.cardinality
2
>>> "true" in rain.domain
True

Notes
-----
Only discrete, finite-domain random variables are supported. Continuous
random variables are out of scope for this module (GitHub issue #26).

See Also
--------
sds.probabilistic.factor : Factor / potential table over a scope of variables.
sds.graph.node : Structural precedent (``GraphNode``) for this pattern.
"""

from typing import Tuple

__all__ = ["RandomVariable"]


class RandomVariable:
    """A discrete random variable with a finite domain of states.

    Parameters
    ----------
    name : str
        Unique, human-readable identifier for the variable (e.g. ``"Rain"``).
    domain : tuple of str
        The finite, ordered set of states the variable can take
        (e.g. ``("true", "false")``). Must contain at least two states.

    Attributes
    ----------
    name : str
        The variable's identifier.
    domain : tuple of str
        The variable's possible states, in a fixed order.

    Raises
    ------
    ValueError
        If ``domain`` has fewer than two states, or contains duplicates.

    Examples
    --------
    >>> weather = RandomVariable("Weather", ("sunny", "rainy", "cloudy"))
    >>> weather.cardinality
    3
    >>> weather.index("rainy")
    1

    Notes
    -----
    ``RandomVariable`` uses ``__slots__`` (GitHub issue #16) and is hashable/immutable
    by identity of ``(name, domain)`` so it can be used as a dictionary key
    or set member, mirroring how ``GraphNode`` is used across ``sds.graph``.

    See Also
    --------
    Factor : Potential table defined over a scope of ``RandomVariable``.
    """

    __slots__ = ("_name", "_domain")

    def __init__(self, name: str, domain: Tuple[str, ...]) -> None:
        if len(domain) < 2:
            raise ValueError(
                f"RandomVariable '{name}' domain must have at least 2 states, "
                f"got {len(domain)}"
            )
        if len(set(domain)) != len(domain):
            raise ValueError(f"RandomVariable '{name}' domain contains duplicates")
        self._name = name
        self._domain = tuple(domain)

    @property
    def name(self) -> str:
        """str: The variable's identifier."""
        return self._name

    @property
    def domain(self) -> Tuple[str, ...]:
        """tuple of str: The variable's possible states, in fixed order."""
        return self._domain

    @property
    def cardinality(self) -> int:
        """int: Number of states in the domain (``len(domain)``)."""
        return len(self._domain)

    def index(self, state: str) -> int:
        """Return the position of ``state`` within the domain.

        Parameters
        ----------
        state : str
            A state belonging to ``domain``.

        Returns
        -------
        int
            Zero-based index of ``state`` in ``domain``.

        Raises
        ------
        ValueError
            If ``state`` is not part of the domain.
        """
        try:
            return self._domain.index(state)
        except ValueError as exc:
            raise ValueError(
                f"'{state}' is not a valid state of RandomVariable '{self._name}' "
                f"(domain={self._domain})"
            ) from exc

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RandomVariable):
            return NotImplemented
        return self._name == other._name and self._domain == other._domain

    def __hash__(self) -> int:
        return hash((self._name, self._domain))

    def __repr__(self) -> str:
        return f"RandomVariable(name={self._name!r}, domain={self._domain!r})"
