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

"""The forward algorithm: likelihood of an observation sequence.

For a hidden Markov model with hidden states :math:`S_t` and observations
:math:`O_t`, the *forward variable* is the joint probability of the first
``t`` observations and the state at time ``t``:

.. math::

    \\alpha_t(s) = P(o_1, \\dots, o_t,\\; S_t = s)

It obeys a recursion that sums over the previous state instead of over
every one of the :math:`|S|^T` state sequences:

.. math::

    \\alpha_1(s) = \\pi(s)\\, e(o_1 \\mid s) \\qquad
    \\alpha_t(s) = e(o_t \\mid s) \\sum_{r} \\alpha_{t-1}(r)\\, T(s \\mid r)

and the likelihood of the whole sequence is
:math:`P(o_1, \\dots, o_T) = \\sum_s \\alpha_T(s)`.

The raw :math:`\\alpha_t` shrink geometrically with ``t`` and underflow to
zero after a few hundred steps. The implementation therefore rescales
them at every step to sum to one; the rescaled values are exactly the
*filtered* distributions :math:`P(S_t \\mid o_1, \\dots, o_t)`, and the log
of the likelihood is the sum of the logs of the scaling constants.
"""

import math
from typing import Dict, List, Sequence, Tuple

from ...probabilistic.factor import Factor
from ...probabilistic.interfaces import AbstractHiddenMarkovModel
from ._hmm import hmm_accessors

__all__ = ["forward"]


def forward(
    hmm: AbstractHiddenMarkovModel, observations: Sequence[str]
) -> Tuple[float, List[Factor]]:
    """Compute the log-likelihood of ``observations`` and the filtered states.

    Parameters
    ----------
    hmm : AbstractHiddenMarkovModel
        A fully configured hidden Markov model.
    observations : sequence of str
        The observed symbols ``o_1 ... o_T``, each in the observation
        domain.

    Returns
    -------
    log_likelihood : float
        Natural logarithm of ``P(o_1, ..., o_T)``.
    filtered : list of Factor
        For each time step ``t``, a factor over the hidden-state variable
        holding ``P(S_t | o_1, ..., o_t)``.

    Raises
    ------
    ValueError
        If the sequence is empty, contains an unknown symbol, if the model
        is not fully configured, or if the sequence has probability zero
        under the model.

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
    >>> log_p, filtered = forward(hmm, ["yes", "yes"])
    >>> round(filtered[-1].value({weather: "rain"}), 3)
    0.883

    Notes
    -----
    Time complexity: :math:`O(T |S|^2)`. Space complexity:
    :math:`O(T |S|)` for the filtered distributions.

    The likelihood itself is ``math.exp(log_likelihood)``, which may
    underflow to 0.0 for long sequences even though the log stays finite.
    """
    domain, sequence, (p_initial, p_transition, p_emission) = hmm_accessors(
        hmm, observations
    )
    states = hmm.states()

    log_likelihood = 0.0
    filtered: List[Factor] = []
    previous: Dict[str, float] = {}
    for t, symbol in enumerate(sequence):
        if t == 0:
            alpha = {s: p_initial(s) * p_emission(symbol, s) for s in domain}
        else:
            alpha = {
                s: p_emission(symbol, s)
                * sum(previous[r] * p_transition(s, r) for r in domain)
                for s in domain
            }
        scale = sum(alpha.values())
        if scale <= 0.0:
            raise ValueError(
                f"The observation sequence has probability zero under the model "
                f"(no hidden state can emit '{symbol}' at step {t})"
            )
        log_likelihood += math.log(scale)
        previous = {s: value / scale for s, value in alpha.items()}
        filtered.append(Factor((states,), {(s,): previous[s] for s in domain}))
    return log_likelihood, filtered
