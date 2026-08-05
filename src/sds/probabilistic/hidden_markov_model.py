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

"""Hidden Markov model implementation.

This module provides ``HiddenMarkovModel``, a concrete
``AbstractHiddenMarkovModel``. Unlike ``BayesianNetwork`` and
``MarkovRandomField``, it composes no ``sds.graph`` structure: its topology
is fixed (a two-variable chain), not an open graph.

Its three components — initial distribution, transition model, emission
model — are each stored as a ``Factor`` and validated exactly like a
Bayesian network CPT (scope starting with the conditioned variable,
normalized per configuration of the remaining "parent" variable). The
transition model conditions ``states`` on ``previous_states``, a second
variable sharing ``states``'s domain, derived automatically by
``set_states`` (see the interfaces module docstring for why a single
``RandomVariable`` cannot appear twice in one ``Factor.scope``).

No inference lives here: ``joint()`` only multiplies the stored components
together for one fully known sequence — an O(n) structural computation, not
a search over hidden sequences. Computing the Forward algorithm (marginal
likelihood) or Viterbi (most likely hidden sequence) belongs to
``sds.algorithms``.

Classes
-------
HiddenMarkovModel
    Sequential model with fixed states/observations variables and
    initial/transition/emission components.

Examples
--------
>>> from sds.probabilistic import Factor, HiddenMarkovModel, RandomVariable
>>> weather = RandomVariable("Weather", ("sunny", "rainy"))
>>> umbrella = RandomVariable("Umbrella", ("yes", "no"))
>>> hmm = HiddenMarkovModel()
>>> hmm.set_states(weather)
>>> hmm.set_observations(umbrella)
>>> previous = hmm.previous_states()
>>> hmm.set_initial_distribution(
...     Factor((weather,), {("sunny",): 0.6, ("rainy",): 0.4})
... )
>>> hmm.set_transition_model(Factor(
...     (weather, previous),
...     {
...         ("sunny", "sunny"): 0.7, ("rainy", "sunny"): 0.3,
...         ("sunny", "rainy"): 0.4, ("rainy", "rainy"): 0.6,
...     },
... ))
>>> hmm.set_emission_model(Factor(
...     (umbrella, weather),
...     {
...         ("yes", "sunny"): 0.1, ("no", "sunny"): 0.9,
...         ("yes", "rainy"): 0.8, ("no", "rainy"): 0.2,
...     },
... ))
>>> round(hmm.joint(["sunny", "rainy"], ["no", "yes"]), 4)
0.1296

See Also
--------
sds.probabilistic.interfaces.AbstractHiddenMarkovModel : Contract implemented here.
sds.probabilistic.bayesian_network.BayesianNetwork : The CPT-validation
    pattern mirrored here.
"""

import math
from itertools import product
from typing import Any, Dict, Iterator, List, Optional, Sequence, Tuple

from .factor import Factor
from .interfaces import AbstractHiddenMarkovModel
from .variable import RandomVariable

__all__ = ["HiddenMarkovModel"]

_NORMALIZATION_TOLERANCE = 1e-9
_PREVIOUS_SUFFIX = "__prev"


