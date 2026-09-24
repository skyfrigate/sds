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

"""The Viterbi algorithm: most likely sequence of hidden states.

Given observations :math:`o_1 \\dots o_T`, Viterbi finds the hidden state
sequence maximizing :math:`P(s_1 \\dots s_T, o_1 \\dots o_T)`. It is the
forward recursion with the sum replaced by a maximum, plus a *back-pointer*
recording which previous state achieved it:

.. math::

    \\delta_1(s) = \\pi(s)\\, e(o_1 \\mid s) \\qquad
    \\delta_t(s) = e(o_t \\mid s) \\max_{r}\\; \\delta_{t-1}(r)\\, T(s \\mid r)

The best final state is :math:`\\arg\\max_s \\delta_T(s)`; following the
back-pointers from it, backwards in time, rebuilds the whole path.

Products of probabilities underflow on long sequences, so the computation
runs on logarithms: products become sums, and a zero probability becomes
:math:`-\\infty`.
"""

import math
from typing import Dict, List, Sequence, Tuple

from ...probabilistic.interfaces import AbstractHiddenMarkovModel
from ._hmm import hmm_accessors

__all__ = ["viterbi"]


def _log(p: float) -> float:
    return math.log(p) if p > 0.0 else -math.inf


def viterbi(
    hmm: AbstractHiddenMarkovModel, observations: Sequence[str]
) -> Tuple[List[str], float]:
    """Return the most likely hidden-state path and its log-probability.

    Parameters
    ----------
    hmm : AbstractHiddenMarkovModel
        A fully configured hidden Markov model.
    observations : sequence of str
        The observed symbols ``o_1 ... o_T``, each in the observation
        domain.

    Returns
    -------
    path : list of str
        The most likely states ``s_1 ... s_T``. When several paths tie, the
        one preferring earlier states of the domain is returned.
    log_probability : float
        Natural logarithm of the joint probability
        ``P(s_1 ... s_T, o_1 ... o_T)`` of that path with the observations,
        the quantity ``hmm.joint(path, observations)`` returns.

    Raises
    ------
    ValueError
        If the sequence is empty, contains an unknown symbol, if the model
        is not fully configured, or if every state path has probability
        zero.

    Examples
    --------
    >>> from sds.probabilistic import Factor, HiddenMarkovModel, RandomVariable
    >>> weather = RandomVariable("Weather", ("rain", "sun"))
    >>> umbrella = RandomVariable("Umbrella", ("yes", "no"))
    >>> hmm = HiddenMarkovModel()
    >>> hmm.set_states(weather)
    >>> hmm.set_observations(umbrella)
    >>> prev = hmm.previous_states()
    >>> hmm.set_initial_distribution(
    ...     Factor((weather,), {("rain",): 0.5, ("sun",): 0.5}))
    >>> hmm.set_transition_model(Factor((weather, prev), {
    ...     ("rain", "rain"): 0.7, ("sun", "rain"): 0.3,
    ...     ("rain", "sun"): 0.3, ("sun", "sun"): 0.7}))
    >>> hmm.set_emission_model(Factor((umbrella, weather), {
    ...     ("yes", "rain"): 0.9, ("no", "rain"): 0.1,
    ...     ("yes", "sun"): 0.2, ("no", "sun"): 0.8}))
    >>> path, log_p = viterbi(hmm, ["yes", "yes", "no", "yes", "yes"])
    >>> path
    ['rain', 'rain', 'sun', 'rain', 'rain']

    Notes
    -----
    Time complexity: :math:`O(T |S|^2)`. Space complexity:
    :math:`O(T |S|)` for the back-pointers.

    The most likely *path* is not the sequence of individually most likely
    states: filtering or smoothing each step separately can yield a
    sequence that is improbable, or even impossible, as a whole.
    """
    domain, sequence, (p_initial, p_transition, p_emission) = hmm_accessors(
        hmm, observations
    )

    delta: Dict[str, float] = {
        s: _log(p_initial(s)) + _log(p_emission(sequence[0], s)) for s in domain
    }
    back: List[Dict[str, str]] = []
    for symbol in sequence[1:]:
        step: Dict[str, str] = {}
        new_delta: Dict[str, float] = {}
        for s in domain:
            best_prev = domain[0]
            best_score = -math.inf
            for r in domain:
                score = delta[r] + _log(p_transition(s, r))
                if score > best_score:  # strict: ties keep the earlier state
                    best_prev, best_score = r, score
            step[s] = best_prev
            new_delta[s] = best_score + _log(p_emission(symbol, s))
        back.append(step)
        delta = new_delta

    last = max(domain, key=lambda s: (delta[s], -domain.index(s)))
    if delta[last] == -math.inf:
        raise ValueError(
            "The observation sequence has probability zero under the model"
        )
    path = [last]
    for step in reversed(back):
        path.append(step[path[-1]])
    path.reverse()
    return path, delta[last]
