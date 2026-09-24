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

"""Model access shared by the HMM algorithms (internal)."""

from typing import Callable, List, Sequence, Tuple

from ...probabilistic.interfaces import AbstractHiddenMarkovModel

# (initial(s), transition(s, previous), emission(o, s))
Probabilities = Tuple[
    Callable[[str], float],
    Callable[[str, str], float],
    Callable[[str, str], float],
]


def hmm_accessors(
    hmm: AbstractHiddenMarkovModel, observations: Sequence[str]
) -> Tuple[Tuple[str, ...], List[str], Probabilities]:
    """Validate an observation sequence and expose the model's probabilities.

    Returns the hidden-state domain, the observations as a list, and three
    lookup functions over the model's initial, transition and emission
    factors.

    Raises
    ------
    ValueError
        If the sequence is empty, contains a symbol outside the
        observation domain, or the model is not fully configured.
    """
    sequence = list(observations)
    if not sequence:
        raise ValueError("observations must contain at least one symbol")
    states = hmm.states()
    previous = hmm.previous_states()
    symbols = hmm.observations()
    for symbol in sequence:
        symbols.index(symbol)  # raises ValueError for an unknown symbol
    initial = hmm.initial_distribution()
    transition = hmm.transition_model()
    emission = hmm.emission_model()

    def p_initial(s: str) -> float:
        return initial.value({states: s})

    def p_transition(s: str, r: str) -> float:
        return transition.value({states: s, previous: r})

    def p_emission(o: str, s: str) -> float:
        return emission.value({symbols: o, states: s})

    return states.domain, sequence, (p_initial, p_transition, p_emission)
