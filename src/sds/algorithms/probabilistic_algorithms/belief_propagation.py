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

"""Belief propagation (sum-product) on the factor graph of a model.

The *factor graph* of a model is bipartite: one node per variable, one per
factor, and an edge between a factor and each variable of its scope.
Belief propagation computes the marginal of every variable at once by
passing *messages* along those edges:

.. math::

    \\mu_{x \\to f}(x) = \\prod_{g \\in N(x) \\setminus f} \\mu_{g \\to x}(x)

    \\mu_{f \\to x}(x) = \\sum_{X_f \\setminus x} f(X_f)
                        \\prod_{y \\in N(f) \\setminus x} \\mu_{y \\to f}(y)

    P(x) \\;\\propto\\; \\prod_{f \\in N(x)} \\mu_{f \\to x}(x)

Messages start uniform and are all recomputed at every iteration (the
*flooding* schedule) until no message moves by more than a tolerance.

- On a **tree-shaped** factor graph (no cycle, as in a polytree Bayesian
  network or a chain), the messages settle after at most as many
  iterations as the graph's diameter, and the marginals are **exact**.
- On a graph **with cycles**, the same procedure is *loopy* belief
  propagation: it often converges to good approximations, but the result
  is not exact and convergence is not guaranteed. Use
  :func:`variable_elimination` when an exact answer is required.
"""

import warnings
from typing import Dict, List, Mapping, Optional, Tuple

from ...probabilistic.factor import Factor
from ...probabilistic.interfaces import AbstractGraphicalModel
from ...probabilistic.variable import RandomVariable
from ._tables import Assignment, Table, assignments
from ._validation import check_evidence

__all__ = ["belief_propagation"]

Message = Dict[str, float]


def belief_propagation(
    model: AbstractGraphicalModel,
    evidence: Optional[Mapping[RandomVariable, str]] = None,
    *,
    max_iterations: int = 100,
    tolerance: float = 1e-9,
) -> Dict[RandomVariable, Factor]:
    """Compute the marginal ``P(X | evidence)`` of every variable.

    Parameters
    ----------
    model : AbstractGraphicalModel
        A Bayesian network or a Markov random field, read through
        ``variables()`` and ``factors()`` only.
    evidence : mapping of RandomVariable to str, optional
        Observed states. An observed variable's marginal puts all its mass
        on the observed state.
    max_iterations : int, optional
        Upper bound on the number of message-passing rounds (default 100).
    tolerance : float, optional
        Convergence threshold on the largest change of any message
        between two rounds (default 1e-9).

    Returns
    -------
    dict of RandomVariable to Factor
        For every variable of the model, a one-variable factor holding its
        normalized marginal, in the model's variable order.

    Raises
    ------
    ValueError
        If the evidence names an unknown variable or state, if
        ``max_iterations`` is not positive, or if the evidence has
        probability zero.

    Warns
    -----
    RuntimeWarning
        If the messages have not converged after ``max_iterations`` rounds
        (possible only on a factor graph with cycles). The marginals
        returned are then those of the last round.

    Examples
    --------
    >>> from sds.probabilistic import BayesianNetwork, Factor, RandomVariable
    >>> rain = RandomVariable("Rain", ("yes", "no"))
    >>> wet = RandomVariable("Wet", ("yes", "no"))
    >>> bn = BayesianNetwork()
    >>> for v in (rain, wet):
    ...     bn.add_variable(v)
    >>> bn.add_edge(rain, wet)
    >>> bn.set_cpt(rain, Factor((rain,), {("yes",): 0.2, ("no",): 0.8}))
    >>> bn.set_cpt(wet, Factor((wet, rain), {
    ...     ("yes", "yes"): 0.9, ("no", "yes"): 0.1,
    ...     ("yes", "no"): 0.1, ("no", "no"): 0.9}))
    >>> marginals = belief_propagation(bn, {wet: "yes"})
    >>> round(marginals[rain].value({rain: "yes"}), 4)
    0.6923

    Notes
    -----
    Time complexity: :math:`O(I \\sum_f |f| \\cdot |\\mathrm{scope}(f)|)` for
    :math:`I` rounds, with :math:`|f|` the number of entries of factor
    :math:`f`. Space complexity: one message of the variable's domain size
    per factor-variable pair, in each direction.

    Evidence is applied by *clamping*: each observed variable receives an
    extra unary factor that is 1 on the observed state and 0 elsewhere.
    Messages are normalized after every update, which changes no marginal
    and keeps the numbers in a safe range.
    """
    evidence = dict(evidence or {})
    check_evidence(model, evidence)
    if max_iterations < 1:
        raise ValueError(f"max_iterations must be positive, got {max_iterations}")

    variables = list(model.variables())
    tables: List[Table] = [Table.from_factor(f) for f in model.factors()]
    for variable, observed in evidence.items():
        indicator: Dict[Assignment, float] = {
            (s,): (1.0 if s == observed else 0.0) for s in variable.domain
        }
        tables.append(Table((variable,), indicator))

    # Factor graph adjacency: factor index -> scope, variable -> factor indices.
    factors_of: Dict[RandomVariable, List[int]] = {v: [] for v in variables}
    for index, table in enumerate(tables):
        for variable in table.scope:
            factors_of[variable].append(index)

    to_factor: Dict[Tuple[RandomVariable, int], Message] = {}
    to_variable: Dict[Tuple[int, RandomVariable], Message] = {}
    for index, table in enumerate(tables):
        for variable in table.scope:
            to_factor[(variable, index)] = _uniform(variable)
            to_variable[(index, variable)] = _uniform(variable)

    converged = False
    for _ in range(max_iterations):
        new_to_variable = {
            (index, variable): _factor_message(
                tables[index], variable, index, to_factor
            )
            for (index, variable) in to_variable
        }
        new_to_factor = {
            (variable, index): _variable_message(
                variable, index, factors_of[variable], new_to_variable
            )
            for (variable, index) in to_factor
        }
        change = max(
            [_distance(to_variable[k], new_to_variable[k]) for k in to_variable]
            + [_distance(to_factor[k], new_to_factor[k]) for k in to_factor],
            default=0.0,
        )
        to_variable, to_factor = new_to_variable, new_to_factor
        if change <= tolerance:
            converged = True
            break
    if not converged:
        warnings.warn(
            f"belief_propagation did not converge in {max_iterations} iterations; "
            "the marginals returned are approximate",
            RuntimeWarning,
            stacklevel=2,
        )

    marginals: Dict[RandomVariable, Factor] = {}
    for variable in variables:
        belief = _variable_message(variable, None, factors_of[variable], to_variable)
        marginals[variable] = Factor(
            (variable,), {(state,): belief[state] for state in variable.domain}
        )
    return marginals


