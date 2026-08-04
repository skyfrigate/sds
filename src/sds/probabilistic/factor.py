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

"""Factor (potential table) building block for probabilistic graphical models.

This module provides ``Factor``, a non-negative real-valued function defined
over a scope (an ordered tuple) of ``RandomVariable`` instances. A factor is
pure storage plus lookup: it makes no assumption about normalization, so the
same class backs both a Bayesian network's conditional probability tables
(locally normalized) and a Markov random field's potential functions
(generally unnormalized). It plays the same structural role for this module
that ``Edge`` plays for ``sds.graph``.

Classes
-------
Factor
    A potential table mapping joint assignments over its scope to a
    non-negative value.

Examples
--------
>>> from sds.probabilistic.variable import RandomVariable
>>> from sds.probabilistic.factor import Factor
>>> rain = RandomVariable("Rain", ("true", "false"))
>>> sprinkler = RandomVariable("Sprinkler", ("true", "false"))
>>> table = {
...     ("true", "true"): 0.01,
...     ("true", "false"): 0.99,
...     ("false", "true"): 0.4,
...     ("false", "false"): 0.6,
... }
>>> cpt = Factor((rain, sprinkler), table)
>>> cpt.value({rain: "true", sprinkler: "false"})
0.99

Notes
-----
No inference (marginalization, product of factors, normalization by a
partition function) lives here — that belongs to ``sds.algorithms``
per the structures/algorithms separation (GitHub issue #14). ``Factor``
only stores and looks up values.

See Also
--------
sds.probabilistic.variable : RandomVariable, the scope element type.
sds.graph.edge : Structural precedent (``Edge``) for this pattern.
"""

from typing import Dict, Mapping, Tuple

from .variable import RandomVariable

__all__ = ["Factor"]


class Factor:
    """A non-negative real-valued function over a scope of random variables.

    Parameters
    ----------
    scope : tuple of RandomVariable
        Ordered tuple of variables this factor is defined over. The order
        fixes how state-tuples are read in ``table``.
    table : mapping of tuple of str to float
        Maps every joint state assignment (in the order of ``scope``) to a
        non-negative value. Must contain exactly one entry per combination
        of states across ``scope`` (the full Cartesian product).

    Attributes
    ----------
    scope : tuple of RandomVariable
        The variables this factor is defined over.

    Raises
    ------
    ValueError
        If ``scope`` is empty, if ``table`` is missing entries, contains
        unknown keys, or contains a negative value.

    Examples
    --------
    >>> fever = RandomVariable("Fever", ("true", "false"))
    >>> potential = Factor((fever,), {("true",): 0.3, ("false",): 0.7})
    >>> potential.value({fever: "true"})
    0.3

    Notes
    -----
    ``Factor`` deliberately does not check that values sum to 1 — that
    constraint is meaningful for a Bayesian network's CPTs but not for a
    Markov random field's potentials. Normalization checks, if needed,
    belong to the concrete structure that uses the factor (e.g.
    ``BayesianNetwork.set_cpt``), not to ``Factor`` itself.

    See Also
    --------
    RandomVariable : Scope element type.
    """

    __slots__ = ("_scope", "_table")

    def __init__(
        self,
        scope: Tuple[RandomVariable, ...],
        table: Mapping[Tuple[str, ...], float],
    ) -> None:
        if len(scope) == 0:
            raise ValueError("Factor scope must contain at least one variable")

        expected_keys = self._cartesian_product(scope)
        actual_keys = set(table.keys())
        if actual_keys != expected_keys:
            missing = expected_keys - actual_keys
            unknown = actual_keys - expected_keys
            raise ValueError(
                f"Factor table over scope {[v.name for v in scope]} is incomplete "
                f"or invalid (missing={len(missing)}, unknown={len(unknown)})"
            )
        for key, value in table.items():
            if value < 0:
                raise ValueError(
                    f"Factor value for assignment {key} must be non-negative, "
                    f"got {value}"
                )

        self._scope: Tuple[RandomVariable, ...] = tuple(scope)
        self._table: Dict[Tuple[str, ...], float] = dict(table)

    @staticmethod
    def _cartesian_product(
        scope: Tuple[RandomVariable, ...],
    ) -> set[Tuple[str, ...]]:
        """Compute the full set of joint state-tuples over ``scope``."""
        keys: set[Tuple[str, ...]] = {()}
        for variable in scope:
            keys = {key + (state,) for key in keys for state in variable.domain}
        return keys

    @property
    def scope(self) -> Tuple[RandomVariable, ...]:
        """tuple of RandomVariable: The variables this factor is defined over."""
        return self._scope

    def value(self, assignment: Mapping[RandomVariable, str]) -> float:
        """Look up the factor's value for a joint assignment.

        Parameters
        ----------
        assignment : mapping of RandomVariable to str
            Must provide a state for every variable in ``scope`` (extra
            entries for variables outside the scope are ignored).

        Returns
        -------
        float
            The stored value for that assignment.

        Raises
        ------
        KeyError
            If ``assignment`` does not cover every variable in ``scope``.

        Examples
        --------
        >>> potential.value({fever: "false"})  # doctest: +SKIP
        0.7
        """
        key = tuple(assignment[variable] for variable in self._scope)
        return self._table[key]

    def __repr__(self) -> str:
        names = [v.name for v in self._scope]
        return f"Factor(scope={names!r}, entries={len(self._table)})"
