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

"""Working tables for inference, built from factors inside the algorithms.

``Factor`` is a read-only lookup table: it exposes ``scope`` and ``value()``
and deliberately offers no algebra (#84). Inference needs to multiply
tables and sum variables out, so the algorithms of this package first copy
each factor into a private :class:`Table` and do all the arithmetic there.
The result handed back to the caller is again a plain ``Factor``.

This module is internal: nothing in it is part of the public API.
"""

from itertools import product
from typing import Dict, Iterator, Mapping, Optional, Sequence, Tuple

from ...probabilistic.factor import Factor
from ...probabilistic.variable import RandomVariable

Assignment = Tuple[str, ...]


def assignments(scope: Sequence[RandomVariable]) -> Iterator[Assignment]:
    """Yield every joint state tuple over ``scope``, in domain order."""
    return product(*(variable.domain for variable in scope))


class Table:
    """An immutable working copy of a factor: a scope and its values.

    Instances are never modified after construction; every operation
    returns a new table.
    """

    __slots__ = ("scope", "values")

    def __init__(
        self, scope: Tuple[RandomVariable, ...], values: Dict[Assignment, float]
    ) -> None:
        self.scope = scope
        self.values = values

    @classmethod
    def from_factor(cls, factor: Factor) -> "Table":
        """Copy a factor through its public interface."""
        scope = factor.scope
        values = {
            key: factor.value(dict(zip(scope, key))) for key in assignments(scope)
        }
        return cls(scope, values)

    @classmethod
    def unit(cls) -> "Table":
        """The neutral element of the product: empty scope, value 1."""
        return cls((), {(): 1.0})

    def to_factor(self) -> Factor:
        """Return a ``Factor`` holding the same scope and values."""
        return Factor(self.scope, dict(self.values))

    def multiply(self, other: "Table") -> "Table":
        """Pointwise product; the scope is the union of both scopes."""
        extra = tuple(v for v in other.scope if v not in self.scope)
        scope = self.scope + extra
        own = [scope.index(v) for v in self.scope]
        theirs = [scope.index(v) for v in other.scope]
        values: Dict[Assignment, float] = {}
        for key in assignments(scope):
            a = tuple(key[i] for i in own)
            b = tuple(key[i] for i in theirs)
            values[key] = self.values[a] * other.values[b]
        return Table(scope, values)

    def sum_out(self, variable: RandomVariable) -> "Table":
        """Marginalize ``variable`` away by summing over its states."""
        position = self.scope.index(variable)
        scope = self.scope[:position] + self.scope[position + 1 :]
        values: Dict[Assignment, float] = {}
        for key, value in self.values.items():
            reduced = key[:position] + key[position + 1 :]
            values[reduced] = values.get(reduced, 0.0) + value
        return Table(scope, values)

    def reduce(self, evidence: Mapping[RandomVariable, str]) -> "Table":
        """Keep only entries consistent with ``evidence``; drop those variables."""
        observed = [i for i, v in enumerate(self.scope) if v in evidence]
        if not observed:
            return self
        kept = [i for i in range(len(self.scope)) if i not in observed]
        scope = tuple(self.scope[i] for i in kept)
        values: Dict[Assignment, float] = {}
        for key, value in self.values.items():
            if all(key[i] == evidence[self.scope[i]] for i in observed):
                values[tuple(key[i] for i in kept)] = value
        return Table(scope, values)

    def total(self) -> float:
        """Sum of all values."""
        return sum(self.values.values())

    def normalized(self, what: Optional[str] = None) -> "Table":
        """Return a copy scaled so that its values sum to 1.

        Raises
        ------
        ValueError
            If every value is zero (e.g. evidence of probability zero).
        """
        z = self.total()
        if z <= 0.0:
            raise ValueError(
                f"Cannot normalize {what or 'the result'}: total mass is zero "
                "(the evidence has probability zero under the model)"
            )
        return Table(self.scope, {k: v / z for k, v in self.values.items()})

    def reordered(self, scope: Tuple[RandomVariable, ...]) -> "Table":
        """Return the same table with its variables listed in ``scope`` order."""
        if scope == self.scope:
            return self
        positions = [self.scope.index(v) for v in scope]
        values = {
            tuple(key[i] for i in positions): value
            for key, value in self.values.items()
        }
        return Table(scope, values)