def _uniform(variable: RandomVariable) -> Message:
    share = 1.0 / variable.cardinality
    return {state: share for state in variable.domain}


def _normalize(message: Message, variable: RandomVariable) -> Message:
    total = sum(message.values())
    if total <= 0.0:
        raise ValueError(
            f"Belief propagation reached a zero message for '{variable.name}': "
            "the evidence has probability zero under the model"
        )
    return {state: value / total for state, value in message.items()}


def _factor_message(
    table: Table,
    target: RandomVariable,
    index: int,
    to_factor: Dict[Tuple[RandomVariable, int], Message],
) -> Message:
    """Sum out every variable but ``target``, weighting by incoming messages."""
    message = {state: 0.0 for state in target.domain}
    position = table.scope.index(target)
    for key in assignments(table.scope):
        weight = table.values[key]
        if weight == 0.0:
            continue
        for other_position, other in enumerate(table.scope):
            if other_position != position:
                weight *= to_factor[(other, index)][key[other_position]]
        message[key[position]] += weight
    return _normalize(message, target)


def _variable_message(
    variable: RandomVariable,
    exclude: Optional[int],
    factor_indices: List[int],
    to_variable: Dict[Tuple[int, RandomVariable], Message],
) -> Message:
    """Product of incoming factor messages, except the one from ``exclude``.

    With ``exclude=None`` this is the variable's (normalized) belief.
    """
    message = {state: 1.0 for state in variable.domain}
    for index in factor_indices:
        if index != exclude:
            incoming = to_variable[(index, variable)]
            for state in variable.domain:
                message[state] *= incoming[state]
    return _normalize(message, variable)


def _distance(old: Message, new: Message) -> float:
    return max(abs(old[s] - new[s]) for s in old)