class HiddenMarkovModel(AbstractHiddenMarkovModel):
    """Sequential model with fixed states/observations variables.

    Examples
    --------
    See the module-level docstring for a full worked example.

    Notes
    -----
    Composes no ``sds.graph`` structure — a hidden Markov model's topology
    (a two-variable chain) is fixed, not an open graph to build.

    See Also
    --------
    AbstractHiddenMarkovModel : The interface this class implements.
    """

    __slots__ = (
        "_states",
        "_previous_states",
        "_observations",
        "_initial",
        "_transition",
        "_emission",
    )

    def __init__(self) -> None:
        self._states: Optional[RandomVariable] = None
        self._previous_states: Optional[RandomVariable] = None
        self._observations: Optional[RandomVariable] = None
        self._initial: Optional[Factor] = None
        self._transition: Optional[Factor] = None
        self._emission: Optional[Factor] = None

    # ------------------------------------------------------------------
    # Collection
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        return sum(
            component is not None
            for component in (
                self._states,
                self._observations,
                self._initial,
                self._transition,
                self._emission,
            )
        )

    def is_empty(self) -> bool:
        return len(self) == 0

    def clear(self) -> None:
        self._states = None
        self._previous_states = None
        self._observations = None
        self._initial = None
        self._transition = None
        self._emission = None

    def __iter__(self) -> Iterator[RandomVariable]:
        for variable in (self._states, self._observations):
            if variable is not None:
                yield variable

    def __contains__(self, item: Any) -> bool:
        return isinstance(item, RandomVariable) and item in (
            self._states,
            self._observations,
        )

    # ------------------------------------------------------------------
    # Variables
    # ------------------------------------------------------------------

    def set_states(self, variable: RandomVariable) -> None:
        """See AbstractHiddenMarkovModel.set_states."""
        if self._states is not None:
            raise ValueError("States variable is already set")
        self._states = variable
        self._previous_states = RandomVariable(
            f"{variable.name}{_PREVIOUS_SUFFIX}", variable.domain
        )

    def set_observations(self, variable: RandomVariable) -> None:
        """See AbstractHiddenMarkovModel.set_observations."""
        if self._observations is not None:
            raise ValueError("Observations variable is already set")
        self._observations = variable

    def states(self) -> RandomVariable:
        """See AbstractHiddenMarkovModel.states."""
        if self._states is None:
            raise ValueError("States variable has not been set yet")
        return self._states

    def previous_states(self) -> RandomVariable:
        """See AbstractHiddenMarkovModel.previous_states."""
        if self._previous_states is None:
            raise ValueError("States variable has not been set yet")
        return self._previous_states

    def observations(self) -> RandomVariable:
        """See AbstractHiddenMarkovModel.observations."""
        if self._observations is None:
            raise ValueError("Observations variable has not been set yet")
        return self._observations

    # ------------------------------------------------------------------
    # Components (each validated like a BayesianNetwork CPT)
    # ------------------------------------------------------------------

    def set_initial_distribution(self, factor: Factor) -> None:
        """See AbstractHiddenMarkovModel.set_initial_distribution."""
        states = self.states()
        if factor.scope != (states,):
            raise ValueError(
                f"Initial distribution scope must be exactly ('{states.name}',), "
                f"got {[v.name for v in factor.scope]}"
            )
        self._validate_normalization(states, factor)
        self._initial = factor

    def set_transition_model(self, factor: Factor) -> None:
        """See AbstractHiddenMarkovModel.set_transition_model."""
        states = self.states()
        previous = self.previous_states()
        if factor.scope != (states, previous):
            raise ValueError(
                f"Transition model scope must be exactly "
                f"('{states.name}', '{previous.name}'), "
                f"got {[v.name for v in factor.scope]}"
            )
        self._validate_normalization(states, factor)
        self._transition = factor

    def set_emission_model(self, factor: Factor) -> None:
        """See AbstractHiddenMarkovModel.set_emission_model."""
        observations = self.observations()
        states = self.states()
        if factor.scope != (observations, states):
            raise ValueError(
                f"Emission model scope must be exactly "
                f"('{observations.name}', '{states.name}'), "
                f"got {[v.name for v in factor.scope]}"
            )
        self._validate_normalization(observations, factor)
        self._emission = factor

    @staticmethod
    def _validate_normalization(variable: RandomVariable, factor: Factor) -> None:
        """Check that ``factor`` sums to 1 over ``variable`` for every
        configuration of the remaining scope (mirrors
        BayesianNetwork._validate_normalization: same CPT-shaped
        constraint, applied here to initial/transition/emission)."""
        conditioning_vars: Tuple[RandomVariable, ...] = factor.scope[1:]
        conditioning_domains: List[Tuple[str, ...]] = [
            v.domain for v in conditioning_vars
        ]

        for conditioning_states in product(*conditioning_domains):
            assignment: Dict[RandomVariable, str] = dict(
                zip(conditioning_vars, conditioning_states)
            )
            total = 0.0
            for state in variable.domain:
                assignment[variable] = state
                total += factor.value(assignment)
            if not math.isclose(total, 1.0, abs_tol=_NORMALIZATION_TOLERANCE):
                raise ValueError(
                    f"Factor for '{variable.name}' is not normalized: values "
                    f"for configuration "
                    f"{dict(zip((v.name for v in conditioning_vars), conditioning_states))} "
                    f"sum to {total}, expected 1.0"
                )

    def initial_distribution(self) -> Factor:
        """See AbstractHiddenMarkovModel.initial_distribution."""
        if self._initial is None:
            raise ValueError("Initial distribution has not been set yet")
        return self._initial

    def transition_model(self) -> Factor:
        """See AbstractHiddenMarkovModel.transition_model."""
        if self._transition is None:
            raise ValueError("Transition model has not been set yet")
        return self._transition

    def emission_model(self) -> Factor:
        """See AbstractHiddenMarkovModel.emission_model."""
        if self._emission is None:
            raise ValueError("Emission model has not been set yet")
        return self._emission

    # ------------------------------------------------------------------
    # Joint evaluation
    # ------------------------------------------------------------------

    def joint(
        self,
        states_sequence: Sequence[str],
        observations_sequence: Sequence[str],
    ) -> float:
        """See AbstractHiddenMarkovModel.joint."""
        if len(states_sequence) == 0 or len(observations_sequence) == 0:
            raise ValueError("Sequences must contain at least one time step")
        if len(states_sequence) != len(observations_sequence):
            raise ValueError(
                "states_sequence and observations_sequence must have the "
                f"same length, got {len(states_sequence)} and "
                f"{len(observations_sequence)}"
            )

        states = self.states()
        previous = self.previous_states()
        observations = self.observations()
        initial = self.initial_distribution()
        transition = self.transition_model()
        emission = self.emission_model()

        result = initial.value({states: states_sequence[0]})
        result *= emission.value(
            {observations: observations_sequence[0], states: states_sequence[0]}
        )

        for t in range(1, len(states_sequence)):
            result *= transition.value(
                {states: states_sequence[t], previous: states_sequence[t - 1]}
            )
            result *= emission.value(
                {observations: observations_sequence[t], states: states_sequence[t]}
            )

        return result

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        configured = len(self)
        return (
            f"HiddenMarkovModel(states={self._states!r}, "
            f"observations={self._observations!r}, "
            f"configured={configured}/5)"
        )
